---
difficulty: Beginner
tags: [security, nonces, csrf, forms]
related: [security/sanitize-input, ajax/admin-ajax]
use_case: CSRF protection for forms and AJAX
---

# WordPress Nonces - Complete Examples

## Form Nonce

```php
// In form
<form method="post" action="">
    <?php wp_nonce_field( 'my_action', 'my_nonce_field' ); ?>
    <input type="text" name="data">
    <input type="submit" value="Submit">
</form>

// Verify nonce
if ( isset( $_POST['my_nonce_field'] ) && 
     wp_verify_nonce( $_POST['my_nonce_field'], 'my_action' ) ) {
    // Process form
    $data = sanitize_text_field( $_POST['data'] );
} else {
    wp_die( 'Security check failed' );
}
```

## URL Nonce

```php
// Create nonce URL
$delete_url = wp_nonce_url(
    admin_url( 'admin.php?action=delete&id=' . $post_id ),
    'delete_post_' . $post_id,
    'delete_nonce'
);

echo '<a href="' . esc_url( $delete_url ) . '">Delete</a>';

// Verify nonce from URL
if ( isset( $_GET['delete_nonce'] ) && 
     wp_verify_nonce( $_GET['delete_nonce'], 'delete_post_' . $post_id ) ) {
    // Process deletion
    wp_delete_post( $post_id );
}
```

## AJAX Nonce

```php
// Create nonce for AJAX
wp_localize_script( 'my-script', 'myAjax', array(
    'ajaxurl' => admin_url( 'admin-ajax.php' ),
    'nonce'   => wp_create_nonce( 'my_ajax_action' )
));

// JavaScript
jQuery.ajax({
    url: myAjax.ajaxurl,
    type: 'POST',
    data: {
        action: 'my_ajax_handler',
        nonce: myAjax.nonce,
        data: formData
    },
    success: function(response) {
        console.log(response);
    }
});

// PHP AJAX handler
add_action( 'wp_ajax_my_ajax_handler', 'handle_ajax_request' );
function handle_ajax_request() {
    // Verify nonce
    check_ajax_referer( 'my_ajax_action', 'nonce' );
    
    // Process request
    $data = sanitize_text_field( $_POST['data'] );
    
    wp_send_json_success( array( 'message' => 'Success' ) );
}
```

## REST API Nonce

```php
// JavaScript
wp.apiFetch({
    path: '/myplugin/v1/endpoint',
    method: 'POST',
    data: {
        value: 'test'
    }
}).then( response => {
    console.log(response);
});

// PHP REST endpoint
add_action( 'rest_api_init', function() {
    register_rest_route( 'myplugin/v1', '/endpoint', array(
        'methods' => 'POST',
        'callback' => 'my_rest_callback',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        }
    ));
});

function my_rest_callback( $request ) {
    // Nonce is automatically verified by WordPress
    $value = sanitize_text_field( $request['value'] );
    
    return rest_ensure_response( array( 'success' => true ) );
}
```

## Admin Action Nonce

```php
// Admin action link
$action_url = wp_nonce_url(
    admin_url( 'admin.php?page=my-plugin&action=reset' ),
    'reset_settings',
    'reset_nonce'
);

// Verify in admin page
function my_plugin_admin_page() {
    if ( isset( $_GET['action'] ) && $_GET['action'] === 'reset' ) {
        if ( ! isset( $_GET['reset_nonce'] ) || 
             ! wp_verify_nonce( $_GET['reset_nonce'], 'reset_settings' ) ) {
            wp_die( 'Security check failed' );
        }
        
        // Check capability
        if ( ! current_user_can( 'manage_options' ) ) {
            wp_die( 'Unauthorized' );
        }
        
        // Reset settings
        delete_option( 'my_plugin_settings' );
        
        wp_redirect( admin_url( 'admin.php?page=my-plugin&reset=1' ) );
        exit;
    }
    
    // Display admin page
}
```

## Custom Nonce Name

```php
// Use unique nonce names
wp_nonce_field( 'save_post_' . $post_id, 'post_nonce' );

// Verify
wp_verify_nonce( $_POST['post_nonce'], 'save_post_' . $post_id );
```

## Nonce Lifetime

```php
// Default: 24 hours (86400 seconds)
// Can be modified with filter
add_filter( 'nonce_life', function() {
    return 12 * HOUR_IN_SECONDS;  // 12 hours
});
```

## Complete Example: Save Post Meta

```php
// Add nonce field to meta box
function my_meta_box_html( $post ) {
    wp_nonce_field( 'save_my_meta_' . $post->ID, 'my_meta_nonce' );
    
    $value = get_post_meta( $post->ID, '_my_meta_key', true );
    ?>
    <label for="my_field"><?php esc_html_e( 'My Field', 'textdomain' ); ?></label>
    <input 
        type="text" 
        id="my_field" 
        name="my_field" 
        value="<?php echo esc_attr( $value ); ?>"
    >
    <?php
}

// Save post meta with nonce verification
add_action( 'save_post', 'save_my_meta_box' );
function save_my_meta_box( $post_id ) {
    // Check if nonce is set
    if ( ! isset( $_POST['my_meta_nonce'] ) ) {
        return;
    }
    
    // Verify nonce
    if ( ! wp_verify_nonce( $_POST['my_meta_nonce'], 'save_my_meta_' . $post_id ) ) {
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
    
    // Sanitize and save
    if ( isset( $_POST['my_field'] ) ) {
        $value = sanitize_text_field( $_POST['my_field'] );
        update_post_meta( $post_id, '_my_meta_key', $value );
    }
}
```

## Best Practices

1. **Always use nonces** for forms, AJAX, and URL actions
2. **Unique nonce names** - Include IDs or context
3. **Verify before processing** - Check nonce first
4. **Combine with capability checks** - Nonces alone aren't enough
5. **Use specific actions** - Don't reuse generic nonce names

