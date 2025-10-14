# Timber Framework

Comprehensive guide to Timber Framework - modern WordPress development with Twig templating.

## Timber Fundamentals

### Installation and Setup

```php
// Install Timber via Composer
composer require timber/timber

// Or install via WordPress plugin
// Download from https://wordpress.org/plugins/timber-library/

// Initialize Timber in functions.php
function timber_setup() {
    // Check if Timber is loaded
    if (!class_exists('Timber\Timber')) {
        add_action('admin_notices', function() {
            echo '<div class="error"><p>Timber not activated. Make sure you activate the plugin.</p></div>';
        });
        add_filter('template_include', function($template) {
            return get_stylesheet_directory() . '/static/no-timber.html';
        });
        return;
    }
    
    // Set up Timber
    $timber = new \Timber\Timber();
    
    // Set Twig directories
    \Timber\Timber::$dirname = array('templates', 'views');
    
    // Set Twig cache (disable in development)
    if (WP_DEBUG) {
        \Timber\Timber::$cache = false;
    }
}

add_action('after_setup_theme', 'timber_setup');
```

### Basic Timber Usage

```php
// Basic Timber context setup
class Site extends \Timber\Site {
    
    public function __construct() {
        add_filter('timber_context', array($this, 'add_to_context'));
        add_filter('timber/twig', array($this, 'add_to_twig'));
        parent::__construct();
    }
    
    public function add_to_context($context) {
        $context['menu'] = new \Timber\Menu('primary');
        $context['site'] = $this;
        $context['custom_data'] = 'Hello Timber!';
        
        return $context;
    }
    
    public function add_to_twig($twig) {
        $twig->addExtension(new \Twig\Extension\StringLoaderExtension());
        $twig->addFilter(new \Twig\TwigFilter('myfilter', 'my_twig_filter'));
        
        return $twig;
    }
}

new Site();

// Basic template rendering
function render_template($template, $context = array()) {
    $context = \Timber\Timber::context($context);
    \Timber\Timber::render($template, $context);
}

// Usage in WordPress hooks
add_action('wp_head', function() {
    $context = \Timber\Timber::context();
    \Timber\Timber::render('partials/head.twig', $context);
});
```

## Twig Templating

### Basic Twig Syntax

```twig
{# templates/base.twig #}
<!DOCTYPE html>
<html {{ function('language_attributes') }}>
<head>
    <meta charset="{{ site.charset }}">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    
    {{ wp_head }}
</head>

<body {{ function('body_class') }}>
    <div id="page" class="site">
        <a class="skip-link screen-reader-text" href="#primary">Skip to content</a>

        <header id="masthead" class="site-header">
            <div class="site-branding">
                {% if site.logo %}
                    <img src="{{ site.logo.url }}" alt="{{ site.name }}" class="site-logo">
                {% else %}
                    <h1 class="site-title">
                        <a href="{{ site.url }}" rel="home">{{ site.name }}</a>
                    </h1>
                {% endif %}
                
                {% if site.description %}
                    <p class="site-description">{{ site.description }}</p>
                {% endif %}
            </div>

            <nav id="site-navigation" class="main-navigation">
                {{ menu }}
            </nav>
        </header>

        <main id="primary" class="site-main">
            {% block content %}
                <p>Sorry, no content</p>
            {% endblock %}
        </main>

        <footer id="colophon" class="site-footer">
            <div class="site-info">
                <a href="{{ site.url }}">{{ site.name }}</a>
                <span class="sep"> | </span>
                {{ __('Proudly powered by', 'textdomain') }} 
                <a href="https://wordpress.org/">WordPress</a>
            </div>
        </footer>
    </div>

    {{ wp_footer }}
</body>
</html>
```

### Template Inheritance

