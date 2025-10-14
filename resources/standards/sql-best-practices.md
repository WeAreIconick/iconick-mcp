# WordPress SQL Best Practices

Comprehensive SQL best practices and security guidelines for WordPress development.

## Basic SQL Standards

### Prepared Statements (Critical for Security)

```php
// ✅ CORRECT: Using prepared statements
global $wpdb;

// Simple prepared statement
$user_id = 123;
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d AND post_status = %s",
        $user_id,
        'publish'
    )
);

// Multiple parameters
$search_term = 'wordpress';
$post_type = 'post';
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} 
         WHERE post_title LIKE %s 
         AND post_type = %s 
         AND post_status = %s",
        '%' . $wpdb->esc_like($search_term) . '%',
        $post_type,
        'publish'
    )
);

// INSERT with prepared statement
$wpdb->insert(
    $wpdb->usermeta,
    array(
        'user_id' => $user_id,
        'meta_key' => 'custom_field',
        'meta_value' => $meta_value
    ),
    array('%d', '%s', '%s')
);

// UPDATE with prepared statement
$updated = $wpdb->update(
    $wpdb->posts,
    array('post_status' => 'draft'),
    array('ID' => $post_id),
    array('%s'),
    array('%d')
);
```

### WordPress Database API Usage

```php
// ✅ CORRECT: Using WordPress database functions
global $wpdb;

// Get single value
$count = $wpdb->get_var(
    $wpdb->prepare(
        "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_author = %d",
        $author_id
    )
);

// Get single row
$post = $wpdb->get_row(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
        $post_id
    ),
    ARRAY_A
);

// Get multiple rows
$posts = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT ID, post_title, post_date 
         FROM {$wpdb->posts} 
         WHERE post_status = %s 
         ORDER BY post_date DESC 
         LIMIT %d",
        'publish',
        10
    )
);

// Get column values
$post_ids = $wpdb->get_col(
    $wpdb->prepare(
        "SELECT ID FROM {$wpdb->posts} 
         WHERE post_type = %s 
         AND post_status = %s",
        'product',
        'publish'
    )
);
```

## Advanced SQL Practices

### Complex Queries with Joins

```php
// Complex query with proper joins and prepared statements
function get_posts_with_meta($meta_key, $meta_value, $limit = 10) {
    global $wpdb;
    
    $results = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT p.*, pm.meta_value 
             FROM {$wpdb->posts} p
             INNER JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id
             WHERE p.post_status = %s
             AND p.post_type = %s
             AND pm.meta_key = %s
             AND pm.meta_value = %s
             ORDER BY p.post_date DESC
             LIMIT %d",
            'publish',
            'post',
            $meta_key,
            $meta_value,
            $limit
        )
    );
    
    return $results;
}

// Query with multiple meta fields
function get_products_by_category_and_price($category_id, $max_price) {
    global $wpdb;
    
    $results = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT p.*, 
                    price_meta.meta_value as price,
                    category_meta.meta_value as category
             FROM {$wpdb->posts} p
             LEFT JOIN {$wpdb->postmeta} price_meta ON p.ID = price_meta.post_id 
                 AND price_meta.meta_key = %s
             LEFT JOIN {$wpdb->postmeta} category_meta ON p.ID = category_meta.post_id 
                 AND category_meta.meta_key = %s
             WHERE p.post_type = %s
             AND p.post_status = %s
             AND CAST(price_meta.meta_value AS DECIMAL) <= %f
             AND category_meta.meta_value = %s
             ORDER BY p.post_date DESC",
            '_price',
            '_category_id',
            'product',
            'publish',
            $max_price,
            $category_id
        )
    );
    
    return $results;
}
```

### Transaction Management

```php
// Database transactions for data integrity
function create_user_with_meta($user_data, $meta_data) {
    global $wpdb;
    
    // Start transaction
    $wpdb->query('START TRANSACTION');
    
    try {
        // Insert user
        $user_inserted = $wpdb->insert(
            $wpdb->users,
            array(
                'user_login' => $user_data['username'],
                'user_email' => $user_data['email'],
                'user_pass' => wp_hash_password($user_data['password']),
                'user_registered' => current_time('mysql')
            ),
            array('%s', '%s', '%s', '%s')
        );
        
        if (!$user_inserted) {
            throw new Exception('Failed to insert user');
        }
        
        $user_id = $wpdb->insert_id;
        
        // Insert user meta
        foreach ($meta_data as $key => $value) {
            $meta_inserted = $wpdb->insert(
                $wpdb->usermeta,
                array(
                    'user_id' => $user_id,
                    'meta_key' => $key,
                    'meta_value' => $value
                ),
                array('%d', '%s', '%s')
            );
            
            if (!$meta_inserted) {
                throw new Exception('Failed to insert user meta');
            }
        }
        
        // Commit transaction
        $wpdb->query('COMMIT');
        return $user_id;
        
    } catch (Exception $e) {
        // Rollback on error
        $wpdb->query('ROLLBACK');
        error_log('Transaction failed: ' . $e->getMessage());
        return false;
    }
}
```

