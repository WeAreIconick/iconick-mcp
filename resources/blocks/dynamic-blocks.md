# WordPress Dynamic Blocks

Dynamic blocks render content on the server-side, perfect for data that changes frequently or requires server processing.

## Server-Side Rendering

### Basic Dynamic Block

```php
// PHP: Register dynamic block
function register_dynamic_block() {
    register_block_type( 'my-plugin/dynamic-block', array(
        'attributes' => array(
            'post_id' => array(
                'type' => 'number',
                'default' => 0
            ),
            'show_title' => array(
                'type' => 'boolean',
                'default' => true
            ),
            'limit' => array(
                'type' => 'number',
                'default' => 5
            )
        ),
        'render_callback' => 'render_dynamic_block'
    ) );
}
add_action( 'init', 'register_dynamic_block' );

// PHP: Render callback
function render_dynamic_block( $attributes, $content ) {
    $post_id = $attributes['post_id'];
    $show_title = $attributes['show_title'];
    $limit = $attributes['limit'];
    
    // Validate inputs
    if ( $post_id <= 0 ) {
        return '<p class="block-error">Invalid post ID provided.</p>';
    }
    
    $limit = max( 1, min( 20, intval( $limit ) ) );
    
    // Query posts
    $posts = get_posts( array(
        'posts_per_page' => $limit,
        'post_status' => 'publish',
        'exclude' => array( $post_id )
    ) );
    
    if ( empty( $posts ) ) {
        return '<p class="no-posts">No posts found.</p>';
    }
    
    ob_start();
    ?>
    <div class="dynamic-posts-block">
        <?php if ( $show_title ) : ?>
            <h3 class="block-title">Related Posts</h3>
        <?php endif; ?>
        
        <ul class="posts-list">
            <?php foreach ( $posts as $post ) : setup_postdata( $post ); ?>
                <li class="post-item">
                    <h4 class="post-title">
                        <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                    </h4>
                    <div class="post-excerpt">
                        <?php the_excerpt(); ?>
                    </div>
                    <div class="post-meta">
                        <span class="post-date"><?php the_date(); ?></span>
                        <span class="post-author">by <?php the_author(); ?></span>
                    </div>
                </li>
            <?php endforeach; wp_reset_postdata(); ?>
        </ul>
    </div>
    <?php
    
    return ob_get_clean();
}
```

### JavaScript Dynamic Block

```javascript
// JavaScript: Block registration
registerBlockType('my-plugin/dynamic-block', {
    title: 'Dynamic Posts Block',
    icon: 'admin-post',
    category: 'widgets',
    
    attributes: {
        post_id: {
            type: 'number',
            default: 0
        },
        show_title: {
            type: 'boolean',
            default: true
        },
        limit: {
            type: 'number',
            default: 5
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { post_id, show_title, limit } = attributes;
        
        return (
            <div className="dynamic-block-editor">
                <h3>Dynamic Posts Block</h3>
                <p>This block will display posts dynamically on the frontend.</p>
                
                <div className="block-controls">
                    <TextControl
                        label="Post ID (0 for current post)"
                        type="number"
                        value={post_id}
                        onChange={(value) => setAttributes({ post_id: parseInt(value) || 0 })}
                    />
                    
                    <ToggleControl
                        label="Show Title"
                        checked={show_title}
                        onChange={(value) => setAttributes({ show_title: value })}
                    />
                    
                    <RangeControl
                        label="Number of Posts"
                        value={limit}
                        onChange={(value) => setAttributes({ limit: value })}
                        min={1}
                        max={20}
                    />
                </div>
                
                <div className="block-preview">
                    <p>Preview: Will show {limit} posts</p>
                    {show_title && <p>Title will be displayed</p>}
                </div>
            </div>
        );
    },
    
    save: () => {
        return null; // Dynamic blocks return null
    }
});
```

## Advanced Dynamic Block Patterns

### AJAX-Powered Dynamic Block

