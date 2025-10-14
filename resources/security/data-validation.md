# WordPress Data Validation

Data validation ensures that data is in the expected format before processing.

## Validation vs Sanitization vs Escaping

- **Validation**: Check if data meets expected criteria (reject if invalid)
- **Sanitization**: Clean data before storing (remove unwanted parts)
- **Escaping**: Make data safe for output (prevent XSS)

## Common Validation Functions

### Email Validation

```php
$email = 'user@example.com';

if ( is_email( $email ) ) {
    // Valid email
} else {
    // Invalid email
}

// Or use built-in validation
$clean_email = sanitize_email( $email );
if ( ! is_email( $clean_email ) ) {
    wp_die( 'Invalid email address' );
}
```

### URL Validation

```php
$url = 'https://example.com';

if ( filter_var( $url, FILTER_VALIDATE_URL ) ) {
    // Valid URL
}

// WordPress way
$url = esc_url_raw( $url );
if ( empty( $url ) ) {
    // Invalid URL
}
```

### Integer Validation

```php
$id = $_POST['post_id'];

if ( ! is_numeric( $id ) || $id < 1 ) {
    wp_die( 'Invalid ID' );
}

// Cast to int
$id = absint( $id );  // Absolute integer (always positive)
$id = intval( $id );  // Integer value
```

### Boolean Validation

```php
$enabled = $_POST['enabled'];

// Convert to boolean
$enabled = rest_sanitize_boolean( $enabled );

// Or check explicitly
if ( ! in_array( $enabled, array( true, false, 'true', 'false', 1, 0, '1', '0' ), true ) ) {
    wp_die( 'Invalid boolean value' );
}
```

## Form Validation Example

```php
function validate_custom_form() {
    // Verify nonce first
    if ( ! isset( $_POST['custom_nonce'] ) || 
         ! wp_verify_nonce( $_POST['custom_nonce'], 'custom_action' ) ) {
        wp_die( 'Security check failed' );
    }
    
    $errors = array();
    
    // Validate email
    $email = isset( $_POST['email'] ) ? sanitize_email( $_POST['email'] ) : '';
    if ( empty( $email ) || ! is_email( $email ) ) {
        $errors[] = 'Please provide a valid email address';
    }
    
    // Validate required field
    $name = isset( $_POST['name'] ) ? sanitize_text_field( $_POST['name'] ) : '';
    if ( empty( $name ) ) {
        $errors[] = 'Name is required';
    }
    
    // Validate number
    $age = isset( $_POST['age'] ) ? absint( $_POST['age'] ) : 0;
    if ( $age < 1 || $age > 120 ) {
        $errors[] = 'Please provide a valid age';
    }
    
    // Validate selection
    $country = isset( $_POST['country'] ) ? sanitize_text_field( $_POST['country'] ) : '';
    $valid_countries = array( 'US', 'UK', 'CA', 'AU' );
    if ( ! in_array( $country, $valid_countries, true ) ) {
        $errors[] = 'Please select a valid country';
    }
    
    if ( ! empty( $errors ) ) {
        foreach ( $errors as $error ) {
            add_settings_error( 'custom_form', 'validation_error', $error );
        }
        return false;
    }
    
    return true;
}
```

## Validation Functions

### String Validation

```php
// Check if empty
if ( empty( $value ) ) { }

// Check length
if ( strlen( $value ) > 100 ) {
    // Too long
}

// Check pattern
if ( ! preg_match( '/^[a-zA-Z0-9_]+$/', $username ) ) {
    // Invalid characters
}
```

### Array Validation

```php
// Check if array
if ( ! is_array( $data ) ) {
    wp_die( 'Expected array' );
}

// Check if associative array
if ( ! wp_is_numeric_array( $data ) ) {
    // Is associative
}

// Validate array values
$allowed_values = array( 'draft', 'publish', 'private' );
if ( ! in_array( $status, $allowed_values, true ) ) {
    wp_die( 'Invalid status' );
}
```

