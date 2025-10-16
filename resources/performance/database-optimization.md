---
difficulty: Advanced
tags: [database, performance, optimization, queries]
related: [core/database-api, performance/caching-systems]
wp_version: All
---

# WordPress Database Performance and Optimization

## Overview

WordPress database optimization involves implementing advanced techniques to improve query performance, reduce database load, optimize storage, and enhance overall database efficiency for high-traffic WordPress websites.

## Database Performance Analysis

### Query Performance Monitoring

**Slow Query Analysis**
```sql
-- Enable slow query logging
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;
SET GLOBAL log_queries_not_using_indexes = 'ON';
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';

-- Analyze slow queries
SELECT 
    query_time,
    lock_time,
    rows_sent,
    rows_examined,
    sql_text
FROM mysql.slow_log 
WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 DAY)
ORDER BY query_time DESC 
LIMIT 10;

-- Query performance statistics
SHOW STATUS LIKE 'Slow_queries';
SHOW STATUS LIKE 'Questions';
SHOW STATUS LIKE 'Uptime';
```

**Query Execution Analysis**
```sql
-- Analyze query execution plans
EXPLAIN SELECT p.*, pm.meta_value 
FROM wp_posts p 
LEFT JOIN wp_postmeta pm ON p.ID = pm.post_id 
WHERE p.post_status = 'publish' 
AND pm.meta_key = 'featured_image'
ORDER BY p.post_date DESC 
LIMIT 10;

-- Index usage analysis
SHOW INDEX FROM wp_posts;
SHOW INDEX FROM wp_postmeta;

-- Table statistics
SELECT 
    table_name,
    table_rows,
    data_length,
    index_length,
    (data_length + index_length) as total_size,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size in MB'
FROM information_schema.tables 
WHERE table_schema = 'wordpress_db'
ORDER BY (data_length + index_length) DESC;
```

### Performance Metrics

**Database Performance Monitoring**
```php
// Database performance monitoring
class Database_Performance_Monitor {
    private $query_log = array();
    private $slow_queries = array();
    
    public function __construct() {
        add_filter('query', array($this, 'log_query'));
        add_action('wp_footer', array($this, 'log_performance_metrics'));
    }
    
    public function log_query($query) {
        $start_time = microtime(true);
        
        // Store original query
        $original_query = $query;
        
        // Add filter to capture execution time
        add_filter('posts_results', array($this, 'capture_query_time'), 10, 2);
        
        return $query;
    }
    
    public function capture_query_time($posts, $query) {
        $end_time = microtime(true);
        $execution_time = ($end_time - $GLOBALS['query_start_time']) * 1000; // Convert to milliseconds
        
        // Log slow queries (> 100ms)
        if ($execution_time > 100) {
            $this->slow_queries[] = array(
                'query' => $GLOBALS['current_query'],
                'execution_time' => $execution_time,
                'timestamp' => current_time('mysql'),
                'memory_usage' => memory_get_usage(true)
            );
        }
        
        $this->query_log[] = array(
            'query' => $GLOBALS['current_query'],
            'execution_time' => $execution_time,
            'memory_usage' => memory_get_usage(true)
        );
        
        return $posts;
    }
    
    public function log_performance_metrics() {
        global $wpdb;
        
        $metrics = array(
            'total_queries' => count($this->query_log),
            'slow_queries' => count($this->slow_queries),
            'avg_execution_time' => $this->calculate_average_execution_time(),
            'total_execution_time' => $this->calculate_total_execution_time(),
            'memory_peak_usage' => memory_get_peak_usage(true),
            'db_connections' => $this->get_db_connection_count()
        );
        
        // Log metrics to database
        $this->store_performance_metrics($metrics);
        
        // Display performance info in admin
        if (current_user_can('manage_options')) {
            echo '<!-- Database Performance: ' . json_encode($metrics) . ' -->';
        }
    }
    
    private function calculate_average_execution_time() {
        if (empty($this->query_log)) {
            return 0;
        }
        
        $total_time = array_sum(array_column($this->query_log, 'execution_time'));
        return $total_time / count($this->query_log);
    }
    
    private function calculate_total_execution_time() {
        return array_sum(array_column($this->query_log, 'execution_time'));
    }
    
    private function get_db_connection_count() {
        global $wpdb;
        
        $result = $wpdb->get_var("SHOW STATUS LIKE 'Threads_connected'");
        return $result ? $result : 0;
    }
    
    private function store_performance_metrics($metrics) {
        global $wpdb;
        
        $wpdb->insert(
            $wpdb->prefix . 'performance_metrics',
            array_merge($metrics, array('timestamp' => current_time('mysql'))),
            array('%d', '%d', '%f', '%f', '%d', '%d', '%s')
        );
    }
}

// Initialize database performance monitoring
new Database_Performance_Monitor();
```

