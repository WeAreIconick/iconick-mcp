# WordPress Multisite Development

Comprehensive guide to WordPress Multisite development, administration, and customization.

## Multisite Fundamentals

### Understanding WordPress Multisite

```php
// Check if site is multisite
if (is_multisite()) {
    // Multisite-specific code
    $current_site = get_current_site();
    $current_blog = get_current_blog_id();
    
    echo "Current site: " . $current_site->domain;
    echo "Current blog ID: " . $current_blog;
}

// Get site information
function get_site_info() {
    if (!is_multisite()) {
        return false;
    }
    
    $site_info = array(
        'site_id' => get_current_blog_id(),
        'site_url' => get_site_url(),
        'site_name' => get_bloginfo('name'),
        'admin_email' => get_option('admin_email'),
        'is_main_site' => is_main_site(),
        'is_subdomain_install' => is_subdomain_install(),
        'network_site_url' => network_site_url(),
        'network_admin_url' => network_admin_url()
    );
    
    return $site_info;
}
```

### Multisite Database Structure

```sql
-- WordPress Multisite Database Tables

-- Network-wide tables
wp_blogs          -- All sites in the network
wp_blog_versions  -- Site versions
wp_registration_log -- User registrations
wp_signups        -- Pending site/user signups
wp_site           -- Network information
wp_sitemeta       -- Network options

-- Site-specific tables (wp_2_, wp_3_, etc.)
wp_2_posts        -- Posts for site ID 2
wp_2_posts_meta   -- Post meta for site ID 2
wp_2_users        -- Users for site ID 2
wp_2_usermeta     -- User meta for site ID 2
```

```php
// Working with multisite database tables
function get_network_sites($args = array()) {
    global $wpdb;
    
    $defaults = array(
        'public' => 1,
        'archived' => 0,
        'deleted' => 0,
        'spam' => 0
    );
    
    $args = wp_parse_args($args, $defaults);
    
    $where = "WHERE public = %d AND archived = %d AND deleted = %d AND spam = %d";
    $values = array($args['public'], $args['archived'], $args['deleted'], $args['spam']);
    
    $sites = $wpdb->get_results(
        $wpdb->prepare(
            "SELECT blog_id, domain, path, registered, last_updated 
             FROM {$wpdb->blogs} $where 
             ORDER BY registered DESC",
            $values
        )
    );
    
    return $sites;
}

// Get site-specific data
function get_site_data($blog_id) {
    global $wpdb;
    
    $table_prefix = $wpdb->get_blog_prefix($blog_id);
    
    $site_data = $wpdb->get_row(
        $wpdb->prepare(
            "SELECT option_name, option_value 
             FROM {$table_prefix}options 
             WHERE option_name IN ('blogname', 'blogdescription', 'admin_email', 'users_can_register')"
        )
    );
    
    return $site_data;
}
```

## Site Management

### Creating and Managing Sites

```php
// Create a new site programmatically
function create_new_site($domain, $path, $title, $admin_email, $options = array()) {
    if (!current_user_can('manage_sites')) {
        return new WP_Error('insufficient_permissions', 'You do not have permission to create sites.');
    }
    
    $defaults = array(
        'public' => 1,
        'archived' => 0,
        'deleted' => 0,
        'spam' => 0,
        'lang_id' => 0
    );
    
    $options = wp_parse_args($options, $defaults);
    
    // Validate domain and path
    if (empty($domain) || empty($path)) {
        return new WP_Error('invalid_domain_path', 'Domain and path are required.');
    }
    
    // Check if domain/path combination already exists
    $existing_site = get_id_from_blogname($domain . $path);
    if ($existing_site) {
        return new WP_Error('site_exists', 'A site with this domain and path already exists.');
    }
    
    // Create the site
    $site_id = wpmu_create_blog($domain, $path, $title, $admin_email, $options);
    
    if (is_wp_error($site_id)) {
        return $site_id;
    }
    
    // Switch to the new site and configure it
    switch_to_blog($site_id);
    
    // Set default options
    update_option('blogdescription', 'Just another WordPress site');
    update_option('users_can_register', 0);
    update_option('default_role', 'subscriber');
    
    // Install default theme if specified
    if (!empty($options['theme'])) {
        switch_theme($options['theme']);
    }
    
    // Create default pages
    create_default_pages();
    
    restore_current_blog();
    
    return $site_id;
}

// Create default pages for new sites
function create_default_pages() {
    $pages = array(
        'Home' => array(
            'post_content' => 'Welcome to your new site!',
            'post_status' => 'publish',
            'post_type' => 'page'
        ),
        'About' => array(
            'post_content' => 'This is an about page.',
            'post_status' => 'publish',
            'post_type' => 'page'
        ),
        'Contact' => array(
            'post_content' => 'Contact us here.',
            'post_status' => 'publish',
            'post_type' => 'page'
        )
    );
    
    foreach ($pages as $title => $page_data) {
        $page_data['post_title'] = $title;
        wp_insert_post($page_data);
    }
}
```

