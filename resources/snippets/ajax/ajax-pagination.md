# AJAX Pagination

```php
// JavaScript
var currentPage = 1;

jQuery('#load-more-button').on('click', function(e) {
    e.preventDefault();
    currentPage++;
    
    jQuery.ajax({
        url: myAjax.ajaxurl,
        type: 'POST',
        data: {
            action: 'load_more_posts',
            nonce: myAjax.nonce,
            page: currentPage,
            category: myAjax.category
        },
        beforeSend: function() {
            jQuery('#load-more-button').text('Loading...');
        },
        success: function(response) {
            if (response.success) {
                jQuery('#posts-container').append(response.data.html);
                
                if (!response.data.has_more) {
                    jQuery('#load-more-button').hide();
                }
            }
        },
        complete: function() {
            jQuery('#load-more-button').text('Load More');
        }
    });
});

// PHP Handler
add_action( 'wp_ajax_load_more_posts', 'handle_load_more' );
add_action( 'wp_ajax_nopriv_load_more_posts', 'handle_load_more' );

function handle_load_more() {
    check_ajax_referer( 'load_more_nonce', 'nonce' );
    
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
            get_template_part( 'template-parts/content', 'grid' );
        }
        
        $html = ob_get_clean();
        wp_reset_postdata();
        
        wp_send_json_success( array(
            'html' => $html,
            'has_more' => $page < $query->max_num_pages,
            'current_page' => $page,
            'max_pages' => $query->max_num_pages
        ));
    } else {
        wp_send_json_error( 'No more posts' );
    }
}
```
