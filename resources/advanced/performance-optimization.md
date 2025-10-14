# WordPress Performance Optimization

Comprehensive guide to optimizing WordPress performance, caching, and database efficiency.

## Performance Fundamentals

### Performance Metrics and Monitoring

```php
// Performance monitoring functions
function start_performance_timer($name) {
    global $performance_timers;
    $performance_timers[$name] = microtime(true);
}

function end_performance_timer($name) {
    global $performance_timers;
    
    if (isset($performance_timers[$name])) {
        $duration = microtime(true) - $performance_timers[$name];
        
        if (WP_DEBUG) {
            error_log("Performance Timer [$name]: " . round($duration * 1000, 2) . "ms");
        }
        
        return $duration;
    }
    
    return false;
}

// Monitor database queries
function monitor_database_queries() {
    if (!WP_DEBUG) {
        return;
    }
    
    add_action('wp_footer', function() {
        global $wpdb;
        
        echo "<!-- Database Queries: " . count($wpdb->queries) . " -->";
        echo "<!-- Query Time: " . round($wpdb->time_by_type['SELECT'], 4) . "s -->";
        echo "<!-- Memory Usage: " . round(memory_get_peak_usage(true) / 1024 / 1024, 2) . "MB -->";
    });
}

// Track page load time
function track_page_load_time() {
    if (!WP_DEBUG) {
        return;
    }
    
    add_action('wp_head', function() {
        echo '<script>
        window.performance && window.performance.mark && window.performance.mark("wp-start");
        </script>';
    });
    
    add_action('wp_footer', function() {
        echo '<script>
        window.performance && window.performance.mark && window.performance.mark("wp-end");
        window.performance && window.performance.measure && window.performance.measure("wp-load", "wp-start", "wp-end");
        </script>';
    });
}
```

### Core Performance Settings

```php
// WordPress performance optimizations
function optimize_wordpress_performance() {
    // Remove unnecessary WordPress features
    remove_action('wp_head', 'wp_generator');
    remove_action('wp_head', 'wlwmanifest_link');
    remove_action('wp_head', 'rsd_link');
    remove_action('wp_head', 'wp_shortlink_wp_head');
    remove_action('wp_head', 'feed_links', 2);
    remove_action('wp_head', 'feed_links_extra', 3);
    
    // Remove emoji scripts
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('wp_print_styles', 'print_emoji_styles');
    remove_action('admin_print_scripts', 'print_emoji_detection_script');
    remove_action('admin_print_styles', 'print_emoji_styles');
    remove_filter('the_content_feed', 'wp_staticize_emoji');
    remove_filter('comment_text_rss', 'wp_staticize_emoji');
    remove_filter('wp_mail', 'wp_staticize_emoji_for_email');
    
    // Disable XML-RPC if not needed
    add_filter('xmlrpc_enabled', '__return_false');
    
    // Remove unnecessary HTTP headers
    remove_action('template_redirect', 'wp_shortlink_header', 11);
    
    // Optimize admin bar
    if (!is_admin()) {
        show_admin_bar(false);
    }
}

add_action('init', 'optimize_wordpress_performance');
```

## Database Optimization

### Query Optimization

