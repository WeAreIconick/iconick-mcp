# WordPress REST API Custom Endpoints

Creating custom REST API endpoints for your WordPress applications.

## Basic Custom Endpoint

### Simple Endpoint Registration

```php
// Register a simple custom endpoint
function register_custom_endpoint() {
    register_rest_route( 'my-plugin/v1', '/hello', array(
        'methods' => 'GET',
        'callback' => 'handle_hello_endpoint',
        'permission_callback' => '__return_true'
    ) );
}
add_action( 'rest_api_init', 'register_custom_endpoint' );

function handle_hello_endpoint( $request ) {
    $name = $request->get_param( 'name' );
    $name = $name ? sanitize_text_field( $name ) : 'World';
    
    return rest_ensure_response( array(
        'message' => "Hello, $name!",
        'timestamp' => current_time( 'mysql' )
    ) );
}
```

### Endpoint with Parameters

```php
// Endpoint with URL parameters
function register_parameterized_endpoint() {
    register_rest_route( 'my-plugin/v1', '/posts/(?P<id>\d+)', array(
        'methods' => 'GET',
        'callback' => 'handle_post_endpoint',
        'args' => array(
            'id' => array(
                'validate_callback' => function( $param, $request, $key ) {
                    return is_numeric( $param );
                }
            )
        ),
        'permission_callback' => '__return_true'
    ) );
}
add_action( 'rest_api_init', 'register_parameterized_endpoint' );

function handle_post_endpoint( $request ) {
    $post_id = $request['id'];
    $post = get_post( $post_id );
    
    if ( ! $post ) {
        return new WP_Error( 'post_not_found', 'Post not found', array( 'status' => 404 ) );
    }
    
    return rest_ensure_response( array(
        'id' => $post->ID,
        'title' => $post->post_title,
        'content' => $post->post_content,
        'excerpt' => $post->post_excerpt,
        'date' => $post->post_date,
        'status' => $post->post_status
    ) );
}
```

## Advanced Endpoint Patterns

### CRUD Operations

