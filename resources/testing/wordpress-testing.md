# WordPress Testing

Comprehensive guide to testing WordPress plugins, themes, and applications with modern testing practices.

## WordPress Testing Fundamentals

### WordPress Test Environment Setup

```php
// tests/bootstrap.php - WordPress test environment setup
<?php
/**
 * PHPUnit bootstrap file for WordPress testing
 */

// Load WordPress test environment
$_tests_dir = getenv('WP_TESTS_DIR');

if (!$_tests_dir) {
    $_tests_dir = rtrim(sys_get_temp_dir(), '/\\') . '/wordpress-tests-lib';
}

if (!file_exists($_tests_dir . '/includes/functions.php')) {
    echo "Could not find $_tests_dir/includes/functions.php, have you run bin/install-wp-tests.sh ?" . PHP_EOL;
    exit(1);
}

// Give access to tests_add_filter() function
require_once $_tests_dir . '/includes/functions.php';

/**
 * Manually load the plugin being tested
 */
function _manually_load_plugin() {
    require dirname(dirname(__FILE__)) . '/your-plugin.php';
}
tests_add_filter('muplugins_loaded', '_manually_load_plugin');

// Start up the WP testing environment
require $_tests_dir . '/includes/bootstrap.php';
```

### Basic WordPress Test Class

```php
// tests/test-basic.php
<?php
/**
 * Basic WordPress functionality tests
 */

class Basic_Test extends WP_UnitTestCase {

    /**
     * Test that WordPress is loaded correctly
     */
    public function test_wordpress_loaded() {
        $this->assertTrue(function_exists('wp_head'), 'WordPress should be loaded');
        $this->assertTrue(function_exists('get_option'), 'WordPress functions should be available');
    }

    /**
     * Test database connection
     */
    public function test_database_connection() {
        global $wpdb;
        $this->assertNotNull($wpdb, 'Database connection should be established');
        
        $result = $wpdb->get_var("SELECT 1");
        $this->assertEquals(1, $result, 'Database should respond to queries');
    }

    /**
     * Test WordPress options
     */
    public function test_wordpress_options() {
        $blogname = get_option('blogname');
        $this->assertNotEmpty($blogname, 'Blog name should be set');
        
        $admin_email = get_option('admin_email');
        $this->assertContains('@', $admin_email, 'Admin email should be valid');
    }

    /**
     * Test post creation
     */
    public function test_post_creation() {
        $post_data = array(
            'post_title' => 'Test Post',
            'post_content' => 'This is a test post content',
            'post_status' => 'publish',
            'post_type' => 'post'
        );
        
        $post_id = wp_insert_post($post_data);
        $this->assertGreaterThan(0, $post_id, 'Post should be created successfully');
        
        $post = get_post($post_id);
        $this->assertEquals('Test Post', $post->post_title, 'Post title should match');
        $this->assertEquals('publish', $post->post_status, 'Post status should be publish');
    }
}
```

## Plugin Testing

### Plugin Functionality Tests

```php
// tests/test-plugin.php
<?php
/**
 * Plugin functionality tests
 */

class Plugin_Test extends WP_UnitTestCase {

    protected $plugin;

    public function setUp() {
        parent::setUp();
        $this->plugin = new Your_Plugin();
    }

    public function tearDown() {
        parent::tearDown();
    }

    /**
     * Test plugin activation
     */
    public function test_plugin_activation() {
        $this->assertTrue(class_exists('Your_Plugin'), 'Plugin class should exist');
        $this->assertTrue(method_exists($this->plugin, 'activate'), 'Plugin should have activate method');
    }

    /**
     * Test plugin initialization
     */
    public function test_plugin_initialization() {
        $this->plugin->init();
        
        // Test that hooks are registered
        $this->assertGreaterThan(0, has_action('init', array($this->plugin, 'init')), 'Init hook should be registered');
        $this->assertGreaterThan(0, has_action('wp_enqueue_scripts', array($this->plugin, 'enqueue_scripts')), 'Scripts hook should be registered');
    }

    /**
     * Test plugin options
     */
    public function test_plugin_options() {
        $default_options = $this->plugin->get_default_options();
        
        $this->assertIsArray($default_options, 'Default options should be an array');
        $this->assertArrayHasKey('option1', $default_options, 'Default options should contain option1');
        
        // Test option saving
        $this->plugin->save_option('test_option', 'test_value');
        $saved_value = get_option('your_plugin_test_option');
        $this->assertEquals('test_value', $saved_value, 'Option should be saved correctly');
    }

    /**
     * Test plugin database operations
     */
    public function test_plugin_database_operations() {
        global $wpdb;
        
        // Test table creation
        $this->plugin->create_tables();
        
        $table_name = $wpdb->prefix . 'your_plugin_data';
        $table_exists = $wpdb->get_var("SHOW TABLES LIKE '$table_name'");
        $this->assertEquals($table_name, $table_exists, 'Plugin table should be created');
        
        // Test data insertion
        $data = array(
            'name' => 'Test Data',
            'value' => 'Test Value',
            'created_at' => current_time('mysql')
        );
        
        $result = $wpdb->insert($table_name, $data);
        $this->assertNotFalse($result, 'Data should be inserted successfully');
        
        $inserted_id = $wpdb->insert_id;
        $this->assertGreaterThan(0, $inserted_id, 'Insert ID should be returned');
    }
}
```

