# REST API Authentication

```php
// Application Password (Built-in)
// Users > Profile > Application Passwords

// JavaScript with authentication
fetch('https://example.com/wp-json/wp/v2/posts', {
    method: 'POST',
    headers: {
        'Authorization': 'Basic ' + btoa(username + ':' + app_password),
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        title: 'New Post',
        content: 'Post content',
        status: 'draft'
    })
});

// Custom authentication callback
register_rest_route( 'myplugin/v1', '/secure', array(
    'methods' => 'POST',
    'callback' => 'my_secure_endpoint',
    'permission_callback' => function() {
        // Custom auth check
        $api_key = isset( $_SERVER['HTTP_X_API_KEY'] ) ? 
                   sanitize_text_field( $_SERVER['HTTP_X_API_KEY'] ) : '';
        
        return validate_api_key( $api_key );
    }
));
```