### Site Switching and Context

```php
// Switch between sites
function perform_multisite_operation() {
    // Get all sites
    $sites = get_sites();
    
    foreach ($sites as $site) {
        switch_to_blog($site->blog_id);
        
        // Perform operations on current site
        $post_count = wp_count_posts();
        $user_count = count_users();
        
        echo "Site: " . get_bloginfo('name') . "\n";
        echo "Posts: " . $post_count->publish . "\n";
        echo "Users: " . $user_count['total_users'] . "\n";
        
        // Restore original site context
        restore_current_blog();
    }
}

// Get data from multiple sites
function get_network_wide_stats() {
    $stats = array(
        'total_sites' => 0,
        'total_posts' => 0,
        'total_users' => 0,
        'sites_data' => array()
    );
    
    $sites = get_sites();
    $stats['total_sites'] = count($sites);
    
    foreach ($sites as $site) {
        switch_to_blog($site->blog_id);
        
        $post_count = wp_count_posts();
        $user_count = count_users();
        
        $site_data = array(
            'blog_id' => $site->blog_id,
            'name' => get_bloginfo('name'),
            'url' => get_site_url(),
            'posts' => $post_count->publish,
            'users' => $user_count['total_users']
        );
        
        $stats['total_posts'] += $post_count->publish;
        $stats['total_users'] += $user_count['total_users'];
        $stats['sites_data'][] = $site_data;
        
        restore_current_blog();
    }
    
    return $stats;
}
```

## User Management

### Network User Management

```php
// Add user to network
function add_user_to_network($user_email, $username = '', $password = '', $site_id = 0) {
    if (empty($username)) {
        $username = sanitize_user(substr($user_email, 0, strpos($user_email, '@')));
    }
    
    if (empty($password)) {
        $password = wp_generate_password();
    }
    
    // Create user if doesn't exist
    $user_id = username_exists($username);
    if (!$user_id) {
        $user_id = wp_create_user($username, $password, $user_email);
        
        if (is_wp_error($user_id)) {
            return $user_id;
        }
    }
    
    // Add user to specific site if specified
    if ($site_id > 0) {
        $added = add_user_to_blog($site_id, $user_id, 'subscriber');
        
        if (is_wp_error($added)) {
            return $added;
        }
    }
    
    return $user_id;
}

// Get user's sites
function get_user_sites($user_id) {
    $user_blogs = get_blogs_of_user($user_id);
    
    $sites = array();
    foreach ($user_blogs as $blog_id => $blog) {
        switch_to_blog($blog_id);
        
        $user_role = get_user_role($user_id);
        
        $sites[] = array(
            'blog_id' => $blog_id,
            'name' => $blog->blogname,
            'url' => $blog->siteurl,
            'role' => $user_role
        );
        
        restore_current_blog();
    }
    
    return $sites;
}

// Get user role on current site
function get_user_role($user_id) {
    $user = get_userdata($user_id);
    $roles = $user->roles;
    
    return !empty($roles) ? $roles[0] : 'no-role';
}
```

### User Registration and Signup

```php
// Custom user signup process
function custom_user_signup($user_login, $user_email, $errors) {
    // Validate signup data
    if (empty($user_login)) {
        $errors->add('empty_username', 'Username is required.');
    }
    
    if (empty($user_email)) {
        $errors->add('empty_email', 'Email is required.');
    }
    
    if (!is_email($user_email)) {
        $errors->add('invalid_email', 'Please enter a valid email address.');
    }
    
    if (username_exists($user_login)) {
        $errors->add('username_exists', 'Username already exists.');
    }
    
    if (email_exists($user_email)) {
        $errors->add('email_exists', 'Email already exists.');
    }
    
    // Custom validation
    if (strlen($user_login) < 3) {
        $errors->add('username_too_short', 'Username must be at least 3 characters long.');
    }
    
    // If no errors, proceed with signup
    if (!$errors->get_error_codes()) {
        $result = wpmu_signup_user($user_login, $user_email);
        
        if (is_wp_error($result)) {
            $errors->merge_from($result);
        } else {
            // Send confirmation email
            send_confirmation_email($user_login, $user_email);
        }
    }
    
    return $errors;
}

// Send confirmation email
function send_confirmation_email($user_login, $user_email) {
    $activation_key = get_user_meta(get_user_by('login', $user_login)->ID, 'activation_key', true);
    $activation_url = network_site_url("wp-activate.php?key=$activation_key");
    
    $subject = 'Activate your account';
    $message = "Please click the link below to activate your account:\n\n$activation_url";
    
    wp_mail($user_email, $subject, $message);
}
```