```twig
{# templates/index.twig #}
{% extends "base.twig" %}

{% block content %}
    <div class="posts-container">
        {% for post in posts %}
            <article class="post-item">
                <header class="entry-header">
                    {% if post.thumbnail %}
                        <div class="post-thumbnail">
                            <a href="{{ post.link }}">
                                <img src="{{ post.thumbnail.src('medium') }}" alt="{{ post.title }}">
                            </a>
                        </div>
                    {% endif %}
                    
                    <h2 class="entry-title">
                        <a href="{{ post.link }}" rel="bookmark">{{ post.title }}</a>
                    </h2>
                    
                    <div class="entry-meta">
                        <span class="posted-on">
                            <time class="entry-date published" datetime="{{ post.date('c') }}">
                                {{ post.date }}
                            </time>
                        </span>
                        <span class="byline">
                            {{ __('by', 'textdomain') }} 
                            <span class="author vcard">
                                <a class="url fn n" href="{{ post.author.link }}">
                                    {{ post.author.name }}
                                </a>
                            </span>
                        </span>
                    </div>
                </header>

                <div class="entry-content">
                    {{ post.preview.length(55).read_more('Continue reading') }}
                </div>

                <footer class="entry-footer">
                    <span class="cat-links">
                        {{ __('Posted in', 'textdomain') }} {{ post.terms('category') }}
                    </span>
                    
                    {% if post.comment_count > 0 %}
                        <span class="comments-link">
                            <a href="{{ post.link }}#comments">{{ post.comment_count }} {{ __('Comments', 'textdomain') }}</a>
                        </span>
                    {% endif %}
                </footer>
            </article>
        {% endfor %}
    </div>
    
    {% if pagination %}
        {{ pagination }}
    {% endif %}
{% endblock %}
```

### Advanced Twig Features

```twig
{# templates/single.twig #}
{% extends "base.twig" %}

{% block content %}
    <article id="post-{{ post.ID }}" class="post-{{ post.ID }} {{ post.post_type }} type-{{ post.post_type }} status-{{ post.post_status }} hentry">
        
        {% if post.thumbnail %}
            <div class="post-thumbnail">
                <img src="{{ post.thumbnail.src('large') }}" alt="{{ post.title }}">
            </div>
        {% endif %}

        <header class="entry-header">
            <h1 class="entry-title">{{ post.title }}</h1>
            
            <div class="entry-meta">
                <span class="posted-on">
                    <time class="entry-date published" datetime="{{ post.date('c') }}">
                        {{ post.date }}
                    </time>
                    {% if post.modified != post.date %}
                        <time class="updated" datetime="{{ post.modified('c') }}">
                            {{ __('Updated on', 'textdomain') }} {{ post.modified }}
                        </time>
                    {% endif %}
                </span>
                
                <span class="byline">
                    {{ __('by', 'textdomain') }} 
                    <span class="author vcard">
                        <a class="url fn n" href="{{ post.author.link }}">
                            {{ post.author.name }}
                        </a>
                    </span>
                </span>
            </div>
        </header>

        <div class="entry-content">
            {{ post.content }}
        </div>

        <footer class="entry-footer">
            {% if post.terms('category') %}
                <span class="cat-links">
                    {{ __('Categories:', 'textdomain') }} {{ post.terms('category') }}
                </span>
            {% endif %}
            
            {% if post.terms('post_tag') %}
                <span class="tags-links">
                    {{ __('Tags:', 'textdomain') }} {{ post.terms('post_tag') }}
                </span>
            {% endif %}
        </footer>
    </article>

    {# Related posts #}
    {% if related_posts %}
        <section class="related-posts">
            <h3>{{ __('Related Posts', 'textdomain') }}</h3>
            <div class="related-posts-grid">
                {% for related in related_posts %}
                    <div class="related-post">
                        {% if related.thumbnail %}
                            <img src="{{ related.thumbnail.src('thumbnail') }}" alt="{{ related.title }}">
                        {% endif %}
                        <h4><a href="{{ related.link }}">{{ related.title }}</a></h4>
                    </div>
                {% endfor %}
            </div>
        </section>
    {% endif %}

    {# Comments #}
    {% if post.comment_status == 'open' %}
        <div class="comments-area">
            {{ function('comments_template') }}
        </div>
    {% endif %}
{% endblock %}
```

## Timber Classes and Objects

### Custom Post Classes

