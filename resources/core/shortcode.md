# WordPress Shortcode API

Shortcodes provide a way to add dynamic content to posts and pages using simple tags.

## Basic Shortcode Registration

```php
// Register a simple shortcode
add_shortcode( 'my_shortcode', 'my_shortcode_callback' );

function my_shortcode_callback( $atts, $content = null ) {
    // Default attributes
    $atts = shortcode_atts( array(
        'title' => 'Default Title',
        'color' => 'blue',
        'size' => 'medium'
    ), $atts, 'my_shortcode' );
    
    $output = '<div class="my-shortcode" style="color: ' . esc_attr( $atts['color'] ) . '">';
    $output .= '<h3>' . esc_html( $atts['title'] ) . '</h3>';
    
    if ( $content ) {
        $output .= '<div class="shortcode-content">' . do_shortcode( $content ) . '</div>';
    }
    
    $output .= '</div>';
    
    return $output;
}
```

## Usage Examples

```php
// Simple shortcode
[my_shortcode]

// Shortcode with attributes
[my_shortcode title="My Custom Title" color="red" size="large"]

// Shortcode with content (enclosing)
[my_shortcode title="Box Title"]This is the content inside the shortcode.[/my_shortcode]
```

## Advanced Shortcode Features

### Attribute Validation and Sanitization

```php
function advanced_shortcode_callback( $atts, $content = null ) {
    // Validate and sanitize attributes
    $atts = shortcode_atts( array(
        'post_id' => 0,
        'show_title' => true,
        'limit' => 5
    ), $atts, 'advanced_shortcode' );
    
    // Validate post_id
    if ( ! is_numeric( $atts['post_id'] ) || $atts['post_id'] <= 0 ) {
        return '<p class="shortcode-error">Invalid post ID provided.</p>';
    }
    
    // Sanitize boolean
    $show_title = rest_sanitize_boolean( $atts['show_title'] );
    
    // Sanitize limit
    $limit = max( 1, min( 50, intval( $atts['limit'] ) ) );
    
    // Get post
    $post = get_post( $atts['post_id'] );
    if ( ! $post ) {
        return '<p class="shortcode-error">Post not found.</p>';
    }
    
    $output = '<div class="advanced-shortcode">';
    
    if ( $show_title ) {
        $output .= '<h3>' . esc_html( $post->post_title ) . '</h3>';
    }
    
    $output .= '<div class="post-content">' . wp_kses_post( $post->post_content ) . '</div>';
    $output .= '</div>';
    
    return $output;
}
```

### Nested Shortcodes

```php
function container_shortcode( $atts, $content = null ) {
    $atts = shortcode_atts( array(
        'class' => 'container',
        'style' => ''
    ), $atts, 'container' );
    
    $output = '<div class="' . esc_attr( $atts['class'] ) . '"';
    
    if ( $atts['style'] ) {
        $output .= ' style="' . esc_attr( $atts['style'] ) . '"';
    }
    
    $output .= '>';
    
    if ( $content ) {
        $output .= do_shortcode( $content );
    }
    
    $output .= '</div>';
    
    return $output;
}

function item_shortcode( $atts, $content = null ) {
    $atts = shortcode_atts( array(
        'title' => '',
        'icon' => ''
    ), $atts, 'item' );
    
    $output = '<div class="item">';
    
    if ( $atts['title'] ) {
        $output .= '<h4>' . esc_html( $atts['title'] ) . '</h4>';
    }
    
    if ( $atts['icon'] ) {
        $output .= '<span class="icon">' . esc_html( $atts['icon'] ) . '</span>';
    }
    
    if ( $content ) {
        $output .= '<div class="item-content">' . do_shortcode( $content ) . '</div>';
    }
    
    $output .= '</div>';
    
    return $output;
}

// Register both shortcodes
add_shortcode( 'container', 'container_shortcode' );
add_shortcode( 'item', 'item_shortcode' );

// Usage:
// [container class="feature-grid"]
// [item title="Feature 1" icon="★"]Description here[/item]
// [item title="Feature 2" icon="★"]Another description[/item]
// [/container]
```

### Shortcode with Database Queries

