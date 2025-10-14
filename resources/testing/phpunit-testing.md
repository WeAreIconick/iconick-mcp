# PHPUnit Testing

Comprehensive guide to PHPUnit testing for WordPress development with advanced testing techniques and best practices.

## PHPUnit Setup and Configuration

### PHPUnit Configuration

```xml
<!-- phpunit.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.5/phpunit.xsd"
         bootstrap="tests/bootstrap.php"
         colors="true"
         processIsolation="false"
         stopOnFailure="false"
         syntaxCheck="false">
    
    <testsuites>
        <testsuite name="WordPress Plugin Tests">
            <directory>tests/</directory>
        </testsuite>
    </testsuites>
    
    <filter>
        <whitelist>
            <directory suffix=".php">includes/</directory>
            <exclude>
                <directory>tests/</directory>
                <directory>vendor/</directory>
            </exclude>
        </whitelist>
    </filter>
    
    <logging>
        <log type="coverage-html" target="tests/coverage/"/>
        <log type="coverage-clover" target="tests/coverage.xml"/>
        <log type="junit" target="tests/junit.xml"/>
    </logging>
    
    <php>
        <const name="WP_TESTS_DIR" value="/tmp/wordpress-tests-lib"/>
        <const name="WP_TESTS_DOMAIN" value="example.org"/>
        <const name="WP_TESTS_EMAIL" value="admin@example.org"/>
        <const name="WP_TESTS_TITLE" value="Test Blog"/>
        <const name="WP_PHP_BINARY" value="php"/>
        <const name="WP_TESTS_FORCE_KNOWN_BUGS" value="true"/>
    </php>
</phpunit>
```

### Composer Configuration

```json
{
    "require-dev": {
        "phpunit/phpunit": "^9.5",
        "yoast/phpunit-polyfills": "^1.0",
        "brain/monkey": "^2.6",
        "mockery/mockery": "^1.4"
    },
    "autoload-dev": {
        "psr-4": {
            "Tests\\": "tests/"
        }
    },
    "scripts": {
        "test": "phpunit",
        "test-coverage": "phpunit --coverage-html tests/coverage/",
        "test-watch": "phpunit --watch"
    }
}
```

## Basic PHPUnit Testing

### Test Case Structure

```php
<?php
// tests/Unit/PluginTest.php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use YourPlugin\Plugin;

class PluginTest extends TestCase {

    private $plugin;

    protected function setUp(): void {
        parent::setUp();
        $this->plugin = new Plugin();
    }

    protected function tearDown(): void {
        parent::tearDown();
        $this->plugin = null;
    }

    /**
     * @test
     */
    public function it_can_be_instantiated() {
        $this->assertInstanceOf(Plugin::class, $this->plugin);
    }

    /**
     * @test
     */
    public function it_has_correct_version() {
        $this->assertEquals('1.0.0', $this->plugin->get_version());
    }

    /**
     * @test
     */
    public function it_returns_plugin_name() {
        $this->assertEquals('Your Plugin', $this->plugin->get_name());
    }
}
```

### Assertion Methods

```php
<?php
// tests/Unit/AssertionTest.php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class AssertionTest extends TestCase {

    /**
     * @test
     */
    public function basic_assertions() {
        // Basic assertions
        $this->assertTrue(true);
        $this->assertFalse(false);
        $this->assertNull(null);
        $this->assertNotNull('not null');
        
        // Equality assertions
        $this->assertEquals('expected', 'expected');
        $this->assertNotEquals('expected', 'actual');
        $this->assertSame(1, 1);
        $this->assertNotSame(1, '1');
    }

    /**
     * @test
     */
    public function array_assertions() {
        $array = ['apple', 'banana', 'cherry'];
        
        $this->assertIsArray($array);
        $this->assertCount(3, $array);
        $this->assertContains('banana', $array);
        $this->assertNotContains('orange', $array);
        $this->assertArrayHasKey(1, $array);
        $this->assertArrayNotHasKey(3, $array);
        
        // Array subset
        $this->assertArraySubset(['banana', 'cherry'], $array);
    }

    /**
     * @test
     */
    public function string_assertions() {
        $string = 'Hello World';
        
        $this->assertStringContainsString('World', $string);
        $this->assertStringNotContainsString('Universe', $string);
        $this->assertStringStartsWith('Hello', $string);
        $this->assertStringEndsWith('World', $string);
        $this->assertMatchesRegularExpression('/^Hello/', $string);
        $this->assertStringEqualsFile('expected.txt', $string);
    }

    /**
     * @test
     */
    public function numeric_assertions() {
        $number = 42;
        
        $this->assertGreaterThan(40, $number);
        $this->assertGreaterThanOrEqual(42, $number);
        $this->assertLessThan(50, $number);
        $this->assertLessThanOrEqual(42, $number);
        $this->assertIsInt($number);
        $this->assertIsFloat(3.14);
        $this->assertIsNumeric('123');
    }
}
```

