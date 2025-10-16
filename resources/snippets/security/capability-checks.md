---
difficulty: Beginner
tags: [security, capabilities, permissions, authorization]
related: [security/nonces, admin/add-admin-page]
use_case: Checking user permissions before actions
---

# Capability Checks

```php
// Check if user can edit posts
if ( current_user_can( 'edit_posts' ) ) {
    // Allow action
}

// Check if user can manage options
if ( current_user_can( 'manage_options' ) ) {
    // Admin-only action
}

// Check specific post
if ( current_user_can( 'edit_post', $post_id ) ) {
    // Edit this specific post
}

// Check custom capability
if ( current_user_can( 'edit_products' ) ) {
    // Custom capability
}

// Die if no capability
if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( __( 'You do not have sufficient permissions', 'textdomain' ) );
}
```