```php
function recent_posts_shortcode( $atts ) {
    $atts = shortcode_atts( array(
        'limit' => 5,
        'category' => '',
        'show_excerpt' => true,
        'show_thumbnail' => true
    ), $atts, 'recent_posts' );
    
    // Build query args
    $query_args = array(
        'posts_per_page' => max( 1, min( 20, intval( $atts['limit'] ) ) ),
        'post_status' => 'publish',
        'orderby' => 'date',
        'order' => 'DESC'
    );
    
    if ( $atts['category'] ) {
        $query_args['category_name'] = sanitize_text_field( $atts['category'] );
    }
    
    $posts = get_posts( $query_args );
    
    if ( empty( $posts ) ) {
        return '<p class="no-posts">No posts found.</p>';
    }
    
    $output = '<div class="recent-posts-shortcode">';
    $output .= '<ul class="posts-list">';
    
    foreach ( $posts as $post ) {
        $output .= '<li class="post-item">';
        
        // Thumbnail
        if ( $atts['show_thumbnail'] && has_post_thumbnail( $post->ID ) ) {
            $thumbnail = get_the_post_thumbnail( $post->ID, 'thumbnail' );
            $output .= '<div class="post-thumbnail">' . $thumbnail . '</div>';
        }
        
        // Title
        $output .= '<h4 class="post-title">';
        $output .= '<a href="' . get_permalink( $post->ID ) . '">';
        $output .= esc_html( $post->post_title );
        $output .= '</a></h4>';
        
        // Excerpt
        if ( $atts['show_excerpt'] ) {
            $excerpt = has_excerpt( $post->ID ) ? 
                get_the_excerpt( $post->ID ) : 
                wp_trim_words( $post->post_content, 20 );
            $output .= '<div class="post-excerpt">' . wp_kses_post( $excerpt ) . '</div>';
        }
        
        $output .= '</li>';
    }
    
    $output .= '</ul></div>';
    
    wp_reset_postdata();
    
    return $output;
}

add_shortcode( 'recent_posts', 'recent_posts_shortcode' );
```

## Security Considerations

### Input Sanitization

```php
function secure_shortcode_callback( $atts, $content = null ) {
    $atts = shortcode_atts( array(
        'url' => '',
        'text' => 'Click here',
        'target' => '_self'
    ), $atts, 'secure_shortcode' );
    
    // Validate URL
    if ( ! empty( $atts['url'] ) ) {
        $atts['url'] = esc_url( $atts['url'] );
        
        // Only allow http/https URLs
        if ( ! wp_http_validate_url( $atts['url'] ) ) {
            return '<p class="shortcode-error">Invalid URL provided.</p>';
        }
    }
    
    // Sanitize text
    $atts['text'] = sanitize_text_field( $atts['text'] );
    
    // Validate target
    $allowed_targets = array( '_self', '_blank', '_parent', '_top' );
    if ( ! in_array( $atts['target'], $allowed_targets ) ) {
        $atts['target'] = '_self';
    }
    
    // Sanitize content if present
    if ( $content ) {
        $content = wp_kses_post( $content );
    }
    
    $output = '<a href="' . $atts['url'] . '" target="' . esc_attr( $atts['target'] ) . '">';
    $output .= esc_html( $atts['text'] );
    $output .= '</a>';
    
    return $output;
}
```

### Capability Checks

```php
function admin_only_shortcode( $atts, $content = null ) {
    // Check if user has required capability
    if ( ! current_user_can( 'manage_options' ) ) {
        return '<p class="shortcode-error">You do not have permission to view this content.</p>';
    }
    
    $atts = shortcode_atts( array(
        'info' => 'admin'
    ), $atts, 'admin_only' );
    
    $output = '<div class="admin-content">';
    $output .= '<p>This content is only visible to administrators.</p>';
    
    if ( $content ) {
        $output .= '<div class="admin-shortcode-content">' . wp_kses_post( $content ) . '</div>';
    }
    
    $output .= '</div>';
    
    return $output;
}

add_shortcode( 'admin_only', 'admin_only_shortcode' );
```

## Shortcode UI Integration

### Adding to TinyMCE

```php
// Add shortcode button to editor
function add_shortcode_button() {
    if ( ! current_user_can( 'edit_posts' ) && ! current_user_can( 'edit_pages' ) ) {
        return;
    }
    
    if ( get_user_option( 'rich_editing' ) == 'true' ) {
        add_filter( 'mce_external_plugins', 'add_shortcode_plugin' );
        add_filter( 'mce_buttons', 'register_shortcode_button' );
    }
}
add_action( 'init', 'add_shortcode_button' );

function register_shortcode_button( $buttons ) {
    array_push( $buttons, 'separator', 'my_shortcode' );
    return $buttons;
}

function add_shortcode_plugin( $plugin_array ) {
    $plugin_array['my_shortcode'] = plugins_url( 'js/shortcode-button.js', __FILE__ );
    return $plugin_array;
}
```

### Shortcode JavaScript

