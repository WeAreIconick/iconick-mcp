# WordPress Action Hooks

Action hooks allow you to execute code at specific points in WordPress execution.

## Core Action Hooks

### Initialization Hooks

```php
// Fired after WordPress finishes loading
add_action( 'init', 'my_init_function' );

function my_init_function() {
    // Register post types, taxonomies, etc.
}

// Fired when admin area loads
add_action( 'admin_init', 'my_admin_init' );

// Fired when WordPress completes loading (but after init)
add_action( 'wp_loaded', 'my_wp_loaded' );
```

### Enqueue Scripts & Styles

```php
// Frontend scripts
add_action( 'wp_enqueue_scripts', 'my_enqueue_scripts' );

function my_enqueue_scripts() {
    wp_enqueue_style( 'my-style', get_stylesheet_uri() );
    wp_enqueue_script( 'my-script', get_template_directory_uri() . '/js/main.js', array( 'jquery' ), '1.0', true );
}

// Admin scripts
add_action( 'admin_enqueue_scripts', 'my_admin_scripts' );

// Login page scripts
add_action( 'login_enqueue_scripts', 'my_login_scripts' );
```

### Post Hooks

```php
// Before saving post
add_action( 'save_post', 'my_save_post', 10, 3 );

function my_save_post( $post_id, $post, $update ) {
    // Runs every time a post is created or updated
}

// Save specific post type
add_action( 'save_post_product', 'save_product_meta' );

// After post is published
add_action( 'publish_post', 'on_post_publish' );

// Post deleted
add_action( 'delete_post', 'on_post_delete' );

// Post status changes
add_action( 'transition_post_status', 'on_status_change', 10, 3 );
```

### Template Hooks

```php
// Head section
add_action( 'wp_head', 'add_custom_meta_tags' );

// Footer section
add_action( 'wp_footer', 'add_tracking_code' );

// Before header
add_action( 'get_header', 'before_header' );

// Before footer
add_action( 'get_footer', 'before_footer' );
```

### User Hooks

```php
// User registration
add_action( 'user_register', 'on_user_register' );

// User login
add_action( 'wp_login', 'on_user_login', 10, 2 );

// User profile update
add_action( 'profile_update', 'on_profile_update', 10, 2 );

// User deletion
add_action( 'delete_user', 'on_user_delete' );
```

### Admin Hooks

```php
// Admin menu
add_action( 'admin_menu', 'add_custom_menu' );

function add_custom_menu() {
    add_menu_page( 'Custom Page', 'Custom Menu', 'manage_options', 'custom-page', 'render_page' );
}

// Admin notices
add_action( 'admin_notices', 'show_admin_notice' );

function show_admin_notice() {
    ?>
    <div class="notice notice-success">
        <p>Settings saved!</p>
    </div>
    <?php
}
```

### Plugin/Theme Hooks

```php
// Plugin activation
register_activation_hook( __FILE__, 'my_plugin_activate' );

// Plugin deactivation
register_deactivation_hook( __FILE__, 'my_plugin_deactivate' );

// Theme switch
add_action( 'after_switch_theme', 'theme_activation' );
```

### AJAX Hooks

```php
// For logged-in users
add_action( 'wp_ajax_my_action', 'handle_ajax' );

// For non-logged-in users
add_action( 'wp_ajax_nopriv_my_action', 'handle_ajax' );

function handle_ajax() {
    check_ajax_referer( 'my_nonce' );
    
    // Process AJAX request
    wp_send_json_success( array( 'message' => 'Success' ) );
}
```

### Cron Hooks

```php
// Register cron event
add_action( 'init', 'schedule_custom_cron' );

function schedule_custom_cron() {
    if ( ! wp_next_scheduled( 'my_daily_task' ) ) {
        wp_schedule_event( time(), 'daily', 'my_daily_task' );
    }
}

// Handle cron
add_action( 'my_daily_task', 'do_daily_task' );

function do_daily_task() {
    // Run daily task
}
```

## Hook Priority

```php
// Default priority is 10
add_action( 'init', 'function1' );  // Priority 10

// Run earlier (lower number = earlier)
add_action( 'init', 'function2', 5 );

// Run later (higher number = later)
add_action( 'init', 'function3', 20 );

// Execution order: function2 → function1 → function3
```

## Removing Actions

```php
// Remove action
remove_action( 'init', 'function_name', 10 );

// Remove all actions
remove_all_actions( 'init' );
```

## Complete Examples

### Save Post Meta

```php
add_action( 'save_post', 'save_custom_meta', 10, 2 );

function save_custom_meta( $post_id, $post ) {
    // Check nonce
    if ( ! isset( $_POST['custom_nonce'] ) || 
         ! wp_verify_nonce( $_POST['custom_nonce'], 'save_meta' ) ) {
        return;
    }
    
    // Check autosave
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    
    // Check permissions
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }
    
    // Save meta
    if ( isset( $_POST['custom_field'] ) ) {
        update_post_meta( $post_id, 'custom_field', 
            sanitize_text_field( $_POST['custom_field'] ) );
    }
}
```

### Custom Dashboard Widget

```php
add_action( 'wp_dashboard_setup', 'add_custom_dashboard_widget' );

function add_custom_dashboard_widget() {
    wp_add_dashboard_widget(
        'custom_widget',
        'Custom Dashboard Widget',
        'render_custom_widget'
    );
}

function render_custom_widget() {
    echo '<p>Custom widget content</p>';
}
```

## Official Documentation

https://developer.wordpress.org/plugins/hooks/actions/
https://developer.wordpress.org/reference/hooks/