```php
// Complete CRUD endpoint for custom post type
function register_crud_endpoint() {
    // GET - List all items
    register_rest_route( 'my-plugin/v1', '/products', array(
        'methods' => 'GET',
        'callback' => 'get_products',
        'permission_callback' => '__return_true',
        'args' => array(
            'page' => array(
                'default' => 1,
                'sanitize_callback' => 'absint'
            ),
            'per_page' => array(
                'default' => 10,
                'sanitize_callback' => 'absint'
            ),
            'search' => array(
                'sanitize_callback' => 'sanitize_text_field'
            )
        )
    ) );
    
    // GET - Single item
    register_rest_route( 'my-plugin/v1', '/products/(?P<id>\d+)', array(
        'methods' => 'GET',
        'callback' => 'get_product',
        'permission_callback' => '__return_true',
        'args' => array(
            'id' => array(
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                }
            )
        )
    ) );
    
    // POST - Create item
    register_rest_route( 'my-plugin/v1', '/products', array(
        'methods' => 'POST',
        'callback' => 'create_product',
        'permission_callback' => 'check_create_permission',
        'args' => array(
            'title' => array(
                'required' => true,
                'sanitize_callback' => 'sanitize_text_field'
            ),
            'content' => array(
                'sanitize_callback' => 'wp_kses_post'
            ),
            'price' => array(
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                }
            )
        )
    ) );
    
    // PUT - Update item
    register_rest_route( 'my-plugin/v1', '/products/(?P<id>\d+)', array(
        'methods' => 'PUT',
        'callback' => 'update_product',
        'permission_callback' => 'check_update_permission',
        'args' => array(
            'id' => array(
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                }
            ),
            'title' => array(
                'sanitize_callback' => 'sanitize_text_field'
            ),
            'content' => array(
                'sanitize_callback' => 'wp_kses_post'
            ),
            'price' => array(
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                }
            )
        )
    ) );
    
    // DELETE - Delete item
    register_rest_route( 'my-plugin/v1', '/products/(?P<id>\d+)', array(
        'methods' => 'DELETE',
        'callback' => 'delete_product',
        'permission_callback' => 'check_delete_permission',
        'args' => array(
            'id' => array(
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                }
            )
        )
    ) );
}
add_action( 'rest_api_init', 'register_crud_endpoint' );

// CRUD callback functions
function get_products( $request ) {
    $page = $request->get_param( 'page' );
    $per_page = $request->get_param( 'per_page' );
    $search = $request->get_param( 'search' );
    
    $args = array(
        'post_type' => 'product',
        'posts_per_page' => $per_page,
        'paged' => $page,
        'post_status' => 'publish'
    );
    
    if ( $search ) {
        $args['s'] = $search;
    }
    
    $posts = get_posts( $args );
    $total_posts = wp_count_posts( 'product' )->publish;
    
    $products = array();
    foreach ( $posts as $post ) {
        $products[] = format_product_response( $post );
    }
    
    return rest_ensure_response( array(
        'products' => $products,
        'total' => $total_posts,
        'pages' => ceil( $total_posts / $per_page )
    ) );
}

function get_product( $request ) {
    $post_id = $request['id'];
    $post = get_post( $post_id );
    
    if ( ! $post || $post->post_type !== 'product' ) {
        return new WP_Error( 'product_not_found', 'Product not found', array( 'status' => 404 ) );
    }
    
    return rest_ensure_response( format_product_response( $post ) );
}

function create_product( $request ) {
    $title = $request->get_param( 'title' );
    $content = $request->get_param( 'content' );
    $price = $request->get_param( 'price' );
    
    $post_data = array(
        'post_title' => $title,
        'post_content' => $content,
        'post_type' => 'product',
        'post_status' => 'publish'
    );
    
    $post_id = wp_insert_post( $post_data );
    
    if ( is_wp_error( $post_id ) ) {
        return new WP_Error( 'creation_failed', 'Failed to create product', array( 'status' => 500 ) );
    }
    
    if ( $price ) {
        update_post_meta( $post_id, 'price', floatval( $price ) );
    }
    
    $post = get_post( $post_id );
    return rest_ensure_response( format_product_response( $post ), 201 );
}

function update_product( $request ) {
    $post_id = $request['id'];
    $post = get_post( $post_id );
    
    if ( ! $post || $post->post_type !== 'product' ) {
        return new WP_Error( 'product_not_found', 'Product not found', array( 'status' => 404 ) );
    }
    
    $title = $request->get_param( 'title' );
    $content = $request->get_param( 'content' );
    $price = $request->get_param( 'price' );
    
    $post_data = array(
        'ID' => $post_id
    );
    
    if ( $title ) {
        $post_data['post_title'] = $title;
    }
    
    if ( $content ) {
        $post_data['post_content'] = $content;
    }
    
    $updated = wp_update_post( $post_data );
    
    if ( is_wp_error( $updated ) ) {
        return new WP_Error( 'update_failed', 'Failed to update product', array( 'status' => 500 ) );
    }
    
    if ( $price !== null ) {
        update_post_meta( $post_id, 'price', floatval( $price ) );
    }
    
    $post = get_post( $post_id );
    return rest_ensure_response( format_product_response( $post ) );
}

function delete_product( $request ) {
    $post_id = $request['id'];
    $post = get_post( $post_id );
    
    if ( ! $post || $post->post_type !== 'product' ) {
        return new WP_Error( 'product_not_found', 'Product not found', array( 'status' => 404 ) );
    }
    
    $deleted = wp_delete_post( $post_id, true );
    
    if ( ! $deleted ) {
        return new WP_Error( 'delete_failed', 'Failed to delete product', array( 'status' => 500 ) );
    }
    
    return rest_ensure_response( array(
        'message' => 'Product deleted successfully',
        'id' => $post_id
    ) );
}

// Helper function to format product response
function format_product_response( $post ) {
    return array(
        'id' => $post->ID,
        'title' => $post->post_title,
        'content' => $post->post_content,
        'excerpt' => $post->post_excerpt,
        'price' => get_post_meta( $post->ID, 'price', true ),
        'featured' => get_post_meta( $post->ID, 'featured', true ),
        'date' => $post->post_date,
        'modified' => $post->post_modified,
        'status' => $post->post_status,
        'link' => get_permalink( $post->ID )
    );
}
```

## Permission Callbacks

### Custom Permission Functions

