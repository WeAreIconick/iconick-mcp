---
difficulty: Advanced
tags: [database, tables, schema, sql]
related: [database/wpdb-queries]
use_case: Creating custom database tables
---

# Custom Database Tables

```php
// Create custom table
function create_custom_table() {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'my_analytics';
    $charset_collate = $wpdb->get_charset_collate();
    
    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        user_id bigint(20) NOT NULL,
        event_type varchar(50) NOT NULL,
        event_data text,
        created_at datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY  (id),
        KEY user_id (user_id),
        KEY event_type (event_type)
    ) $charset_collate;";
    
    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );
}
register_activation_hook( __FILE__, 'create_custom_table' );

// Insert data
global $wpdb;
$wpdb->insert(
    $wpdb->prefix . 'my_analytics',
    array(
        'user_id' => get_current_user_id(),
        'event_type' => 'page_view',
        'event_data' => json_encode( array( 'page' => get_the_ID() ) )
    ),
    array( '%d', '%s', '%s' )
);

// Query custom table
$results = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->prefix}my_analytics WHERE user_id = %d ORDER BY created_at DESC LIMIT 10",
    $user_id
));
```