## Database Schema Optimization

### Index Optimization

**Essential WordPress Indexes**
```sql
-- Posts table optimization
ALTER TABLE wp_posts ADD INDEX idx_post_status_date (post_status, post_date);
ALTER TABLE wp_posts ADD INDEX idx_post_type_status (post_type, post_status);
ALTER TABLE wp_posts ADD INDEX idx_post_author_status (post_author, post_status);
ALTER TABLE wp_posts ADD INDEX idx_post_parent (post_parent);

-- Postmeta table optimization
ALTER TABLE wp_postmeta ADD INDEX idx_meta_key_value (meta_key, meta_value(191));
ALTER TABLE wp_postmeta ADD INDEX idx_post_id_key (post_id, meta_key);

-- Comments table optimization
ALTER TABLE wp_comments ADD INDEX idx_comment_post_approved (comment_post_ID, comment_approved);
ALTER TABLE wp_comments ADD INDEX idx_comment_date (comment_date);
ALTER TABLE wp_comments ADD INDEX idx_comment_author_email (comment_author_email);

-- Users table optimization
ALTER TABLE wp_users ADD INDEX idx_user_login (user_login);
ALTER TABLE wp_users ADD INDEX idx_user_email (user_email);

-- Usermeta table optimization
ALTER TABLE wp_usermeta ADD INDEX idx_user_id_key (user_id, meta_key);
ALTER TABLE wp_usermeta ADD INDEX idx_meta_key_value (meta_key, meta_value(191));

-- Options table optimization
ALTER TABLE wp_options ADD INDEX idx_autoload (autoload, option_name);
ALTER TABLE wp_options ADD INDEX idx_option_name (option_name);

-- Terms table optimization
ALTER TABLE wp_terms ADD INDEX idx_name_slug (name, slug);
ALTER TABLE wp_term_taxonomy ADD INDEX idx_taxonomy (taxonomy);
ALTER TABLE wp_term_relationships ADD INDEX idx_object_term (object_id, term_taxonomy_id);
```

**Custom Index Creation**
```php
// Custom index management
class Database_Index_Manager {
    
    public function __construct() {
        add_action('admin_init', array($this, 'check_and_create_indexes'));
    }
    
    public function check_and_create_indexes() {
        $required_indexes = $this->get_required_indexes();
        
        foreach ($required_indexes as $table => $indexes) {
            foreach ($indexes as $index_name => $index_definition) {
                if (!$this->index_exists($table, $index_name)) {
                    $this->create_index($table, $index_name, $index_definition);
                }
            }
        }
    }
    
    private function get_required_indexes() {
        global $wpdb;
        
        return array(
            $wpdb->posts => array(
                'idx_posts_status_date' => 'post_status, post_date',
                'idx_posts_type_status' => 'post_type, post_status',
                'idx_posts_author_status' => 'post_author, post_status'
            ),
            $wpdb->postmeta => array(
                'idx_postmeta_key_value' => 'meta_key, meta_value(191)',
                'idx_postmeta_post_key' => 'post_id, meta_key'
            ),
            $wpdb->comments => array(
                'idx_comments_post_approved' => 'comment_post_ID, comment_approved',
                'idx_comments_date' => 'comment_date'
            ),
            $wpdb->users => array(
                'idx_users_login' => 'user_login',
                'idx_users_email' => 'user_email'
            ),
            $wpdb->usermeta => array(
                'idx_usermeta_user_key' => 'user_id, meta_key'
            ),
            $wpdb->options => array(
                'idx_options_autoload' => 'autoload, option_name'
            )
        );
    }
    
    private function index_exists($table, $index_name) {
        global $wpdb;
        
        $result = $wpdb->get_var($wpdb->prepare(
            "SELECT COUNT(*) 
             FROM INFORMATION_SCHEMA.STATISTICS 
             WHERE table_schema = %s 
             AND table_name = %s 
             AND index_name = %s",
            DB_NAME,
            $table,
            $index_name
        ));
        
        return $result > 0;
    }
    
    private function create_index($table, $index_name, $columns) {
        global $wpdb;
        
        $sql = "ALTER TABLE {$table} ADD INDEX {$index_name} ({$columns})";
        $result = $wpdb->query($sql);
        
        if ($result === false) {
            error_log("Failed to create index {$index_name} on table {$table}: " . $wpdb->last_error);
        } else {
            error_log("Successfully created index {$index_name} on table {$table}");
        }
        
        return $result !== false;
    }
}

// Initialize index manager
new Database_Index_Manager();
```