```php
// Permission callback functions
function check_create_permission() {
    return current_user_can( 'edit_posts' );
}

function check_update_permission( $request ) {
    $post_id = $request['id'];
    return current_user_can( 'edit_post', $post_id );
}

function check_delete_permission( $request ) {
    $post_id = $request['id'];
    return current_user_can( 'delete_post', $post_id );
}

// Advanced permission callback
function check_admin_permission() {
    return current_user_can( 'manage_options' );
}

function check_author_permission( $request ) {
    if ( ! is_user_logged_in() ) {
        return false;
    }
    
    $user_id = get_current_user_id();
    $post_id = $request->get_param( 'id' );
    
    if ( $post_id ) {
        $post = get_post( $post_id );
        return $post && $post->post_author == $user_id;
    }
    
    return true;
}

// Conditional permission based on request data
function check_dynamic_permission( $request ) {
    $action = $request->get_param( 'action' );
    
    switch ( $action ) {
        case 'read':
            return true; // Public read access
        case 'create':
            return current_user_can( 'edit_posts' );
        case 'update':
            return current_user_can( 'edit_others_posts' );
        case 'delete':
            return current_user_can( 'delete_others_posts' );
        default:
            return false;
    }
}
```

## Schema Definition

### Comprehensive Schema

```php
// Define schema for endpoint
function get_product_schema() {
    return array(
        '$schema' => 'http://json-schema.org/draft-04/schema#',
        'title' => 'Product',
        'type' => 'object',
        'properties' => array(
            'id' => array(
                'description' => 'Unique identifier for the product',
                'type' => 'integer',
                'readonly' => true
            ),
            'title' => array(
                'description' => 'Product title',
                'type' => 'string',
                'context' => array( 'view', 'edit' ),
                'arg_options' => array(
                    'sanitize_callback' => 'sanitize_text_field'
                )
            ),
            'content' => array(
                'description' => 'Product description',
                'type' => 'string',
                'context' => array( 'view', 'edit' ),
                'arg_options' => array(
                    'sanitize_callback' => 'wp_kses_post'
                )
            ),
            'price' => array(
                'description' => 'Product price',
                'type' => 'number',
                'context' => array( 'view', 'edit' ),
                'arg_options' => array(
                    'validate_callback' => function( $param ) {
                        return is_numeric( $param );
                    }
                )
            ),
            'featured' => array(
                'description' => 'Whether product is featured',
                'type' => 'boolean',
                'context' => array( 'view', 'edit' ),
                'arg_options' => array(
                    'sanitize_callback' => 'rest_sanitize_boolean'
                )
            ),
            'categories' => array(
                'description' => 'Product categories',
                'type' => 'array',
                'items' => array(
                    'type' => 'object',
                    'properties' => array(
                        'id' => array( 'type' => 'integer' ),
                        'name' => array( 'type' => 'string' ),
                        'slug' => array( 'type' => 'string' )
                    )
                ),
                'context' => array( 'view', 'edit' )
            ),
            'date' => array(
                'description' => 'Product creation date',
                'type' => 'string',
                'format' => 'date-time',
                'context' => array( 'view', 'edit' ),
                'readonly' => true
            )
        )
    );
}

// Register endpoint with schema
function register_schema_endpoint() {
    register_rest_route( 'my-plugin/v1', '/products/(?P<id>\d+)', array(
        'methods' => 'GET',
        'callback' => 'get_product',
        'permission_callback' => '__return_true',
        'schema' => 'get_product_schema'
    ) );
}
add_action( 'rest_api_init', 'register_schema_endpoint' );
```

## Error Handling

### Comprehensive Error Handling

```php
// Advanced error handling
function handle_robust_endpoint( $request ) {
    try {
        // Validate request
        $validation_result = validate_request( $request );
        if ( is_wp_error( $validation_result ) ) {
            return $validation_result;
        }
        
        // Process request
        $result = process_request( $request );
        
        if ( is_wp_error( $result ) ) {
            return $result;
        }
        
        return rest_ensure_response( $result );
        
    } catch ( Exception $e ) {
        // Log error
        error_log( 'REST API Error: ' . $e->getMessage() );
        
        // Return appropriate error
        return new WP_Error( 
            'internal_error', 
            'An internal error occurred', 
            array( 'status' => 500 ) 
        );
    }
}

function validate_request( $request ) {
    $required_params = array( 'title', 'content' );
    
    foreach ( $required_params as $param ) {
        if ( empty( $request->get_param( $param ) ) ) {
            return new WP_Error( 
                'missing_param', 
                "Missing required parameter: $param", 
                array( 'status' => 400 ) 
            );
        }
    }
    
    return true;
}

function process_request( $request ) {
    // Complex processing logic here
    $data = $request->get_json_params();
    
    if ( ! $data ) {
        return new WP_Error( 
            'invalid_json', 
            'Invalid JSON data', 
            array( 'status' => 400 ) 
        );
    }
    
    // Process data
    return array( 'success' => true, 'data' => $data );
}
```

