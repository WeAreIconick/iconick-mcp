---
difficulty: Beginner
tags: [standards, php, coding, style]
related: [standards/javascript, standards/css]
wp_version: All
---

# WordPress PHP Coding Standards

Official WordPress PHP coding standards and best practices.

## Key Principles

1. **Readability over cleverness**
2. **Consistency with WordPress core**
3. **Follow PSR standards where applicable**
4. **Security first**

## Naming Conventions

### Variables

```php
// Use lowercase with underscores
$user_name = 'John';
$post_count = 10;

// NOT camelCase
$userName = 'John'; // ❌
```

### Functions

```php
// Lowercase with underscores, prefixed
function my_plugin_get_data() {
    // ...
}

// Class methods can use camelCase
class My_Class {
    public function getData() {
        // ...
    }
}
```

### Constants

```php
// Uppercase with underscores
define( 'MY_CONSTANT', 'value' );

const API_KEY = 'key123';
```

### Classes

```php
// Capitalize words, underscores for separation
class My_Custom_Plugin {
    // ...
}

// Or use PSR-4
class MyCustomPlugin {
    // ...
}
```

## Spacing & Formatting

### Indentation

```php
// Use tabs, not spaces
function my_function() {
	$var = 'value';
	
	if ( $condition ) {
		// indented with tabs
	}
}
```

### Braces

```php
// Opening brace on same line
if ( $condition ) {
	// code
}

// NOT on new line
if ( $condition )  // ❌
{
	// code
}
```

### Spaces

```php
// Space after control structures
if ( $condition ) {  // ✅
if ($condition) {    // ❌

// Space around operators
$sum = $a + $b;  // ✅
$sum = $a+$b;    // ❌

// No space after function names
my_function( $arg );  // ✅
my_function ( $arg ); // ❌

// Space after comma
array( 'one', 'two', 'three' );  // ✅
array('one','two','three');      // ❌
```

## Arrays

### Short vs Long Syntax

```php
// Use array(), not []
$items = array( 'one', 'two', 'three' );  // ✅
$items = [ 'one', 'two', 'three' ];       // ❌ (unless PHP 5.4+)

// Associative arrays
$data = array(
	'name'  => 'John',
	'email' => 'john@example.com',
	'age'   => 30,
);
```

### Multi-line Arrays

```php
// Align arrow operators
$args = array(
	'post_type'   => 'post',
	'post_status' => 'publish',
	'numberposts' => 10,
);
```

## Control Structures

### If/Else

```php
if ( $condition ) {
	// code
} elseif ( $other_condition ) {
	// code
} else {
	// code
}

// Ternary
$result = ( $condition ) ? 'yes' : 'no';
```

### Loops

```php
// Foreach
foreach ( $items as $item ) {
	echo $item;
}

foreach ( $items as $key => $value ) {
	echo $key . ': ' . $value;
}

// For
for ( $i = 0; $i < 10; $i++ ) {
	echo $i;
}

// While
while ( $condition ) {
	// code
}
```

### Switch

```php
switch ( $value ) {
	case 'one':
		// code
		break;
		
	case 'two':
		// code
		break;
		
	default:
		// code
		break;
}
```

## Functions

### Function Structure

```php
function my_function( $arg1, $arg2 = 'default' ) {
	// Validate inputs
	if ( empty( $arg1 ) ) {
		return false;
	}
	
	// Process
	$result = do_something( $arg1, $arg2 );
	
	// Return
	return $result;
}
```

### Return Early

```php
// Good: Early returns
function process_data( $data ) {
	if ( empty( $data ) ) {
		return false;
	}
	
	if ( ! is_array( $data ) ) {
		return false;
	}
	
	// Main logic
	return processed_data;
}

// Avoid deep nesting
function process_data( $data ) {  // ❌
	if ( ! empty( $data ) ) {
		if ( is_array( $data ) ) {
			// deep nesting
		}
	}
}
```

## Documentation

### File Headers