### Table Optimization

**Table Structure Optimization**
```sql
-- Analyze and optimize tables
ANALYZE TABLE wp_posts, wp_postmeta, wp_comments, wp_users, wp_usermeta, wp_options;
OPTIMIZE TABLE wp_posts, wp_postmeta, wp_comments, wp_users, wp_usermeta, wp_options;

-- Check table fragmentation
SELECT 
    table_name,
    engine,
    table_rows,
    avg_row_length,
    data_length,
    max_data_length,
    index_length,
    data_free,
    ROUND(data_free / (data_length + index_length) * 100, 2) as fragmentation_percent
FROM information_schema.tables 
WHERE table_schema = 'wordpress_db' 
AND data_free > 0
ORDER BY data_free DESC;

-- Repair fragmented tables
REPAIR TABLE wp_posts;
REPAIR TABLE wp_postmeta;
REPAIR TABLE wp_comments;
```

**Database Cleanup**
```sql
-- Clean up WordPress database
-- Remove post revisions (keep last 3)
DELETE FROM wp_posts 
WHERE post_type = 'revision' 
AND post_date < DATE_SUB(NOW(), INTERVAL 30 DAY)
AND ID NOT IN (
    SELECT ID FROM (
        SELECT ID FROM wp_posts 
        WHERE post_type = 'revision' 
        ORDER BY post_date DESC 
        LIMIT 3
    ) AS temp
);

-- Clean up spam comments
DELETE FROM wp_comments WHERE comment_approved = 'spam';
DELETE FROM wp_commentmeta WHERE comment_id NOT IN (SELECT comment_ID FROM wp_comments);

-- Clean up orphaned post meta
DELETE pm FROM wp_postmeta pm 
LEFT JOIN wp_posts p ON pm.post_id = p.ID 
WHERE p.ID IS NULL;

-- Clean up orphaned user meta
DELETE um FROM wp_usermeta um 
LEFT JOIN wp_users u ON um.user_id = u.ID 
WHERE u.ID IS NULL;

-- Clean up expired transients
DELETE FROM wp_options 
WHERE option_name LIKE '_transient_timeout_%' 
AND option_value < UNIX_TIMESTAMP();
```

## Query Optimization

### Efficient Query Patterns

