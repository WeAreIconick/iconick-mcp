# WordPress Plugin Check - Complete Compliance Guide

The Plugin Check (PCP) tool is the official WordPress.org plugin validation tool. This guide covers all checks to ensure your plugins pass validation and never encounter common issues.

## 🎯 Overview

Plugin Check tests whether your plugin meets WordPress.org plugin directory requirements and follows development best practices across security, performance, accessibility, and code quality.

## 📋 Check Categories

1. **Plugin Repo** - Required for WordPress.org approval
2. **Security** - Critical security standards
3. **Performance** - Optimization best practices
4. **General** - Code quality and standards

---

## 1. Plugin Header Requirements

### Required Headers

```php
/**
 * Plugin Name:       My Awesome Plugin
 * Plugin URI:        https://example.com/my-plugin
 * Description:       A clear, descriptive plugin description
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            Your Name
 * Author URI:        https://example.com
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       my-plugin-slug
 * Domain Path:       /languages
 */
```

### ✅ Plugin Name Requirements

- **Not default text**: Avoid "Plugin Name", "My Basics Plugin"
- **Minimum 5 characters**: Must contain at least 5 latin letters (a-Z) and/or numbers
- **Descriptive**: Should clearly describe what the plugin does

```php
// ❌ BAD
Plugin Name: Plugin Name
Plugin Name: Test
Plugin Name: !!

// ✅ GOOD
Plugin Name: Contact Form Manager
Plugin Name: WooCommerce Shipping Calculator
```

### ✅ Description Requirements

- **Required**: Must not be empty
- **Not default text**: Avoid placeholder descriptions
- **Clear and concise**: Explain what the plugin does

```php
// ❌ BAD
Description: This is a short description of what the plugin does
Description: Here is a short description of the plugin
Description: Handle the basics with this plugin

// ✅ GOOD
Description: Adds advanced contact forms with spam protection and email notifications
Description: Extends WooCommerce with real-time shipping calculations
```

### ✅ Version Requirements

- **Required**: Must not be empty
- **Format**: Only numbers, letters, periods, and hyphens
- **Pattern**: `1.0.0`, `2.5.1-beta`, `1.2.3`

```php
// ❌ BAD
Version: v1.0.0
Version: 1.0 (beta)
Version: version_1

// ✅ GOOD
Version: 1.0.0
Version: 2.5.1-beta
Version: 1.2.3
```

### ✅ License Requirements

- **Required**: Must be GPLv2 or later compatible
- **Valid licenses**: GPL-2.0+, GPL-3.0+, MIT, Apache-2.0, ISC, MPL-2.0

```php
// ❌ BAD
License: Proprietary
License: Commercial
// Missing license header

// ✅ GOOD
License: GPL v2 or later
License: GPL-3.0-or-later
License: MIT
License: Apache-2.0
```

### ✅ Plugin URI Requirements

- **Valid URL**: Must be a properly formatted URL
- **No discouraged domains**: Avoid wordpress.org, github.com (as plugin homepage)
- **Unique**: Should be your plugin's official website

```php
// ❌ BAD
Plugin URI: not-a-url
Plugin URI: wordpress.org/plugins/my-plugin
Plugin URI: http://github.com/user/repo (as main plugin URI)

// ✅ GOOD
Plugin URI: https://example.com/my-plugin
Plugin URI: https://yoursite.com/plugins/contact-form
// GitHub URLs are acceptable if properly formatted
```

### ✅ Author URI Requirements

- **Valid URL**: Must be properly formatted
- **No discouraged domains**: Avoid WordPress.org, generic repository sites
- **Personal/Company**: Author's website or profile

```php
// ❌ BAD
Author URI: wordpress.org/support/users/username

// ✅ GOOD
Author URI: https://example.com
Author URI: https://yourcompany.com
Author URI: https://profiles.wordpress.org/username
```

### ✅ Requires at least / Requires PHP

- **Format**: Must be valid version numbers
- **Reasonable**: Don't require future WordPress versions

```php
// ❌ BAD
Requires at least: 10.0  // Future version
Requires PHP: php7.4     // Invalid format

// ✅ GOOD
Requires at least: 6.0
Requires at least: 6.2
Requires PHP: 7.4
Requires PHP: 8.0
```

### ✅ Text Domain Requirements