```php
// Optimize database queries
function optimize_database_queries($query) {
    if (is_admin() || !$query->is_main_query()) {
        return;
    }
    
    // Limit posts per page
    if (is_home() || is_archive()) {
        $query->set('posts_per_page', 10);
    }
    
    // Optimize category queries
    if (is_category()) {
        $query->set('posts_per_page', 12);
        $query->set('no_found_rows', true);
    }
    
    // Optimize search queries
    if (is_search()) {
        $query->set('posts_per_page', 8);
        $query->set('meta_query', array(
            array(
                'key' => '_thumbnail_id',
                'compare' => 'EXISTS'
            )
        ));
    }
}

add_action('pre_get_posts', 'optimize_database_queries');

// Optimize meta queries
function optimize_meta_queries($args) {
    // Add indexes for commonly queried meta fields
    $args['meta_query'] = array(
        'relation' => 'AND',
        array(
            'key' => '_featured',
            'value' => '1',
            'compare' => '='
        ),
        array(
            'key' => '_stock_status',
            'value' => 'instock',
            'compare' => '='
        )
    );
    
    return $args;
}

// Database cleanup functions
function cleanup_database() {
    global $wpdb;
    
    // Remove spam comments
    $wpdb->query("DELETE FROM {$wpdb->comments} WHERE comment_approved = 'spam'");
    
    // Remove trashed posts
    $wpdb->query("DELETE FROM {$wpdb->posts} WHERE post_status = 'trash'");
    
    // Remove orphaned post meta
    $wpdb->query("DELETE pm FROM {$wpdb->postmeta} pm LEFT JOIN {$wpdb->posts} p ON pm.post_id = p.ID WHERE p.ID IS NULL");
    
    // Remove orphaned comment meta
    $wpdb->query("DELETE cm FROM {$wpdb->commentmeta} cm LEFT JOIN {$wpdb->comments} c ON cm.comment_id = c.comment_ID WHERE c.comment_ID IS NULL");
    
    // Optimize tables
    $tables = array(
        $wpdb->posts,
        $wpdb->postmeta,
        $wpdb->comments,
        $wpdb->commentmeta,
        $wpdb->options,
        $wpdb->usermeta
    );
    
    foreach ($tables as $table) {
        $wpdb->query("OPTIMIZE TABLE $table");
    }
}

// Schedule database cleanup
add_action('wp_scheduled_delete', 'cleanup_database');
```

### Database Caching

```php
// Object caching implementation
class Simple_Object_Cache {
    private $cache = array();
    private $cache_group = 'default';
    
    public function set($key, $data, $group = 'default', $expire = 3600) {
        $cache_key = $group . '_' . $key;
        $this->cache[$cache_key] = array(
            'data' => $data,
            'expire' => time() + $expire
        );
        
        // Also store in transients for persistence
        set_transient($cache_key, $data, $expire);
    }
    
    public function get($key, $group = 'default') {
        $cache_key = $group . '_' . $key;
        
        // Check memory cache first
        if (isset($this->cache[$cache_key])) {
            if ($this->cache[$cache_key]['expire'] > time()) {
                return $this->cache[$cache_key]['data'];
            } else {
                unset($this->cache[$cache_key]);
            }
        }
        
        // Fallback to transient
        $data = get_transient($cache_key);
        if ($data !== false) {
            $this->cache[$cache_key] = array(
                'data' => $data,
                'expire' => time() + 3600
            );
            return $data;
        }
        
        return false;
    }
    
    public function delete($key, $group = 'default') {
        $cache_key = $group . '_' . $key;
        unset($this->cache[$cache_key]);
        delete_transient($cache_key);
    }
    
    public function flush() {
        $this->cache = array();
    }
}

$simple_cache = new Simple_Object_Cache();

// Cache expensive database queries
function get_cached_posts($args = array()) {
    global $simple_cache;
    
    $cache_key = 'posts_' . md5(serialize($args));
    $posts = $simple_cache->get($cache_key, 'posts');
    
    if ($posts === false) {
        $posts = get_posts($args);
        $simple_cache->set($cache_key, $posts, 'posts', 300); // 5 minutes
    }
    
    return $posts;
}

// Cache user data
function get_cached_user_data($user_id) {
    global $simple_cache;
    
    $cache_key = 'user_' . $user_id;
    $user_data = $simple_cache->get($cache_key, 'users');
    
    if ($user_data === false) {
        $user = get_userdata($user_id);
        $user_data = array(
            'id' => $user->ID,
            'login' => $user->user_login,
            'email' => $user->user_email,
            'display_name' => $user->display_name,
            'roles' => $user->roles
        );
        
        $simple_cache->set($cache_key, $user_data, 'users', 1800); // 30 minutes
    }
    
    return $user_data;
}
```