```php
// PHP: AJAX handler for dynamic content
function handle_dynamic_block_ajax() {
    // Verify nonce
    if ( ! wp_verify_nonce( $_POST['nonce'], 'dynamic_block_nonce' ) ) {
        wp_die( 'Security check failed' );
    }
    
    $attributes = json_decode( stripslashes( $_POST['attributes'] ), true );
    $response = render_dynamic_block( $attributes, '' );
    
    wp_send_json_success( array(
        'html' => $response,
        'timestamp' => current_time( 'timestamp' )
    ) );
}
add_action( 'wp_ajax_dynamic_block_content', 'handle_dynamic_block_ajax' );
add_action( 'wp_ajax_nopriv_dynamic_block_content', 'handle_dynamic_block_ajax' );

// JavaScript: AJAX-powered block
registerBlockType('my-plugin/ajax-dynamic-block', {
    edit: ({ attributes, setAttributes }) => {
        const [loading, setLoading] = useState(false);
        const [previewHtml, setPreviewHtml] = useState('');
        
        const loadPreview = async () => {
            setLoading(true);
            
            try {
                const response = await fetch(ajaxurl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        action: 'dynamic_block_content',
                        nonce: wp.data.select('core/editor').getCurrentPost().meta.dynamic_block_nonce,
                        attributes: JSON.stringify(attributes)
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    setPreviewHtml(data.data.html);
                }
            } catch (error) {
                console.error('Error loading preview:', error);
            } finally {
                setLoading(false);
            }
        };
        
        return (
            <div className="ajax-dynamic-block">
                <InspectorControls>
                    <PanelBody title="Settings">
                        <TextControl
                            label="Search Term"
                            value={attributes.search_term}
                            onChange={(value) => setAttributes({ search_term: value })}
                        />
                        <Button onClick={loadPreview} isBusy={loading}>
                            Load Preview
                        </Button>
                    </PanelBody>
                </InspectorControls>
                
                <div className="block-preview">
                    {loading ? (
                        <p>Loading preview...</p>
                    ) : previewHtml ? (
                        <div dangerouslySetInnerHTML={{ __html: previewHtml }} />
                    ) : (
                        <p>Click "Load Preview" to see content</p>
                    )}
                </div>
            </div>
        );
    },
    
    save: () => null
});
```

### Cached Dynamic Block

```php
// PHP: Cached dynamic block with cache invalidation
function render_cached_dynamic_block( $attributes, $content ) {
    $cache_key = 'dynamic_block_' . md5( serialize( $attributes ) );
    $cache_time = 3600; // 1 hour
    
    // Try to get cached content
    $cached_content = get_transient( $cache_key );
    
    if ( false === $cached_content ) {
        // Generate fresh content
        $cached_content = generate_dynamic_content( $attributes );
        
        // Cache the content
        set_transient( $cache_key, $cached_content, $cache_time );
    }
    
    return $cached_content;
}

function generate_dynamic_content( $attributes ) {
    $post_type = $attributes['post_type'] ?? 'post';
    $limit = $attributes['limit'] ?? 5;
    
    $posts = get_posts( array(
        'post_type' => $post_type,
        'posts_per_page' => $limit,
        'post_status' => 'publish',
        'meta_key' => 'featured',
        'meta_value' => '1'
    ) );
    
    if ( empty( $posts ) ) {
        return '<p class="no-posts">No featured posts found.</p>';
    }
    
    ob_start();
    ?>
    <div class="featured-posts-block">
        <h3>Featured <?php echo esc_html( get_post_type_object( $post_type )->label ); ?></h3>
        <div class="posts-grid">
            <?php foreach ( $posts as $post ) : setup_postdata( $post ); ?>
                <article class="featured-post">
                    <?php if ( has_post_thumbnail() ) : ?>
                        <div class="post-thumbnail">
                            <?php the_post_thumbnail( 'medium' ); ?>
                        </div>
                    <?php endif; ?>
                    
                    <div class="post-content">
                        <h4 class="post-title">
                            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                        </h4>
                        <div class="post-excerpt">
                            <?php the_excerpt(); ?>
                        </div>
                        <div class="post-meta">
                            <time datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>">
                                <?php the_date(); ?>
                            </time>
                        </div>
                    </div>
                </article>
            <?php endforeach; wp_reset_postdata(); ?>
        </div>
    </div>
    <?php
    
    return ob_get_clean();
}

// Cache invalidation hooks
function invalidate_dynamic_block_cache( $post_id ) {
    // Clear all dynamic block caches when a post is updated
    global $wpdb;
    $wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_dynamic_block_%'" );
}
add_action( 'save_post', 'invalidate_dynamic_block_cache' );
add_action( 'delete_post', 'invalidate_dynamic_block_cache' );
```

## Dynamic Block with Forms

### Contact Form Block

