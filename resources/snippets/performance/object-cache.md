# Object Caching

```php
// Get from cache
$data = wp_cache_get( 'my_data', 'my_group' );

if ( false === $data ) {
    // Not in cache, generate it
    $data = get_posts( array( 'posts_per_page' => 100 ) );
    
    // Cache it (no expiration - cleared on each request unless persistent caching)
    wp_cache_set( 'my_data', 'my_group', $data );
}

// Delete from cache
wp_cache_delete( 'my_data', 'my_group' );

// Flush entire cache
wp_cache_flush();

// Cache post data
function get_cached_post_data( $post_id ) {
    $cache_key = 'post_data_' . $post_id;
    $data = wp_cache_get( $cache_key, 'posts' );
    
    if ( false === $data ) {
        $post = get_post( $post_id );
        $data = array(
            'title' => $post->post_title,
            'content' => $post->post_content,
            'meta' => get_post_meta( $post_id )
        );
        
        wp_cache_set( $cache_key, $data, 'posts', 3600 );
    }
    
    return $data;
}
```
