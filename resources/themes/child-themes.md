# WordPress Child Themes

Child themes allow you to modify an existing theme without losing your changes when the parent theme updates.

## Child Theme Structure

### Basic Child Theme Files

```
my-child-theme/
├── style.css
├── functions.php
├── index.php (optional)
├── single.php (optional)
├── page.php (optional)
├── screenshot.png (optional)
└── assets/
    ├── css/
    │   └── custom.css
    ├── js/
    │   └── custom.js
    └── images/
        └── logo.png
```

### Child Theme Style.css

```css
/*
Theme Name: My Child Theme
Description: Child theme of Twenty Twenty-Three
Author: Your Name
Version: 1.0.0
Template: twentytwentythree
Text Domain: my-child-theme
*/

/* Import parent theme styles */
@import url("../twentytwentythree/style.css");

/* Custom styles */
.site-header {
    background-color: #0073aa;
    padding: 1rem 0;
}

.site-title a {
    color: #ffffff;
    text-decoration: none;
}

.site-title a:hover {
    color: #f0f0f0;
}

/* Custom button styles */
.btn-primary {
    background-color: #ff6b35;
    border: none;
    padding: 12px 24px;
    border-radius: 4px;
    color: white;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.btn-primary:hover {
    background-color: #e55a2b;
}

/* Responsive design */
@media (max-width: 768px) {
    .site-header {
        padding: 0.5rem 0;
    }
    
    .site-title {
        font-size: 1.5rem;
    }
}
```

## Child Theme Functions

### Basic functions.php

```php
<?php
/**
 * Child theme functions and definitions
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Enqueue parent and child theme styles
 */
function my_child_theme_enqueue_styles() {
    // Enqueue parent theme style
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
    
    // Enqueue child theme style
    wp_enqueue_style('child-style', 
        get_stylesheet_directory_uri() . '/style.css',
        array('parent-style'),
        wp_get_theme()->get('Version')
    );
    
    // Enqueue custom CSS
    wp_enqueue_style('child-custom-css',
        get_stylesheet_directory_uri() . '/assets/css/custom.css',
        array('child-style'),
        wp_get_theme()->get('Version')
    );
    
    // Enqueue custom JavaScript
    wp_enqueue_script('child-custom-js',
        get_stylesheet_directory_uri() . '/assets/js/custom.js',
        array('jquery'),
        wp_get_theme()->get('Version'),
        true
    );
}
add_action('wp_enqueue_scripts', 'my_child_theme_enqueue_styles');

/**
 * Add theme support for additional features
 */
function my_child_theme_setup() {
    // Add custom logo support
    add_theme_support('custom-logo', array(
        'height'      => 100,
        'width'       => 400,
        'flex-height' => true,
        'flex-width'  => true,
    ));
    
    // Add post thumbnail support
    add_theme_support('post-thumbnails');
    
    // Add custom image sizes
    add_image_size('custom-thumbnail', 300, 200, true);
    add_image_size('custom-large', 800, 600, true);
    
    // Add HTML5 support
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script'
    ));
}
add_action('after_setup_theme', 'my_child_theme_setup');

/**
 * Register custom navigation menus
 */
function my_child_theme_menus() {
    register_nav_menus(array(
        'primary' => __('Primary Menu', 'my-child-theme'),
        'footer'  => __('Footer Menu', 'my-child-theme'),
        'social'  => __('Social Menu', 'my-child-theme')
    ));
}
add_action('init', 'my_child_theme_menus');

/**
 * Register widget areas
 */
function my_child_theme_widgets_init() {
    register_sidebar(array(
        'name'          => __('Custom Sidebar', 'my-child-theme'),
        'id'            => 'custom-sidebar',
        'description'   => __('Add widgets here to appear in your custom sidebar.', 'my-child-theme'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h2 class="widget-title">',
        'after_title'   => '</h2>',
    ));
}
add_action('widgets_init', 'my_child_theme_widgets_init');
```

## Template Overrides

### Override Parent Theme Templates

