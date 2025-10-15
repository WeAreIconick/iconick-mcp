# WordPress AJAX Development

## Admin AJAX

### Basic Admin AJAX Setup
```php
// Add AJAX actions for logged-in users
add_action('wp_ajax_my_action', 'my_ajax_handler');
// Add AJAX actions for non-logged-in users
add_action('wp_ajax_nopriv_my_action', 'my_ajax_handler');

function my_ajax_handler() {
    // Verify nonce for security
    check_ajax_referer('my_ajax_nonce', 'nonce');
    
    // Check user capabilities
    if (!current_user_can('edit_posts')) {
        wp_die('Unauthorized');
    }
    
    $data = $_POST['data'];
    $result = process_data($data);
    
    wp_send_json_success($result);
}
```

### Admin AJAX with Nonce Security
```php
class SecureAjaxHandler {
    public function __construct() {
        add_action('wp_ajax_secure_action', array($this, 'handle_secure_action'));
        add_action('wp_ajax_nopriv_secure_action', array($this, 'handle_secure_action'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_scripts'));
    }

    public function enqueue_scripts() {
        wp_enqueue_script('jquery');
        
        wp_localize_script('jquery', 'ajax_object', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('secure_ajax_nonce')
        ));
    }

    public function handle_secure_action() {
        // Verify nonce
        if (!wp_verify_nonce($_POST['nonce'], 'secure_ajax_nonce')) {
            wp_send_json_error('Invalid nonce');
        }

        // Check user capabilities
        if (!current_user_can('manage_options')) {
            wp_send_json_error('Insufficient permissions');
        }

        // Validate and sanitize input
        $input_data = sanitize_text_field($_POST['data']);
        
        if (empty($input_data)) {
            wp_send_json_error('Data is required');
        }

        // Process the data
        $result = $this->process_data($input_data);
        
        wp_send_json_success($result);
    }

    private function process_data($data) {
        // Your processing logic here
        return array('processed' => $data, 'timestamp' => current_time('mysql'));
    }
}

new SecureAjaxHandler();
```

### Frontend AJAX with JavaScript
```php
// Enqueue scripts for frontend AJAX
function enqueue_frontend_ajax_scripts() {
    wp_enqueue_script('jquery');
    
    wp_localize_script('jquery', 'frontend_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('frontend_ajax_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'enqueue_frontend_ajax_scripts');

// Handle frontend AJAX
add_action('wp_ajax_frontend_action', 'handle_frontend_ajax');
add_action('wp_ajax_nopriv_frontend_action', 'handle_frontend_ajax');

function handle_frontend_ajax() {
    check_ajax_referer('frontend_ajax_nonce', 'nonce');
    
    $action = sanitize_text_field($_POST['action_type']);
    
    switch ($action) {
        case 'get_posts':
            $posts = get_posts(array('numberposts' => 5));
            wp_send_json_success($posts);
            break;
            
        case 'update_meta':
            $post_id = intval($_POST['post_id']);
            $meta_value = sanitize_text_field($_POST['meta_value']);
            update_post_meta($post_id, '_custom_meta', $meta_value);
            wp_send_json_success('Meta updated');
            break;
            
        default:
            wp_send_json_error('Invalid action');
    }
}
```

### JavaScript AJAX Implementation
```javascript
// Frontend AJAX with jQuery
jQuery(document).ready(function($) {
    $('#ajax-button').click(function(e) {
        e.preventDefault();
        
        var button = $(this);
        var postId = button.data('post-id');
        
        // Disable button during request
        button.prop('disabled', true).text('Processing...');
        
        $.ajax({
            url: frontend_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'frontend_action',
                action_type: 'update_meta',
                post_id: postId,
                meta_value: 'new_value',
                nonce: frontend_ajax.nonce
            },
            success: function(response) {
                if (response.success) {
                    $('#result').html('<div class="success">' + response.data + '</div>');
                } else {
                    $('#result').html('<div class="error">' + response.data + '</div>');
                }
            },
            error: function() {
                $('#result').html('<div class="error">Request failed</div>');
            },
            complete: function() {
                // Re-enable button
                button.prop('disabled', false).text('Update Meta');
            }
        });
    });
});
```

## Advanced AJAX Patterns

### AJAX with REST API
```php
// Register REST API endpoint for AJAX
add_action('rest_api_init', function () {
    register_rest_route('myplugin/v1', '/ajax-action', array(
        'methods' => 'POST',
        'callback' => 'handle_rest_ajax',
        'permission_callback' => function () {
            return current_user_can('edit_posts');
        },
        'args' => array(
            'data' => array(
                'required' => true,
                'sanitize_callback' => 'sanitize_text_field'
            )
        )
    ));
});

function handle_rest_ajax($request) {
    $data = $request->get_param('data');
    $result = process_ajax_data($data);
    
    return new WP_REST_Response($result, 200);
}
```