- **Match plugin slug**: Should match your plugin folder name
- **Format**: Only lowercase letters, numbers, and hyphens
- **No special characters**: Avoid underscores, spaces, capitals

```php
// If plugin folder is: my-awesome-plugin

// ❌ BAD
Text Domain: my_awesome_plugin
Text Domain: MyAwesomePlugin
Text Domain: my awesome plugin

// ✅ GOOD
Text Domain: my-awesome-plugin
```

### ✅ Domain Path Requirements

- **Start with slash**: Must begin with `/`
- **Directory exists**: Path must point to existing folder

```php
// ❌ BAD
Domain Path: languages  // Missing slash
Domain Path: /translations  // If folder doesn't exist

// ✅ GOOD
Domain Path: /languages
Domain Path: /lang
```

---

## 2. Readme.txt Requirements

### Required Readme Structure

```
=== Plugin Name ===
Contributors: username1, username2
Tags: tag1, tag2, tag3
Requires at least: 6.0
Tested up to: 6.4
Stable tag: 1.0.0
Requires PHP: 7.4
License: GPLv2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html

Short description of the plugin.

== Description ==

Long description here.

== Installation ==

Installation instructions.

== Frequently Asked Questions ==

= Question? =

Answer.

== Screenshots ==

1. Screenshot description
2. Another screenshot

== Changelog ==

= 1.0.0 =
* Initial release

== Upgrade Notice ==

= 1.0.0 =
Important upgrade information.
```

### ✅ Required Headers

- **Plugin Name**: Must match plugin header (=== Name ===)
- **Contributors**: Valid WordPress.org usernames
- **Stable tag**: Must be a valid version number (not "trunk")
- **Tested up to**: Current or recent WordPress version
- **Requires at least**: Minimum WordPress version
- **License**: GPL-compatible license

### ✅ Contributors

- **Valid usernames**: Must be existing WordPress.org usernames
- **Not restricted**: Avoid banned contributors
- **Comma-separated**: `username1, username2`

```
// ❌ BAD
Contributors: not_real_user, banned_user

// ✅ GOOD
Contributors: johnsmith, janedoe
```

### ✅ Stable Tag

- **Not "trunk"**: Must be a version number
- **Match plugin version**: Should match Version header
- **Valid format**: Semantic versioning

```
// ❌ BAD
Stable tag: trunk
Stable tag: latest

// ✅ GOOD
Stable tag: 1.0.0
Stable tag: 2.5.1
```

### ✅ Tested Up To

- **Current WordPress**: Should be current or recent version
- **Not too old**: Within two major versions
- **Not future**: Can't be beyond released WordPress

```
// If current WordPress is 6.4

// ❌ BAD
Tested up to: 5.0  // Too old
Tested up to: 7.0  // Future version

// ✅ GOOD
Tested up to: 6.4
Tested up to: 6.3
```

### ✅ Donate Link

- **Valid URL**: Must be properly formatted if included
- **Optional but recommended**

```
Donate link: https://example.com/donate
```

---

## 3. Security Requirements (CRITICAL)

### ✅ Data Validation

**ALWAYS validate ALL input data:**

```php
// ❌ BAD - No validation
$user_id = $_POST['user_id'];
update_user_meta( $user_id, 'key', 'value' );

// ✅ GOOD - Validated
$user_id = isset( $_POST['user_id'] ) ? absint( $_POST['user_id'] ) : 0;
if ( $user_id > 0 ) {
    update_user_meta( $user_id, 'key', 'value' );
}
```

### ✅ Data Sanitization

**ALWAYS sanitize data before saving:**

```php
// ❌ BAD - No sanitization
$title = $_POST['title'];
update_option( 'my_title', $title );

// ✅ GOOD - Sanitized
$title = isset( $_POST['title'] ) ? sanitize_text_field( $_POST['title'] ) : '';
update_option( 'my_title', $title );
```

**Sanitization functions:**
- `sanitize_text_field()` - Text fields
- `sanitize_email()` - Email addresses
- `sanitize_url()` / `esc_url_raw()` - URLs
- `sanitize_textarea_field()` - Textarea content
- `sanitize_key()` - Keys, slugs
- `wp_kses_post()` - HTML content (post-like)
- `wp_kses()` - Custom allowed HTML

### ✅ Output Escaping (CRITICAL)

**ALWAYS escape ALL output:**

