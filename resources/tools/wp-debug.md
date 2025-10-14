# WordPress Debug System

The WordPress debug system helps developers identify and fix issues during development.

## Debug Constants

### Basic Debug Configuration

```php
// wp-config.php
// Enable debugging
define( 'WP_DEBUG', true );

// Log errors to file
define( 'WP_DEBUG_LOG', true );

// Display errors on screen (development only)
define( 'WP_DEBUG_DISPLAY', true );

// Use unminified scripts and styles
define( 'SCRIPT_DEBUG', true );

// Save database queries for analysis
define( 'SAVEQUERIES', true );
```

### Production-Safe Debug Configuration

```php
// wp-config.php - Production configuration
// Enable debugging
define( 'WP_DEBUG', true );

// Log errors to file
define( 'WP_DEBUG_LOG', true );

// Never display errors on screen in production
define( 'WP_DEBUG_DISPLAY', false );

// Hide errors from visitors
@ini_set( 'display_errors', 0 );

// Use minified scripts in production
define( 'SCRIPT_DEBUG', false );

// Don't save queries in production
define( 'SAVEQUERIES', false );
```

### Advanced Debug Configuration

```php
// wp-config.php - Advanced debugging
// Enable debugging
define( 'WP_DEBUG', true );

// Log errors to file
define( 'WP_DEBUG_LOG', true );

// Display errors only for administrators
define( 'WP_DEBUG_DISPLAY', current_user_can( 'manage_options' ) );

// Use unminified scripts
define( 'SCRIPT_DEBUG', true );

// Save database queries
define( 'SAVEQUERIES', true );

// Log database errors
define( 'DIEONDBERROR', true );

// Enable multisite debugging
define( 'WP_DEBUG_LOG', true );
define( 'MULTISITE_DEBUG_LOG', true );
```

## Debug Log Management

### Reading Debug Logs

```php
// functions.php - Debug log viewer for admins
function display_debug_log() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    
    $debug_log = WP_CONTENT_DIR . '/debug.log';
    
    if ( ! file_exists( $debug_log ) ) {
        echo '<p>No debug log found.</p>';
        return;
    }
    
    $log_content = file_get_contents( $debug_log );
    $log_lines = explode( "\n", $log_content );
    
    // Show last 100 lines
    $recent_lines = array_slice( $log_lines, -100 );
    
    echo '<div style="background: #f1f1f1; padding: 10px; font-family: monospace; white-space: pre-wrap;">';
    echo htmlspecialchars( implode( "\n", $recent_lines ) );
    echo '</div>';
}

// Add debug log viewer to admin menu
function add_debug_log_menu() {
    add_management_page(
        'Debug Log',
        'Debug Log',
        'manage_options',
        'debug-log',
        'display_debug_log'
    );
}
add_action( 'admin_menu', 'add_debug_log_menu' );
```

### Log Rotation and Cleanup

```php
// functions.php - Automatic log rotation
function rotate_debug_log() {
    $debug_log = WP_CONTENT_DIR . '/debug.log';
    
    if ( ! file_exists( $debug_log ) ) {
        return;
    }
    
    // Check if log is larger than 10MB
    if ( filesize( $debug_log ) > 10 * 1024 * 1024 ) {
        // Create backup
        $backup_log = WP_CONTENT_DIR . '/debug-' . date( 'Y-m-d-H-i-s' ) . '.log';
        copy( $debug_log, $backup_log );
        
        // Clear current log
        file_put_contents( $debug_log, '' );
        
        // Log the rotation
        error_log( 'Debug log rotated. Backup created: ' . basename( $backup_log ) );
    }
}

// Run log rotation on admin_init
add_action( 'admin_init', 'rotate_debug_log' );
```

### Custom Debug Functions

