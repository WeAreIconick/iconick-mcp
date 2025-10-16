# Register Custom Post Type

## Basic Custom Post Type

```php
function register_portfolio_post_type() {
    $labels = array(
        'name'               => _x( 'Portfolio', 'post type general name', 'textdomain' ),
        'singular_name'      => _x( 'Portfolio Item', 'post type singular name', 'textdomain' ),
        'menu_name'          => _x( 'Portfolio', 'admin menu', 'textdomain' ),
        'name_admin_bar'     => _x( 'Portfolio Item', 'add new on admin bar', 'textdomain' ),
        'add_new'            => _x( 'Add New', 'portfolio', 'textdomain' ),
        'add_new_item'       => __( 'Add New Portfolio Item', 'textdomain' ),
        'new_item'           => __( 'New Portfolio Item', 'textdomain' ),
        'edit_item'          => __( 'Edit Portfolio Item', 'textdomain' ),
        'view_item'          => __( 'View Portfolio Item', 'textdomain' ),
        'all_items'          => __( 'All Portfolio', 'textdomain' ),
        'search_items'       => __( 'Search Portfolio', 'textdomain' ),
        'parent_item_colon'  => __( 'Parent Portfolio:', 'textdomain' ),
        'not_found'          => __( 'No portfolio items found.', 'textdomain' ),
        'not_found_in_trash' => __( 'No portfolio items found in Trash.', 'textdomain' )
    );

    $args = array(
        'labels'             => $labels,
        'description'        => __( 'Portfolio items for showcase', 'textdomain' ),
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'query_var'          => true,
        'rewrite'            => array( 'slug' => 'portfolio' ),
        'capability_type'    => 'post',
        'has_archive'        => true,
        'hierarchical'       => false,
        'menu_position'      => 5,
        'menu_icon'          => 'dashicons-portfolio',
        'show_in_rest'       => true,  // Enable Gutenberg editor
        'supports'           => array( 'title', 'editor', 'thumbnail', 'excerpt' ),
        'taxonomies'         => array( 'portfolio_category' )
    );

    register_post_type( 'portfolio', $args );
}
add_action( 'init', 'register_portfolio_post_type' );
```

## Hierarchical CPT (Like Pages)

```php
function register_documentation_cpt() {
    $args = array(
        'label'              => __( 'Documentation', 'textdomain' ),
        'public'             => true,
        'hierarchical'       => true,  // Makes it work like pages
        'supports'           => array( 'title', 'editor', 'page-attributes' ),
        'show_in_rest'       => true,
        'has_archive'        => true,
        'rewrite'            => array( 'slug' => 'docs' )
    );
    
    register_post_type( 'documentation', $args );
}
add_action( 'init', 'register_documentation_cpt' );
```

## CPT with Custom Capabilities

```php
function register_secure_document_cpt() {
    $args = array(
        'label'              => __( 'Documents', 'textdomain' ),
        'public'             => true,
        'capability_type'    => 'document',  // Custom capability
        'map_meta_cap'       => true,
        'capabilities'       => array(
            'edit_post'          => 'edit_document',
            'read_post'          => 'read_document',
            'delete_post'        => 'delete_document',
            'edit_posts'         => 'edit_documents',
            'edit_others_posts'  => 'edit_others_documents',
            'delete_posts'       => 'delete_documents',
            'publish_posts'      => 'publish_documents',
            'read_private_posts' => 'read_private_documents'
        ),
        'supports'           => array( 'title', 'editor' ),
        'show_in_rest'       => true
    );
    
    register_post_type( 'document', $args );
}
add_action( 'init', 'register_secure_document_cpt' );

// Add capabilities to role
function add_document_capabilities() {
    $role = get_role( 'editor' );
    $role->add_cap( 'edit_document' );
    $role->add_cap( 'edit_documents' );
    $role->add_cap( 'edit_others_documents' );
    $role->add_cap( 'publish_documents' );
    $role->add_cap( 'read_document' );
    $role->add_cap( 'read_private_documents' );
    $role->add_cap( 'delete_document' );
}
register_activation_hook( __FILE__, 'add_document_capabilities' );
```

## CPT with REST API Fields

