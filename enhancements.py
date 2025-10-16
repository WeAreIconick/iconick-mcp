#!/usr/bin/env python3
"""
MCP Server Enhancements - Code to add to wordpress_mcp.py

This file contains all the new features ready to be integrated.
"""

# Add this after the existing resources, before the prompts section

SNIPPET_RESOURCE_CODE = '''
# === CODE SNIPPETS LIBRARY ===

@mcp.resource("wordpress://snippets/{category}/{topic}")
def get_code_snippet(uri: str) -> str:
    """
    Get WordPress code snippets by category and topic
    
    Examples:
      wordpress://snippets/security/sanitize-input
      wordpress://snippets/ajax/admin-ajax
      wordpress://snippets/cpt/register-custom-post-type
      wordpress://snippets/hooks/action-hooks
      wordpress://snippets/database/wpdb-queries
      wordpress://snippets/rest-api/custom-endpoint
      wordpress://snippets/blocks/register-block
      wordpress://snippets/forms/settings-api
      wordpress://snippets/admin/add-admin-page
      wordpress://snippets/performance/caching-transients
    """
    from urllib.parse import urlparse
    
    try:
        path = urlparse(uri).path
        parts = [p for p in path.split('/') if p]
        
        if len(parts) < 2:
            return "Error: URI must be in format wordpress://snippets/{category}/{topic}"
        
        category = parts[1] if len(parts) > 1 else None
        topic = parts[2] if len(parts) > 2 else None
        
        if not category or not topic:
            return list_available_snippets()
        
        return load_resource_content("snippets/" + category, topic)
        
    except FileNotFoundError as e:
        return str(e) + "\\n\\nAvailable categories: security, ajax, cpt, hooks, database, rest-api, blocks, forms, admin, performance"
    except Exception as e:
        return f"Error loading snippet: {str(e)}"

def list_available_snippets() -> str:
    """List all available code snippets"""
    snippets_dir = RESOURCES_DIR / "snippets"
    
    if not snippets_dir.exists():
        return "Snippets directory not found"
    
    output = "# Available WordPress Code Snippets\\n\\n"
    
    for category_dir in sorted(snippets_dir.iterdir()):
        if category_dir.is_dir():
            category = category_dir.name
            output += f"## {category.replace('-', ' ').title()}\\n"
            
            for snippet_file in sorted(category_dir.glob("*.md")):
                topic = snippet_file.stem
                output += f"- `wordpress://snippets/{category}/{topic}`\\n"
            
            output += "\\n"
    
    return output
'''

# New tools to add

