---
difficulty: Beginner
tags: [database, transients, cache, performance]
related: [performance/caching-transients, performance/object-cache]
use_case: Caching data with transients
---

# Transients for Caching

```php
// Basic transient usage
function get_cached_api_data() {
    $cache_key = 'api_data_response';
    $data = get_transient( $cache_key );
    
    if ( false === $data ) {
        // Data not in cache, fetch it
        $response = wp_remote_get( 'https://api.example.com/data' );
        
        if ( ! is_wp_error( $response ) ) {
            $data = json_decode( wp_remote_retrieve_body( $response ), true );
            // Cache for 1 hour
            set_transient( $cache_key, $data, HOUR_IN_SECONDS );
        }
    }
    
    return $data;
}

// User-specific transients
function get_user_cached_data( $user_id ) {
    $cache_key = 'user_data_' . $user_id;
    $data = get_transient( $cache_key );
    
    if ( false === $data ) {
        $data = expensive_user_query( $user_id );
        set_transient( $cache_key, $data, DAY_IN_SECONDS );
    }
    
    return $data;
}

// Delete transient when data changes
add_action( 'save_post', 'clear_post_cache' );
function clear_post_cache( $post_id ) {
    delete_transient( 'recent_posts' );
    delete_transient( 'post_count' );
}

// Cache expensive query
function get_popular_posts() {
    $cache_key = 'popular_posts_week';
    $posts = get_transient( $cache_key );
    
    if ( false === $posts ) {
        $posts = get_posts( array(
            'meta_key' => 'views',
            'orderby' => 'meta_value_num',
            'posts_per_page' => 10
        ));
        
        set_transient( $cache_key, $posts, WEEK_IN_SECONDS );
    }
    
    return $posts;
}

// Multisite: Site transients
set_site_transient( 'network_data', $data, DAY_IN_SECONDS );
$data = get_site_transient( 'network_data' );
delete_site_transient( 'network_data' );
```
