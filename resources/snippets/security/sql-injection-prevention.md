# SQL Injection Prevention

```php
global $wpdb;

// ✅ ALWAYS use prepare()
$results = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_author = %d AND post_status = %s",
    $author_id,
    'publish'
));

// Multiple values
$results = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID IN (" . implode(',', array_fill(0, count($ids), '%d')) . ")",
    ...$ids
));

// ❌ NEVER do this
$wpdb->query( "DELETE FROM {$wpdb->posts} WHERE ID = $id" );

// ✅ Use prepare
$wpdb->query( $wpdb->prepare(
    "DELETE FROM {$wpdb->posts} WHERE ID = %d",
    $id
));
```
