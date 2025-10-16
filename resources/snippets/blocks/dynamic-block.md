# Dynamic Block (Server-Side Rendering)

```php
// Register dynamic block
function register_my_dynamic_block() {
    register_block_type( 'myplugin/dynamic-block', array(
        'api_version' => 2,
        'attributes' => array(
            'count' => array(
                'type' => 'number',
                'default' => 5
            )
        ),
        'render_callback' => 'render_dynamic_block'
    ));
}
add_action( 'init', 'register_my_dynamic_block' );

// Render function
function render_dynamic_block( $attributes ) {
    $count = $attributes['count'];
    
    $posts = get_posts( array(
        'posts_per_page' => $count,
        'post_status' => 'publish'
    ));
    
    ob_start();
    ?>
    <div class="dynamic-block">
        <h3>Latest Posts</h3>
        <ul>
            <?php foreach ( $posts as $post ) : ?>
                <li>
                    <a href="<?php echo esc_url( get_permalink( $post->ID ) ); ?>">
                        <?php echo esc_html( $post->post_title ); ?>
                    </a>
                </li>
            <?php endforeach; ?>
        </ul>
    </div>
    <?php
    return ob_get_clean();
}
```
