# Optimize WordPress Queries

```php
// ❌ INEFFICIENT
$posts = get_posts( array( 'posts_per_page' => -1 ) );

// ✅ OPTIMIZED
$posts = get_posts( array(
    'posts_per_page' => 20,
    'fields' => 'ids',  // Only get IDs
    'no_found_rows' => true,  // Skip pagination count
    'update_post_meta_cache' => false,  // Skip meta if not needed
    'update_post_term_cache' => false   // Skip terms if not needed
));

// Pre-fetch meta data to avoid N+1
$posts = get_posts( array( 'post_type' => 'product' ) );
update_post_meta_cache( wp_list_pluck( $posts, 'ID' ) );

foreach ( $posts as $post ) {
    // Now get_post_meta is cached
    $price = get_post_meta( $post->ID, '_price', true );
}

// Use WP_Query for complex queries
$query = new WP_Query( array(
    'post_type' => 'product',
    'posts_per_page' => 10,
    'meta_query' => array(
        array(
            'key' => '_stock_status',
            'value' => 'instock'
        )
    ),
    'tax_query' => array(
        array(
            'taxonomy' => 'product_cat',
            'field' => 'slug',
            'terms' => 'electronics'
        )
    )
));

// Cache complex queries
function get_featured_products() {
    $cache_key = 'featured_products';
    $products = wp_cache_get( $cache_key, 'products' );
    
    if ( false === $products ) {
        $products = get_posts( array(
            'post_type' => 'product',
            'meta_key' => '_featured',
            'meta_value' => 'yes',
            'posts_per_page' => 10
        ));
        
        wp_cache_set( $cache_key, $products, 'products', 3600 );
    }
    
    return $products;
}
```
