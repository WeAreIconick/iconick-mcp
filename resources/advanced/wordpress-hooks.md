# WordPress Hooks System

## Understanding WordPress Hooks

WordPress hooks allow you to modify or extend functionality without editing core files. There are two types:

1. **Actions** - Execute code at specific points
2. **Filters** - Modify data before it's used

## Common Action Hooks

### Post Actions
```php
// After post is published
add_action('publish_post', 'send_notification_email');
function send_notification_email($post_id) {
    $post = get_post($post_id);
    $author = get_userdata($post->post_author);
    
    wp_mail(
        $author->user_email,
        'Post Published',
        'Your post "' . $post->post_title . '" has been published.'
    );
}

// Before post is deleted
add_action('before_delete_post', 'backup_post_before_delete');
function backup_post_before_delete($post_id) {
    $post = get_post($post_id);
    // Create backup logic here
}

// After post is saved
add_action('save_post', 'update_post_meta_on_save');
function update_post_meta_on_save($post_id) {
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }
    
    if (!current_user_can('edit_post', $post_id)) {
        return;
    }
    
    // Update custom meta fields
    if (isset($_POST['custom_field'])) {
        update_post_meta($post_id, '_custom_field', sanitize_text_field($_POST['custom_field']));
    }
}
```

### User Actions
```php
// After user registration
add_action('user_register', 'send_welcome_email');
function send_welcome_email($user_id) {
    $user = get_userdata($user_id);
    
    wp_mail(
        $user->user_email,
        'Welcome!',
        'Welcome to our site, ' . $user->display_name . '!'
    );
}

// After user login
add_action('wp_login', 'log_user_login', 10, 2);
function log_user_login($user_login, $user) {
    update_user_meta($user->ID, 'last_login', current_time('mysql'));
}

// Before user logout
add_action('wp_logout', 'clear_user_session_data');
function clear_user_session_data() {
    // Clear any temporary user data
}
```

### Admin Actions
```php
// Add custom admin menu
add_action('admin_menu', 'add_custom_admin_menu');
function add_custom_admin_menu() {
    add_menu_page(
        'Custom Page',
        'Custom Menu',
        'manage_options',
        'custom-page',
        'custom_admin_page_callback',
        'dashicons-admin-tools',
        30
    );
}

// Add admin notices
add_action('admin_notices', 'display_admin_notices');
function display_admin_notices() {
    if (get_option('show_custom_notice')) {
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p>This is a custom admin notice!</p>';
        echo '</div>';
    }
}

// Add admin footer text
add_action('admin_footer_text', 'custom_admin_footer');
function custom_admin_footer($text) {
    return 'Custom footer text';
}
```

## Common Filter Hooks

### Content Filters
```php
// Modify post content
add_filter('the_content', 'add_custom_content_to_posts');
function add_custom_content_to_posts($content) {
    if (is_single() && get_post_type() === 'post') {
        $custom_content = '<div class="custom-content">Custom content here</div>';
        $content .= $custom_content;
    }
    return $content;
}

// Modify post title
add_filter('the_title', 'modify_post_title');
function modify_post_title($title) {
    if (is_single()) {
        $title = '📖 ' . $title;
    }
    return $title;
}

// Modify excerpt length
add_filter('excerpt_length', 'custom_excerpt_length');
function custom_excerpt_length($length) {
    return 30; // 30 words
}

// Modify excerpt more text
add_filter('excerpt_more', 'custom_excerpt_more');
function custom_excerpt_more($more) {
    return '... <a href="' . get_permalink() . '">Read more</a>';
}
```

### Query Filters
```php
// Modify main query
add_action('pre_get_posts', 'modify_main_query');
function modify_main_query($query) {
    if (!is_admin() && $query->is_main_query()) {
        if (is_home()) {
            $query->set('posts_per_page', 5);
            $query->set('post_type', array('post', 'custom_post_type'));
        }
    }
}

// Modify post query args
add_filter('posts_where', 'modify_posts_where');
function modify_posts_where($where) {
    if (is_admin()) {
        return $where;
    }
    
    // Add custom WHERE clause
    $where .= " AND post_title NOT LIKE '%spam%'";
    return $where;
}

// Modify post query order
add_filter('posts_orderby', 'modify_posts_orderby');
function modify_posts_orderby($orderby) {
    if (is_home()) {
        $orderby = 'post_date DESC, post_title ASC';
    }
    return $orderby;
}
```