```php
<?php
/**
 * Single post template for child theme
 */

get_header(); ?>

<div class="container">
    <div class="row">
        <div class="col-md-8">
            <?php while (have_posts()) : the_post(); ?>
                <article id="post-<?php the_ID(); ?>" <?php post_class('single-post'); ?>>
                    <header class="entry-header">
                        <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
                        
                        <div class="entry-meta">
                            <span class="posted-on">
                                <?php echo get_the_date(); ?>
                            </span>
                            <span class="byline">
                                <?php _e('by', 'my-child-theme'); ?> 
                                <span class="author vcard">
                                    <?php the_author(); ?>
                                </span>
                            </span>
                        </div>
                    </header>
                    
                    <?php if (has_post_thumbnail()) : ?>
                        <div class="entry-thumbnail">
                            <?php the_post_thumbnail('custom-large'); ?>
                        </div>
                    <?php endif; ?>
                    
                    <div class="entry-content">
                        <?php the_content(); ?>
                    </div>
                    
                    <footer class="entry-footer">
                        <?php
                        $tags = get_the_tags();
                        if ($tags) {
                            echo '<div class="post-tags">';
                            echo '<strong>' . __('Tags:', 'my-child-theme') . '</strong> ';
                            the_tags('', ', ', '');
                            echo '</div>';
                        }
                        ?>
                    </footer>
                </article>
                
                <?php
                // Custom navigation
                the_post_navigation(array(
                    'prev_text' => '<span class="nav-subtitle">' . __('Previous:', 'my-child-theme') . '</span> <span class="nav-title">%title</span>',
                    'next_text' => '<span class="nav-subtitle">' . __('Next:', 'my-child-theme') . '</span> <span class="nav-title">%title</span>',
                ));
                
                // Comments
                if (comments_open() || get_comments_number()) {
                    comments_template();
                }
                ?>
                
            <?php endwhile; ?>
        </div>
        
        <div class="col-md-4">
            <?php get_sidebar(); ?>
        </div>
    </div>
</div>

<?php get_footer(); ?>
```

### Custom Page Template

```php
<?php
/**
 * Template Name: Custom Page Template
 * Description: A custom page template for the child theme
 */

get_header(); ?>

<div class="custom-page-template">
    <div class="container">
        <div class="row">
            <div class="col-12">
                <header class="page-header">
                    <h1 class="page-title"><?php the_title(); ?></h1>
                </header>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-8">
                <div class="page-content">
                    <?php while (have_posts()) : the_post(); ?>
                        <div class="entry-content">
                            <?php the_content(); ?>
                        </div>
                    <?php endwhile; ?>
                </div>
            </div>
            
            <div class="col-md-4">
                <aside class="page-sidebar">
                    <?php
                    // Custom sidebar content
                    if (is_active_sidebar('custom-sidebar')) {
                        dynamic_sidebar('custom-sidebar');
                    }
                    ?>
                </aside>
            </div>
        </div>
    </div>
</div>

<?php get_footer(); ?>
```

## Advanced Child Theme Features

### Custom Post Types and Taxonomies

```php
<?php
/**
 * Register custom post types and taxonomies
 */

// Register custom post type
function my_child_theme_custom_post_types() {
    register_post_type('portfolio', array(
        'labels' => array(
            'name' => __('Portfolio', 'my-child-theme'),
            'singular_name' => __('Portfolio Item', 'my-child-theme'),
            'add_new' => __('Add New', 'my-child-theme'),
            'add_new_item' => __('Add New Portfolio Item', 'my-child-theme'),
            'edit_item' => __('Edit Portfolio Item', 'my-child-theme'),
            'new_item' => __('New Portfolio Item', 'my-child-theme'),
            'view_item' => __('View Portfolio Item', 'my-child-theme'),
            'search_items' => __('Search Portfolio', 'my-child-theme'),
            'not_found' => __('No portfolio items found', 'my-child-theme'),
            'not_found_in_trash' => __('No portfolio items found in trash', 'my-child-theme')
        ),
        'public' => true,
        'has_archive' => true,
        'menu_icon' => 'dashicons-portfolio',
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
        'rewrite' => array('slug' => 'portfolio'),
        'show_in_rest' => true
    ));
}
add_action('init', 'my_child_theme_custom_post_types');

// Register custom taxonomy
function my_child_theme_custom_taxonomies() {
    register_taxonomy('portfolio_category', 'portfolio', array(
        'labels' => array(
            'name' => __('Portfolio Categories', 'my-child-theme'),
            'singular_name' => __('Portfolio Category', 'my-child-theme'),
            'search_items' => __('Search Categories', 'my-child-theme'),
            'all_items' => __('All Categories', 'my-child-theme'),
            'parent_item' => __('Parent Category', 'my-child-theme'),
            'parent_item_colon' => __('Parent Category:', 'my-child-theme'),
            'edit_item' => __('Edit Category', 'my-child-theme'),
            'update_item' => __('Update Category', 'my-child-theme'),
            'add_new_item' => __('Add New Category', 'my-child-theme'),
            'new_item_name' => __('New Category Name', 'my-child-theme'),
            'menu_name' => __('Categories', 'my-child-theme')
        ),
        'hierarchical' => true,
        'public' => true,
        'show_in_rest' => true,
        'rewrite' => array('slug' => 'portfolio-category')
    ));
}
add_action('init', 'my_child_theme_custom_taxonomies');
```