## Advanced PHPUnit Features

### Data Providers

```php
<?php
// tests/Unit/DataProviderTest.php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class DataProviderTest extends TestCase {

    /**
     * @test
     * @dataProvider additionProvider
     */
    public function test_addition($a, $b, $expected) {
        $this->assertEquals($expected, $a + $b);
    }

    public function additionProvider() {
        return [
            'adding zeros' => [0, 0, 0],
            'adding positive numbers' => [1, 1, 2],
            'adding negative numbers' => [-1, -1, -2],
            'adding mixed numbers' => [1, -1, 0],
        ];
    }

    /**
     * @test
     * @dataProvider stringProvider
     */
    public function test_string_operations($input, $expected_length, $expected_uppercase) {
        $this->assertEquals($expected_length, strlen($input));
        $this->assertEquals($expected_uppercase, strtoupper($input));
    }

    public function stringProvider() {
        return [
            'empty string' => ['', 0, ''],
            'single character' => ['a', 1, 'A'],
            'word' => ['hello', 5, 'HELLO'],
            'sentence' => ['hello world', 11, 'HELLO WORLD'],
        ];
    }
}
```

### Test Doubles (Mocks and Stubs)

```php
<?php
// tests/Unit/MockTest.php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use YourPlugin\ApiClient;
use YourPlugin\DataProcessor;

class MockTest extends TestCase {

    /**
     * @test
     */
    public function it_uses_mock_api_client() {
        // Create a mock
        $mockApiClient = $this->createMock(ApiClient::class);
        
        // Configure the mock
        $mockApiClient->expects($this->once())
                     ->method('fetch_data')
                     ->with('test_endpoint')
                     ->willReturn(['status' => 'success', 'data' => 'test']);
        
        // Use the mock
        $processor = new DataProcessor($mockApiClient);
        $result = $processor->process_data('test_endpoint');
        
        $this->assertEquals('test', $result);
    }

    /**
     * @test
     */
    public function it_handles_api_failure() {
        $mockApiClient = $this->createMock(ApiClient::class);
        
        $mockApiClient->expects($this->once())
                     ->method('fetch_data')
                     ->willThrowException(new \Exception('API Error'));
        
        $processor = new DataProcessor($mockApiClient);
        
        $this->expectException(\Exception::class);
        $processor->process_data('failing_endpoint');
    }

    /**
     * @test
     */
    public function it_uses_stub_for_database() {
        $stub = $this->createStub(\wpdb::class);
        
        $stub->method('get_results')
             ->willReturn([
                 (object)['id' => 1, 'name' => 'Test'],
                 (object)['id' => 2, 'name' => 'Test2']
             ]);
        
        $dataService = new DataService($stub);
        $results = $dataService->get_all_records();
        
        $this->assertCount(2, $results);
        $this->assertEquals('Test', $results[0]->name);
    }
}
```

### Exception Testing

```php
<?php
// tests/Unit/ExceptionTest.php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use YourPlugin\Validator;
use YourPlugin\InvalidDataException;

class ExceptionTest extends TestCase {

    /**
     * @test
     */
    public function it_throws_exception_for_invalid_email() {
        $validator = new Validator();
        
        $this->expectException(InvalidDataException::class);
        $this->expectExceptionMessage('Invalid email format');
        $this->expectExceptionCode(400);
        
        $validator->validate_email('invalid-email');
    }

    /**
     * @test
     */
    public function it_throws_exception_for_empty_data() {
        $validator = new Validator();
        
        $this->expectException(\InvalidArgumentException::class);
        $validator->validate_required_field('');
    }

    /**
     * @test
     */
    public function it_does_not_throw_for_valid_data() {
        $validator = new Validator();
        
        $this->expectNotToPerformAssertions();
        $validator->validate_email('test@example.com');
    }
}
```

## WordPress-Specific Testing

