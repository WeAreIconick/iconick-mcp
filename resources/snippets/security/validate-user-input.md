# Validate User Input

```php
// Validate integer
function validate_post_id( $id ) {
    $id = absint( $id );
    if ( $id === 0 || ! get_post( $id ) ) {
        return new WP_Error( 'invalid_id', 'Invalid post ID' );
    }
    return $id;
}

// Validate email
function validate_email_field( $email ) {
    $email = sanitize_email( $email );
    if ( ! is_email( $email ) ) {
        return new WP_Error( 'invalid_email', 'Please enter a valid email' );
    }
    return $email;
}

// Validate URL
function validate_url_field( $url ) {
    $url = esc_url_raw( $url );
    if ( ! filter_var( $url, FILTER_VALIDATE_URL ) ) {
        return new WP_Error( 'invalid_url', 'Please enter a valid URL' );
    }
    return $url;
}

// Validate array of IDs
function validate_id_array( $ids ) {
    if ( ! is_array( $ids ) ) {
        return new WP_Error( 'invalid_input', 'Expected array' );
    }
    
    $clean_ids = array_map( 'absint', $ids );
    $clean_ids = array_filter( $clean_ids ); // Remove zeros
    
    if ( empty( $clean_ids ) ) {
        return new WP_Error( 'empty_array', 'No valid IDs provided' );
    }
    
    return $clean_ids;
}

// Validate slug
function validate_slug( $slug ) {
    $slug = sanitize_title( $slug );
    if ( empty( $slug ) || ! preg_match( '/^[a-z0-9-]+$/', $slug ) ) {
        return new WP_Error( 'invalid_slug', 'Invalid slug format' );
    }
    return $slug;
}

// Complete form validation
function validate_contact_form( $data ) {
    $errors = new WP_Error();
    
    // Name (required, min 2 chars)
    $name = sanitize_text_field( $data['name'] ?? '' );
    if ( strlen( $name ) < 2 ) {
        $errors->add( 'name', 'Name must be at least 2 characters' );
    }
    
    // Email (required, valid format)
    $email = sanitize_email( $data['email'] ?? '' );
    if ( ! is_email( $email ) ) {
        $errors->add( 'email', 'Please enter a valid email address' );
    }
    
    // Phone (optional, but validate if provided)
    $phone = sanitize_text_field( $data['phone'] ?? '' );
    if ( ! empty( $phone ) && ! preg_match( '/^[0-9-+() ]+$/', $phone ) ) {
        $errors->add( 'phone', 'Invalid phone number format' );
    }
    
    // Message (required, min 10 chars)
    $message = sanitize_textarea_field( $data['message'] ?? '' );
    if ( strlen( $message ) < 10 ) {
        $errors->add( 'message', 'Message must be at least 10 characters' );
    }
    
    if ( $errors->has_errors() ) {
        return $errors;
    }
    
    return array(
        'name' => $name,
        'email' => $email,
        'phone' => $phone,
        'message' => $message
    );
}
```
