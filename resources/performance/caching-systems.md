# Advanced WordPress Caching Systems

## Overview

Advanced WordPress caching systems implement sophisticated multi-layer caching strategies to dramatically improve website performance, reduce server load, and enhance user experience through intelligent data storage and retrieval mechanisms.

## Caching Architecture

### Multi-Tier Caching Model

**L1 Cache - Memory (Fastest)**
- In-memory caching
- Application-level caching
- PHP opcode caching
- WordPress object cache
- Session storage

**L2 Cache - Redis/Memcached (Fast)**
- Distributed caching
- Network-accessible
- Persistent across requests
- Shared between servers
- High availability

**L3 Cache - Database (Medium)**
- Database query caching
- WordPress transients
- Custom cache tables
- Persistent storage
- Fallback mechanism

**L4 Cache - CDN/Edge (Distributed)**
- Geographic distribution
- Edge server caching
- Static asset caching
- Global content delivery
- Reduced latency

### Caching Strategy Matrix

**Cache Types by Content**
- Static content: CDN + Browser cache
- Dynamic content: Application cache
- Database queries: Query cache + Object cache
- User sessions: Distributed cache
- API responses: Edge cache

## Object Caching

### Redis Object Cache Implementation

**Redis Configuration**
```ini
# Redis server configuration
port 6379
bind 127.0.0.1
timeout 0
tcp-keepalive 300
maxmemory 2gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000

# Persistence settings
appendonly yes
appendfsync everysec
no-appendfsync-on-rewrite no
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

**WordPress Redis Integration**
```php
// wp-content/object-cache.php
class Redis_Object_Cache {
    private $redis;
    private $cache_prefix;
    private $global_groups = array('users', 'userlogins', 'usermeta', 'user_meta', 'site-transient', 'site-options', 'site-lookup', 'blog-lookup', 'blog-details', 'rss', 'global-posts', 'blog-id-cache');
    private $non_persistent_groups = array('comment', 'counts');
    
    public function __construct() {
        $this->redis = new Redis();
        $this->redis->connect('127.0.0.1', 6379, 1);
        $this->redis->setOption(Redis::OPT_SERIALIZER, Redis::SERIALIZE_PHP);
        $this->cache_prefix = $this->get_cache_prefix();
    }
    
    public function get($key, $group = 'default') {
        $redis_key = $this->build_key($key, $group);
        
        try {
            $value = $this->redis->get($redis_key);
            return $value !== false ? $value : false;
        } catch (Exception $e) {
            error_log('Redis get error: ' . $e->getMessage());
            return false;
        }
    }
    
    public function set($key, $value, $group = 'default', $expire = 0) {
        $redis_key = $this->build_key($key, $group);
        
        if (in_array($group, $this->non_persistent_groups)) {
            return true; // Don't cache non-persistent groups
        }
        
        try {
            if ($expire > 0) {
                return $this->redis->setex($redis_key, $expire, $value);
            } else {
                return $this->redis->set($redis_key, $value);
            }
        } catch (Exception $e) {
            error_log('Redis set error: ' . $e->getMessage());
            return false;
        }
    }
    
    public function delete($key, $group = 'default') {
        $redis_key = $this->build_key($key, $group);
        
        try {
            return $this->redis->del($redis_key) > 0;
        } catch (Exception $e) {
            error_log('Redis delete error: ' . $e->getMessage());
            return false;
        }
    }
    
    public function flush() {
        try {
            $keys = $this->redis->keys($this->cache_prefix . '*');
            if (!empty($keys)) {
                return $this->redis->del($keys) > 0;
            }
            return true;
        } catch (Exception $e) {
            error_log('Redis flush error: ' . $e->getMessage());
            return false;
        }
    }
    
    private function build_key($key, $group) {
        if (in_array($group, $this->global_groups)) {
            $prefix = $this->cache_prefix;
        } else {
            $prefix = $this->cache_prefix . get_current_blog_id() . ':';
        }
        
        return $prefix . $group . ':' . $key;
    }
    
    private function get_cache_prefix() {
        $prefix = defined('WP_CACHE_KEY_SALT') ? WP_CACHE_KEY_SALT : '';
        return $prefix . 'wp_cache:';
    }
}