```php
// Custom post class for enhanced functionality
class CustomPost extends \Timber\Post {
    
    public function custom_method() {
        return 'This is a custom method for ' . $this->title();
    }
    
    public function related_posts() {
        $related = get_posts(array(
            'post_type' => $this->post_type,
            'posts_per_page' => 3,
            'exclude' => array($this->ID),
            'meta_query' => array(
                array(
                    'key' => 'related_category',
                    'value' => $this->get_field('related_category'),
                    'compare' => '='
                )
            )
        ));
        
        return \Timber\Timber::get_posts($related);
    }
    
    public function get_field($field_name) {
        // ACF integration
        if (function_exists('get_field')) {
            return get_field($field_name, $this->ID);
        }
        
        // Fallback to post meta
        return get_post_meta($this->ID, $field_name, true);
    }
    
    public function formatted_date($format = 'F j, Y') {
        return $this->date($format);
    }
}

// Register custom post class
add_filter('timber/post/classmap', function($classmap) {
    $classmap['custom_post_type'] = 'CustomPost';
    return $classmap;
});
```

### Custom Term Classes

```php
// Custom term class
class CustomTerm extends \Timber\Term {
    
    public function post_count_formatted() {
        $count = $this->count;
        
        if ($count == 1) {
            return '1 post';
        } else {
            return $count . ' posts';
        }
    }
    
    public function related_terms() {
        $related = get_terms(array(
            'taxonomy' => $this->taxonomy,
            'exclude' => array($this->ID),
            'number' => 5
        ));
        
        return \Timber\Timber::get_terms($related);
    }
}

// Register custom term class
add_filter('timber/term/classmap', function($classmap) {
    $classmap['category'] = 'CustomTerm';
    $classmap['post_tag'] = 'CustomTerm';
    return $classmap;
});
```

### Custom User Classes

```php
// Custom user class
class CustomUser extends \Timber\User {
    
    public function full_name() {
        return $this->first_name . ' ' . $this->last_name;
    }
    
    public function author_posts() {
        $posts = get_posts(array(
            'author' => $this->ID,
            'posts_per_page' => 5,
            'post_status' => 'publish'
        ));
        
        return \Timber\Timber::get_posts($posts);
    }
    
    public function social_links() {
        return array(
            'twitter' => get_user_meta($this->ID, 'twitter', true),
            'facebook' => get_user_meta($this->ID, 'facebook', true),
            'linkedin' => get_user_meta($this->ID, 'linkedin', true)
        );
    }
}

// Register custom user class
add_filter('timber/user/classmap', function($classmap) {
    $classmap['user'] = 'CustomUser';
    return $classmap;
});
```

## Advanced Timber Features

### Custom Twig Functions and Filters

```php
// Custom Twig functions
add_filter('timber/twig', function($twig) {
    // Custom function
    $twig->addFunction(new \Twig\TwigFunction('get_theme_option', function($option_name, $default = '') {
        return get_theme_mod($option_name, $default);
    }));
    
    // Custom filter
    $twig->addFilter(new \Twig\TwigFilter('truncate', function($text, $length = 100, $suffix = '...') {
        if (strlen($text) <= $length) {
            return $text;
        }
        
        return substr($text, 0, $length) . $suffix;
    }));
    
    // Custom filter for ACF fields
    $twig->addFilter(new \Twig\TwigFilter('acf_field', function($post_id, $field_name) {
        if (function_exists('get_field')) {
            return get_field($field_name, $post_id);
        }
        return '';
    }));
    
    return $twig;
});

// Usage in Twig templates
/*
{{ get_theme_option('site_logo') }}
{{ post.content|truncate(150) }}
{{ post.id|acf_field('custom_field') }}
*/
```

### Timber with ACF (Advanced Custom Fields)

```php
// ACF integration with Timber
class ACFPost extends \Timber\Post {
    
    public function acf_fields() {
        if (!function_exists('get_fields')) {
            return array();
        }
        
        return get_fields($this->ID);
    }
    
    public function get_acf_field($field_name, $format_value = true) {
        if (!function_exists('get_field')) {
            return null;
        }
        
        return get_field($field_name, $this->ID, $format_value);
    }
    
    public function has_acf_field($field_name) {
        if (!function_exists('get_field')) {
            return false;
        }
        
        return !empty(get_field($field_name, $this->ID));
    }
}

// Register ACF post class
add_filter('timber/post/classmap', function($classmap) {
    $classmap['post'] = 'ACFPost';
    $classmap['page'] = 'ACFPost';
    return $classmap;
});

// ACF Twig functions
add_filter('timber/twig', function($twig) {
    $twig->addFunction(new \Twig\TwigFunction('acf_field', function($post_id, $field_name) {
        if (function_exists('get_field')) {
            return get_field($field_name, $post_id);
        }
        return null;
    }));
    
    $twig->addFunction(new \Twig\TwigFunction('acf_options', function($field_name) {
        if (function_exists('get_field')) {
            return get_field($field_name, 'option');
        }
        return null;
    }));
    
    return $twig;
});
```

