# Underscores Framework

Comprehensive guide to Underscores (_s) - the official WordPress starter theme for professional theme development.

## Underscores Fundamentals

### Installation and Setup

```bash
# Install Underscores via WP-CLI
wp scaffold _s your-theme-name --theme_name="Your Theme Name" --author="Your Name" --author_uri="https://example.com" --sassify

# Or download from underscores.me
# Visit https://underscores.me/ and fill out the form

# Manual installation
git clone https://github.com/automattic/_s.git your-theme-name
cd your-theme-name
rm -rf .git
```

### Basic Theme Structure

```php
// style.css - Theme header
/*
Theme Name: Your Theme Name
Description: A custom WordPress theme built with Underscores
Author: Your Name
Author URI: https://example.com
Version: 1.0.0
License: GPL v2 or later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: your-theme-name
Domain Path: /languages
*/

// functions.php - Main theme functions
function your_theme_name_setup() {
    // Make theme available for translation
    load_theme_textdomain('your-theme-name', get_template_directory() . '/languages');

    // Add default posts and comments RSS feed links to head
    add_theme_support('automatic-feed-links');

    // Let WordPress manage the document title
    add_theme_support('title-tag');

    // Enable support for Post Thumbnails on posts and pages
    add_theme_support('post-thumbnails');

    // This theme uses wp_nav_menu() in one location
    register_nav_menus(array(
        'menu-1' => esc_html__('Primary', 'your-theme-name'),
    ));

    // Switch default core markup for search form, comment form, and comments
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script',
    ));

    // Add theme support for selective refresh for widgets
    add_theme_support('customize-selective-refresh-widgets');

    // Add support for core custom logo
    add_theme_support('custom-logo', array(
        'height'      => 250,
        'width'       => 250,
        'flex-width'  => true,
        'flex-height' => true,
    ));
}
add_action('after_setup_theme', 'your_theme_name_setup');

// Set the content width in pixels, based on the theme's design and stylesheet
function your_theme_name_content_width() {
    $GLOBALS['content_width'] = apply_filters('your_theme_name_content_width', 640);
}
add_action('after_setup_theme', 'your_theme_name_content_width', 0);

// Register widget areas
function your_theme_name_widgets_init() {
    register_sidebar(array(
        'name'          => esc_html__('Sidebar', 'your-theme-name'),
        'id'            => 'sidebar-1',
        'description'   => esc_html__('Add widgets here.', 'your-theme-name'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h2 class="widget-title">',
        'after_title'   => '</h2>',
    ));
}
add_action('widgets_init', 'your_theme_name_widgets_init');

// Enqueue scripts and styles
function your_theme_name_scripts() {
    wp_enqueue_style('your-theme-name-style', get_stylesheet_uri(), array(), _S_VERSION);
    wp_style_add_data('your-theme-name-style', 'rtl', 'replace');

    wp_enqueue_script('your-theme-name-navigation', get_template_directory_uri() . '/js/navigation.js', array(), _S_VERSION, true);

    if (is_singular() && comments_open() && get_option('thread_comments')) {
        wp_enqueue_script('comment-reply');
    }
}
add_action('wp_enqueue_scripts', 'your_theme_name_scripts');
```

## Template Structure

### Header Template

```php
// header.php
<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">

    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<div id="page" class="site">
    <a class="skip-link screen-reader-text" href="#primary"><?php esc_html_e('Skip to content', 'your-theme-name'); ?></a>

    <header id="masthead" class="site-header">
        <div class="site-branding">
            <?php
            the_custom_logo();
            if (is_front_page() && is_home()) :
                ?>
                <h1 class="site-title"><a href="<?php echo esc_url(home_url('/')); ?>" rel="home"><?php bloginfo('name'); ?></a></h1>
                <?php
            else :
                ?>
                <p class="site-title"><a href="<?php echo esc_url(home_url('/')); ?>" rel="home"><?php bloginfo('name'); ?></a></p>
                <?php
            endif;
            $your_theme_name_description = get_bloginfo('description', 'display');
            if ($your_theme_name_description || is_customize_preview()) :
                ?>
                <p class="site-description"><?php echo $your_theme_name_description; /* WPCS: xss ok. */ ?></p>
            <?php endif; ?>
        </div><!-- .site-branding -->

        <nav id="site-navigation" class="main-navigation">
            <button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false"><?php esc_html_e('Primary Menu', 'your-theme-name'); ?></button>
            <?php
            wp_nav_menu(array(
                'theme_location' => 'menu-1',
                'menu_id'        => 'primary-menu',
            ));
            ?>
        </nav><!-- #site-navigation -->
    </header><!-- #masthead -->

    <div id="content" class="site-content">
```