```javascript
// shortcode-button.js
(function() {
    tinymce.PluginManager.add('my_shortcode', function(editor, url) {
        editor.addButton('my_shortcode', {
            title: 'Insert My Shortcode',
            icon: 'icon dashicons-admin-tools',
            onclick: function() {
                editor.window.open({
                    title: 'Insert Shortcode',
                    body: [
                        {
                            type: 'textbox',
                            name: 'title',
                            label: 'Title'
                        },
                        {
                            type: 'listbox',
                            name: 'color',
                            label: 'Color',
                            values: [
                                {text: 'Blue', value: 'blue'},
                                {text: 'Red', value: 'red'},
                                {text: 'Green', value: 'green'}
                            ]
                        }
                    ],
                    onsubmit: function(e) {
                        var title = e.data.title;
                        var color = e.data.color;
                        
                        var shortcode = '[my_shortcode title="' + title + '" color="' + color + '"]';
                        editor.insertContent(shortcode);
                    }
                });
            }
        });
    });
})();
```

## Best Practices

### Performance

```php
// Cache shortcode output when possible
function cached_shortcode_callback( $atts ) {
    $atts = shortcode_atts( array(
        'cache_time' => 3600,
        'data' => ''
    ), $atts, 'cached_shortcode' );
    
    // Create cache key
    $cache_key = 'shortcode_' . md5( serialize( $atts ) );
    
    // Try to get cached output
    $output = get_transient( $cache_key );
    
    if ( false === $output ) {
        // Generate output (expensive operation)
        $output = generate_expensive_output( $atts['data'] );
        
        // Cache the output
        set_transient( $cache_key, $output, intval( $atts['cache_time'] ) );
    }
    
    return $output;
}
```

### Accessibility

```php
function accessible_shortcode_callback( $atts, $content = null ) {
    $atts = shortcode_atts( array(
        'title' => '',
        'aria_label' => ''
    ), $atts, 'accessible_shortcode' );
    
    $output = '<div class="accessible-shortcode"';
    
    if ( $atts['aria_label'] ) {
        $output .= ' aria-label="' . esc_attr( $atts['aria_label'] ) . '"';
    }
    
    $output .= '>';
    
    if ( $atts['title'] ) {
        $output .= '<h3>' . esc_html( $atts['title'] ) . '</h3>';
    }
    
    if ( $content ) {
        $output .= '<div class="shortcode-content">' . wp_kses_post( $content ) . '</div>';
    }
    
    $output .= '</div>';
    
    return $output;
}
```

## Common Patterns

### Contact Form Shortcode

```php
function contact_form_shortcode( $atts ) {
    $atts = shortcode_atts( array(
        'email' => get_option( 'admin_email' ),
        'subject' => 'Contact Form Submission'
    ), $atts, 'contact_form' );
    
    $output = '<form class="contact-form-shortcode" method="post" action="">';
    $output .= wp_nonce_field( 'contact_form_submit', 'contact_form_nonce', true, false );
    
    $output .= '<p><label for="contact_name">Name:</label>';
    $output .= '<input type="text" id="contact_name" name="contact_name" required /></p>';
    
    $output .= '<p><label for="contact_email">Email:</label>';
    $output .= '<input type="email" id="contact_email" name="contact_email" required /></p>';
    
    $output .= '<p><label for="contact_message">Message:</label>';
    $output .= '<textarea id="contact_message" name="contact_message" required></textarea></p>';
    
    $output .= '<p><input type="submit" name="contact_form_submit" value="Send Message" /></p>';
    $output .= '</form>';
    
    // Handle form submission
    if ( isset( $_POST['contact_form_submit'] ) && wp_verify_nonce( $_POST['contact_form_nonce'], 'contact_form_submit' ) ) {
        $name = sanitize_text_field( $_POST['contact_name'] );
        $email = sanitize_email( $_POST['contact_email'] );
        $message = sanitize_textarea_field( $_POST['contact_message'] );
        
        $headers = array( 'Content-Type: text/html; charset=UTF-8' );
        $subject = $atts['subject'];
        $body = "<p>Name: $name</p><p>Email: $email</p><p>Message: $message</p>";
        
        if ( wp_mail( $atts['email'], $subject, $body, $headers ) ) {
            $output .= '<div class="contact-form-success">Thank you for your message!</div>';
        } else {
            $output .= '<div class="contact-form-error">Sorry, there was an error sending your message.</div>';
        }
    }
    
    return $output;
}

add_shortcode( 'contact_form', 'contact_form_shortcode' );
```

## Official Documentation

https://developer.wordpress.org/plugins/shortcodes/
https://developer.wordpress.org/reference/functions/add_shortcode/
https://developer.wordpress.org/reference/functions/shortcode_atts/
https://developer.wordpress.org/reference/functions/do_shortcode/
