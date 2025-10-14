# WordPress Sidebars & Widgets

Sidebars and widgets provide flexible content areas that users can customize through the WordPress admin.

## Sidebar Registration

### Basic Sidebar Registration

```php
// functions.php - Register sidebars
function my_theme_sidebars() {
    register_sidebar(array(
        'name'          => __('Primary Sidebar', 'my-theme'),
        'id'            => 'sidebar-1',
        'description'   => __('Add widgets here to appear in your sidebar.', 'my-theme'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h2 class="widget-title">',
        'after_title'   => '</h2>',
    ));
    
    register_sidebar(array(
        'name'          => __('Footer Widget Area', 'my-theme'),
        'id'            => 'footer-widgets',
        'description'   => __('Add widgets here to appear in your footer.', 'my-theme'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
}
add_action('widgets_init', 'my_theme_sidebars');
```

### Advanced Sidebar Registration

```php
// functions.php - Advanced sidebar registration
function my_theme_advanced_sidebars() {
    // Main sidebar
    register_sidebar(array(
        'name'          => __('Main Sidebar', 'my-theme'),
        'id'            => 'main-sidebar',
        'description'   => __('Primary sidebar for blog posts and pages.', 'my-theme'),
        'before_widget' => '<aside id="%1$s" class="widget %2$s">',
        'after_widget'  => '</aside>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    
    // Footer sidebars
    for ($i = 1; $i <= 4; $i++) {
        register_sidebar(array(
            'name'          => sprintf(__('Footer Widget Area %d', 'my-theme'), $i),
            'id'            => 'footer-' . $i,
            'description'   => sprintf(__('Add widgets here to appear in footer column %d.', 'my-theme'), $i),
            'before_widget' => '<div id="%1$s" class="widget %2$s">',
            'after_widget'  => '</div>',
            'before_title'  => '<h4 class="widget-title">',
            'after_title'   => '</h4>',
        ));
    }
    
    // Shop sidebar (for WooCommerce)
    register_sidebar(array(
        'name'          => __('Shop Sidebar', 'my-theme'),
        'id'            => 'shop-sidebar',
        'description'   => __('Sidebar for WooCommerce shop pages.', 'my-theme'),
        'before_widget' => '<aside id="%1$s" class="widget %2$s">',
        'after_widget'  => '</aside>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ));
    
    // Homepage widgets
    register_sidebar(array(
        'name'          => __('Homepage Widgets', 'my-theme'),
        'id'            => 'homepage-widgets',
        'description'   => __('Widgets for the homepage template.', 'my-theme'),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h2 class="widget-title">',
        'after_title'   => '</h2>',
    ));
}
add_action('widgets_init', 'my_theme_advanced_sidebars');
```

## Sidebar Display

### Basic Sidebar Display

```php
// Display sidebar in template
if (is_active_sidebar('sidebar-1')) {
    dynamic_sidebar('sidebar-1');
}
```

### Conditional Sidebar Display

```php
// Display different sidebars based on page type
function display_conditional_sidebar() {
    if (is_shop() || is_product_category() || is_product_tag()) {
        // WooCommerce shop sidebar
        if (is_active_sidebar('shop-sidebar')) {
            dynamic_sidebar('shop-sidebar');
        }
    } elseif (is_home() || is_category() || is_tag() || is_archive()) {
        // Blog sidebar
        if (is_active_sidebar('main-sidebar')) {
            dynamic_sidebar('main-sidebar');
        }
    } else {
        // Default sidebar
        if (is_active_sidebar('sidebar-1')) {
            dynamic_sidebar('sidebar-1');
        }
    }
}
```

### Sidebar with Fallback Content

```php
// Sidebar with fallback content
function display_sidebar_with_fallback() {
    if (is_active_sidebar('sidebar-1')) {
        dynamic_sidebar('sidebar-1');
    } else {
        // Fallback content
        echo '<aside class="widget">';
        echo '<h3 class="widget-title">' . __('Welcome', 'my-theme') . '</h3>';
        echo '<p>' . __('Add widgets to this sidebar from the Widgets section in the WordPress admin.', 'my-theme') . '</p>';
        echo '</aside>';
    }
}
```

## Custom Widgets

### Basic Custom Widget