```php
// functions.php - Custom debug functions
function debug_log( $message, $context = null ) {
    if ( ! WP_DEBUG_LOG ) {
        return;
    }
    
    $timestamp = current_time( 'Y-m-d H:i:s' );
    $context_info = $context ? ' [' . $context . ']' : '';
    $log_message = "[{$timestamp}]{$context_info} {$message}" . PHP_EOL;
    
    error_log( $log_message );
}

function debug_dump( $variable, $label = null ) {
    if ( ! WP_DEBUG_LOG ) {
        return;
    }
    
    $label = $label ? $label . ': ' : '';
    debug_log( $label . print_r( $variable, true ) );
}

function debug_trace( $message = 'Debug trace' ) {
    if ( ! WP_DEBUG_LOG ) {
        return;
    }
    
    $trace = debug_backtrace( DEBUG_BACKTRACE_IGNORE_ARGS, 10 );
    debug_log( $message . ' - Trace:', $trace );
}

// Usage examples
debug_log( 'Plugin activated successfully', 'my-plugin' );
debug_dump( $_POST, 'POST data' );
debug_trace( 'Function called' );
```

## Error Handling

### Custom Error Handler

```php
// functions.php - Custom error handler
function custom_error_handler( $errno, $errstr, $errfile, $errline ) {
    // Don't log if error reporting is turned off
    if ( ! ( error_reporting() & $errno ) ) {
        return false;
    }
    
    $error_types = array(
        E_ERROR => 'Fatal Error',
        E_WARNING => 'Warning',
        E_PARSE => 'Parse Error',
        E_NOTICE => 'Notice',
        E_CORE_ERROR => 'Core Error',
        E_CORE_WARNING => 'Core Warning',
        E_COMPILE_ERROR => 'Compile Error',
        E_COMPILE_WARNING => 'Compile Warning',
        E_USER_ERROR => 'User Error',
        E_USER_WARNING => 'User Warning',
        E_USER_NOTICE => 'User Notice',
        E_STRICT => 'Strict Notice',
        E_RECOVERABLE_ERROR => 'Recoverable Error',
        E_DEPRECATED => 'Deprecated',
        E_USER_DEPRECATED => 'User Deprecated'
    );
    
    $error_type = isset( $error_types[ $errno ] ) ? $error_types[ $errno ] : 'Unknown Error';
    
    $error_message = sprintf(
        '[%s] %s: %s in %s on line %d',
        $error_type,
        $errno,
        $errstr,
        $errfile,
        $errline
    );
    
    error_log( $error_message );
    
    // Don't execute PHP internal error handler
    return true;
}

// Set custom error handler
set_error_handler( 'custom_error_handler' );
```

### Exception Handling

```php
// functions.php - Exception handling
function custom_exception_handler( $exception ) {
    $error_message = sprintf(
        'Uncaught Exception: %s in %s on line %d',
        $exception->getMessage(),
        $exception->getFile(),
        $exception->getLine()
    );
    
    error_log( $error_message );
    
    // In development, show error
    if ( WP_DEBUG && WP_DEBUG_DISPLAY ) {
        echo '<div class="error"><p>' . esc_html( $error_message ) . '</p></div>';
    }
}

// Set custom exception handler
set_exception_handler( 'custom_exception_handler' );
```

## Database Query Debugging

### Query Monitoring

```php
// functions.php - Database query debugging
function debug_database_queries() {
    if ( ! WP_DEBUG || ! SAVEQUERIES ) {
        return;
    }
    
    global $wpdb;
    
    if ( ! empty( $wpdb->queries ) ) {
        echo '<div id="query-debug" style="background: #f1f1f1; padding: 10px; margin: 10px 0;">';
        echo '<h3>Database Queries (' . count( $wpdb->queries ) . ')</h3>';
        
        foreach ( $wpdb->queries as $i => $query ) {
            $time = round( $query[1], 6 );
            $backtrace = $query[2];
            
            echo '<div style="margin-bottom: 10px; padding: 5px; border: 1px solid #ccc;">';
            echo '<strong>Query ' . ( $i + 1 ) . ':</strong> ' . esc_html( $query[0] ) . '<br>';
            echo '<strong>Time:</strong> ' . $time . ' seconds<br>';
            echo '<strong>Backtrace:</strong> ' . esc_html( $backtrace );
            echo '</div>';
        }
        
        echo '</div>';
    }
}

// Add query debug to footer for admins
function add_query_debug_to_footer() {
    if ( current_user_can( 'manage_options' ) ) {
        debug_database_queries();
    }
}
add_action( 'wp_footer', 'add_query_debug_to_footer' );
add_action( 'admin_footer', 'add_query_debug_to_footer' );
```