### Plugin API Tests

```php
// tests/test-plugin-api.php
<?php
/**
 * Plugin API tests
 */

class Plugin_API_Test extends WP_UnitTestCase {

    public function setUp() {
        parent::setUp();
        $this->plugin = new Your_Plugin();
    }

    /**
     * Test REST API endpoints
     */
    public function test_rest_api_endpoints() {
        // Register REST API routes
        $this->plugin->register_rest_routes();
        
        // Test endpoint registration
        $routes = rest_get_server()->get_routes();
        $this->assertArrayHasKey('/your-plugin/v1/data', $routes, 'REST endpoint should be registered');
        
        // Test GET request
        $request = new WP_REST_Request('GET', '/your-plugin/v1/data');
        $response = rest_get_server()->dispatch($request);
        
        $this->assertEquals(200, $response->get_status(), 'GET request should return 200');
        
        $data = $response->get_data();
        $this->assertIsArray($data, 'Response data should be an array');
    }

    /**
     * Test AJAX endpoints
     */
    public function test_ajax_endpoints() {
        // Test AJAX action registration
        $this->assertGreaterThan(0, has_action('wp_ajax_your_plugin_action', array($this->plugin, 'handle_ajax')), 'AJAX action should be registered');
        
        // Simulate AJAX request
        $_POST['action'] = 'your_plugin_action';
        $_POST['data'] = 'test_data';
        $_POST['nonce'] = wp_create_nonce('your_plugin_nonce');
        
        // Capture output
        ob_start();
        $this->plugin->handle_ajax();
        $output = ob_get_clean();
        
        $response = json_decode($output, true);
        $this->assertIsArray($response, 'AJAX response should be valid JSON');
        $this->assertTrue($response['success'], 'AJAX request should be successful');
    }

    /**
     * Test shortcode functionality
     */
    public function test_shortcode_functionality() {
        // Register shortcode
        add_shortcode('your_plugin_shortcode', array($this->plugin, 'shortcode_handler'));
        
        // Test shortcode output
        $output = do_shortcode('[your_plugin_shortcode]');
        $this->assertNotEmpty($output, 'Shortcode should produce output');
        $this->assertStringContainsString('your-plugin', $output, 'Shortcode output should contain plugin identifier');
        
        // Test shortcode with attributes
        $output_with_attrs = do_shortcode('[your_plugin_shortcode attr1="value1" attr2="value2"]');
        $this->assertStringContainsString('value1', $output_with_attrs, 'Shortcode should handle attributes');
    }
}
```

## Theme Testing

### Theme Functionality Tests