## Theme and Plugin Management

### Network-Wide Themes and Plugins

```php
// Activate theme network-wide
function activate_theme_network_wide($theme_slug) {
    if (!current_user_can('manage_network_themes')) {
        return new WP_Error('insufficient_permissions', 'You do not have permission to manage network themes.');
    }
    
    // Get all sites
    $sites = get_sites();
    $results = array();
    
    foreach ($sites as $site) {
        switch_to_blog($site->blog_id);
        
        // Check if theme is available
        $available_themes = wp_get_themes();
        
        if (isset($available_themes[$theme_slug])) {
            $activated = switch_theme($theme_slug);
            
            $results[] = array(
                'site_id' => $site->blog_id,
                'site_name' => get_bloginfo('name'),
                'success' => !is_wp_error($activated),
                'message' => is_wp_error($activated) ? $activated->get_error_message() : 'Theme activated successfully'
            );
        } else {
            $results[] = array(
                'site_id' => $site->blog_id,
                'site_name' => get_bloginfo('name'),
                'success' => false,
                'message' => 'Theme not available'
            );
        }
        
        restore_current_blog();
    }
    
    return $results;
}

// Install plugin network-wide
function install_plugin_network_wide($plugin_file) {
    if (!current_user_can('manage_network_plugins')) {
        return new WP_Error('insufficient_permissions', 'You do not have permission to manage network plugins.');
    }
    
    // Include required files
    if (!function_exists('download_url')) {
        require_once ABSPATH . 'wp-admin/includes/file.php';
    }
    
    if (!function_exists('install_plugin')) {
        require_once ABSPATH . 'wp-admin/includes/plugin-install.php';
        require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
    }
    
    // Install plugin
    $upgrader = new Plugin_Upgrader();
    $result = $upgrader->install($plugin_file);
    
    if (is_wp_error($result)) {
        return $result;
    }
    
    // Activate plugin network-wide if successful
    if ($result === true) {
        $plugin_slug = dirname($plugin_file);
        activate_plugin_network_wide($plugin_slug . '/' . basename($plugin_file));
    }
    
    return $result;
}

// Activate plugin network-wide
function activate_plugin_network_wide($plugin_file) {
    $sites = get_sites();
    $results = array();
    
    foreach ($sites as $site) {
        switch_to_blog($site->blog_id);
        
        $activated = activate_plugin($plugin_file);
        
        $results[] = array(
            'site_id' => $site->blog_id,
            'site_name' => get_bloginfo('name'),
            'success' => !is_wp_error($activated),
            'message' => is_wp_error($activated) ? $activated->get_error_message() : 'Plugin activated successfully'
        );
        
        restore_current_blog();
    }
    
    return $results;
}
```

## Network Administration

### Custom Network Admin Pages

