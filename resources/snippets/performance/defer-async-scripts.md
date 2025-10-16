---
difficulty: Intermediate
tags: [performance, scripts, async, defer]
related: [hooks/wp-enqueue-scripts]
use_case: Optimizing script loading
---

# Defer and Async Scripts

```php
// Add defer to specific scripts
add_filter( 'script_loader_tag', 'add_defer_to_scripts', 10, 3 );
function add_defer_to_scripts( $tag, $handle, $src ) {
    // Scripts to defer
    $defer_scripts = array(
        'my-theme-script',
        'analytics-script',
        'social-sharing'
    );
    
    if ( in_array( $handle, $defer_scripts ) ) {
        return '<script src="' . esc_url( $src ) . '" defer></script>';
    }
    
    return $tag;
}

// Add async to specific scripts
add_filter( 'script_loader_tag', 'add_async_to_scripts', 10, 3 );
function add_async_to_scripts( $tag, $handle, $src ) {
    // Scripts to load async
    $async_scripts = array(
        'google-ads',
        'facebook-pixel'
    );
    
    if ( in_array( $handle, $async_scripts ) ) {
        return '<script src="' . esc_url( $src ) . '" async></script>';
    }
    
    return $tag;
}

// Defer all scripts except jQuery
add_filter( 'script_loader_tag', 'defer_all_scripts', 10, 3 );
function defer_all_scripts( $tag, $handle, $src ) {
    // Don't defer jQuery
    if ( 'jquery' === $handle || 'jquery-core' === $handle ) {
        return $tag;
    }
    
    // Add defer attribute
    return str_replace( ' src', ' defer src', $tag );
}

// Load scripts in footer
add_action( 'wp_enqueue_scripts', 'enqueue_footer_scripts' );
function enqueue_footer_scripts() {
    wp_enqueue_script(
        'my-script',
        get_template_directory_uri() . '/js/script.js',
        array( 'jquery' ),
        '1.0.0',
        true  // Load in footer
    );
}
```