### Footer Template

```php
// footer.php
    </div><!-- #content -->

    <footer id="colophon" class="site-footer">
        <div class="site-info">
            <a href="<?php echo esc_url(__('https://wordpress.org/', 'your-theme-name')); ?>">
                <?php
                /* translators: %s: CMS name, i.e. WordPress. */
                printf(esc_html__('Proudly powered by %s', 'your-theme-name'), 'WordPress');
                ?>
            </a>
            <span class="sep"> | </span>
                <?php
                /* translators: 1: Theme name, 2: Theme author. */
                printf(esc_html__('Theme: %1$s by %2$s.', 'your-theme-name'), 'your-theme-name', '<a href="https://example.com">Your Name</a>');
                ?>
        </div><!-- .site-info -->
    </footer><!-- #colophon -->
</div><!-- #page -->

<?php wp_footer(); ?>

</body>
</html>
```

### Index Template

```php
// index.php
get_header();
?>

<main id="primary" class="site-main">

    <?php if (have_posts()) : ?>

        <?php if (is_home() && !is_front_page()) : ?>
            <header>
                <h1 class="page-title screen-reader-text"><?php single_post_title(); ?></h1>
            </header>
        <?php endif; ?>

        <?php
        /* Start the Loop */
        while (have_posts()) :
            the_post();

            /*
             * Include the Post-Type-specific template for the content.
             * If you want to override this in a child theme, then include a file
             * called content-___.php (where ___ is the Post Type name) and that will be used instead.
             */
            get_template_part('template-parts/content', get_post_type());

        endwhile;

        the_posts_navigation();

    else :

        get_template_part('template-parts/content', 'none');

    endif;
    ?>

</main><!-- #main -->

<?php
get_sidebar();
get_footer();
```

### Content Template Parts

```php
// template-parts/content.php
<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <header class="entry-header">
        <?php
        if (is_singular()) :
            the_title('<h1 class="entry-title">', '</h1>');
        else :
            the_title('<h2 class="entry-title"><a href="' . esc_url(get_permalink()) . '" rel="bookmark">', '</a></h2>');
        endif;

        if ('post' === get_post_type()) :
            ?>
            <div class="entry-meta">
                <?php
                your_theme_name_posted_on();
                your_theme_name_posted_by();
                ?>
            </div><!-- .entry-meta -->
        <?php endif; ?>
    </header><!-- .entry-header -->

    <?php your_theme_name_post_thumbnail(); ?>

    <div class="entry-content">
        <?php
        the_content(
            sprintf(
                wp_kses(
                    /* translators: %s: Name of current post. Only visible to screen readers */
                    __('Continue reading<span class="screen-reader-text"> "%s"</span>', 'your-theme-name'),
                    array(
                        'span' => array(
                            'class' => array(),
                        ),
                    )
                ),
                wp_kses_post(get_the_title())
            )
        );

        wp_link_pages(array(
            'before' => '<div class="page-links">' . esc_html__('Pages:', 'your-theme-name'),
            'after'  => '</div>',
        ));
        ?>
    </div><!-- .entry-content -->

    <footer class="entry-footer">
        <?php your_theme_name_entry_footer(); ?>
    </footer><!-- .entry-footer -->
</article><!-- #post-<?php the_ID(); ?> -->
```

## Template Functions

### Template Tags