### Custom Table Operations

```php
// Custom table creation and management
function create_custom_table() {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'custom_data';
    
    $charset_collate = $wpdb->get_charset_collate();
    
    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        user_id bigint(20) NOT NULL,
        data_key varchar(255) NOT NULL,
        data_value longtext,
        created_at datetime DEFAULT CURRENT_TIMESTAMP,
        updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        PRIMARY KEY (id),
        KEY user_id (user_id),
        KEY data_key (data_key),
        KEY created_at (created_at)
    ) $charset_collate;";
    
    require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
    dbDelta($sql);
}

// Operations on custom table
function insert_custom_data($user_id, $data_key, $data_value) {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'custom_data';
    
    $result = $wpdb->insert(
        $table_name,
        array(
            'user_id' => $user_id,
            'data_key' => $data_key,
            'data_value' => $data_value
        ),
        array('%d', '%s', '%s')
    );
    
    return $result ? $wpdb->insert_id : false;
}

function get_custom_data($user_id, $data_key = null) {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'custom_data';
    
    if ($data_key) {
        // Get specific data
        $result = $wpdb->get_var(
            $wpdb->prepare(
                "SELECT data_value FROM $table_name 
                 WHERE user_id = %d AND data_key = %s",
                $user_id,
                $data_key
            )
        );
    } else {
        // Get all data for user
        $results = $wpdb->get_results(
            $wpdb->prepare(
                "SELECT data_key, data_value FROM $table_name 
                 WHERE user_id = %d",
                $user_id
            ),
            OBJECT_K
        );
        
        $result = array();
        foreach ($results as $row) {
            $result[$row->data_key] = $row->data_value;
        }
    }
    
    return $result;
}
```

## Performance Optimization

### Query Optimization

```php
// Efficient pagination
function get_paginated_posts($page = 1, $per_page = 10) {
    global $wpdb;
    
    $offset = ($page - 1) * $per_page;
    
    // Get total count efficiently
    $total = $wpdb->get_var(
        "SELECT COUNT(*) FROM {$wpdb->posts} 
         WHERE post_type = %s AND post_status = %s",
        'post',
        'publish'
    );
    
    // Get posts with pagination
    $posts = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT ID, post_title, post_date, post_excerpt 
             FROM {$wpdb->posts} 
             WHERE post_type = %s 
             AND post_status = %s 
             ORDER BY post_date DESC 
             LIMIT %d OFFSET %d",
            'post',
            'publish',
            $per_page,
            $offset
        )
    );
    
    return array(
        'posts' => $posts,
        'total' => $total,
        'pages' => ceil($total / $per_page)
    );
}

// Efficient meta queries
function get_posts_by_meta_range($meta_key, $min_value, $max_value) {
    global $wpdb;
    
    $results = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT p.ID, p.post_title, pm.meta_value
             FROM {$wpdb->posts} p
             INNER JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id
             WHERE p.post_type = %s
             AND p.post_status = %s
             AND pm.meta_key = %s
             AND CAST(pm.meta_value AS DECIMAL) BETWEEN %f AND %f
             ORDER BY CAST(pm.meta_value AS DECIMAL) ASC",
            'product',
            'publish',
            $meta_key,
            $min_value,
            $max_value
        )
    );
    
    return $results;
}
```

### Caching Database Queries

```php
// Cache expensive queries
function get_cached_user_stats($user_id) {
    $cache_key = 'user_stats_' . $user_id;
    $stats = get_transient($cache_key);
    
    if ($stats === false) {
        global $wpdb;
        
        $stats = $wpdb->get_row(
            $wpdb->prepare(
                "SELECT 
                    COUNT(p.ID) as post_count,
                    COUNT(c.comment_ID) as comment_count,
                    MAX(p.post_date) as last_post_date
                 FROM {$wpdb->posts} p
                 LEFT JOIN {$wpdb->comments} c ON p.ID = c.comment_post_ID
                 WHERE p.post_author = %d
                 AND p.post_status = %s",
                $user_id,
                'publish'
            ),
            ARRAY_A
        );
        
        // Cache for 1 hour
        set_transient($cache_key, $stats, HOUR_IN_SECONDS);
    }
    
    return $stats;
}

// Clear cache when data changes
function clear_user_stats_cache($user_id) {
    $cache_key = 'user_stats_' . $user_id;
    delete_transient($cache_key);
}

// Hook to clear cache when posts are updated
add_action('save_post', function($post_id) {
    $post = get_post($post_id);
    if ($post) {
        clear_user_stats_cache($post->post_author);
    }
});
```

