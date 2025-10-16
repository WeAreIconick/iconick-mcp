# Custom WP_Query Examples

```php
// Recent posts with thumbnails
$query = new WP_Query( array(
    'post_type' => 'post',
    'posts_per_page' => 5,
    'meta_query' => array(
        array(
            'key' => '_thumbnail_id',
            'compare' => 'EXISTS'
        )
    )
));

// Posts by specific author
$query = new WP_Query( array(
    'author' => 2,
    'posts_per_page' => 10
));

// Posts from last 30 days
$query = new WP_Query( array(
    'date_query' => array(
        array(
            'after' => '30 days ago'
        )
    )
));

// Complex meta query
$query = new WP_Query( array(
    'post_type' => 'product',
    'meta_query' => array(
        'relation' => 'AND',
        array(
            'key' => '_price',
            'value' => array( 10, 100 ),
            'compare' => 'BETWEEN',
            'type' => 'NUMERIC'
        ),
        array(
            'key' => '_stock_status',
            'value' => 'instock'
        )
    )
));

// Search with meta
$query = new WP_Query( array(
    's' => $search_term,
    'meta_query' => array(
        array(
            'key' => '_visibility',
            'value' => 'public'
        )
    )
));

// Sticky posts
$query = new WP_Query( array(
    'post__in' => get_option( 'sticky_posts' ),
    'ignore_sticky_posts' => 1
));
```