```php
// ❌ BAD - Not escaped
echo "<div>" . $user_input . "</div>";
echo '<a href="' . $url . '">Link</a>';

// ✅ GOOD - Properly escaped
echo "<div>" . esc_html( $user_input ) . "</div>";
echo '<a href="' . esc_url( $url ) . '">' . esc_html( $text ) . '</a>';
```

**Escaping functions:**
- `esc_html()` - HTML content
- `esc_attr()` - HTML attributes
- `esc_url()` - URLs in HTML
- `esc_js()` - JavaScript strings
- `esc_textarea()` - Textarea values
- `wp_kses_post()` - Allow safe HTML tags

### ✅ Nonces (CRITICAL)

**ALWAYS verify nonces for forms and AJAX:**

```php
// ❌ BAD - No nonce
if ( isset( $_POST['action'] ) ) {
    // Process action
}

// ✅ GOOD - Verified nonce
if ( isset( $_POST['my_nonce'] ) && wp_verify_nonce( $_POST['my_nonce'], 'my_action' ) ) {
    // Process action
}

// Form example
<form method="post">
    <?php wp_nonce_field( 'my_action', 'my_nonce' ); ?>
    <input type="text" name="data">
    <input type="submit">
</form>

// AJAX example
$.ajax({
    url: ajaxurl,
    data: {
        action: 'my_action',
        nonce: my_ajax_object.nonce,
        data: data
    }
});

// PHP handler
add_action( 'wp_ajax_my_action', 'my_ajax_handler' );
function my_ajax_handler() {
    check_ajax_referer( 'my_action_nonce', 'nonce' );
    // Process
    wp_die();
}
```

### ✅ Capability Checks

**ALWAYS check user capabilities:**

```php
// ❌ BAD - No capability check
if ( isset( $_POST['delete'] ) ) {
    wp_delete_post( $_POST['post_id'] );
}

// ✅ GOOD - Capability checked
if ( current_user_can( 'delete_posts' ) && isset( $_POST['delete'] ) ) {
    wp_delete_post( absint( $_POST['post_id'] ) );
}
```

### ✅ Database Queries

**ALWAYS use prepared statements:**

```php
global $wpdb;

// ❌ BAD - SQL injection risk
$results = $wpdb->get_results( "SELECT * FROM {$wpdb->posts} WHERE ID = {$_GET['id']}" );

// ✅ GOOD - Prepared statement
$results = $wpdb->get_results( 
    $wpdb->prepare( 
        "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
        absint( $_GET['id'] )
    )
);
```

### ✅ Direct Database Query Warnings

**Prefer WordPress functions over direct queries:**

```php
// ❌ AVOID - Direct query
global $wpdb;
$wpdb->query( "DELETE FROM {$wpdb->posts} WHERE post_type = 'my_type'" );

// ✅ BETTER - WordPress function
$posts = get_posts( array( 'post_type' => 'my_type', 'numberposts' => -1 ) );
foreach ( $posts as $post ) {
    wp_delete_post( $post->ID, true );
}

// ✅ ACCEPTABLE - When necessary, use prepared statements
global $wpdb;
$wpdb->query( 
    $wpdb->prepare(
        "DELETE FROM {$wpdb->prefix}my_custom_table WHERE user_id = %d",
        $user_id
    )
);
```

### ✅ No Unfiltered Uploads

**NEVER allow unfiltered uploads:**

```php
// ❌ NEVER DO THIS
define( 'ALLOW_UNFILTERED_UPLOADS', true );

// ✅ Use WordPress media functions
$attachment_id = media_handle_upload( 'file', 0 );
if ( is_wp_error( $attachment_id ) ) {
    // Handle error
}
```

---

## 4. File and Code Requirements

### ✅ No Code Obfuscation

**NEVER obfuscate your code:**

```php
// ❌ FORBIDDEN
// - Zend Guard encoded files
// - SourceGuardian encoded files
// - ionCube encoded files
// - Base64 encoded PHP code (unless clearly commented and justified)

// ✅ GOOD
// - Readable, well-formatted code
// - Clear variable names
// - Proper comments
```

### ✅ Allowed File Types

**Only include necessary files:**

