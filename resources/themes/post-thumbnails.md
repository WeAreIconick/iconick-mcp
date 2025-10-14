# WordPress Post Thumbnails (Featured Images)

Post thumbnails (featured images) provide visual representation for posts, pages, and custom post types.

## Theme Support

### Enable Post Thumbnail Support

```php
// functions.php - Enable post thumbnail support
function my_theme_setup() {
    // Add theme support for post thumbnails
    add_theme_support('post-thumbnails');
    
    // Enable for specific post types
    add_theme_support('post-thumbnails', array('post', 'page', 'product'));
}
add_action('after_setup_theme', 'my_theme_setup');
```

### Custom Image Sizes

```php
// functions.php - Add custom image sizes
function my_theme_image_sizes() {
    // Add custom image sizes
    add_image_size('custom-thumbnail', 300, 200, true); // Hard crop
    add_image_size('custom-medium', 600, 400, false);   // Soft crop
    add_image_size('custom-large', 1200, 800, true);    // Hard crop
    
    // Add custom sizes for specific use cases
    add_image_size('hero-image', 1920, 1080, true);     // Hero section
    add_image_size('card-image', 400, 300, true);       // Card layouts
    add_image_size('square-thumb', 300, 300, true);     // Square thumbnails
}
add_action('after_setup_theme', 'my_theme_image_sizes');
```

### Remove Default Image Sizes

```php
// Remove default WordPress image sizes to save space
function remove_default_image_sizes() {
    // Remove default sizes
    remove_image_size('medium');
    remove_image_size('large');
    remove_image_size('medium_large');
}
add_action('init', 'remove_default_image_sizes');
```

## Displaying Featured Images

### Basic Featured Image Display

```php
// Basic featured image display
if (has_post_thumbnail()) {
    the_post_thumbnail();
}

// With specific size
if (has_post_thumbnail()) {
    the_post_thumbnail('medium');
}

// With custom attributes
if (has_post_thumbnail()) {
    the_post_thumbnail('large', array(
        'class' => 'featured-image',
        'alt' => get_the_title()
    ));
}
```

### Advanced Featured Image Display

```php
// Advanced featured image with fallback
function display_featured_image($size = 'medium', $class = '') {
    if (has_post_thumbnail()) {
        // Get the featured image
        $thumbnail_id = get_post_thumbnail_id();
        $thumbnail_url = wp_get_attachment_image_url($thumbnail_id, $size);
        $thumbnail_alt = get_post_meta($thumbnail_id, '_wp_attachment_image_alt', true);
        
        // Generate responsive image
        $image_meta = wp_get_attachment_metadata($thumbnail_id);
        
        echo '<div class="featured-image-container ' . esc_attr($class) . '">';
        echo '<img src="' . esc_url($thumbnail_url) . '" ';
        echo 'alt="' . esc_attr($thumbnail_alt) . '" ';
        echo 'class="featured-image" ';
        echo 'loading="lazy" ';
        echo '/>';
        echo '</div>';
    } else {
        // Fallback image
        echo '<div class="featured-image-fallback ' . esc_attr($class) . '">';
        echo '<img src="' . get_template_directory_uri() . '/assets/images/placeholder.jpg" ';
        echo 'alt="' . esc_attr(get_the_title()) . '" ';
        echo 'class="featured-image" ';
        echo '/>';
        echo '</div>';
    }
}
```

### Responsive Featured Images

```php
// Responsive featured image function
function display_responsive_featured_image($size = 'medium', $class = '') {
    if (has_post_thumbnail()) {
        $thumbnail_id = get_post_thumbnail_id();
        
        // Get different sizes for responsive images
        $sizes = array(
            'thumbnail' => wp_get_attachment_image_url($thumbnail_id, 'thumbnail'),
            'medium' => wp_get_attachment_image_url($thumbnail_id, 'medium'),
            'large' => wp_get_attachment_image_url($thumbnail_id, 'large'),
            'full' => wp_get_attachment_image_url($thumbnail_id, 'full')
        );
        
        $alt_text = get_post_meta($thumbnail_id, '_wp_attachment_image_alt', true);
        
        echo '<picture class="responsive-featured-image ' . esc_attr($class) . '">';
        
        // Source elements for different screen sizes
        echo '<source media="(min-width: 768px)" srcset="' . esc_url($sizes['large']) . '">';
        echo '<source media="(min-width: 480px)" srcset="' . esc_url($sizes['medium']) . '">';
        
        // Default image
        echo '<img src="' . esc_url($sizes['medium']) . '" ';
        echo 'alt="' . esc_attr($alt_text) . '" ';
        echo 'class="featured-image" ';
        echo 'loading="lazy" ';
        echo '/>';
        
        echo '</picture>';
    }
}
```