```php
// Custom widget class
class My_Custom_Widget extends WP_Widget {
    
    public function __construct() {
        parent::__construct(
            'my_custom_widget',
            __('Custom Widget', 'my-theme'),
            array('description' => __('A custom widget for displaying content.', 'my-theme'))
        );
    }
    
    // Widget front-end display
    public function widget($args, $instance) {
        $title = apply_filters('widget_title', $instance['title']);
        $text = $instance['text'];
        $show_date = !empty($instance['show_date']) ? true : false;
        
        echo $args['before_widget'];
        
        if (!empty($title)) {
            echo $args['before_title'] . $title . $args['after_title'];
        }
        
        if ($show_date) {
            echo '<p class="widget-date">' . date('F j, Y') . '</p>';
        }
        
        if (!empty($text)) {
            echo '<div class="widget-text">' . wpautop($text) . '</div>';
        }
        
        echo $args['after_widget'];
    }
    
    // Widget backend form
    public function form($instance) {
        $title = isset($instance['title']) ? $instance['title'] : '';
        $text = isset($instance['text']) ? $instance['text'] : '';
        $show_date = isset($instance['show_date']) ? (bool) $instance['show_date'] : false;
        ?>
        <p>
            <label for="<?php echo $this->get_field_id('title'); ?>"><?php _e('Title:', 'my-theme'); ?></label>
            <input class="widefat" id="<?php echo $this->get_field_id('title'); ?>" name="<?php echo $this->get_field_name('title'); ?>" type="text" value="<?php echo esc_attr($title); ?>">
        </p>
        <p>
            <label for="<?php echo $this->get_field_id('text'); ?>"><?php _e('Text:', 'my-theme'); ?></label>
            <textarea class="widefat" id="<?php echo $this->get_field_id('text'); ?>" name="<?php echo $this->get_field_name('text'); ?>" rows="5"><?php echo esc_textarea($text); ?></textarea>
        </p>
        <p>
            <input class="checkbox" type="checkbox" <?php checked($show_date); ?> id="<?php echo $this->get_field_id('show_date'); ?>" name="<?php echo $this->get_field_name('show_date'); ?>" />
            <label for="<?php echo $this->get_field_id('show_date'); ?>"><?php _e('Display date?', 'my-theme'); ?></label>
        </p>
        <?php
    }
    
    // Widget update
    public function update($new_instance, $old_instance) {
        $instance = array();
        $instance['title'] = (!empty($new_instance['title'])) ? strip_tags($new_instance['title']) : '';
        $instance['text'] = (!empty($new_instance['text'])) ? $new_instance['text'] : '';
        $instance['show_date'] = (!empty($new_instance['show_date'])) ? 1 : 0;
        
        return $instance;
    }
}

// Register the widget
function register_my_custom_widget() {
    register_widget('My_Custom_Widget');
}
add_action('widgets_init', 'register_my_custom_widget');
```

### Advanced Custom Widget