```php
// PHP: Contact form dynamic block
function render_contact_form_block( $attributes, $content ) {
    $form_id = $attributes['form_id'] ?? 'default';
    $email = $attributes['email'] ?? get_option( 'admin_email' );
    $subject = $attributes['subject'] ?? 'Contact Form Submission';
    
    // Handle form submission
    $message = '';
    if ( isset( $_POST['contact_form_submit'] ) && wp_verify_nonce( $_POST['contact_form_nonce'], 'contact_form_' . $form_id ) ) {
        $name = sanitize_text_field( $_POST['contact_name'] );
        $email_from = sanitize_email( $_POST['contact_email'] );
        $message_text = sanitize_textarea_field( $_POST['contact_message'] );
        
        if ( ! empty( $name ) && ! empty( $email_from ) && ! empty( $message_text ) ) {
            $headers = array(
                'Content-Type: text/html; charset=UTF-8',
                'From: ' . $name . ' <' . $email_from . '>'
            );
            
            $email_body = sprintf(
                '<h3>Contact Form Submission</h3>
                <p><strong>Name:</strong> %s</p>
                <p><strong>Email:</strong> %s</p>
                <p><strong>Message:</strong></p>
                <p>%s</p>',
                esc_html( $name ),
                esc_html( $email_from ),
                nl2br( esc_html( $message_text ) )
            );
            
            if ( wp_mail( $email, $subject, $email_body, $headers ) ) {
                $message = '<div class="contact-success">Thank you for your message!</div>';
            } else {
                $message = '<div class="contact-error">Sorry, there was an error sending your message.</div>';
            }
        } else {
            $message = '<div class="contact-error">Please fill in all required fields.</div>';
        }
    }
    
    ob_start();
    ?>
    <div class="contact-form-block">
        <?php if ( $message ) : ?>
            <?php echo $message; ?>
        <?php endif; ?>
        
        <form method="post" class="contact-form">
            <?php wp_nonce_field( 'contact_form_' . $form_id, 'contact_form_nonce' ); ?>
            
            <div class="form-group">
                <label for="contact_name">Name *</label>
                <input type="text" id="contact_name" name="contact_name" required 
                       value="<?php echo esc_attr( $_POST['contact_name'] ?? '' ); ?>" />
            </div>
            
            <div class="form-group">
                <label for="contact_email">Email *</label>
                <input type="email" id="contact_email" name="contact_email" required 
                       value="<?php echo esc_attr( $_POST['contact_email'] ?? '' ); ?>" />
            </div>
            
            <div class="form-group">
                <label for="contact_message">Message *</label>
                <textarea id="contact_message" name="contact_message" rows="5" required><?php echo esc_textarea( $_POST['contact_message'] ?? '' ); ?></textarea>
            </div>
            
            <div class="form-group">
                <input type="submit" name="contact_form_submit" value="Send Message" class="submit-button" />
            </div>
        </form>
    </div>
    <?php
    
    return ob_get_clean();
}

// Register contact form block
register_block_type( 'my-plugin/contact-form', array(
    'attributes' => array(
        'form_id' => array(
            'type' => 'string',
            'default' => 'default'
        ),
        'email' => array(
            'type' => 'string',
            'default' => ''
        ),
        'subject' => array(
            'type' => 'string',
            'default' => 'Contact Form Submission'
        )
    ),
    'render_callback' => 'render_contact_form_block'
) );
```

### Search Block

```php
// PHP: Dynamic search block
function render_search_block( $attributes, $content ) {
    $placeholder = $attributes['placeholder'] ?? 'Search...';
    $button_text = $attributes['button_text'] ?? 'Search';
    $post_types = $attributes['post_types'] ?? array( 'post' );
    
    $search_query = get_search_query();
    $search_results = array();
    
    if ( $search_query ) {
        $search_results = get_posts( array(
            'post_type' => $post_types,
            'posts_per_page' => 10,
            's' => $search_query,
            'post_status' => 'publish'
        ) );
    }
    
    ob_start();
    ?>
    <div class="search-block">
        <form role="search" method="get" class="search-form" action="<?php echo esc_url( home_url( '/' ) ); ?>">
            <label for="search-field"><?php _e( 'Search for:', 'textdomain' ); ?></label>
            <input type="search" id="search-field" class="search-field" 
                   placeholder="<?php echo esc_attr( $placeholder ); ?>" 
                   value="<?php echo esc_attr( $search_query ); ?>" 
                   name="s" />
            <input type="hidden" name="post_type" value="<?php echo esc_attr( implode( ',', $post_types ) ); ?>" />
            <input type="submit" class="search-submit" value="<?php echo esc_attr( $button_text ); ?>" />
        </form>
        
        <?php if ( $search_query && ! empty( $search_results ) ) : ?>
            <div class="search-results">
                <h3>Search Results for "<?php echo esc_html( $search_query ); ?>"</h3>
                <ul class="results-list">
                    <?php foreach ( $search_results as $post ) : setup_postdata( $post ); ?>
                        <li class="result-item">
                            <h4 class="result-title">
                                <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                            </h4>
                            <div class="result-excerpt">
                                <?php the_excerpt(); ?>
                            </div>
                            <div class="result-meta">
                                <span class="result-type"><?php echo esc_html( get_post_type_object( get_post_type() )->label ); ?></span>
                                <span class="result-date"><?php the_date(); ?></span>
                            </div>
                        </li>
                    <?php endforeach; wp_reset_postdata(); ?>
                </ul>
            </div>
        <?php elseif ( $search_query && empty( $search_results ) ) : ?>
            <div class="no-results">
                <p>No results found for "<?php echo esc_html( $search_query ); ?>".</p>
            </div>
        <?php endif; ?>
    </div>
    <?php
    
    return ob_get_clean();
}
```