### Timber with WooCommerce

```php
// WooCommerce integration with Timber
class WooCommercePost extends \Timber\Post {
    
    public function is_product() {
        return $this->post_type === 'product';
    }
    
    public function get_product() {
        if ($this->is_product()) {
            return wc_get_product($this->ID);
        }
        return null;
    }
    
    public function product_price() {
        $product = $this->get_product();
        if ($product) {
            return $product->get_price_html();
        }
        return '';
    }
    
    public function product_rating() {
        $product = $this->get_product();
        if ($product) {
            return $product->get_average_rating();
        }
        return 0;
    }
}

// WooCommerce context
add_filter('timber_context', function($context) {
    if (class_exists('WooCommerce')) {
        $context['cart'] = WC()->cart;
        $context['shop_url'] = wc_get_page_permalink('shop');
        $context['cart_url'] = wc_get_cart_url();
        $context['checkout_url'] = wc_get_checkout_url();
        $context['my_account_url'] = wc_get_page_permalink('myaccount');
    }
    
    return $context;
});

// WooCommerce Twig functions
add_filter('timber/twig', function($twig) {
    if (class_exists('WooCommerce')) {
        $twig->addFunction(new \Twig\TwigFunction('wc_cart_count', function() {
            return WC()->cart->get_cart_contents_count();
        }));
        
        $twig->addFunction(new \Twig\TwigFunction('wc_cart_total', function() {
            return WC()->cart->get_cart_total();
        }));
    }
    
    return $twig;
});
```

## Timber Best Practices

### Performance Optimization

```php
// Timber performance optimization
function optimize_timber_performance() {
    // Enable Timber cache in production
    if (!WP_DEBUG) {
        \Timber\Timber::$cache = true;
        \Timber\Timber::$cache_mode = \Timber\Loader::CACHE_USE_DEFAULT;
    }
    
    // Set cache duration
    \Timber\Timber::$cache_time = 3600; // 1 hour
    
    // Optimize Twig compilation
    \Timber\Timber::$autoescape = false;
    
    // Use compiled templates in production
    if (!WP_DEBUG) {
        \Timber\Timber::$dirname = array('templates-compiled');
    }
}

add_action('init', 'optimize_timber_performance');

// Custom Timber loader for better performance
class OptimizedTimberLoader extends \Timber\Loader {
    
    public function get_cache_key($name, $data) {
        $key = parent::get_cache_key($name, $data);
        
        // Add additional cache key components
        $key .= '_' . get_current_blog_id();
        $key .= '_' . (is_user_logged_in() ? 'logged_in' : 'logged_out');
        
        return $key;
    }
}

// Use optimized loader
\Timber\Timber::$loader = new OptimizedTimberLoader();
```

### Security Best Practices

```php
// Timber security enhancements
function timber_security() {
    // Enable auto-escaping for security
    \Timber\Timber::$autoescape = true;
    
    // Custom Twig security policies
    add_filter('timber/twig', function($twig) {
        $twig->addExtension(new \Twig\Extension\SandboxExtension());
        
        // Define allowed functions
        $policy = new \Twig\Sandbox\SecurityPolicy(array(), array(), array(), array(), array());
        $twig->addExtension(new \Twig\Extension\SandboxExtension($policy));
        
        return $twig;
    });
}

add_action('init', 'timber_security');

// Sanitize Timber context data
function sanitize_timber_context($context) {
    // Recursively sanitize context data
    array_walk_recursive($context, function(&$value, $key) {
        if (is_string($value)) {
            $value = wp_kses_post($value);
        }
    });
    
    return $context;
}

add_filter('timber_context', 'sanitize_timber_context');
```