## Caching Strategies

### Page Caching

```php
// Simple page caching
class Simple_Page_Cache {
    private $cache_dir;
    private $cache_time = 3600; // 1 hour
    
    public function __construct() {
        $this->cache_dir = WP_CONTENT_DIR . '/cache/pages/';
        
        if (!file_exists($this->cache_dir)) {
            wp_mkdir_p($this->cache_dir);
        }
    }
    
    public function get_cache_key() {
        $request_uri = $_SERVER['REQUEST_URI'];
        $user_agent = $_SERVER['HTTP_USER_AGENT'];
        
        // Different cache for mobile vs desktop
        $is_mobile = wp_is_mobile();
        $cache_key = md5($request_uri . $user_agent . ($is_mobile ? 'mobile' : 'desktop'));
        
        return $cache_key;
    }
    
    public function get($cache_key) {
        $cache_file = $this->cache_dir . $cache_key . '.html';
        
        if (file_exists($cache_file) && (time() - filemtime($cache_file)) < $this->cache_time) {
            return file_get_contents($cache_file);
        }
        
        return false;
    }
    
    public function set($cache_key, $content) {
        // Don't cache admin pages, logged-in users, or pages with errors
        if (is_admin() || is_user_logged_in() || is_404() || is_search()) {
            return false;
        }
        
        $cache_file = $this->cache_dir . $cache_key . '.html';
        
        // Add cache headers
        $cache_headers = "<!-- Cached: " . date('Y-m-d H:i:s') . " -->\n";
        $content = $cache_headers . $content;
        
        return file_put_contents($cache_file, $content);
    }
    
    public function delete($cache_key) {
        $cache_file = $this->cache_dir . $cache_key . '.html';
        
        if (file_exists($cache_file)) {
            return unlink($cache_file);
        }
        
        return false;
    }
    
    public function flush() {
        $files = glob($this->cache_dir . '*.html');
        
        foreach ($files as $file) {
            unlink($file);
        }
        
        return true;
    }
}

$page_cache = new Simple_Page_Cache();

// Implement page caching
add_action('template_redirect', function() {
    global $page_cache;
    
    $cache_key = $page_cache->get_cache_key();
    $cached_content = $page_cache->get($cache_key);
    
    if ($cached_content !== false) {
        echo $cached_content;
        exit;
    }
    
    // Start output buffering to capture content
    ob_start();
});

add_action('wp_footer', function() {
    global $page_cache;
    
    $cache_key = $page_cache->get_cache_key();
    $content = ob_get_contents();
    
    $page_cache->set($cache_key, $content);
    ob_end_flush();
});

// Clear cache when content is updated
add_action('save_post', function($post_id) {
    global $page_cache;
    $page_cache->flush();
});

add_action('comment_post', function($comment_id) {
    global $page_cache;
    $page_cache->flush();
});
```

### Fragment Caching

```php
// Fragment caching for dynamic content
function get_cached_fragment($key, $callback, $expire = 3600) {
    $cache_key = 'fragment_' . $key;
    $cached_content = get_transient($cache_key);
    
    if ($cached_content === false) {
        ob_start();
        call_user_func($callback);
        $cached_content = ob_get_clean();
        
        set_transient($cache_key, $cached_content, $expire);
    }
    
    echo $cached_content;
}

// Usage example
function display_recent_posts() {
    get_cached_fragment('recent_posts', function() {
        $posts = get_posts(array(
            'numberposts' => 5,
            'post_status' => 'publish'
        ));
        
        echo '<div class="recent-posts">';
        echo '<h3>Recent Posts</h3>';
        echo '<ul>';
        
        foreach ($posts as $post) {
            echo '<li><a href="' . get_permalink($post->ID) . '">' . $post->post_title . '</a></li>';
        }
        
        echo '</ul>';
        echo '</div>';
    }, 1800); // 30 minutes
}

// Clear fragment cache
function clear_fragment_cache($key = null) {
    if ($key) {
        delete_transient('fragment_' . $key);
    } else {
        // Clear all fragment caches
        global $wpdb;
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_fragment_%'");
        $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_fragment_%'");
    }
}
```

