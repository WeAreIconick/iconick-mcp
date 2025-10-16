# Caching with Transients

```php
// Get cached data
$data = get_transient( 'my_cached_data' );

if ( false === $data ) {
    // Data not in cache, fetch it
    $data = expensive_database_query();
    
    // Cache for 1 hour
    set_transient( 'my_cached_data', $data, HOUR_IN_SECONDS );
}

// Use the data
foreach ( $data as $item ) {
    echo esc_html( $item->title );
}

// Delete transient
delete_transient( 'my_cached_data' );

// Cache external API
function get_api_data() {
    $cache_key = 'api_data_' . md5( $api_url );
    $data = get_transient( $cache_key );
    
    if ( false === $data ) {
        $response = wp_remote_get( $api_url );
        
        if ( ! is_wp_error( $response ) ) {
            $data = json_decode( wp_remote_retrieve_body( $response ), true );
            set_transient( $cache_key, $data, 15 * MINUTE_IN_SECONDS );
        }
    }
    
    return $data;
}
```