```php
// tests/test-theme.php
<?php
/**
 * Theme functionality tests
 */

class Theme_Test extends WP_UnitTestCase {

    protected $theme;

    public function setUp() {
        parent::setUp();
        $this->theme = wp_get_theme();
    }

    /**
     * Test theme setup
     */
    public function test_theme_setup() {
        $this->assertTrue(current_theme_supports('post-thumbnails'), 'Theme should support post thumbnails');
        $this->assertTrue(current_theme_supports('html5'), 'Theme should support HTML5');
        $this->assertTrue(current_theme_supports('title-tag'), 'Theme should support title tag');
    }

    /**
     * Test theme functions
     */
    public function test_theme_functions() {
        $this->assertTrue(function_exists('your_theme_name_setup'), 'Theme setup function should exist');
        $this->assertTrue(function_exists('your_theme_name_scripts'), 'Theme scripts function should exist');
        $this->assertTrue(function_exists('your_theme_name_widgets_init'), 'Theme widgets function should exist');
    }

    /**
     * Test theme menus
     */
    public function test_theme_menus() {
        $menus = get_registered_nav_menus();
        $this->assertArrayHasKey('primary', $menus, 'Primary menu should be registered');
        
        // Test menu creation
        $menu_id = wp_create_nav_menu('Test Menu');
        $this->assertGreaterThan(0, $menu_id, 'Menu should be created successfully');
        
        // Test menu item addition
        $menu_item_id = wp_update_nav_menu_item($menu_id, 0, array(
            'menu-item-title' => 'Test Page',
            'menu-item-url' => home_url('/test-page/'),
            'menu-item-status' => 'publish'
        ));
        
        $this->assertGreaterThan(0, $menu_item_id, 'Menu item should be added successfully');
    }

    /**
     * Test theme widgets
     */
    public function test_theme_widgets() {
        $sidebars = $GLOBALS['wp_registered_sidebars'];
        $this->assertArrayHasKey('sidebar-1', $sidebars, 'Main sidebar should be registered');
        
        // Test widget registration
        $widgets = $GLOBALS['wp_registered_widgets'];
        $this->assertNotEmpty($widgets, 'Widgets should be registered');
    }

    /**
     * Test theme templates
     */
    public function test_theme_templates() {
        $template_hierarchy = array(
            'index.php',
            'home.php',
            'single.php',
            'page.php',
            'archive.php',
            'search.php',
            '404.php'
        );
        
        foreach ($template_hierarchy as $template) {
            $template_path = locate_template($template);
            $this->assertNotEmpty($template_path, "Template $template should exist");
        }
    }
}
```

### Theme Customizer Tests

```php
// tests/test-theme-customizer.php
<?php
/**
 * Theme customizer tests
 */

class Theme_Customizer_Test extends WP_UnitTestCase {

    public function setUp() {
        parent::setUp();
        $this->customizer = new WP_Customize_Manager();
    }

    /**
     * Test customizer sections
     */
    public function test_customizer_sections() {
        $sections = $this->customizer->sections();
        
        $this->assertArrayHasKey('your_theme_name_colors', $sections, 'Colors section should be registered');
        $this->assertArrayHasKey('your_theme_name_layout', $sections, 'Layout section should be registered');
    }

    /**
     * Test customizer settings
     */
    public function test_customizer_settings() {
        $settings = $this->customizer->settings();
        
        $this->assertArrayHasKey('your_theme_name_primary_color', $settings, 'Primary color setting should be registered');
        $this->assertArrayHasKey('your_theme_name_layout', $settings, 'Layout setting should be registered');
    }

    /**
     * Test customizer controls
     */
    public function test_customizer_controls() {
        $controls = $this->customizer->controls();
        
        $this->assertArrayHasKey('your_theme_name_primary_color', $controls, 'Primary color control should be registered');
        $this->assertInstanceOf('WP_Customize_Color_Control', $controls['your_theme_name_primary_color'], 'Primary color should be color control');
    }

    /**
     * Test customizer values
     */
    public function test_customizer_values() {
        $primary_color = get_theme_mod('your_theme_name_primary_color', '#007cba');
        $this->assertEquals('#007cba', $primary_color, 'Default primary color should be set');
        
        // Test setting custom value
        set_theme_mod('your_theme_name_primary_color', '#ff0000');
        $new_color = get_theme_mod('your_theme_name_primary_color');
        $this->assertEquals('#ff0000', $new_color, 'Custom primary color should be saved');
    }
}
```

## Database Testing

### Database Operations Tests