## Advanced Features

### Batch Operations

```php
// Batch endpoint for multiple operations
function register_batch_endpoint() {
    register_rest_route( 'my-plugin/v1', '/batch', array(
        'methods' => 'POST',
        'callback' => 'handle_batch_request',
        'permission_callback' => 'check_batch_permission',
        'args' => array(
            'operations' => array(
                'required' => true,
                'validate_callback' => function( $param ) {
                    return is_array( $param );
                }
            )
        )
    ) );
}
add_action( 'rest_api_init', 'register_batch_endpoint' );

function handle_batch_request( $request ) {
    $operations = $request->get_param( 'operations' );
    $results = array();
    
    foreach ( $operations as $operation ) {
        $result = process_batch_operation( $operation );
        $results[] = array(
            'operation' => $operation,
            'result' => $result
        );
    }
    
    return rest_ensure_response( array(
        'results' => $results,
        'total' => count( $operations )
    ) );
}

function process_batch_operation( $operation ) {
    $action = $operation['action'];
    $data = $operation['data'];
    
    switch ( $action ) {
        case 'create':
            return create_product( new WP_REST_Request( 'POST', '', $data ) );
        case 'update':
            return update_product( new WP_REST_Request( 'PUT', '', $data ) );
        case 'delete':
            return delete_product( new WP_REST_Request( 'DELETE', '', $data ) );
        default:
            return new WP_Error( 'invalid_action', 'Invalid action' );
    }
}
```

### Caching Integration

```php
// Endpoint with caching
function register_cached_endpoint() {
    register_rest_route( 'my-plugin/v1', '/cached-data', array(
        'methods' => 'GET',
        'callback' => 'get_cached_data',
        'permission_callback' => '__return_true',
        'args' => array(
            'cache_time' => array(
                'default' => 3600,
                'sanitize_callback' => 'absint'
            )
        )
    ) );
}
add_action( 'rest_api_init', 'register_cached_endpoint' );

function get_cached_data( $request ) {
    $cache_key = 'rest_cache_' . md5( serialize( $request->get_params() ) );
    $cache_time = $request->get_param( 'cache_time' );
    
    // Try to get cached data
    $cached_data = get_transient( $cache_key );
    
    if ( false === $cached_data ) {
        // Generate fresh data
        $data = generate_expensive_data();
        
        // Cache the data
        set_transient( $cache_key, $data, $cache_time );
        
        $cached_data = $data;
    }
    
    return rest_ensure_response( array(
        'data' => $cached_data,
        'cached' => true,
        'cache_time' => $cache_time
    ) );
}

function generate_expensive_data() {
    // Simulate expensive operation
    sleep( 2 );
    
    return array(
        'expensive_data' => 'This took time to generate',
        'timestamp' => current_time( 'mysql' )
    );
}
```

## Best Practices

### Security

```php
// Secure endpoint implementation
function secure_endpoint_handler( $request ) {
    // Rate limiting check
    if ( ! check_rate_limit( $request ) ) {
        return new WP_Error( 
            'rate_limit_exceeded', 
            'Too many requests', 
            array( 'status' => 429 ) 
        );
    }
    
    // Input validation
    $params = $request->get_params();
    $sanitized_params = array();
    
    foreach ( $params as $key => $value ) {
        $sanitized_params[ $key ] = sanitize_text_field( $value );
    }
    
    // Process with sanitized data
    return process_secure_request( $sanitized_params );
}

function check_rate_limit( $request ) {
    $ip = $request->get_header( 'x-forwarded-for' ) ?: $_SERVER['REMOTE_ADDR'];
    $cache_key = 'rate_limit_' . md5( $ip );
    
    $requests = get_transient( $cache_key ) ?: 0;
    
    if ( $requests >= 100 ) { // 100 requests per hour
        return false;
    }
    
    set_transient( $cache_key, $requests + 1, HOUR_IN_SECONDS );
    return true;
}
```

## Official Documentation

https://developer.wordpress.org/rest-api/extending-the-rest-api/
https://developer.wordpress.org/reference/functions/register_rest_route/
https://developer.wordpress.org/rest-api/reference/