### File Upload Validation

```php
function validate_file_upload( $file ) {
    // Check if file was uploaded
    if ( ! isset( $file['error'] ) || is_array( $file['error'] ) ) {
        return new WP_Error( 'invalid_file', 'Invalid file upload' );
    }
    
    // Check for upload errors
    if ( $file['error'] !== UPLOAD_ERR_OK ) {
        return new WP_Error( 'upload_error', 'File upload failed' );
    }
    
    // Check file size (2MB max)
    if ( $file['size'] > 2097152 ) {
        return new WP_Error( 'file_too_large', 'File exceeds 2MB limit' );
    }
    
    // Check file type
    $allowed_types = array( 'image/jpeg', 'image/png', 'image/gif' );
    $finfo = new finfo( FILEINFO_MIME_TYPE );
    $mime = $finfo->file( $file['tmp_name'] );
    
    if ( ! in_array( $mime, $allowed_types, true ) ) {
        return new WP_Error( 'invalid_type', 'Only JPG, PNG, and GIF files allowed' );
    }
    
    // Check file extension
    $allowed_ext = array( 'jpg', 'jpeg', 'png', 'gif' );
    $ext = strtolower( pathinfo( $file['name'], PATHINFO_EXTENSION ) );
    
    if ( ! in_array( $ext, $allowed_ext, true ) ) {
        return new WP_Error( 'invalid_extension', 'Invalid file extension' );
    }
    
    return true;
}
```

## REST API Validation

```php
function validate_rest_param( $value, $request, $param ) {
    // Validate email
    if ( ! is_email( $value ) ) {
        return new WP_Error(
            'invalid_email',
            'Please provide a valid email address',
            array( 'status' => 400 )
        );
    }
    
    return true;
}

register_rest_route( 'myplugin/v1', '/users', array(
    'methods'  => 'POST',
    'callback' => 'create_user_callback',
    'args' => array(
        'email' => array(
            'required' => true,
            'type' => 'string',
            'format' => 'email',
            'validate_callback' => 'validate_rest_param',
        ),
        'age' => array(
            'required' => false,
            'type' => 'integer',
            'minimum' => 1,
            'maximum' => 120,
        ),
    ),
) );
```

## User Capability Validation

```php
// Check if user can perform action
if ( ! current_user_can( 'edit_posts' ) ) {
    wp_die( 'You do not have permission to perform this action' );
}

// Check specific post permission
if ( ! current_user_can( 'edit_post', $post_id ) ) {
    wp_die( 'You cannot edit this post' );
}

// Check for administrator
if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( 'Administrator access required' );
}
```

## Nonce Validation

```php
// Validate nonce (ALWAYS do this for forms)
if ( ! isset( $_POST['my_nonce'] ) || 
     ! wp_verify_nonce( $_POST['my_nonce'], 'my_action' ) ) {
    wp_die( 'Security verification failed' );
}
```

## Best Practices

1. **Validate early** - Check data before processing
2. **Use strict comparison** (`===`, `in_array( $val, $arr, true )`)
3. **Whitelist over blacklist** - Define what's allowed, not what's forbidden
4. **Validate user capabilities** before sensitive operations
5. **Always verify nonces** for form submissions
6. **Return meaningful errors** for user feedback
7. **Log validation failures** for security monitoring
8. **Use WordPress functions** when available (`is_email()`, `absint()`, etc.)

## Validation Checklist

- [ ] Verify nonce for forms
- [ ] Check user capabilities
- [ ] Validate required fields are present
- [ ] Validate data types (int, string, email, URL)
- [ ] Validate value ranges (min/max)
- [ ] Validate against whitelist of allowed values
- [ ] Validate file uploads (type, size, extension)
- [ ] Check array structure if expected
- [ ] Provide clear error messages
- [ ] Log validation failures

## Official Documentation

https://developer.wordpress.org/apis/security/data-validation/
https://developer.wordpress.org/plugins/security/