## Featured Image in Loops

### Post Loop with Featured Images

```php
// Display featured images in post loops
if (have_posts()) {
    while (have_posts()) {
        the_post();
        ?>
        <article id="post-<?php the_ID(); ?>" <?php post_class('post-item'); ?>>
            <?php if (has_post_thumbnail()) : ?>
                <div class="post-thumbnail">
                    <a href="<?php the_permalink(); ?>">
                        <?php the_post_thumbnail('medium', array('class' => 'post-image')); ?>
                    </a>
                </div>
            <?php endif; ?>
            
            <div class="post-content">
                <h2 class="post-title">
                    <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                </h2>
                <div class="post-excerpt">
                    <?php the_excerpt(); ?>
                </div>
            </div>
        </article>
        <?php
    }
}
```

### Grid Layout with Featured Images

```php
// Grid layout with featured images
function display_posts_grid($posts_per_page = 6) {
    $posts = get_posts(array(
        'posts_per_page' => $posts_per_page,
        'post_status' => 'publish'
    ));
    
    if ($posts) {
        echo '<div class="posts-grid">';
        foreach ($posts as $post) {
            setup_postdata($post);
            ?>
            <div class="grid-item">
                <?php if (has_post_thumbnail()) : ?>
                    <div class="grid-thumbnail">
                        <a href="<?php the_permalink(); ?>">
                            <?php the_post_thumbnail('card-image', array('class' => 'grid-image')); ?>
                        </a>
                    </div>
                <?php endif; ?>
                
                <div class="grid-content">
                    <h3 class="grid-title">
                        <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                    </h3>
                    <div class="grid-meta">
                        <span class="grid-date"><?php echo get_the_date(); ?></span>
                    </div>
                </div>
            </div>
            <?php
        }
        echo '</div>';
        wp_reset_postdata();
    }
}
```

## Custom Post Type Featured Images

### Enable for Custom Post Types

```php
// Enable featured images for custom post types
function enable_featured_images_cpt() {
    // Enable for specific custom post types
    add_post_type_support('product', 'thumbnail');
    add_post_type_support('portfolio', 'thumbnail');
    add_post_type_support('team', 'thumbnail');
}
add_action('init', 'enable_featured_images_cpt');
```

### Custom Post Type Display

```php
// Display featured images for custom post types
function display_cpt_featured_image($post_type = 'product') {
    if (has_post_thumbnail()) {
        $thumbnail_id = get_post_thumbnail_id();
        
        // Get custom sizes based on post type
        $size = ($post_type === 'product') ? 'product-thumbnail' : 'medium';
        
        echo '<div class="cpt-featured-image">';
        echo '<a href="' . get_permalink() . '">';
        the_post_thumbnail($size, array(
            'class' => 'cpt-image',
            'alt' => get_the_title()
        ));
        echo '</a>';
        echo '</div>';
    }
}
```

## Featured Image Functions

### Get Featured Image URL

```php
// Get featured image URL
function get_featured_image_url($post_id = null, $size = 'medium') {
    if (!$post_id) {
        $post_id = get_the_ID();
    }
    
    $thumbnail_id = get_post_thumbnail_id($post_id);
    
    if ($thumbnail_id) {
        return wp_get_attachment_image_url($thumbnail_id, $size);
    }
    
    return false;
}

// Usage
$image_url = get_featured_image_url(get_the_ID(), 'large');
if ($image_url) {
    echo '<img src="' . esc_url($image_url) . '" alt="Featured Image">';
}
```

### Get Featured Image with Metadata

```php
// Get featured image with complete metadata
function get_featured_image_metadata($post_id = null, $size = 'medium') {
    if (!$post_id) {
        $post_id = get_the_ID();
    }
    
    $thumbnail_id = get_post_thumbnail_id($post_id);
    
    if ($thumbnail_id) {
        $metadata = wp_get_attachment_metadata($thumbnail_id);
        $image_url = wp_get_attachment_image_url($thumbnail_id, $size);
        $alt_text = get_post_meta($thumbnail_id, '_wp_attachment_image_alt', true);
        
        return array(
            'id' => $thumbnail_id,
            'url' => $image_url,
            'alt' => $alt_text,
            'width' => $metadata['width'] ?? 0,
            'height' => $metadata['height'] ?? 0,
            'sizes' => $metadata['sizes'] ?? array()
        );
    }
    
    return false;
}
```

## Featured Image Styling

### CSS for Featured Images

