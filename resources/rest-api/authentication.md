---
difficulty: Advanced
tags: [rest, api, authentication, security]
related: [rest-api/rest-api-basics, security/capabilities]
wp_version: 4.7+
---

# WordPress REST API Authentication

Comprehensive authentication methods for WordPress REST API endpoints.

## Basic Authentication Methods

### Application Passwords

WordPress 5.6+ native authentication method.

```php
// PHP: Enable application passwords for users
function enable_application_passwords() {
    // Application passwords are enabled by default in WordPress 5.6+
    // Users can generate them in their profile page
}

// Using application passwords in requests
// Username: your_username
// Password: your_application_password (generated in profile)

// Example cURL request
$curl = curl_init();
curl_setopt_array($curl, array(
    CURLOPT_URL => 'https://example.com/wp-json/wp/v2/posts',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_USERPWD => 'username:application_password',
    CURLOPT_HTTPHEADER => array(
        'Content-Type: application/json'
    )
));
$response = curl_exec($curl);
curl_close($curl);
```

### Cookie Authentication

For logged-in users in WordPress admin or frontend.

```php
// PHP: Cookie authentication for logged-in users
function rest_api_cookie_auth() {
    // This works automatically for logged-in users
    // No additional setup required
    
    // Example AJAX request from frontend
    wp_localize_script('my-script', 'ajax_object', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('rest_api_nonce')
    ));
}

// JavaScript: Making authenticated requests
fetch('/wp-json/wp/v2/posts', {
    credentials: 'same-origin',
    headers: {
        'X-WP-Nonce': wpApiSettings.nonce
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

### Nonce Authentication

WordPress nonce-based authentication.

```php
// PHP: Nonce authentication setup
function setup_rest_nonce_auth() {
    // Add nonce to REST API responses
    add_action('rest_api_init', function() {
        wp_localize_script('wp-api', 'wpApiSettings', array(
            'root' => esc_url_raw(rest_url()),
            'nonce' => wp_create_nonce('wp_rest')
        ));
    });
}
add_action('init', 'setup_rest_nonce_auth');

// Custom nonce endpoint
function create_nonce_endpoint() {
    register_rest_route('my-plugin/v1', '/nonce', array(
        'methods' => 'GET',
        'callback' => 'get_rest_nonce',
        'permission_callback' => '__return_true'
    ));
}
add_action('rest_api_init', 'create_nonce_endpoint');

function get_rest_nonce() {
    return rest_ensure_response(array(
        'nonce' => wp_create_nonce('wp_rest'),
        'user_id' => get_current_user_id()
    ));
}
```

## Advanced Authentication Methods

### OAuth 2.0 Implementation

```php
// PHP: OAuth 2.0 server implementation
class WordPress_OAuth_Server {
    
    private $client_id;
    private $client_secret;
    private $redirect_uri;
    
    public function __construct() {
        $this->client_id = get_option('oauth_client_id');
        $this->client_secret = get_option('oauth_client_secret');
        $this->redirect_uri = get_option('oauth_redirect_uri');
    }
    
    // Authorization endpoint
    public function authorize_endpoint($request) {
        $client_id = $request->get_param('client_id');
        $redirect_uri = $request->get_param('redirect_uri');
        $response_type = $request->get_param('response_type');
        $scope = $request->get_param('scope');
        $state = $request->get_param('state');
        
        // Validate client
        if ($client_id !== $this->client_id) {
            return new WP_Error('invalid_client', 'Invalid client ID');
        }
        
        // Generate authorization code
        $auth_code = wp_generate_password(32, false);
        
        // Store authorization code temporarily
        set_transient('oauth_auth_code_' . $auth_code, array(
            'client_id' => $client_id,
            'redirect_uri' => $redirect_uri,
            'scope' => $scope,
            'user_id' => get_current_user_id(),
            'expires' => time() + 600 // 10 minutes
        ), 600);
        
        // Redirect to client with authorization code
        $redirect_url = add_query_arg(array(
            'code' => $auth_code,
            'state' => $state
        ), $redirect_uri);
        
        wp_redirect($redirect_url);
        exit;
    }
    