```php
// tests/test-database.php
<?php
/**
 * Database operations tests
 */

class Database_Test extends WP_UnitTestCase {

    protected $table_name;

    public function setUp() {
        parent::setUp();
        global $wpdb;
        $this->table_name = $wpdb->prefix . 'test_table';
        
        // Create test table
        $this->create_test_table();
    }

    public function tearDown() {
        global $wpdb;
        $wpdb->query("DROP TABLE IF EXISTS {$this->table_name}");
        parent::tearDown();
    }

    /**
     * Create test table
     */
    private function create_test_table() {
        global $wpdb;
        
        $charset_collate = $wpdb->get_charset_collate();
        
        $sql = "CREATE TABLE {$this->table_name} (
            id mediumint(9) NOT NULL AUTO_INCREMENT,
            name varchar(100) NOT NULL,
            email varchar(100) NOT NULL,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (id)
        ) $charset_collate;";
        
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql);
    }

    /**
     * Test table creation
     */
    public function test_table_creation() {
        global $wpdb;
        
        $table_exists = $wpdb->get_var("SHOW TABLES LIKE '{$this->table_name}'");
        $this->assertEquals($this->table_name, $table_exists, 'Test table should exist');
    }

    /**
     * Test data insertion
     */
    public function test_data_insertion() {
        global $wpdb;
        
        $data = array(
            'name' => 'John Doe',
            'email' => 'john@example.com'
        );
        
        $result = $wpdb->insert($this->table_name, $data);
        $this->assertNotFalse($result, 'Data insertion should succeed');
        
        $inserted_id = $wpdb->insert_id;
        $this->assertGreaterThan(0, $inserted_id, 'Insert ID should be returned');
    }

    /**
     * Test data retrieval
     */
    public function test_data_retrieval() {
        global $wpdb;
        
        // Insert test data
        $wpdb->insert($this->table_name, array(
            'name' => 'Jane Doe',
            'email' => 'jane@example.com'
        ));
        
        // Retrieve data
        $results = $wpdb->get_results("SELECT * FROM {$this->table_name} WHERE name = 'Jane Doe'");
        
        $this->assertCount(1, $results, 'Should retrieve one record');
        $this->assertEquals('jane@example.com', $results[0]->email, 'Email should match');
    }

    /**
     * Test data update
     */
    public function test_data_update() {
        global $wpdb;
        
        // Insert test data
        $wpdb->insert($this->table_name, array(
            'name' => 'Bob Smith',
            'email' => 'bob@example.com'
        ));
        
        $inserted_id = $wpdb->insert_id;
        
        // Update data
        $result = $wpdb->update(
            $this->table_name,
            array('email' => 'bob.smith@example.com'),
            array('id' => $inserted_id)
        );
        
        $this->assertEquals(1, $result, 'One record should be updated');
        
        // Verify update
        $updated_data = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->table_name} WHERE id = %d", $inserted_id));
        $this->assertEquals('bob.smith@example.com', $updated_data->email, 'Email should be updated');
    }

    /**
     * Test data deletion
     */
    public function test_data_deletion() {
        global $wpdb;
        
        // Insert test data
        $wpdb->insert($this->table_name, array(
            'name' => 'Alice Johnson',
            'email' => 'alice@example.com'
        ));
        
        $inserted_id = $wpdb->insert_id;
        
        // Delete data
        $result = $wpdb->delete($this->table_name, array('id' => $inserted_id));
        
        $this->assertEquals(1, $result, 'One record should be deleted');
        
        // Verify deletion
        $deleted_data = $wpdb->get_row($wpdb->prepare("SELECT * FROM {$this->table_name} WHERE id = %d", $inserted_id));
        $this->assertNull($deleted_data, 'Record should be deleted');
    }
}
```

## Integration Testing

### WordPress Integration Tests

