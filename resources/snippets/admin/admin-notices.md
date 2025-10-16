# Admin Notices

```php
// Success notice
add_action( 'admin_notices', 'my_success_notice' );
function my_success_notice() {
    ?>
    <div class="notice notice-success is-dismissible">
        <p><?php esc_html_e( 'Settings saved successfully!', 'textdomain' ); ?></p>
    </div>
    <?php
}

// Error notice
add_action( 'admin_notices', 'my_error_notice' );
function my_error_notice() {
    ?>
    <div class="notice notice-error">
        <p><?php esc_html_e( 'An error occurred!', 'textdomain' ); ?></p>
    </div>
    <?php
}

// Warning notice
add_action( 'admin_notices', 'my_warning_notice' );
function my_warning_notice() {
    ?>
    <div class="notice notice-warning">
        <p><?php esc_html_e( 'Please update your settings.', 'textdomain' ); ?></p>
    </div>
    <?php
}

// Info notice
add_action( 'admin_notices', 'my_info_notice' );
function my_info_notice() {
    ?>
    <div class="notice notice-info">
        <p><?php esc_html_e( 'New features available!', 'textdomain' ); ?></p>
    </div>
    <?php
}

// Conditional notice (only on specific page)
add_action( 'admin_notices', 'conditional_admin_notice' );
function conditional_admin_notice() {
    $screen = get_current_screen();
    
    if ( $screen->id !== 'toplevel_page_myplugin' ) {
        return;
    }
    
    if ( ! get_option( 'myplugin_api_key' ) ) {
        ?>
        <div class="notice notice-warning">
            <p><?php esc_html_e( 'Please configure your API key in settings.', 'textdomain' ); ?></p>
        </div>
        <?php
    }
}

// Dismissible notice with user meta
add_action( 'admin_notices', 'dismissible_notice' );
function dismissible_notice() {
    $user_id = get_current_user_id();
    
    if ( get_user_meta( $user_id, 'dismissed_notice', true ) ) {
        return;
    }
    
    ?>
    <div class="notice notice-info is-dismissible" data-notice="my-notice">
        <p><?php esc_html_e( 'Check out our new features!', 'textdomain' ); ?></p>
    </div>
    
    <script>
    jQuery(document).on('click', '.notice[data-notice="my-notice"] .notice-dismiss', function() {
        jQuery.post(ajaxurl, {
            action: 'dismiss_admin_notice',
            nonce: '<?php echo wp_create_nonce( "dismiss_notice" ); ?>'
        });
    });
    </script>
    <?php
}

add_action( 'wp_ajax_dismiss_admin_notice', 'handle_dismiss_notice' );
function handle_dismiss_notice() {
    check_ajax_referer( 'dismiss_notice', 'nonce' );
    update_user_meta( get_current_user_id(), 'dismissed_notice', true );
    wp_die();
}
```