// Initialize the cache
if (!defined('WP_USE_THEMES')) {
    $GLOBALS['wp_object_cache'] = new Redis_Object_Cache();
}
```

### Memcached Object Cache

**Memcached Configuration**
```ini
# Memcached configuration
-m 2048
-p 11211
-u memcached
-l 127.0.0.1
-c 1024
-t 4
-R 5
-b 8192
-B binary
```

**WordPress Memcached Integration**
```php
// wp-content/object-cache.php
class Memcached_Object_Cache {
    private $memcached;
    private $cache_prefix;
    private $global_groups = array('users', 'userlogins', 'usermeta', 'user_meta', 'site-transient', 'site-options', 'site-lookup', 'blog-lookup', 'blog-details', 'rss', 'global-posts', 'blog-id-cache');
    
    public function __construct() {
        $this->memcached = new Memcached();
        $this->memcached->addServer('127.0.0.1', 11211);
        $this->memcached->setOption(Memcached::OPT_COMPRESSION, true);
        $this->memcached->setOption(Memcached::OPT_DISTRIBUTION, Memcached::DISTRIBUTION_CONSISTENT);
        $this->cache_prefix = $this->get_cache_prefix();
    }
    
    public function get($key, $group = 'default') {
        $memcached_key = $this->build_key($key, $group);
        
        $value = $this->memcached->get($memcached_key);
        return $value !== false ? $value : false;
    }
    
    public function set($key, $value, $group = 'default', $expire = 0) {
        $memcached_key = $this->build_key($key, $group);
        
        if ($expire > 0) {
            return $this->memcached->set($memcached_key, $value, $expire);
        } else {
            return $this->memcached->set($memcached_key, $value);
        }
    }
    
    public function delete($key, $group = 'default') {
        $memcached_key = $this->build_key($key, $group);
        return $this->memcached->delete($memcached_key);
    }
    
    public function flush() {
        return $this->memcached->flush();
    }
    
    private function build_key($key, $group) {
        if (in_array($group, $this->global_groups)) {
            $prefix = $this->cache_prefix;
        } else {
            $prefix = $this->cache_prefix . get_current_blog_id() . ':';
        }
        
        return $prefix . $group . ':' . $key;
    }
    
    private function get_cache_prefix() {
        $prefix = defined('WP_CACHE_KEY_SALT') ? WP_CACHE_KEY_SALT : '';
        return $prefix . 'wp_cache:';
    }
}

// Initialize the cache
if (!defined('WP_USE_THEMES')) {
    $GLOBALS['wp_object_cache'] = new Memcached_Object_Cache();
}
```

## Page Caching

### Advanced Page Cache Implementation

**Nginx FastCGI Cache**
```nginx
# Nginx FastCGI cache configuration
fastcgi_cache_path /var/cache/nginx levels=1:2 keys_zone=WORDPRESS:100m inactive=60m max_size=1g;
fastcgi_cache_key "$scheme$request_method$host$request_uri$is_args$args";
fastcgi_cache_valid 200 60m;
fastcgi_cache_valid 404 1m;
fastcgi_cache_valid 301 302 10m;
fastcgi_cache_valid any 1m;
fastcgi_cache_use_stale error timeout invalid_header updating http_500 http_503;
fastcgi_cache_background_update on;
fastcgi_cache_lock on;
fastcgi_cache_lock_timeout 5s;

# Cache bypass conditions
map $request_uri $skip_cache {
    default 0;
    ~*/wp-admin/ 1;
    ~*/wp-login.php 1;
    ~*/wp-cron.php 1;
    ~*/xmlrpc.php 1;
    ~*/wp-json/ 1;
    ~*/feed/ 1;
    ~*/sitemap 1;
    ~*/robots.txt 1;
    ~*/favicon.ico 1;
}

server {
    listen 80;
    server_name example.com;
    root /var/www/html/wordpress;
    index index.php index.html;
    
    # Cache static files
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        add_header Vary Accept-Encoding;
        access_log off;
    }
    
    # WordPress PHP processing
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        
        # Cache configuration
        fastcgi_cache WORDPRESS;
        fastcgi_cache_bypass $skip_cache;
        fastcgi_no_cache $skip_cache;
        fastcgi_cache_valid 200 60m;
        
        # Cache headers
        add_header X-FastCGI-Cache $upstream_cache_status;
        add_header Cache-Control "public, max-age=3600";
    }
    
    # Cache purging
    location ~ /purge(/.*) {
        fastcgi_cache_purge WORDPRESS "$scheme$request_method$host$1";
    }
}
```

**WordPress Page Cache Plugin**
```php
// Advanced page cache plugin
class Advanced_Page_Cache {
    private $cache_dir;
    private $cache_time = 3600; // 1 hour
    private $excluded_pages = array();
    