### WordPress Mock Functions

```php
<?php
// tests/Unit/WordPressMockTest.php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use Brain\Monkey;
use Brain\Monkey\Functions;

class WordPressMockTest extends TestCase {

    protected function setUp(): void {
        parent::setUp();
        Monkey\setUp();
    }

    protected function tearDown(): void {
        Monkey\tearDown();
        parent::tearDown();
    }

    /**
     * @test
     */
    public function it_mocks_wordpress_functions() {
        // Mock WordPress functions
        Functions\when('get_option')->justReturn('test_value');
        Functions\when('update_option')->justReturn(true);
        Functions\when('wp_remote_get')->justReturn(['body' => '{"status": "success"}']);
        
        $service = new WordPressService();
        
        $this->assertEquals('test_value', $service->get_setting('test_option'));
        $this->assertTrue($service->update_setting('test_option', 'new_value'));
        $this->assertEquals(['status' => 'success'], $service->fetch_remote_data());
    }

    /**
     * @test
     */
    public function it_mocks_wordpress_hooks() {
        Functions\when('add_action')->justReturn(true);
        Functions\when('add_filter')->justReturn(true);
        Functions\when('apply_filters')->returnArg();
        
        $plugin = new YourPlugin();
        $plugin->init();
        
        // Verify hooks were registered
        Functions\expect('add_action')->with('init', [$plugin, 'init'])->once();
        Functions\expect('add_filter')->with('the_content', [$plugin, 'filter_content'])->once();
    }

    /**
     * @test
     */
    public function it_mocks_database_operations() {
        global $wpdb;
        
        $wpdb = $this->createMock(\wpdb::class);
        $wpdb->method('get_results')->willReturn([
            (object)['id' => 1, 'title' => 'Test Post']
        ]);
        $wpdb->method('insert')->willReturn(1);
        $wpdb->insert_id = 123;
        
        $repository = new PostRepository();
        
        $posts = $repository->get_all_posts();
        $this->assertCount(1, $posts);
        
        $post_id = $repository->create_post(['title' => 'New Post']);
        $this->assertEquals(123, $post_id);
    }
}
```

### WordPress Integration Tests

```php
<?php
// tests/Integration/WordPressIntegrationTest.php

namespace Tests\Integration;

use WP_UnitTestCase;

class WordPressIntegrationTest extends WP_UnitTestCase {

    /**
     * @test
     */
    public function it_integrates_with_wordpress_hooks() {
        $plugin = new YourPlugin();
        
        // Test that hooks are actually registered
        $this->assertGreaterThan(0, has_action('init', [$plugin, 'init']));
        $this->assertGreaterThan(0, has_action('wp_enqueue_scripts', [$plugin, 'enqueue_scripts']));
        $this->assertGreaterThan(0, has_filter('the_content', [$plugin, 'filter_content']));
    }

    /**
     * @test
     */
    public function it_creates_database_tables() {
        $plugin = new YourPlugin();
        $plugin->activate();
        
        global $wpdb;
        $table_name = $wpdb->prefix . 'your_plugin_data';
        
        $table_exists = $wpdb->get_var("SHOW TABLES LIKE '$table_name'");
        $this->assertEquals($table_name, $table_exists);
    }

    /**
     * @test
     */
    public function it_handles_shortcodes() {
        add_shortcode('your_plugin_shortcode', [$this, 'shortcode_handler']);
        
        $output = do_shortcode('[your_plugin_shortcode]');
        $this->assertStringContainsString('your-plugin', $output);
    }

    public function shortcode_handler($atts) {
        return '<div class="your-plugin">Shortcode output</div>';
    }
}
```

## Test Organization and Structure

### Test Suites

```php
<?php
// tests/TestSuite.php

namespace Tests;

use PHPUnit\Framework\TestSuite;

class TestSuite extends TestSuite {

    public static function suite() {
        $suite = new TestSuite('Your Plugin Test Suite');
        
        // Add unit tests
        $suite->addTestSuite(\Tests\Unit\PluginTest::class);
        $suite->addTestSuite(\Tests\Unit\ApiClientTest::class);
        $suite->addTestSuite(\Tests\Unit\DataProcessorTest::class);
        
        // Add integration tests
        $suite->addTestSuite(\Tests\Integration\WordPressIntegrationTest::class);
        $suite->addTestSuite(\Tests\Integration\DatabaseIntegrationTest::class);
        
        // Add functional tests
        $suite->addTestSuite(\Tests\Functional\ApiFunctionalTest::class);
        
        return $suite;
    }
}
```

