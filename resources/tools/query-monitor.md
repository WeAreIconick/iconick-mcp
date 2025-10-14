# Query Monitor Plugin

Query Monitor is the most comprehensive debugging plugin for WordPress, providing detailed information about database queries, hooks, scripts, and performance.

## Installation and Setup

### Basic Installation

```php
// Install via WP-CLI
wp plugin install query-monitor --activate

// Or download from WordPress.org
// https://wordpress.org/plugins/query-monitor/
```

### Configuration

```php
// wp-config.php - Query Monitor configuration
// Enable Query Monitor in production (optional)
define( 'QM_ENABLE', true );

// Hide Query Monitor for non-administrators
define( 'QM_HIDE_CORE_UPDATE_NOTIFICATIONS', true );

// Enable Query Monitor for AJAX requests
define( 'QM_COOKIE', 'query_monitor' );

// Custom Query Monitor settings
if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
    define( 'QM_ENABLE', true );
} else {
    define( 'QM_ENABLE', false );
}
```

## Database Query Analysis

### Understanding Query Output

Query Monitor displays database queries with:
- **Query text** - The actual SQL query
- **Time** - How long the query took to execute
- **Component** - Which plugin/theme/core generated the query
- **Caller** - The function that made the query
- **Stack trace** - Complete call stack

### Identifying Slow Queries

```php
// Look for queries with high execution time
// Red highlighting indicates slow queries (>0.05s)
// Yellow highlighting indicates moderate queries (>0.01s)

// Common slow query patterns:
// 1. Queries without LIMIT
// 2. Queries with ORDER BY on non-indexed columns
// 3. Queries with complex JOINs
// 4. Queries with LIKE patterns starting with wildcards
```

### Query Optimization Examples

```php
// Before: Slow query
$posts = get_posts( array(
    'post_type' => 'product',
    'meta_key' => 'featured',
    'meta_value' => '1',
    'orderby' => 'rand'
) );

// After: Optimized query
$posts = get_posts( array(
    'post_type' => 'product',
    'meta_key' => 'featured',
    'meta_value' => '1',
    'orderby' => 'menu_order',
    'posts_per_page' => 10
) );
```

## Hook Analysis

### Understanding Hooks Panel

Query Monitor shows:
- **Actions** - Functions attached to action hooks
- **Filters** - Functions attached to filter hooks
- **Execution order** - When hooks are fired
- **Parameters** - What data is passed to hooks

### Hook Performance Analysis

```php
// Example: Analyzing expensive hooks
add_action( 'wp_head', 'expensive_function' );

function expensive_function() {
    // This will show up in Query Monitor's Hooks panel
    // Check execution time and frequency
    $data = get_transient( 'expensive_data' );
    
    if ( false === $data ) {
        $data = expensive_calculation();
        set_transient( 'expensive_data', $data, HOUR_IN_SECONDS );
    }
    
    return $data;
}
```

### Hook Debugging

```php
// Add debug information to hooks
add_action( 'init', 'debug_init_hook' );

function debug_init_hook() {
    // This will appear in Query Monitor's Hooks panel
    if ( WP_DEBUG ) {
        error_log( 'Init hook fired at: ' . current_time( 'mysql' ) );
    }
}
```

## Script and Style Analysis

### Asset Loading Analysis

Query Monitor shows:
- **Scripts** - JavaScript files loaded
- **Styles** - CSS files loaded
- **Dependencies** - What depends on what
- **Loading order** - When assets are loaded

### Optimizing Asset Loading

```php
// Before: Loading unnecessary assets
function enqueue_all_assets() {
    wp_enqueue_script( 'jquery' );
    wp_enqueue_script( 'my-script' );
    wp_enqueue_style( 'my-style' );
}
add_action( 'wp_enqueue_scripts', 'enqueue_all_assets' );

// After: Conditional loading
function enqueue_conditional_assets() {
    // Only load on specific pages
    if ( is_page( 'contact' ) ) {
        wp_enqueue_script( 'contact-form' );
    }
    
    // Only load for logged-in users
    if ( is_user_logged_in() ) {
        wp_enqueue_style( 'admin-bar' );
    }
}
add_action( 'wp_enqueue_scripts', 'enqueue_conditional_assets' );
```

## Performance Analysis

### Understanding Performance Metrics

Query Monitor provides:
- **Page load time** - Total time to load the page
- **Database query time** - Time spent on database operations
- **PHP execution time** - Time spent executing PHP code
- **Memory usage** - Peak memory consumption

### Performance Optimization

```php
// Example: Optimizing database queries
function get_featured_products() {
    // Use transients to cache expensive queries
    $cache_key = 'featured_products';
    $products = get_transient( $cache_key );
    
    if ( false === $products ) {
        // This query will show up in Query Monitor
        $products = get_posts( array(
            'post_type' => 'product',
            'meta_key' => 'featured',
            'meta_value' => '1',
            'posts_per_page' => 10
        ) );
        
        // Cache for 1 hour
        set_transient( $cache_key, $products, HOUR_IN_SECONDS );
    }
    
    return $products;
}
```

## AJAX Request Debugging