```php
// Add custom network admin menu
function add_custom_network_admin_menu() {
    add_menu_page(
        'Network Dashboard',
        'Network Dashboard',
        'manage_network',
        'network-dashboard',
        'network_dashboard_page',
        'dashicons-dashboard',
        1
    );
    
    add_submenu_page(
        'network-dashboard',
        'Site Management',
        'Site Management',
        'manage_sites',
        'site-management',
        'site_management_page'
    );
    
    add_submenu_page(
        'network-dashboard',
        'User Management',
        'User Management',
        'manage_network_users',
        'user-management',
        'user_management_page'
    );
}

add_action('network_admin_menu', 'add_custom_network_admin_menu');

// Network dashboard page
function network_dashboard_page() {
    if (!current_user_can('manage_network')) {
        wp_die('You do not have permission to access this page.');
    }
    
    $stats = get_network_wide_stats();
    ?>
    <div class="wrap">
        <h1>Network Dashboard</h1>
        
        <div class="network-stats">
            <div class="stat-box">
                <h3>Total Sites</h3>
                <p class="stat-number"><?php echo $stats['total_sites']; ?></p>
            </div>
            
            <div class="stat-box">
                <h3>Total Posts</h3>
                <p class="stat-number"><?php echo $stats['total_posts']; ?></p>
            </div>
            
            <div class="stat-box">
                <h3>Total Users</h3>
                <p class="stat-number"><?php echo $stats['total_users']; ?></p>
            </div>
        </div>
        
        <h2>Recent Sites</h2>
        <table class="wp-list-table widefat fixed striped">
            <thead>
                <tr>
                    <th>Site Name</th>
                    <th>URL</th>
                    <th>Posts</th>
                    <th>Users</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($stats['sites_data'] as $site): ?>
                <tr>
                    <td><?php echo esc_html($site['name']); ?></td>
                    <td><a href="<?php echo esc_url($site['url']); ?>" target="_blank"><?php echo esc_url($site['url']); ?></a></td>
                    <td><?php echo $site['posts']; ?></td>
                    <td><?php echo $site['users']; ?></td>
                    <td>
                        <a href="<?php echo network_admin_url('site-info.php?id=' . $site['blog_id']); ?>">Edit</a>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
    
    <style>
    .network-stats {
        display: flex;
        gap: 20px;
        margin: 20px 0;
    }
    
    .stat-box {
        background: #fff;
        border: 1px solid #ccd0d4;
        border-radius: 4px;
        padding: 20px;
        text-align: center;
        flex: 1;
    }
    
    .stat-number {
        font-size: 2em;
        font-weight: bold;
        color: #0073aa;
        margin: 10px 0 0 0;
    }
    </style>
    <?php
}
```

### Network Settings Management

```php
// Add custom network settings
function add_custom_network_settings() {
    add_settings_section(
        'custom_network_settings',
        'Custom Network Settings',
        'custom_network_settings_section_callback',
        'network_settings'
    );
    
    add_settings_field(
        'default_site_theme',
        'Default Site Theme',
        'default_site_theme_field_callback',
        'network_settings',
        'custom_network_settings'
    );
    
    add_settings_field(
        'allowed_file_types',
        'Allowed File Types',
        'allowed_file_types_field_callback',
        'network_settings',
        'custom_network_settings'
    );
    
    register_setting('network_settings', 'default_site_theme');
    register_setting('network_settings', 'allowed_file_types');
}

add_action('network_admin_menu', 'add_custom_network_settings');

function custom_network_settings_section_callback() {
    echo '<p>Configure custom settings for your network.</p>';
}

function default_site_theme_field_callback() {
    $default_theme = get_site_option('default_site_theme', '');
    $themes = wp_get_themes();
    
    echo '<select name="default_site_theme">';
    echo '<option value="">Select a theme</option>';
    
    foreach ($themes as $theme_slug => $theme) {
        $selected = selected($default_theme, $theme_slug, false);
        echo "<option value='$theme_slug' $selected>" . $theme->get('Name') . "</option>";
    }
    
    echo '</select>';
    echo '<p class="description">Theme to assign to new sites by default.</p>';
}

function allowed_file_types_field_callback() {
    $allowed_types = get_site_option('allowed_file_types', array('jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx'));
    
    $file_types = array(
        'jpg' => 'JPEG Images',
        'jpeg' => 'JPEG Images',
        'png' => 'PNG Images',
        'gif' => 'GIF Images',
        'pdf' => 'PDF Documents',
        'doc' => 'Word Documents',
        'docx' => 'Word Documents (DOCX)',
        'xls' => 'Excel Spreadsheets',
        'xlsx' => 'Excel Spreadsheets (XLSX)',
        'zip' => 'ZIP Archives'
    );
    
    echo '<fieldset>';
    
    foreach ($file_types as $extension => $description) {
        $checked = checked(in_array($extension, $allowed_types), true, false);
        echo "<label><input type='checkbox' name='allowed_file_types[]' value='$extension' $checked> $description ($extension)</label><br>";
    }
    
    echo '</fieldset>';
    echo '<p class="description">File types allowed for upload across the network.</p>';
}
```

## Content Management

### Cross-Site Content Operations