## Asset Optimization

### CSS and JavaScript Optimization

```php
// Optimize CSS and JavaScript loading
function optimize_asset_loading() {
    // Remove unnecessary scripts
    wp_dequeue_script('wp-embed');
    wp_dequeue_script('jquery-migrate');
    
    // Defer non-critical JavaScript
    add_filter('script_loader_tag', function($tag, $handle, $src) {
        $defer_scripts = array(
            'wp-embed',
            'comment-reply',
            'wp-emoji'
        );
        
        if (in_array($handle, $defer_scripts)) {
            return str_replace(' src', ' defer src', $tag);
        }
        
        return $tag;
    }, 10, 3);
    
    // Async load non-critical scripts
    add_filter('script_loader_tag', function($tag, $handle, $src) {
        $async_scripts = array(
            'google-analytics',
            'facebook-pixel'
        );
        
        if (in_array($handle, $async_scripts)) {
            return str_replace(' src', ' async src', $tag);
        }
        
        return $tag;
    }, 10, 3);
    
    // Remove unused CSS
    add_action('wp_enqueue_scripts', function() {
        if (!is_admin()) {
            wp_dequeue_style('wp-block-library');
            wp_dequeue_style('wp-block-library-theme');
            wp_dequeue_style('wc-block-style');
        }
    });
}

add_action('wp_enqueue_scripts', 'optimize_asset_loading', 100);

// Critical CSS implementation
function add_critical_css() {
    $critical_css = "
    /* Critical CSS for above-the-fold content */
    .header { display: flex; justify-content: space-between; align-items: center; }
    .hero { background: #f0f0f0; padding: 2rem; text-align: center; }
    .navigation { display: flex; list-style: none; }
    ";
    
    echo '<style id="critical-css">' . $critical_css . '</style>';
    
    // Load non-critical CSS asynchronously
    echo '<link rel="preload" href="' . get_stylesheet_uri() . '" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">';
    echo '<noscript><link rel="stylesheet" href="' . get_stylesheet_uri() . '"></noscript>';
}

add_action('wp_head', 'add_critical_css', 1);

// Combine and minify CSS
function combine_css_files() {
    $css_files = array(
        get_stylesheet_directory_uri() . '/style.css',
        get_stylesheet_directory_uri() . '/responsive.css',
        get_stylesheet_directory_uri() . '/custom.css'
    );
    
    $combined_css = '';
    
    foreach ($css_files as $css_file) {
        $css_content = file_get_contents($css_file);
        $combined_css .= $css_content . "\n";
    }
    
    // Minify CSS
    $combined_css = preg_replace('/\s+/', ' ', $combined_css);
    $combined_css = preg_replace('/;\s*}/', '}', $combined_css);
    $combined_css = preg_replace('/{\s*/', '{', $combined_css);
    
    // Save combined CSS
    $upload_dir = wp_upload_dir();
    $combined_file = $upload_dir['basedir'] . '/combined.css';
    file_put_contents($combined_file, $combined_css);
    
    // Enqueue combined CSS
    wp_enqueue_style('combined-css', $upload_dir['baseurl'] . '/combined.css', array(), filemtime($combined_file));
}

add_action('wp_enqueue_scripts', 'combine_css_files');
```

### Image Optimization

