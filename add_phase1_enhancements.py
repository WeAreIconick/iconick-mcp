#!/usr/bin/env python3
"""
Phase 1 Enhancements - Safe Integration
Adds: Snippet list resource + 8 more prompts + 3 code generator tools
"""

import re
import shutil

def backup():
    shutil.copy('wordpress_mcp.py', 'wordpress_mcp.py.backup')
    print("✅ Backup created")

SNIPPET_LIST_RESOURCE = '''
@mcp.resource("wordpress://snippets/list")
def list_code_snippets() -> str:
    """Complete list of all available code snippets"""
    return """# WordPress Code Snippets Library

Quick-reference code examples for common WordPress development tasks.

## Security (5 snippets)
- **sanitize-input** - Sanitize all types of user input
- **escape-output** - Escape output for HTML, attributes, URLs, JS
- **nonces** - CSRF protection with nonces
- **capability-checks** - User permission verification
- **sql-injection-prevention** - Safe database queries

## AJAX (3 snippets)
- **admin-ajax** - Complete admin AJAX pattern
- **frontend-ajax** - Public-facing AJAX
- **heartbeat-api** - WordPress Heartbeat API

## Custom Post Types (2 snippets)
- **register-custom-post-type** - Complete CPT registration
- **cpt-query-examples** - Query custom post types

## Hooks (2 snippets)
- **action-hooks** - Common action hooks
- **filter-hooks** - Common filter hooks

## Database (2 snippets)
- **wpdb-queries** - $wpdb query examples
- **custom-tables** - Create and use custom tables

## REST API (2 snippets)
- **custom-endpoint** - Register REST endpoints
- **rest-authentication** - API authentication

## Blocks (1 snippet)
- **register-block** - Gutenberg block registration

## Forms (1 snippet)
- **settings-api** - WordPress Settings API

## Admin (2 snippets)
- **add-admin-page** - Create admin pages
- **meta-box** - Add meta boxes

## Performance (2 snippets)
- **caching-transients** - Cache with transients
- **object-cache** - WordPress object caching

---

**Total: 22 Ready-to-Use Code Snippets**

To view a specific snippet, ask your AI assistant for it by category and name.
Example: "Show me the sanitize-input snippet" or "Get the admin-ajax example"
"""
'''

EXTRA_PROMPTS = '''
@mcp.prompt()
def woocommerce_development():
    """WooCommerce development and customization workflow"""
    return """I'm developing a WooCommerce extension. Let's work through it:

## What Are You Building?

1. Payment Gateway
2. Shipping Method  
3. Product Type
4. Custom Fields
5. Email Template
6. Integration

Tell me which and I'll guide you through WooCommerce-specific hooks, security, and testing!
"""

@mcp.prompt()
def gutenberg_block_development():
    """Modern Gutenberg block development with React"""
    return """Let's build a Gutenberg block with React:

## Block Development Steps

1. Setup (@wordpress/create-block or manual)
2. block.json configuration
3. React edit component
4. Attributes and controls
5. InspectorControls and toolbar
6. Build and test

Describe your block idea and I'll provide complete React code!
"""

@mcp.prompt()
def rest_api_development():
    """WordPress REST API development workflow"""
    return """Building a WordPress REST API:

## API Design

1. What resources? (posts, products, custom data)
2. What operations? (GET, POST, PUT, DELETE)
3. Authentication needed?
4. Public or private?

I'll help you create secure, well-documented REST endpoints!
"""

@mcp.prompt()
def multisite_development():
    """WordPress Multisite development guide"""
    return """Working with WordPress Multisite:

## Multisite Development

1. Network vs Site code
2. Network activation
3. Cross-site queries
4. Site switching
5. Super Admin capabilities

What multisite feature are you building?
"""

@mcp.prompt()
def database_optimization():
    """Database performance optimization workflow"""
    return """Let's optimize your WordPress database:

## Optimization Areas

1. Slow queries (EXPLAIN analysis)
2. Index optimization
3. N+1 query problems
4. Table cleanup
5. Transient management

Share your performance issue and I'll help fix it!
"""

@mcp.prompt()
def accessibility_compliance():
    """WCAG 2.1 accessibility compliance guide"""
    return """Making your site accessible (WCAG 2.1 Level AA):

## Compliance Areas

1. Perceivable (alt text, contrast, headings)
2. Operable (keyboard, skip links, focus)
3. Understandable (labels, errors, consistency)
4. Robust (valid HTML, ARIA)

I'll audit your code for accessibility issues!
"""

@mcp.prompt()
def deployment_workflow():
    """WordPress deployment and DevOps workflow"""
    return """Setting up WordPress deployment:

## Deployment Pipeline

1. Environment setup (dev/staging/prod)
2. Version control (Git workflow)
3. CI/CD (GitHub Actions, automated tests)
4. Database migrations
5. Zero-downtime deployment

What's your current deployment process?
"""

@mcp.prompt()
def troubleshooting_guide():
    """WordPress debugging and troubleshooting"""
    return """Debugging WordPress issues:

## Common Problems

1. White Screen of Death
2. Database connection errors
3. Plugin conflicts
4. Performance issues
5. 500 errors

## Debug Tools

- WP_DEBUG
- Query Monitor
- Error logs
- Browser console

What issue are you experiencing?
"""
'''