```php
// Copy content between sites
function copy_content_between_sites($source_site_id, $target_site_id, $post_ids) {
    switch_to_blog($source_site_id);
    
    $copied_posts = array();
    
    foreach ($post_ids as $post_id) {
        $post = get_post($post_id);
        
        if (!$post) {
            continue;
        }
        
        $post_data = array(
            'post_title' => $post->post_title,
            'post_content' => $post->post_content,
            'post_excerpt' => $post->post_excerpt,
            'post_status' => $post->post_status,
            'post_type' => $post->post_type,
            'post_author' => get_current_user_id(),
            'post_date' => current_time('mysql')
        );
        
        // Get post meta
        $meta_data = get_post_meta($post_id);
        
        // Get featured image
        $featured_image_id = get_post_thumbnail_id($post_id);
        
        restore_current_blog();
        
        // Switch to target site
        switch_to_blog($target_site_id);
        
        // Insert post
        $new_post_id = wp_insert_post($post_data);
        
        if ($new_post_id) {
            // Copy meta data
            foreach ($meta_data as $meta_key => $meta_values) {
                foreach ($meta_values as $meta_value) {
                    add_post_meta($new_post_id, $meta_key, maybe_unserialize($meta_value));
                }
            }
            
            // Copy featured image
            if ($featured_image_id) {
                copy_featured_image($featured_image_id, $new_post_id, $source_site_id);
            }
            
            $copied_posts[] = $new_post_id;
        }
        
        restore_current_blog();
        
        // Switch back to source site for next iteration
        switch_to_blog($source_site_id);
    }
    
    restore_current_blog();
    
    return $copied_posts;
}

// Copy featured image between sites
function copy_featured_image($image_id, $target_post_id, $source_site_id) {
    switch_to_blog($source_site_id);
    
    $image_url = wp_get_attachment_url($image_id);
    $image_alt = get_post_meta($image_id, '_wp_attachment_image_alt', true);
    
    restore_current_blog();
    
    // Switch to target site
    switch_to_blog(get_current_blog_id());
    
    // Download and import image
    $upload_dir = wp_upload_dir();
    $image_data = wp_remote_get($image_url);
    
    if (!is_wp_error($image_data)) {
        $filename = basename($image_url);
        $file = $upload_dir['path'] . '/' . $filename;
        
        file_put_contents($file, wp_remote_retrieve_body($image_data));
        
        $attachment = array(
            'post_mime_type' => wp_check_filetype($filename)['type'],
            'post_title' => sanitize_file_name($filename),
            'post_content' => '',
            'post_status' => 'inherit'
        );
        
        $attach_id = wp_insert_attachment($attachment, $file, $target_post_id);
        
        if ($attach_id) {
            set_post_thumbnail($target_post_id, $attach_id);
            update_post_meta($attach_id, '_wp_attachment_image_alt', $image_alt);
        }
    }
    
    restore_current_blog();
}
```

## Security and Performance

### Multisite Security

```php
// Network-wide security measures
function implement_multisite_security() {
    // Disable file editing across network
    if (!defined('DISALLOW_FILE_EDIT')) {
        define('DISALLOW_FILE_EDIT', true);
    }
    
    // Disable plugin/theme installation for non-super admins
    if (!defined('DISALLOW_FILE_MODS')) {
        define('DISALLOW_FILE_MODS', true);
    }
    
    // Limit login attempts
    add_action('wp_login_failed', 'track_failed_login_attempts');
    add_action('wp_authenticate_user', 'check_login_attempts', 10, 2);
    
    // Network-wide user registration controls
    add_filter('wpmu_signup_user_notification', 'custom_signup_notification', 10, 3);
    
    // Secure file uploads
    add_filter('upload_mimes', 'restrict_upload_mimes');
    add_filter('wp_check_filetype_and_ext', 'validate_file_uploads', 10, 4);
}

function track_failed_login_attempts($username) {
    $ip = $_SERVER['REMOTE_ADDR'];
    $attempts = get_transient('login_attempts_' . $ip);
    
    if ($attempts === false) {
        set_transient('login_attempts_' . $ip, 1, 15 * MINUTE_IN_SECONDS);
    } else {
        set_transient('login_attempts_' . $ip, $attempts + 1, 15 * MINUTE_IN_SECONDS);
    }
}

function check_login_attempts($user, $password) {
    $ip = $_SERVER['REMOTE_ADDR'];
    $attempts = get_transient('login_attempts_' . $ip);
    
    if ($attempts && $attempts >= 5) {
        return new WP_Error('too_many_attempts', 'Too many login attempts. Please try again later.');
    }
    
    return $user;
}

function restrict_upload_mimes($mimes) {
    $allowed_types = get_site_option('allowed_file_types', array('jpg', 'jpeg', 'png', 'gif', 'pdf'));
    
    $restricted_mimes = array();
    foreach ($allowed_types as $type) {
        switch ($type) {
            case 'jpg':
            case 'jpeg':
                $restricted_mimes['jpg|jpeg'] = 'image/jpeg';
                break;
            case 'png':
                $restricted_mimes['png'] = 'image/png';
                break;
            case 'gif':
                $restricted_mimes['gif'] = 'image/gif';
                break;
            case 'pdf':
                $restricted_mimes['pdf'] = 'application/pdf';
                break;
        }
    }
    
    return $restricted_mimes;
}
```

