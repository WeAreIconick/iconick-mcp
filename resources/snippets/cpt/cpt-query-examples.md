# Custom Post Type Queries

```php
// Basic CPT query
$args = array(
    'post_type' => 'portfolio',
    'posts_per_page' => 10,
    'orderby' => 'date',
    'order' => 'DESC'
);
$query = new WP_Query( $args );

// With custom fields
$args = array(
    'post_type' => 'product',
    'meta_key' => '_price',
    'orderby' => 'meta_value_num',
    'order' => 'ASC',
    'meta_query' => array(
        array(
            'key' => '_featured',
            'value' => '1'
        )
    )
);

// With taxonomy
$args = array(
    'post_type' => 'portfolio',
    'tax_query' => array(
        array(
            'taxonomy' => 'portfolio_cat',
            'field' => 'slug',
            'terms' => 'web-design'
        )
    )
);
```