```css
/* Featured image styling */
.featured-image {
    width: 100%;
    height: auto;
    border-radius: 8px;
    transition: transform 0.3s ease;
}

.featured-image:hover {
    transform: scale(1.05);
}

.featured-image-container {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
}

/* Grid layout styling */
.posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.grid-item {
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.grid-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.grid-thumbnail {
    position: relative;
    overflow: hidden;
}

.grid-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.grid-item:hover .grid-image {
    transform: scale(1.1);
}

.grid-content {
    padding: 1.5rem;
}

.grid-title {
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
    line-height: 1.3;
}

.grid-title a {
    color: #333;
    text-decoration: none;
}

.grid-title a:hover {
    color: #0073aa;
}

/* Responsive featured images */
.responsive-featured-image {
    width: 100%;
    height: auto;
}

@media (max-width: 768px) {
    .posts-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .grid-image {
        height: 150px;
    }
}
```

## Featured Image Optimization

### Lazy Loading

```php
// Add lazy loading to featured images
function add_lazy_loading_to_featured_images($attr, $attachment, $size) {
    // Add lazy loading attribute
    $attr['loading'] = 'lazy';
    
    // Add data attributes for lazy loading
    if (isset($attr['src'])) {
        $attr['data-src'] = $attr['src'];
        $attr['src'] = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMSIgaGVpZ2h0PSIxIiB2aWV3Qm94PSIwIDAgMSAxIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiNmMGYwZjAiLz48L3N2Zz4=';
    }
    
    return $attr;
}
add_filter('wp_get_attachment_image_attributes', 'add_lazy_loading_to_featured_images', 10, 3);
```

### WebP Support

```php
// Add WebP support for featured images
function add_webp_support_to_featured_images($attr, $attachment, $size) {
    $thumbnail_id = $attachment->ID;
    $webp_url = wp_get_attachment_image_url($thumbnail_id, $size);
    
    // Convert to WebP if available
    if (function_exists('imagewebp')) {
        $webp_url = str_replace(array('.jpg', '.jpeg', '.png'), '.webp', $webp_url);
    }
    
    // Add WebP source
    if (isset($attr['src'])) {
        $attr['data-webp'] = $webp_url;
    }
    
    return $attr;
}
add_filter('wp_get_attachment_image_attributes', 'add_webp_support_to_featured_images', 10, 3);
```

## Featured Image Hooks and Filters

### Custom Featured Image Filters

```php
// Filter featured image output
function custom_featured_image_filter($html, $post_id, $post_thumbnail_id, $size, $attr) {
    // Add custom classes
    if (isset($attr['class'])) {
        $attr['class'] .= ' custom-featured-image';
    } else {
        $attr['class'] = 'custom-featured-image';
    }
    
    // Add data attributes
    $attr['data-post-id'] = $post_id;
    $attr['data-size'] = $size;
    
    return $html;
}
add_filter('post_thumbnail_html', 'custom_featured_image_filter', 10, 5);

// Filter featured image size
function custom_featured_image_size($size, $post_id) {
    // Use different sizes based on post type
    $post_type = get_post_type($post_id);
    
    switch ($post_type) {
        case 'product':
            return 'product-thumbnail';
        case 'portfolio':
            return 'portfolio-thumbnail';
        default:
            return $size;
    }
}
add_filter('post_thumbnail_size', 'custom_featured_image_size', 10, 2);
```

## Featured Image Admin Customization

### Custom Admin Columns

```php
// Add featured image column to admin
function add_featured_image_admin_column($columns) {
    // Insert featured image column after title
    $new_columns = array();
    foreach ($columns as $key => $value) {
        $new_columns[$key] = $value;
        if ($key === 'title') {
            $new_columns['featured_image'] = __('Featured Image', 'my-theme');
        }
    }
    return $new_columns;
}
add_filter('manage_posts_columns', 'add_featured_image_admin_column');

// Display featured image in admin column
function display_featured_image_admin_column($column, $post_id) {
    if ($column === 'featured_image') {
        if (has_post_thumbnail($post_id)) {
            echo '<a href="' . get_edit_post_link($post_id) . '">';
            echo get_the_post_thumbnail($post_id, 'thumbnail');
            echo '</a>';
        } else {
            echo '<span class="dashicons dashicons-format-image"></span>';
        }
    }
}
add_action('manage_posts_custom_column', 'display_featured_image_admin_column', 10, 2);
```

## Official Documentation

https://developer.wordpress.org/themes/functionality/featured-images-post-thumbnails/
https://developer.wordpress.org/reference/functions/add_theme_support/
https://developer.wordpress.org/reference/functions/add_image_size/