### Slow Query Detection

```php
// functions.php - Slow query detection
function detect_slow_queries() {
    if ( ! WP_DEBUG || ! SAVEQUERIES ) {
        return;
    }
    
    global $wpdb;
    
    foreach ( $wpdb->queries as $query ) {
        $time = $query[1];
        
        // Flag queries taking longer than 1 second
        if ( $time > 1.0 ) {
            $slow_query_message = sprintf(
                'Slow query detected: %s (Time: %s seconds)',
                $query[0],
                $time
            );
            
            error_log( $slow_query_message );
        }
    }
}

// Check for slow queries on shutdown
add_action( 'shutdown', 'detect_slow_queries' );
```

## Plugin and Theme Debugging

### Plugin Debug Information

```php
// functions.php - Plugin debugging
function debug_plugin_info() {
    if ( ! WP_DEBUG || ! current_user_can( 'manage_options' ) ) {
        return;
    }
    
    $active_plugins = get_option( 'active_plugins' );
    
    echo '<div id="plugin-debug" style="background: #f1f1f1; padding: 10px; margin: 10px 0;">';
    echo '<h3>Active Plugins Debug Info</h3>';
    
    foreach ( $active_plugins as $plugin ) {
        $plugin_data = get_plugin_data( WP_PLUGIN_DIR . '/' . $plugin );
        
        echo '<div style="margin-bottom: 10px; padding: 5px; border: 1px solid #ccc;">';
        echo '<strong>Plugin:</strong> ' . esc_html( $plugin_data['Name'] ) . '<br>';
        echo '<strong>Version:</strong> ' . esc_html( $plugin_data['Version'] ) . '<br>';
        echo '<strong>File:</strong> ' . esc_html( $plugin );
        echo '</div>';
    }
    
    echo '</div>';
}

// Add plugin debug to admin footer
add_action( 'admin_footer', 'debug_plugin_info' );
```

### Theme Debug Information

```php
// functions.php - Theme debugging
function debug_theme_info() {
    if ( ! WP_DEBUG || ! current_user_can( 'manage_options' ) ) {
        return;
    }
    
    $theme = wp_get_theme();
    
    echo '<div id="theme-debug" style="background: #f1f1f1; padding: 10px; margin: 10px 0;">';
    echo '<h3>Theme Debug Info</h3>';
    echo '<strong>Name:</strong> ' . esc_html( $theme->get( 'Name' ) ) . '<br>';
    echo '<strong>Version:</strong> ' . esc_html( $theme->get( 'Version' ) ) . '<br>';
    echo '<strong>Author:</strong> ' . esc_html( $theme->get( 'Author' ) ) . '<br>';
    echo '<strong>Template:</strong> ' . esc_html( get_template() ) . '<br>';
    echo '<strong>Stylesheet:</strong> ' . esc_html( get_stylesheet() ) . '<br>';
    echo '<strong>Child Theme:</strong> ' . ( is_child_theme() ? 'Yes' : 'No' ) . '<br>';
    echo '</div>';
}

// Add theme debug to admin footer
add_action( 'admin_footer', 'debug_theme_info' );
```

## Performance Debugging

### Memory Usage Monitoring