    // Token endpoint
    public function token_endpoint($request) {
        $grant_type = $request->get_param('grant_type');
        $code = $request->get_param('code');
        $redirect_uri = $request->get_param('redirect_uri');
        $client_id = $request->get_param('client_id');
        $client_secret = $request->get_param('client_secret');
        
        if ($grant_type !== 'authorization_code') {
            return new WP_Error('unsupported_grant_type', 'Unsupported grant type');
        }
        
        // Validate client credentials
        if ($client_id !== $this->client_id || $client_secret !== $this->client_secret) {
            return new WP_Error('invalid_client', 'Invalid client credentials');
        }
        
        // Validate authorization code
        $auth_data = get_transient('oauth_auth_code_' . $code);
        if (!$auth_data) {
            return new WP_Error('invalid_grant', 'Invalid authorization code');
        }
        
        // Generate access token
        $access_token = wp_generate_password(64, false);
        $refresh_token = wp_generate_password(64, false);
        
        // Store tokens
        set_transient('oauth_access_token_' . $access_token, array(
            'user_id' => $auth_data['user_id'],
            'scope' => $auth_data['scope'],
            'expires' => time() + 3600 // 1 hour
        ), 3600);
        
        set_transient('oauth_refresh_token_' . $refresh_token, array(
            'user_id' => $auth_data['user_id'],
            'scope' => $auth_data['scope'],
            'expires' => time() + 86400 * 30 // 30 days
        ), 86400 * 30);
        
        return rest_ensure_response(array(
            'access_token' => $access_token,
            'token_type' => 'Bearer',
            'expires_in' => 3600,
            'refresh_token' => $refresh_token,
            'scope' => $auth_data['scope']
        ));
    }
}

// Register OAuth endpoints
function register_oauth_endpoints() {
    $oauth_server = new WordPress_OAuth_Server();
    
    register_rest_route('oauth/v1', '/authorize', array(
        'methods' => 'GET',
        'callback' => array($oauth_server, 'authorize_endpoint'),
        'permission_callback' => 'is_user_logged_in'
    ));
    
    register_rest_route('oauth/v1', '/token', array(
        'methods' => 'POST',
        'callback' => array($oauth_server, 'token_endpoint'),
        'permission_callback' => '__return_true'
    ));
}
add_action('rest_api_init', 'register_oauth_endpoints');
```

### JWT Authentication

```php
// PHP: JWT authentication implementation
class WordPress_JWT_Auth {
    
    private $secret_key;
    
    public function __construct() {
        $this->secret_key = get_option('jwt_secret_key', wp_salt());
    }
    
    // Generate JWT token
    public function generate_token($user_id, $expires_in = 3600) {
        $header = json_encode(array(
            'typ' => 'JWT',
            'alg' => 'HS256'
        ));
        
        $payload = json_encode(array(
            'user_id' => $user_id,
            'iat' => time(),
            'exp' => time() + $expires_in,
            'iss' => home_url()
        ));
        
        $header_encoded = $this->base64url_encode($header);
        $payload_encoded = $this->base64url_encode($payload);
        
        $signature = hash_hmac('sha256', $header_encoded . '.' . $payload_encoded, $this->secret_key, true);
        $signature_encoded = $this->base64url_encode($signature);
        
        return $header_encoded . '.' . $payload_encoded . '.' . $signature_encoded;
    }
    
    // Validate JWT token
    public function validate_token($token) {
        $parts = explode('.', $token);
        
        if (count($parts) !== 3) {
            return false;
        }
        
        list($header_encoded, $payload_encoded, $signature_encoded) = $parts;
        
        // Verify signature
        $signature = hash_hmac('sha256', $header_encoded . '.' . $payload_encoded, $this->secret_key, true);
        $signature_expected = $this->base64url_encode($signature);
        
        if (!hash_equals($signature_expected, $signature_encoded)) {
            return false;
        }
        
        // Decode payload
        $payload = json_decode($this->base64url_decode($payload_encoded), true);
        
        // Check expiration
        if ($payload['exp'] < time()) {
            return false;
        }
        
        return $payload;
    }
    
    // Base64 URL encode
    private function base64url_encode($data) {
        return rtrim(strtr(base64_encode($data), '+/', '-_'), '=');
    }
    
