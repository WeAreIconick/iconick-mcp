# Common Action Hooks

```php
// Init - Register post types, taxonomies
add_action( 'init', 'my_custom_init' );

// Enqueue scripts
add_action( 'wp_enqueue_scripts', 'my_enqueue_scripts' );
add_action( 'admin_enqueue_scripts', 'my_admin_scripts' );

// Save post
add_action( 'save_post', 'my_save_post_function', 10, 2 );

// Admin init
add_action( 'admin_init', 'my_admin_init' );

// Admin menu
add_action( 'admin_menu', 'my_add_admin_menu' );

// Widgets init
add_action( 'widgets_init', 'my_register_widgets' );

// User register
add_action( 'user_register', 'my_user_register', 10, 1 );

// wp_head - Add to header
add_action( 'wp_head', 'my_header_code' );

// wp_footer - Add to footer
add_action( 'wp_footer', 'my_footer_code' );
```
