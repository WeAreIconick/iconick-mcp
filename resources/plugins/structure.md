# WordPress Plugin Structure

## Basic Plugin Structure

### Minimum Plugin File

```php
<?php
/**
 * Plugin Name: My Custom Plugin
 * Plugin URI: https://example.com/my-plugin
 * Description: Description of what the plugin does
 * Version: 1.0.0
 * Author: Your Name
 * Author URI: https://example.com
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: my-plugin
 * Domain Path: /languages
 */

// Prevent direct access
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Plugin code here
```

### Recommended File Structure

```
my-plugin/
├── my-plugin.php              # Main plugin file
├── README.md                  # Documentation
├── includes/                  # Core plugin files
│   ├── class-plugin.php      # Main plugin class
│   ├── class-admin.php       # Admin functionality
│   ├── class-public.php      # Public-facing functionality
│   └── functions.php         # Helper functions
├── admin/                     # Admin-specific files
│   ├── css/
│   ├── js/
│   └── views/                # Admin templates
├── public/                    # Public-facing files
│   ├── css/
│   ├── js/
│   └── views/                # Public templates
├── languages/                 # Translation files
├── assets/                    # Images, fonts, etc.
└── vendor/                    # Third-party libraries (if using Composer)
```

## Main Plugin File

```php
<?php
/**
 * Plugin Name: My Custom Plugin
 * Version: 1.0.0
 * Text Domain: my-plugin
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Define constants
define( 'MY_PLUGIN_VERSION', '1.0.0' );
define( 'MY_PLUGIN_PATH', plugin_dir_path( __FILE__ ) );
define( 'MY_PLUGIN_URL', plugin_dir_url( __FILE__ ) );

// Require dependencies
require_once MY_PLUGIN_PATH . 'includes/class-plugin.php';

// Initialize plugin
function my_plugin_init() {
    $plugin = new My_Plugin();
    $plugin->run();
}
add_action( 'plugins_loaded', 'my_plugin_init' );

// Activation hook
register_activation_hook( __FILE__, 'my_plugin_activate' );

function my_plugin_activate() {
    // Setup database, options, etc.
    flush_rewrite_rules();
}

// Deactivation hook
register_deactivation_hook( __FILE__, 'my_plugin_deactivate' );

function my_plugin_deactivate() {
    flush_rewrite_rules();
}
```

## Main Plugin Class

```php
<?php
// includes/class-plugin.php

class My_Plugin {
    
    private $version = '1.0.0';
    
    public function __construct() {
        $this->load_dependencies();
        $this->define_hooks();
    }
    
    private function load_dependencies() {
        require_once MY_PLUGIN_PATH . 'includes/class-admin.php';
        require_once MY_PLUGIN_PATH . 'includes/class-public.php';
    }
    
    private function define_hooks() {
        // Admin hooks
        if ( is_admin() ) {
            $admin = new My_Plugin_Admin();
            add_action( 'admin_menu', array( $admin, 'add_menu' ) );
            add_action( 'admin_enqueue_scripts', array( $admin, 'enqueue_scripts' ) );
        }
        
        // Public hooks
        $public = new My_Plugin_Public();
        add_action( 'wp_enqueue_scripts', array( $public, 'enqueue_scripts' ) );
        add_action( 'init', array( $public, 'register_shortcodes' ) );
    }
    
    public function run() {
        // Additional initialization
    }
}
```

## Admin Class

```php
<?php
// includes/class-admin.php

class My_Plugin_Admin {
    
    public function add_menu() {
        add_menu_page(
            'My Plugin',
            'My Plugin',
            'manage_options',
            'my-plugin',
            array( $this, 'render_admin_page' ),
            'dashicons-admin-generic'
        );
    }
    
    public function render_admin_page() {
        if ( ! current_user_can( 'manage_options' ) ) {
            return;
        }
        
        include MY_PLUGIN_PATH . 'admin/views/settings.php';
    }
    
    public function enqueue_scripts( $hook ) {
        if ( 'toplevel_page_my-plugin' !== $hook ) {
            return;
        }
        
        wp_enqueue_style(
            'my-plugin-admin',
            MY_PLUGIN_URL . 'admin/css/admin.css',
            array(),
            MY_PLUGIN_VERSION
        );
        
        wp_enqueue_script(
            'my-plugin-admin',
            MY_PLUGIN_URL . 'admin/js/admin.js',
            array( 'jquery' ),
            MY_PLUGIN_VERSION,
            true
        );
    }
}
```

## Public Class

```php
<?php
// includes/class-public.php

class My_Plugin_Public {
    
    public function enqueue_scripts() {
        wp_enqueue_style(
            'my-plugin',
            MY_PLUGIN_URL . 'public/css/style.css',
            array(),
            MY_PLUGIN_VERSION
        );
        
        wp_enqueue_script(
            'my-plugin',
            MY_PLUGIN_URL . 'public/js/script.js',
            array( 'jquery' ),
            MY_PLUGIN_VERSION,
            true
        );
        
        wp_localize_script( 'my-plugin', 'myPluginData', array(
            'ajaxurl' => admin_url( 'admin-ajax.php' ),
            'nonce'   => wp_create_nonce( 'my_plugin_nonce' ),
        ) );
    }
    
    public function register_shortcodes() {
        add_shortcode( 'my_shortcode', array( $this, 'render_shortcode' ) );
    }
    
    public function render_shortcode( $atts ) {
        $atts = shortcode_atts( array(
            'title' => 'Default Title',
            'content' => '',
        ), $atts );
        
        ob_start();
        include MY_PLUGIN_PATH . 'public/views/shortcode.php';
        return ob_get_clean();
    }
}
```

## Uninstall

```php
<?php
// uninstall.php

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

// Delete options
delete_option( 'my_plugin_options' );

// Delete post meta
delete_post_meta_by_key( 'my_plugin_meta' );

// Drop custom tables
global $wpdb;
$wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}my_plugin_table" );

// Clear any caches
wp_cache_flush();
```

## Best Practices

1. **Prefix everything** - Use unique prefix for functions, classes, constants
2. **Use classes** - Organize code in classes for better structure
3. **Separate admin and public** - Keep admin and frontend code separate
4. **Security first** - Nonces, capability checks, sanitization, escaping
5. **Enqueue properly** - Use wp_enqueue_scripts, not hardcoded scripts
6. **Use WordPress APIs** - Don't reinvent the wheel
7. **Internationalization** - Make strings translatable
8. **Clean uninstall** - Remove all plugin data on uninstall

## Official Documentation

https://developer.wordpress.org/plugins/plugin-basics/
https://developer.wordpress.org/plugins/plugin-basics/best-practices/
