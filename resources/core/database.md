# WordPress Database API (wpdb)

The `$wpdb` global object provides a safe interface for interacting with the WordPress database.

## Basic Usage

```php
global $wpdb;

// Get results
$results = $wpdb->get_results( 
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_status = %s",
        'publish'
    )
);

// Get a single row
$post = $wpdb->get_row(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
        $post_id
    )
);

// Get a single variable
$count = $wpdb->get_var(
    "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'post'"
);
```

## Prepared Statements (CRITICAL for Security)

**ALWAYS use `$wpdb->prepare()` to prevent SQL injection:**

```php
// ❌ NEVER DO THIS
$wpdb->query( "SELECT * FROM {$wpdb->posts} WHERE ID = $id" );

// ✅ ALWAYS DO THIS
$wpdb->query( $wpdb->prepare( 
    "SELECT * FROM {$wpdb->posts} WHERE ID = %d", 
    $id 
) );
```

### Placeholders

- `%s` - String
- `%d` - Integer
- `%f` - Float

## Insert, Update, Delete

```php
// Insert
$wpdb->insert(
    $wpdb->posts,
    array(
        'post_title' => 'My Title',
        'post_content' => 'Content here',
        'post_status' => 'publish'
    ),
    array( '%s', '%s', '%s' )
);

// Update
$wpdb->update(
    $wpdb->posts,
    array( 'post_status' => 'draft' ),  // Data
    array( 'ID' => 1 ),                  // Where
    array( '%s' ),                        // Data format
    array( '%d' )                         // Where format
);

// Delete
$wpdb->delete(
    $wpdb->posts,
    array( 'ID' => 1 ),
    array( '%d' )
);
```

## Custom Tables

```php
// Create custom table
function create_custom_table() {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'custom_data';
    $charset_collate = $wpdb->get_charset_collate();
    
    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        time datetime DEFAULT '0000-00-00 00:00:00' NOT NULL,
        name tinytext NOT NULL,
        value text NOT NULL,
        PRIMARY KEY  (id)
    ) $charset_collate;";
    
    require_once( ABSPATH . 'wp-admin/includes/upgrade.php' );
    dbDelta( $sql );
}
```

## Common Table References

```php
$wpdb->posts          // wp_posts
$wpdb->postmeta       // wp_postmeta
$wpdb->users          // wp_users
$wpdb->usermeta       // wp_usermeta
$wpdb->terms          // wp_terms
$wpdb->term_taxonomy  // wp_term_taxonomy
$wpdb->term_relationships  // wp_term_relationships
$wpdb->options        // wp_options
$wpdb->comments       // wp_comments
$wpdb->commentmeta    // wp_commentmeta
$wpdb->prefix         // Table prefix (default: wp_)
```

## Error Handling

```php
// Show errors (only in development)
$wpdb->show_errors();

// Hide errors
$wpdb->hide_errors();

// Get last error
$wpdb->last_error;

// Get last query
$wpdb->last_query;
```

## Transactions

```php
// Start transaction
$wpdb->query( 'START TRANSACTION' );

try {
    // Your queries here
    $wpdb->insert( /* ... */ );
    $wpdb->update( /* ... */ );
    
    // Commit
    $wpdb->query( 'COMMIT' );
} catch ( Exception $e ) {
    // Rollback on error
    $wpdb->query( 'ROLLBACK' );
}
```

## Best Practices

1. **Always use prepared statements** with `$wpdb->prepare()`
2. **Use `dbDelta()`** for creating/updating tables
3. **Escape output** when displaying data: `esc_html()`, `esc_attr()`
4. **Check for errors** after queries
5. **Use transactions** for multiple related queries
6. **Avoid direct queries** when WordPress has a function (use `get_posts()` instead of SELECT)
7. **Index your custom tables** for better performance
8. **Use `$wpdb->prefix`** instead of hardcoding 'wp_'

## Performance Tips

1. Use `get_var()` for single values instead of `get_results()`
2. Limit results with LIMIT clause
3. Use indexes on frequently queried columns
4. Cache results with transients for expensive queries
5. Avoid SELECT * - specify needed columns
6. Use EXPLAIN to analyze slow queries

## Official Documentation

https://developer.wordpress.org/reference/classes/wpdb/
https://developer.wordpress.org/apis/handbook/database/
