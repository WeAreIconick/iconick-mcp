# Frontend AJAX - Public Facing

## Complete Frontend AJAX Example

### 1. Enqueue Script (Frontend)

```php
function myplugin_enqueue_frontend_scripts() {
    if ( ! is_singular( 'post' ) ) {
        return;  // Only load on single posts
    }
    
    wp_enqueue_script(
        'myplugin-frontend-ajax',
        plugins_url( 'js/frontend-ajax.js', __FILE__ ),
        array( 'jquery' ),
        '1.0.0',
        true
    );
    
    wp_localize_script( 'myplugin-frontend-ajax', 'frontendAjax', array(
        'ajaxurl' => admin_url( 'admin-ajax.php' ),
        'nonce'   => wp_create_nonce( 'frontend_nonce' ),
        'post_id' => get_the_ID()
    ));
}
add_action( 'wp_enqueue_scripts', 'myplugin_enqueue_frontend_scripts' );
```

### 2. JavaScript (No jQuery)

```javascript
// frontend-ajax.js (Vanilla JavaScript)
document.addEventListener('DOMContentLoaded', function() {
    
    const form = document.getElementById('ajax-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            formData.append('action', 'submit_form');
            formData.append('nonce', frontendAjax.nonce);
            formData.append('post_id', frontendAjax.post_id);
            formData.append('name', document.getElementById('name').value);
            formData.append('email', document.getElementById('email').value);
            
            // Show loading
            const button = form.querySelector('button[type="submit"]');
            button.disabled = true;
            button.textContent = 'Sending...';
            
            fetch(frontendAjax.ajaxurl, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.data.message);
                    form.reset();
                } else {
                    alert('Error: ' + data.data);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred');
            })
            .finally(() => {
                button.disabled = false;
                button.textContent = 'Submit';
            });
        });
    }
    
});
```

### 3. PHP AJAX Handler (Public)

```php
// Register for logged-in users
add_action( 'wp_ajax_submit_form', 'handle_form_submission' );

// Register for non-logged-in users
add_action( 'wp_ajax_nopriv_submit_form', 'handle_form_submission' );

function handle_form_submission() {
    // Verify nonce
    check_ajax_referer( 'frontend_nonce', 'nonce' );
    
    // Get data
    $post_id = isset( $_POST['post_id'] ) ? absint( $_POST['post_id'] ) : 0;
    $name = isset( $_POST['name'] ) ? sanitize_text_field( $_POST['name'] ) : '';
    $email = isset( $_POST['email'] ) ? sanitize_email( $_POST['email'] ) : '';
    
    // Validate
    if ( empty( $name ) || empty( $email ) ) {
        wp_send_json_error( 'All fields are required' );
    }
    
    if ( ! is_email( $email ) ) {
        wp_send_json_error( 'Invalid email address' );
    }
    
    // Process (save to database, send email, etc.)
    $comment_data = array(
        'comment_post_ID' => $post_id,
        'comment_author' => $name,
        'comment_author_email' => $email,
        'comment_content' => 'Submitted via AJAX',
        'comment_type' => 'ajax_submission'
    );
    
    $comment_id = wp_insert_comment( $comment_data );
    
    if ( $comment_id ) {
        wp_send_json_success( array(
            'message' => 'Thank you! Your submission was received.',
            'comment_id' => $comment_id
        ));
    } else {
        wp_send_json_error( 'Failed to save submission' );
    }
}
```

## Load More Posts Pattern

### JavaScript

```javascript
jQuery(document).ready(function($) {
    
    var page = 2;  // Start from page 2
    var loading = false;
    
    $('#load-more').on('click', function(e) {
        e.preventDefault();
        
        if (loading) return;
        loading = true;
        
        var button = $(this);
        button.text('Loading...').prop('disabled', true);
        
        $.ajax({
            url: frontendAjax.ajaxurl,
            type: 'POST',
            data: {
                action: 'load_more_posts',
                nonce: frontendAjax.nonce,
                page: page,
                category: frontendAjax.category
            },
            success: function(response) {
                if (response.success) {
                    $('#posts-container').append(response.data.html);
                    page++;
                    
                    if (!response.data.has_more) {
                        button.hide();
                    }
                } else {
                    alert('No more posts');
                }
            },
            complete: function() {
                loading = false;
                button.text('Load More').prop('disabled', false);
            }
        });
    });
    
});
```