**Optimized WordPress Queries**
```php
// Optimized query patterns
class Optimized_Queries {
    
    // Efficient post queries
    public function get_posts_by_meta_optimized($meta_key, $meta_value, $limit = 10) {
        global $wpdb;
        
        // Use proper indexing
        $sql = $wpdb->prepare("
            SELECT p.* 
            FROM {$wpdb->posts} p
            INNER JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id
            WHERE pm.meta_key = %s 
            AND pm.meta_value = %s
            AND p.post_status = 'publish'
            AND p.post_type = 'post'
            ORDER BY p.post_date DESC
            LIMIT %d
        ", $meta_key, $meta_value, $limit);
        
        return $wpdb->get_results($sql);
    }
    
    // Efficient user queries
    public function get_users_with_meta($meta_key, $meta_value) {
        global $wpdb;
        
        $sql = $wpdb->prepare("
            SELECT u.* 
            FROM {$wpdb->users} u
            INNER JOIN {$wpdb->usermeta} um ON u.ID = um.user_id
            WHERE um.meta_key = %s 
            AND um.meta_value = %s
        ", $meta_key, $meta_value);
        
        return $wpdb->get_results($sql);
    }
    
    // Efficient comment queries
    public function get_comments_by_post_optimized($post_id, $status = 'approve') {
        global $wpdb;
        
        $sql = $wpdb->prepare("
            SELECT c.* 
            FROM {$wpdb->comments} c
            WHERE c.comment_post_ID = %d
            AND c.comment_approved = %s
            ORDER BY c.comment_date ASC
        ", $post_id, $status);
        
        return $wpdb->get_results($sql);
    }
    
    // Batch operations
    public function update_multiple_posts_meta($post_ids, $meta_key, $meta_value) {
        global $wpdb;
        
        if (empty($post_ids)) {
            return false;
        }
        
        $placeholders = implode(',', array_fill(0, count($post_ids), '%d'));
        $sql = $wpdb->prepare("
            UPDATE {$wpdb->postmeta} 
            SET meta_value = %s 
            WHERE post_id IN ({$placeholders}) 
            AND meta_key = %s
        ", array_merge(array($meta_value), $post_ids, array($meta_key)));
        
        return $wpdb->query($sql);
    }
    
    // Efficient pagination
    public function get_posts_paginated($page = 1, $per_page = 10, $post_type = 'post') {
        global $wpdb;
        
        $offset = ($page - 1) * $per_page;
        
        // Get posts with total count
        $sql = $wpdb->prepare("
            SELECT SQL_CALC_FOUND_ROWS p.*
            FROM {$wpdb->posts} p
            WHERE p.post_status = 'publish'
            AND p.post_type = %s
            ORDER BY p.post_date DESC
            LIMIT %d OFFSET %d
        ", $post_type, $per_page, $offset);
        
        $posts = $wpdb->get_results($sql);
        $total = $wpdb->get_var("SELECT FOUND_ROWS()");
        
        return array(
            'posts' => $posts,
            'total' => $total,
            'pages' => ceil($total / $per_page),
            'current_page' => $page
        );
    }
    
    // Efficient search queries
    public function search_posts_optimized($search_term, $limit = 10) {
        global $wpdb;
        
        $search_term = '%' . $wpdb->esc_like($search_term) . '%';
        
        $sql = $wpdb->prepare("
            SELECT DISTINCT p.*, 
                   MATCH(p.post_title, p.post_content) AGAINST(%s IN BOOLEAN MODE) as relevance
            FROM {$wpdb->posts} p
            WHERE p.post_status = 'publish'
            AND p.post_type = 'post'
            AND (
                MATCH(p.post_title, p.post_content) AGAINST(%s IN BOOLEAN MODE)
                OR p.post_title LIKE %s
                OR p.post_content LIKE %s
            )
            ORDER BY relevance DESC, p.post_date DESC
            LIMIT %d
        ", $search_term, $search_term, $search_term, $search_term, $limit);
        
        return $wpdb->get_results($sql);
    }
}
```

### Query Caching

