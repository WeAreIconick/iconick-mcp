# WordPress Navigation Menus

Navigation menus provide site structure and user navigation throughout your WordPress site.

## Menu Registration

### Basic Menu Registration

```php
// functions.php - Register navigation menus
function my_theme_navigation_menus() {
    register_nav_menus(array(
        'primary' => __('Primary Menu', 'my-theme'),
        'footer'  => __('Footer Menu', 'my-theme'),
        'social'  => __('Social Menu', 'my-theme'),
        'mobile'  => __('Mobile Menu', 'my-theme')
    ));
}
add_action('init', 'my_theme_navigation_menus');
```

### Advanced Menu Registration

```php
// functions.php - Advanced menu registration with custom locations
function my_theme_advanced_menus() {
    register_nav_menus(array(
        'primary' => array(
            'name' => __('Primary Navigation', 'my-theme'),
            'description' => __('Main navigation menu in the header', 'my-theme')
        ),
        'footer' => array(
            'name' => __('Footer Navigation', 'my-theme'),
            'description' => __('Navigation links in the footer area', 'my-theme')
        ),
        'sidebar' => array(
            'name' => __('Sidebar Navigation', 'my-theme'),
            'description' => __('Navigation menu for sidebar area', 'my-theme')
        ),
        'mobile' => array(
            'name' => __('Mobile Navigation', 'my-theme'),
            'description' => __('Navigation menu for mobile devices', 'my-theme')
        )
    ));
}
add_action('init', 'my_theme_advanced_menus');
```

## Menu Display Functions

### Basic Menu Display

```php
// Display navigation menu
wp_nav_menu(array(
    'theme_location' => 'primary',
    'menu_class' => 'nav-menu',
    'container' => 'nav',
    'container_class' => 'main-navigation'
));
```

### Advanced Menu Display Options

```php
// Advanced menu display with custom options
wp_nav_menu(array(
    'theme_location'  => 'primary',
    'menu'            => '', // Use specific menu ID or slug
    'container'       => 'nav',
    'container_class' => 'main-navigation',
    'container_id'    => 'primary-navigation',
    'menu_class'      => 'nav-menu',
    'menu_id'         => 'primary-menu',
    'echo'            => true,
    'fallback_cb'     => 'wp_page_menu',
    'before'          => '',
    'after'           => '',
    'link_before'     => '',
    'link_after'      => '',
    'items_wrap'      => '<ul id="%1$s" class="%2$s">%3$s</ul>',
    'item_spacing'    => 'preserve',
    'depth'           => 0,
    'walker'          => new Custom_Nav_Walker()
));
```

### Conditional Menu Display

```php
// Display different menus based on conditions
function display_conditional_menu() {
    if (is_user_logged_in()) {
        wp_nav_menu(array(
            'theme_location' => 'logged-in-menu',
            'fallback_cb' => false
        ));
    } else {
        wp_nav_menu(array(
            'theme_location' => 'guest-menu',
            'fallback_cb' => false
        ));
    }
}
```

## Custom Walker Classes

### Basic Custom Walker

```php
// Custom navigation walker
class Custom_Nav_Walker extends Walker_Nav_Menu {
    
    // Start the list before the elements are added
    function start_lvl(&$output, $depth = 0, $args = null) {
        $indent = str_repeat("\t", $depth);
        $output .= "\n$indent<ul class=\"sub-menu\">\n";
    }
    
    // End the list after the elements are added
    function end_lvl(&$output, $depth = 0, $args = null) {
        $indent = str_repeat("\t", $depth);
        $output .= "$indent</ul>\n";
    }
    
    // Start the element output
    function start_el(&$output, $item, $depth = 0, $args = null, $id = 0) {
        $indent = ($depth) ? str_repeat("\t", $depth) : '';
        
        $classes = empty($item->classes) ? array() : (array) $item->classes;
        $classes[] = 'menu-item-' . $item->ID;
        
        $class_names = join(' ', apply_filters('nav_menu_css_class', array_filter($classes), $item, $args));
        $class_names = $class_names ? ' class="' . esc_attr($class_names) . '"' : '';
        
        $id = apply_filters('nav_menu_item_id', 'menu-item-'. $item->ID, $item, $args);
        $id = $id ? ' id="' . esc_attr($id) . '"' : '';
        
        $output .= $indent . '<li' . $id . $class_names .'>';
        
        $attributes = ! empty($item->attr_title) ? ' title="'  . esc_attr($item->attr_title) .'"' : '';
        $attributes .= ! empty($item->target)     ? ' target="' . esc_attr($item->target     ) .'"' : '';
        $attributes .= ! empty($item->xfn)        ? ' rel="'    . esc_attr($item->xfn        ) .'"' : '';
        $attributes .= ! empty($item->url)        ? ' href="'   . esc_attr($item->url        ) .'"' : '';
        
        $item_output = isset($args->before) ? $args->before : '';
        $item_output .= '<a' . $attributes .'>';
        $item_output .= (isset($args->link_before) ? $args->link_before : '') . apply_filters('the_title', $item->title, $item->ID) . (isset($args->link_after) ? $args->link_after : '');
        $item_output .= '</a>';
        $item_output .= isset($args->after) ? $args->after : '';
        
        $output .= apply_filters('walker_nav_menu_start_el', $item_output, $item, $depth, $args);
    }
    
    // End the element output
    function end_el(&$output, $item, $depth = 0, $args = null) {
        $output .= "</li>\n";
    }
}
```