### Performance Optimization

```php
// Network-wide caching
function implement_multisite_caching() {
    // Object caching for network queries
    add_action('init', 'setup_network_object_cache');
    
    // Database query optimization
    add_action('pre_get_posts', 'optimize_multisite_queries');
    
    // CDN integration for media files
    add_filter('wp_get_attachment_url', 'cdn_attachment_url', 10, 2);
}

function setup_network_object_cache() {
    if (function_exists('wp_cache_add_global_groups')) {
        wp_cache_add_global_groups(array('sites', 'site-details', 'blog-details'));
    }
}

function optimize_multisite_queries($query) {
    if (is_admin() || !$query->is_main_query()) {
        return;
    }
    
    // Optimize queries for network sites
    if (is_home() || is_archive()) {
        $query->set('posts_per_page', get_option('posts_per_page', 10));
        $query->set('no_found_rows', true);
    }
}

function cdn_attachment_url($url, $post_id) {
    $cdn_domain = get_site_option('cdn_domain');
    
    if ($cdn_domain) {
        $upload_dir = wp_upload_dir();
        $url = str_replace($upload_dir['baseurl'], $cdn_domain, $url);
    }
    
    return $url;
}

// Network-wide database optimization
function optimize_multisite_database() {
    global $wpdb;
    
    // Optimize network tables
    $network_tables = array(
        $wpdb->blogs,
        $wpdb->blog_versions,
        $wpdb->registration_log,
        $wpdb->signups,
        $wpdb->site,
        $wpdb->sitemeta
    );
    
    foreach ($network_tables as $table) {
        $wpdb->query("OPTIMIZE TABLE $table");
    }
    
    // Get all site tables and optimize them
    $sites = get_sites();
    foreach ($sites as $site) {
        $table_prefix = $wpdb->get_blog_prefix($site->blog_id);
        
        $site_tables = array(
            $table_prefix . 'posts',
            $table_prefix . 'postmeta',
            $table_prefix . 'comments',
            $table_prefix . 'commentmeta',
            $table_prefix . 'options',
            $table_prefix . 'usermeta'
        );
        
        foreach ($site_tables as $table) {
            $wpdb->query("OPTIMIZE TABLE $table");
        }
    }
}
```

## Best Practices

### Development Guidelines

```php
// Multisite development best practices

// 1. Always check if multisite is enabled
function my_multisite_function() {
    if (!is_multisite()) {
        return false;
    }
    
    // Multisite-specific code here
}

// 2. Use proper site switching
function perform_network_operation() {
    $sites = get_sites();
    
    foreach ($sites as $site) {
        switch_to_blog($site->blog_id);
        
        // Perform operation
        
        restore_current_blog(); // Always restore!
    }
}

// 3. Handle network vs site-specific options
function get_network_or_site_option($option_name, $default = false) {
    if (is_multisite()) {
        return get_site_option($option_name, $default);
    } else {
        return get_option($option_name, $default);
    }
}

// 4. Use proper capabilities
function check_multisite_capabilities() {
    if (is_multisite()) {
        if (!current_user_can('manage_network')) {
            wp_die('Network admin access required');
        }
    } else {
        if (!current_user_can('manage_options')) {
            wp_die('Admin access required');
        }
    }
}

// 5. Handle user roles across sites
function get_user_network_roles($user_id) {
    $user_blogs = get_blogs_of_user($user_id);
    $roles = array();
    
    foreach ($user_blogs as $blog_id => $blog) {
        switch_to_blog($blog_id);
        
        $user = get_userdata($user_id);
        if ($user) {
            $roles[$blog_id] = array(
                'blog_name' => $blog->blogname,
                'blog_url' => $blog->siteurl,
                'roles' => $user->roles
            );
        }
        
        restore_current_blog();
    }
    
    return $roles;
}
```

## Official Documentation

https://developer.wordpress.org/advanced-administration/multisite/
https://codex.wordpress.org/Create_A_Network
https://developer.wordpress.org/reference/functions/is_multisite/
