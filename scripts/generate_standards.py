#!/usr/bin/env python3
"""Generate WordPress coding standards resources"""

from pathlib import Path

RESOURCES_DIR = Path(__file__).parent.parent / "resources"

STANDARDS = {
    "standards/php.md": """# WordPress PHP Coding Standards

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
\t$var = 'value';
\t
\tif ( $condition ) {
\t\t// indented with tabs
\t}
}
```

### Braces

```php
// Opening brace on same line
if ( $condition ) {
\t// code
}

// NOT on new line
if ( $condition )  // ❌
{
\t// code
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
\t'name'  => 'John',
\t'email' => 'john@example.com',
\t'age'   => 30,
);
```

### Multi-line Arrays

```php
// Align arrow operators
$args = array(
\t'post_type'   => 'post',
\t'post_status' => 'publish',
\t'numberposts' => 10,
);
```

## Control Structures

### If/Else

```php
if ( $condition ) {
\t// code
} elseif ( $other_condition ) {
\t// code
} else {
\t// code
}

// Ternary
$result = ( $condition ) ? 'yes' : 'no';
```

### Loops

```php
// Foreach
foreach ( $items as $item ) {
\techo $item;
}

foreach ( $items as $key => $value ) {
\techo $key . ': ' . $value;
}

// For
for ( $i = 0; $i < 10; $i++ ) {
\techo $i;
}

// While
while ( $condition ) {
\t// code
}
```

### Switch

```php
switch ( $value ) {
\tcase 'one':
\t\t// code
\t\tbreak;
\t\t
\tcase 'two':
\t\t// code
\t\tbreak;
\t\t
\tdefault:
\t\t// code
\t\tbreak;
}
```

## Functions

### Function Structure

```php
function my_function( $arg1, $arg2 = 'default' ) {
\t// Validate inputs
\tif ( empty( $arg1 ) ) {
\t\treturn false;
\t}
\t
\t// Process
\t$result = do_something( $arg1, $arg2 );
\t
\t// Return
\treturn $result;
}
```

### Return Early

```php
// Good: Early returns
function process_data( $data ) {
\tif ( empty( $data ) ) {
\t\treturn false;
\t}
\t
\tif ( ! is_array( $data ) ) {
\t\treturn false;
\t}
\t
\t// Main logic
\treturn processed_data;
}

// Avoid deep nesting
function process_data( $data ) {  // ❌
\tif ( ! empty( $data ) ) {
\t\tif ( is_array( $data ) ) {
\t\t\t// deep nesting
\t\t}
\t}
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
\texit;
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
\t// ...
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
\t
\t/**
\t * Class properties
\t */
\tprivate $version = '1.0.0';
\tprotected $options = array();
\tpublic $name = 'My Plugin';
\t
\t/**
\t * Constructor
\t */
\tpublic function __construct() {
\t\t$this->init();
\t}
\t
\t/**
\t * Initialize
\t */
\tprivate function init() {
\t\tadd_action( 'init', array( $this, 'setup' ) );
\t}
\t
\t/**
\t * Setup
\t */
\tpublic function setup() {
\t\t// ...
\t}
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
\t"DELETE FROM {$wpdb->posts} WHERE ID = %d",
\t$post_id
) );
```

## Security Patterns

```php
// Always validate, sanitize, escape
function save_data() {
\t// 1. Verify nonce
\tcheck_admin_referer( 'save_action', 'save_nonce' );
\t
\t// 2. Check capability
\tif ( ! current_user_can( 'edit_posts' ) ) {
\t\twp_die( 'Unauthorized' );
\t}
\t
\t// 3. Validate & sanitize
\t$value = isset( $_POST['value'] ) ? sanitize_text_field( $_POST['value'] ) : '';
\t
\tif ( empty( $value ) ) {
\t\treturn false;
\t}
\t
\t// 4. Process
\tupdate_option( 'my_option', $value );
\t
\treturn true;
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
\t<description>WordPress coding standards</description>
\t
\t<file>.</file>
\t
\t<exclude-pattern>*/vendor/*</exclude-pattern>
\t<exclude-pattern>*/node_modules/*</exclude-pattern>
\t
\t<rule ref="WordPress-Core"/>
\t<rule ref="WordPress-Extra"/>
\t<rule ref="WordPress-Docs"/>
\t
\t<config name="minimum_supported_wp_version" value="5.0"/>
</ruleset>
```

## Official Resources

- https://developer.wordpress.org/coding-standards/wordpress-coding-standards/php/
- https://make.wordpress.org/core/handbook/best-practices/coding-standards/php/
""",

    "standards/javascript.md": """# WordPress JavaScript Coding Standards

Official WordPress JavaScript coding standards and best practices.

## Modern JavaScript (ES6+)

WordPress supports modern JavaScript with transpilation via `@wordpress/scripts`.

### Variables

```javascript
// Use const for unchanging values
const API_URL = 'https://api.example.com';

// Use let for changing values
let count = 0;

// Avoid var
var oldStyle = 'avoid';  // ❌
```

### Functions

```javascript
// Arrow functions
const add = ( a, b ) => a + b;

// Function declarations
function calculateTotal( items ) {
\treturn items.reduce( ( sum, item ) => sum + item.price, 0 );
}

// Async/await
async function fetchData() {
\tconst response = await fetch( API_URL );
\tconst data = await response.json();
\treturn data;
}
```

### Template Literals

```javascript
// Use template literals for strings
const message = `Hello, ${ userName }!`;

// Multi-line strings
const html = `
\t<div class="message">
\t\t<h2>${ title }</h2>
\t\t<p>${ content }</p>
\t</div>
`;
```

### Destructuring

```javascript
// Object destructuring
const { title, content, author } = post;

// Array destructuring
const [ first, second, ...rest ] = items;

// Function parameters
function renderPost( { title, content, date } ) {
\t// ...
}
```

### Spread Operator

```javascript
// Copy array
const newItems = [ ...items ];

// Merge objects
const settings = {
\t...defaultSettings,
\t...userSettings,
};
```

## WordPress JavaScript Patterns

### @wordpress/scripts

```javascript
// Import WordPress packages
import { __ } from '@wordpress/i18n';
import { useSelect } from '@wordpress/data';
import { Button } from '@wordpress/components';

// Use translation
const message = __( 'Hello World', 'textdomain' );
```

### jQuery (Legacy)

```javascript
// Wrap in ready
jQuery( document ).ready( function( $ ) {
\t// Use $ safely
\t$( '.button' ).on( 'click', function() {
\t\t// Handle click
\t} );
} );

// Or use IIFE
( function( $ ) {
\t$( '.element' ).hide();
} )( jQuery );
```

### AJAX

```javascript
// Modern approach with fetch
async function saveData( data ) {
\tconst response = await fetch( ajaxurl, {
\t\tmethod: 'POST',
\t\theaders: {
\t\t\t'Content-Type': 'application/x-www-form-urlencoded',
\t\t},
\t\tbody: new URLSearchParams( {
\t\t\taction: 'save_data',
\t\t\tnonce: myData.nonce,
\t\t\tdata: JSON.stringify( data ),
\t\t} ),
\t} );
\t
\treturn response.json();
}

// jQuery approach
jQuery.ajax( {
\turl: ajaxurl,
\ttype: 'POST',
\tdata: {
\t\taction: 'save_data',
\t\tnonce: myData.nonce,
\t\tdata: formData,
\t},
\tsuccess: function( response ) {
\t\tconsole.log( response );
\t},
} );
```

### wp.apiFetch (REST API)

```javascript
import apiFetch from '@wordpress/api-fetch';

// GET request
const posts = await apiFetch( { path: '/wp/v2/posts' } );

// POST request
const newPost = await apiFetch( {
\tpath: '/wp/v2/posts',
\tmethod: 'POST',
\tdata: {
\t\ttitle: 'My Post',
\t\tcontent: 'Content here',
\t\tstatus: 'publish',
\t},
} );
```

## React Best Practices

### Functional Components

```javascript
import { useState } from '@wordpress/element';

function MyComponent( { initialValue } ) {
\tconst [ value, setValue ] = useState( initialValue );
\t
\treturn (
\t\t<div>
\t\t\t<input
\t\t\t\ttype="text"
\t\t\t\tvalue={ value }
\t\t\t\tonChange={ ( e ) => setValue( e.target.value ) }
\t\t\t/>
\t\t</div>
\t);
}
```

### Hooks

```javascript
import { useState, useEffect } from '@wordpress/element';

function DataComponent() {
\tconst [ data, setData ] = useState( null );
\t
\tuseEffect( () => {
\t\tfetchData().then( setData );
\t}, [] );
\t
\tif ( ! data ) {
\t\treturn <Spinner />;
\t}
\t
\treturn <div>{ data.title }</div>;
}
```

## Code Style

### Indentation

```javascript
// Use tabs for indentation
function myFunction() {
\tif ( condition ) {
\t\t// code
\t}
}
```

### Spacing

```javascript
// Space after keywords
if ( condition ) {
\t// code
}

// Space around operators
const sum = a + b;

// No space after function name
myFunction( arg );

// Space after comma
const arr = [ 'one', 'two', 'three' ];
```

### Quotes

```javascript
// Use single quotes
const message = 'Hello World';

// Unless string contains single quote
const text = "It's a nice day";

// Or use template literals
const text = `It's a nice day`;
```

### Semicolons

```javascript
// Always use semicolons
const value = 123;
doSomething();
```

## Event Handling

### Event Listeners

```javascript
// Modern
element.addEventListener( 'click', handleClick );

function handleClick( event ) {
\tevent.preventDefault();
\t// Handle click
}

// Remove listener
element.removeEventListener( 'click', handleClick );
```

### Event Delegation

```javascript
// Delegate to parent
document.addEventListener( 'click', function( event ) {
\tif ( event.target.matches( '.button' ) ) {
\t\t// Handle button click
\t}
} );
```

## Error Handling

```javascript
// Try/catch
try {
\tconst data = JSON.parse( jsonString );
} catch ( error ) {
\tconsole.error( 'Parse error:', error );
}

// Async/await error handling
async function fetchData() {
\ttry {
\t\tconst response = await fetch( url );
\t\tif ( ! response.ok ) {
\t\t\tthrow new Error( 'Network error' );
\t\t}
\t\treturn response.json();
\t} catch ( error ) {
\t\tconsole.error( 'Fetch error:', error );
\t\treturn null;
\t}
}
```

## Performance

### Debouncing

```javascript
import { debounce } from '@wordpress/compose';

const debouncedSearch = debounce( ( value ) => {
\t// Perform search
}, 300 );

<input onChange={ ( e ) => debouncedSearch( e.target.value ) } />
```

### Memoization

```javascript
import { useMemo } from '@wordpress/element';

const expensiveValue = useMemo( () => {
\treturn computeExpensiveValue( a, b );
}, [ a, b ] );
```

## ESLint Configuration

### .eslintrc.js

```javascript
module.exports = {
\textends: [ 'plugin:@wordpress/eslint-plugin/recommended' ],
\trules: {
\t\t'@wordpress/no-unused-vars-before-return': 'error',
\t\t'@wordpress/dependency-group': 'error',
\t},
};
```

### Package Scripts

```json
{
\t"scripts": {
\t\t"lint:js": "wp-scripts lint-js",
\t\t"format:js": "wp-scripts format-js"
\t}
}
```

## Security

### XSS Prevention

```javascript
// Escape HTML
import { escapeHTML } from '@wordpress/escape-html';

const safe = escapeHTML( userInput );

// Create elements safely
const div = document.createElement( 'div' );
div.textContent = userInput;  // Safe
div.innerHTML = userInput;    // Unsafe!
```

### Nonce Verification

```javascript
// Include nonce in AJAX
wp_localize_script( 'my-script', 'myData', {
\tajaxurl: admin_url( 'admin-ajax.php' ),
\tnonce: wp_create_nonce( 'my_action' ),
} );

// Use in request
fetch( myData.ajaxurl, {
\tmethod: 'POST',
\tbody: new URLSearchParams( {
\t\taction: 'my_action',
\t\tnonce: myData.nonce,
\t} ),
} );
```

## Official Resources

- https://developer.wordpress.org/coding-standards/wordpress-coding-standards/javascript/
- https://developer.wordpress.org/block-editor/reference-guides/packages/
""",
}

# Create resources
for filepath, content in STANDARDS.items():
    full_path = RESOURCES_DIR / filepath
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip())
    print(f"Created: {filepath}")

print(f"\\nGenerated {len(STANDARDS)} standards files")