```php
// inc/template-functions.php
// Template tags for Underscores theme

if (!function_exists('your_theme_name_posted_on')) :
    /**
     * Prints HTML with meta information for the current post-date/time.
     */
    function your_theme_name_posted_on() {
        $time_string = '<time class="entry-date published updated" datetime="%1$s">%2$s</time>';
        if (get_the_time('U') !== get_the_modified_time('U')) {
            $time_string = '<time class="entry-date published" datetime="%1$s">%2$s</time><time class="updated" datetime="%3$s">%4$s</time>';
        }

        $time_string = sprintf(
            $time_string,
            esc_attr(get_the_date(DATE_W3C)),
            esc_html(get_the_date()),
            esc_attr(get_the_modified_date(DATE_W3C)),
            esc_html(get_the_modified_date())
        );

        $posted_on = sprintf(
            /* translators: %s: post date. */
            esc_html_x('Posted on %s', 'post date', 'your-theme-name'),
            '<a href="' . esc_url(get_permalink()) . '" rel="bookmark">' . $time_string . '</a>'
        );

        echo '<span class="posted-on">' . $posted_on . '</span>'; // WPCS: XSS OK.

    }
endif;

if (!function_exists('your_theme_name_posted_by')) :
    /**
     * Prints HTML with meta information for the current author.
     */
    function your_theme_name_posted_by() {
        $byline = sprintf(
            /* translators: %s: post author. */
            esc_html_x('by %s', 'post author', 'your-theme-name'),
            '<span class="author vcard"><a class="url fn n" href="' . esc_url(get_author_posts_url(get_the_author_meta('ID'))) . '">' . esc_html(get_the_author()) . '</a></span>'
        );

        echo '<span class="byline"> ' . $byline . '</span>'; // WPCS: XSS OK.

    }
endif;

if (!function_exists('your_theme_name_entry_footer')) :
    /**
     * Prints HTML with meta information for the categories, tags and comments.
     */
    function your_theme_name_entry_footer() {
        // Hide category and tag text for pages.
        if ('post' === get_post_type()) {
            /* translators: used between list items, there is a space after the comma */
            $categories_list = get_the_category_list(esc_html__(', ', 'your-theme-name'));
            if ($categories_list) {
                /* translators: 1: list of categories. */
                printf('<span class="cat-links">' . esc_html__('Posted in %1$s', 'your-theme-name') . '</span>', $categories_list); // WPCS: XSS OK.
            }

            /* translators: used between list items, there is a space after the comma */
            $tags_list = get_the_tag_list('', esc_html_x(', ', 'list item separator', 'your-theme-name'));
            if ($tags_list) {
                /* translators: 1: list of tags. */
                printf('<span class="tags-links">' . esc_html__('Tagged %1$s', 'your-theme-name') . '</span>', $tags_list); // WPCS: XSS OK.
            }
        }

        if (!is_single() && !post_password_required() && (comments_open() || get_comments_number())) {
            echo '<span class="comments-link">';
            comments_popup_link(
                sprintf(
                    wp_kses(
                        /* translators: %s: post title */
                        __('Leave a Comment<span class="screen-reader-text"> on %s</span>', 'your-theme-name'),
                        array(
                            'span' => array(
                                'class' => array(),
                            ),
                        )
                    ),
                    wp_kses_post(get_the_title())
                )
            );
            echo '</span>';
        }

        edit_post_link(
            sprintf(
                wp_kses(
                    /* translators: %s: Name of current post. Only visible to screen readers */
                    __('Edit <span class="screen-reader-text">%s</span>', 'your-theme-name'),
                    array(
                        'span' => array(
                            'class' => array(),
                        ),
                    )
                ),
                wp_kses_post(get_the_title())
            ),
            '<span class="edit-link">',
            '</span>'
        );
    }
endif;

if (!function_exists('your_theme_name_post_thumbnail')) :
    /**
     * Displays an optional post thumbnail.
     *
     * Wraps the post thumbnail in an anchor element on index views, or a div
     * element when on single views.
     */
    function your_theme_name_post_thumbnail() {
        if (post_password_required() || is_attachment() || !has_post_thumbnail()) {
            return;
        }

        if (is_singular()) :
            ?>
            <div class="post-thumbnail">
                <?php the_post_thumbnail(); ?>
            </div><!-- .post-thumbnail -->
        <?php else : ?>
        <a class="post-thumbnail" href="<?php the_permalink(); ?>" aria-hidden="true" tabindex="-1">
            <?php
            the_post_thumbnail(
                'post-thumbnail',
                array(
                    'alt' => the_title_attribute(
                        array(
                            'echo' => false,
                        )
                    ),
                )
            );
            ?>
        </a>
            <?php
        endif; // End is_singular().
    }
endif;
```

## Custom Post Types and Taxonomies

### Custom Post Type Registration

