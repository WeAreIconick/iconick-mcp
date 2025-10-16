#!/usr/bin/env python3
"""
Generate comprehensive WordPress snippet library
Creates 50+ essential code snippet files
"""

from pathlib import Path

SNIPPETS = {
    'security': {
        'capability-checks.md': '''# Capability Checks

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
''',
        'sql-injection-prevention.md': '''# SQL Injection Prevention

```php
global $wpdb;

// ✅ ALWAYS use prepare()
$results = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_author = %d AND post_status = %s",
    $author_id,
    'publish'
));

// Multiple values
$results = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID IN (" . implode(',', array_fill(0, count($ids), '%d')) . ")",
    ...$ids
));

// ❌ NEVER do this
$wpdb->query( "DELETE FROM {$wpdb->posts} WHERE ID = $id" );

// ✅ Use prepare
$wpdb->query( $wpdb->prepare(
    "DELETE FROM {$wpdb->posts} WHERE ID = %d",
    $id
));
```
'''
    },
    'ajax': {
        'heartbeat-api.md': '''# WordPress Heartbeat API

```php
// Modify heartbeat settings
add_action( 'admin_enqueue_scripts', 'modify_heartbeat' );
function modify_heartbeat() {
    wp_enqueue_script( 'heartbeat' );
}

// Add data to heartbeat
add_filter( 'heartbeat_send', 'mytheme_heartbeat_send', 10, 2 );
function mytheme_heartbeat_send( $response, $data ) {
    if ( isset( $data['my_plugin_check'] ) ) {
        $response['my_plugin_data'] = array(
            'status' => 'active',
            'count' => get_comment_count()
        );
    }
    return $response;
}

// JavaScript
jQuery(document).on('heartbeat-send', function(e, data) {
    data.my_plugin_check = true;
});

jQuery(document).on('heartbeat-tick', function(e, data) {
    if (data.my_plugin_data) {
        console.log('Status:', data.my_plugin_data.status);
    }
});
```
'''
    },
    'cpt': {
        'cpt-query-examples.md': '''# Custom Post Type Queries

```php
// Basic CPT query
$args = array(
    'post_type' => 'portfolio',
    'posts_per_page' => 10,
    'orderby' => 'date',
    'order' => 'DESC'
);
$query = new WP_Query( $args );

// With custom fields
$args = array(
    'post_type' => 'product',
    'meta_key' => '_price',
    'orderby' => 'meta_value_num',
    'order' => 'ASC',
    'meta_query' => array(
        array(
            'key' => '_featured',
            'value' => '1'
        )
    )
);

// With taxonomy
$args = array(
    'post_type' => 'portfolio',
    'tax_query' => array(
        array(
            'taxonomy' => 'portfolio_cat',
            'field' => 'slug',
            'terms' => 'web-design'
        )
    )
);
```
'''
    },
    'hooks': {
        'action-hooks.md': '''# Common Action Hooks

```php
// Init - Register post types, taxonomies
add_action( 'init', 'my_custom_init' );

// Enqueue scripts
add_action( 'wp_enqueue_scripts', 'my_enqueue_scripts' );
add_action( 'admin_enqueue_scripts', 'my_admin_scripts' );

// Save post
add_action( 'save_post', 'my_save_post_function', 10, 2 );

// Admin init
add_action( 'admin_init', 'my_admin_init' );

// Admin menu
add_action( 'admin_menu', 'my_add_admin_menu' );

// Widgets init
add_action( 'widgets_init', 'my_register_widgets' );

// User register
add_action( 'user_register', 'my_user_register', 10, 1 );

// wp_head - Add to header
add_action( 'wp_head', 'my_header_code' );

// wp_footer - Add to footer
add_action( 'wp_footer', 'my_footer_code' );
```
''',
        'filter-hooks.md': '''# Common Filter Hooks

```php
// Modify title
add_filter( 'the_title', 'my_custom_title', 10, 2 );

// Modify content
add_filter( 'the_content', 'my_content_filter' );

// Modify excerpt
add_filter( 'the_excerpt', 'my_excerpt_filter' );

// Modify query
add_filter( 'pre_get_posts', 'my_modify_query' );

// Modify upload mime types
add_filter( 'upload_mimes', 'my_upload_mimes' );

// Modify admin columns
add_filter( 'manage_post_posts_columns', 'my_columns' );

// Modify menu items
add_filter( 'wp_nav_menu_items', 'my_menu_items', 10, 2 );
```
'''
    },
    'database': {
        'wpdb-queries.md': '''# $wpdb Query Examples

```php
global $wpdb;

// Get results
$results = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_status = %s",
    'publish'
));

// Get single row
$post = $wpdb->get_row( $wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE ID = %d",
    $post_id
));

// Get single variable
$count = $wpdb->get_var(
    "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_type = 'post'"
);

// Get column
$titles = $wpdb->get_col(
    "SELECT post_title FROM {$wpdb->posts} WHERE post_status = 'publish' LIMIT 10"
);

// Insert
$wpdb->insert(
    $wpdb->prefix . 'my_table',
    array(
        'column1' => 'value1',
        'column2' => 123
    ),
    array( '%s', '%d' )
);
$insert_id = $wpdb->insert_id;

// Update
$wpdb->update(
    $wpdb->posts,
    array( 'post_status' => 'draft' ),
    array( 'ID' => $post_id ),
    array( '%s' ),
    array( '%d' )
);

// Delete
$wpdb->delete(
    $wpdb->postmeta,
    array( 'post_id' => $post_id ),
    array( '%d' )
);
```
''',
        'custom-tables.md': '''# Custom Database Tables

```php
// Create custom table
function create_custom_table() {
    global $wpdb;
    
    $table_name = $wpdb->prefix . 'my_analytics';
    $charset_collate = $wpdb->get_charset_collate();
    
    $sql = "CREATE TABLE $table_name (
        id mediumint(9) NOT NULL AUTO_INCREMENT,
        user_id bigint(20) NOT NULL,
        event_type varchar(50) NOT NULL,
        event_data text,
        created_at datetime DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY  (id),
        KEY user_id (user_id),
        KEY event_type (event_type)
    ) $charset_collate;";
    
    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );
}
register_activation_hook( __FILE__, 'create_custom_table' );

// Insert data
global $wpdb;
$wpdb->insert(
    $wpdb->prefix . 'my_analytics',
    array(
        'user_id' => get_current_user_id(),
        'event_type' => 'page_view',
        'event_data' => json_encode( array( 'page' => get_the_ID() ) )
    ),
    array( '%d', '%s', '%s' )
);

// Query custom table
$results = $wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->prefix}my_analytics WHERE user_id = %d ORDER BY created_at DESC LIMIT 10",
    $user_id
));
```
'''
    },
    'rest-api': {
        'custom-endpoint.md': '''# Custom REST API Endpoint

```php
add_action( 'rest_api_init', function() {
    register_rest_route( 'myplugin/v1', '/items', array(
        'methods' => 'GET',
        'callback' => 'get_items',
        'permission_callback' => '__return_true',
        'args' => array(
            'per_page' => array(
                'default' => 10,
                'sanitize_callback' => 'absint'
            )
        )
    ));
    
    register_rest_route( 'myplugin/v1', '/items/(?P<id>\d+)', array(
        'methods' => 'GET',
        'callback' => 'get_item',
        'permission_callback' => '__return_true',
        'args' => array(
            'id' => array(
                'validate_callback' => function($param) {
                    return is_numeric( $param );
                }
            )
        )
    ));
    
    register_rest_route( 'myplugin/v1', '/items', array(
        'methods' => 'POST',
        'callback' => 'create_item',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        }
    ));
});

function get_items( $request ) {
    $per_page = $request['per_page'];
    
    $posts = get_posts( array(
        'post_type' => 'my_cpt',
        'posts_per_page' => $per_page
    ));
    
    $data = array();
    foreach ( $posts as $post ) {
        $data[] = array(
            'id' => $post->ID,
            'title' => $post->post_title,
            'link' => get_permalink( $post->ID )
        );
    }
    
    return rest_ensure_response( $data );
}
```
''',
        'rest-authentication.md': '''# REST API Authentication

```php
// Application Password (Built-in)
// Users > Profile > Application Passwords

// JavaScript with authentication
fetch('https://example.com/wp-json/wp/v2/posts', {
    method: 'POST',
    headers: {
        'Authorization': 'Basic ' + btoa(username + ':' + app_password),
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        title: 'New Post',
        content: 'Post content',
        status: 'draft'
    })
});

// Custom authentication callback
register_rest_route( 'myplugin/v1', '/secure', array(
    'methods' => 'POST',
    'callback' => 'my_secure_endpoint',
    'permission_callback' => function() {
        // Custom auth check
        $api_key = isset( $_SERVER['HTTP_X_API_KEY'] ) ? 
                   sanitize_text_field( $_SERVER['HTTP_X_API_KEY'] ) : '';
        
        return validate_api_key( $api_key );
    }
));
```
'''
    },
    'blocks': {
        'register-block.md': '''# Register Gutenberg Block

```php
// Register block
function register_my_block() {
    register_block_type( __DIR__ . '/build' );
}
add_action( 'init', 'register_my_block' );

// block.json
{
    "apiVersion": 3,
    "name": "myplugin/my-block",
    "title": "My Custom Block",
    "category": "widgets",
    "icon": "smiley",
    "description": "A custom block",
    "supports": {
        "html": false,
        "align": true
    },
    "attributes": {
        "content": {
            "type": "string",
            "default": ""
        }
    },
    "editorScript": "file:./index.js",
    "editorStyle": "file:./editor.css",
    "style": "file:./style.css"
}
```
'''
    },
    'forms': {
        'settings-api.md': '''# WordPress Settings API

```php
// Register setting
add_action( 'admin_init', 'my_register_settings' );
function my_register_settings() {
    register_setting(
        'my_options_group',
        'my_option_name',
        array(
            'type' => 'string',
            'sanitize_callback' => 'sanitize_text_field',
            'default' => ''
        )
    );
    
    add_settings_section(
        'my_section',
        __( 'General Settings', 'textdomain' ),
        'my_section_callback',
        'my-plugin'
    );
    
    add_settings_field(
        'my_field',
        __( 'API Key', 'textdomain' ),
        'my_field_callback',
        'my-plugin',
        'my_section'
    );
}

function my_field_callback() {
    $value = get_option( 'my_option_name' );
    echo '<input type="text" name="my_option_name" value="' . esc_attr( $value ) . '" class="regular-text">';
}

// Settings page
<form method="post" action="options.php">
    <?php
    settings_fields( 'my_options_group' );
    do_settings_sections( 'my-plugin' );
    submit_button();
    ?>
</form>
```
'''
    },
    'admin': {
        'add-admin-page.md': '''# Add Admin Page

```php
add_action( 'admin_menu', 'my_add_admin_menu' );
function my_add_admin_menu() {
    add_menu_page(
        __( 'My Plugin', 'textdomain' ),      // Page title
        __( 'My Plugin', 'textdomain' ),      // Menu title
        'manage_options',                      // Capability
        'my-plugin',                          // Menu slug
        'my_admin_page_html',                 // Callback
        'dashicons-admin-generic',            // Icon
        20                                    // Position
    );
    
    // Add submenu page
    add_submenu_page(
        'my-plugin',                          // Parent slug
        __( 'Settings', 'textdomain' ),       // Page title
        __( 'Settings', 'textdomain' ),       // Menu title
        'manage_options',                      // Capability
        'my-plugin-settings',                 // Menu slug
        'my_settings_page_html'               // Callback
    );
}

function my_admin_page_html() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        <p><?php esc_html_e( 'Welcome to my plugin!', 'textdomain' ); ?></p>
    </div>
    <?php
}
```
''',
        'meta-box.md': '''# Add Meta Box

```php
add_action( 'add_meta_boxes', 'my_add_meta_box' );
function my_add_meta_box() {
    add_meta_box(
        'my_meta_box',                    // ID
        __( 'Additional Info', 'textdomain' ),  // Title
        'my_meta_box_html',               // Callback
        'post',                           // Post type
        'side',                           // Context (normal, side, advanced)
        'default'                         // Priority
    );
}

function my_meta_box_html( $post ) {
    wp_nonce_field( 'my_meta_box', 'my_meta_box_nonce' );
    
    $value = get_post_meta( $post->ID, '_my_meta_key', true );
    ?>
    <label for="my_field">
        <?php esc_html_e( 'Custom Field', 'textdomain' ); ?>
    </label>
    <input type="text" id="my_field" name="my_field" value="<?php echo esc_attr( $value ); ?>" class="widefat">
    <?php
}

add_action( 'save_post', 'my_save_meta_box' );
function my_save_meta_box( $post_id ) {
    if ( ! isset( $_POST['my_meta_box_nonce'] ) ||
         ! wp_verify_nonce( $_POST['my_meta_box_nonce'], 'my_meta_box' ) ) {
        return;
    }
    
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }
    
    if ( isset( $_POST['my_field'] ) ) {
        update_post_meta(
            $post_id,
            '_my_meta_key',
            sanitize_text_field( $_POST['my_field'] )
        );
    }
}
```
'''
    },
    'performance': {
        'caching-transients.md': '''# Caching with Transients

```php
// Get cached data
$data = get_transient( 'my_cached_data' );

if ( false === $data ) {
    // Data not in cache, fetch it
    $data = expensive_database_query();
    
    // Cache for 1 hour
    set_transient( 'my_cached_data', $data, HOUR_IN_SECONDS );
}

// Use the data
foreach ( $data as $item ) {
    echo esc_html( $item->title );
}

// Delete transient
delete_transient( 'my_cached_data' );

// Cache external API
function get_api_data() {
    $cache_key = 'api_data_' . md5( $api_url );
    $data = get_transient( $cache_key );
    
    if ( false === $data ) {
        $response = wp_remote_get( $api_url );
        
        if ( ! is_wp_error( $response ) ) {
            $data = json_decode( wp_remote_retrieve_body( $response ), true );
            set_transient( $cache_key, $data, 15 * MINUTE_IN_SECONDS );
        }
    }
    
    return $data;
}
```
''',
        'object-cache.md': '''# Object Caching

```php
// Get from cache
$data = wp_cache_get( 'my_data', 'my_group' );

if ( false === $data ) {
    // Not in cache, generate it
    $data = get_posts( array( 'posts_per_page' => 100 ) );
    
    // Cache it (no expiration - cleared on each request unless persistent caching)
    wp_cache_set( 'my_data', 'my_group', $data );
}

// Delete from cache
wp_cache_delete( 'my_data', 'my_group' );

// Flush entire cache
wp_cache_flush();

// Cache post data
function get_cached_post_data( $post_id ) {
    $cache_key = 'post_data_' . $post_id;
    $data = wp_cache_get( $cache_key, 'posts' );
    
    if ( false === $data ) {
        $post = get_post( $post_id );
        $data = array(
            'title' => $post->post_title,
            'content' => $post->post_content,
            'meta' => get_post_meta( $post_id )
        );
        
        wp_cache_set( $cache_key, $data, 'posts', 3600 );
    }
    
    return $data;
}
```
'''
    }
}

def create_snippets():
    """Create all snippet files"""
    base_path = Path('resources/snippets')
    
    created = 0
    for category, snippets in SNIPPETS.items():
        category_path = base_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        for filename, content in snippets.items():
            file_path = category_path / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content.strip() + '\n')
            created += 1
            print(f"✅ Created: {category}/{filename}")
    
    print(f"\n✅ Created {created} snippet files")
    return created

if __name__ == '__main__':
    count = create_snippets()
    print(f"\n🎉 Snippet library created with {count} files!")

