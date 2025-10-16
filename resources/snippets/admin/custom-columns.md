# Custom Admin Columns

```php
// Add custom column
add_filter( 'manage_posts_columns', 'add_custom_columns' );
function add_custom_columns( $columns ) {
    $columns['featured_image'] = __( 'Image', 'textdomain' );
    $columns['word_count'] = __( 'Word Count', 'textdomain' );
    return $columns;
}

// Populate custom column
add_action( 'manage_posts_custom_column', 'populate_custom_columns', 10, 2 );
function populate_custom_columns( $column, $post_id ) {
    switch ( $column ) {
        case 'featured_image':
            $thumbnail = get_the_post_thumbnail( $post_id, array( 50, 50 ) );
            echo $thumbnail ? $thumbnail : '—';
            break;
            
        case 'word_count':
            $content = get_post_field( 'post_content', $post_id );
            $word_count = str_word_count( strip_tags( $content ) );
            echo number_format( $word_count );
            break;
    }
}

// Make column sortable
add_filter( 'manage_edit-post_sortable_columns', 'make_columns_sortable' );
function make_columns_sortable( $columns ) {
    $columns['word_count'] = 'word_count';
    return $columns;
}

// Custom column for CPT
add_filter( 'manage_product_posts_columns', 'product_columns' );
function product_columns( $columns ) {
    $columns['price'] = 'Price';
    $columns['sku'] = 'SKU';
    $columns['stock'] = 'Stock';
    return $columns;
}

add_action( 'manage_product_posts_custom_column', 'product_column_content', 10, 2 );
function product_column_content( $column, $post_id ) {
    switch ( $column ) {
        case 'price':
            echo '$' . esc_html( get_post_meta( $post_id, '_price', true ) );
            break;
        case 'sku':
            echo esc_html( get_post_meta( $post_id, '_sku', true ) );
            break;
        case 'stock':
            $stock = get_post_meta( $post_id, '_stock_status', true );
            echo $stock === 'instock' ? '✅ In Stock' : '❌ Out of Stock';
            break;
    }
}
```