### AJAX with File Upload
```php
// Handle file upload via AJAX
add_action('wp_ajax_upload_file', 'handle_file_upload');
function handle_file_upload() {
    check_ajax_referer('upload_nonce', 'nonce');
    
    if (!current_user_can('upload_files')) {
        wp_send_json_error('Insufficient permissions');
    }
    
    if (!isset($_FILES['file'])) {
        wp_send_json_error('No file uploaded');
    }
    
    $file = $_FILES['file'];
    
    // Validate file type
    $allowed_types = array('image/jpeg', 'image/png', 'image/gif');
    if (!in_array($file['type'], $allowed_types)) {
        wp_send_json_error('Invalid file type');
    }
    
    // Validate file size (2MB limit)
    if ($file['size'] > 2 * 1024 * 1024) {
        wp_send_json_error('File too large');
    }
    
    // Upload file
    $upload = wp_handle_upload($file, array('test_form' => false));
    
    if ($upload && !isset($upload['error'])) {
        wp_send_json_success(array(
            'url' => $upload['url'],
            'file' => $upload['file']
        ));
    } else {
        wp_send_json_error($upload['error']);
    }
}
```

### AJAX with Database Operations
```php
// AJAX database operations
add_action('wp_ajax_db_operation', 'handle_db_operation');
function handle_db_operation() {
    check_ajax_referer('db_ajax_nonce', 'nonce');
    
    global $wpdb;
    
    $operation = sanitize_text_field($_POST['operation']);
    $table_name = $wpdb->prefix . 'custom_table';
    
    switch ($operation) {
        case 'insert':
            $name = sanitize_text_field($_POST['name']);
            $email = sanitize_email($_POST['email']);
            
            $result = $wpdb->insert(
                $table_name,
                array(
                    'name' => $name,
                    'email' => $email,
                    'created_at' => current_time('mysql')
                ),
                array('%s', '%s', '%s')
            );
            
            if ($result) {
                wp_send_json_success('Record inserted successfully');
            } else {
                wp_send_json_error('Failed to insert record');
            }
            break;
            
        case 'update':
            $id = intval($_POST['id']);
            $name = sanitize_text_field($_POST['name']);
            
            $result = $wpdb->update(
                $table_name,
                array('name' => $name),
                array('id' => $id),
                array('%s'),
                array('%d')
            );
            
            if ($result !== false) {
                wp_send_json_success('Record updated successfully');
            } else {
                wp_send_json_error('Failed to update record');
            }
            break;
            
        case 'delete':
            $id = intval($_POST['id']);
            
            $result = $wpdb->delete(
                $table_name,
                array('id' => $id),
                array('%d')
            );
            
            if ($result) {
                wp_send_json_success('Record deleted successfully');
            } else {
                wp_send_json_error('Failed to delete record');
            }
            break;
            
        default:
            wp_send_json_error('Invalid operation');
    }
}
```

## AJAX Security Best Practices

### Input Validation and Sanitization
```php
class SecureAjaxValidator {
    public static function validate_email($email) {
        if (!is_email($email)) {
            wp_send_json_error('Invalid email address');
        }
        return sanitize_email($email);
    }
    
    public static function validate_text($text, $max_length = 255) {
        if (strlen($text) > $max_length) {
            wp_send_json_error('Text too long');
        }
        return sanitize_text_field($text);
    }
    
    public static function validate_number($number, $min = null, $max = null) {
        if (!is_numeric($number)) {
            wp_send_json_error('Invalid number');
        }
        
        $number = floatval($number);
        
        if ($min !== null && $number < $min) {
            wp_send_json_error('Number too small');
        }
        
        if ($max !== null && $number > $max) {
            wp_send_json_error('Number too large');
        }
        
        return $number;
    }
}
```

### Rate Limiting for AJAX
```php
class AjaxRateLimiter {
    private static $limit = 10; // requests per minute
    private static $window = 60; // seconds
    
    public static function check_rate_limit($user_id = null) {
        if (!$user_id) {
            $user_id = get_current_user_id();
        }
        
        $transient_key = 'ajax_rate_limit_' . $user_id;
        $requests = get_transient($transient_key);
        
        if ($requests === false) {
            set_transient($transient_key, 1, self::$window);
            return true;
        }
        
        if ($requests >= self::$limit) {
            wp_send_json_error('Rate limit exceeded');
        }
        
        set_transient($transient_key, $requests + 1, self::$window);
        return true;
    }
}
```

## Best Practices

1. **Always use nonces** for security
2. **Validate and sanitize** all input data
3. **Check user capabilities** before processing
4. **Use proper error handling** and user feedback
5. **Implement rate limiting** to prevent abuse
6. **Use REST API** for complex operations
7. **Handle file uploads** securely
8. **Provide loading states** in JavaScript
9. **Test with different user roles**
10. **Log AJAX requests** for debugging

## Resources

- [WordPress AJAX Documentation](https://developer.wordpress.org/plugins/javascript/ajax/)
- [WordPress Nonces Documentation](https://developer.wordpress.org/plugins/security/nonces/)
- [WordPress REST API Documentation](https://developer.wordpress.org/rest-api/)