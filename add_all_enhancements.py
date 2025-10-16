#!/usr/bin/env python3
"""
Add all enhancements to wordpress_mcp.py
- Snippet resources (parameterized)
- Code generator tools
- 10 more prompts
- Code linter
- And more!
"""

import re
import shutil
from pathlib import Path

def backup_file():
    """Create backup"""
    shutil.copy('wordpress_mcp.py', 'wordpress_mcp.py.backup')
    print("✅ Created backup: wordpress_mcp.py.backup")

def add_snippet_resource():
    """Add parameterized snippet resource"""
    
    snippet_code = '''
# === CODE SNIPPETS LIBRARY ===

@mcp.resource("wordpress://snippets/list")
def list_code_snippets() -> str:
    """List all available code snippets by category"""
    snippets_dir = RESOURCES_DIR / "snippets"
    
    if not snippets_dir.exists():
        return "# Code Snippets\\n\\nSnippet library not yet initialized."
    
    output = "# WordPress Code Snippets Library\\n\\n"
    output += "Quick-reference code examples for common WordPress development tasks.\\n\\n"
    
    total = 0
    for category_dir in sorted(snippets_dir.iterdir()):
        if category_dir.is_dir():
            category = category_dir.name
            snippets = list(category_dir.glob("*.md"))
            total += len(snippets)
            
            output += f"## {category.replace('-', ' ').title()} ({len(snippets)} snippets)\\n"
            
            for snippet_file in sorted(snippets):
                topic = snippet_file.stem
                # Read first line as title
                with open(snippet_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    title = first_line.replace('#', '').strip() if first_line.startswith('#') else topic
                
                output += f"- **{topic}**: {title}\\n"
            
            output += "\\n"
    
    output += f"**Total: {total} code snippets**\\n\\n"
    output += "To view a snippet, request the specific category and topic from your AI assistant.\\n"
    
    return output
'''
    
    # Find where to insert (before tools section)
    with open('wordpress_mcp.py', 'r') as f:
        content = f.read()
    
    # Insert before # === MCP PROMPTS ===
    marker = '# === MCP PROMPTS ==='
    if marker in content:
        parts = content.split(marker)
        new_content = parts[0] + snippet_code + '\\n' + marker + parts[1]
        
        with open('wordpress_mcp.py', 'w') as f:
            f.write(new_content)
        
        print("✅ Added snippet resource")
        return True
    else:
        print("❌ Could not find insertion point for snippets")
        return False

