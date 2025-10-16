# $wpdb Query Examples

```php
global $wpdb;

// Get results
$results = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_status = %s",
    'publish'
));

// Get single row
$post = $wpdb->get_row( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
    $post_id
));

// Get single variable
$count = $wpdb->get_var(
    "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'post'"
);

// Get column
$titles = $wpdb->get_col(
    "SELECT post_title FROM {$wpdb->posts} WHERE post_status = 'publish' LIMIT 10"
);

// Insert
$wpdb->insert(
    $wpdb->prefix . 'my_table',
    array(
        'column1' => 'value1',
        'column2' => 123
    ),
    array( '%s', '%d' )
);
$insert_id = $wpdb->insert_id;

// Update
$wpdb->update(
    $wpdb->posts,
    array( 'post_status' => 'draft' ),
    array( 'ID' => $post_id ),
    array( '%s' ),
    array( '%d' )
);

// Delete
$wpdb->delete(
    $wpdb->postmeta,
    array( 'post_id' => $post_id ),
    array( '%d' )
);
```