```php
// inc/custom-post-types.php
function your_theme_name_register_custom_post_types() {
    // Portfolio Post Type
    register_post_type('portfolio', array(
        'labels' => array(
            'name' => 'Portfolio',
            'singular_name' => 'Portfolio Item',
            'add_new' => 'Add New Item',
            'add_new_item' => 'Add New Portfolio Item',
            'edit_item' => 'Edit Portfolio Item',
            'new_item' => 'New Portfolio Item',
            'view_item' => 'View Portfolio Item',
            'search_items' => 'Search Portfolio',
            'not_found' => 'No portfolio items found',
            'not_found_in_trash' => 'No portfolio items found in trash',
            'parent_item_colon' => 'Parent Portfolio Item:',
            'menu_name' => 'Portfolio',
        ),
        'public' => true,
        'has_archive' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_rest' => true,
        'query_var' => true,
        'rewrite' => array('slug' => 'portfolio'),
        'capability_type' => 'post',
        'hierarchical' => false,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-portfolio',
        'supports' => array('title', 'editor', 'author', 'thumbnail', 'excerpt', 'comments', 'custom-fields'),
    ));

    // Testimonial Post Type
    register_post_type('testimonial', array(
        'labels' => array(
            'name' => 'Testimonials',
            'singular_name' => 'Testimonial',
            'add_new' => 'Add New Testimonial',
            'add_new_item' => 'Add New Testimonial',
            'edit_item' => 'Edit Testimonial',
            'new_item' => 'New Testimonial',
            'view_item' => 'View Testimonial',
            'search_items' => 'Search Testimonials',
            'not_found' => 'No testimonials found',
            'not_found_in_trash' => 'No testimonials found in trash',
            'menu_name' => 'Testimonials',
        ),
        'public' => true,
        'has_archive' => false,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_rest' => true,
        'query_var' => true,
        'rewrite' => array('slug' => 'testimonial'),
        'capability_type' => 'post',
        'hierarchical' => false,
        'menu_position' => 6,
        'menu_icon' => 'dashicons-format-quote',
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields'),
    ));
}
add_action('init', 'your_theme_name_register_custom_post_types');

// Custom Taxonomies
function your_theme_name_register_custom_taxonomies() {
    // Portfolio Category
    register_taxonomy('portfolio_category', 'portfolio', array(
        'labels' => array(
            'name' => 'Portfolio Categories',
            'singular_name' => 'Portfolio Category',
            'search_items' => 'Search Portfolio Categories',
            'all_items' => 'All Portfolio Categories',
            'parent_item' => 'Parent Portfolio Category',
            'parent_item_colon' => 'Parent Portfolio Category:',
            'edit_item' => 'Edit Portfolio Category',
            'update_item' => 'Update Portfolio Category',
            'add_new_item' => 'Add New Portfolio Category',
            'new_item_name' => 'New Portfolio Category Name',
            'menu_name' => 'Portfolio Categories',
        ),
        'hierarchical' => true,
        'public' => true,
        'show_ui' => true,
        'show_admin_column' => true,
        'show_in_nav_menus' => true,
        'show_tagcloud' => true,
        'show_in_rest' => true,
        'rewrite' => array('slug' => 'portfolio-category'),
    ));

    // Portfolio Tag
    register_taxonomy('portfolio_tag', 'portfolio', array(
        'labels' => array(
            'name' => 'Portfolio Tags',
            'singular_name' => 'Portfolio Tag',
            'search_items' => 'Search Portfolio Tags',
            'popular_items' => 'Popular Portfolio Tags',
            'all_items' => 'All Portfolio Tags',
            'edit_item' => 'Edit Portfolio Tag',
            'update_item' => 'Update Portfolio Tag',
            'add_new_item' => 'Add New Portfolio Tag',
            'new_item_name' => 'New Portfolio Tag Name',
            'separate_items_with_commas' => 'Separate portfolio tags with commas',
            'add_or_remove_items' => 'Add or remove portfolio tags',
            'choose_from_most_used' => 'Choose from the most used portfolio tags',
            'menu_name' => 'Portfolio Tags',
        ),
        'hierarchical' => false,
        'public' => true,
        'show_ui' => true,
        'show_admin_column' => true,
        'show_in_nav_menus' => true,
        'show_tagcloud' => true,
        'show_in_rest' => true,
        'rewrite' => array('slug' => 'portfolio-tag'),
    ));
}
add_action('init', 'your_theme_name_register_custom_taxonomies');
```

