---
difficulty: Beginner
tags: [security, nonces, csrf, forms]
related: [security/data-validation, advanced/ajax-development]
wp_version: 2.0+
---

# WordPress Nonces

Nonces (Number Used Once) protect against CSRF attacks by verifying request intent.

## Creating Nonces

### Form Nonces

```php
// Create nonce field in form
<form method="post">
    <?php wp_nonce_field( 'my_action', 'my_nonce' ); ?>
    <!-- form fields -->
</form>
```

### URL Nonces

```php
// Add nonce to URL
$url = wp_nonce_url( 
    admin_url( 'admin.php?page=my-page&action=delete&id=' . $id ),
    'delete_item_' . $id
);

echo '<a href="' . esc_url( $url ) . '">Delete</a>';
```

### Get Nonce Value

```php
// Get nonce value directly
$nonce = wp_create_nonce( 'my_action' );

echo '<input type="hidden" name="my_nonce" value="' . esc_attr( $nonce ) . '">';
```

## Verifying Nonces

### Form Verification

```php
// Verify nonce from form
if ( ! isset( $_POST['my_nonce'] ) || 
     ! wp_verify_nonce( $_POST['my_nonce'], 'my_action' ) ) {
    wp_die( 'Security check failed' );
}

// Alternative (dies automatically on failure)
check_admin_referer( 'my_action', 'my_nonce' );
```

### URL Verification

```php
// Verify nonce from URL
if ( ! isset( $_GET['_wpnonce'] ) || 
     ! wp_verify_nonce( $_GET['_wpnonce'], 'delete_item_' . $id ) ) {
    wp_die( 'Security check failed' );
}

// Alternative
check_admin_referer( 'delete_item_' . $id );
```

## AJAX Nonces

### Creating AJAX Nonce

```php
// Localize script with nonce
wp_localize_script( 'my-ajax-script', 'myAjax', array(
    'ajax_url' => admin_url( 'admin-ajax.php' ),
    'nonce' => wp_create_nonce( 'my_ajax_action' ),
) );
```

### AJAX JavaScript

```javascript
jQuery.ajax({
    url: myAjax.ajax_url,
    type: 'POST',
    data: {
        action: 'my_ajax_action',
        nonce: myAjax.nonce,
        data: formData
    },
    success: function(response) {
        console.log(response);
    }
});
```

### Verify in AJAX Handler

```php
add_action( 'wp_ajax_my_ajax_action', 'handle_ajax_request' );

function handle_ajax_request() {
    // Verify nonce
    check_ajax_referer( 'my_ajax_action', 'nonce' );
    
    // Process request
    $result = array( 'success' => true );
    
    wp_send_json_success( $result );
}
```

## REST API Nonces

```php
// JavaScript
wp.apiFetch({
    path: '/wp/v2/posts',
    method: 'POST',
    data: {
        title: 'My Post',
        content: 'Content here'
    }
}).then(response => {
    console.log(response);
});

// Nonce is auto-added via wp_rest nonce in wp-api.js
```

## Complete Examples

### Meta Box with Nonce

```php
function add_custom_meta_box() {
    add_meta_box(
        'custom_meta',
        'Custom Meta',
        'render_custom_meta_box',
        'post'
    );
}
add_action( 'add_meta_boxes', 'add_custom_meta_box' );

function render_custom_meta_box( $post ) {
    // Create nonce
    wp_nonce_field( 'save_custom_meta', 'custom_meta_nonce' );
    
    $value = get_post_meta( $post->ID, 'custom_field', true );
    ?>
    <input type="text" name="custom_field" value="<?php echo esc_attr( $value ); ?>">
    <?php
}

function save_custom_meta( $post_id ) {
    // Verify nonce
    if ( ! isset( $_POST['custom_meta_nonce'] ) || 
         ! wp_verify_nonce( $_POST['custom_meta_nonce'], 'save_custom_meta' ) ) {
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
    
    // Save data
    if ( isset( $_POST['custom_field'] ) ) {
        update_post_meta( $post_id, 'custom_field', 
            sanitize_text_field( $_POST['custom_field'] ) );
    }
}
add_action( 'save_post', 'save_custom_meta' );
```

### Settings Page with Nonce

```php
function render_settings_page() {
    ?>
    <div class="wrap">
        <h1>Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields( 'my_options_group' );
            do_settings_sections( 'my_options_page' );
            submit_button();
            ?>
        </form>
    </div>
    <?php
}

// settings_fields() automatically adds nonce
```

## Nonce Lifespan

- Default lifespan: 24 hours (2 nonce ticks of 12 hours each)
- Nonces are tied to: User ID, action name, and time
- Old nonces (previous tick) still work for grace period

## Best Practices

1. **Always use unique action names** - Be specific
2. **Verify before processing** - Check nonce first
3. **Use check_admin_referer()** for admin forms
4. **Use check_ajax_referer()** for AJAX
5. **Include user-specific data in action** for unique items
6. **Don't expose nonces** in public content
7. **Combine with capability checks** - Nonces aren't permission checks

## Common Patterns

```php
// Admin form processing
if ( isset( $_POST['submit'] ) ) {
    check_admin_referer( 'my_action', 'my_nonce' );
    
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'Unauthorized' );
    }
    
    // Process form
}

// AJAX handler
function my_ajax_handler() {
    check_ajax_referer( 'my_ajax_nonce', 'nonce' );
    
    // Process AJAX request
    wp_send_json_success( $data );
}
```

## Security Checklist

- [ ] Use unique, descriptive action names
- [ ] Create nonce: `wp_nonce_field()` or `wp_create_nonce()`
- [ ] Verify nonce: `wp_verify_nonce()` or `check_*_referer()`
- [ ] Verify BEFORE processing data
- [ ] Check user capabilities too
- [ ] Use `check_ajax_referer()` for AJAX
- [ ] Don't cache pages with nonces
- [ ] Handle nonce failures gracefully

## Official Documentation

https://developer.wordpress.org/apis/security/nonces/
https://developer.wordpress.org/reference/functions/wp_nonce_field/