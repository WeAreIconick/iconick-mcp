# WordPress HTTP API

The WordPress HTTP API provides a safe and standardized way to make HTTP requests.

## Basic GET Request

```php
$response = wp_remote_get( 'https://api.example.com/data' );

if ( is_wp_error( $response ) ) {
    $error_message = $response->get_error_message();
    echo "Something went wrong: $error_message";
} else {
    $body = wp_remote_retrieve_body( $response );
    $data = json_decode( $body );
}
```

## POST Request

```php
$response = wp_remote_post( 'https://api.example.com/endpoint', array(
    'body' => array(
        'key1' => 'value1',
        'key2' => 'value2'
    ),
    'headers' => array(
        'Content-Type' => 'application/json',
    ),
    'timeout' => 45,
) );
```

## Request with Headers

```php
$response = wp_remote_get( 'https://api.example.com/data', array(
    'headers' => array(
        'Authorization' => 'Bearer ' . $api_token,
        'Accept' => 'application/json',
    ),
    'timeout' => 30,
) );
```

## Response Handling

```php
// Get status code
$status_code = wp_remote_retrieve_response_code( $response );

// Get response body
$body = wp_remote_retrieve_body( $response );

// Get specific header
$header = wp_remote_retrieve_header( $response, 'content-type' );

// Get all headers
$headers = wp_remote_retrieve_headers( $response );

// Get response message
$message = wp_remote_retrieve_response_message( $response );
```

## Available Methods

```php
// GET
wp_remote_get( $url, $args );

// POST
wp_remote_post( $url, $args );

// HEAD
wp_remote_head( $url, $args );

// PUT
wp_remote_request( $url, array( 'method' => 'PUT', ...
$args ) );

// DELETE
wp_remote_request( $url, array( 'method' => 'DELETE', ...$args ) );
```

## Request Arguments

```php
$args = array(
    'method'      => 'GET',
    'timeout'     => 45,
    'redirection' => 5,
    'httpversion' => '1.0',
    'blocking'    => true,
    'headers'     => array(
        'Authorization' => 'Bearer token',
        'Content-Type'  => 'application/json',
    ),
    'body'        => array( 'key' => 'value' ),
    'cookies'     => array(),
    'sslverify'   => true,
);

$response = wp_remote_request( $url, $args );
```

## JSON API Example

```php
function fetch_api_data() {
    $response = wp_remote_get( 'https://api.example.com/v1/posts', array(
        'headers' => array(
            'Authorization' => 'Bearer ' . get_option( 'api_token' ),
        ),
        'timeout' => 30,
    ) );
    
    if ( is_wp_error( $response ) ) {
        return false;
    }
    
    $code = wp_remote_retrieve_response_code( $response );
    
    if ( $code !== 200 ) {
        return false;
    }
    
    $body = wp_remote_retrieve_body( $response );
    $data = json_decode( $body, true );
    
    return $data;
}
```

## Error Handling

```php
$response = wp_remote_get( $url );

if ( is_wp_error( $response ) ) {
    $error_code = $response->get_error_code();
    $error_message = $response->get_error_message();
    
    error_log( "HTTP Error [{$error_code}]: {$error_message}" );
    
    return false;
}

// Check HTTP status
$status = wp_remote_retrieve_response_code( $response );

if ( $status !== 200 ) {
    error_log( "HTTP request returned status: {$status}" );
    return false;
}
```

## File Download

```php
function download_remote_file( $url, $destination ) {
    $response = wp_remote_get( $url, array(
        'timeout' => 300,
        'stream' => true,
        'filename' => $destination
    ) );
    
    if ( is_wp_error( $response ) ) {
        return false;
    }
    
    return true;
}
```

## Best Practices

1. **Always check for errors** with `is_wp_error()`
2. **Set appropriate timeouts** (default is 5 seconds)
3. **Verify SSL certificates** in production (`sslverify => true`)
4. **Use transients** to cache API responses
5. **Handle rate limiting** with appropriate delays
6. **Log errors** for debugging
7. **Validate and sanitize** response data
8. **Use wp_safe_remote_get()** for user-provided URLs

## Caching API Responses

```php
function get_cached_api_data() {
    $cache_key = 'api_data_' . md5( $url );
    $cached = get_transient( $cache_key );
    
    if ( false !== $cached ) {
        return $cached;
    }
    
    $response = wp_remote_get( $url );
    
    if ( is_wp_error( $response ) ) {
        return false;
    }
    
    $data = json_decode( wp_remote_retrieve_body( $response ), true );
    
    // Cache for 1 hour
    set_transient( $cache_key, $data, HOUR_IN_SECONDS );
    
    return $data;
}
```

## Security Considerations

1. **Sanitize URLs** from user input
2. **Validate SSL certificates** unless explicitly disabled
3. **Use wp_safe_remote_*()** functions for untrusted URLs
4. **Don't expose API keys** in client-side code
5. **Rate limit** your own API calls
6. **Timeout protection** to prevent hanging requests

## Official Documentation

https://developer.wordpress.org/plugins/http-api/
https://developer.wordpress.org/reference/functions/wp_remote_get/
https://developer.wordpress.org/reference/functions/wp_remote_post/