CODE_GENERATOR_TOOL = '''
@mcp.tool()
def generate_wordpress_component(
    component_type: str,
    name: str,
    description: str = "",
    features: list = None
) -> str:
    """
    Generate WordPress component code from specifications
    
    Args:
        component_type: plugin, block, cpt, taxonomy, shortcode, widget, rest-endpoint
        name: Component name
        description: What the component should do
        features: Optional list of features (admin-ui, rest-api, ajax, etc.)
    
    Returns:
        Complete, production-ready code with files and structure
        
    Examples:
        generate_wordpress_component("cpt", "Portfolio", "Showcase work items", ["rest-api", "archive"])
        generate_wordpress_component("plugin", "Contact Form", "Simple contact form with email", ["admin-ui", "ajax"])
        generate_wordpress_component("rest-endpoint", "Products", "Product API endpoint", ["auth"])
    """
    if features is None:
        features = []
    
    generators = {
        'plugin': generate_plugin_starter,
        'cpt': generate_custom_post_type,
        'taxonomy': generate_taxonomy,
        'shortcode': generate_shortcode,
        'widget': generate_widget,
        'rest-endpoint': generate_rest_endpoint,
        'block': generate_gutenberg_block,
        'meta-box': generate_meta_box,
        'admin-page': generate_admin_page
    }
    
    if component_type not in generators:
        return f"❌ Invalid component type. Available: {', '.join(generators.keys())}"
    
    try:
        generator_func = generators[component_type]
        return generator_func(name, description, features)
    except Exception as e:
        return f"❌ Error generating component: {str(e)}"

def generate_custom_post_type(name: str, description: str, features: list) -> str:
    """Generate custom post type registration code"""
    slug = name.lower().replace(' ', '_')
    singular = name
    plural = name + 's' if not name.endswith('s') else name
    
    has_rest = 'rest-api' in features or 'rest' in features
    has_archive = 'archive' in features
    is_hierarchical = 'hierarchical' in features
    
    code = f"""# Custom Post Type: {name}

## Description
{description or f"Custom post type for managing {plural.lower()}"}

## Installation
Add this code to your theme's functions.php or create a plugin.

## Registration Code

```php
function register_{slug}_post_type() {{
    $labels = array(
        'name'               => _x( '{plural}', 'post type general name', 'textdomain' ),
        'singular_name'      => _x( '{singular}', 'post type singular name', 'textdomain' ),
        'menu_name'          => _x( '{plural}', 'admin menu', 'textdomain' ),
        'name_admin_bar'     => _x( '{singular}', 'add new on admin bar', 'textdomain' ),
        'add_new'            => _x( 'Add New', '{slug}', 'textdomain' ),
        'add_new_item'       => __( 'Add New {singular}', 'textdomain' ),
        'new_item'           => __( 'New {singular}', 'textdomain' ),
        'edit_item'          => __( 'Edit {singular}', 'textdomain' ),
        'view_item'          => __( 'View {singular}', 'textdomain' ),
        'all_items'          => __( 'All {plural}', 'textdomain' ),
        'search_items'       => __( 'Search {plural}', 'textdomain' ),
        'not_found'          => __( 'No {plural.lower()} found.', 'textdomain' ),
        'not_found_in_trash' => __( 'No {plural.lower()} found in Trash.', 'textdomain' )
    );

    $args = array(
        'labels'             => $labels,
        'description'        => __( '{description}', 'textdomain' ),
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'query_var'          => true,
        'rewrite'            => array( 'slug' => '{slug.replace("_", "-")}' ),
        'capability_type'    => 'post',
        'has_archive'        => {'true' if has_archive else 'false'},
        'hierarchical'       => {'true' if is_hierarchical else 'false'},
        'menu_position'      => null,
        'menu_icon'          => 'dashicons-admin-post',
        'show_in_rest'       => {'true' if has_rest else 'false'},
        'supports'           => array( 'title', 'editor', 'thumbnail', 'excerpt', 'custom-fields' )
    );

    register_post_type( '{slug}', $args );
    
    // Flush rewrite rules on activation
    flush_rewrite_rules();
}}
add_action( 'init', 'register_{slug}_post_type' );
```

## Usage

After adding this code:

1. **Activate/refresh** to register the post type
2. **Go to dashboard** - You'll see "{plural}" in the menu
3. **Create new items** - Add your {plural.lower()}
4. **Display in templates** - Use the query code below

## Query {plural}

```php
// Get all {plural.lower()}
$args = array(
    'post_type' => '{slug}',
    'posts_per_page' => 10,
    'orderby' => 'date',
    'order' => 'DESC'
);

$query = new WP_Query( $args );

if ( $query->have_posts() ) {{
    while ( $query->have_posts() ) {{
        $query->the_post();
        ?>
        <article>
            <h2><?php the_title(); ?></h2>
            <?php if ( has_post_thumbnail() ) {{ the_post_thumbnail(); }} ?>
            <div><?php the_content(); ?></div>
        </article>
        <?php
    }}
    wp_reset_postdata();
}}
```
"""
    
    if has_rest:
        code += f"""
## REST API Access

The {singular} post type is available via REST API at:
```
GET /wp-json/wp/v2/{slug.replace('_', '-')}
GET /wp-json/wp/v2/{slug.replace('_', '-')}/{{id}}
POST /wp-json/wp/v2/{slug.replace('_', '-')}
```

### Example: Fetch via JavaScript

```javascript
fetch('/wp-json/wp/v2/{slug.replace("_", "-")}')
    .then(response => response.json())
    .then(data => console.log(data));
```
"""
    
    return code

def generate_plugin_starter(name: str, description: str, features: list) -> str:
    """Generate complete plugin starter code"""
    slug = name.lower().replace(' ', '-')
    class_name = ''.join(word.capitalize() for word in name.split())
    const_prefix = slug.upper().replace('-', '_')
    
    has_admin = 'admin-ui' in features or 'admin' in features
    has_ajax = 'ajax' in features
    has_rest = 'rest-api' in features or 'rest' in features
    
    code = f"""# WordPress Plugin: {name}

## Description
{description or f"A WordPress plugin for {name.lower()}"}

## File Structure

```
{slug}/
├── {slug}.php (main plugin file)
├── README.md
├── includes/
│   ├── class-{slug}.php
│   ├── class-activator.php
│   └── class-deactivator.php"""
    
    if has_admin:
        code += f"""
├── admin/
│   ├── class-admin.php
│   ├── css/
│   │   └── admin.css
│   └── js/
│       └── admin.js"""
    
    code += f"""
├── public/
│   ├── class-public.php
│   ├── css/
│   │   └── public.css
│   └── js/
│       └── public.js
├── languages/
│   └── {slug}.pot
└── uninstall.php
```

## Main Plugin File: {slug}.php

```php
<?php
/**
 * Plugin Name:       {name}
 * Plugin URI:        https://example.com/{slug}
 * Description:       {description}
 * Version:           1.0.0
 * Requires at least: 6.0
 * Requires PHP:      7.4
 * Author:            Your Name
 * Author URI:        https://example.com
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       {slug}
 * Domain Path:       /languages
 */

// If this file is called directly, abort.
if ( ! defined( 'WPINC' ) ) {{
    die;
}}

// Plugin version
define( '{const_prefix}_VERSION', '1.0.0' );

// Plugin path
define( '{const_prefix}_PATH', plugin_dir_path( __FILE__ ) );

// Plugin URL
define( '{const_prefix}_URL', plugin_dir_url( __FILE__ ) );

/**
 * Activation hook
 */
function activate_{slug.replace('-', '_')}() {{
    require_once {const_prefix}_PATH . 'includes/class-activator.php';
    {class_name}_Activator::activate();
}}
register_activation_hook( __FILE__, 'activate_{slug.replace('-', '_')}' );

/**
 * Deactivation hook
 */
function deactivate_{slug.replace('-', '_')}() {{
    require_once {const_prefix}_PATH . 'includes/class-deactivator.php';
    {class_name}_Deactivator::deactivate();
}}
register_deactivation_hook( __FILE__, 'deactivate_{slug.replace('-', '_')}' );

/**
 * Load plugin
 */
require {const_prefix}_PATH . 'includes/class-{slug}.php';

/**
 * Initialize plugin
 */
function run_{slug.replace('-', '_')}() {{
    $plugin = new {class_name}();
    $plugin->run();
}}
run_{slug.replace('-', '_')}();
```

## Main Class: includes/class-{slug}.php

```php
<?php
/**
 * Main plugin class
 */
class {class_name} {{

    protected $version;
    protected $plugin_name;

    public function __construct() {{
        $this->version = {const_prefix}_VERSION;
        $this->plugin_name = '{slug}';
        
        $this->load_dependencies();
        $this->define_hooks();
    }}

    private function load_dependencies() {{
        require_once {const_prefix}_PATH . 'includes/class-activator.php';
        require_once {const_prefix}_PATH . 'includes/class-deactivator.php';
        {'require_once ' + const_prefix + '_PATH . "admin/class-admin.php";' if has_admin else ''}
        require_once {const_prefix}_PATH . 'public/class-public.php';
    }}

    private function define_hooks() {{
        {'$admin = new ' + class_name + '_Admin($this->plugin_name, $this->version);' if has_admin else ''}
        $public = new {class_name}_Public( $this->plugin_name, $this->version );
        
        {'// Admin hooks' if has_admin else ''}
        {'add_action("admin_enqueue_scripts", array($admin, "enqueue_styles"));' if has_admin else ''}
        {'add_action("admin_enqueue_scripts", array($admin, "enqueue_scripts"));' if has_admin else ''}
        
        // Public hooks
        add_action( 'wp_enqueue_scripts', array( $public, 'enqueue_styles' ) );
        add_action( 'wp_enqueue_scripts', array( $public, 'enqueue_scripts' ) );
    }}

    public function run() {{
        // Plugin is running
    }}
}}
```

## Activator: includes/class-activator.php

```php
<?php
class {class_name}_Activator {{

    public static function activate() {{
        // Activation tasks
        
        // Create custom table if needed
        global $wpdb;
        $table_name = $wpdb->prefix . '{slug.replace('-', '_')}';
        
        // Add default options
        add_option( '{slug}_version', {const_prefix}_VERSION );
        add_option( '{slug}_settings', array() );
        
        // Flush rewrite rules
        flush_rewrite_rules();
    }}
}}
```

## Deactivator: includes/class-deactivator.php

```php
<?php
class {class_name}_Deactivator {{

    public static function deactivate() {{
        // Deactivation tasks
        flush_rewrite_rules();
    }}
}}
```

## Uninstall: uninstall.php

```php
<?php
/**
 * Uninstall script
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {{
    exit;
}}

// Delete options
delete_option( '{slug}_version' );
delete_option( '{slug}_settings' );

// Delete post meta
delete_post_meta_by_key( '_{slug}_meta' );

// Drop custom tables
global $wpdb;
$wpdb->query( "DROP TABLE IF EXISTS {{$wpdb->prefix}}{slug.replace('-', '_')}" );

// Clear scheduled hooks
wp_clear_scheduled_hook( '{slug}_daily_task' );
```

## Next Steps

1. Copy all files to `wp-content/plugins/{slug}/`
2. Activate the plugin in WordPress
3. Configure settings (if admin UI is included)
4. Start customizing for your needs
5. Test with Plugin Check before submitting

## Security Checklist

- [ ] All inputs validated
- [ ] All outputs escaped
- [ ] Nonces on all forms
- [ ] Capability checks on all actions
- [ ] Prepared statements for database
- [ ] No hardcoded secrets

## Testing

```bash
# Install Plugin Check
wp plugin install plugin-check --activate

# Check your plugin
wp plugin check {slug}
```
"""
    
    return code

# Print the code sections
print("SNIPPET_RESOURCE_CODE section:")
print("=" * 60)
print(SNIPPET_RESOURCE_CODE)
print()

if __name__ == '__main__':
    print("✅ Enhancement code ready")
    print("These sections need to be added to wordpress_mcp.py")