### Database Indexing

```sql
-- Create indexes for better performance
CREATE INDEX idx_posts_author_status ON wp_posts(post_author, post_status);
CREATE INDEX idx_posts_type_date ON wp_posts(post_type, post_date);
CREATE INDEX idx_postmeta_key_value ON wp_postmeta(meta_key, meta_value(191));
CREATE INDEX idx_comments_post_approved ON wp_comments(comment_post_ID, comment_approved);

-- Composite indexes for complex queries
CREATE INDEX idx_posts_type_status_date ON wp_posts(post_type, post_status, post_date);
CREATE INDEX idx_usermeta_user_key ON wp_usermeta(user_id, meta_key);
```

## Security Best Practices

### SQL Injection Prevention

```php
// ❌ WRONG: Direct string concatenation (vulnerable to SQL injection)
$user_id = $_GET['user_id'];
$query = "SELECT * FROM {$wpdb->posts} WHERE post_author = " . $user_id;
$results = $wpdb->get_results($query);

// ✅ CORRECT: Using prepared statements
$user_id = intval($_GET['user_id']); // Sanitize input
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_author = %d",
        $user_id
    )
);

// ✅ CORRECT: Using WordPress sanitization functions
$search_term = sanitize_text_field($_GET['search']);
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} 
         WHERE post_title LIKE %s",
        '%' . $wpdb->esc_like($search_term) . '%'
    )
);

// ✅ CORRECT: Validating and sanitizing complex input
function search_posts_by_criteria($criteria) {
    global $wpdb;
    
    // Validate and sanitize input
    $post_type = sanitize_text_field($criteria['post_type']);
    $post_status = sanitize_text_field($criteria['post_status']);
    $date_from = sanitize_text_field($criteria['date_from']);
    $date_to = sanitize_text_field($criteria['date_to']);
    
    // Validate date format
    if (!strtotime($date_from) || !strtotime($date_to)) {
        return new WP_Error('invalid_date', 'Invalid date format');
    }
    
    $results = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT * FROM {$wpdb->posts} 
             WHERE post_type = %s 
             AND post_status = %s 
             AND post_date >= %s 
             AND post_date <= %s 
             ORDER BY post_date DESC",
            $post_type,
            $post_status,
            $date_from,
            $date_to
        )
    );
    
    return $results;
}
```

### Input Validation and Sanitization

```php
// Comprehensive input validation
function validate_and_sanitize_post_data($data) {
    $sanitized = array();
    $errors = array();
    
    // Required fields validation
    if (empty($data['title'])) {
        $errors[] = 'Title is required';
    } else {
        $sanitized['title'] = sanitize_text_field($data['title']);
    }
    
    // Email validation
    if (!empty($data['email'])) {
        $email = sanitize_email($data['email']);
        if (!is_email($email)) {
            $errors[] = 'Invalid email address';
        } else {
            $sanitized['email'] = $email;
        }
    }
    
    // URL validation
    if (!empty($data['website'])) {
        $url = esc_url_raw($data['website']);
        if (!filter_var($url, FILTER_VALIDATE_URL)) {
            $errors[] = 'Invalid URL';
        } else {
            $sanitized['website'] = $url;
        }
    }
    
    // Numeric validation
    if (!empty($data['age'])) {
        $age = intval($data['age']);
        if ($age < 0 || $age > 150) {
            $errors[] = 'Age must be between 0 and 150';
        } else {
            $sanitized['age'] = $age;
        }
    }
    
    // Textarea content
    if (!empty($data['content'])) {
        $sanitized['content'] = wp_kses_post($data['content']);
    }
    
    if (!empty($errors)) {
        return new WP_Error('validation_error', implode(', ', $errors));
    }
    
    return $sanitized;
}

// Safe database operations with validation
function insert_validated_post($data) {
    $sanitized_data = validate_and_sanitize_post_data($data);
    
    if (is_wp_error($sanitized_data)) {
        return $sanitized_data;
    }
    
    global $wpdb;
    
    $result = $wpdb->insert(
        $wpdb->posts,
        array(
            'post_title' => $sanitized_data['title'],
            'post_content' => $sanitized_data['content'] ?? '',
            'post_status' => 'draft',
            'post_type' => 'custom_post',
            'post_date' => current_time('mysql')
        ),
        array('%s', '%s', '%s', '%s', '%s')
    );
    
    if ($result === false) {
        return new WP_Error('db_error', 'Failed to insert post');
    }
    
    return $wpdb->insert_id;
}
```

## Error Handling and Logging

### Database Error Handling

