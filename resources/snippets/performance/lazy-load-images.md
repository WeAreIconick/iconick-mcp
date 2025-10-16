---
difficulty: Beginner
tags: [performance, images, lazy-load, speed]
related: [performance/defer-async-scripts]
use_case: Lazy loading images
---

# Lazy Load Images

```php
// Add loading="lazy" to images
add_filter( 'wp_get_attachment_image_attributes', 'add_lazy_loading', 10, 2 );
function add_lazy_loading( $attr, $attachment ) {
    $attr['loading'] = 'lazy';
    return $attr;
}

// Lazy load in content
add_filter( 'the_content', 'add_lazy_load_to_content' );
function add_lazy_load_to_content( $content ) {
    // Add loading="lazy" to img tags
    $content = preg_replace(
        '/<img((?![^>]*loading=)[^>]*)>/i',
        '<img$1 loading="lazy">',
        $content
    );
    
    return $content;
}

// Disable lazy loading for first image (LCP optimization)
add_filter( 'wp_get_attachment_image_attributes', 'disable_lazy_first_image', 10, 3 );
function disable_lazy_first_image( $attr, $attachment, $size ) {
    static $first_image = true;
    
    if ( $first_image ) {
        $attr['loading'] = 'eager';
        $first_image = false;
    }
    
    return $attr;
}
```