    // Base64 URL decode
    private function base64url_decode($data) {
        return base64_decode(str_pad(strtr($data, '-_', '+/'), strlen($data) % 4, '=', STR_PAD_RIGHT));
    }
}

// JWT authentication middleware
function jwt_auth_middleware($result, $server, $request) {
    $auth_header = $request->get_header('authorization');
    
    if (!$auth_header) {
        return $result;
    }
    
    if (!preg_match('/Bearer\s+(.*)$/i', $auth_header, $matches)) {
        return new WP_Error('invalid_auth_header', 'Invalid authorization header');
    }
    
    $jwt_auth = new WordPress_JWT_Auth();
    $payload = $jwt_auth->validate_token($matches[1]);
    
    if (!$payload) {
        return new WP_Error('invalid_token', 'Invalid or expired token');
    }
    
    // Set current user
    wp_set_current_user($payload['user_id']);
    
    return $result;
}
add_filter('rest_authentication_errors', 'jwt_auth_middleware', 10, 3);

// JWT login endpoint
function jwt_login_endpoint($request) {
    $username = $request->get_param('username');
    $password = $request->get_param('password');
    
    $user = wp_authenticate($username, $password);
    
    if (is_wp_error($user)) {
        return $user;
    }
    
    $jwt_auth = new WordPress_JWT_Auth();
    $token = $jwt_auth->generate_token($user->ID);
    
    return rest_ensure_response(array(
        'token' => $token,
        'user' => array(
            'id' => $user->ID,
            'username' => $user->user_login,
            'email' => $user->user_email,
            'display_name' => $user->display_name
        )
    ));
}

// Register JWT login endpoint
register_rest_route('jwt/v1', '/login', array(
    'methods' => 'POST',
    'callback' => 'jwt_login_endpoint',
    'permission_callback' => '__return_true',
    'args' => array(
        'username' => array(
            'required' => true,
            'sanitize_callback' => 'sanitize_text_field'
        ),
        'password' => array(
            'required' => true,
            'sanitize_callback' => 'sanitize_text_field'
        )
    )
));
```

## Permission Callbacks

### Custom Permission Functions

```php
// PHP: Advanced permission callbacks
function check_user_can_edit_post($request) {
    $post_id = $request->get_param('id');
    
    if (!$post_id) {
        return new WP_Error('missing_post_id', 'Post ID required');
    }
    
    return current_user_can('edit_post', $post_id);
}

function check_user_can_manage_options($request) {
    return current_user_can('manage_options');
}

function check_user_can_read_private_posts($request) {
    return current_user_can('read_private_posts');
}

function check_user_owns_post($request) {
    $post_id = $request->get_param('id');
    $user_id = get_current_user_id();
    
    if (!$post_id || !$user_id) {
        return false;
    }
    
    $post = get_post($post_id);
    return $post && $post->post_author == $user_id;
}

// Conditional permissions based on request data
function check_dynamic_permission($request) {
    $action = $request->get_param('action');
    $post_type = $request->get_param('post_type');
    
    switch ($action) {
        case 'read':
            return current_user_can("read_{$post_type}");
        case 'create':
            return current_user_can("publish_{$post_type}s");
        case 'update':
            return current_user_can("edit_{$post_type}s");
        case 'delete':
            return current_user_can("delete_{$post_type}s");
        default:
            return false;
    }
}
```

### Role-Based Permissions

```php
// PHP: Role-based permission system
function check_role_permission($request) {
    $required_roles = $request->get_param('required_roles');
    $user = wp_get_current_user();
    
    if (!$user->ID) {
        return false;
    }
    
    if (!$required_roles) {
        return true; // No role restriction
    }
    
    $user_roles = $user->roles;
    $required_roles_array = is_array($required_roles) ? $required_roles : array($required_roles);
    
    return !empty(array_intersect($user_roles, $required_roles_array));
}

function check_capability_permission($request) {
    $required_capability = $request->get_param('required_capability');
    
    if (!$required_capability) {
        return true;
    }
    
    return current_user_can($required_capability);
}

// Custom capability checking
function check_custom_capability($request) {
    $post_id = $request->get_param('id');
    $action = $request->get_param('action');
    
    // Custom logic based on post meta, user meta, etc.
    $user_id = get_current_user_id();
    
    if ($action === 'edit') {
        // Check if user has custom edit permission
        $can_edit = get_user_meta($user_id, 'can_edit_posts', true);
        return !empty($can_edit);
    }
    
    return false;
}
```

## Security Best Practices

### Rate Limiting

```php
// PHP: Rate limiting implementation
class REST_API_Rate_Limiter {
    