### Advanced Custom Walker with Icons

```php
// Advanced walker with icon support
class Icon_Nav_Walker extends Walker_Nav_Menu {
    
    function start_el(&$output, $item, $depth = 0, $args = null, $id = 0) {
        $indent = ($depth) ? str_repeat("\t", $depth) : '';
        
        $classes = empty($item->classes) ? array() : (array) $item->classes;
        $classes[] = 'menu-item-' . $item->ID;
        
        // Add custom classes based on depth
        if ($depth > 0) {
            $classes[] = 'sub-menu-item';
        }
        
        $class_names = join(' ', apply_filters('nav_menu_css_class', array_filter($classes), $item, $args));
        $class_names = $class_names ? ' class="' . esc_attr($class_names) . '"' : '';
        
        $id = apply_filters('nav_menu_item_id', 'menu-item-'. $item->ID, $item, $args);
        $id = $id ? ' id="' . esc_attr($id) . '"' : '';
        
        $output .= $indent . '<li' . $id . $class_names .'>';
        
        $attributes = ! empty($item->attr_title) ? ' title="'  . esc_attr($item->attr_title) .'"' : '';
        $attributes .= ! empty($item->target)     ? ' target="' . esc_attr($item->target     ) .'"' : '';
        $attributes .= ! empty($item->xfn)        ? ' rel="'    . esc_attr($item->xfn        ) .'"' : '';
        $attributes .= ! empty($item->url)        ? ' href="'   . esc_attr($item->url        ) .'"' : '';
        
        // Get icon from custom field or meta
        $icon = get_post_meta($item->ID, '_menu_item_icon', true);
        $icon_html = $icon ? '<i class="' . esc_attr($icon) . '"></i> ' : '';
        
        $item_output = isset($args->before) ? $args->before : '';
        $item_output .= '<a' . $attributes .'>';
        $item_output .= $icon_html;
        $item_output .= (isset($args->link_before) ? $args->link_before : '') . apply_filters('the_title', $item->title, $item->ID) . (isset($args->link_after) ? $args->link_after : '');
        $item_output .= '</a>';
        $item_output .= isset($args->after) ? $args->after : '';
        
        $output .= apply_filters('walker_nav_menu_start_el', $item_output, $item, $depth, $args);
    }
    
    function end_el(&$output, $item, $depth = 0, $args = null) {
        $output .= "</li>\n";
    }
    
    function start_lvl(&$output, $depth = 0, $args = null) {
        $indent = str_repeat("\t", $depth);
        $output .= "\n$indent<ul class=\"dropdown-menu\">\n";
    }
    
    function end_lvl(&$output, $depth = 0, $args = null) {
        $indent = str_repeat("\t", $depth);
        $output .= "$indent</ul>\n";
    }
}
```

## Menu Customization

### Add Custom Fields to Menu Items

```php
// Add custom fields to menu items
function add_menu_item_custom_fields($item_id, $item, $depth, $args) {
    ?>
    <p class="field-icon description description-wide">
        <label for="edit-menu-item-icon-<?php echo $item_id; ?>">
            <?php _e('Icon Class', 'my-theme'); ?><br />
            <input type="text" id="edit-menu-item-icon-<?php echo $item_id; ?>" class="widefat code edit-menu-item-icon" name="menu-item-icon[<?php echo $item_id; ?>]" value="<?php echo esc_attr(get_post_meta($item_id, '_menu_item_icon', true)); ?>" />
        </label>
    </p>
    
    <p class="field-description description description-wide">
        <label for="edit-menu-item-description-<?php echo $item_id; ?>">
            <?php _e('Description', 'my-theme'); ?><br />
            <textarea id="edit-menu-item-description-<?php echo $item_id; ?>" class="widefat edit-menu-item-description" rows="3" cols="20" name="menu-item-description[<?php echo $item_id; ?>]"><?php echo esc_html(get_post_meta($item_id, '_menu_item_description', true)); ?></textarea>
        </label>
    </p>
    <?php
}
add_action('wp_nav_menu_item_custom_fields', 'add_menu_item_custom_fields', 10, 4);

// Save custom fields
function save_menu_item_custom_fields($menu_id, $menu_item_db_id, $menu_item_args) {
    if (isset($_POST['menu-item-icon'][$menu_item_db_id])) {
        update_post_meta($menu_item_db_id, '_menu_item_icon', sanitize_text_field($_POST['menu-item-icon'][$menu_item_db_id]));
    }
    
    if (isset($_POST['menu-item-description'][$menu_item_db_id])) {
        update_post_meta($menu_item_db_id, '_menu_item_description', sanitize_textarea_field($_POST['menu-item-description'][$menu_item_db_id]));
    }
}
add_action('wp_update_nav_menu_item', 'save_menu_item_custom_fields', 10, 3);
```

