# WordPress REST API Basics

The WordPress REST API provides endpoints for accessing and modifying WordPress content.

## Basic Concepts

```php
// REST API endpoints follow this pattern:
// GET  /wp-json/wp/v2/posts          - List posts
// GET  /wp-json/wp/v2/posts/123      - Get specific post
// POST /wp-json/wp/v2/posts          - Create new post
// PUT  /wp-json/wp/v2/posts/123      - Update post
// DELETE /wp-json/wp/v2/posts/123    - Delete post
```

## Authentication

### Application Passwords (WordPress 5.6+)

```php
// Create application password in WordPress admin
// Use in requests:
$headers = array(
    'Authorization' => 'Basic ' . base64_encode( $username . ':' . $app_password ),
    'Content-Type' => 'application/json'
);

$response = wp_remote_get( 'https://example.com/wp-json/wp/v2/posts', array(
    'headers' => $headers
) );
```

### Nonce Authentication

```php
// For logged-in users
$nonce = wp_create_nonce( 'wp_rest' );
$headers = array(
    'X-WP-Nonce' => $nonce
);
```

## Common Endpoints

### Posts

```php
// Get all posts
GET /wp-json/wp/v2/posts

// Get specific post
GET /wp-json/wp/v2/posts/123

// Create new post
POST /wp-json/wp/v2/posts
{
    "title": "New Post",
    "content": "Post content here",
    "status": "publish"
}

// Update post
PUT /wp-json/wp/v2/posts/123
{
    "title": "Updated Title"
}

// Delete post
DELETE /wp-json/wp/v2/posts/123
```

### Pages

```php
// Get all pages
GET /wp-json/wp/v2/pages

// Get specific page
GET /wp-json/wp/v2/pages/456

// Create new page
POST /wp-json/wp/v2/pages
{
    "title": "New Page",
    "content": "Page content",
    "status": "publish"
}
```

### Users

```php
// Get all users
GET /wp-json/wp/v2/users

// Get current user
GET /wp-json/wp/v2/users/me

// Get specific user
GET /wp-json/wp/v2/users/1
```

### Media

```php
// Upload media
POST /wp-json/wp/v2/media
Content-Type: multipart/form-data

// Get media
GET /wp-json/wp/v2/media/789
```

## Query Parameters

### Pagination

```php
// Pagination parameters
GET /wp-json/wp/v2/posts?page=2&per_page=10

// Response includes pagination headers:
// X-WP-Total: 100
// X-WP-TotalPages: 10
```

### Filtering

```php
// Filter posts
GET /wp-json/wp/v2/posts?categories=1,2&tags=3
GET /wp-json/wp/v2/posts?author=1
GET /wp-json/wp/v2/posts?status=publish
GET /wp-json/wp/v2/posts?search=keyword

// Date filtering
GET /wp-json/wp/v2/posts?after=2023-01-01T00:00:00
GET /wp-json/wp/v2/posts?before=2023-12-31T23:59:59
```

### Ordering

```php
// Order posts
GET /wp-json/wp/v2/posts?orderby=date&order=desc
GET /wp-json/wp/v2/posts?orderby=title&order=asc
```

## Custom Endpoints

### Register Custom Route

```php
// Register custom endpoint
function register_custom_endpoint() {
    register_rest_route( 'my-plugin/v1', '/products', array(
        'methods' => 'GET',
        'callback' => 'get_products',
        'permission_callback' => '__return_true'
    ) );
}
add_action( 'rest_api_init', 'register_custom_endpoint' );

// Callback function
function get_products( $request ) {
    $products = get_posts( array(
        'post_type' => 'product',
        'posts_per_page' => -1
    ) );
    
    return rest_ensure_response( $products );
}
```

### Endpoint with Parameters

```php
// Endpoint with parameters
function register_product_endpoint() {
    register_rest_route( 'my-plugin/v1', '/products/(?P<id>\d+)', array(
        'methods' => 'GET',
        'callback' => 'get_product',
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
add_action( 'rest_api_init', 'register_product_endpoint' );

function get_product( $request ) {
    $product_id = $request['id'];
    $product = get_post( $product_id );
    
    if ( ! $product ) {
        return new WP_Error( 'product_not_found', 'Product not found', array( 'status' => 404 ) );
    }
    
    return rest_ensure_response( $product );
}
```

