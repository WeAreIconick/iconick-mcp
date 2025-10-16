---
difficulty: Intermediate
tags: [security, capabilities, permissions, roles]
related: [security/user-roles, security/data-validation]
wp_version: 2.0+
---

# WordPress User Capabilities

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