```
✅ Allowed:
- .php, .js, .css, .json
- .txt, .md (documentation)
- .png, .jpg, .gif, .svg (images)
- .pot, .po, .mo (translations)
- .woff, .woff2, .ttf, .eot (fonts)

❌ Forbidden:
- .exe, .dmg, .app (executables)
- .phar (PHP archives)
- .sh (shell scripts)
- .bin, .so, .a (compiled binaries)
- .zip, .tar, .gz (archives)
- .DS_Store (system files)
```

### ✅ No Localhost References

**Remove all localhost URLs:**

```php
// ❌ BAD
define( 'API_URL', 'http://localhost:8080/api' );
$dev_server = 'http://127.0.0.1/test';

// ✅ GOOD
define( 'API_URL', 'https://api.example.com' );
// Or make it configurable
$api_url = get_option( 'my_plugin_api_url', 'https://api.example.com' );
```

### ✅ No Offloading Files

**Don't load code from external servers:**

```php
// ❌ BAD - Remote code execution risk
include( 'http://example.com/includes/functions.php' );
require_once( 'https://cdn.example.com/plugin-core.php' );

// ✅ GOOD - Load from plugin directory
include( plugin_dir_path( __FILE__ ) . 'includes/functions.php' );
require_once( plugin_dir_path( __FILE__ ) . 'includes/class-core.php' );
```

### ✅ Plugin Updater Check

**Don't include custom updater code:**

```php
// ❌ BAD - Custom update check
function check_for_updates() {
    $response = wp_remote_get( 'https://example.com/update-check' );
    // Custom update logic
}

// ✅ GOOD - Use WordPress.org updates or documented approach
// Let WordPress handle updates from the plugin repository
// Or use official libraries like EDD Software Licensing (for premium plugins)
```

---

## 5. Internationalization (i18n)

### ✅ Proper Text Domain Usage

**Always use your plugin's text domain:**

```php
// ❌ BAD
__( 'Hello World', 'wordpress' );  // Wrong domain
__( 'Save Settings' );             // Missing domain

// ✅ GOOD
__( 'Hello World', 'my-plugin-slug' );
_e( 'Save Settings', 'my-plugin-slug' );
esc_html_e( 'Welcome', 'my-plugin-slug' );
```

### ✅ Don't Use load_plugin_textdomain() for WordPress.org

**Not necessary for WordPress.org plugins:**

```php
// ❌ UNNECESSARY for WordPress.org
add_action( 'plugins_loaded', 'my_plugin_load_textdomain' );
function my_plugin_load_textdomain() {
    load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
}

// ✅ GOOD - WordPress.org handles this automatically
// Just include your .pot file and set Domain Path in header
// WordPress.org will handle translation loading
```

### ✅ Translation Functions

```php
// Basic translation
__( 'Text', 'textdomain' );

// Echo translation
_e( 'Text', 'textdomain' );

// Escaped translation
esc_html__( 'Text', 'textdomain' );
esc_html_e( 'Text', 'textdomain' );
esc_attr__( 'Text', 'textdomain' );
esc_attr_e( 'Text', 'textdomain' );

// Plural
_n( 'One item', '%d items', $count, 'textdomain' );

// Context
_x( 'Post', 'noun', 'textdomain' );

// Translators comment
/* translators: %s: user name */
sprintf( __( 'Hello %s', 'textdomain' ), $name );
```

---

## 6. Performance Best Practices

### ✅ Enqueue Scripts Properly

```php
// ❌ BAD - Hardcoded in header
<script src="<?php echo plugins_url( 'js/script.js', __FILE__ ); ?>"></script>

// ✅ GOOD - Properly enqueued
add_action( 'wp_enqueue_scripts', 'my_plugin_enqueue_scripts' );
function my_plugin_enqueue_scripts() {
    wp_enqueue_script(
        'my-plugin-script',
        plugins_url( 'js/script.js', __FILE__ ),
        array( 'jquery' ),
        '1.0.0',
        true  // Load in footer
    );
}
```

### ✅ Script Loading Optimization

```php
// ✅ Use defer or async for non-critical scripts
add_filter( 'script_loader_tag', 'my_plugin_add_defer_attribute', 10, 2 );
function my_plugin_add_defer_attribute( $tag, $handle ) {
    if ( 'my-plugin-script' !== $handle ) {
        return $tag;
    }
    return str_replace( ' src', ' defer src', $tag );
}
```

### ✅ Limit Script/Style Size

- **Keep scripts under 50KB** (minified)
- **Keep styles under 50KB** (minified)
- **Consider code splitting** for larger plugins

