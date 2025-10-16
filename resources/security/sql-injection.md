---
difficulty: Intermediate
tags: [security, sql, database, injection]
related: [core/database-api, security/data-validation]
wp_version: All
---

# WordPress SQL Injection Prevention

SQL injection is a critical security vulnerability. WordPress provides tools to prevent it.

## The Golden Rule

**NEVER concatenate user input directly into SQL queries**

## Use $wpdb->prepare()

### Basic Usage

```php
global $wpdb;

// ❌ DANGEROUS - SQL Injection vulnerability
$user_id = $_GET['id'];
$wpdb->query( "DELETE FROM {$wpdb->users} WHERE ID = $user_id" );

// ✅ SAFE - Using prepared statement
$user_id = $_GET['id'];
$wpdb->query( $wpdb->prepare(
    "DELETE FROM {$wpdb->users} WHERE ID = %d",
    $user_id
) );
```

### Placeholders

```php
// %d - Integer
$wpdb->prepare( "SELECT * FROM table WHERE id = %d", $id );

// %s - String
$wpdb->prepare( "SELECT * FROM table WHERE name = %s", $name );

// %f - Float
$wpdb->prepare( "SELECT * FROM table WHERE price = %f", $price );
```

## Common Patterns

### SELECT Queries

```php
// Get single row
$post = $wpdb->get_row( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
    $post_id
) );

// Get multiple rows
$posts = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_author = %d",
    $author_id
) );

// Get single value
$count = $wpdb->get_var( $wpdb->prepare(
    "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_status = %s",
    'publish'
) );
```

### INSERT

```php
// Safe INSERT using wpdb methods
$wpdb->insert(
    $wpdb->posts,
    array(
        'post_title'   => $title,      // Will be sanitized
        'post_content' => $content,
        'post_author'  => $author_id,
    ),
    array( '%s', '%s', '%d' )         // Format types
);

// Or with prepare
$wpdb->query( $wpdb->prepare(
    "INSERT INTO {$wpdb->posts} (post_title, post_author) VALUES (%s, %d)",
    $title,
    $author_id
) );
```

### UPDATE

```php
// Safe UPDATE using wpdb methods
$wpdb->update(
    $wpdb->posts,
    array( 'post_status' => 'publish' ),  // Data
    array( 'ID' => $post_id ),            // Where
    array( '%s' ),                         // Data format
    array( '%d' )                          // Where format
);

// Or with prepare
$wpdb->query( $wpdb->prepare(
    "UPDATE {$wpdb->posts} SET post_status = %s WHERE ID = %d",
    'publish',
    $post_id
) );
```

### DELETE

```php
// Safe DELETE using wpdb methods
$wpdb->delete(
    $wpdb->posts,
    array( 'ID' => $post_id ),
    array( '%d' )
);

// Or with prepare
$wpdb->query( $wpdb->prepare(
    "DELETE FROM {$wpdb->posts} WHERE ID = %d",
    $post_id
) );
```

## Multiple Values

### WHERE IN Clause

```php
// For array of integers
$ids = array( 1, 2, 3, 4, 5 );
$ids_placeholders = implode( ', ', array_fill( 0, count( $ids ), '%d' ) );

$query = $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID IN ($ids_placeholders)",
    ...$ids  // PHP 7.4+ spread operator
);

// Or for older PHP
$query = $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID IN ($ids_placeholders)",
    $ids
);

$results = $wpdb->get_results( $query );
```

### Multiple String Values

```php
$statuses = array( 'publish', 'draft', 'private' );
$placeholders = implode( ', ', array_fill( 0, count( $statuses ), '%s' ) );

$query = $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_status IN ($placeholders)",
    ...$statuses
);
```

## LIKE Queries

```php
// Search with LIKE
$search = $_GET['search'];

// Escape wildcards first
$search = $wpdb->esc_like( $search );

// Then prepare
$query = $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE %s",
    '%' . $search . '%'
);

$results = $wpdb->get_results( $query );
```

## Complex Queries

### Multiple Conditions

```php
$author_id = $_GET['author'];
$post_type = $_GET['type'];
$status = $_GET['status'];

$query = $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} 
    WHERE post_author = %d 
    AND post_type = %s 
    AND post_status = %s
    ORDER BY post_date DESC
    LIMIT %d",
    $author_id,
    $post_type,
    $status,
    10
);

$posts = $wpdb->get_results( $query );
```

### JOIN Queries

```php
$user_id = get_current_user_id();

$query = $wpdb->prepare(
    "SELECT p.*, pm.meta_value 
    FROM {$wpdb->posts} p
    LEFT JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id
    WHERE p.post_author = %d
    AND pm.meta_key = %s",
    $user_id,
    'custom_field'
);
```

## Custom Tables

```php
// Custom table name
$table_name = $wpdb->prefix . 'custom_data';

// Always prepare even for custom tables
$wpdb->query( $wpdb->prepare(
    "INSERT INTO $table_name (user_id, data) VALUES (%d, %s)",
    $user_id,
    $data
) );
```

## WordPress Query Methods (Safer)

### WP_Query (Recommended)

```php
// Use WP_Query instead of direct SQL when possible
$query = new WP_Query( array(
    'author'         => $author_id,
    'post_type'      => $post_type,
    'post_status'    => $status,
    'posts_per_page' => 10,
) );

// WordPress handles sanitization
```

### get_posts()

```php
$posts = get_posts( array(
    'author'      => $author_id,
    'post_type'   => 'post',
    'numberposts' => -1,
) );
```

### get_users()

```php
$users = get_users( array(
    'role'    => $role,
    'orderby' => 'registered',
    'number'  => 10,
) );
```

## What NOT to Do

```php
// ❌ NEVER do this
$id = $_GET['id'];
$wpdb->query( "DELETE FROM table WHERE id = $id" );

// ❌ NEVER do this
$name = $_POST['name'];
$wpdb->query( "SELECT * FROM table WHERE name = '$name'" );

// ❌ NEVER do this
$sql = "SELECT * FROM table WHERE id = " . $id;
$wpdb->query( $sql );

// ❌ NEVER trust user input
$order = $_GET['order'];
$wpdb->query( "SELECT * FROM table ORDER BY $order" );

// ✅ Instead, whitelist values
$order = ( $_GET['order'] === 'asc' ) ? 'ASC' : 'DESC';
$wpdb->query( "SELECT * FROM table ORDER BY name $order" );
```

## Security Checklist

- [ ] Always use `$wpdb->prepare()` for user input
- [ ] Use `%d`, `%s`, `%f` placeholders correctly
- [ ] Escape LIKE wildcards with `$wpdb->esc_like()`
- [ ] Whitelist values when prepare() can't be used (ORDER BY, LIMIT)
- [ ] Use WordPress query functions when possible (WP_Query, get_posts)
- [ ] Never concatenate user input into SQL
- [ ] Validate data types before using in queries
- [ ] Use `$wpdb->insert()`, `$wpdb->update()`, `$wpdb->delete()` when possible

## Official Documentation

https://developer.wordpress.org/apis/security/data-validation/
https://developer.wordpress.org/reference/classes/wpdb/prepare/
