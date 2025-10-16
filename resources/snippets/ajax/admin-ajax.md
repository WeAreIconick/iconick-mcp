---
difficulty: Intermediate
tags: [ajax, admin, javascript, wp-admin]
related: [security/nonces, ajax/frontend-ajax]
use_case: AJAX requests in WordPress admin
---

# WordPress Admin AJAX - Complete Pattern

## Complete AJAX Implementation

### 1. Enqueue Script with AJAX Data

```php
function myplugin_enqueue_admin_scripts( $hook ) {
    // Only load on specific admin page
    if ( $hook !== 'toplevel_page_my-plugin' ) {
        return;
    }
    
    wp_enqueue_script(
        'myplugin-admin-ajax',
        plugins_url( 'js/admin-ajax.js', __FILE__ ),
        array( 'jquery' ),
        '1.0.0',
        true
    );
    
    // Pass data to JavaScript
    wp_localize_script( 'myplugin-admin-ajax', 'myAjax', array(
        'ajaxurl' => admin_url( 'admin-ajax.php' ),
        'nonce'   => wp_create_nonce( 'my_ajax_nonce' ),
        'strings' => array(
            'loading' => __( 'Loading...', 'textdomain' ),
            'error'   => __( 'An error occurred', 'textdomain' ),
            'success' => __( 'Changes saved', 'textdomain' )
        )
    ));
}
add_action( 'admin_enqueue_scripts', 'myplugin_enqueue_admin_scripts' );
```

### 2. JavaScript AJAX Request

```javascript
// admin-ajax.js
jQuery(document).ready(function($) {
    
    $('#save-button').on('click', function(e) {
        e.preventDefault();
        
        var button = $(this);
        var data = {
            action: 'my_save_data',
            nonce: myAjax.nonce,
            post_id: $('#post_id').val(),
            custom_data: $('#custom_field').val()
        };
        
        // Disable button and show loading
        button.prop('disabled', true).text(myAjax.strings.loading);
        
        $.ajax({
            url: myAjax.ajaxurl,
            type: 'POST',
            data: data,
            success: function(response) {
                if (response.success) {
                    alert(response.data.message);
                    console.log(response.data);
                } else {
                    alert(myAjax.strings.error + ': ' + response.data);
                }
            },
            error: function(xhr, status, error) {
                alert(myAjax.strings.error);
                console.error(error);
            },
            complete: function() {
                button.prop('disabled', false).text('Save');
            }
        });
    });
    
});
```

### 3. PHP AJAX Handler

```php
// Register AJAX handler (for logged-in users)
add_action( 'wp_ajax_my_save_data', 'handle_save_data_ajax' );

function handle_save_data_ajax() {
    // Verify nonce
    check_ajax_referer( 'my_ajax_nonce', 'nonce' );
    
    // Check user capability
    if ( ! current_user_can( 'edit_posts' ) ) {
        wp_send_json_error( 'Insufficient permissions' );
    }
    
    // Get and sanitize data
    $post_id = isset( $_POST['post_id'] ) ? absint( $_POST['post_id'] ) : 0;
    $custom_data = isset( $_POST['custom_data'] ) ? sanitize_text_field( $_POST['custom_data'] ) : '';
    
    // Validate
    if ( $post_id === 0 ) {
        wp_send_json_error( 'Invalid post ID' );
    }
    
    if ( empty( $custom_data ) ) {
        wp_send_json_error( 'Data is required' );
    }
    
    // Process data
    $result = update_post_meta( $post_id, '_custom_meta', $custom_data );
    
    if ( $result ) {
        wp_send_json_success( array(
            'message' => 'Data saved successfully',
            'post_id' => $post_id,
            'value' => $custom_data
        ));
    } else {
        wp_send_json_error( 'Failed to save data' );
    }
    
    // ALWAYS die at the end
    wp_die();
}
```

## Frontend AJAX (Non-logged-in Users)

```php
// Register for both logged-in and non-logged-in
add_action( 'wp_ajax_my_public_action', 'my_public_ajax_handler' );
add_action( 'wp_ajax_nopriv_my_public_action', 'my_public_ajax_handler' );

function my_public_ajax_handler() {
    check_ajax_referer( 'public_nonce', 'nonce' );
    
    // No capability check needed for public action
    
    $email = sanitize_email( $_POST['email'] );
    
    if ( ! is_email( $email ) ) {
        wp_send_json_error( 'Invalid email' );
    }
    
    // Process...
    
    wp_send_json_success( 'Thank you!' );
}
```

## AJAX with File Upload