    public function __construct() {
        $this->cache_dir = WP_CONTENT_DIR . '/cache/pages/';
        $this->init_hooks();
        $this->create_cache_directory();
    }
    
    public function init_hooks() {
        add_action('template_redirect', array($this, 'serve_cache'), 1);
        add_action('wp_footer', array($this, 'cache_page'));
        add_action('save_post', array($this, 'clear_post_cache'));
        add_action('comment_post', array($this, 'clear_comment_cache'));
        add_action('wp_set_comment_status', array($this, 'clear_comment_cache'));
    }
    
    public function serve_cache() {
        if ($this->should_cache()) {
            $cache_file = $this->get_cache_file();
            
            if (file_exists($cache_file) && $this->is_cache_valid($cache_file)) {
                // Serve cached content
                $content = file_get_contents($cache_file);
                $this->add_cache_headers();
                echo $content;
                exit;
            }
        }
    }
    
    public function cache_page() {
        if ($this->should_cache()) {
            $content = ob_get_contents();
            $cache_file = $this->get_cache_file();
            
            // Compress content
            if (function_exists('gzencode')) {
                $content = gzencode($content, 9);
                $cache_file .= '.gz';
            }
            
            file_put_contents($cache_file, $content);
        }
    }
    
    public function clear_post_cache($post_id) {
        $post = get_post($post_id);
        
        // Clear post cache
        $this->clear_cache_by_pattern('post_' . $post_id);
        
        // Clear related caches
        $this->clear_cache_by_pattern('home');
        $this->clear_cache_by_pattern('blog');
        $this->clear_cache_by_pattern('archive');
        
        // Clear category and tag caches
        $categories = wp_get_post_categories($post_id);
        foreach ($categories as $cat_id) {
            $this->clear_cache_by_pattern('category_' . $cat_id);
        }
        
        $tags = wp_get_post_tags($post_id);
        foreach ($tags as $tag) {
            $this->clear_cache_by_pattern('tag_' . $tag->term_id);
        }
    }
    
    private function should_cache() {
        // Don't cache for logged-in users
        if (is_user_logged_in()) {
            return false;
        }
        
        // Don't cache admin pages
        if (is_admin()) {
            return false;
        }
        
        // Don't cache 404 pages
        if (is_404()) {
            return false;
        }
        
        // Don't cache search pages
        if (is_search()) {
            return false;
        }
        
        // Don't cache excluded pages
        $current_url = $_SERVER['REQUEST_URI'];
        foreach ($this->excluded_pages as $pattern) {
            if (strpos($current_url, $pattern) !== false) {
                return false;
            }
        }
        
        return true;
    }
    
    private function get_cache_file() {
        $uri = $_SERVER['REQUEST_URI'];
        $filename = md5($uri) . '.html';
        return $this->cache_dir . $filename;
    }
    
    private function is_cache_valid($cache_file) {
        return (time() - filemtime($cache_file)) < $this->cache_time;
    }
    
    private function clear_cache_by_pattern($pattern) {
        $files = glob($this->cache_dir . '*' . $pattern . '*');
        foreach ($files as $file) {
            unlink($file);
        }
    }
    
    private function add_cache_headers() {
        header('X-Cache: HIT');
        header('Cache-Control: public, max-age=3600');
        header('Expires: ' . gmdate('D, d M Y H:i:s', time() + 3600) . ' GMT');
    }
    
    private function create_cache_directory() {
        if (!file_exists($this->cache_dir)) {
            wp_mkdir_p($this->cache_dir);
        }
    }
}

// Initialize the page cache
new Advanced_Page_Cache();
```

## Database Caching

### Query Cache Implementation

**MySQL Query Cache**
```sql
-- Enable query cache
SET GLOBAL query_cache_type = ON;
SET GLOBAL query_cache_size = 256M;
SET GLOBAL query_cache_limit = 2M;

-- Monitor query cache
SHOW STATUS LIKE 'Qcache%';

-- Query cache statistics
SELECT 
    Qcache_hits / (Qcache_hits + Qcache_inserts) * 100 AS hit_ratio,
    Qcache_hits,
    Qcache_inserts,
    Qcache_not_cached