```php
// Advanced custom widget with multiple options
class Advanced_Custom_Widget extends WP_Widget {
    
    public function __construct() {
        parent::__construct(
            'advanced_custom_widget',
            __('Advanced Custom Widget', 'my-theme'),
            array('description' => __('An advanced widget with multiple display options.', 'my-theme'))
        );
    }
    
    public function widget($args, $instance) {
        $title = apply_filters('widget_title', $instance['title']);
        $post_type = !empty($instance['post_type']) ? $instance['post_type'] : 'post';
        $number = !empty($instance['number']) ? absint($instance['number']) : 5;
        $show_excerpt = !empty($instance['show_excerpt']) ? true : false;
        $show_thumbnail = !empty($instance['show_thumbnail']) ? true : false;
        
        echo $args['before_widget'];
        
        if (!empty($title)) {
            echo $args['before_title'] . $title . $args['after_title'];
        }
        
        // Query posts
        $query_args = array(
            'post_type' => $post_type,
            'posts_per_page' => $number,
            'post_status' => 'publish'
        );
        
        $posts = new WP_Query($query_args);
        
        if ($posts->have_posts()) {
            echo '<ul class="widget-posts-list">';
            while ($posts->have_posts()) {
                $posts->the_post();
                echo '<li class="widget-post-item">';
                
                if ($show_thumbnail && has_post_thumbnail()) {
                    echo '<div class="widget-post-thumbnail">';
                    the_post_thumbnail('thumbnail');
                    echo '</div>';
                }
                
                echo '<div class="widget-post-content">';
                echo '<h4 class="widget-post-title"><a href="' . get_permalink() . '">' . get_the_title() . '</a></h4>';
                
                if ($show_excerpt) {
                    echo '<div class="widget-post-excerpt">' . wp_trim_words(get_the_excerpt(), 15) . '</div>';
                }
                
                echo '<div class="widget-post-meta">' . get_the_date() . '</div>';
                echo '</div>';
                echo '</li>';
            }
            echo '</ul>';
            wp_reset_postdata();
        } else {
            echo '<p>' . __('No posts found.', 'my-theme') . '</p>';
        }
        
        echo $args['after_widget'];
    }
    
    public function form($instance) {
        $title = isset($instance['title']) ? $instance['title'] : '';
        $post_type = isset($instance['post_type']) ? $instance['post_type'] : 'post';
        $number = isset($instance['number']) ? absint($instance['number']) : 5;
        $show_excerpt = isset($instance['show_excerpt']) ? (bool) $instance['show_excerpt'] : false;
        $show_thumbnail = isset($instance['show_thumbnail']) ? (bool) $instance['show_thumbnail'] : false;
        
        // Get available post types
        $post_types = get_post_types(array('public' => true), 'objects');
        ?>
        <p>
            <label for="<?php echo $this->get_field_id('title'); ?>"><?php _e('Title:', 'my-theme'); ?></label>
            <input class="widefat" id="<?php echo $this->get_field_id('title'); ?>" name="<?php echo $this->get_field_name('title'); ?>" type="text" value="<?php echo esc_attr($title); ?>">
        </p>
        <p>
            <label for="<?php echo $this->get_field_id('post_type'); ?>"><?php _e('Post Type:', 'my-theme'); ?></label>
            <select class="widefat" id="<?php echo $this->get_field_id('post_type'); ?>" name="<?php echo $this->get_field_name('post_type'); ?>">
                <?php foreach ($post_types as $type) : ?>
                    <option value="<?php echo esc_attr($type->name); ?>" <?php selected($post_type, $type->name); ?>>
                        <?php echo esc_html($type->label); ?>
                    </option>
                <?php endforeach; ?>
            </select>
        </p>
        <p>
            <label for="<?php echo $this->get_field_id('number'); ?>"><?php _e('Number of posts:', 'my-theme'); ?></label>
            <input class="tiny-text" id="<?php echo $this->get_field_id('number'); ?>" name="<?php echo $this->get_field_name('number'); ?>" type="number" step="1" min="1" value="<?php echo $number; ?>" size="3">
        </p>
        <p>
            <input class="checkbox" type="checkbox" <?php checked($show_excerpt); ?> id="<?php echo $this->get_field_id('show_excerpt'); ?>" name="<?php echo $this->get_field_name('show_excerpt'); ?>" />
            <label for="<?php echo $this->get_field_id('show_excerpt'); ?>"><?php _e('Show excerpt?', 'my-theme'); ?></label>
        </p>
        <p>
            <input class="checkbox" type="checkbox" <?php checked($show_thumbnail); ?> id="<?php echo $this->get_field_id('show_thumbnail'); ?>" name="<?php echo $this->get_field_name('show_thumbnail'); ?>" />
            <label for="<?php echo $this->get_field_id('show_thumbnail'); ?>"><?php _e('Show thumbnail?', 'my-theme'); ?></label>
        </p>
        <?php
    }
    
    public function update($new_instance, $old_instance) {
        $instance = array();
        $instance['title'] = (!empty($new_instance['title'])) ? strip_tags($new_instance['title']) : '';
        $instance['post_type'] = (!empty($new_instance['post_type'])) ? sanitize_text_field($new_instance['post_type']) : 'post';
        $instance['number'] = (!empty($new_instance['number'])) ? absint($new_instance['number']) : 5;
        $instance['show_excerpt'] = (!empty($new_instance['show_excerpt'])) ? 1 : 0;
        $instance['show_thumbnail'] = (!empty($new_instance['show_thumbnail'])) ? 1 : 0;
        
        return $instance;
    }
}

// Register the advanced widget
function register_advanced_custom_widget() {
    register_widget('Advanced_Custom_Widget');
}
add_action('widgets_init', 'register_advanced_custom_widget');
```

## Widget Areas Styling

### Basic Widget Styling

```css
/* Basic widget styling */
.widget {
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: #fff;
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.widget-title {
    margin: 0 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #0073aa;
    font-size: 1.25rem;
    font-weight: 600;
    color: #333;
}

.widget ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.widget li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f0f0;
}

.widget li:last-child {
    border-bottom: none;
}

.widget a {
    color: #0073aa;
    text-decoration: none;
    transition: color 0.3s ease;
}

.widget a:hover {
    color: #005177;
}
```