**Advanced Query Caching**
```php
// Advanced query caching system
class Advanced_Query_Cache {
    private $cache_time = 3600; // 1 hour
    private $cache_group = 'wp_query_cache';
    
    public function __construct() {
        add_filter('posts_pre_query', array($this, 'cache_query'), 10, 2);
        add_action('save_post', array($this, 'invalidate_cache'));
        add_action('delete_post', array($this, 'invalidate_cache'));
    }
    
    public function cache_query($posts, $query) {
        // Only cache main queries
        if (!$query->is_main_query() || is_admin() || is_user_logged_in()) {
            return null;
        }
        
        $cache_key = $this->generate_cache_key($query);
        $cached_result = wp_cache_get($cache_key, $this->cache_group);
        
        if ($cached_result !== false) {
            // Return cached result
            $query->posts = $cached_result['posts'];
            $query->post_count = $cached_result['post_count'];
            $query->found_posts = $cached_result['found_posts'];
            $query->max_num_pages = $cached_result['max_num_pages'];
            
            return $cached_result['posts'];
        }
        
        return null; // Let WordPress handle the query
    }
    
    public function cache_query_results($posts, $query) {
        if ($query->is_main_query() && !is_admin() && !is_user_logged_in()) {
            $cache_key = $this->generate_cache_key($query);
            
            $cache_data = array(
                'posts' => $posts,
                'post_count' => $query->post_count,
                'found_posts' => $query->found_posts,
                'max_num_pages' => $query->max_num_pages,
                'timestamp' => time()
            );
            
            wp_cache_set($cache_key, $cache_data, $this->cache_group, $this->cache_time);
        }
        
        return $posts;
    }
    
    private function generate_cache_key($query) {
        $query_vars = $query->query_vars;
        
        // Remove non-cacheable variables
        unset($query_vars['cache_results']);
        unset($query_vars['update_post_meta_cache']);
        unset($query_vars['update_post_term_cache']);
        unset($query_vars['suppress_filters']);
        
        // Add current page and pagination info
        $query_vars['paged'] = get_query_var('paged') ?: 1;
        $query_vars['posts_per_page'] = get_option('posts_per_page');
        
        return 'query_' . md5(serialize($query_vars));
    }
    
    public function invalidate_cache($post_id) {
        // Clear all query cache
        wp_cache_flush_group($this->cache_group);
        
        // Clear specific post cache
        wp_cache_delete('post_' . $post_id, 'post_cache');
        
        // Clear related caches
        $this->clear_related_caches($post_id);
    }
    
    private function clear_related_caches($post_id) {
        $post = get_post($post_id);
        
        // Clear category caches
        $categories = wp_get_post_categories($post_id);
        foreach ($categories as $cat_id) {
            wp_cache_delete('category_' . $cat_id, 'category_cache');
        }
        
        // Clear tag caches
        $tags = wp_get_post_tags($post_id);
        foreach ($tags as $tag) {
            wp_cache_delete('tag_' . $tag->term_id, 'tag_cache');
        }
        
        // Clear author cache
        wp_cache_delete('author_' . $post->post_author, 'author_cache');
        
        // Clear archive caches
        wp_cache_delete('archive_' . date('Y-m', strtotime($post->post_date)), 'archive_cache');
    }
}

// Initialize query cache
new Advanced_Query_Cache();
```

## Database Configuration Optimization

### MySQL/MariaDB Tuning

**High-Performance MySQL Configuration**
```ini
# MySQL/MariaDB optimization for WordPress
[mysqld]
# Basic settings
port = 3306
socket = /var/run/mysqld/mysqld.sock
datadir = /var/lib/mysql
tmpdir = /tmp
pid-file = /var/run/mysqld/mysqld.pid

# InnoDB settings for high performance
default-storage-engine = InnoDB
innodb_buffer_pool_size = 4G
innodb_log_file_size = 1G
innodb_log_buffer_size = 64M
innodb_flush_log_at_trx_commit = 2
innodb_file_per_table = 1
innodb_open_files = 400
innodb_io_capacity = 2000
innodb_io_capacity_max = 4000
innodb_read_io_threads = 8
innodb_write_io_threads = 8
innodb_thread_concurrency = 16
innodb_flush_method = O_DIRECT
innodb_buffer_pool_instances = 8

# Query cache
query_cache_type = 1
query_cache_size = 256M
query_cache_limit = 4M

# Connection settings
max_connections = 500
max_connect_errors = 100000
connect_timeout = 10
wait_timeout = 600
interactive_timeout = 600
thread_cache_size = 32
table_open_cache = 8000
table_definition_cache = 2000

# Temporary tables
tmp_table_size = 256M
max_heap_table_size = 256M
tmpdir = /tmp

# MyISAM settings
key_buffer_size = 256M
myisam_sort_buffer_size = 128M
myisam_max_sort_file_size = 10G
myisam_repair_threads = 1

# Logging
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1
log_queries_not_using_indexes = 1
log_slow_admin_statements = 1

# Binary logging
log-bin = mysql-bin
binlog_format = ROW
expire_logs_days = 7
max_binlog_size = 100M

# Security
local-infile = 0
symbolic-links = 0
skip-name-resolve
```

### Database Monitoring