    private $max_requests = 100;
    private $time_window = 3600; // 1 hour
    
    public function check_rate_limit($request) {
        $client_ip = $this->get_client_ip($request);
        $cache_key = 'rate_limit_' . md5($client_ip);
        
        $requests = get_transient($cache_key);
        
        if ($requests === false) {
            $requests = 0;
        }
        
        if ($requests >= $this->max_requests) {
            return new WP_Error(
                'rate_limit_exceeded',
                'Too many requests. Please try again later.',
                array('status' => 429)
            );
        }
        
        set_transient($cache_key, $requests + 1, $this->time_window);
        
        return true;
    }
    
    private function get_client_ip($request) {
        $ip = $request->get_header('x-forwarded-for');
        
        if (!$ip) {
            $ip = $request->get_header('x-real-ip');
        }
        
        if (!$ip) {
            $ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
        }
        
        return $ip;
    }
}

// Apply rate limiting to all REST API requests
function apply_rate_limiting($result, $server, $request) {
    $rate_limiter = new REST_API_Rate_Limiter();
    $rate_limit_result = $rate_limiter->check_rate_limit($request);
    
    if (is_wp_error($rate_limit_result)) {
        return $rate_limit_result;
    }
    
    return $result;
}
add_filter('rest_authentication_errors', 'apply_rate_limiting', 5, 3);
```

### Input Validation

```php
// PHP: Comprehensive input validation
function validate_rest_request($request) {
    $params = $request->get_params();
    $errors = array();
    
    foreach ($params as $key => $value) {
        // Validate based on parameter type
        switch ($key) {
            case 'email':
                if (!is_email($value)) {
                    $errors[$key] = 'Invalid email format';
                }
                break;
                
            case 'url':
                if (!filter_var($value, FILTER_VALIDATE_URL)) {
                    $errors[$key] = 'Invalid URL format';
                }
                break;
                
            case 'post_id':
                if (!is_numeric($value) || $value <= 0) {
                    $errors[$key] = 'Invalid post ID';
                }
                break;
                
            case 'date':
                if (!strtotime($value)) {
                    $errors[$key] = 'Invalid date format';
                }
                break;
        }
    }
    
    if (!empty($errors)) {
        return new WP_Error('validation_error', 'Validation failed', array(
            'status' => 400,
            'errors' => $errors
        ));
    }
    
    return true;
}

// Apply validation to specific endpoints
function validate_post_endpoint($request) {
    return validate_rest_request($request);
}

register_rest_route('my-plugin/v1', '/posts', array(
    'methods' => 'POST',
    'callback' => 'create_post',
    'permission_callback' => 'check_user_can_edit_post',
    'validate_callback' => 'validate_post_endpoint'
));
```

## Error Handling

### Secure Error Responses

```php
// PHP: Secure error handling
function handle_rest_api_errors($error, $request) {
    // Log detailed error information
    error_log(sprintf(
        'REST API Error: %s - Request: %s %s - User: %d',
        $error->get_error_message(),
        $request->get_method(),
        $request->get_route(),
        get_current_user_id()
    ));
    
    // Return sanitized error response
    $error_data = array(
        'code' => $error->get_error_code(),
        'message' => $error->get_error_message()
    );
    
    // Only include additional data in debug mode
    if (WP_DEBUG) {
        $error_data['data'] = $error->get_error_data();
    }
    
    return new WP_REST_Response($error_data, $error->get_error_data()['status'] ?? 500);
}

// Custom error handler
function custom_rest_error_handler($request) {
    try {
        // Your endpoint logic here
        return rest_ensure_response($data);
        
    } catch (Exception $e) {
        return new WP_Error(
            'internal_error',
            'An internal error occurred',
            array('status' => 500)
        );
    }
}
```

## Official Documentation

https://developer.wordpress.org/rest-api/using-the-rest-api/authentication/
https://developer.wordpress.org/rest-api/reference/
https://developer.wordpress.org/rest-api/extending-the-rest-api/