### Advanced Widget Styling

```css
/* Advanced widget styling */
.widget {
    position: relative;
    overflow: hidden;
}

.widget::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #0073aa, #00a0d2);
}

/* Widget post list styling */
.widget-posts-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.widget-post-item {
    display: flex;
    gap: 1rem;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 6px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.widget-post-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.widget-post-thumbnail {
    flex-shrink: 0;
}

.widget-post-thumbnail img {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 4px;
}

.widget-post-content {
    flex: 1;
}

.widget-post-title {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    line-height: 1.3;
}

.widget-post-title a {
    color: #333;
    text-decoration: none;
}

.widget-post-title a:hover {
    color: #0073aa;
}

.widget-post-excerpt {
    font-size: 0.8rem;
    color: #666;
    line-height: 1.4;
}

.widget-post-meta {
    font-size: 0.75rem;
    color: #999;
    margin-top: 0.5rem;
}

/* Footer widget styling */
.footer-widgets .widget {
    background: transparent;
    border: none;
    box-shadow: none;
    padding: 0;
}

.footer-widgets .widget-title {
    color: #fff;
    border-bottom-color: #fff;
}

.footer-widgets .widget a {
    color: #ccc;
}

.footer-widgets .widget a:hover {
    color: #fff;
}
```

## Block Widgets (Gutenberg)

### Block Widget Areas

```php
// Register block widget areas
function register_block_widget_areas() {
    register_sidebar(array(
        'name'          => __('Block Widget Area', 'my-theme'),
        'id'            => 'block-widget-area',
        'description'   => __('Add block widgets here.', 'my-theme'),
        'before_widget' => '',
        'after_widget'  => '',
        'before_title'  => '',
        'after_title'   => '',
    ));
}
add_action('widgets_init', 'register_block_widget_areas');
```

### Custom Block Widget

```php
// Custom block widget
class Custom_Block_Widget extends WP_Widget_Block {
    
    public function __construct() {
        parent::__construct(
            'custom_block_widget',
            __('Custom Block Widget', 'my-theme'),
            array('description' => __('A custom block widget.', 'my-theme'))
        );
    }
    
    public function render_block_content($args, $instance) {
        // Custom block content
        return '<div class="custom-block-widget">Custom block content</div>';
    }
}

// Register block widget
function register_custom_block_widget() {
    register_widget('Custom_Block_Widget');
}
add_action('widgets_init', 'register_custom_block_widget');
```

## Widget Performance

### Widget Caching

```php
// Cache widget output
function cache_widget_output($widget_content, $widget_id) {
    $cache_key = 'widget_' . $widget_id . '_' . md5(serialize($widget_content));
    $cached_content = get_transient($cache_key);
    
    if ($cached_content === false) {
        $cached_content = $widget_content;
        set_transient($cache_key, $cached_content, HOUR_IN_SECONDS);
    }
    
    return $cached_content;
}
add_filter('widget_text', 'cache_widget_output', 10, 2);
```

### Widget Optimization

```php
// Optimize widget queries
function optimize_widget_queries($query_args) {
    // Limit posts per page for widget queries
    if (isset($query_args['posts_per_page']) && $query_args['posts_per_page'] > 10) {
        $query_args['posts_per_page'] = 10;
    }
    
    // Add meta query optimization
    $query_args['meta_query'] = array(
        'relation' => 'AND',
        array(
            'key' => '_thumbnail_id',
            'compare' => 'EXISTS'
        )
    );
    
    return $query_args;
}
add_filter('widget_posts_args', 'optimize_widget_queries');
```

## Accessibility

### Accessible Widget Markup

```php
// Add accessibility attributes to widgets
function add_widget_accessibility_attributes($args, $widget_id, $widget_name) {
    $args['before_widget'] = '<section id="' . $widget_id . '" class="widget ' . $widget_name . '" role="complementary" aria-label="' . esc_attr($widget_name) . '">';
    $args['after_widget'] = '</section>';
    
    return $args;
}
add_filter('dynamic_sidebar_params', 'add_widget_accessibility_attributes', 10, 3);
```

## Official Documentation

https://developer.wordpress.org/themes/functionality/sidebars/
https://developer.wordpress.org/themes/functionality/widgets/
https://developer.wordpress.org/themes/basics/sidebars/