```php
function register_product_cpt() {
    register_post_type( 'product', array(
        'label'        => __( 'Products', 'textdomain' ),
        'public'       => true,
        'show_in_rest' => true,
        'rest_base'    => 'products',
        'supports'     => array( 'title', 'editor', 'thumbnail', 'custom-fields' )
    ));
}
add_action( 'init', 'register_product_cpt' );

// Add custom REST API fields
add_action( 'rest_api_init', function() {
    register_rest_field( 'product', 'price', array(
        'get_callback' => function( $post ) {
            return get_post_meta( $post['id'], '_product_price', true );
        },
        'update_callback' => function( $value, $post ) {
            if ( ! is_numeric( $value ) ) {
                return new WP_Error( 'invalid_price', 'Price must be numeric' );
            }
            return update_post_meta( $post->ID, '_product_price', floatval( $value ) );
        },
        'schema' => array(
            'type' => 'number',
            'description' => 'Product price',
            'context' => array( 'view', 'edit' )
        )
    ));
    
    register_rest_field( 'product', 'sku', array(
        'get_callback' => function( $post ) {
            return get_post_meta( $post['id'], '_product_sku', true );
        },
        'update_callback' => function( $value, $post ) {
            return update_post_meta( $post->ID, '_product_sku', sanitize_text_field( $value ) );
        },
        'schema' => array(
            'type' => 'string',
            'description' => 'Product SKU'
        )
    ));
});
```

## Query Custom Post Type

```php
// Simple query
$args = array(
    'post_type' => 'portfolio',
    'posts_per_page' => 10
);
$query = new WP_Query( $args );

// With meta query
$args = array(
    'post_type' => 'product',
    'meta_query' => array(
        array(
            'key' => '_product_price',
            'value' => 100,
            'compare' => '<',
            'type' => 'NUMERIC'
        )
    )
);

// With taxonomy query
$args = array(
    'post_type' => 'portfolio',
    'tax_query' => array(
        array(
            'taxonomy' => 'portfolio_category',
            'field' => 'slug',
            'terms' => 'web-design'
        )
    )
);
```

## Flush Rewrite Rules

```php
// Flush on plugin activation
register_activation_hook( __FILE__, 'myplugin_activate' );
function myplugin_activate() {
    register_portfolio_post_type();
    flush_rewrite_rules();
}

// Flush on plugin deactivation
register_deactivation_hook( __FILE__, 'myplugin_deactivate' );
function myplugin_deactivate() {
    flush_rewrite_rules();
}
```

## Complete Example with Everything

```php
function register_complete_cpt() {
    $labels = array(
        'name'               => _x( 'Events', 'post type general name', 'textdomain' ),
        'singular_name'      => _x( 'Event', 'post type singular name', 'textdomain' ),
        'menu_name'          => _x( 'Events', 'admin menu', 'textdomain' ),
        'add_new_item'       => __( 'Add New Event', 'textdomain' ),
        'edit_item'          => __( 'Edit Event', 'textdomain' ),
        'view_item'          => __( 'View Event', 'textdomain' ),
        'all_items'          => __( 'All Events', 'textdomain' ),
        'search_items'       => __( 'Search Events', 'textdomain' ),
        'not_found'          => __( 'No events found.', 'textdomain' )
    );

    $args = array(
        'labels'             => $labels,
        'description'        => __( 'Event management', 'textdomain' ),
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'show_in_nav_menus'  => true,
        'show_in_admin_bar'  => true,
        'query_var'          => true,
        'rewrite'            => array( 
            'slug' => 'events',
            'with_front' => false
        ),
        'capability_type'    => 'post',
        'has_archive'        => true,
        'hierarchical'       => false,
        'menu_position'      => 5,
        'menu_icon'          => 'dashicons-calendar-alt',
        'show_in_rest'       => true,
        'rest_base'          => 'events',
        'rest_controller_class' => 'WP_REST_Posts_Controller',
        'supports'           => array( 
            'title', 
            'editor', 
            'thumbnail', 
            'excerpt',
            'custom-fields'
        ),
        'taxonomies'         => array( 'event_category', 'post_tag' )
    );

    register_post_type( 'event', $args );
}
add_action( 'init', 'register_complete_cpt' );
```