## Schema Definition

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
                'context' => array( 'view', 'edit' )
            ),
            'price' => array(
                'description' => 'Product price',
                'type' => 'number',
                'context' => array( 'view', 'edit' )
            ),
            'featured' => array(
                'description' => 'Whether product is featured',
                'type' => 'boolean',
                'context' => array( 'view', 'edit' )
            )
        )
    );
}

// Use schema in endpoint registration
register_rest_route( 'my-plugin/v1', '/products', array(
    'methods' => 'GET',
    'callback' => 'get_products',
    'schema' => 'get_product_schema'
) );
```

## Permission Callbacks

```php
// Check if user can edit posts
function can_edit_posts() {
    return current_user_can( 'edit_posts' );
}

// Check if user is logged in
function is_user_logged_in() {
    return is_user_logged_in();
}

// Custom permission check
function can_access_product( $request ) {
    $product_id = $request['id'];
    $product = get_post( $product_id );
    
    if ( ! $product ) {
        return false;
    }
    
    // Custom logic here
    return current_user_can( 'read_product', $product_id );
}

// Use in endpoint registration
register_rest_route( 'my-plugin/v1', '/products/(?P<id>\d+)', array(
    'methods' => 'GET',
    'callback' => 'get_product',
    'permission_callback' => 'can_access_product'
) );
```

## Error Handling

```php
// Return custom error
function get_product_with_error_handling( $request ) {
    $product_id = $request['id'];
    
    if ( ! is_numeric( $product_id ) ) {
        return new WP_Error( 'invalid_id', 'Invalid product ID', array( 'status' => 400 ) );
    }
    
    $product = get_post( $product_id );
    
    if ( ! $product ) {
        return new WP_Error( 'product_not_found', 'Product not found', array( 'status' => 404 ) );
    }
    
    if ( $product->post_type !== 'product' ) {
        return new WP_Error( 'invalid_product', 'Not a product', array( 'status' => 400 ) );
    }
    
    return rest_ensure_response( $product );
}
```

## Response Formatting

```php
// Format response data
function format_product_response( $product ) {
    return array(
        'id' => $product->ID,
        'title' => $product->post_title,
        'content' => $product->post_content,
        'price' => get_post_meta( $product->ID, 'price', true ),
        'featured' => get_post_meta( $product->ID, 'featured', true ),
        'date' => $product->post_date,
        'modified' => $product->post_modified
    );
}

function get_products_formatted( $request ) {
    $products = get_posts( array(
        'post_type' => 'product',
        'posts_per_page' => 10
    ) );
    
    $formatted_products = array_map( 'format_product_response', $products );
    
    return rest_ensure_response( $formatted_products );
}
```

## CORS and Headers

```php
// Enable CORS
function add_cors_http_header() {
    header( 'Access-Control-Allow-Origin: *' );
    header( 'Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS' );
    header( 'Access-Control-Allow-Headers: Authorization, Content-Type' );
}

add_action( 'rest_api_init', function() {
    remove_filter( 'rest_pre_serve_request', 'rest_send_cors_headers' );
    add_filter( 'rest_pre_serve_request', 'add_cors_http_header' );
} );
```

## Best Practices

### Security

```php
// Always validate and sanitize input
function validate_product_data( $request ) {
    $data = $request->get_json_params();
    
    // Validate required fields
    if ( empty( $data['title'] ) ) {
        return new WP_Error( 'missing_title', 'Title is required', array( 'status' => 400 ) );
    }
    
    // Sanitize data
    $sanitized_data = array(
        'title' => sanitize_text_field( $data['title'] ),
        'content' => wp_kses_post( $data['content'] ),
        'price' => floatval( $data['price'] )
    );
    
    return $sanitized_data;
}
```

### Performance

```php
// Limit response size
function get_products_with_limit( $request ) {
    $per_page = $request->get_param( 'per_page' );
    $per_page = min( $per_page ?: 10, 100 ); // Max 100 items
    
    $products = get_posts( array(
        'post_type' => 'product',
        'posts_per_page' => $per_page
    ) );
    
    return rest_ensure_response( $products );
}
```

## Official Documentation

https://developer.wordpress.org/rest-api/
https://developer.wordpress.org/rest-api/reference/
https://developer.wordpress.org/rest-api/extending-the-rest-api/
