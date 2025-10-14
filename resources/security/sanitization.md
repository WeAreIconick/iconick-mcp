# WordPress Data Sanitization

Sanitization cleans data before storing it in the database.

## Key Sanitization Functions

### Text Sanitization

```php
// Remove all HTML tags and encode special characters
$clean = sanitize_text_field( $_POST['input'] );

// For textarea (preserves line breaks)
$clean = sanitize_textarea_field( $_POST['message'] );

// For titles
$clean = sanitize_title( $_POST['title'] );  // Converts to slug

// For file names
$clean = sanitize_file_name( $_POST['filename'] );

// For HTML class names
$clean = sanitize_html_class( $_POST['class_name'] );

// For meta keys
$clean = sanitize_key( $_POST['meta_key'] );
```

### URL Sanitization

```php
// Sanitize URL
$clean_url = esc_url_raw( $_POST['url'] );

// For database storage
$clean_url = sanitize_url( $_POST['url'] );
```

### Email Sanitization

```php
$clean_email = sanitize_email( $_POST['email'] );

// Always validate after sanitizing
if ( ! is_email( $clean_email ) ) {
    // Invalid email
}
```

### HTML/Rich Content

```php
// Allow specific HTML tags
$allowed_html = array(
    'a' => array(
        'href' => array(),
        'title' => array()
    ),
    'br' => array(),
    'em' => array(),
    'strong' => array(),
);

$clean = wp_kses( $_POST['content'], $allowed_html );

// Allow all post content tags
$clean = wp_kses_post( $_POST['content'] );

// Strip all HTML
$clean = wp_strip_all_tags( $_POST['content'] );
```

### Numeric Sanitization

```php
// Absolute integer (always positive)
$id = absint( $_POST['id'] );

// Integer (can be negative)
$number = intval( $_POST['number'] );

// Float
$price = floatval( $_POST['price'] );
```

### Array Sanitization

```php
// Sanitize array of text fields
$clean_array = array_map( 'sanitize_text_field', $_POST['items'] );

// Sanitize array of IDs
$ids = array_map( 'absint', $_POST['ids'] );

// Complex array sanitization
function sanitize_user_data( $data ) {
    return array(
        'name'  => sanitize_text_field( $data['name'] ?? '' ),
        'email' => sanitize_email( $data['email'] ?? '' ),
        'age'   => absint( $data['age'] ?? 0 ),
        'bio'   => sanitize_textarea_field( $data['bio'] ?? '' ),
    );
}
```

## Meta Data Sanitization

```php
// When saving meta data
function save_custom_meta( $post_id ) {
    if ( ! isset( $_POST['custom_nonce'] ) || 
         ! wp_verify_nonce( $_POST['custom_nonce'], 'save_meta' ) ) {
        return;
    }
    
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }
    
    // Sanitize and save
    if ( isset( $_POST['custom_field'] ) ) {
        $value = sanitize_text_field( $_POST['custom_field'] );
        update_post_meta( $post_id, 'custom_field', $value );
    }
    
    // For rich content
    if ( isset( $_POST['custom_content'] ) ) {
        $value = wp_kses_post( $_POST['custom_content'] );
        update_post_meta( $post_id, 'custom_content', $value );
    }
}
add_action( 'save_post', 'save_custom_meta' );
```

## Settings API Sanitization

```php
// Register setting with sanitization callback
register_setting(
    'my_options_group',
    'my_option_name',
    array(
        'type' => 'string',
        'sanitize_callback' => 'sanitize_my_option',
        'default' => '',
    )
);

function sanitize_my_option( $input ) {
    // Text field
    if ( isset( $input['text'] ) ) {
        $output['text'] = sanitize_text_field( $input['text'] );
    }
    
    // Email
    if ( isset( $input['email'] ) ) {
        $output['email'] = sanitize_email( $input['email'] );
    }
    
    // Checkbox
    if ( isset( $input['checkbox'] ) ) {
        $output['checkbox'] = rest_sanitize_boolean( $input['checkbox'] );
    }
    
    // Select (whitelist)
    if ( isset( $input['select'] ) ) {
        $valid = array( 'option1', 'option2', 'option3' );
        $output['select'] = in_array( $input['select'], $valid ) ? $input['select'] : 'option1';
    }
    
    return $output;
}
```

