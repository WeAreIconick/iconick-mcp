# WordPress Template Hierarchy

The template hierarchy is WordPress's system for determining which template file to load for any given request. Understanding this hierarchy is crucial for theme development.

## How It Works

WordPress follows a specific order when looking for template files, starting with the most specific and falling back to more general templates.

## Single Post Templates

```php
// For a single post, WordPress looks for templates in this order:
1. single-{post_type}-{slug}.php     // single-product-awesome-widget.php
2. single-{post_type}.php           // single-product.php
3. single.php                       // single.php
4. singular.php                     // singular.php
5. index.php                        // index.php (fallback)
```

### Examples

```php
// Single post with slug "hello-world"
single-post-hello-world.php → single-post.php → single.php → singular.php → index.php

// Single product with slug "awesome-widget"
single-product-awesome-widget.php → single-product.php → single.php → singular.php → index.php

// Single page with slug "about"
single-page-about.php → page-about.php → page.php → singular.php → index.php
```

## Page Templates

```php
// For pages, WordPress looks for:
1. Custom page template (assigned in admin)
2. page-{slug}.php                 // page-about.php
3. page-{id}.php                   // page-123.php
4. page-{template}.php             // page-full-width.php
5. page.php                        // page.php
6. singular.php                    // singular.php
7. index.php                       // index.php (fallback)
```

## Archive Templates

### Post Archives

```php
// Blog posts archive
1. home.php                        // home.php
2. index.php                       // index.php

// Category archives
1. category-{slug}.php             // category-news.php
2. category-{id}.php               // category-1.php
3. category.php                    // category.php
4. archive.php                     // archive.php
5. index.php                       // index.php

// Tag archives
1. tag-{slug}.php                  // tag-wordpress.php
2. tag-{id}.php                    // tag-5.php
3. tag.php                         // tag.php
4. archive.php                     // archive.php
5. index.php                       // index.php
```

### Custom Post Type Archives

```php
// Custom post type archives
1. archive-{post_type}.php         // archive-product.php
2. archive.php                     // archive.php
3. index.php                       // index.php
```

### Custom Taxonomy Archives

```php
// Custom taxonomy archives
1. taxonomy-{taxonomy}-{term}.php  // taxonomy-genre-action.php
2. taxonomy-{taxonomy}.php         // taxonomy-genre.php
3. taxonomy.php                    // taxonomy.php
4. archive.php                     // archive.php
5. index.php                       // index.php
```

## Date Archives

```php
// Date-based archives
1. date.php                        // date.php
2. archive.php                     // archive.php
3. index.php                       // index.php

// Specific date archives
1. year-{year}.php                 // year-2023.php
2. month-{month}.php               // month-01.php
3. day-{day}.php                   // day-15.php
```

## Author Archives

```php
// Author archives
1. author-{nicename}.php           // author-john-doe.php
2. author-{id}.php                 // author-1.php
3. author.php                      // author.php
4. archive.php                     // archive.php
5. index.php                       // index.php
```

## Search Results

```php
// Search results
1. search.php                      // search.php
2. index.php                       // index.php
```

## 404 Error Pages

```php
// 404 error page
1. 404.php                         // 404.php
2. index.php                       // index.php
```

## Attachment Pages

```php
// Attachment pages
1. MIME_type.php                   // image.php, video.php
2. attachment.php                  // attachment.php
3. single-attachment.php           // single-attachment.php
4. single.php                      // single.php
5. singular.php                    // singular.php
6. index.php                       // index.php
```

## Conditional Tags

Use these functions to determine which template to load:

```php
// Check current page type
is_home()                          // Blog posts page
is_front_page()                    // Front page (static page or blog)
is_single()                        // Single post
is_page()                          // Single page
is_archive()                       // Any archive page
is_category()                      // Category archive
is_tag()                           // Tag archive
is_author()                        // Author archive
is_date()                          // Date archive
is_search()                        // Search results
is_404()                           // 404 error page
is_attachment()                    // Attachment page

// Check post type
is_singular( 'product' )           // Single product
is_post_type_archive( 'product' )  // Product archive

// Check taxonomy
is_tax( 'genre' )                  // Genre taxonomy archive
is_tax( 'genre', 'action' )        // Action genre archive
```

## Template Hierarchy in Practice

### Creating a Custom Template

```php
// For a specific page, create page-about.php
<?php
/**
 * Template Name: About Page
 * Template for the About page
 */

get_header(); ?>

<div class="about-page">
    <h1><?php the_title(); ?></h1>
    <div class="about-content">
        <?php the_content(); ?>
    </div>
</div>

<?php get_footer(); ?>
```