CODE_GEN_TOOLS = '''
@mcp.tool()
def generate_custom_post_type(
    name: str,
    description: str = "",
    has_archive: bool = True,
    hierarchical: bool = False
) -> str:
    """
    Generate complete custom post type registration code
    
    Args:
        name: Post type name (e.g., "Portfolio", "Event")
        description: Purpose of this post type
        has_archive: Enable archive pages
        hierarchical: Page-like (True) or post-like (False)
    """
    slug = name.lower().replace(' ', '_')
    plural = name + 's' if not name.endswith('s') else name
    
    return f"""# Custom Post Type: {name}

```php
function register_{slug}_cpt() {{
    register_post_type( '{slug}', array(
        'labels' => array(
            'name' => '{plural}',
            'singular_name' => '{name}'
        ),
        'public' => true,
        'has_archive' => {'true' if has_archive else 'false'},
        'hierarchical' => {'true' if hierarchical else 'false'},
        'show_in_rest' => true,
        'supports' => array( 'title', 'editor', 'thumbnail' ),
        'menu_icon' => 'dashicons-admin-post'
    ));
}}
add_action( 'init', 'register_{slug}_cpt' );
```

Visit Settings > Permalinks to activate!
"""

@mcp.tool()
def generate_shortcode(name: str, description: str = "") -> str:
    """
    Generate WordPress shortcode code
    
    Args:
        name: Shortcode name (e.g., "pricing_table")
        description: What the shortcode does
    """
    func_name = name.replace('-', '_')
    
    return f"""# Shortcode: [{name}]

{description}

```php
function {func_name}_shortcode( $atts ) {{
    $atts = shortcode_atts( array(
        'title' => '',
        'content' => ''
    ), $atts, '{name}' );
    
    ob_start();
    ?>
    <div class="{name}">
        <h3><?php echo esc_html( $atts['title'] ); ?></h3>
        <div><?php echo wp_kses_post( $atts['content'] ); ?></div>
    </div>
    <?php
    return ob_get_clean();
}}
add_shortcode( '{name}', '{func_name}_shortcode' );
```

Usage: [{name} title="My Title" content="Content here"]
"""

@mcp.tool()
def generate_rest_endpoint(namespace: str, route: str, methods: str = "GET") -> str:
    """
    Generate REST API endpoint code
    
    Args:
        namespace: API namespace (e.g., "myplugin/v1")
        route: Route path (e.g., "/items")
        methods: HTTP methods (GET, POST, PUT, DELETE)
    """
    callback = 'handle_' + route.replace('/', '_').strip('_')
    
    return f"""# REST API Endpoint

```php
add_action( 'rest_api_init', function() {{
    register_rest_route( '{namespace}', '{route}', array(
        'methods' => '{methods}',
        'callback' => '{callback}',
        'permission_callback' => function() {{
            return current_user_can( 'edit_posts' );
        }}
    ));
}});

function {callback}( $request ) {{
    $data = array(
        'message' => 'Endpoint working',
        'params' => $request->get_params()
    );
    
    return rest_ensure_response( $data );
}}
```

Access at: /wp-json/{namespace}{route}
"""
'''

def add_to_file():
    """Add all Phase 1 enhancements"""
    
    with open('wordpress_mcp.py', 'r') as f:
        content = f.read()
    
    # Find insertion point before prompts
    marker = '# === MCP PROMPTS ==='
    
    if marker not in content:
        print("❌ Could not find prompts marker")
        return False
    
    # Split and insert snippet resource
    parts = content.split(marker)
    new_content = parts[0] + SNIPPET_LIST_RESOURCE + '\\n' + marker + parts[1]
    
    # Now find end of prompts section to add more prompts
    tools_marker = '# === MCP TOOLS IMPLEMENTATION ==='
    if tools_marker in new_content:
        parts2 = new_content.split(tools_marker)
        new_content = parts2[0] + EXTRA_PROMPTS + '\\n' + tools_marker + parts2[1]
    
    # Find end of tools to add code gen tools
    # Add after backup_tool
    backup_tool_end = new_content.rfind('return f"Error running backup tool: {str(e)}"')
    
    if backup_tool_end > 0:
        # Find the newline after this line
        next_newline = new_content.find('\\n', backup_tool_end)
        new_content = new_content[:next_newline] + '\\n' + CODE_GEN_TOOLS + new_content[next_newline:]
    
    # Write new file
    with open('wordpress_mcp.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Added all Phase 1 enhancements")
    return True

def main():
    print("🚀 Adding Phase 1 Enhancements...")
    print()
    
    backup()
    
    if add_to_file():
        # Verify syntax
        import subprocess
        result = subprocess.run(['python3', '-m', 'py_compile', 'wordpress_mcp.py'],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            with open('wordpress_mcp.py', 'r') as f:
                content = f.read()
            
            resources = len(re.findall(r'@mcp\\.resource', content))
            tools = len(re.findall(r'@mcp\\.tool', content))
            prompts = len(re.findall(r'@mcp\\.prompt', content))
            
            print("\\n✅ PHASE 1 COMPLETE!\\n")
            print(f"📊 Server Stats:")
            print(f"   Resources: {resources} (+1 snippet list)")
            print(f"   Tools: {tools} (+3 code generators)")
            print(f"   Prompts: {prompts} (+8 workflows)")
            print(f"\\n✅ Syntax: VALID")
            
            return True
        else:
            print("❌ Syntax error:")
            print(result.stderr)
            shutil.copy('wordpress_mcp.py.backup', 'wordpress_mcp.py')
            print("✅ Restored backup")
            return False
    
    return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