## File Upload Sanitization

```php
function handle_file_upload() {
    if ( ! function_exists( 'wp_handle_upload' ) ) {
        require_once( ABSPATH . 'wp-admin/includes/file.php' );
    }
    
    $uploadedfile = $_FILES['file'];
    
    // Sanitize filename
    $uploadedfile['name'] = sanitize_file_name( $uploadedfile['name'] );
    
    $upload_overrides = array(
        'test_form' => false,
        'mimes' => array(
            'jpg|jpeg|jpe' => 'image/jpeg',
            'png' => 'image/png',
        ),
    );
    
    $movefile = wp_handle_upload( $uploadedfile, $upload_overrides );
    
    if ( isset( $movefile['error'] ) ) {
        return new WP_Error( 'upload_error', $movefile['error'] );
    }
    
    return $movefile;
}
```

## Custom Sanitization Functions

```php
// Sanitize hex color
function sanitize_hex_color( $color ) {
    if ( preg_match( '/^#[a-f0-9]{6}$/i', $color ) ) {
        return $color;
    }
    return '';
}

// Sanitize phone number
function sanitize_phone( $phone ) {
    return preg_replace( '/[^0-9+\-\(\)\s]/', '', $phone );
}

// Sanitize comma-separated list
function sanitize_csv_list( $input ) {
    $items = explode( ',', $input );
    $items = array_map( 'trim', $items );
    $items = array_map( 'sanitize_text_field', $items );
    $items = array_filter( $items ); // Remove empty
    return implode( ', ', $items );
}
```

## REST API Sanitization

```php
register_rest_route( 'myplugin/v1', '/items', array(
    'methods'  => 'POST',
    'callback' => 'create_item',
    'args' => array(
        'title' => array(
            'required' => true,
            'type' => 'string',
            'sanitize_callback' => 'sanitize_text_field',
        ),
        'content' => array(
            'type' => 'string',
            'sanitize_callback' => 'wp_kses_post',
        ),
    ),
) );
```

## Best Practices

1. **Sanitize ALL user input** before storing
2. **Use specific functions** for data type (sanitize_email, not sanitize_text_field)
3. **Whitelist allowed values** for selections
4. **Combine with validation** - sanitize then validate
5. **Don't rely on client-side validation**
6. **Sanitize before database operations**
7. **Use WordPress functions** over custom regex when possible

## Sanitization Flow

```
User Input → Validate → Sanitize → Store → Escape on Output
```

## Common Patterns

```php
// Form processing
function process_form_submission() {
    // 1. Verify nonce
    check_admin_referer( 'my_action', 'my_nonce' );
    
    // 2. Check capabilities
    if ( ! current_user_can( 'edit_posts' ) ) {
        wp_die( 'Unauthorized' );
    }
    
    // 3. Sanitize input
    $title = sanitize_text_field( $_POST['title'] ?? '' );
    $content = wp_kses_post( $_POST['content'] ?? '' );
    $email = sanitize_email( $_POST['email'] ?? '' );
    
    // 4. Validate
    if ( empty( $title ) || ! is_email( $email ) ) {
        return new WP_Error( 'validation_failed', 'Invalid input' );
    }
    
    // 5. Save
    $post_id = wp_insert_post( array(
        'post_title' => $title,
        'post_content' => $content,
    ) );
    
    update_post_meta( $post_id, 'contact_email', $email );
    
    return $post_id;
}
```

## Security Checklist

- [ ] Sanitize all `$_POST`, `$_GET`, `$_REQUEST` data
- [ ] Use type-specific sanitization functions
- [ ] Validate after sanitizing
- [ ] Whitelist allowed values for dropdowns/radios
- [ ] Use `wp_kses()` or `wp_kses_post()` for HTML content
- [ ] Sanitize file names before upload
- [ ] Don't trust client-side validation
- [ ] Combine sanitization with nonce verification
- [ ] Check user capabilities before processing

## Official Documentation

https://developer.wordpress.org/apis/security/sanitizing/
https://developer.wordpress.org/reference/functions/sanitize_text_field/
https://developer.wordpress.org/reference/functions/wp_kses/