### Custom Widget

```php
<?php
/**
 * Custom widget for child theme
 */

class My_Custom_Widget extends WP_Widget {
    
    public function __construct() {
        parent::__construct(
            'my_custom_widget',
            __('Custom Widget', 'my-child-theme'),
            array('description' => __('A custom widget for the child theme', 'my-child-theme'))
        );
    }
    
    public function widget($args, $instance) {
        $title = apply_filters('widget_title', $instance['title']);
        $text = $instance['text'];
        
        echo $args['before_widget'];
        
        if (!empty($title)) {
            echo $args['before_title'] . $title . $args['after_title'];
        }
        
        if (!empty($text)) {
            echo '<div class="widget-text">' . wpautop($text) . '</div>';
        }
        
        echo $args['after_widget'];
    }
    
    public function form($instance) {
        $title = isset($instance['title']) ? $instance['title'] : '';
        $text = isset($instance['text']) ? $instance['text'] : '';
        ?>
        <p>
            <label for="<?php echo $this->get_field_id('title'); ?>"><?php _e('Title:', 'my-child-theme'); ?></label>
            <input class="widefat" id="<?php echo $this->get_field_id('title'); ?>" name="<?php echo $this->get_field_name('title'); ?>" type="text" value="<?php echo esc_attr($title); ?>">
        </p>
        <p>
            <label for="<?php echo $this->get_field_id('text'); ?>"><?php _e('Text:', 'my-child-theme'); ?></label>
            <textarea class="widefat" id="<?php echo $this->get_field_id('text'); ?>" name="<?php echo $this->get_field_name('text'); ?>" rows="5"><?php echo esc_textarea($text); ?></textarea>
        </p>
        <?php
    }
    
    public function update($new_instance, $old_instance) {
        $instance = array();
        $instance['title'] = (!empty($new_instance['title'])) ? strip_tags($new_instance['title']) : '';
        $instance['text'] = (!empty($new_instance['text'])) ? $new_instance['text'] : '';
        return $instance;
    }
}

// Register the widget
function register_my_custom_widget() {
    register_widget('My_Custom_Widget');
}
add_action('widgets_init', 'register_my_custom_widget');
```

## Child Theme Best Practices

### Security and Performance

```php
<?php
/**
 * Security and performance improvements for child theme
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Remove unnecessary WordPress features
 */
function my_child_theme_cleanup() {
    // Remove WordPress version from head
    remove_action('wp_head', 'wp_generator');
    
    // Remove unnecessary links from head
    remove_action('wp_head', 'wlwmanifest_link');
    remove_action('wp_head', 'rsd_link');
    remove_action('wp_head', 'wp_shortlink_wp_head');
    
    // Remove emoji scripts
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('wp_print_styles', 'print_emoji_styles');
    remove_action('admin_print_scripts', 'print_emoji_detection_script');
    remove_action('admin_print_styles', 'print_emoji_styles');
}
add_action('init', 'my_child_theme_cleanup');

/**
 * Optimize database queries
 */
function my_child_theme_optimize_queries($query) {
    if (!is_admin() && $query->is_main_query()) {
        // Limit posts per page for better performance
        if (is_home()) {
            $query->set('posts_per_page', 10);
        }
        
        // Optimize category queries
        if (is_category()) {
            $query->set('posts_per_page', 12);
        }
    }
}
add_action('pre_get_posts', 'my_child_theme_optimize_queries');

/**
 * Add security headers
 */
function my_child_theme_security_headers() {
    if (!is_admin()) {
        header('X-Content-Type-Options: nosniff');
        header('X-Frame-Options: SAMEORIGIN');
        header('X-XSS-Protection: 1; mode=block');
    }
}
add_action('send_headers', 'my_child_theme_security_headers');
```