### Menu Item Filters and Hooks

```php
// Filter menu item classes
function custom_menu_item_classes($classes, $item, $args) {
    // Add custom class based on menu item
    if ($item->object == 'page') {
        $classes[] = 'page-menu-item';
    }
    
    if ($item->url && strpos($item->url, 'http') === 0) {
        $classes[] = 'external-link';
    }
    
    return $classes;
}
add_filter('nav_menu_css_class', 'custom_menu_item_classes', 10, 3);

// Filter menu item attributes
function custom_menu_item_attributes($atts, $item, $args) {
    // Add custom attributes
    if ($item->object == 'custom' && strpos($item->url, 'http') === 0) {
        $atts['target'] = '_blank';
        $atts['rel'] = 'noopener noreferrer';
    }
    
    return $atts;
}
add_filter('nav_menu_link_attributes', 'custom_menu_item_attributes', 10, 3);
```

## Responsive Navigation

### Mobile-First Navigation

```html
<!-- HTML structure for responsive navigation -->
<nav class="main-navigation" role="navigation">
    <div class="nav-container">
        <div class="nav-brand">
            <a href="<?php echo home_url(); ?>">
                <?php bloginfo('name'); ?>
            </a>
        </div>
        
        <button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">
            <span class="menu-toggle-text"><?php _e('Menu', 'my-theme'); ?></span>
            <span class="menu-toggle-icon">
                <span></span>
                <span></span>
                <span></span>
            </span>
        </button>
        
        <?php
        wp_nav_menu(array(
            'theme_location' => 'primary',
            'menu_id' => 'primary-menu',
            'container' => false,
            'menu_class' => 'nav-menu',
            'fallback_cb' => false
        ));
        ?>
    </div>
</nav>
```

### Responsive Navigation CSS

```css
/* Responsive navigation styles */
.main-navigation {
    position: relative;
    background: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

.nav-brand a {
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    color: #333;
}

.menu-toggle {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
}

.menu-toggle-icon {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.menu-toggle-icon span {
    width: 25px;
    height: 3px;
    background: #333;
    transition: all 0.3s ease;
}

.nav-menu {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 2rem;
}

.nav-menu li {
    position: relative;
}

.nav-menu a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
    transition: color 0.3s ease;
}

.nav-menu a:hover {
    color: #0073aa;
}

/* Dropdown styles */
.nav-menu .sub-menu {
    position: absolute;
    top: 100%;
    left: 0;
    background: #fff;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    min-width: 200px;
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.3s ease;
    z-index: 1000;
}

.nav-menu li:hover .sub-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.sub-menu li {
    border-bottom: 1px solid #eee;
}

.sub-menu a {
    display: block;
    padding: 0.75rem 1rem;
}

/* Mobile styles */
@media (max-width: 768px) {
    .menu-toggle {
        display: block;
    }
    
    .nav-menu {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: #fff;
        flex-direction: column;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }
    
    .nav-menu.active {
        max-height: 500px;
    }
    
    .nav-menu li {
        border-bottom: 1px solid #eee;
    }
    
    .nav-menu a {
        display: block;
        padding: 1rem;
    }
    
    .sub-menu {
        position: static;
        opacity: 1;
        visibility: visible;
        transform: none;
        box-shadow: none;
        background: #f8f8f8;
    }
    
    .sub-menu a {
        padding-left: 2rem;
    }
}
```

### Mobile Navigation JavaScript

```javascript
// Mobile navigation functionality
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            this.setAttribute('aria-expanded', !isExpanded);
            navMenu.classList.toggle('active');
            
            // Update toggle text
            const toggleText = this.querySelector('.menu-toggle-text');
            if (toggleText) {
                toggleText.textContent = isExpanded ? 'Menu' : 'Close';
            }
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!menuToggle.contains(e.target) && !navMenu.contains(e.target)) {
                menuToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
            }
        });
        
        // Close menu on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                menuToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
            }
        });
    }
});
```