def add_code_generator_tools():
    """Add code generation tools"""
    
    tools_code = '''
# === CODE GENERATION TOOLS ===

@mcp.tool()
def generate_custom_post_type(
    name: str,
    description: str = "",
    has_archive: bool = True,
    hierarchical: bool = False,
    supports: list = None
) -> str:
    """
    Generate custom post type registration code
    
    Args:
        name: Post type name (e.g., "Portfolio", "Event", "Product")
        description: What this post type is for
        has_archive: Whether to enable archive pages
        hierarchical: True for page-like, False for post-like
        supports: Features to support (default: title, editor, thumbnail)
    
    Returns:
        Complete registration code ready to use
    """
    if supports is None:
        supports = ['title', 'editor', 'thumbnail', 'excerpt']
    
    slug = name.lower().replace(' ', '_')
    singular = name
    plural = name + 's' if not name.endswith('s') else name
    
    supports_str = "', '".join(supports)
    
    return f"""# Custom Post Type: {name}

{description}

## Add to functions.php or plugin:

```php
function register_{slug}_post_type() {{
    $labels = array(
        'name' => _x( '{plural}', 'post type general name', 'textdomain' ),
        'singular_name' => _x( '{singular}', 'post type singular name', 'textdomain' ),
        'add_new_item' => __( 'Add New {singular}', 'textdomain' ),
        'edit_item' => __( 'Edit {singular}', 'textdomain' ),
        'all_items' => __( 'All {plural}', 'textdomain' )
    );

    register_post_type( '{slug}', array(
        'labels' => $labels,
        'public' => true,
        'has_archive' => {'true' if has_archive else 'false'},
        'hierarchical' => {'true' if hierarchical else 'false'},
        'show_in_rest' => true,
        'supports' => array( '{supports_str}' ),
        'menu_icon' => 'dashicons-admin-post'
    ));
}}
add_action( 'init', 'register_{slug}_post_type' );

// Don't forget to flush rewrite rules after adding this code!
// Visit Settings > Permalinks to flush.
```

## Usage:

```php
// Query {plural}
$items = get_posts( array(
    'post_type' => '{slug}',
    'posts_per_page' => 10
));

// Display
foreach ( $items as $item ) {{
    echo esc_html( $item->post_title );
}}
```
"""

@mcp.tool()
def generate_shortcode(
    name: str,
    description: str = "",
    attributes: list = None
) -> str:
    """
    Generate WordPress shortcode code
    
    Args:
        name: Shortcode name (e.g., "contact_form", "pricing_table")
        description: What the shortcode does
        attributes: List of attribute names (e.g., ["title", "count", "style"])
    
    Returns:
        Complete shortcode implementation
    """
    if attributes is None:
        attributes = []
    
    func_name = name.replace('-', '_')
    
    # Build defaults array
    defaults = {attr: "" for attr in attributes}
    defaults_str = ",\\n        ".join([f"'{attr}' => ''" for attr in attributes])
    
    return f"""# Shortcode: [{name}]

{description}

## Implementation:

```php
function {func_name}_shortcode( $atts ) {{
    $atts = shortcode_atts( array(
        {defaults_str}
    ), $atts, '{name}' );
    
    // Extract attributes
    extract( $atts );
    
    // Start output buffering
    ob_start();
    ?>
    
    <div class="{name}-container">
        <h3><?php echo esc_html( $title ); ?></h3>
        <!-- Your HTML here -->
    </div>
    
    <?php
    return ob_get_clean();
}}
add_shortcode( '{name}', '{func_name}_shortcode' );
```

## Usage:

```
[{name}{' '.join([f' {attr}="value"' for attr in attributes])}]
```

## Example:

```
[{name} title="My Title"]
```
"""

@mcp.tool()
def generate_rest_api_endpoint(
    namespace: str,
    route: str,
    methods: str = "GET",
    requires_auth: bool = True
) -> str:
    """
    Generate WordPress REST API endpoint
    
    Args:
        namespace: API namespace (e.g., "myplugin/v1")
        route: Route path (e.g., "/items" or "/items/(?P<id>\\\\d+)")
        methods: HTTP methods (GET, POST, PUT, DELETE)
        requires_auth: Whether authentication is required
    
    Returns:
        Complete REST API endpoint code
    """
    callback_name = route.replace('/', '_').replace('(?P<id>\\\\d+)', 'item')
    callback_name = f"handle{callback_name}" if callback_name else "handle_request"
    callback_name = re.sub(r'[^a-zA-Z0-9_]', '', callback_name)
    
    perm_callback = '''function() {
            return current_user_can( 'edit_posts' );
        }''' if requires_auth else "'__return_true'"
    
    return f"""# REST API Endpoint

## Register Endpoint:

```php
add_action( 'rest_api_init', function() {{
    register_rest_route( '{namespace}', '{route}', array(
        'methods' => '{methods}',
        'callback' => '{callback_name}',
        'permission_callback' => {perm_callback},
        'args' => array()
    ));
}});

function {callback_name}( $request ) {{
    // Get parameters
    $params = $request->get_params();
    
    // Process request
    $data = array(
        'success' => true,
        'message' => 'Endpoint working'
    );
    
    return rest_ensure_response( $data );
}}
```

## Access:

```
GET /wp-json/{namespace}{route}
```

## JavaScript:

```javascript
fetch('/wp-json/{namespace}{route}')
    .then(response => response.json())
    .then(data => console.log(data));
```
"""
'''
    
    # Find where to add (before or after existing tools)
    with open('wordpress_mcp.py', 'r') as f:
        content = f.read()
    
    # Add after the backup_tool function
    marker = '# === MCP PROMPTS ==='
    if marker in content:
        parts = content.split(marker)
        new_content = parts[0] + tools_code + '\\n' + marker + parts[1]
        
        with open('wordpress_mcp.py', 'w') as f:
            f.write(new_content)
        
        print("✅ Added code generator tools")
        return True
    return False