```php
// Image optimization and lazy loading
function optimize_images() {
    // Add lazy loading to images
    add_filter('the_content', function($content) {
        $content = preg_replace('/<img(.*?)src=/', '<img$1loading="lazy" src=', $content);
        return $content;
    });
    
    // Add WebP support
    add_filter('wp_get_attachment_image_src', function($image, $attachment_id, $size) {
        if (function_exists('imagewebp')) {
            $webp_url = str_replace(array('.jpg', '.jpeg', '.png'), '.webp', $image[0]);
            
            if (file_exists(str_replace(wp_upload_dir()['baseurl'], wp_upload_dir()['basedir'], $webp_url))) {
                $image[0] = $webp_url;
            }
        }
        
        return $image;
    }, 10, 3);
    
    // Responsive images
    add_filter('wp_get_attachment_image_attributes', function($attr, $attachment, $size) {
        $attr['sizes'] = '(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw';
        return $attr;
    }, 10, 3);
}

add_action('init', 'optimize_images');

// Generate WebP images
function generate_webp_images($attachment_id) {
    $file_path = get_attached_file($attachment_id);
    $file_info = pathinfo($file_path);
    
    if (!in_array(strtolower($file_info['extension']), array('jpg', 'jpeg', 'png'))) {
        return false;
    }
    
    $webp_path = $file_info['dirname'] . '/' . $file_info['filename'] . '.webp';
    
    if (function_exists('imagewebp')) {
        switch (strtolower($file_info['extension'])) {
            case 'jpg':
            case 'jpeg':
                $image = imagecreatefromjpeg($file_path);
                break;
            case 'png':
                $image = imagecreatefrompng($file_path);
                break;
        }
        
        if ($image) {
            imagewebp($image, $webp_path, 80);
            imagedestroy($image);
            return true;
        }
    }
    
    return false;
}

add_action('add_attachment', 'generate_webp_images');

// Optimize image sizes
function optimize_image_sizes() {
    // Remove unnecessary image sizes
    remove_image_size('medium_large');
    
    // Add custom image sizes
    add_image_size('custom-thumbnail', 300, 200, true);
    add_image_size('custom-medium', 600, 400, true);
    add_image_size('custom-large', 1200, 800, true);
    
    // Limit image quality
    add_filter('jpeg_quality', function($quality) {
        return 85;
    });
    
    add_filter('wp_editor_set_quality', function($quality) {
        return 85;
    });
}

add_action('after_setup_theme', 'optimize_image_sizes');
```

## CDN Integration

### Content Delivery Network

```php
// CDN integration
function setup_cdn() {
    $cdn_domain = get_option('cdn_domain');
    
    if (!$cdn_domain) {
        return;
    }
    
    // Replace URLs with CDN URLs
    add_filter('wp_get_attachment_url', function($url) use ($cdn_domain) {
        $upload_dir = wp_upload_dir();
        return str_replace($upload_dir['baseurl'], $cdn_domain, $url);
    });
    
    add_filter('the_content', function($content) use ($cdn_domain) {
        $upload_dir = wp_upload_dir();
        return str_replace($upload_dir['baseurl'], $cdn_domain, $content);
    });
    
    // CDN for CSS and JS
    add_filter('style_loader_src', function($src) use ($cdn_domain) {
        return str_replace(home_url(), $cdn_domain, $src);
    });
    
    add_filter('script_loader_src', function($src) use ($cdn_domain) {
        return str_replace(home_url(), $cdn_domain, $src);
    });
}

add_action('init', 'setup_cdn');

// CloudFlare integration
function cloudflare_optimization() {
    // Add CloudFlare headers
    add_action('wp_head', function() {
        echo '<meta name="cf-2fa-verify" content="your-2fa-token">';
    });
    
    // Purge CloudFlare cache
    function purge_cloudflare_cache($urls = array()) {
        $zone_id = get_option('cloudflare_zone_id');
        $api_token = get_option('cloudflare_api_token');
        
        if (!$zone_id || !$api_token) {
            return false;
        }
        
        $data = array(
            'purge_everything' => empty($urls)
        );
        
        if (!empty($urls)) {
            $data['files'] = $urls;
        }
        
        $response = wp_remote_post("https://api.cloudflare.com/client/v4/zones/{$zone_id}/purge_cache", array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $api_token,
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode($data)
        ));
        
        return !is_wp_error($response);
    }
    
    // Purge cache on content update
    add_action('save_post', function($post_id) {
        $urls = array(get_permalink($post_id));
        purge_cloudflare_cache($urls);
    });
    
    add_action('comment_post', function($comment_id) {
        $comment = get_comment($comment_id);
        $urls = array(get_permalink($comment->comment_post_ID));
        purge_cloudflare_cache($urls);
    });
}

add_action('init', 'cloudflare_optimization');
```