**Real-time Database Monitoring**
```php
// Real-time database monitoring
class Database_Monitor {
    private $metrics = array();
    
    public function __construct() {
        add_action('wp_ajax_db_metrics', array($this, 'get_database_metrics'));
        add_action('wp_ajax_nopriv_db_metrics', array($this, 'get_database_metrics'));
    }
    
    public function get_database_metrics() {
        global $wpdb;
        
        $metrics = array(
            'connection_count' => $this->get_connection_count(),
            'slow_queries' => $this->get_slow_query_count(),
            'query_cache_hit_rate' => $this->get_query_cache_hit_rate(),
            'table_size' => $this->get_table_sizes(),
            'index_usage' => $this->get_index_usage_stats(),
            'innodb_stats' => $this->get_innodb_stats(),
            'buffer_pool_usage' => $this->get_buffer_pool_usage()
        );
        
        wp_send_json($metrics);
    }
    
    private function get_connection_count() {
        global $wpdb;
        
        $result = $wpdb->get_var("SHOW STATUS LIKE 'Threads_connected'");
        return $result ? $result : 0;
    }
    
    private function get_slow_query_count() {
        global $wpdb;
        
        $result = $wpdb->get_var("SHOW STATUS LIKE 'Slow_queries'");
        return $result ? $result : 0;
    }
    
    private function get_query_cache_hit_rate() {
        global $wpdb;
        
        $hits = $wpdb->get_var("SHOW STATUS LIKE 'Qcache_hits'");
        $inserts = $wpdb->get_var("SHOW STATUS LIKE 'Qcache_inserts'");
        
        if (!$hits || !$inserts) {
            return 0;
        }
        
        $total = $hits + $inserts;
        return $total > 0 ? ($hits / $total) * 100 : 0;
    }
    
    private function get_table_sizes() {
        global $wpdb;
        
        $results = $wpdb->get_results("
            SELECT 
                table_name,
                ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size in MB',
                table_rows
            FROM information_schema.tables 
            WHERE table_schema = DATABASE()
            ORDER BY (data_length + index_length) DESC
            LIMIT 10
        ");
        
        return $results;
    }
    
    private function get_index_usage_stats() {
        global $wpdb;
        
        $results = $wpdb->get_results("
            SELECT 
                t.table_name,
                t.index_name,
                t.cardinality,
                s.rows_read,
                s.rows_requested
            FROM information_schema.statistics t
            LEFT JOIN performance_schema.table_io_waits_summary_by_index_usage s 
                ON t.table_schema = s.object_schema 
                AND t.table_name = s.object_name 
                AND t.index_name = s.index_name
            WHERE t.table_schema = DATABASE()
            ORDER BY s.rows_read DESC
            LIMIT 20
        ");
        
        return $results;
    }
    
    private function get_innodb_stats() {
        global $wpdb;
        
        $stats = array();
        $innodb_vars = array(
            'Innodb_buffer_pool_pages_data',
            'Innodb_buffer_pool_pages_total',
            'Innodb_buffer_pool_read_requests',
            'Innodb_buffer_pool_reads',
            'Innodb_buffer_pool_wait_free',
            'Innodb_log_waits',
            'Innodb_row_lock_waits',
            'Innodb_row_lock_time_avg'
        );
        
        foreach ($innodb_vars as $var) {
            $result = $wpdb->get_var("SHOW STATUS LIKE '{$var}'");
            $stats[$var] = $result ? $result : 0;
        }
        
        return $stats;
    }
    
    private function get_buffer_pool_usage() {
        global $wpdb;
        
        $data_pages = $wpdb->get_var("SHOW STATUS LIKE 'Innodb_buffer_pool_pages_data'");
        $total_pages = $wpdb->get_var("SHOW STATUS LIKE 'Innodb_buffer_pool_pages_total'");
        
        if (!$data_pages || !$total_pages) {
            return 0;
        }
        
        return ($data_pages / $total_pages) * 100;
    }
}

// Initialize database monitor
new Database_Monitor();
```

## Database Maintenance

### Automated Maintenance

