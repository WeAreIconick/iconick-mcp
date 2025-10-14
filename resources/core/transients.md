# WordPress Transients API

Transients provide temporary, cached data storage with automatic expiration.

## Basic Usage

```php
// Set a transient (expires in 1 hour)
set_transient( 'my_cache_key', $data, HOUR_IN_SECONDS );

// Get a transient
$data = get_transient( 'my_cache_key' );

// Delete a transient
delete_transient( 'my_cache_key' );
```

## Time Constants

```php
// WordPress time constants
MINUTE_IN_SECONDS = 60
HOUR_IN_SECONDS = 3600
DAY_IN_SECONDS = 86400
WEEK_IN_SECONDS = 604800
MONTH_IN_SECONDS = 2592000
YEAR_IN_SECONDS = 31536000

// Usage
set_transient( 'api_data', $response, HOUR_IN_SECONDS );
set_transient( 'daily_report', $report, DAY_IN_SECONDS );
```

## Common Patterns

### API Response Caching

```php
function get_weather_data( $city ) {
    $cache_key = 'weather_' . sanitize_key( $city );
    
    // Try to get cached data
    $data = get_transient( $cache_key );
    
    if ( false === $data ) {
        // Cache miss - fetch from API
        $response = wp_remote_get( "https://api.weather.com/{$city}" );
        
        if ( ! is_wp_error( $response ) ) {
            $data = json_decode( wp_remote_retrieve_body( $response ), true );
            
            // Cache for 30 minutes
            set_transient( $cache_key, $data, 30 * MINUTE_IN_SECONDS );
        }
    }
    
    return $data;
}
```

## Best Practices

### Naming Conventions

```php
// Good naming patterns
$cache_key = 'plugin_name_data_' . $identifier;
$cache_key = 'user_' . $user_id . '_posts';
$cache_key = 'api_response_' . md5( $url . serialize( $params ) );

// Bad naming (too generic)
$cache_key = 'data';
$cache_key = 'cache';
```

## Official Documentation

https://developer.wordpress.org/apis/transients/
https://developer.wordpress.org/reference/functions/set_transient/
https://developer.wordpress.org/reference/functions/get_transient/