### Development Workflow

```php
// Timber development tools
function timber_dev_tools() {
    if (!WP_DEBUG) {
        return;
    }
    
    // Add Timber debug information
    add_action('wp_footer', function() {
        if (current_user_can('manage_options')) {
            echo '<!-- Timber Debug Info -->';
            echo '<!-- Cache: ' . (\Timber\Timber::$cache ? 'Enabled' : 'Disabled') . ' -->';
            echo '<!-- Templates: ' . implode(', ', \Timber\Timber::$dirname) . ' -->';
        }
    });
    
    // Timber template debugging
    add_filter('timber/loader/render_file', function($file, $name) {
        if (current_user_can('manage_options')) {
            error_log("Timber rendering: $name from $file");
        }
        return $file;
    }, 10, 2);
}

add_action('init', 'timber_dev_tools');

// Custom Timber error handling
function timber_error_handling() {
    set_error_handler(function($severity, $message, $file, $line) {
        if (error_reporting() & $severity) {
            throw new \ErrorException($message, 0, $severity, $file, $line);
        }
    });
}

add_action('init', 'timber_error_handling');
```

## Timber Examples

### Complete Theme Structure

```php
// Complete Timber theme setup
class TimberTheme {
    
    public function __construct() {
        add_action('after_setup_theme', array($this, 'setup'));
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_filter('timber_context', array($this, 'add_to_context'));
        add_filter('timber/twig', array($this, 'add_to_twig'));
    }
    
    public function setup() {
        // Theme support
        add_theme_support('post-thumbnails');
        add_theme_support('menus');
        add_theme_support('html5', array('comment-list', 'comment-form', 'search-form', 'gallery', 'caption'));
        
        // Register menus
        register_nav_menus(array(
            'primary' => __('Primary Menu', 'textdomain'),
            'footer' => __('Footer Menu', 'textdomain'),
        ));
        
        // Register widget areas
        register_sidebar(array(
            'name' => __('Sidebar', 'textdomain'),
            'id' => 'sidebar-1',
            'description' => __('Add widgets here.', 'textdomain'),
        ));
    }
    
    public function enqueue_scripts() {
        wp_enqueue_style('theme-style', get_stylesheet_uri(), array(), '1.0.0');
        wp_enqueue_script('theme-script', get_template_directory_uri() . '/js/script.js', array('jquery'), '1.0.0', true);
    }
    
    public function add_to_context($context) {
        $context['menu'] = new \Timber\Menu('primary');
        $context['footer_menu'] = new \Timber\Menu('footer');
        $context['site'] = $this;
        $context['sidebar'] = \Timber\Timber::get_widgets('sidebar-1');
        
        return $context;
    }
    
    public function add_to_twig($twig) {
        $twig->addExtension(new \Twig\Extension\StringLoaderExtension());
        
        return $twig;
    }
}

new TimberTheme();
```

### Custom Post Type with Timber

```php
// Custom post type with Timber integration
function register_custom_post_type() {
    register_post_type('portfolio', array(
        'labels' => array(
            'name' => 'Portfolio',
            'singular_name' => 'Portfolio Item',
        ),
        'public' => true,
        'has_archive' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'custom-fields'),
        'menu_icon' => 'dashicons-portfolio',
    ));
}

add_action('init', 'register_custom_post_type');

// Custom portfolio class
class Portfolio extends \Timber\Post {
    
    public function gallery() {
        $gallery = get_field('gallery', $this->ID);
        
        if ($gallery) {
            return \Timber\Timber::get_posts($gallery);
        }
        
        return array();
    }
    
    public function client() {
        return get_field('client', $this->ID);
    }
    
    public function project_url() {
        return get_field('project_url', $this->ID);
    }
    
    public function technologies() {
        return get_field('technologies', $this->ID);
    }
}

// Register portfolio class
add_filter('timber/post/classmap', function($classmap) {
    $classmap['portfolio'] = 'Portfolio';
    return $classmap;
});
```

## Official Documentation

https://timber.github.io/docs/
https://github.com/timber/timber
https://twig.symfony.com/doc/3.x/