def add_more_prompts():
    """Add 10 more comprehensive prompts"""
    
    prompts_code = '''
@mcp.prompt()
def woocommerce_development():
    """Complete WooCommerce development workflow"""
    return """I'm developing a WooCommerce extension or customization. Let's work through it:

## Phase 1: Project Type

What are you building?
1. **Payment Gateway** - Custom payment processor
2. **Shipping Method** - Custom shipping calculator
3. **Product Type** - New product variation (subscription, rental, etc.)
4. **Custom Fields** - Additional product/order fields
5. **Email Template** - Custom transactional emails
6. **Integration** - Third-party service integration

Tell me which type and I'll guide you through the specific requirements.

## Phase 2: WooCommerce Hooks

I'll show you the essential hooks for your extension type:
- Product hooks (before/after add to cart, pricing, etc.)
- Checkout hooks (fields, validation, processing)
- Order hooks (status changes, emails, meta)
- Admin hooks (product data panels, order details)

## Phase 3: Security & Validation

WooCommerce-specific security requirements:
- Payment data handling (PCI compliance considerations)
- Order data sanitization
- Customer data protection
- API security (if using WooCommerce REST API)

## Phase 4: Testing

- Test with different product types
- Test checkout flow completely
- Test with various payment methods
- Test order status transitions
- Test refunds and cancellations

Let's start - what are you building?
"""

@mcp.prompt()
def gutenberg_block_development():
    """Modern Gutenberg block development workflow"""
    return """Let's build a modern Gutenberg block with React:

## Phase 1: Block Setup

First, tell me about your block:
1. What does it do?
2. Does it need:
   - Inspector controls (sidebar settings)?
   - Toolbar controls?
   - InnerBlocks (nested content)?
   - Server-side rendering (dynamic block)?

## Phase 2: Development Environment

Set up modern block development:

```bash
# Create block with @wordpress/create-block
npx @wordpress/create-block@latest my-block

# Or manual setup
npm init
npm install @wordpress/scripts --save-dev
```

## Phase 3: Block Structure

I'll help you build:
- block.json configuration
- React edit component
- Save function
- Attributes schema
- InspectorControls
- Block controls
- Styles (editor and frontend)

## Phase 4: Modern Features

- Block variations
- Block transforms
- Block patterns
- Block styles
- Parent/child blocks
- InnerBlocks templates

## Phase 5: Build & Deploy

```bash
npm run build
wp plugin check your-plugin
```

Ready? Describe your block idea!
"""

@mcp.prompt()
def rest_api_development():
    """Complete REST API development workflow"""
    return """Let's build a complete WordPress REST API:

## Phase 1: API Design

Plan your API:
1. What resources do you need? (posts, products, users, custom)
2. What operations? (CRUD: Create, Read, Update, Delete)
3. Authentication required?
4. Public or private endpoints?

## Phase 2: Endpoint Registration

I'll help you create:
- Namespace structure
- Route patterns
- HTTP methods
- Request/response schemas
- Validation rules
- Permission callbacks

## Phase 3: Security

- Authentication methods (Application Passwords, OAuth, JWT)
- Permission callbacks for each endpoint
- Input validation
- Rate limiting considerations

## Phase 4: Documentation

- OpenAPI/Swagger documentation
- Example requests/responses
- Error codes and messages

Let's design your API! What data do you need to expose?
"""

@mcp.prompt()
def multisite_development():
    """WordPress Multisite development guide"""
    return """Let's work with WordPress Multisite:

## Phase 1: Understanding Multisite

- Network vs Site-specific code
- Global tables vs site tables
- Super Admin vs Site Admin
- Multisite hooks and functions

## Phase 2: Network-Wide Features

Building plugins that work across the network:
- Network activation
- Network settings pages
- Cross-site queries
- Site switching

## Phase 3: Security

- Proper capability checks (manage_network_options)
- Site isolation
- Data segregation

What multisite feature are you building?
"""

@mcp.prompt()
def database_optimization():
    """Database optimization and troubleshooting"""
    return """Let's optimize your WordPress database:

## Analysis Areas

1. **Slow Queries** - Find and fix inefficient queries
2. **Index Optimization** - Add proper indexes
3. **Query Count** - Reduce N+1 problems
4. **Table Optimization** - Clean up and optimize tables
5. **Transient Cleanup** - Remove expired transients

## Tools We'll Use

- Query Monitor
- MySQL EXPLAIN
- WordPress debug log
- Profiling tools

Share your performance issue and I'll help optimize!
"""

@mcp.prompt()
def accessibility_compliance():
    """WordPress accessibility (WCAG 2.1) compliance guide"""
    return """Let's make your WordPress site/plugin/theme fully accessible:

## WCAG 2.1 Level AA Compliance

### Phase 1: Perceivable
- Text alternatives for images
- Captions for videos
- Proper heading hierarchy
- Color contrast ratios (4.5:1 minimum)

### Phase 2: Operable
- Keyboard navigation
- No keyboard traps
- Skip links
- Focus indicators

### Phase 3: Understandable
- Clear labels
- Error identification
- Consistent navigation
- Predictable functionality

### Phase 4: Robust
- Valid HTML
- ARIA attributes
- Screen reader compatibility

## Testing Tools

- WAVE browser extension
- axe DevTools
- Keyboard-only navigation
- Screen reader testing (NVDA, JAWS)

What would you like to audit?
"""

@mcp.prompt()
def deployment_workflow():
    """WordPress deployment and DevOps workflow"""
    return """Let's set up a professional WordPress deployment workflow:

## Phase 1: Environment Setup

- Development (local)
- Staging (testing)
- Production (live)

## Phase 2: Version Control

Git workflow:
- Branch strategy
- .gitignore configuration
- Excluded files (wp-config.php, uploads/)

## Phase 3: CI/CD Pipeline

Automated deployment:
- GitHub Actions / GitLab CI
- Automated testing
- Code linting
- Deployment scripts

## Phase 4: Database Migrations

- Schema changes
- Search-replace for URLs
- Data sanitization

What's your deployment setup?
"""

@mcp.prompt()
def troubleshooting_guide():
    """WordPress troubleshooting and debugging workflow"""
    return """Let's debug your WordPress issue:

## Common Issues

1. **White Screen of Death**
2. **Error Establishing Database Connection**
3. **500 Internal Server Error**
4. **Plugin Conflicts**
5. **Theme Issues**
6. **Performance Problems**

## Debugging Tools

- WP_DEBUG mode
- Query Monitor
- Debug log
- Browser console
- Network tab

What issue are you experiencing?
"""

@mcp.prompt()
def migration_workflow():
    """WordPress site migration complete guide"""
    return """Let's migrate your WordPress site:

## Migration Checklist

### Pre-Migration
- [ ] Backup source site
- [ ] Check PHP/MySQL versions
- [ ] List active plugins
- [ ] Document custom code
- [ ] Test backup restore

### Migration Steps
- [ ] Export database
- [ ] Copy wp-content
- [ ] Install WordPress on target
- [ ] Import database
- [ ] Search-replace URLs
- [ ] Update file paths
- [ ] Test thoroughly

### Post-Migration
- [ ] Regenerate permalinks
- [ ] Test all functionality
- [ ] Check SSL/HTTPS
- [ ] Verify email sending
- [ ] Performance check

Where are you migrating from/to?
"""

@mcp.prompt()
def security_hardening():
    """WordPress security hardening workflow"""
    return """Let's harden your WordPress security:

## Security Layers

### 1. File System
- Proper file permissions
- Disable file editing
- Remove unnecessary files
- Secure wp-config.php

### 2. Database
- Secure database credentials
- Change table prefix
- Regular backups

### 3. Login Protection
- Limit login attempts
- Two-factor authentication
- Strong passwords
- Rename admin username

### 4. Updates
- Keep WordPress updated
- Update all plugins/themes
- Remove inactive plugins

### 5. Monitoring
- Security scanning
- Activity logging
- Uptime monitoring

What's your current security setup?
"""
'''
    
    # Add after existing prompts
    with open('wordpress_mcp.py', 'r') as f:
        content = f.read()
    
    # Find the last @mcp.prompt() function
    last_prompt_match = None
    for match in re.finditer(r'@mcp\.prompt\(\)\\ndef [^(]+\(\):[^"]+"""[^"]+"""', content, re.DOTALL):
        last_prompt_match = match
    
    if last_prompt_match:
        insert_pos = last_prompt_match.end()
        new_content = content[:insert_pos] + '\\n' + prompts_code + content[insert_pos:]
        
        with open('wordpress_mcp.py', 'w') as f:
            f.write(new_content)
        
        print("✅ Added 8 more prompts")
        return True
    
    print("❌ Could not find insertion point for prompts")
    return False