```php
// functions.php - Memory usage debugging
function debug_memory_usage() {
    if ( ! WP_DEBUG || ! current_user_can( 'manage_options' ) ) {
        return;
    }
    
    $memory_usage = memory_get_usage( true );
    $memory_peak = memory_get_peak_usage( true );
    $memory_limit = ini_get( 'memory_limit' );
    
    echo '<div id="memory-debug" style="background: #f1f1f1; padding: 10px; margin: 10px 0;">';
    echo '<h3>Memory Usage Debug</h3>';
    echo '<strong>Current Usage:</strong> ' . size_format( $memory_usage ) . '<br>';
    echo '<strong>Peak Usage:</strong> ' . size_format( $memory_peak ) . '<br>';
    echo '<strong>Memory Limit:</strong> ' . esc_html( $memory_limit ) . '<br>';
    echo '<strong>Usage Percentage:</strong> ' . round( ( $memory_usage / wp_convert_hr_to_bytes( $memory_limit ) ) * 100, 2 ) . '%';
    echo '</div>';
}

// Add memory debug to admin footer
add_action( 'admin_footer', 'debug_memory_usage' );
```

### Load Time Monitoring

```php
// functions.php - Load time debugging
function debug_load_time() {
    if ( ! WP_DEBUG || ! current_user_can( 'manage_options' ) ) {
        return;
    }
    
    $load_time = timer_stop( 0, 3 );
    
    echo '<div id="load-time-debug" style="background: #f1f1f1; padding: 10px; margin: 10px 0;">';
    echo '<h3>Load Time Debug</h3>';
    echo '<strong>Page Load Time:</strong> ' . $load_time . ' seconds';
    echo '</div>';
}

// Add load time debug to footer
add_action( 'wp_footer', 'debug_load_time' );
add_action( 'admin_footer', 'debug_load_time' );
```

## Best Practices

### Production Debug Settings

```php
// wp-config.php - Production debug configuration
if ( defined( 'WP_ENV' ) && WP_ENV === 'production' ) {
    // Minimal debugging in production
    define( 'WP_DEBUG', false );
    define( 'WP_DEBUG_LOG', false );
    define( 'WP_DEBUG_DISPLAY', false );
    define( 'SCRIPT_DEBUG', false );
    define( 'SAVEQUERIES', false );
} else {
    // Full debugging in development
    define( 'WP_DEBUG', true );
    define( 'WP_DEBUG_LOG', true );
    define( 'WP_DEBUG_DISPLAY', true );
    define( 'SCRIPT_DEBUG', true );
    define( 'SAVEQUERIES', true );
}
```

### Environment-Specific Configuration

```php
// wp-config.php - Environment-specific debugging
switch ( $_SERVER['HTTP_HOST'] ) {
    case 'localhost':
    case 'dev.example.com':
        // Development environment
        define( 'WP_DEBUG', true );
        define( 'WP_DEBUG_LOG', true );
        define( 'WP_DEBUG_DISPLAY', true );
        define( 'SCRIPT_DEBUG', true );
        define( 'SAVEQUERIES', true );
        break;
        
    case 'staging.example.com':
        // Staging environment
        define( 'WP_DEBUG', true );
        define( 'WP_DEBUG_LOG', true );
        define( 'WP_DEBUG_DISPLAY', false );
        define( 'SCRIPT_DEBUG', false );
        define( 'SAVEQUERIES', true );
        break;
        
    case 'example.com':
        // Production environment
        define( 'WP_DEBUG', false );
        define( 'WP_DEBUG_LOG', false );
        define( 'WP_DEBUG_DISPLAY', false );
        define( 'SCRIPT_DEBUG', false );
        define( 'SAVEQUERIES', false );
        break;
}
```

## Official Documentation

https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/
https://wordpress.org/support/article/debugging-in-wordpress/
https://developer.wordpress.org/themes/getting-started/setting-up-a-development-environment/