### AJAX Performance Analysis

```php
// AJAX handler that will be tracked by Query Monitor
function handle_ajax_request() {
    // Check nonce for security
    if ( ! wp_verify_nonce( $_POST['nonce'], 'ajax_action' ) ) {
        wp_die( 'Security check failed' );
    }
    
    // This AJAX request will appear in Query Monitor
    $data = process_ajax_data();
    
    wp_send_json_success( $data );
}
add_action( 'wp_ajax_my_action', 'handle_ajax_request' );
add_action( 'wp_ajax_nopriv_my_action', 'handle_ajax_request' );
```

### AJAX Error Debugging

```php
// AJAX handler with error logging
function handle_ajax_with_debug() {
    try {
        // AJAX processing logic
        $result = perform_ajax_operation();
        
        wp_send_json_success( $result );
        
    } catch ( Exception $e ) {
        // Log error for debugging
        error_log( 'AJAX Error: ' . $e->getMessage() );
        
        // Send error response
        wp_send_json_error( array(
            'message' => 'An error occurred',
            'debug' => WP_DEBUG ? $e->getMessage() : null
        ) );
    }
}
```

## Custom Query Monitor Extensions

### Adding Custom Collectors

```php
// Custom Query Monitor collector
class My_Custom_Collector extends QM_Collector {
    
    public $id = 'my-custom';
    
    public function name() {
        return __( 'My Custom Data' );
    }
    
    public function process() {
        $this->data['custom_data'] = array(
            'timestamp' => current_time( 'mysql' ),
            'memory_usage' => memory_get_usage( true ),
            'custom_metric' => get_option( 'my_custom_metric' )
        );
    }
}

// Register the collector
add_filter( 'qm/collectors', function( array $collectors ) {
    $collectors['my-custom'] = new My_Custom_Collector();
    return $collectors;
});
```

### Custom Query Monitor Panel

```php
// Custom Query Monitor panel
class My_Custom_Panel extends QM_Output_Html {
    
    public function __construct( QM_Collector $collector ) {
        parent::__construct( $collector );
    }
    
    public function name() {
        return __( 'My Custom Panel' );
    }
    
    public function output() {
        $data = $this->collector->get_data();
        
        echo '<div class="qm-section">';
        echo '<h3>Custom Data</h3>';
        echo '<table>';
        echo '<tr><td>Timestamp:</td><td>' . esc_html( $data['custom_data']['timestamp'] ) . '</td></tr>';
        echo '<tr><td>Memory Usage:</td><td>' . esc_html( size_format( $data['custom_data']['memory_usage'] ) ) . '</td></tr>';
        echo '</table>';
        echo '</div>';
    }
}

// Register the panel
add_filter( 'qm/outputter/html', function( array $output ) {
    $collector = QM_Collectors::get( 'my-custom' );
    if ( $collector ) {
        $output['my-custom'] = new My_Custom_Panel( $collector );
    }
    return $output;
});
```

## Common Query Monitor Use Cases

### Plugin Development

```php
// Debug plugin performance
class My_Plugin {
    
    public function __construct() {
        add_action( 'init', array( $this, 'init' ) );
    }
    
    public function init() {
        // This will show up in Query Monitor
        $this->load_dependencies();
        $this->register_hooks();
    }
    
    private function load_dependencies() {
        // Track which files are loaded
        if ( WP_DEBUG ) {
            error_log( 'Loading plugin dependencies' );
        }
    }
    
    private function register_hooks() {
        // Track hook registration
        add_action( 'wp_enqueue_scripts', array( $this, 'enqueue_scripts' ) );
    }
}
```

### Theme Development

```php
// Debug theme performance
function my_theme_debug() {
    if ( ! WP_DEBUG ) {
        return;
    }
    
    // Track template loading
    add_filter( 'template_include', function( $template ) {
        error_log( 'Loading template: ' . $template );
        return $template;
    });
    
    // Track query modifications
    add_action( 'pre_get_posts', function( $query ) {
        if ( ! is_admin() && $query->is_main_query() ) {
            error_log( 'Main query modified' );
        }
    });
}
add_action( 'after_setup_theme', 'my_theme_debug' );
```

## Best Practices

### Production Considerations

```php
// wp-config.php - Production Query Monitor settings
if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
    // Only enable in development
    define( 'QM_ENABLE', true );
} else {
    // Disable in production for performance
    define( 'QM_ENABLE', false );
}
```

### Security Considerations

```php
// Restrict Query Monitor access
add_filter( 'qm/collect/user_capability', function( $capability ) {
    // Only allow administrators to see Query Monitor
    return 'manage_options';
});
```

### Performance Impact

```php
// Minimize Query Monitor overhead
add_filter( 'qm/collect/db_queries', '__return_false' ); // Disable query collection
add_filter( 'qm/collect/hooks', '__return_false' ); // Disable hook collection
add_filter( 'qm/collect/assets', '__return_false' ); // Disable asset collection
```

## Official Documentation

https://querymonitor.com/
https://github.com/johnbillion/query-monitor
https://wordpress.org/plugins/query-monitor/
