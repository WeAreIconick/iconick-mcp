# Enqueue Scripts and Styles

```php
// Frontend scripts
add_action( 'wp_enqueue_scripts', 'mytheme_enqueue_scripts' );
function mytheme_enqueue_scripts() {
    // Enqueue CSS
    wp_enqueue_style(
        'mytheme-style',
        get_stylesheet_uri(),
        array(),
        wp_get_theme()->get( 'Version' )
    );
    
    // Enqueue JavaScript
    wp_enqueue_script(
        'mytheme-script',
        get_template_directory_uri() . '/js/script.js',
        array( 'jquery' ),
        wp_get_theme()->get( 'Version' ),
        true  // Load in footer
    );
    
    // Pass data to JavaScript
    wp_localize_script( 'mytheme-script', 'themeData', array(
        'ajaxurl' => admin_url( 'admin-ajax.php' ),
        'nonce' => wp_create_nonce( 'theme_nonce' ),
        'siteUrl' => home_url()
    ));
}

// Admin scripts
add_action( 'admin_enqueue_scripts', 'myplugin_admin_scripts' );
function myplugin_admin_scripts( $hook ) {
    // Only load on specific pages
    if ( $hook !== 'toplevel_page_myplugin' ) {
        return;
    }
    
    wp_enqueue_style( 'myplugin-admin', plugins_url( 'css/admin.css', __FILE__ ) );
    wp_enqueue_script( 'myplugin-admin', plugins_url( 'js/admin.js', __FILE__ ), array( 'jquery' ) );
}

// Conditional loading
add_action( 'wp_enqueue_scripts', 'conditional_scripts' );
function conditional_scripts() {
    // Only on single product pages
    if ( is_singular( 'product' ) ) {
        wp_enqueue_script( 'product-viewer', get_template_directory_uri() . '/js/product.js' );
    }
    
    // Only on homepage
    if ( is_front_page() ) {
        wp_enqueue_style( 'homepage-style', get_template_directory_uri() . '/css/home.css' );
    }
}

// Add defer attribute
add_filter( 'script_loader_tag', 'add_defer_attribute', 10, 2 );
function add_defer_attribute( $tag, $handle ) {
    if ( 'mytheme-script' === $handle ) {
        return str_replace( ' src', ' defer src', $tag );
    }
    return $tag;
}
```