## Customizer Integration

### Customizer Options

```php
// inc/customizer.php
function your_theme_name_customize_register($wp_customize) {
    // Add Theme Options Panel
    $wp_customize->add_panel('your_theme_name_options', array(
        'title' => __('Theme Options', 'your-theme-name'),
        'description' => __('Customize your theme options', 'your-theme-name'),
        'priority' => 160,
    ));

    // Header Section
    $wp_customize->add_section('your_theme_name_header', array(
        'title' => __('Header Settings', 'your-theme-name'),
        'panel' => 'your_theme_name_options',
    ));

    // Header Background Color
    $wp_customize->add_setting('your_theme_name_header_bg_color', array(
        'default' => '#ffffff',
        'sanitize_callback' => 'sanitize_hex_color',
    ));

    $wp_customize->add_control(new WP_Customize_Color_Control($wp_customize, 'your_theme_name_header_bg_color', array(
        'label' => __('Header Background Color', 'your-theme-name'),
        'section' => 'your_theme_name_header',
        'settings' => 'your_theme_name_header_bg_color',
    )));

    // Footer Section
    $wp_customize->add_section('your_theme_name_footer', array(
        'title' => __('Footer Settings', 'your-theme-name'),
        'panel' => 'your_theme_name_options',
    ));

    // Footer Text
    $wp_customize->add_setting('your_theme_name_footer_text', array(
        'default' => 'Copyright © 2023 Your Theme Name. All rights reserved.',
        'sanitize_callback' => 'sanitize_text_field',
    ));

    $wp_customize->add_control('your_theme_name_footer_text', array(
        'label' => __('Footer Text', 'your-theme-name'),
        'section' => 'your_theme_name_footer',
        'type' => 'textarea',
    ));

    // Social Media Section
    $wp_customize->add_section('your_theme_name_social', array(
        'title' => __('Social Media', 'your-theme-name'),
        'panel' => 'your_theme_name_options',
    ));

    // Social Media Links
    $social_networks = array(
        'facebook' => 'Facebook',
        'twitter' => 'Twitter',
        'instagram' => 'Instagram',
        'linkedin' => 'LinkedIn',
        'youtube' => 'YouTube',
    );

    foreach ($social_networks as $network => $label) {
        $wp_customize->add_setting("your_theme_name_social_{$network}", array(
            'default' => '',
            'sanitize_callback' => 'esc_url_raw',
        ));

        $wp_customize->add_control("your_theme_name_social_{$network}", array(
            'label' => __("{$label} URL", 'your-theme-name'),
            'section' => 'your_theme_name_social',
            'type' => 'url',
        ));
    }
}
add_action('customize_register', 'your_theme_name_customize_register');

// Customizer CSS
function your_theme_name_customizer_css() {
    $header_bg_color = get_theme_mod('your_theme_name_header_bg_color', '#ffffff');
    ?>
    <style type="text/css">
        .site-header {
            background-color: <?php echo esc_attr($header_bg_color); ?>;
        }
    </style>
    <?php
}
add_action('wp_head', 'your_theme_name_customizer_css');
```

## JavaScript and CSS

### Navigation JavaScript