## Best Practices

### Performance Optimization

```php
// Optimize database queries in dynamic blocks
function optimized_dynamic_block( $attributes ) {
    $post_type = $attributes['post_type'] ?? 'post';
    $limit = $attributes['limit'] ?? 5;
    
    // Use specific fields to reduce memory usage
    $posts = get_posts( array(
        'post_type' => $post_type,
        'posts_per_page' => $limit,
        'fields' => 'ids', // Only get IDs
        'post_status' => 'publish'
    ) );
    
    if ( empty( $posts ) ) {
        return '<p class="no-posts">No posts found.</p>';
    }
    
    // Get full post data only when needed
    $full_posts = array_map( 'get_post', $posts );
    
    // Render content
    ob_start();
    foreach ( $full_posts as $post ) {
        // Render individual post
        render_post_item( $post );
    }
    
    return ob_get_clean();
}
```

### Error Handling

```php
// Robust error handling for dynamic blocks
function safe_dynamic_block_render( $attributes, $content ) {
    try {
        // Validate attributes
        if ( ! validate_block_attributes( $attributes ) ) {
            return '<p class="block-error">Invalid block configuration.</p>';
        }
        
        // Render content
        return render_dynamic_content( $attributes );
        
    } catch ( Exception $e ) {
        // Log error for debugging
        error_log( 'Dynamic block error: ' . $e->getMessage() );
        
        // Return user-friendly error message
        if ( WP_DEBUG ) {
            return '<p class="block-error">Block error: ' . esc_html( $e->getMessage() ) . '</p>';
        } else {
            return '<p class="block-error">Unable to display content at this time.</p>';
        }
    }
}

function validate_block_attributes( $attributes ) {
    // Validate required attributes
    if ( ! isset( $attributes['post_type'] ) ) {
        return false;
    }
    
    // Validate post type exists
    if ( ! post_type_exists( $attributes['post_type'] ) ) {
        return false;
    }
    
    // Validate numeric attributes
    if ( isset( $attributes['limit'] ) && ( ! is_numeric( $attributes['limit'] ) || $attributes['limit'] <= 0 ) ) {
        return false;
    }
    
    return true;
}
```

### Security Considerations

```php
// Secure dynamic block rendering
function secure_dynamic_block( $attributes, $content ) {
    // Sanitize all input attributes
    $safe_attributes = array();
    
    if ( isset( $attributes['post_type'] ) ) {
        $safe_attributes['post_type'] = sanitize_text_field( $attributes['post_type'] );
    }
    
    if ( isset( $attributes['limit'] ) ) {
        $safe_attributes['limit'] = max( 1, min( 50, intval( $attributes['limit'] ) ) );
    }
    
    if ( isset( $attributes['search_term'] ) ) {
        $safe_attributes['search_term'] = sanitize_text_field( $attributes['search_term'] );
    }
    
    // Capability check for sensitive data
    if ( isset( $attributes['show_draft_posts'] ) && $attributes['show_draft_posts'] ) {
        if ( ! current_user_can( 'edit_posts' ) ) {
            $safe_attributes['show_draft_posts'] = false;
        }
    }
    
    return render_dynamic_content( $safe_attributes );
}
```

## Official Documentation

https://developer.wordpress.org/block-editor/reference-guides/block-api/block-registration/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-attributes/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-supports/