```php
// tests/test-integration.php
<?php
/**
 * WordPress integration tests
 */

class Integration_Test extends WP_UnitTestCase {

    /**
     * Test WordPress hooks integration
     */
    public function test_hooks_integration() {
        $plugin = new Your_Plugin();
        $plugin->init();
        
        // Test that hooks are properly registered
        $this->assertGreaterThan(0, has_action('init', array($plugin, 'init')), 'Init hook should be registered');
        $this->assertGreaterThan(0, has_action('wp_enqueue_scripts', array($plugin, 'enqueue_scripts')), 'Scripts hook should be registered');
        $this->assertGreaterThan(0, has_action('admin_menu', array($plugin, 'add_admin_menu')), 'Admin menu hook should be registered');
    }

    /**
     * Test WordPress filters integration
     */
    public function test_filters_integration() {
        $plugin = new Your_Plugin();
        $plugin->init();
        
        // Test content filter
        $content = 'Original content';
        $filtered_content = apply_filters('the_content', $content);
        
        $this->assertStringContainsString('your-plugin', $filtered_content, 'Content should be filtered by plugin');
    }

    /**
     * Test WordPress user integration
     */
    public function test_user_integration() {
        // Create test user
        $user_id = wp_create_user('testuser', 'password', 'test@example.com');
        $this->assertGreaterThan(0, $user_id, 'User should be created');
        
        // Test user capabilities
        $user = new WP_User($user_id);
        $this->assertTrue($user->has_cap('read'), 'User should have read capability');
        
        // Test user meta
        update_user_meta($user_id, 'your_plugin_setting', 'test_value');
        $meta_value = get_user_meta($user_id, 'your_plugin_setting', true);
        $this->assertEquals('test_value', $meta_value, 'User meta should be saved and retrieved');
    }

    /**
     * Test WordPress post integration
     */
    public function test_post_integration() {
        // Create test post
        $post_id = wp_insert_post(array(
            'post_title' => 'Test Post',
            'post_content' => 'Test content',
            'post_status' => 'publish'
        ));
        
        $this->assertGreaterThan(0, $post_id, 'Post should be created');
        
        // Test post meta
        update_post_meta($post_id, 'your_plugin_meta', 'meta_value');
        $meta_value = get_post_meta($post_id, 'your_plugin_meta', true);
        $this->assertEquals('meta_value', $meta_value, 'Post meta should be saved and retrieved');
        
        // Test post terms
        $term_id = wp_insert_term('Test Category', 'category');
        wp_set_post_terms($post_id, array($term_id['term_id']), 'category');
        
        $post_terms = wp_get_post_terms($post_id, 'category');
        $this->assertCount(1, $post_terms, 'Post should have one category');
        $this->assertEquals('Test Category', $post_terms[0]->name, 'Category name should match');
    }
}
```

## Performance Testing

### WordPress Performance Tests

```php
// tests/test-performance.php
<?php
/**
 * WordPress performance tests
 */

class Performance_Test extends WP_UnitTestCase {

    /**
     * Test database query performance
     */
    public function test_database_query_performance() {
        global $wpdb;
        
        // Reset query count
        $wpdb->queries = array();
        
        // Perform operations
        $posts = get_posts(array('numberposts' => 10));
        
        // Check query count
        $query_count = count($wpdb->queries);
        $this->assertLessThan(5, $query_count, 'Should not exceed 5 queries for 10 posts');
        
        // Test query time
        $total_time = 0;
        foreach ($wpdb->queries as $query) {
            $total_time += $query[1];
        }
        
        $this->assertLessThan(0.1, $total_time, 'Total query time should be less than 0.1 seconds');
    }

    /**
     * Test memory usage
     */
    public function test_memory_usage() {
        $initial_memory = memory_get_usage();
        
        // Perform memory-intensive operations
        $data = array();
        for ($i = 0; $i < 1000; $i++) {
            $data[] = str_repeat('x', 1000);
        }
        
        $peak_memory = memory_get_peak_usage();
        $memory_increase = $peak_memory - $initial_memory;
        
        // Memory increase should be reasonable (less than 10MB)
        $this->assertLessThan(10 * 1024 * 1024, $memory_increase, 'Memory usage should be reasonable');
        
        unset($data);
    }

    /**
     * Test execution time
     */
    public function test_execution_time() {
        $start_time = microtime(true);
        
        // Perform operations
        for ($i = 0; $i < 100; $i++) {
            wp_insert_post(array(
                'post_title' => "Test Post $i",
                'post_content' => 'Test content',
                'post_status' => 'publish'
            ));
        }
        
        $end_time = microtime(true);
        $execution_time = $end_time - $start_time;
        
        // Should complete within 2 seconds
        $this->assertLessThan(2, $execution_time, 'Operations should complete within 2 seconds');
    }
}
```

## Testing Best Practices

### Test Organization and Structure