```javascript
// js/navigation.js
(function() {
    'use strict';

    var mobileMenu = {
        init: function() {
            this.cacheDom();
            this.bindEvents();
        },

        cacheDom: function() {
            this.menuToggle = document.querySelector('.menu-toggle');
            this.menu = document.querySelector('.main-navigation');
            this.body = document.body;
        },

        bindEvents: function() {
            if (this.menuToggle) {
                this.menuToggle.addEventListener('click', this.toggleMenu.bind(this));
            }

            // Close menu when clicking outside
            document.addEventListener('click', this.closeMenuOnOutsideClick.bind(this));

            // Close menu on escape key
            document.addEventListener('keydown', this.closeMenuOnEscape.bind(this));
        },

        toggleMenu: function(e) {
            e.preventDefault();
            
            if (this.menu.classList.contains('toggled')) {
                this.closeMenu();
            } else {
                this.openMenu();
            }
        },

        openMenu: function() {
            this.menu.classList.add('toggled');
            this.menuToggle.classList.add('toggled');
            this.body.classList.add('menu-open');
            this.menuToggle.setAttribute('aria-expanded', 'true');
        },

        closeMenu: function() {
            this.menu.classList.remove('toggled');
            this.menuToggle.classList.remove('toggled');
            this.body.classList.remove('menu-open');
            this.menuToggle.setAttribute('aria-expanded', 'false');
        },

        closeMenuOnOutsideClick: function(e) {
            if (this.menu.classList.contains('toggled') && 
                !this.menu.contains(e.target) && 
                !this.menuToggle.contains(e.target)) {
                this.closeMenu();
            }
        },

        closeMenuOnEscape: function(e) {
            if (e.keyCode === 27 && this.menu.classList.contains('toggled')) {
                this.closeMenu();
            }
        }
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', mobileMenu.init.bind(mobileMenu));
    } else {
        mobileMenu.init();
    }
})();
```

### Responsive CSS

```scss
// sass/components/_navigation.scss
.main-navigation {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    
    ul {
        display: flex;
        list-style: none;
        margin: 0;
        padding: 0;
        
        li {
            position: relative;
            
            a {
                display: block;
                padding: 1rem;
                text-decoration: none;
                color: $color__text-main;
                transition: color 0.3s ease;
                
                &:hover,
                &:focus {
                    color: $color__link-hover;
                }
            }
            
            // Dropdown menu
            .sub-menu {
                position: absolute;
                top: 100%;
                left: 0;
                background: $color__background-body;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                min-width: 200px;
                opacity: 0;
                visibility: hidden;
                transform: translateY(-10px);
                transition: all 0.3s ease;
                
                li {
                    display: block;
                    
                    a {
                        padding: 0.75rem 1rem;
                        border-bottom: 1px solid $color__border-light;
                    }
                }
            }
            
            &:hover .sub-menu {
                opacity: 1;
                visibility: visible;
                transform: translateY(0);
            }
        }
    }
    
    // Mobile menu toggle
    .menu-toggle {
        display: none;
        background: none;
        border: none;
        padding: 0.5rem;
        cursor: pointer;
        
        @media screen and (max-width: 768px) {
            display: block;
        }
    }
    
    // Mobile menu styles
    @media screen and (max-width: 768px) {
        ul {
            display: none;
            width: 100%;
            flex-direction: column;
            position: absolute;
            top: 100%;
            left: 0;
            background: $color__background-body;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            
            &.toggled {
                display: flex;
            }
            
            li {
                width: 100%;
                
                .sub-menu {
                    position: static;
                    opacity: 1;
                    visibility: visible;
                    transform: none;
                    box-shadow: none;
                    background: $color__background-light;
                    
                    li a {
                        padding-left: 2rem;
                    }
                }
            }
        }
    }
}
```

## Underscores Best Practices

### Performance Optimization

```php
// inc/performance.php
function your_theme_name_performance_optimizations() {
    // Remove unnecessary WordPress features
    remove_action('wp_head', 'wp_generator');
    remove_action('wp_head', 'wlwmanifest_link');
    remove_action('wp_head', 'rsd_link');
    remove_action('wp_head', 'wp_shortlink_wp_head');
    
    // Remove emoji scripts
    remove_action('wp_head', 'print_emoji_detection_script', 7);
    remove_action('wp_print_styles', 'print_emoji_styles');
    remove_action('admin_print_scripts', 'print_emoji_detection_script');
    remove_action('admin_print_styles', 'print_emoji_styles');
    
    // Disable XML-RPC
    add_filter('xmlrpc_enabled', '__return_false');
    
    // Optimize queries
    add_action('pre_get_posts', 'your_theme_name_optimize_queries');
}
add_action('init', 'your_theme_name_performance_optimizations');

function your_theme_name_optimize_queries($query) {
    if (is_admin() || !$query->is_main_query()) {
        return;
    }
    
    // Limit posts per page
    if (is_home() || is_archive()) {
        $query->set('posts_per_page', 10);
    }
    
    // Optimize search queries
    if (is_search()) {
        $query->set('posts_per_page', 8);
    }
}
```

### Security Enhancements