## Custom Hooks

### Creating Custom Actions
```php
// Define custom action
function process_custom_data($data) {
    // Do some processing
    $processed_data = sanitize_text_field($data);
    
    // Fire custom action
    do_action('custom_data_processed', $processed_data, $data);
    
    return $processed_data;
}

// Use custom action
add_action('custom_data_processed', 'log_custom_data_processing', 10, 2);
function log_custom_data_processing($processed_data, $original_data) {
    error_log('Custom data processed: ' . $original_data . ' -> ' . $processed_data);
}

add_action('custom_data_processed', 'send_custom_data_notification');
function send_custom_data_notification($processed_data) {
    // Send notification logic
}
```

### Creating Custom Filters
```php
// Define custom filter
function get_custom_data($data) {
    // Apply custom filters
    $filtered_data = apply_filters('custom_data_filter', $data);
    
    return $filtered_data;
}

// Use custom filter
add_filter('custom_data_filter', 'add_custom_prefix');
function add_custom_prefix($data) {
    return 'CUSTOM: ' . $data;
}

add_filter('custom_data_filter', 'add_timestamp', 20);
function add_timestamp($data) {
    return $data . ' [' . current_time('Y-m-d H:i:s') . ']';
}
```

## Hook Priority and Arguments

### Priority System
```php
// Default priority is 10
add_action('init', 'function_one'); // Priority 10
add_action('init', 'function_two', 5); // Priority 5 (runs first)
add_action('init', 'function_three', 15); // Priority 15 (runs last)
add_action('init', 'function_four', 10, 2); // Priority 10, 2 arguments
```

### Multiple Arguments
```php
// Action with multiple arguments
add_action('save_post', 'save_post_with_arguments', 10, 3);
function save_post_with_arguments($post_id, $post, $update) {
    if ($update) {
        // Post was updated
        error_log('Post updated: ' . $post->post_title);
    } else {
        // Post was created
        error_log('Post created: ' . $post->post_title);
    }
}

// Filter with multiple arguments
add_filter('post_link', 'modify_post_link', 10, 3);
function modify_post_link($post_link, $post, $leavename) {
    if ($post->post_type === 'custom_post_type') {
        $post_link = home_url('/custom/' . $post->post_name . '/');
    }
    return $post_link;
}
```

## Advanced Hook Usage

### Conditional Hooks
```php
// Only run on specific pages
add_action('wp_head', 'add_custom_meta_tags');
function add_custom_meta_tags() {
    if (is_single() && get_post_type() === 'product') {
        $product_price = get_post_meta(get_the_ID(), '_product_price', true);
        if ($product_price) {
            echo '<meta property="product:price" content="' . esc_attr($product_price) . '">';
        }
    }
}

// Only run for specific user roles
add_action('admin_init', 'add_custom_capabilities');
function add_custom_capabilities() {
    if (current_user_can('manage_options')) {
        // Add custom capabilities
    }
}
```

### Hook Removal
```php
// Remove default hooks
remove_action('wp_head', 'wp_generator');
remove_filter('the_content', 'wpautop');

// Remove hooks with priority
remove_action('save_post', 'save_post_function', 10);

// Remove all hooks for a specific action
remove_all_actions('wp_footer');

// Check if hook exists before removing
if (has_action('wp_head', 'some_function')) {
    remove_action('wp_head', 'some_function');
}
```

## Best Practices

1. **Use descriptive function names** for hook callbacks
2. **Always check conditions** before executing hook code
3. **Use proper priority** to control execution order
4. **Sanitize and validate** data in hooks
5. **Use nonces** for security in admin hooks
6. **Remove hooks** when no longer needed
7. **Document custom hooks** for other developers
8. **Test hooks thoroughly** in different scenarios
9. **Use conditional logic** to prevent conflicts
10. **Follow WordPress coding standards**

## Resources

- [WordPress Plugin API Documentation](https://developer.wordpress.org/plugins/hooks/)
- [Action Reference](https://codex.wordpress.org/Plugin_API/Action_Reference)
- [Filter Reference](https://codex.wordpress.org/Plugin_API/Filter_Reference)
- [Hook Priority Documentation](https://developer.wordpress.org/plugins/hooks/priority/)