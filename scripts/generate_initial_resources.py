#!/usr/bin/env python3
"""
Generate initial WordPress resource files
"""

import os
from pathlib import Path

RESOURCES_DIR = Path(__file__).parent.parent / "resources"

RESOURCES = {
    "security/escaping.md": """# WordPress Output Escaping

Escaping makes data safe for output by encoding special characters.

## When to Escape

**ALWAYS escape data when outputting to:**
- HTML
- HTML attributes
- JavaScript
- URLs
- SQL queries (use $wpdb->prepare instead)

## Core Escaping Functions

### HTML Context

```php
// Escape HTML output
echo esc_html( $text );

// Example
<h1><?php echo esc_html( $page_title ); ?></h1>
<p><?php echo esc_html( get_the_title() ); ?></p>
```

### HTML Attributes

```php
// Escape for attributes
echo '<div class="' . esc_attr( $class_name ) . '">';
echo '<input type="text" value="' . esc_attr( $value ) . '">';

// For data attributes
<div data-id="<?php echo esc_attr( $post_id ); ?>">
```

### URLs

```php
// Escape URL
<a href="<?php echo esc_url( $link ); ?>">Link</a>

// For use in code (raw)
$redirect = esc_url_raw( $_GET['redirect_to'] );
wp_redirect( $redirect );
```

### JavaScript

```php
// Escape for JS
<script>
var data = '<?php echo esc_js( $data ); ?>';
</script>

// Better: use wp_localize_script
wp_localize_script( 'my-script', 'myData', array(
    'value' => $data, // Auto-escaped
) );
```

### SQL (Use wpdb->prepare)

```php
// ❌ NEVER

$wpdb->query( "DELETE FROM table WHERE id = " . $id );

// ✅ ALWAYS
$wpdb->query( $wpdb->prepare(
    "DELETE FROM {$wpdb->prefix}table WHERE id = %d",
    $id
) );
```

### Translation with Escaping

```php
// Escape translated text
esc_html_e( 'Hello World', 'textdomain' );
esc_attr_e( 'Placeholder', 'textdomain' );

// Return escaped translated string
$text = esc_html__( 'Hello World', 'textdomain' );
$attr = esc_attr__( 'Placeholder', 'textdomain' );
```

## Advanced Escaping

### wp_kses (Allow Specific HTML)

```php
$allowed_html = array(
    'a' => array(
        'href' => array(),
        'title' => array(),
    ),
    'br' => array(),
    'strong' => array(),
);

echo wp_kses( $content, $allowed_html );

// For post content (allows standard post HTML)
echo wp_kses_post( $content );
```

### JSON Encoding

```php
<script>
var config = <?php echo wp_json_encode( $config_array ); ?>;
</script>
```

## Context-Specific Examples

### Form Output

```php
<form method="post">
    <?php wp_nonce_field( 'my_action', 'my_nonce' ); ?>
    
    <input type="text" 
           name="title" 
           value="<?php echo esc_attr( $title ); ?>" 
           placeholder="<?php esc_attr_e( 'Enter title', 'textdomain' ); ?>">
    
    <textarea name="content"><?php echo esc_textarea( $content ); ?></textarea>
    
    <select name="category">
        <?php foreach ( $categories as $cat_id => $cat_name ) : ?>
            <option value="<?php echo esc_attr( $cat_id ); ?>"
                    <?php selected( $selected_cat, $cat_id ); ?>>
                <?php echo esc_html( $cat_name ); ?>
            </option>
        <?php endforeach; ?>
    </select>
</form>
```

### Link Output

```php
<a href="<?php echo esc_url( $external_link ); ?>" 
   target="_blank"
   rel="noopener noreferrer">
    <?php echo esc_html( $link_text ); ?>
</a>
```

### Style Attributes

```php
<div style="background-color: <?php echo esc_attr( $color ); ?>; 
            width: <?php echo esc_attr( $width ); ?>px;">
```

## Best Practices

1. **Escape late** - Escape at output, not storage
2. **Use correct function** for context (HTML vs attribute vs URL)
3. **wp_kses for rich content** - Allow specific HTML safely
4. **Never trust user data** - Even from admins
5. **Escape translation strings** - Use esc_html__(), esc_attr__()
6. **Use wp_json_encode()** for JavaScript data
7. **Don't double-escape** - Escape once at output

## Quick Reference

| Context | Function | Example |
|---------|----------|---------|
| HTML | `esc_html()` | `<p><?php echo esc_html( $text ); ?></p>` |
| Attribute | `esc_attr()` | `<div class="<?php echo esc_attr( $class ); ?>">` |
| URL | `esc_url()` | `<a href="<?php echo esc_url( $link ); ?>">` |
| JavaScript | `esc_js()` | `var x = '<?php echo esc_js( $val ); ?>';` |
| Textarea | `esc_textarea()` | `<textarea><?php echo esc_textarea( $val ); ?></textarea>` |
| Rich HTML | `wp_kses_post()` | `<?php echo wp_kses_post( $content ); ?>` |
| SQL | `$wpdb->prepare()` | `$wpdb->prepare( "... %s", $val )` |

## Official Documentation

https://developer.wordpress.org/apis/security/escaping/
https://developer.wordpress.org/reference/functions/esc_html/
""",

    "security/nonces.md": """# WordPress Nonces

Nonces (Number Used Once) protect against CSRF attacks by verifying request intent.

## Creating Nonces

### Form Nonces

```php
// Create nonce field in form
<form method="post">
    <?php wp_nonce_field( 'my_action', 'my_nonce' ); ?>
    <!-- form fields -->
</form>
```

### URL Nonces

```php
// Add nonce to URL
$url = wp_nonce_url( 
    admin_url( 'admin.php?page=my-page&action=delete&id=' . $id ),
    'delete_item_' . $id
);

echo '<a href="' . esc_url( $url ) . '">Delete</a>';
```

### Get Nonce Value

```php
// Get nonce value directly
$nonce = wp_create_nonce( 'my_action' );

echo '<input type="hidden" name="my_nonce" value="' . esc_attr( $nonce ) . '">';
```

## Verifying Nonces

### Form Verification

```php
// Verify nonce from form
if ( ! isset( $_POST['my_nonce'] ) || 
     ! wp_verify_nonce( $_POST['my_nonce'], 'my_action' ) ) {
    wp_die( 'Security check failed' );
}

// Alternative (dies automatically on failure)
check_admin_referer( 'my_action', 'my_nonce' );
```

### URL Verification

```php
// Verify nonce from URL
if ( ! isset( $_GET['_wpnonce'] ) || 
     ! wp_verify_nonce( $_GET['_wpnonce'], 'delete_item_' . $id ) ) {
    wp_die( 'Security check failed' );
}

// Alternative
check_admin_referer( 'delete_item_' . $id );
```

## AJAX Nonces

### Creating AJAX Nonce

```php
// Localize script with nonce
wp_localize_script( 'my-ajax-script', 'myAjax', array(
    'ajax_url' => admin_url( 'admin-ajax.php' ),
    'nonce' => wp_create_nonce( 'my_ajax_action' ),
) );
```

### AJAX JavaScript

```javascript
jQuery.ajax({
    url: myAjax.ajax_url,
    type: 'POST',
    data: {
        action: 'my_ajax_action',
        nonce: myAjax.nonce,
        data: formData
    },
    success: function(response) {
        console.log(response);
    }
});
```

### Verify in AJAX Handler

```php
add_action( 'wp_ajax_my_ajax_action', 'handle_ajax_request' );

function handle_ajax_request() {
    // Verify nonce
    check_ajax_referer( 'my_ajax_action', 'nonce' );
    
    // Process request
    $result = array( 'success' => true );
    
    wp_send_json_success( $result );
}
```

## REST API Nonces

```php
// JavaScript
wp.apiFetch({
    path: '/wp/v2/posts',
    method: 'POST',
    data: {
        title: 'My Post',
        content: 'Content here'
    }
}).then(response => {
    console.log(response);
});

// Nonce is auto-added via wp_rest nonce in wp-api.js
```

## Complete Examples

### Meta Box with Nonce

```php
function add_custom_meta_box() {
    add_meta_box(
        'custom_meta',
        'Custom Meta',
        'render_custom_meta_box',
        'post'
    );
}
add_action( 'add_meta_boxes', 'add_custom_meta_box' );

function render_custom_meta_box( $post ) {
    // Create nonce
    wp_nonce_field( 'save_custom_meta', 'custom_meta_nonce' );
    
    $value = get_post_meta( $post->ID, 'custom_field', true );
    ?>
    <input type="text" name="custom_field" value="<?php echo esc_attr( $value ); ?>">
    <?php
}

function save_custom_meta( $post_id ) {
    // Verify nonce
    if ( ! isset( $_POST['custom_meta_nonce'] ) || 
         ! wp_verify_nonce( $_POST['custom_meta_nonce'], 'save_custom_meta' ) ) {
        return;
    }
    
    // Check autosave
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    
    // Check permissions
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }
    
    // Save data
    if ( isset( $_POST['custom_field'] ) ) {
        update_post_meta( $post_id, 'custom_field', 
            sanitize_text_field( $_POST['custom_field'] ) );
    }
}
add_action( 'save_post', 'save_custom_meta' );
```

### Settings Page with Nonce

```php
function render_settings_page() {
    ?>
    <div class="wrap">
        <h1>Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields( 'my_options_group' );
            do_settings_sections( 'my_options_page' );
            submit_button();
            ?>
        </form>
    </div>
    <?php
}

// settings_fields() automatically adds nonce
```

## Nonce Lifespan

- Default lifespan: 24 hours (2 nonce ticks of 12 hours each)
- Nonces are tied to: User ID, action name, and time
- Old nonces (previous tick) still work for grace period

## Best Practices

1. **Always use unique action names** - Be specific
2. **Verify before processing** - Check nonce first
3. **Use check_admin_referer()** for admin forms
4. **Use check_ajax_referer()** for AJAX
5. **Include user-specific data in action** for unique items
6. **Don't expose nonces** in public content
7. **Combine with capability checks** - Nonces aren't permission checks

## Common Patterns

```php
// Admin form processing
if ( isset( $_POST['submit'] ) ) {
    check_admin_referer( 'my_action', 'my_nonce' );
    
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'Unauthorized' );
    }
    
    // Process form
}

// AJAX handler
function my_ajax_handler() {
    check_ajax_referer( 'my_ajax_nonce', 'nonce' );
    
    // Process AJAX request
    wp_send_json_success( $data );
}
```

## Security Checklist

- [ ] Use unique, descriptive action names
- [ ] Create nonce: `wp_nonce_field()` or `wp_create_nonce()`
- [ ] Verify nonce: `wp_verify_nonce()` or `check_*_referer()`
- [ ] Verify BEFORE processing data
- [ ] Check user capabilities too
- [ ] Use `check_ajax_referer()` for AJAX
- [ ] Don't cache pages with nonces
- [ ] Handle nonce failures gracefully

## Official Documentation

https://developer.wordpress.org/apis/security/nonces/
https://developer.wordpress.org/reference/functions/wp_nonce_field/
""",

    "security/capabilities.md": """# WordPress User Capabilities

Capabilities control what users can do in WordPress.

## Checking Capabilities

```php
// Check if current user has capability
if ( current_user_can( 'edit_posts' ) ) {
    // User can edit posts
}

// Check specific post
if ( current_user_can( 'edit_post', $post_id ) ) {
    // User can edit this specific post
}

// Check for specific user
if ( user_can( $user_id, 'publish_posts' ) ) {
    // User can publish posts
}
```

## Common Capabilities

### Content Management
- `edit_posts` - Edit own posts
- `edit_others_posts` - Edit others' posts
- `publish_posts` - Publish posts
- `delete_posts` - Delete own posts
- `delete_others_posts` - Delete others' posts
- `edit_published_posts` - Edit published posts
- `edit_pages` - Edit pages
- `edit_others_pages` - Edit others' pages

### Administration
- `manage_options` - Manage settings
- `manage_categories` - Manage categories
- `manage_links` - Manage links
- `upload_files` - Upload files
- `import` - Import content
- `unfiltered_html` - Post unfiltered HTML

### Users
- `list_users` - List users
- `edit_users` - Edit users
- `create_users` - Create users
- `delete_users` - Delete users
- `promote_users` - Change user roles

### Plugins & Themes
- `activate_plugins` - Activate plugins
- `edit_plugins` - Edit plugin files
- `install_plugins` - Install plugins
- `update_plugins` - Update plugins
- `delete_plugins` - Delete plugins
- `switch_themes` - Switch themes
- `edit_themes` - Edit theme files
- `install_themes` - Install themes

## Default Roles & Capabilities

### Super Admin (Multisite)
- All capabilities

### Administrator
- All capabilities on single site

### Editor
- Edit/publish/delete posts and pages (own and others)
- Moderate comments
- Manage categories, tags, links
- Upload files

### Author
- Edit/publish/delete own posts
- Upload files

### Contributor
- Edit/delete own posts (unpublished)
- Cannot publish or upload files

### Subscriber
- Read content
- Edit own profile

## Custom Capabilities

### Add Capability to Role

```php
// Get role
$role = get_role( 'editor' );

// Add capability
$role->add_cap( 'manage_custom_data' );

// Remove capability
$role->remove_cap( 'manage_custom_data' );
```

### Create Custom Role

```php
add_role(
    'custom_role',
    'Custom Role',
    array(
        'read' => true,
        'edit_posts' => true,
        'delete_posts' => false,
        'publish_posts' => false,
        'upload_files' => true,
        'manage_custom_data' => true, // Custom capability
    )
);
```

### Remove Custom Role

```php
remove_role( 'custom_role' );
```

## Capability Checking in Code

### Meta Box Example

```php
function add_custom_meta_box() {
    // Only show to users who can edit posts
    if ( current_user_can( 'edit_posts' ) ) {
        add_meta_box( /* ... */ );
    }
}
```

### Menu Item Example

```php
add_menu_page(
    'Custom Page',
    'Custom Menu',
    'manage_options',  // Capability required
    'custom-page',
    'render_custom_page'
);
```

### AJAX Handler Example

```php
function handle_ajax_request() {
    check_ajax_referer( 'my_nonce' );
    
    // Check capability
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_send_json_error( 'Insufficient permissions' );
    }
    
    // Process request
    wp_send_json_success( $data );
}
```

### REST API Example

```php
register_rest_route( 'myplugin/v1', '/data', array(
    'methods'  => 'POST',
    'callback' => 'create_data',
    'permission_callback' => function() {
        return current_user_can( 'edit_posts' );
    },
) );
```

## Map Meta Capabilities

```php
// Map custom capability to existing capabilities
function map_custom_capabilities( $caps, $cap, $user_id, $args ) {
    if ( 'edit_custom_item' === $cap ) {
        // Get the item
        $item_id = isset( $args[0] ) ? $args[0] : 0;
        $item = get_post( $item_id );
        
        if ( ! $item ) {
            $caps[] = 'do_not_allow';
        } elseif ( $item->post_author == $user_id ) {
            $caps[] = 'edit_posts';
        } else {
            $caps[] = 'edit_others_posts';
        }
    }
    
    return $caps;
}
add_filter( 'map_meta_cap', 'map_custom_capabilities', 10, 4 );

// Now you can use:
if ( current_user_can( 'edit_custom_item', $item_id ) ) {
    // User can edit this item
}
```

## Best Practices

1. **Always check capabilities** before sensitive operations
2. **Use specific capabilities** (not just 'administrator')
3. **Check early** - Before processing data
4. **Combine with nonce verification**
5. **Use map_meta_cap** for complex permission logic
6. **Don't hardcode role names** - Check capabilities instead
7. **Provide clear error messages** for denied access

## Security Pattern

```php
function process_admin_action() {
    // 1. Verify nonce
    check_admin_referer( 'my_action', 'my_nonce' );
    
    // 2. Check capability
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'You do not have permission to perform this action.' );
    }
    
    // 3. Validate input
    $value = isset( $_POST['value'] ) ? sanitize_text_field( $_POST['value'] ) : '';
    
    if ( empty( $value ) ) {
        wp_die( 'Invalid input.' );
    }
    
    // 4. Process action
    update_option( 'my_option', $value );
    
    // 5. Redirect
    wp_redirect( admin_url( 'admin.php?page=my-page&updated=true' ) );
    exit;
}
```

## Checking Capabilities Checklist

- [ ] Verify nonce first
- [ ] Check capability before processing
- [ ] Use specific capabilities, not roles
- [ ] Check capability on specific items when relevant
- [ ] Provide meaningful error messages
- [ ] Log unauthorized access attempts
- [ ] Don't expose capability checks in client-side code

## Official Documentation

https://wordpress.org/documentation/article/roles-and-capabilities/
https://developer.wordpress.org/reference/functions/current_user_can/
https://developer.wordpress.org/apis/security/user-capabilities/
""",
}

# Create resources
for filepath, content in RESOURCES.items():
    full_path = RESOURCES_DIR / filepath
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip())
    print(f"Created: {filepath}")

print(f"\\nGenerated {len(RESOURCES)} resource files")