## Advanced Optimization

### Query Optimization

```php
// Advanced query optimization
function optimize_wp_queries() {
    // Disable unnecessary queries
    add_action('wp_head', function() {
        remove_action('wp_head', 'wp_generator');
        remove_action('wp_head', 'wlwmanifest_link');
        remove_action('wp_head', 'rsd_link');
        remove_action('wp_head', 'wp_shortlink_wp_head');
    });
    
    // Optimize main query
    add_action('pre_get_posts', function($query) {
        if (is_admin() || !$query->is_main_query()) {
            return;
        }
        
        // Limit posts per page
        if (is_home() || is_archive()) {
            $query->set('posts_per_page', 10);
        }
        
        // Optimize search queries
        if (is_search()) {
            $query->set('posts_per_page', 8);
            $query->set('orderby', 'relevance');
        }
        
        // Optimize category queries
        if (is_category()) {
            $query->set('posts_per_page', 12);
            $query->set('no_found_rows', true);
        }
    });
    
    // Optimize meta queries
    add_filter('posts_where', function($where, $query) {
        global $wpdb;
        
        if (is_search() && $query->is_main_query()) {
            // Add meta search
            $search_term = $query->get('s');
            $where .= " OR EXISTS (
                SELECT 1 FROM {$wpdb->postmeta} 
                WHERE {$wpdb->postmeta}.post_id = {$wpdb->posts}.ID 
                AND {$wpdb->postmeta}.meta_value LIKE '%{$search_term}%'
            )";
        }
        
        return $where;
    }, 10, 2);
}

add_action('init', 'optimize_wp_queries');

// Database query caching
function cache_database_queries() {
    global $wpdb;
    
    // Cache common queries
    add_filter('posts_results', function($posts, $query) {
        if ($query->is_main_query() && !is_admin()) {
            $cache_key = 'query_' . md5(serialize($query->query_vars));
            set_transient($cache_key, $posts, 300); // 5 minutes
        }
        
        return $posts;
    }, 10, 2);
    
    // Use cached results
    add_filter('posts_pre_query', function($posts, $query) {
        if ($query->is_main_query() && !is_admin()) {
            $cache_key = 'query_' . md5(serialize($query->query_vars));
            $cached_posts = get_transient($cache_key);
            
            if ($cached_posts !== false) {
                return $cached_posts;
            }
        }
        
        return $posts;
    }, 10, 2);
}

add_action('init', 'cache_database_queries');
```

### Memory Optimization

```php
// Memory optimization
function optimize_memory_usage() {
    // Increase memory limit
    ini_set('memory_limit', '256M');
    
    // Optimize WordPress memory usage
    add_action('wp_loaded', function() {
        // Clear unnecessary globals
        unset($GLOBALS['wp_filter']['wp_head']);
        unset($GLOBALS['wp_filter']['wp_footer']);
    });
    
    // Optimize database queries
    add_filter('posts_clauses', function($clauses, $query) {
        if ($query->is_main_query() && !is_admin()) {
            // Use specific fields instead of SELECT *
            $clauses['fields'] = 'ID, post_title, post_date, post_status, post_type';
        }
        
        return $clauses;
    }, 10, 2);
    
    // Limit revision count
    add_filter('wp_revisions_to_keep', function($num, $post) {
        return 3; // Keep only 3 revisions
    }, 10, 2);
}

add_action('init', 'optimize_memory_usage');

// Garbage collection
function cleanup_memory() {
    // Clear transients
    global $wpdb;
    
    $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_%' AND option_value < UNIX_TIMESTAMP()");
    $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_%' AND option_name NOT IN (SELECT option_name FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_%')");
    
    // Clear expired cache
    wp_cache_flush();
}

add_action('wp_scheduled_delete', 'cleanup_memory');
```