```php
// tests/TestCase.php - Base test case class
<?php
/**
 * Base test case class for WordPress testing
 */

abstract class TestCase extends WP_UnitTestCase {

    protected $plugin;
    protected $user_id;
    protected $post_id;

    public function setUp() {
        parent::setUp();
        
        // Initialize plugin
        if (class_exists('Your_Plugin')) {
            $this->plugin = new Your_Plugin();
        }
        
        // Create test user
        $this->user_id = wp_create_user('testuser', 'password', 'test@example.com');
        
        // Create test post
        $this->post_id = wp_insert_post(array(
            'post_title' => 'Test Post',
            'post_content' => 'Test content',
            'post_status' => 'publish'
        ));
    }

    public function tearDown() {
        // Clean up test data
        wp_delete_user($this->user_id);
        wp_delete_post($this->post_id, true);
        
        parent::tearDown();
    }

    /**
     * Helper method to create test data
     */
    protected function create_test_data($type = 'post', $count = 1) {
        $data = array();
        
        for ($i = 0; $i < $count; $i++) {
            switch ($type) {
                case 'post':
                    $data[] = wp_insert_post(array(
                        'post_title' => "Test Post $i",
                        'post_content' => "Test content $i",
                        'post_status' => 'publish'
                    ));
                    break;
                    
                case 'user':
                    $data[] = wp_create_user("testuser$i", 'password', "test$i@example.com");
                    break;
            }
        }
        
        return $data;
    }

    /**
     * Helper method to assert array structure
     */
    protected function assertArrayStructure(array $structure, array $array) {
        foreach ($structure as $key => $value) {
            $this->assertArrayHasKey($key, $array, "Array should have key '$key'");
            
            if (is_array($value)) {
                $this->assertIsArray($array[$key], "Key '$key' should be an array");
                $this->assertArrayStructure($value, $array[$key]);
            } else {
                $this->assertEquals($value, $array[$key], "Key '$key' should equal '$value'");
            }
        }
    }
}
```

### Test Data Management

```php
// tests/TestData.php - Test data management
<?php
/**
 * Test data management class
 */

class TestData {

    private static $created_posts = array();
    private static $created_users = array();
    private static $created_terms = array();

    /**
     * Create test post
     */
    public static function create_post($args = array()) {
        $defaults = array(
            'post_title' => 'Test Post',
            'post_content' => 'Test content',
            'post_status' => 'publish',
            'post_type' => 'post'
        );
        
        $args = wp_parse_args($args, $defaults);
        $post_id = wp_insert_post($args);
        
        if ($post_id) {
            self::$created_posts[] = $post_id;
        }
        
        return $post_id;
    }

    /**
     * Create test user
     */
    public static function create_user($args = array()) {
        $defaults = array(
            'user_login' => 'testuser',
            'user_email' => 'test@example.com',
            'user_pass' => 'password',
            'role' => 'subscriber'
        );
        
        $args = wp_parse_args($args, $defaults);
        $user_id = wp_create_user($args['user_login'], $args['user_pass'], $args['user_email']);
        
        if ($user_id) {
            $user = new WP_User($user_id);
            $user->set_role($args['role']);
            self::$created_users[] = $user_id;
        }
        
        return $user_id;
    }

    /**
     * Create test term
     */
    public static function create_term($args = array()) {
        $defaults = array(
            'name' => 'Test Term',
            'taxonomy' => 'category',
            'description' => 'Test term description'
        );
        
        $args = wp_parse_args($args, $defaults);
        $result = wp_insert_term($args['name'], $args['taxonomy'], $args);
        
        if (!is_wp_error($result)) {
            self::$created_terms[] = array(
                'term_id' => $result['term_id'],
                'taxonomy' => $args['taxonomy']
            );
            return $result['term_id'];
        }
        
        return false;
    }

    /**
     * Clean up all created test data
     */
    public static function cleanup() {
        // Clean up posts
        foreach (self::$created_posts as $post_id) {
            wp_delete_post($post_id, true);
        }
        self::$created_posts = array();
        
        // Clean up users
        foreach (self::$created_users as $user_id) {
            wp_delete_user($user_id);
        }
        self::$created_users = array();
        
        // Clean up terms
        foreach (self::$created_terms as $term_data) {
            wp_delete_term($term_data['term_id'], $term_data['taxonomy']);
        }
        self::$created_terms = array();
    }
}
```

## Official Documentation

https://make.wordpress.org/core/handbook/testing/
https://phpunit.de/documentation.html
https://github.com/wp-cli/wp-cli