FROM (
    SELECT 
        VARIABLE_VALUE AS Qcache_hits
    FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
    WHERE VARIABLE_NAME = 'Qcache_hits'
) a
CROSS JOIN (
    SELECT 
        VARIABLE_VALUE AS Qcache_inserts
    FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
    WHERE VARIABLE_NAME = 'Qcache_inserts'
) b
CROSS JOIN (
    SELECT 
        VARIABLE_VALUE AS Qcache_not_cached
    FROM INFORMATION_SCHEMA.GLOBAL_STATUS 
    WHERE VARIABLE_NAME = 'Qcache_not_cached'
) c;
```

**WordPress Query Cache**
```php
// WordPress query cache implementation
class WordPress_Query_Cache {
    private $cache_group = 'wp_query_cache';
    private $cache_time = 3600; // 1 hour
    
    public function __construct() {
        add_filter('posts_pre_query', array($this, 'cache_query'), 10, 2);
        add_action('save_post', array($this, 'invalidate_related_queries'));
        add_action('delete_post', array($this, 'invalidate_related_queries'));
    }
    
    public function cache_query($posts, $query) {
        // Only cache main queries
        if (!$query->is_main_query()) {
            return null;
        }
        
        // Don't cache admin queries
        if (is_admin()) {
            return null;
        }
        
        // Don't cache user-specific queries
        if (is_user_logged_in()) {
            return null;
        }
        
        $cache_key = $this->generate_cache_key($query);
        $cached_posts = wp_cache_get($cache_key, $this->cache_group);
        
        if ($cached_posts !== false) {
            // Set the cached posts and return early
            $query->posts = $cached_posts;
            $query->post_count = count($cached_posts);
            $query->found_posts = wp_cache_get($cache_key . '_found', $this->cache_group);
            return $cached_posts;
        }
        
        return null; // Let WordPress handle the query
    }
    
    public function cache_query_results($posts, $query) {
        if ($query->is_main_query() && !is_admin() && !is_user_logged_in()) {
            $cache_key = $this->generate_cache_key($query);
            
            wp_cache_set($cache_key, $posts, $this->cache_group, $this->cache_time);
            wp_cache_set($cache_key . '_found', $query->found_posts, $this->cache_group, $this->cache_time);
        }
        
        return $posts;
    }
    
    public function invalidate_related_queries($post_id) {
        $post = get_post($post_id);
        
        // Clear homepage cache
        $this->clear_cache_pattern('home');
        
        // Clear blog archive cache
        $this->clear_cache_pattern('blog');
        
        // Clear category caches
        $categories = wp_get_post_categories($post_id);
        foreach ($categories as $cat_id) {
            $this->clear_cache_pattern('category_' . $cat_id);
        }
        
        // Clear tag caches
        $tags = wp_get_post_tags($post_id);
        foreach ($tags as $tag) {
            $this->clear_cache_pattern('tag_' . $tag->term_id);
        }
        
        // Clear author cache
        $this->clear_cache_pattern('author_' . $post->post_author);
    }
    
    private function generate_cache_key($query) {
        $query_vars = $query->query_vars;
        
        // Remove non-cacheable variables
        unset($query_vars['cache_results']);
        unset($query_vars['update_post_meta_cache']);
        unset($query_vars['update_post_term_cache']);
        
        return 'query_' . md5(serialize($query_vars));
    }
    
    private function clear_cache_pattern($pattern) {
        global $wpdb;
        
        // Clear from object cache
        wp_cache_flush_group($this->cache_group);
        
        // Clear from database if using persistent cache
        $wpdb->query($wpdb->prepare(
            "DELETE FROM {$wpdb->options} WHERE option_name LIKE %s",
            '_transient_' . $pattern . '%'
        ));
    }
}

// Initialize query cache
new WordPress_Query_Cache();
```

## CDN and Edge Caching

### CDN Integration

**CloudFlare Integration**
```php
// CloudFlare cache management
class CloudFlare_Cache {
    private $api_email;
    private $api_key;
    private $zone_id;
    
    public function __construct($api_email, $api_key, $zone_id) {
        $this->api_email = $api_email;
        $this->api_key = $api_key;
        $this->zone_id = $zone_id;
    }
    
    public function purge_cache($urls = array()) {
        if (empty($urls)) {
            // Purge all cache
            return $this->purge_all_cache();
        } else {
            // Purge specific URLs
            return $this->purge_urls($urls);
        }
    }
    
