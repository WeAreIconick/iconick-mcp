---
difficulty: Beginner
tags: [admin, menu, pages, settings]
related: [forms/settings-api, admin/settings-page-tabs]
use_case: Adding admin menu pages
---

# Add Admin Page

```php
add_action( 'admin_menu', 'my_add_admin_menu' );
function my_add_admin_menu() {
    add_menu_page(
        __( 'My Plugin', 'textdomain' ),      // Page title
        __( 'My Plugin', 'textdomain' ),      // Menu title
        'manage_options',                      // Capability
        'my-plugin',                          // Menu slug
        'my_admin_page_html',                 // Callback
        'dashicons-admin-generic',            // Icon
        20                                    // Position
    );
    
    // Add submenu page
    add_submenu_page(
        'my-plugin',                          // Parent slug
        __( 'Settings', 'textdomain' ),       // Page title
        __( 'Settings', 'textdomain' ),       // Menu title
        'manage_options',                      // Capability
        'my-plugin-settings',                 // Menu slug
        'my_settings_page_html'               // Callback
    );
}

function my_admin_page_html() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        <p><?php esc_html_e( 'Welcome to my plugin!', 'textdomain' ); ?></p>
    </div>
    <?php
}
```