```php
// inc/security.php
function your_theme_name_security_enhancements() {
    // Remove WordPress version
    remove_action('wp_head', 'wp_generator');
    
    // Disable file editing
    if (!defined('DISALLOW_FILE_EDIT')) {
        define('DISALLOW_FILE_EDIT', true);
    }
    
    // Security headers
    add_action('send_headers', 'your_theme_name_security_headers');
    
    // Sanitize inputs
    add_filter('pre_comment_content', 'your_theme_name_sanitize_comment');
}
add_action('init', 'your_theme_name_security_enhancements');

function your_theme_name_security_headers() {
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: SAMEORIGIN');
    header('X-XSS-Protection: 1; mode=block');
}

function your_theme_name_sanitize_comment($comment_content) {
    return wp_kses_post($comment_content);
}
```

## Underscores Examples

### Complete Theme Setup

```php
// functions.php - Complete setup
// Theme setup
your_theme_name_setup();

// Content width
your_theme_name_content_width();

// Widgets
your_theme_name_widgets_init();

// Scripts and styles
your_theme_name_scripts();

// Custom post types
your_theme_name_register_custom_post_types();

// Custom taxonomies
your_theme_name_register_custom_taxonomies();

// Performance optimizations
your_theme_name_performance_optimizations();

// Security enhancements
your_theme_name_security_enhancements();

// Include additional files
require get_template_directory() . '/inc/template-functions.php';
require get_template_directory() . '/inc/customizer.php';
require get_template_directory() . '/inc/custom-post-types.php';
require get_template_directory() . '/inc/performance.php';
require get_template_directory() . '/inc/security.php';
```

### Custom Page Template

```php
// page-portfolio.php
<?php
/*
Template Name: Portfolio Page
*/

get_header();
?>

<main id="primary" class="site-main">
    <header class="page-header">
        <h1 class="page-title"><?php the_title(); ?></h1>
        <?php if (get_the_content()) : ?>
            <div class="page-description">
                <?php the_content(); ?>
            </div>
        <?php endif; ?>
    </header>

    <?php
    $portfolio_query = new WP_Query(array(
        'post_type' => 'portfolio',
        'posts_per_page' => 12,
        'post_status' => 'publish',
    ));

    if ($portfolio_query->have_posts()) :
    ?>
        <div class="portfolio-grid">
            <?php while ($portfolio_query->have_posts()) : $portfolio_query->the_post(); ?>
                <article class="portfolio-item">
                    <?php if (has_post_thumbnail()) : ?>
                        <div class="portfolio-thumbnail">
                            <a href="<?php the_permalink(); ?>">
                                <?php the_post_thumbnail('medium'); ?>
                            </a>
                        </div>
                    <?php endif; ?>
                    
                    <div class="portfolio-content">
                        <h2 class="portfolio-title">
                            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                        </h2>
                        
                        <?php if (get_the_excerpt()) : ?>
                            <div class="portfolio-excerpt">
                                <?php the_excerpt(); ?>
                            </div>
                        <?php endif; ?>
                        
                        <div class="portfolio-meta">
                            <?php
                            $categories = get_the_terms(get_the_ID(), 'portfolio_category');
                            if ($categories && !is_wp_error($categories)) :
                                echo '<span class="portfolio-categories">';
                                foreach ($categories as $category) {
                                    echo '<span class="category">' . esc_html($category->name) . '</span>';
                                }
                                echo '</span>';
                            endif;
                            ?>
                        </div>
                    </div>
                </article>
            <?php endwhile; ?>
        </div>
        
        <?php
        // Pagination
        $total_pages = $portfolio_query->max_num_pages;
        if ($total_pages > 1) :
            $current_page = max(1, get_query_var('paged'));
            echo paginate_links(array(
                'total' => $total_pages,
                'current' => $current_page,
                'format' => '?paged=%#%',
                'prev_text' => __('Previous', 'your-theme-name'),
                'next_text' => __('Next', 'your-theme-name'),
            ));
        endif;
        ?>
        
    <?php else : ?>
        <p><?php _e('No portfolio items found.', 'your-theme-name'); ?></p>
    <?php endif; ?>
    
    <?php wp_reset_postdata(); ?>
</main>

<?php
get_footer();
```

## Official Documentation

https://underscores.me/
https://github.com/automattic/_s
https://developer.wordpress.org/themes/basics/template-hierarchy/