    private function purge_all_cache() {
        $url = "https://api.cloudflare.com/client/v4/zones/{$this->zone_id}/purge_cache";
        
        $data = array(
            'purge_everything' => true
        );
        
        return $this->make_api_request($url, $data);
    }
    
    private function purge_urls($urls) {
        $url = "https://api.cloudflare.com/client/v4/zones/{$this->zone_id}/purge_cache";
        
        $data = array(
            'files' => $urls
        );
        
        return $this->make_api_request($url, $data);
    }
    
    private function make_api_request($url, $data) {
        $headers = array(
            'X-Auth-Email: ' . $this->api_email,
            'X-Auth-Key: ' . $this->api_key,
            'Content-Type: application/json'
        );
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        return $http_code === 200;
    }
}

// WordPress integration
class WordPress_CloudFlare {
    private $cloudflare;
    
    public function __construct() {
        $this->cloudflare = new CloudFlare_Cache(
            get_option('cloudflare_api_email'),
            get_option('cloudflare_api_key'),
            get_option('cloudflare_zone_id')
        );
        
        add_action('save_post', array($this, 'purge_post_cache'));
        add_action('delete_post', array($this, 'purge_post_cache'));
    }
    
    public function purge_post_cache($post_id) {
        $post = get_post($post_id);
        $urls = array(
            get_permalink($post_id),
            home_url('/'),
            home_url('/blog/')
        );
        
        $this->cloudflare->purge_cache($urls);
    }
}
```

## Cache Invalidation Strategies

### Smart Cache Invalidation

**Event-Based Invalidation**
```php
// Smart cache invalidation system
class Smart_Cache_Invalidation {
    private $invalidation_rules;
    
    public function __construct() {
        $this->invalidation_rules = array(
            'post' => array(
                'save_post' => array('home', 'blog', 'archive', 'category', 'tag', 'author'),
                'delete_post' => array('home', 'blog', 'archive', 'category', 'tag', 'author'),
                'transition_post_status' => array('home', 'blog', 'archive', 'category', 'tag', 'author')
            ),
            'comment' => array(
                'comment_post' => array('post', 'home'),
                'wp_set_comment_status' => array('post', 'home')
            ),
            'term' => array(
                'created_term' => array('archive', 'category', 'tag'),
                'edited_term' => array('archive', 'category', 'tag'),
                'delete_term' => array('archive', 'category', 'tag')
            ),
            'user' => array(
                'user_register' => array('home'),
                'profile_update' => array('author'),
                'delete_user' => array('author')
            )
        );
        
        $this->init_hooks();
    }
    
    public function init_hooks() {
        foreach ($this->invalidation_rules as $object_type => $events) {
            foreach ($events as $event => $cache_types) {
                add_action($event, array($this, 'invalidate_cache'), 10, 1);
            }
        }
    }
    
    public function invalidate_cache($object_id) {
        $event = current_action();
        $object_type = $this->get_object_type_from_event($event);
        
        if (isset($this->invalidation_rules[$object_type][$event])) {
            $cache_types = $this->invalidation_rules[$object_type][$event];
            
            foreach ($cache_types as $cache_type) {
                $this->clear_cache_by_type($cache_type, $object_id);
            }
        }
    }
    
    private function get_object_type_from_event($event) {
        foreach ($this->invalidation_rules as $object_type => $events) {
            if (array_key_exists($event, $events)) {
                return $object_type;
            }
        }
        return null;
    }
    
    private function clear_cache_by_type($cache_type, $object_id) {
        switch ($cache_type) {
            case 'home':
                $this->clear_home_cache();
                break;
            case 'blog':
                $this->clear_blog_cache();
                break;
            case 'archive':
                $this->clear_archive_cache();
                break;
            case 'category':
                $this->clear_category_cache($object_id);
                break;
            case 'tag':
                $this->clear_tag_cache($object_id);
                break;
            case 'author':
                $this->clear_author_cache($object_id);
                break;
            case 'post':
                $this->clear_post_cache($object_id);
                break;
        }
    }
    
    private function clear_home_cache() {
        wp_cache_delete('home_page', 'page_cache');
        $this->purge_cdn_cache(array(home_url('/')));
    }
    
    private function clear_blog_cache() {
        wp_cache_delete('blog_page', 'page_cache');
        $this->purge_cdn_cache(array(home_url('/blog/')));
    }
    
    private function clear_post_cache($post_id) {
        wp_cache_delete('post_' . $post_id, 'page_cache');
        $this->purge_cdn_cache(array(get_permalink($post_id)));
    }
    