### Customizer Integration

```php
<?php
/**
 * WordPress Customizer integration for child theme
 */

function my_child_theme_customize_register($wp_customize) {
    // Add custom section
    $wp_customize->add_section('my_child_theme_options', array(
        'title' => __('Child Theme Options', 'my-child-theme'),
        'priority' => 30
    ));
    
    // Add custom setting
    $wp_customize->add_setting('custom_color', array(
        'default' => '#0073aa',
        'sanitize_callback' => 'sanitize_hex_color'
    ));
    
    // Add custom control
    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'custom_color', array(
        'label' => __('Custom Color', 'my-child-theme'),
        'section' => 'my_child_theme_options',
        'settings' => 'custom_color'
    )));
    
    // Add text setting
    $wp_customize->add_setting('custom_text', array(
        'default' => '',
        'sanitize_callback' => 'sanitize_text_field'
    ));
    
    $wp_customize->add_control('custom_text', array(
        'label' => __('Custom Text', 'my-child-theme'),
        'section' => 'my_child_theme_options',
        'type' => 'text'
    ));
}
add_action('customize_register', 'my_child_theme_customize_register');

/**
 * Output customizer CSS
 */
function my_child_theme_customizer_css() {
    $custom_color = get_theme_mod('custom_color', '#0073aa');
    ?>
    <style type="text/css">
        .custom-color {
            color: <?php echo esc_attr($custom_color); ?> !important;
        }
        
        .custom-background {
            background-color: <?php echo esc_attr($custom_color); ?> !important;
        }
    </style>
    <?php
}
add_action('wp_head', 'my_child_theme_customizer_css');
```

### Internationalization

```php
<?php
/**
 * Internationalization for child theme
 */

/**
 * Load theme textdomain
 */
function my_child_theme_load_textdomain() {
    load_child_theme_textdomain('my-child-theme', get_stylesheet_directory() . '/languages');
}
add_action('after_setup_theme', 'my_child_theme_load_textdomain');

/**
 * Add custom strings for translation
 */
function my_child_theme_translation_strings() {
    // Example strings
    __('Read More', 'my-child-theme');
    __('Previous Post', 'my-child-theme');
    __('Next Post', 'my-child-theme');
    __('Posted on', 'my-child-theme');
    __('By', 'my-child-theme');
}
```

## Child Theme for Block Themes

### Block Theme Child Structure

```
my-block-child-theme/
├── style.css
├── functions.php
├── theme.json (optional - overrides parent)
├── templates/
│   ├── index.html (optional)
│   └── single.html (optional)
├── template-parts/
│   ├── header.html (optional)
│   └── footer.html (optional)
└── patterns/
    └── my-pattern.php (optional)
```

### Block Theme Child functions.php

```php
<?php
/**
 * Block theme child functions
 */

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Enqueue parent theme styles
 */
function my_block_child_theme_enqueue_styles() {
    // Enqueue parent theme style
    wp_enqueue_style('parent-style', get_template_directory_uri() . '/style.css');
    
    // Enqueue child theme style
    wp_enqueue_style('child-style', 
        get_stylesheet_directory_uri() . '/style.css',
        array('parent-style'),
        wp_get_theme()->get('Version')
    );
}
add_action('wp_enqueue_scripts', 'my_block_child_theme_enqueue_styles');

/**
 * Override parent theme.json settings
 */
function my_block_child_theme_override_theme_json() {
    // This would be handled by theme.json in the child theme
    // if you want to override parent theme settings
}
```

## Official Documentation

https://developer.wordpress.org/themes/advanced-topics/child-themes/
https://developer.wordpress.org/themes/basics/template-hierarchy/
https://developer.wordpress.org/themes/block-themes/