## Breadcrumb Navigation

### Breadcrumb Implementation

```php
// Breadcrumb navigation function
function get_breadcrumbs() {
    $breadcrumbs = array();
    
    // Home link
    $breadcrumbs[] = array(
        'title' => __('Home', 'my-theme'),
        'url' => home_url('/'),
        'current' => is_home() && is_front_page()
    );
    
    if (is_category() || is_single()) {
        // Category breadcrumb
        $category = get_the_category();
        if ($category) {
            $breadcrumbs[] = array(
                'title' => $category[0]->name,
                'url' => get_category_link($category[0]->term_id),
                'current' => false
            );
        }
    }
    
    if (is_single()) {
        // Single post
        $breadcrumbs[] = array(
            'title' => get_the_title(),
            'url' => '',
            'current' => true
        );
    } elseif (is_page()) {
        // Page breadcrumb
        $page_id = get_the_ID();
        $ancestors = get_post_ancestors($page_id);
        
        if ($ancestors) {
            $ancestors = array_reverse($ancestors);
            foreach ($ancestors as $ancestor_id) {
                $breadcrumbs[] = array(
                    'title' => get_the_title($ancestor_id),
                    'url' => get_permalink($ancestor_id),
                    'current' => false
                );
            }
        }
        
        $breadcrumbs[] = array(
            'title' => get_the_title(),
            'url' => '',
            'current' => true
        );
    } elseif (is_category()) {
        // Category page
        $breadcrumbs[] = array(
            'title' => single_cat_title('', false),
            'url' => '',
            'current' => true
        );
    }
    
    return $breadcrumbs;
}

// Display breadcrumbs
function display_breadcrumbs() {
    $breadcrumbs = get_breadcrumbs();
    
    if (count($breadcrumbs) <= 1) {
        return; // Don't show breadcrumbs if only home
    }
    
    echo '<nav class="breadcrumbs" aria-label="Breadcrumb">';
    echo '<ol class="breadcrumb-list">';
    
    foreach ($breadcrumbs as $index => $breadcrumb) {
        echo '<li class="breadcrumb-item' . ($breadcrumb['current'] ? ' current' : '') . '">';
        
        if ($breadcrumb['current']) {
            echo '<span aria-current="page">' . esc_html($breadcrumb['title']) . '</span>';
        } else {
            echo '<a href="' . esc_url($breadcrumb['url']) . '">' . esc_html($breadcrumb['title']) . '</a>';
        }
        
        echo '</li>';
        
        // Add separator (except for last item)
        if ($index < count($breadcrumbs) - 1) {
            echo '<li class="breadcrumb-separator" aria-hidden="true">›</li>';
        }
    }
    
    echo '</ol>';
    echo '</nav>';
}
```

## Menu Performance Optimization

### Menu Caching

```php
// Cache menu output for performance
function get_cached_menu($theme_location, $args = array()) {
    $cache_key = 'menu_' . $theme_location . '_' . md5(serialize($args));
    $cached_menu = get_transient($cache_key);
    
    if ($cached_menu === false) {
        ob_start();
        wp_nav_menu(array_merge(array('theme_location' => $theme_location), $args));
        $cached_menu = ob_get_clean();
        
        // Cache for 1 hour
        set_transient($cache_key, $cached_menu, HOUR_IN_SECONDS);
    }
    
    return $cached_menu;
}

// Clear menu cache when menu is updated
function clear_menu_cache($menu_id) {
    $locations = get_nav_menu_locations();
    foreach ($locations as $location => $menu_id_in_location) {
        if ($menu_id_in_location == $menu_id) {
            delete_transient('menu_' . $location . '_*');
        }
    }
}
add_action('wp_update_nav_menu', 'clear_menu_cache');
```

## Accessibility Features

### Accessible Navigation

```php
// Add accessibility attributes to menu
function add_menu_accessibility_attributes($atts, $item, $args) {
    // Add aria-label for external links
    if ($item->object == 'custom' && strpos($item->url, 'http') === 0 && !strpos($item->url, home_url()) === 0) {
        $atts['aria-label'] = $item->title . ' (opens in new window)';
    }
    
    // Add skip link for main navigation
    if ($args->theme_location == 'primary') {
        $atts['aria-current'] = (is_front_page() && $item->url == home_url('/')) ? 'page' : '';
    }
    
    return $atts;
}
add_filter('nav_menu_link_attributes', 'add_menu_accessibility_attributes', 10, 3);
```

## Official Documentation

https://developer.wordpress.org/themes/functionality/navigation-menus/
https://developer.wordpress.org/reference/classes/walker_nav_menu/
https://developer.wordpress.org/themes/basics/navigation-menus/
