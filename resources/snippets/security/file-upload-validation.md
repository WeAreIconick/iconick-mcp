---
difficulty: Advanced
tags: [security, uploads, files, validation]
related: [security/validate-user-input, admin/add-admin-page]
use_case: Secure file upload handling
---

# Secure File Upload

```php
function handle_secure_file_upload() {
    // Check nonce
    check_ajax_referer( 'file_upload', 'nonce' );
    
    // Check capability
    if ( ! current_user_can( 'upload_files' ) ) {
        wp_send_json_error( 'Insufficient permissions' );
    }
    
    // Check file was uploaded
    if ( empty( $_FILES['file'] ) ) {
        wp_send_json_error( 'No file uploaded' );
    }
    
    $file = $_FILES['file'];
    
    // Validate file size (5MB max)
    if ( $file['size'] > 5 * 1024 * 1024 ) {
        wp_send_json_error( 'File too large (5MB maximum)' );
    }
    
    // Validate file type
    $allowed_types = array( 'image/jpeg', 'image/png', 'image/gif', 'application/pdf' );
    $file_type = wp_check_filetype_and_ext( $file['tmp_name'], $file['name'] );
    
    if ( ! in_array( $file_type['type'], $allowed_types ) ) {
        wp_send_json_error( 'Invalid file type' );
    }
    
    // Use WordPress upload handler
    require_once ABSPATH . 'wp-admin/includes/file.php';
    
    $upload = wp_handle_upload( $file, array(
        'test_form' => false,
        'mimes' => array(
            'jpg|jpeg|jpe' => 'image/jpeg',
            'png' => 'image/png',
            'gif' => 'image/gif',
            'pdf' => 'application/pdf'
        )
    ));
    
    if ( isset( $upload['error'] ) ) {
        wp_send_json_error( $upload['error'] );
    }
    
    // Create attachment
    $attachment = array(
        'post_mime_type' => $upload['type'],
        'post_title' => sanitize_file_name( basename( $upload['file'] ) ),
        'post_content' => '',
        'post_status' => 'inherit'
    );
    
    $attach_id = wp_insert_attachment( $attachment, $upload['file'] );
    
    // Generate metadata
    require_once ABSPATH . 'wp-admin/includes/image.php';
    $attach_data = wp_generate_attachment_metadata( $attach_id, $upload['file'] );
    wp_update_attachment_metadata( $attach_id, $attach_data );
    
    wp_send_json_success( array(
        'id' => $attach_id,
        'url' => $upload['url'],
        'type' => $upload['type']
    ));
}
```