    private function purge_cdn_cache($urls) {
        // Implement CDN cache purging
        if (class_exists('CloudFlare_Cache')) {
            $cloudflare = new CloudFlare_Cache(
                get_option('cloudflare_api_email'),
                get_option('cloudflare_api_key'),
                get_option('cloudflare_zone_id')
            );
            $cloudflare->purge_cache($urls);
        }
    }
}

// Initialize smart cache invalidation
new Smart_Cache_Invalidation();
```

## Performance Monitoring

### Cache Performance Metrics

**Cache Hit Rate Monitoring**
```php
// Cache performance monitoring
class Cache_Performance_Monitor {
    private $metrics = array();
    
    public function __construct() {
        add_action('wp_footer', array($this, 'log_cache_metrics'));
        add_action('wp_ajax_cache_metrics', array($this, 'handle_cache_metrics'));
    }
    
    public function log_cache_metrics() {
        global $wp_object_cache;
        
        $metrics = array(
            'cache_hits' => $wp_object_cache->cache_hits,
            'cache_misses' => $wp_object_cache->cache_misses,
            'cache_ratio' => $this->calculate_cache_ratio(),
            'memory_usage' => memory_get_peak_usage(true),
            'page_load_time' => $this->get_page_load_time(),
            'timestamp' => time()
        );
        
        $this->store_metrics($metrics);
    }
    
    private function calculate_cache_ratio() {
        global $wp_object_cache;
        
        $total = $wp_object_cache->cache_hits + $wp_object_cache->cache_misses;
        if ($total === 0) {
            return 0;
        }
        
        return ($wp_object_cache->cache_hits / $total) * 100;
    }
    
    private function get_page_load_time() {
        if (isset($_SERVER['REQUEST_TIME_FLOAT'])) {
            return microtime(true) - $_SERVER['REQUEST_TIME_FLOAT'];
        }
        
        return 0;
    }
    
    private function store_metrics($metrics) {
        global $wpdb;
        
        $wpdb->insert(
            $wpdb->prefix . 'cache_metrics',
            $metrics,
            array('%d', '%d', '%f', '%d', '%f', '%d')
        );
    }
    
    public function get_cache_performance_report($days = 7) {
        global $wpdb;
        
        $results = $wpdb->get_results($wpdb->prepare(
            "SELECT 
                DATE(FROM_UNIXTIME(timestamp)) as date,
                AVG(cache_ratio) as avg_cache_ratio,
                AVG(page_load_time) as avg_load_time,
                AVG(memory_usage) as avg_memory_usage,
                COUNT(*) as page_views
            FROM {$wpdb->prefix}cache_metrics 
            WHERE timestamp >= %d 
            GROUP BY DATE(FROM_UNIXTIME(timestamp))
            ORDER BY date DESC",
            time() - ($days * 24 * 60 * 60)
        ));
        
        return $results;
    }
}
```

## Best Practices

### Caching Strategy Guidelines

**Cache Hierarchy**
1. Browser cache (longest TTL)
2. CDN cache (medium TTL)
3. Application cache (short TTL)
4. Database cache (shortest TTL)

**Cache Key Design**
- Use consistent naming conventions
- Include version numbers for cache busting
- Use hierarchical keys for easy invalidation
- Avoid special characters in keys
- Keep keys reasonably short

**Cache TTL Strategy**
- Static content: 1 year
- Dynamic content: 1 hour
- User-specific content: 15 minutes
- Real-time data: 1 minute
- Session data: Until logout

### Common Caching Pitfalls

**Cache Invalidation Issues**
- Stale data serving
- Partial cache invalidation
- Race conditions
- Memory leaks
- Performance degradation

**Cache Configuration Problems**
- Inappropriate TTL values
- Memory limits exceeded
- Network latency issues
- Cache warming problems
- Monitoring gaps

## Future Trends

### Emerging Caching Technologies

**Edge Computing Caching**
- Edge server caching
- Geographic distribution
- Reduced latency
- Bandwidth optimization
- Real-time invalidation

**AI-Powered Caching**
- Predictive cache warming
- Intelligent invalidation
- Dynamic TTL adjustment
- Performance optimization
- Anomaly detection

### Industry Evolution

**Modern Caching Approaches**
- Microservices caching
- Event-driven invalidation
- Distributed caching
- Cloud-native solutions
- Performance-first design