```php
// Comprehensive error handling
function safe_database_operation($query, $params = array()) {
    global $wpdb;
    
    // Enable error reporting
    $wpdb->show_errors();
    
    try {
        if (empty($params)) {
            $result = $wpdb->query($query);
        } else {
            $prepared_query = $wpdb->prepare($query, $params);
            $result = $wpdb->query($prepared_query);
        }
        
        if ($result === false) {
            $error_message = $wpdb->last_error;
            $error_query = $wpdb->last_query;
            
            // Log the error
            error_log(sprintf(
                'Database error: %s. Query: %s',
                $error_message,
                $error_query
            ));
            
            return new WP_Error('db_error', $error_message);
        }
        
        return $result;
        
    } catch (Exception $e) {
        error_log('Database exception: ' . $e->getMessage());
        return new WP_Error('db_exception', $e->getMessage());
    }
}

// Safe query execution with fallback
function get_posts_with_fallback($args) {
    global $wpdb;
    
    // Try optimized query first
    $results = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT p.*, pm.meta_value 
             FROM {$wpdb->posts} p
             LEFT JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id 
                 AND pm.meta_key = %s
             WHERE p.post_type = %s 
             AND p.post_status = %s
             ORDER BY p.post_date DESC
             LIMIT %d",
            $args['meta_key'],
            $args['post_type'],
            $args['post_status'],
            $args['limit']
        )
    );
    
    if ($wpdb->last_error) {
        // Fallback to simpler query
        error_log('Optimized query failed, using fallback: ' . $wpdb->last_error);
        
        $results = $wpdb->get_results(
            $wpdb->prepare(
                "SELECT * FROM {$wpdb->posts} 
                 WHERE post_type = %s 
                 AND post_status = %s
                 ORDER BY post_date DESC
                 LIMIT %d",
                $args['post_type'],
                $args['post_status'],
                $args['limit']
            )
        );
    }
    
    return $results;
}
```

## WordPress-Specific SQL Patterns

### Custom Post Type Queries

```php
// Efficient custom post type queries
function get_custom_posts_by_meta($post_type, $meta_query) {
    global $wpdb;
    
    $where_conditions = array();
    $where_values = array();
    
    $where_conditions[] = "p.post_type = %s";
    $where_values[] = $post_type;
    
    $where_conditions[] = "p.post_status = %s";
    $where_values[] = 'publish';
    
    // Build meta query conditions
    foreach ($meta_query as $meta) {
        $where_conditions[] = "pm{$meta['alias']}.meta_key = %s";
        $where_values[] = $meta['key'];
        
        $where_conditions[] = "pm{$meta['alias']}.meta_value {$meta['compare']} %s";
        $where_values[] = $meta['value'];
    }
    
    $where_clause = implode(' AND ', $where_conditions);
    
    $query = "SELECT DISTINCT p.* 
              FROM {$wpdb->posts} p";
    
    // Add JOIN clauses for meta
    foreach ($meta_query as $meta) {
        $query .= " INNER JOIN {$wpdb->postmeta} pm{$meta['alias']} 
                    ON p.ID = pm{$meta['alias']}.post_id";
    }
    
    $query .= " WHERE $where_clause ORDER BY p.post_date DESC";
    
    return $wpdb->get_results($wpdb->prepare($query, $where_values));
}
```

### Taxonomy Queries

```php
// Efficient taxonomy queries
function get_posts_by_taxonomy($post_type, $taxonomy, $term_slug, $limit = 10) {
    global $wpdb;
    
    $results = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT DISTINCT p.*
             FROM {$wpdb->posts} p
             INNER JOIN {$wpdb->term_relationships} tr ON p.ID = tr.object_id
             INNER JOIN {$wpdb->term_taxonomy} tt ON tr.term_taxonomy_id = tt.term_taxonomy_id
             INNER JOIN {$wpdb->terms} t ON tt.term_id = t.term_id
             WHERE p.post_type = %s
             AND p.post_status = %s
             AND tt.taxonomy = %s
             AND t.slug = %s
             ORDER BY p.post_date DESC
             LIMIT %d",
            $post_type,
            'publish',
            $taxonomy,
            $term_slug,
            $limit
        )
    );
    
    return $results;
}
```

## Best Practices Summary

### Security
- Always use prepared statements
- Validate and sanitize all input data
- Use WordPress sanitization functions
- Implement proper error handling
- Never trust user input

### Performance
- Use appropriate indexes
- Limit query results with LIMIT
- Cache expensive queries
- Use efficient JOIN operations
- Avoid SELECT * when possible

### Maintainability
- Use WordPress database API
- Follow WordPress coding standards
- Implement proper error handling
- Use transactions for data integrity
- Document complex queries

### Reliability
- Handle database errors gracefully
- Implement fallback queries
- Use transactions for critical operations
- Validate data before database operations
- Log errors for debugging

## Official Documentation

https://developer.wordpress.org/reference/classes/wpdb/
https://developer.wordpress.org/plugins/plugin-basics/database-operations/
https://developer.wordpress.org/themes/basics/database-operations/