**Database Maintenance System**
```php
// Automated database maintenance
class Database_Maintenance {
    
    public function __construct() {
        add_action('wp_scheduled_delete', array($this, 'daily_maintenance'));
        add_action('wp_ajax_db_maintenance', array($this, 'run_maintenance'));
    }
    
    public function daily_maintenance() {
        $this->cleanup_revisions();
        $this->cleanup_spam_comments();
        $this->cleanup_orphaned_meta();
        $this->cleanup_expired_transients();
        $this->optimize_tables();
    }
    
    private function cleanup_revisions() {
        global $wpdb;
        
        // Keep only last 3 revisions per post
        $wpdb->query("
            DELETE r1 FROM {$wpdb->posts} r1
            INNER JOIN {$wpdb->posts} r2 
            WHERE r1.post_type = 'revision'
            AND r2.post_type = 'revision'
            AND r1.post_parent = r2.post_parent
            AND r1.post_date < r2.post_date
            AND (
                SELECT COUNT(*) 
                FROM {$wpdb->posts} r3 
                WHERE r3.post_parent = r1.post_parent 
                AND r3.post_type = 'revision'
                AND r3.post_date > r1.post_date
            ) >= 3
        ");
    }
    
    private function cleanup_spam_comments() {
        global $wpdb;
        
        // Delete spam comments older than 30 days
        $wpdb->query("
            DELETE c FROM {$wpdb->comments} c
            WHERE c.comment_approved = 'spam'
            AND c.comment_date < DATE_SUB(NOW(), INTERVAL 30 DAY)
        ");
        
        // Delete orphaned comment meta
        $wpdb->query("
            DELETE cm FROM {$wpdb->commentmeta} cm
            LEFT JOIN {$wpdb->comments} c ON cm.comment_id = c.comment_ID
            WHERE c.comment_ID IS NULL
        ");
    }
    
    private function cleanup_orphaned_meta() {
        global $wpdb;
        
        // Clean orphaned post meta
        $wpdb->query("
            DELETE pm FROM {$wpdb->postmeta} pm
            LEFT JOIN {$wpdb->posts} p ON pm.post_id = p.ID
            WHERE p.ID IS NULL
        ");
        
        // Clean orphaned user meta
        $wpdb->query("
            DELETE um FROM {$wpdb->usermeta} um
            LEFT JOIN {$wpdb->users} u ON um.user_id = u.ID
            WHERE u.ID IS NULL
        ");
        
        // Clean orphaned term meta
        $wpdb->query("
            DELETE tm FROM {$wpdb->termmeta} tm
            LEFT JOIN {$wpdb->terms} t ON tm.term_id = t.term_id
            WHERE t.term_id IS NULL
        ");
    }
    
    private function cleanup_expired_transients() {
        global $wpdb;
        
        // Delete expired transients
        $wpdb->query("
            DELETE FROM {$wpdb->options}
            WHERE option_name LIKE '_transient_timeout_%'
            AND option_value < UNIX_TIMESTAMP()
        ");
        
        $wpdb->query("
            DELETE FROM {$wpdb->options}
            WHERE option_name LIKE '_site_transient_timeout_%'
            AND option_value < UNIX_TIMESTAMP()
        ");
    }
    
    private function optimize_tables() {
        global $wpdb;
        
        $tables = array(
            $wpdb->posts,
            $wpdb->postmeta,
            $wpdb->comments,
            $wpdb->commentmeta,
            $wpdb->users,
            $wpdb->usermeta,
            $wpdb->options,
            $wpdb->terms,
            $wpdb->term_taxonomy,
            $wpdb->term_relationships,
            $wpdb->termmeta
        );
        
        foreach ($tables as $table) {
            $wpdb->query("OPTIMIZE TABLE {$table}");
        }
    }
    
    public function run_maintenance() {
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        $this->daily_maintenance();
        
        wp_send_json_success('Database maintenance completed');
    }
}

// Initialize database maintenance
new Database_Maintenance();
```

## Best Practices

### Database Optimization Guidelines

**Essential Optimizations**
- Regular index optimization
- Query performance monitoring
- Table structure optimization
- Connection pooling
- Query caching implementation

**Performance Monitoring**
- Slow query analysis
- Index usage statistics
- Connection monitoring
- Buffer pool optimization
- Regular maintenance tasks

### Common Database Issues

**Performance Problems**
- Missing indexes
- Inefficient queries
- Table fragmentation
- Connection limits
- Memory constraints

**Optimization Solutions**
- Proper indexing strategy
- Query optimization
- Regular maintenance
- Configuration tuning
- Monitoring implementation

## Future Trends

### Emerging Database Technologies

**Modern Database Solutions**
- Columnar storage
- In-memory databases
- Distributed databases
- NoSQL integration
- Cloud-native databases

**Performance Innovations**
- AI-powered optimization
- Predictive indexing
- Automated tuning
- Real-time monitoring
- Performance analytics