### ✅ Conditional Loading

```php
// ✅ Only load on relevant pages
add_action( 'wp_enqueue_scripts', 'my_plugin_conditional_scripts' );
function my_plugin_conditional_scripts() {
    if ( is_singular( 'product' ) ) {
        wp_enqueue_script( 'product-script', /* ... */ );
    }
}
```

### ✅ Optimize WP_Query

```php
// ❌ BAD - Inefficient query
$posts = get_posts( array(
    'posts_per_page' => -1,  // Gets ALL posts
    'post_type' => 'post'
) );

// ✅ GOOD - Optimized query
$posts = get_posts( array(
    'posts_per_page' => 10,
    'post_type' => 'post',
    'fields' => 'ids',  // Only get IDs if that's all you need
    'no_found_rows' => true,  // Skip pagination if not needed
    'update_post_meta_cache' => false,  // Skip meta if not needed
    'update_post_term_cache' => false   // Skip terms if not needed
) );
```

---

## 7. Trademark Restrictions

### ✅ Avoid Trademarked Terms in Plugin Slug

**Don't use these in your plugin folder name or slug:**

```
❌ Forbidden prefixes/names:
- wordpress-
- google-
- facebook-
- woocommerce-
- elementor-
- jetpack-
- gutenberg-
- contact-form-7-
- yoast-
- akismet-

✅ Allowed usage:
- for-woocommerce (suffix)
- my-google-integration (not prefix)
- facebook-connector (describe functionality)
```

### ✅ Plugin Naming Best Practices

```
❌ BAD:
- woocommerce-shipping
- facebook-login
- google-analytics

✅ GOOD:
- shipping-calculator-for-woocommerce
- social-login-with-facebook
- analytics-tracking-for-wordpress
```

---

## 8. Code Quality Standards

### ✅ No Deprecated Functions

```php
// ❌ BAD - Deprecated
get_settings( 'option_name' );  // Deprecated since WP 2.1
wp_specialchars( $text );       // Deprecated since WP 2.8

// ✅ GOOD - Current functions
get_option( 'option_name' );
esc_html( $text );
```

### ✅ Avoid Discouraged Functions

```php
// ❌ AVOID
query_posts();        // Use WP_Query or get_posts()
eval();              // Security risk
base64_decode();     // Suspicious (unless justified)
extract();           // Security risk

// ✅ USE
$query = new WP_Query( $args );
// Avoid eval entirely
// Base64 only for legitimate use cases with clear comments
// Don't use extract
```

### ✅ Proper Error Handling

```php
// ❌ BAD - Errors displayed
ini_set( 'display_errors', 1 );
error_reporting( E_ALL );

// ✅ GOOD - Errors logged
if ( WP_DEBUG ) {
    ini_set( 'log_errors', 1 );
    ini_set( 'display_errors', 0 );
}
```

### ✅ No HEREDOC/NOWDOC in Critical Code

```php
// ❌ AVOID - Makes code harder to parse
$html = <<<HTML
<div class="wrapper">
    <h1>Title</h1>
</div>
HTML;

// ✅ BETTER - Clear string concatenation
$html = '<div class="wrapper">';
$html .= '<h1>' . esc_html( $title ) . '</h1>';
$html .= '</div>';

// ✅ BEST - Template file
include plugin_dir_path( __FILE__ ) . 'templates/wrapper.php';
```

---

## 9. Settings and Options

### ✅ Sanitize Settings

```php
// ❌ BAD - No sanitization
register_setting( 'my_options', 'my_option' );

// ✅ GOOD - With sanitization
register_setting( 
    'my_options', 
    'my_option',
    array(
        'sanitize_callback' => 'sanitize_text_field',
        'default' => ''
    )
);

// ✅ BETTER - Custom sanitization
register_setting( 
    'my_options', 
    'my_option',
    array(
        'sanitize_callback' => 'my_plugin_sanitize_option',
        'default' => ''
    )
);

function my_plugin_sanitize_option( $value ) {
    // Custom validation
    if ( ! is_numeric( $value ) ) {
        add_settings_error(
            'my_option',
            'invalid_number',
            __( 'Please enter a valid number.', 'my-plugin' )
        );
        return get_option( 'my_option' );
    }
    return absint( $value );
}
```

---

## 10. Plugin Uninstall

### ✅ Provide Uninstall Handler