## Performance Monitoring

### Real-time Monitoring

```php
// Performance monitoring dashboard
function performance_monitoring_dashboard() {
    if (!current_user_can('manage_options')) {
        return;
    }
    
    add_action('wp_dashboard_setup', function() {
        wp_add_dashboard_widget(
            'performance_monitor',
            'Performance Monitor',
            'performance_monitor_widget'
        );
    });
}

function performance_monitor_widget() {
    global $wpdb;
    
    $memory_usage = memory_get_peak_usage(true);
    $memory_limit = ini_get('memory_limit');
    $query_count = count($wpdb->queries);
    $query_time = $wpdb->time_by_type['SELECT'];
    
    echo '<div class="performance-stats">';
    echo '<p><strong>Memory Usage:</strong> ' . round($memory_usage / 1024 / 1024, 2) . 'MB / ' . $memory_limit . '</p>';
    echo '<p><strong>Database Queries:</strong> ' . $query_count . '</p>';
    echo '<p><strong>Query Time:</strong> ' . round($query_time, 4) . 's</p>';
    echo '<p><strong>Page Load Time:</strong> ' . round(timer_stop(0, 3), 3) . 's</p>';
    echo '</div>';
    
    echo '<style>
    .performance-stats p {
        margin: 5px 0;
        padding: 5px;
        background: #f0f0f0;
        border-radius: 3px;
    }
    </style>';
}

add_action('init', 'performance_monitoring_dashboard');

// Performance logging
function log_performance_metrics() {
    if (!WP_DEBUG) {
        return;
    }
    
    add_action('wp_footer', function() {
        global $wpdb;
        
        $metrics = array(
            'memory_peak' => memory_get_peak_usage(true),
            'query_count' => count($wpdb->queries),
            'query_time' => $wpdb->time_by_type['SELECT'],
            'page_load_time' => timer_stop(0, 3),
            'template' => get_template(),
            'plugins' => count(get_option('active_plugins', array()))
        );
        
        error_log('Performance Metrics: ' . json_encode($metrics));
    });
}

add_action('init', 'log_performance_metrics');
```

## Best Practices Summary

### Performance Optimization Checklist

```php
// Performance optimization checklist
function performance_checklist() {
    $checklist = array(
        'Database Optimization' => array(
            'Remove unused plugins and themes',
            'Clean up database regularly',
            'Optimize database queries',
            'Use proper indexing',
            'Limit post revisions'
        ),
        'Caching' => array(
            'Implement page caching',
            'Use object caching',
            'Cache database queries',
            'Use CDN for static assets',
            'Implement fragment caching'
        ),
        'Asset Optimization' => array(
            'Minify CSS and JavaScript',
            'Combine CSS/JS files',
            'Use critical CSS',
            'Optimize images (WebP, lazy loading)',
            'Defer non-critical scripts'
        ),
        'Server Optimization' => array(
            'Use PHP 8.0+',
            'Enable OPcache',
            'Use Redis/Memcached',
            'Optimize server configuration',
            'Use HTTP/2'
        ),
        'WordPress Optimization' => array(
            'Remove unnecessary features',
            'Optimize database queries',
            'Limit admin bar for non-admins',
            'Disable XML-RPC if not needed',
            'Optimize user sessions'
        )
    );
    
    return $checklist;
}
```

## Official Documentation

https://developer.wordpress.org/advanced-administration/performance/
https://wordpress.org/support/article/optimization/
https://developer.wordpress.org/themes/advanced-topics/optimization/