### Custom Assertions

```php
<?php
// tests/Support/CustomAssertions.php

namespace Tests\Support;

use PHPUnit\Framework\TestCase;

trait CustomAssertions {

    public function assertValidEmail($email, $message = '') {
        $this->assertMatchesRegularExpression(
            '/^[^\s@]+@[^\s@]+\.[^\s@]+$/',
            $email,
            $message ?: "Failed asserting that '$email' is a valid email address."
        );
    }

    public function assertValidUrl($url, $message = '') {
        $this->assertNotFalse(
            filter_var($url, FILTER_VALIDATE_URL),
            $message ?: "Failed asserting that '$url' is a valid URL."
        );
    }

    public function assertWordPressPost($post, $message = '') {
        $this->assertInstanceOf(\WP_Post::class, $post, $message);
        $this->assertGreaterThan(0, $post->ID, $message);
        $this->assertNotEmpty($post->post_title, $message);
    }

    public function assertValidJson($json, $message = '') {
        $decoded = json_decode($json, true);
        $this->assertNotNull(
            $decoded,
            $message ?: "Failed asserting that '$json' is valid JSON."
        );
    }
}
```

### Test Helpers

```php
<?php
// tests/Support/TestHelpers.php

namespace Tests\Support;

class TestHelpers {

    public static function create_test_post($args = []) {
        $defaults = [
            'post_title' => 'Test Post',
            'post_content' => 'Test content',
            'post_status' => 'publish',
            'post_type' => 'post'
        ];
        
        return wp_insert_post(array_merge($defaults, $args));
    }

    public static function create_test_user($args = []) {
        $defaults = [
            'user_login' => 'testuser',
            'user_email' => 'test@example.com',
            'user_pass' => 'password'
        ];
        
        return wp_create_user($defaults['user_login'], $defaults['user_pass'], $defaults['user_email']);
    }

    public static function create_test_term($args = []) {
        $defaults = [
            'name' => 'Test Term',
            'taxonomy' => 'category'
        ];
        
        $result = wp_insert_term($defaults['name'], $defaults['taxonomy'], $args);
        
        return is_wp_error($result) ? false : $result['term_id'];
    }

    public static function mock_wp_remote_get($response_body, $response_code = 200) {
        return [
            'body' => $response_body,
            'response' => ['code' => $response_code],
            'headers' => []
        ];
    }
}
```

## Performance Testing

### Performance Test Cases

```php
<?php
// tests/Performance/PerformanceTest.php

namespace Tests\Performance;

use PHPUnit\Framework\TestCase;

class PerformanceTest extends TestCase {

    /**
     * @test
     */
    public function database_queries_are_optimized() {
        global $wpdb;
        
        $wpdb->queries = [];
        
        // Perform operations
        $posts = get_posts(['numberposts' => 10]);
        
        $query_count = count($wpdb->queries);
        $this->assertLessThan(5, $query_count, 'Should not exceed 5 queries');
    }

    /**
     * @test
     */
    public function memory_usage_is_reasonable() {
        $initial_memory = memory_get_usage();
        
        // Perform memory-intensive operations
        $data = array_fill(0, 1000, str_repeat('x', 1000));
        
        $peak_memory = memory_get_peak_usage();
        $memory_increase = $peak_memory - $initial_memory;
        
        // Should not exceed 10MB
        $this->assertLessThan(10 * 1024 * 1024, $memory_increase);
        
        unset($data);
    }

    /**
     * @test
     */
    public function execution_time_is_acceptable() {
        $start_time = microtime(true);
        
        // Perform operations
        for ($i = 0; $i < 100; $i++) {
            wp_insert_post([
                'post_title' => "Test Post $i",
                'post_content' => 'Test content',
                'post_status' => 'publish'
            ]);
        }
        
        $execution_time = microtime(true) - $start_time;
        $this->assertLessThan(2, $execution_time, 'Should complete within 2 seconds');
    }
}
```

## Continuous Integration

### GitHub Actions Configuration