**Create `uninstall.php` to clean up on deletion:**

```php
// uninstall.php
<?php
// If uninstall not called from WordPress, exit
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

// Delete options
delete_option( 'my_plugin_option' );

// Delete post meta
delete_post_meta_by_key( 'my_plugin_meta' );

// Delete custom tables
global $wpdb;
$wpdb->query( "DROP TABLE IF EXISTS {$wpdb->prefix}my_plugin_table" );

// Clear scheduled hooks
wp_clear_scheduled_hook( 'my_plugin_cron' );
```

---

## 11. Testing Your Plugin

### Run Plugin Check

```bash
# Via WP-CLI
wp plugin check your-plugin-slug

# With runtime checks
wp plugin check your-plugin-slug --require=./wp-content/plugins/plugin-check/cli.php

# Check from URL
wp plugin check https://example.com/plugin.zip

# Specific categories
wp plugin check your-plugin-slug --categories=security,performance

# Ignore specific codes
wp plugin check your-plugin-slug --ignore-codes=textdomain_mismatch
```

### Categories to Check

```bash
# All categories
--categories=plugin_repo,security,performance,general,accessibility

# Required for WordPress.org
--categories=plugin_repo,security

# Performance only
--categories=performance
```

---

## 12. Quick Checklist

### Before Submission

- [ ] Plugin header complete with all required fields
- [ ] Valid GPL-compatible license
- [ ] Readme.txt with all required sections
- [ ] Text domain matches plugin slug
- [ ] No hardcoded localhost URLs
- [ ] All input validated and sanitized
- [ ] All output escaped
- [ ] Nonces on all forms and AJAX
- [ ] Capability checks on all actions
- [ ] Prepared statements for all database queries
- [ ] No code obfuscation
- [ ] No executable files (.exe, .sh, .phar)
- [ ] Scripts enqueued properly (not hardcoded)
- [ ] Scripts loaded in footer where possible
- [ ] Translations working (test with Loco Translate)
- [ ] No trademark violations in slug
- [ ] Uninstall.php removes all data
- [ ] Tested with WP_DEBUG enabled
- [ ] Run Plugin Check tool
- [ ] Cross-browser testing
- [ ] PHP 7.4+ compatibility
- [ ] WordPress 6.0+ compatibility

---

## 13. Common Error Codes and Fixes

### plugin_header_invalid_plugin_name
**Fix**: Use a descriptive name with at least 5 alphanumeric characters

### plugin_header_missing_plugin_description
**Fix**: Add a clear Description header

### plugin_header_no_license
**Fix**: Add `License: GPL v2 or later` header

### textdomain_mismatch
**Fix**: Ensure Text Domain matches your plugin slug

### no_plugin_readme
**Fix**: Create readme.txt in plugin root

### late_escaping
**Fix**: Escape all output with `esc_html()`, `esc_attr()`, etc.

### direct_db_query
**Fix**: Use WordPress functions or prepared statements

### localhost_found
**Fix**: Remove all localhost URLs from code

### code_obfuscation
**Fix**: Remove all encoded/obfuscated code

### trademark_violation
**Fix**: Rename plugin to avoid trademarked terms

### unfiltered_uploads
**Fix**: Remove `ALLOW_UNFILTERED_UPLOADS` constant

---

## 14. Resources

- **Plugin Check Tool**: [WordPress.org Plugin Check](https://wordpress.org/plugins/plugin-check/)
- **Plugin Guidelines**: [Plugin Review Guidelines](https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/)
- **Header Requirements**: [Plugin Header Requirements](https://developer.wordpress.org/plugins/plugin-basics/header-requirements/)
- **Readme Validator**: [WordPress.org Readme Validator](https://wordpress.org/plugins/developers/readme-validator/)
- **Security Handbook**: [Plugin Security](https://developer.wordpress.org/apis/security/)
- **Coding Standards**: [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/wordpress-coding-standards/)

---

## 🎯 Final Notes

Following this guide ensures your plugin will:
- ✅ Pass WordPress.org plugin review
- ✅ Follow security best practices
- ✅ Perform optimally
- ✅ Be maintainable and professional
- ✅ Never encounter common submission issues

**Remember**: Plugin Check is a tool to help you, not a perfect system. Some warnings may be acceptable with proper justification. Always focus on building secure, performant, and user-friendly plugins.