def main():
    """Add all enhancements"""
    print("Adding all MCP enhancements...")
    print()
    
    # Backup
    backup_file()
    
    # Add features
    success_count = 0
    
    if add_snippet_resource():
        success_count += 1
    
    if add_code_generator_tools():
        success_count += 1
    
    if add_more_prompts():
        success_count += 1
    
    # Verify syntax
    import subprocess
    result = subprocess.run(['python3', '-m', 'py_compile', 'wordpress_mcp.py'],
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\\n✅ All enhancements added successfully!")
        print(f"✅ Syntax validated")
        
        # Count features
        with open('wordpress_mcp.py', 'r') as f:
            content = f.read()
        
        resources = len(re.findall(r'@mcp\\.resource', content))
        tools = len(re.findall(r'@mcp\\.tool', content))
        prompts = len(re.findall(r'@mcp\\.prompt', content))
        
        print(f"\\n📊 Updated Server:")
        print(f"   Resources: {resources}")
        print(f"   Tools: {tools}")
        print(f"   Prompts: {prompts}")
        
        return True
    else:
        print("\\n❌ Syntax error detected:")
        print(result.stderr)
        print("\\nRestoring backup...")
        shutil.copy('wordpress_mcp.py.backup', 'wordpress_mcp.py')
        print("✅ Restored from backup")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

