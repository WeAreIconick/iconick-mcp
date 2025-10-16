---
difficulty: Beginner
tags: [security, sanitization, input, validation]
related: [security/escape-output, security/nonces, security/validate-user-input]
use_case: Cleaning user input before saving to database
---

# Sanitize User Input

## Text Field Sanitization

```php
// Single text field
$clean_text = sanitize_text_field( $_POST['field_name'] );

// Multiple text fields
$clean_title = sanitize_text_field( $_POST['title'] );
$clean_name = sanitize_text_field( $_POST['name'] );
```

## Email Sanitization

```php
$clean_email = sanitize_email( $_POST['email'] );

// Validate email
if ( ! is_email( $clean_email ) ) {
    wp_die( 'Invalid email address' );
}
```

## URL Sanitization

```php
// For saving to database
$clean_url = esc_url_raw( $_POST['website'] );

// For output (includes protocol validation)
$safe_url = esc_url( $_POST['link'] );
```

## Integer Sanitization

```php
// Absolute integer (always positive)
$post_id = absint( $_POST['post_id'] );

// Any integer (can be negative)
$offset = intval( $_POST['offset'] );
```

## Array of IDs

```php
// Sanitize array of post IDs
$post_ids = array_map( 'absint', $_POST['post_ids'] );

// Remove any zeros (invalid IDs)
$post_ids = array_filter( $post_ids );
```

## Textarea Content

```php
// Simple textarea (no HTML)
$clean_text = sanitize_textarea_field( $_POST['description'] );

// Allow some HTML tags
$allowed_html = wp_kses_post( $_POST['content'] );

// Custom allowed tags
$allowed_tags = array(
    'a' => array( 'href' => array(), 'title' => array() ),
    'br' => array(),
    'em' => array(),
    'strong' => array()
);
$clean_html = wp_kses( $_POST['content'], $allowed_tags );
```

## File Name Sanitization

```php
$clean_filename = sanitize_file_name( $_FILES['upload']['name'] );
```

## Key/Slug Sanitization

```php
// For option keys, meta keys, etc.
$clean_key = sanitize_key( $_POST['setting_key'] );

// For post slugs
$clean_slug = sanitize_title( $_POST['post_slug'] );
```

## Checkbox/Boolean Values

```php
// Checkbox (returns true if checked, false if not)
$is_enabled = isset( $_POST['enable_feature'] ) && $_POST['enable_feature'] === '1';

// Or using filter
$is_active = filter_var( $_POST['active'], FILTER_VALIDATE_BOOLEAN );
```

## JSON Data

```php
// Sanitize JSON string
$json_string = sanitize_text_field( $_POST['json_data'] );
$data = json_decode( $json_string, true );

if ( json_last_error() !== JSON_ERROR_NONE ) {
    wp_die( 'Invalid JSON data' );
}

// Sanitize each value in decoded array
array_walk_recursive( $data, function( &$value ) {
    $value = sanitize_text_field( $value );
});
```

## Complete Form Example

```php
// Process form with complete sanitization
function process_contact_form() {
    // Verify nonce
    if ( ! isset( $_POST['contact_nonce'] ) || 
         ! wp_verify_nonce( $_POST['contact_nonce'], 'contact_form' ) ) {
        wp_die( 'Security check failed' );
    }
    
    // Sanitize all fields
    $name = sanitize_text_field( $_POST['name'] );
    $email = sanitize_email( $_POST['email'] );
    $subject = sanitize_text_field( $_POST['subject'] );
    $message = sanitize_textarea_field( $_POST['message'] );
    
    // Validate required fields
    if ( empty( $name ) || empty( $email ) || empty( $message ) ) {
        wp_die( 'All fields are required' );
    }
    
    // Validate email
    if ( ! is_email( $email ) ) {
        wp_die( 'Invalid email address' );
    }
    
    // Process sanitized data
    // ... send email, save to database, etc.
}
add_action( 'admin_post_submit_contact_form', 'process_contact_form' );
```

## Best Practices

1. **Always sanitize** - Never trust user input
2. **Sanitize for storage** - Use `esc_url_raw()`, not `esc_url()` when saving
3. **Validate after sanitizing** - Check if data meets requirements
4. **Type-specific functions** - Use the right function for the data type
5. **Escape on output** - Sanitize on input, escape on output