```php
<?php
/**
 * Plugin Name: My Plugin
 * Description: Plugin description
 * Version: 1.0.0
 * Author: Your Name
 * License: GPL v2 or later
 */

// Prevent direct access
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
```

### Function Documentation

```php
/**
 * Get user data by ID.
 *
 * @param int    $user_id  User ID.
 * @param string $field    Optional. Field to retrieve. Default 'all'.
 * @return array|false User data array or false on failure.
 */
function get_user_data( $user_id, $field = 'all' ) {
	// ...
}
```

### Inline Comments

```php
// Single line comment

/* 
 * Multi-line comment
 * for longer explanations
 */

/**
 * DocBlock comment
 * for documentation
 */
```

## Classes & OOP

```php
class My_Plugin_Class {
	
	/**
	 * Class properties
	 */
	private $version = '1.0.0';
	protected $options = array();
	public $name = 'My Plugin';
	
	/**
	 * Constructor
	 */
	public function __construct() {
		$this->init();
	}
	
	/**
	 * Initialize
	 */
	private function init() {
		add_action( 'init', array( $this, 'setup' ) );
	}
	
	/**
	 * Setup
	 */
	public function setup() {
		// ...
	}
}
```

## Best Practices

### Never Use Short PHP Tags

```php
<?php echo $var; ?>  // ✅

<? echo $var; ?>     // ❌
<?= $var ?>          // ❌
```

### Use Strict Comparisons

```php
if ( $var === 'value' ) {  // ✅
if ( $var == 'value' ) {   // ❌ (unless intentional)

if ( in_array( $val, $arr, true ) ) {  // ✅
```

### Include/Require

```php
// Use require_once for critical files
require_once ABSPATH . 'wp-admin/includes/plugin.php';

// Use include for optional files
include get_template_directory() . '/inc/custom.php';
```

### Yoda Conditions

```php
// Put constant/literal first
if ( 'value' === $var ) {  // ✅ Prevents accidental assignment
if ( $var === 'value' ) {  // Also acceptable

if ( 10 < $count ) {       // ✅
if ( $count > 10 ) {       // Also acceptable
```

### SQL Queries

```php
// Always use $wpdb->prepare
global $wpdb;

$wpdb->query( $wpdb->prepare(
	"DELETE FROM {$wpdb->posts} WHERE ID = %d",
	$post_id
) );
```

## Security Patterns

```php
// Always validate, sanitize, escape
function save_data() {
	// 1. Verify nonce
	check_admin_referer( 'save_action', 'save_nonce' );
	
	// 2. Check capability
	if ( ! current_user_can( 'edit_posts' ) ) {
		wp_die( 'Unauthorized' );
	}
	
	// 3. Validate & sanitize
	$value = isset( $_POST['value'] ) ? sanitize_text_field( $_POST['value'] ) : '';
	
	if ( empty( $value ) ) {
		return false;
	}
	
	// 4. Process
	update_option( 'my_option', $value );
	
	return true;
}

// Escape on output
echo esc_html( $value );
```

## PHPCS Integration

### Install WordPress Standards

```bash
composer require --dev wp-coding-standards/wpcs
phpcs --config-set installed_paths vendor/wp-coding-standards/wpcs
```

### phpcs.xml

```xml
<?xml version="1.0"?>
<ruleset name="WordPress Coding Standards">
	<description>WordPress coding standards</description>
	
	<file>.</file>
	
	<exclude-pattern>*/vendor/*</exclude-pattern>
	<exclude-pattern>*/node_modules/*</exclude-pattern>
	
	<rule ref="WordPress-Core"/>
	<rule ref="WordPress-Extra"/>
	<rule ref="WordPress-Docs"/>
	
	<config name="minimum_supported_wp_version" value="5.0"/>
</ruleset>
```

## Official Resources

- https://developer.wordpress.org/coding-standards/wordpress-coding-standards/php/
- https://make.wordpress.org/core/handbook/best-practices/coding-standards/php/