```php
// JavaScript
var formData = new FormData();
formData.append('action', 'upload_file');
formData.append('nonce', myAjax.nonce);
formData.append('file', $('#file_input')[0].files[0]);

$.ajax({
    url: myAjax.ajaxurl,
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
        console.log(response);
    }
});

// PHP handler
add_action( 'wp_ajax_upload_file', 'handle_file_upload' );
function handle_file_upload() {
    check_ajax_referer( 'my_ajax_nonce', 'nonce' );
    
    if ( ! current_user_can( 'upload_files' ) ) {
        wp_send_json_error( 'Cannot upload files' );
    }
    
    if ( empty( $_FILES['file'] ) ) {
        wp_send_json_error( 'No file provided' );
    }
    
    $file = $_FILES['file'];
    
    // Use WordPress upload handler
    $upload = wp_handle_upload( $file, array( 'test_form' => false ) );
    
    if ( isset( $upload['error'] ) ) {
        wp_send_json_error( $upload['error'] );
    }
    
    wp_send_json_success( array(
        'url' => $upload['url'],
        'file' => $upload['file']
    ));
}
```

## AJAX with Progress Updates

```php
// JavaScript
function processItems(items) {
    var total = items.length;
    var processed = 0;
    
    function processNext(index) {
        if (index >= total) {
            $('#progress').text('Complete!');
            return;
        }
        
        $.ajax({
            url: myAjax.ajaxurl,
            type: 'POST',
            data: {
                action: 'process_item',
                nonce: myAjax.nonce,
                item: items[index]
            },
            success: function() {
                processed++;
                var percent = Math.round((processed / total) * 100);
                $('#progress').text(percent + '%');
                processNext(index + 1);
            }
        });
    }
    
    processNext(0);
}
```

## AJAX Response Formats

```php
// Success response
wp_send_json_success( array(
    'message' => 'Operation completed',
    'data' => $result_data
));

// Error response
wp_send_json_error( 'Error message' );

// Custom response
wp_send_json( array(
    'status' => 'custom',
    'code' => 200,
    'data' => $data
));

// Manual response (not recommended)
header( 'Content-Type: application/json' );
echo json_encode( array( 'success' => true ) );
wp_die();
```

## Heartbeat API AJAX

```php
// Modify heartbeat data sent
add_filter( 'heartbeat_send', 'mytheme_heartbeat_send', 10, 2 );
function mytheme_heartbeat_send( $response, $data ) {
    if ( isset( $data['my_plugin_check'] ) ) {
        $response['my_plugin_response'] = array(
            'status' => 'active',
            'count' => get_user_count()
        );
    }
    return $response;
}

// JavaScript
$(document).on('heartbeat-send', function(e, data) {
    data.my_plugin_check = true;
});

$(document).on('heartbeat-tick', function(e, data) {
    if (data.my_plugin_response) {
        console.log('Status:', data.my_plugin_response.status);
    }
});
```

## Error Handling Best Practices

```php
function robust_ajax_handler() {
    try {
        // Verify nonce
        check_ajax_referer( 'my_nonce', 'nonce' );
        
        // Validate input
        if ( ! isset( $_POST['required_field'] ) ) {
            throw new Exception( 'Missing required field' );
        }
        
        // Process
        $result = do_something();
        
        if ( ! $result ) {
            throw new Exception( 'Processing failed' );
        }
        
        wp_send_json_success( $result );
        
    } catch ( Exception $e ) {
        wp_send_json_error( array(
            'message' => $e->getMessage(),
            'code' => $e->getCode()
        ));
    }
    
    wp_die();
}
```

## Debugging AJAX

```php
// PHP - Log to debug.log
function debug_ajax_handler() {
    error_log( 'AJAX Request: ' . print_r( $_POST, true ) );
    
    // Your code here
    
    wp_send_json_success( 'Check debug.log' );
}

// JavaScript - Console logging
$.ajax({
    // ...
    beforeSend: function(xhr) {
        console.log('Sending:', data);
    },
    success: function(response) {
        console.log('Response:', response);
    },
    error: function(xhr, status, error) {
        console.error('Error:', status, error);
        console.log('Response Text:', xhr.responseText);
    }
});
```

## Best Practices

1. **Always verify nonce** - Use `check_ajax_referer()`
2. **Always check capabilities** - Use `current_user_can()`
3. **Always sanitize input** - Never trust `$_POST` data
4. **Always use wp_send_json_*** - Proper JSON responses
5. **Always wp_die()** - Terminate AJAX handlers properly
6. **Handle errors gracefully** - Use try/catch blocks
7. **Log for debugging** - Use error_log() during development