### PHP Handler

```php
add_action( 'wp_ajax_load_more_posts', 'load_more_posts_ajax' );
add_action( 'wp_ajax_nopriv_load_more_posts', 'load_more_posts_ajax' );

function load_more_posts_ajax() {
    check_ajax_referer( 'frontend_nonce', 'nonce' );
    
    $page = isset( $_POST['page'] ) ? absint( $_POST['page'] ) : 1;
    $category = isset( $_POST['category'] ) ? absint( $_POST['category'] ) : 0;
    
    $args = array(
        'post_type' => 'post',
        'posts_per_page' => 6,
        'paged' => $page
    );
    
    if ( $category > 0 ) {
        $args['cat'] = $category;
    }
    
    $query = new WP_Query( $args );
    
    if ( $query->have_posts() ) {
        ob_start();
        
        while ( $query->have_posts() ) {
            $query->the_post();
            get_template_part( 'template-parts/content', 'excerpt' );
        }
        
        $html = ob_get_clean();
        wp_reset_postdata();
        
        wp_send_json_success( array(
            'html' => $html,
            'has_more' => $page < $query->max_num_pages
        ));
    } else {
        wp_send_json_error( 'No posts found' );
    }
}
```

## Autocomplete Search

### JavaScript

```javascript
$('#search-input').on('keyup', function() {
    var searchTerm = $(this).val();
    
    if (searchTerm.length < 3) {
        $('#search-results').empty();
        return;
    }
    
    $.ajax({
        url: frontendAjax.ajaxurl,
        type: 'POST',
        data: {
            action: 'search_posts',
            nonce: frontendAjax.nonce,
            term: searchTerm
        },
        success: function(response) {
            if (response.success) {
                displayResults(response.data);
            }
        }
    });
});

function displayResults(posts) {
    var html = '<ul>';
    posts.forEach(function(post) {
        html += '<li><a href="' + post.url + '">' + post.title + '</a></li>';
    });
    html += '</ul>';
    $('#search-results').html(html);
}
```

### PHP Handler

```php
add_action( 'wp_ajax_search_posts', 'ajax_search_posts' );
add_action( 'wp_ajax_nopriv_search_posts', 'ajax_search_posts' );

function ajax_search_posts() {
    check_ajax_referer( 'frontend_nonce', 'nonce' );
    
    $search_term = isset( $_POST['term'] ) ? sanitize_text_field( $_POST['term'] ) : '';
    
    if ( strlen( $search_term ) < 3 ) {
        wp_send_json_error( 'Search term too short' );
    }
    
    $args = array(
        's' => $search_term,
        'post_type' => 'post',
        'posts_per_page' => 10
    );
    
    $query = new WP_Query( $args );
    $results = array();
    
    if ( $query->have_posts() ) {
        while ( $query->have_posts() ) {
            $query->the_post();
            $results[] = array(
                'title' => get_the_title(),
                'url' => get_permalink(),
                'excerpt' => get_the_excerpt()
            );
        }
        wp_reset_postdata();
    }
    
    wp_send_json_success( $results );
}
```

## Best Practices

1. **Use wp_ajax_nopriv_** for public AJAX
2. **Throttle/debounce** rapid requests (search, etc.)
3. **Validate on both sides** - JavaScript AND PHP
4. **Use wp_send_json_*** - Consistent response format
5. **Handle errors gracefully** - Show user-friendly messages
6. **Load conditionally** - Only on pages that need AJAX
7. **Clean up event listeners** - Prevent memory leaks