```yaml
# .github/workflows/phpunit.yml
name: PHPUnit Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        php-version: [7.4, 8.0, 8.1, 8.2]
        wordpress-version: ['latest', 'trunk']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: ${{ matrix.php-version }}
        extensions: mbstring, dom, curl, libxml, zip, pcntl, pdo, sqlite, pdo_sqlite, bcmath, soap, intl, gd, exif, iconv
        coverage: xdebug
    
    - name: Setup WordPress Test Environment
      run: |
        bash bin/install-wp-tests.sh wordpress_test root '' localhost ${{ matrix.wordpress-version }}
    
    - name: Install Dependencies
      run: composer install --prefer-dist --no-progress
    
    - name: Run PHPUnit Tests
      run: composer test
    
    - name: Upload Coverage Reports
      uses: codecov/codecov-action@v3
      with:
        file: ./tests/coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false
```

### PHPUnit Configuration for CI

```xml
<!-- phpunit.ci.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="https://schema.phpunit.de/9.5/phpunit.xsd"
         bootstrap="tests/bootstrap.php"
         colors="true"
         processIsolation="false"
         stopOnFailure="false">
    
    <testsuites>
        <testsuite name="Unit Tests">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Integration Tests">
            <directory>tests/Integration</directory>
        </testsuite>
        <testsuite name="Functional Tests">
            <directory>tests/Functional</directory>
        </testsuite>
    </testsuites>
    
    <logging>
        <log type="coverage-clover" target="tests/coverage.xml"/>
        <log type="junit" target="tests/junit.xml"/>
    </logging>
    
    <php>
        <const name="WP_TESTS_DIR" value="/tmp/wordpress-tests-lib"/>
        <const name="WP_TESTS_DOMAIN" value="example.org"/>
        <const name="WP_TESTS_EMAIL" value="admin@example.org"/>
        <const name="WP_TESTS_TITLE" value="Test Blog"/>
        <const name="WP_PHP_BINARY" value="php"/>
        <const name="WP_TESTS_FORCE_KNOWN_BUGS" value="true"/>
    </php>
</phpunit>
```

## Best Practices and Patterns

### Test Organization

```php
<?php
// tests/Unit/ServiceTest.php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use YourPlugin\Service;
use Tests\Support\CustomAssertions;

class ServiceTest extends TestCase {
    use CustomAssertions;

    private $service;

    protected function setUp(): void {
        parent::setUp();
        $this->service = new Service();
    }

    protected function tearDown(): void {
        parent::tearDown();
        $this->service = null;
    }

    /**
     * @test
     */
    public function it_processes_valid_data() {
        $input = ['name' => 'John Doe', 'email' => 'john@example.com'];
        $result = $this->service->process($input);
        
        $this->assertIsArray($result);
        $this->assertArrayHasKey('id', $result);
        $this->assertArrayHasKey('name', $result);
        $this->assertArrayHasKey('email', $result);
    }

    /**
     * @test
     */
    public function it_validates_email_format() {
        $this->assertValidEmail('test@example.com');
        $this->assertValidEmail('user.name+tag@domain.co.uk');
    }
}
```

### Test Data Management

```php
<?php
// tests/Support/TestDataFactory.php

namespace Tests\Support;

class TestDataFactory {

    public static function createUser(array $overrides = []): int {
        $defaults = [
            'user_login' => 'testuser_' . uniqid(),
            'user_email' => 'test_' . uniqid() . '@example.com',
            'user_pass' => 'password',
            'role' => 'subscriber'
        ];
        
        $userData = array_merge($defaults, $overrides);
        $userId = wp_create_user($userData['user_login'], $userData['user_pass'], $userData['user_email']);
        
        if ($userId && isset($userData['role'])) {
            $user = new \WP_User($userId);
            $user->set_role($userData['role']);
        }
        
        return $userId;
    }

    public static function createPost(array $overrides = []): int {
        $defaults = [
            'post_title' => 'Test Post ' . uniqid(),
            'post_content' => 'Test content',
            'post_status' => 'publish',
            'post_type' => 'post'
        ];
        
        return wp_insert_post(array_merge($defaults, $overrides));
    }

    public static function createTerm(array $overrides = []): int {
        $defaults = [
            'name' => 'Test Term ' . uniqid(),
            'taxonomy' => 'category'
        ];
        
        $result = wp_insert_term($defaults['name'], $defaults['taxonomy'], $overrides);
        
        return is_wp_error($result) ? false : $result['term_id'];
    }
}
```

## Official Documentation

https://phpunit.de/documentation.html
https://make.wordpress.org/core/handbook/testing/
https://github.com/yoast/phpunit-polyfills