### Using Conditional Logic

```php
// In index.php or a general template
<?php
if ( is_home() ) {
    // Blog posts page
    get_template_part( 'template-parts/content', 'blog' );
} elseif ( is_single() ) {
    // Single post
    get_template_part( 'template-parts/content', 'single' );
} elseif ( is_page() ) {
    // Single page
    get_template_part( 'template-parts/content', 'page' );
} elseif ( is_archive() ) {
    // Archive page
    get_template_part( 'template-parts/content', 'archive' );
} else {
    // Fallback
    get_template_part( 'template-parts/content', 'none' );
}
?>
```

## Block Theme Hierarchy

In block themes (WordPress 5.9+), the hierarchy works similarly but uses template parts:

```php
// Block theme templates
1. templates/single.html           // Single post template
2. templates/single-{post_type}.html  // Single product template
3. templates/index.html            // Fallback template

// Template parts
1. parts/header.html               // Header template part
2. parts/footer.html               // Footer template part
3. parts/post-content.html         // Post content template part
```

## Advanced Template Hierarchy

### Custom Query Variables

```php
// Handle custom query variables
function handle_custom_template( $template ) {
    if ( is_page() && get_query_var( 'custom_view' ) ) {
        $custom_template = locate_template( 'page-custom.php' );
        if ( $custom_template ) {
            return $custom_template;
        }
    }
    return $template;
}
add_filter( 'template_include', 'handle_custom_template' );
```

### Template Hierarchy Hook

```php
// Modify template hierarchy
function modify_template_hierarchy( $templates ) {
    if ( is_single() && get_post_type() === 'product' ) {
        // Add custom template to hierarchy
        $templates[] = 'single-product-custom.php';
    }
    return $templates;
}
add_filter( 'single_template_hierarchy', 'modify_template_hierarchy' );
```

## Debugging Template Hierarchy

### Template Hierarchy Plugin

Install the "Template Hierarchy" plugin to see which template WordPress is using:

```php
// Or add this to functions.php for debugging
function debug_template_hierarchy() {
    if ( current_user_can( 'manage_options' ) && isset( $_GET['debug_template'] ) ) {
        global $template;
        echo '<div style="background: #f0f0f0; padding: 10px; margin: 10px 0;">';
        echo '<strong>Current Template:</strong> ' . basename( $template );
        echo '</div>';
    }
}
add_action( 'wp_footer', 'debug_template_hierarchy' );
```

### Template Hierarchy Query

```php
// Debug current query
function debug_current_query() {
    if ( WP_DEBUG && current_user_can( 'manage_options' ) ) {
        global $wp_query;
        echo '<pre style="background: #f0f0f0; padding: 10px;">';
        echo 'Query Object: ' . print_r( $wp_query->query_vars, true );
        echo '</pre>';
    }
}
add_action( 'wp_footer', 'debug_current_query' );
```

## Best Practices

### Template Organization

```php
// Organize templates logically
/
├── index.php                      // Main template
├── single.php                     // Single post
├── page.php                       // Single page
├── archive.php                    // Archives
├── category.php                   // Category archives
├── tag.php                        // Tag archives
├── author.php                     // Author archives
├── search.php                     // Search results
├── 404.php                        // 404 page
└── template-parts/                // Reusable parts
    ├── content.php
    ├── content-single.php
    ├── content-page.php
    └── content-none.php
```

### Template Part Usage

```php
// Use template parts for reusability
get_template_part( 'template-parts/content', get_post_format() );
get_template_part( 'template-parts/loop', 'grid' );
get_template_part( 'template-parts/header', 'minimal' );
```

### Conditional Template Loading

```php
// Load different templates based on conditions
function load_conditional_template( $template ) {
    if ( is_single() && has_category( 'featured' ) ) {
        $new_template = locate_template( 'single-featured.php' );
        if ( $new_template ) {
            return $new_template;
        }
    }
    return $template;
}
add_filter( 'template_include', 'load_conditional_template' );
```

## Common Issues and Solutions

### Template Not Loading

```php
// Check if template exists
if ( locate_template( 'custom-template.php' ) ) {
    // Template exists
} else {
    // Template doesn't exist
}

// Flush rewrite rules if needed
flush_rewrite_rules();
```

### Template Hierarchy Not Working

```php
// Ensure proper file naming
// Check file permissions
// Verify template is in correct directory
// Check for syntax errors in template file
```

## Official Documentation

https://developer.wordpress.org/themes/basics/template-hierarchy/
https://developer.wordpress.org/reference/functions/locate_template/
https://developer.wordpress.org/reference/functions/get_template_part/
