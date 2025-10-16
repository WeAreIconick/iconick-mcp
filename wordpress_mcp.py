
"""
WordPress Development MCP Server - Expanded Edition

Provides comprehensive WordPress development resources including documentation,
coding standards, best practices, and code examples through the MCP protocol.
"""

from pathlib import Path
import logging

from fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = FastMCP("WordPress Development Resources")
RESOURCES_DIR = Path(__file__).parent / "resources"

def load_resource_content(category: str, topic: str) -> str:
    """Load resource content from markdown files."""
    resource_path = RESOURCES_DIR / category / f"{topic}.md"
    if not resource_path.exists():
        raise FileNotFoundError(f"Resource not found: {category}/{topic}")
    with open(resource_path, 'r', encoding='utf-8') as f:
        return f.read()

# === CORE WORDPRESS APIs ===

@mcp.resource("wordpress://core/database")
def get_database_api() -> str:
    """WordPress Database API (wpdb) - Queries, prepared statements, custom tables"""
    return load_resource_content("core", "database")
@mcp.resource("wordpress://core/http")
def get_http_api() -> str:
    """WordPress HTTP API - wp_remote_get/post, handling responses"""
    return load_resource_content("core", "http")
@mcp.resource("wordpress://core/options")
def get_options_api() -> str:
    """WordPress Options API - get_option, update_option, autoload"""
    return load_resource_content("core", "options")
@mcp.resource("wordpress://core/transients")
def get_transients_api() -> str:
    """WordPress Transients API - Caching with TTL, object cache integration"""
    return load_resource_content("core", "transients")
@mcp.resource("wordpress://core/rewrite")
def get_rewrite_api() -> str:
    """WordPress Rewrite API - Custom URLs, query vars, permalinks"""
    return load_resource_content("core", "rewrite")
@mcp.resource("wordpress://core/settings")
def get_settings_api() -> str:
    """WordPress Settings API - register_setting, settings sections"""
    return load_resource_content("core", "settings")
# === THEME DEVELOPMENT ===

@mcp.resource("wordpress://themes/template-hierarchy")
def get_template_hierarchy() -> str:
    """WordPress Template Hierarchy - Template selection, conditional tags (CRITICAL)"""
    return load_resource_content("themes", "template-hierarchy")
# === SECURITY BEST PRACTICES ===

@mcp.resource("wordpress://security/data-validation")
def get_data_validation() -> str:
    """WordPress Data Validation - Validating all input data"""
    return load_resource_content("security", "data-validation")
@mcp.resource("wordpress://security/sanitization")
def get_sanitization() -> str:
    """WordPress Data Sanitization - sanitize_text_field and more"""
    return load_resource_content("security", "sanitization")
@mcp.resource("wordpress://security/escaping")
def get_escaping() -> str:
    """WordPress Output Escaping - esc_html, esc_attr, esc_url, esc_js"""
    return load_resource_content("security", "escaping")
@mcp.resource("wordpress://security/nonces")
def get_nonces() -> str:
    """WordPress Nonces - Creating, verifying, AJAX nonces"""
    return load_resource_content("security", "nonces")
@mcp.resource("wordpress://security/capabilities")
def get_capabilities() -> str:
    """WordPress Capabilities - current_user_can, role management"""
    return load_resource_content("security", "capabilities")
@mcp.resource("wordpress://security/sql-injection")
def get_sql_injection() -> str:
    """WordPress SQL Injection Prevention - Prepared statements, $wpdb->prepare"""
    return load_resource_content("security", "sql-injection")
# === CODING STANDARDS ===

@mcp.resource("wordpress://standards/php")
def get_php_standards() -> str:
    """WordPress PHP Coding Standards - Formatting, naming conventions"""
    return load_resource_content("standards", "php")
@mcp.resource("wordpress://standards/javascript")
def get_javascript_standards() -> str:
    """WordPress JavaScript Coding Standards - ESLint configuration"""
    return load_resource_content("standards", "javascript")
# === HOOKS & FILTERS ===

@mcp.resource("wordpress://hooks/actions")
def get_action_hooks() -> str:
    """WordPress Action Hooks - Common actions with examples"""
    return load_resource_content("hooks", "actions")
# === PLUGINS ===

@mcp.resource("wordpress://plugins/structure")
def get_plugin_structure() -> str:
    """WordPress Plugin Structure - File organization, naming conventions"""
    return load_resource_content("plugins", "structure")
# === EXAMPLES ===

@mcp.resource("wordpress://examples/custom-post-types")
def get_cpt_examples() -> str:
    """WordPress Custom Post Types - Complete examples"""
    return load_resource_content("examples", "custom-post-types")
# === THEME DEVELOPMENT ===

# === BLOCK EDITOR (GUTENBERG) ===

@mcp.resource("wordpress://blocks/block-registration")
def get_block_registration() -> str:
    """WordPress Block Registration - block.json, registerBlockType, attributes"""
    return load_resource_content("blocks", "block-registration")
# === REST API ===

@mcp.resource("wordpress://rest-api/basics")
def get_rest_api_basics() -> str:
    """WordPress REST API Basics - Endpoints, authentication, responses"""
    return load_resource_content("rest-api", "basics")
# === ADDITIONAL CORE APIs ===

@mcp.resource("wordpress://core/shortcode")
def get_shortcode_api() -> str:
    """WordPress Shortcode API - Creating secure shortcodes, attributes, nested shortcodes"""
    return load_resource_content("core", "shortcode")
@mcp.resource("wordpress://core/metadata")
def get_metadata_api() -> str:
    """WordPress Metadata API - Custom fields, meta boxes, meta queries"""
    return load_resource_content("core", "metadata")
@mcp.resource("wordpress://core/filesystem")
def get_filesystem_api() -> str:
    """WordPress Filesystem API - WP_Filesystem for secure file operations"""
    return load_resource_content("core", "filesystem")
# === BLOCK EDITOR COMPONENTS ===

@mcp.resource("wordpress://blocks/components")
def get_block_components() -> str:
    """WordPress Block Editor Components - InspectorControls, BlockControls, form components"""
    return load_resource_content("blocks", "components")
# === THEME DEVELOPMENT EXPANSION ===

@mcp.resource("wordpress://themes/template-tags")
def get_template_tags() -> str:
    """WordPress Template Tags - Loop functions, post data, navigation, taxonomies"""
    return load_resource_content("themes", "template-tags")
# === ADDITIONAL BLOCK EDITOR RESOURCES ===

@mcp.resource("wordpress://blocks/dynamic-blocks")
def get_dynamic_blocks() -> str:
    """WordPress Dynamic Blocks - Server-side rendering, AJAX, caching, forms"""
    return load_resource_content("blocks", "dynamic-blocks")
@mcp.resource("wordpress://blocks/block-patterns")
def get_block_patterns() -> str:
    """WordPress Block Patterns - Pattern registration, categories, complex layouts"""
    return load_resource_content("blocks", "block-patterns")
# === ADDITIONAL REST API RESOURCES ===

@mcp.resource("wordpress://rest-api/custom-endpoints")
def get_custom_endpoints() -> str:
    """WordPress REST API Custom Endpoints - CRUD operations, permissions, schema"""
    return load_resource_content("rest-api", "custom-endpoints")
# === ADDITIONAL THEME DEVELOPMENT RESOURCES ===

@mcp.resource("wordpress://themes/theme-json")
def get_theme_json() -> str:
    """WordPress theme.json - Block theme configuration, settings, styles"""
    return load_resource_content("themes", "theme-json")
# === DEVELOPMENT TOOLS RESOURCES ===

@mcp.resource("wordpress://tools/wp-debug")
def get_wp_debug() -> str:
    """WordPress Debug System - Debug constants, logging, error handling"""
    return load_resource_content("tools", "wp-debug")
@mcp.resource("wordpress://tools/query-monitor")
def get_query_monitor() -> str:
    """Query Monitor Plugin - Database queries, hooks, performance analysis"""
    return load_resource_content("tools", "query-monitor")
@mcp.resource("wordpress://tools/wp-cli")
def get_wp_cli() -> str:
    """WordPress CLI (WP-CLI) - Command-line interface, automation, management"""
    return load_resource_content("tools", "wp-cli")

@mcp.resource("wordpress://tools/plugin-check")
def get_plugin_check() -> str:
    """WordPress Plugin Check - Complete compliance guide for WordPress.org plugin requirements"""
    return load_resource_content("tools", "plugin-check")

# === COMPLETE BLOCK EDITOR RESOURCES ===

@mcp.resource("wordpress://blocks/innerblocks")
def get_innerblocks() -> str:
    """WordPress InnerBlocks - Nested block structures, complex layouts"""
    return load_resource_content("blocks", "innerblocks")
@mcp.resource("wordpress://blocks/block-transforms")
def get_block_transforms() -> str:
    """WordPress Block Transforms - Converting between block types, migration"""
    return load_resource_content("blocks", "block-transforms")
@mcp.resource("wordpress://blocks/wordpress-packages")
def get_wordpress_packages() -> str:
    """WordPress @wordpress packages - Components, data, i18n, utilities"""
    return load_resource_content("blocks", "wordpress-packages")
# === ADDITIONAL REST API RESOURCES ===

@mcp.resource("wordpress://rest-api/authentication")
def get_rest_authentication() -> str:
    """WordPress REST API Authentication - Application passwords, OAuth, JWT, nonces"""
    return load_resource_content("rest-api", "authentication")
@mcp.resource("wordpress://rest-api/schema")
def get_rest_schema() -> str:
    """WordPress REST API Schema - Schema definition, validation, documentation"""
    return load_resource_content("rest-api", "schema")
@mcp.resource("wordpress://rest-api/extensions")
def get_rest_extensions() -> str:
    """WordPress REST API Extensions - Endpoint modifications, custom fields, bulk operations"""
    return load_resource_content("rest-api", "extensions")
# === ADDITIONAL THEME DEVELOPMENT RESOURCES ===

@mcp.resource("wordpress://themes/block-themes")
def get_block_themes() -> str:
    """WordPress Block Themes - Modern theme development with HTML templates and block patterns"""
    return load_resource_content("themes", "block-themes")
@mcp.resource("wordpress://themes/child-themes")
def get_child_themes() -> str:
    """WordPress Child Themes - Extending existing themes without losing customizations"""
    return load_resource_content("themes", "child-themes")
@mcp.resource("wordpress://themes/navigation-menus")
def get_navigation_menus() -> str:
    """WordPress Navigation Menus - Creating and customizing site navigation"""
    return load_resource_content("themes", "navigation-menus")
@mcp.resource("wordpress://themes/sidebars-widgets")
def get_sidebars_widgets() -> str:
    """WordPress Sidebars & Widgets - Creating flexible content areas and custom widgets"""
    return load_resource_content("themes", "sidebars-widgets")
@mcp.resource("wordpress://themes/post-thumbnails")
def get_post_thumbnails() -> str:
    """WordPress Post Thumbnails - Featured images, custom sizes, and optimization"""
    return load_resource_content("themes", "post-thumbnails")
# === ADDITIONAL CODING STANDARDS RESOURCES ===

@mcp.resource("wordpress://standards/css-coding-standards")
def get_css_coding_standards() -> str:
    """WordPress CSS Coding Standards - Formatting, BEM methodology, responsive design"""
    return load_resource_content("standards", "css-coding-standards")
@mcp.resource("wordpress://standards/html-coding-standards")
def get_html_coding_standards() -> str:
    """WordPress HTML Coding Standards - Semantic markup, accessibility, security"""
    return load_resource_content("standards", "html-coding-standards")
@mcp.resource("wordpress://standards/sql-best-practices")
def get_sql_best_practices() -> str:
    """WordPress SQL Best Practices - Prepared statements, security, optimization"""
    return load_resource_content("standards", "sql-best-practices")
@mcp.resource("wordpress://standards/accessibility-standards")
def get_accessibility_standards() -> str:
    """WordPress Accessibility Standards - WCAG 2.1 AA compliance, ARIA, testing"""
    return load_resource_content("standards", "accessibility-standards")
# === ADVANCED TOPICS RESOURCES ===

@mcp.resource("wordpress://advanced/multisite-development")
def get_multisite_development() -> str:
    """WordPress Multisite Development - Network management, site switching, user management"""
    return load_resource_content("advanced", "multisite-development")
@mcp.resource("wordpress://advanced/woocommerce-development")
def get_woocommerce_development() -> str:
    """WooCommerce Development - E-commerce functionality, payment gateways, product management"""
    return load_resource_content("advanced", "woocommerce-development")
@mcp.resource("wordpress://advanced/performance-optimization")
def get_performance_optimization() -> str:
    """WordPress Performance Optimization - Caching, database optimization, asset optimization"""
    return load_resource_content("advanced", "performance-optimization")
# === WORDPRESS FRAMEWORKS RESOURCES ===

@mcp.resource("wordpress://frameworks/timber-framework")
def get_timber_framework() -> str:
    """Timber Framework - Modern WordPress development with Twig templating"""
    return load_resource_content("frameworks", "timber-framework")
@mcp.resource("wordpress://frameworks/sage-framework")
def get_sage_framework() -> str:
    """Sage Framework - Modern WordPress development with Blade templating and Laravel components"""
    return load_resource_content("frameworks", "sage-framework")
@mcp.resource("wordpress://frameworks/underscores-framework")
def get_underscores_framework() -> str:
    """Underscores Framework - Official WordPress starter theme for professional theme development"""
    return load_resource_content("frameworks", "underscores-framework")
# === TESTING AND QUALITY ASSURANCE RESOURCES ===

@mcp.resource("wordpress://testing/wordpress-testing")
def get_wordpress_testing() -> str:
    """WordPress Testing - Comprehensive testing for plugins, themes, and applications"""
    return load_resource_content("testing", "wordpress-testing")
@mcp.resource("wordpress://testing/phpunit-testing")
def get_phpunit_testing() -> str:
    """PHPUnit Testing - Advanced testing techniques and best practices for WordPress"""
    return load_resource_content("testing", "phpunit-testing")
@mcp.resource("wordpress://testing/quality-assurance")
def get_quality_assurance() -> str:
    """Quality Assurance - Code quality tools, security testing, and automated workflows"""
    return load_resource_content("testing", "quality-assurance")

# === CODE SNIPPETS LIBRARY ===

@mcp.resource("wordpress://snippets/list")
def list_code_snippets() -> str:
    """Complete catalog of all 62 available code snippets"""
    snippets_dir = RESOURCES_DIR / "snippets"
    
    if not snippets_dir.exists():
        return "# Code Snippets\n\nSnippet library is being initialized."
    
    output = "# WordPress Code Snippets Library\n\n"
    output += "**62 ready-to-use code examples** for common WordPress development tasks.\n\n"
    output += "## How to Use\n\n"
    output += "Ask your AI assistant for any snippet by name. Examples:\n"
    output += '- "Show me the admin-ajax snippet"\n'
    output += '- "Get the sanitize-input code"\n'
    output += '- "Display the custom post type registration example"\n\n'
    
    total = 0
    for category_dir in sorted(snippets_dir.iterdir()):
        if category_dir.is_dir():
            category = category_dir.name
            snippets = sorted([f.stem for f in category_dir.glob("*.md")])
            total += len(snippets)
            
            if snippets:
                output += f"## {category.replace('-', ' ').title()} ({len(snippets)} snippets)\n\n"
                for snippet in snippets:
                    # Get first line as description
                    try:
                        with open(category_dir / f"{snippet}.md", 'r', encoding='utf-8') as f:
                            first_line = f.readline().strip()
                            title = first_line.replace('#', '').strip() if first_line.startswith('#') else snippet
                    except:
                        title = snippet.replace('-', ' ').title()
                    
                    output += f"- **{snippet}** - {title}\n"
                
                output += "\n"
    
    output += f"---\n\n**Total: {total} code snippets**\n\n"
    output += "All snippets include:\n"
    output += "- Complete working code examples\n"
    output += "- Security best practices\n"
    output += "- WordPress coding standards\n"
    output += "- Copy-paste ready implementations\n"
    
    return output

@mcp.resource("wordpress://snippets/{category}/{topic}")
def get_code_snippet(category: str, topic: str) -> str:
    """
    Get specific WordPress code snippet
    
    Examples:
      wordpress://snippets/security/sanitize-input
      wordpress://snippets/ajax/admin-ajax
      wordpress://snippets/cpt/register-custom-post-type
      wordpress://snippets/hooks/save-post-hook
      wordpress://snippets/performance/caching-transients
    
    Use wordpress://snippets/list to see all available snippets
    """
    try:
        if not category or not topic:
            return "Error: Both category and topic are required.\n\nFormat: wordpress://snippets/{category}/{topic}\n\nUse wordpress://snippets/list to see available snippets."
        
        # Load the snippet using the existing function
        snippet_path = f"snippets/{category}"
        return load_resource_content(snippet_path, topic)
        
    except FileNotFoundError:
        # List available snippets in this category
        try:
            category_path = RESOURCES_DIR / "snippets" / category
            if category_path.exists():
                available = sorted([f.stem for f in category_path.glob("*.md")])
                error_msg = f"Snippet not found: {category}/{topic}\n\n"
                error_msg += f"Available in '{category}':\n"
                for snippet in available:
                    error_msg += f"- {snippet}\n"
                return error_msg
            else:
                return f"Category not found: {category}\n\nUse wordpress://snippets/list to see all categories."
        except:
            return "Error loading snippet. Use wordpress://snippets/list to see available snippets."
    except Exception as e:
        return f"Error: {str(e)}\n\nUse wordpress://snippets/list to see all available snippets."

# === RESOURCE CATALOG & DISCOVERY ===

@mcp.resource("wordpress://catalog")
def get_resource_catalog() -> str:
    """Complete searchable catalog of all WordPress resources with metadata, tags, and learning paths"""
    return load_resource_content(".", "catalog")

@mcp.tool()
def search_resources(
    query: str = "",
    difficulty: str = "",
    tag: str = "",
    category: str = ""
) -> str:
    """
    Search and filter WordPress development resources
    
    Args:
        query: Search term (searches titles and tags)
        difficulty: Filter by difficulty (Beginner, Intermediate, Advanced)
        tag: Filter by tag (e.g., "security", "blocks", "api")
        category: Filter by category (e.g., "security", "blocks", "themes")
    
    Returns:
        List of matching resources with metadata
        
    Examples:
        search_resources(query="security")
        search_resources(difficulty="Beginner")
        search_resources(tag="blocks", difficulty="Intermediate")
        search_resources(category="security")
    """
    import re
    from pathlib import Path
    
    results = []
    resources_dir = RESOURCES_DIR
    
    # Scan all resource files (excluding snippets)
    for md_file in resources_dir.glob("**/*.md"):
        if "snippets" in str(md_file) or md_file.name == "catalog.md":
            continue
        
        relative_path = md_file.relative_to(resources_dir)
        file_category = relative_path.parts[0] if len(relative_path.parts) > 1 else "other"
        
        # Read file
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        # Extract metadata
        resource_data = {
            'name': md_file.stem,
            'category': file_category,
            'path': str(relative_path),
            'difficulty': 'Intermediate',
            'tags': [],
            'related': []
        }
        
        # Parse frontmatter if exists
        if content.startswith('---'):
            match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
            if match:
                metadata_str = match.group(1)
                
                # Extract difficulty
                diff_match = re.search(r'difficulty:\s*(\w+)', metadata_str)
                if diff_match:
                    resource_data['difficulty'] = diff_match.group(1)
                
                # Extract tags
                tags_match = re.search(r'tags:\s*\[(.*?)\]', metadata_str)
                if tags_match:
                    resource_data['tags'] = [t.strip() for t in tags_match.group(1).split(',')]
                
                # Extract related
                related_match = re.search(r'related:\s*\[(.*?)\]', metadata_str)
                if related_match:
                    resource_data['related'] = [r.strip() for r in related_match.group(1).split(',')]
        
        # Apply filters
        if difficulty and resource_data['difficulty'] != difficulty:
            continue
        
        if tag and tag not in resource_data['tags']:
            continue
        
        if category and file_category != category:
            continue
        
        if query:
            query_lower = query.lower()
            if (query_lower not in resource_data['name'].lower() and
                query_lower not in file_category.lower() and
                not any(query_lower in t.lower() for t in resource_data['tags'])):
                continue
        
        results.append(resource_data)
    
    # Format results
    if not results:
        return f"""# No Resources Found

**Search criteria:**
- Query: {query or 'all'}
- Difficulty: {difficulty or 'all'}
- Tag: {tag or 'all'}
- Category: {category or 'all'}

Try broader search terms or check `wordpress://catalog` for complete resource list.
"""
    
    output = f"# WordPress Resources Search Results\n\n"
    output += f"**Found {len(results)} resource(s)**\n\n"
    
    if query:
        output += f"**Query:** {query}\n"
    if difficulty:
        output += f"**Difficulty:** {difficulty}\n"
    if tag:
        output += f"**Tag:** {tag}\n"
    if category:
        output += f"**Category:** {category}\n"
    
    output += "\n---\n\n"
    
    # Group by category
    by_category = {}
    for res in results:
        cat = res['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(res)
    
    for cat in sorted(by_category.keys()):
        resources = by_category[cat]
        output += f"## {cat.title()} ({len(resources)})\n\n"
        
        for res in sorted(resources, key=lambda x: x['name']):
            output += f"### {res['name']}\n\n"
            output += f"**Difficulty:** {res['difficulty']}\n\n"
            
            if res['tags']:
                output += f"**Tags:** {', '.join(res['tags'])}\n\n"
            
            output += f"**Resource:** `wordpress://{cat}/{res['name']}`\n\n"
            
            if res['related']:
                output += f"**Related:** {', '.join(res['related'][:3])}\n\n"
            
            output += "---\n\n"
    
    output += f"\n💡 **Tip:** Use `wordpress://catalog` to browse all {len(results)} resources by category, difficulty, and tags.\n"
    
    return output

# === MCP PROMPTS ===

@mcp.prompt()
def plugin_development_workflow():
    """Complete WordPress plugin development workflow with best practices"""
    return """I'm developing a WordPress plugin. Guide me through the complete development workflow:

## Phase 1: Planning & Structure
Help me with:
1. **Plugin structure and file organization**
   - What files are required?
   - How should I organize my code?
   - Best practices for namespacing

2. **Plugin header requirements**
   - All required header fields
   - Validation rules for each field
   - License requirements

Ask me about:
- What is your plugin's purpose and main functionality?
- Will it need database tables?
- Does it require admin pages or settings?
- Will it interact with the REST API?

## Phase 2: Security Implementation
Check and guide me on:
1. **Input validation** - Are all inputs validated?
2. **Data sanitization** - Is all data sanitized before saving?
3. **Output escaping** - Is all output properly escaped?
4. **Nonces** - Are all forms and AJAX requests using nonces?
5. **Capability checks** - Are user permissions checked?
6. **SQL injection prevention** - Are prepared statements used?

For each security item:
- Show me examples of correct implementation
- Explain common vulnerabilities
- Provide code snippets I can use

## Phase 3: Code Quality
Review for:
1. **WordPress Coding Standards** - Does my code follow PHP standards?
2. **Internationalization** - Is my plugin translation-ready?
3. **Performance** - Are queries optimized?
4. **Documentation** - Are functions properly documented?

## Phase 4: Pre-Submission Checklist
Before submitting to WordPress.org:
1. Run through Plugin Check requirements
2. Verify readme.txt format
3. Check for trademark violations
4. Remove development files
5. Test with WP_DEBUG enabled

For each step:
- Provide best practices
- Show code examples
- Highlight common pitfalls
- Link to relevant resources from the server

Let's start with Phase 1. Please describe your plugin idea.
"""

@mcp.prompt()
def security_audit():
    """Comprehensive WordPress security audit workflow"""
    return """I need to perform a security audit on WordPress code. Let's systematically check for all common vulnerabilities:

## Critical Security Checks

### 1. Input Validation
Analyze all code that accepts user input:
- Are $_GET, $_POST, $_REQUEST values validated?
- Are file uploads checked for type and size?
- Are URL parameters validated?

For each issue found, I'll show:
- Vulnerable code
- Secure fix
- WordPress documentation reference

### 2. Output Escaping
Check every instance of output:
- Are variables properly escaped with esc_html(), esc_attr(), esc_url()?
- Is HTML output using wp_kses() or wp_kses_post()?
- Are JavaScript strings escaped with esc_js()?

### 3. SQL Injection
Review all database queries:
- Are $wpdb->prepare() statements used?
- Are direct SQL queries avoided?
- Are dynamic table/column names properly validated?

### 4. CSRF Protection (Nonces)
Verify all state-changing operations:
- Are forms using wp_nonce_field()?
- Are AJAX requests using wp_create_nonce() and check_ajax_referer()?
- Are URL actions using wp_nonce_url() and wp_verify_nonce()?

### 5. Authentication & Authorization
Check permission checks:
- Is current_user_can() used before sensitive operations?
- Are capability checks appropriate for the action?
- Is is_admin() misused for security? (Not a security check!)

### 6. File Upload Security
If handling uploads:
- Are file types whitelisted?
- Is file size limited?
- Is ALLOW_UNFILTERED_UPLOADS avoided?

### 7. API Security
If using REST API:
- Are authentication methods implemented?
- Are permission callbacks defined?
- Is input validated in the schema?

### 8. XSS Prevention
Check for Cross-Site Scripting vectors:
- User-generated content display
- Reflected input in error messages
- Admin page output

Ready to start? Share the code you want me to audit.
"""

@mcp.prompt()
def performance_optimization():
    """WordPress performance analysis and optimization workflow"""
    return """Let's optimize your WordPress site/plugin/theme for maximum performance:

## Performance Analysis Areas

### 1. Database Optimization
- Query efficiency with WP_Query parameters
- Avoiding posts_per_page => -1
- Using fields => 'ids' when appropriate
- N+1 query problems
- Database indexes

### 2. Asset Optimization  
- Proper script/style enqueuing
- Loading scripts in footer
- Using defer/async attributes
- Minification and size limits
- Conditional loading

### 3. Caching Strategy
- Transients for expensive operations
- Object caching
- Page caching considerations

### 4. Code Optimization
- Autoloading classes
- Conditional loading
- Hook priority optimization

### 5. External Requests
- Caching remote requests
- Timeout configuration
- Error handling

Describe your performance issue or share code to analyze!
"""

@mcp.prompt()
def plugin_check_preparation():
    """Prepare WordPress plugin for WordPress.org submission"""
    return """Let's prepare your plugin for WordPress.org submission and ensure it passes all Plugin Check requirements:

## Complete Preparation Workflow

### Phase 1: Required Files & Headers
- Plugin header with all required fields
- readme.txt with proper structure
- Valid GPL-compatible license

### Phase 2: Security Audit
- Input validation checklist
- Output escaping verification
- Nonce usage check
- Capability checks
- SQL injection prevention

### Phase 3: Code Quality
- WordPress Coding Standards
- Internationalization
- File checks
- No deprecated functions

### Phase 4: Required Functionality
- Uninstall cleanup
- Proper script/style enqueuing

### Phase 5: Trademark Check
- Plugin slug validation
- Name compliance

### Phase 6: Testing
- Run Plugin Check tool
- WP_DEBUG testing

### Phase 7: Pre-Submission Checklist
- Complete checklist with all requirements

Share your plugin and I'll review it against all requirements!
"""

@mcp.prompt()
def theme_development_guide():
    """Complete WordPress theme development workflow"""
    return """Let's build a professional WordPress theme together:

## Theme Development Workflow

### Phase 1: Theme Type Decision
- Block Theme (Modern - Full Site Editing)
- Classic Theme (Traditional PHP templates)

### Phase 2: Required Files & Structure
- style.css with proper header
- Required template files
- functions.php setup

### Phase 3: Essential Theme Features
- Theme supports
- Navigation menus
- Widget areas
- Custom post type support

### Phase 4: Template Development
- Template hierarchy
- WordPress template tags
- Security (output escaping)
- Performance optimization

### Phase 5: Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation
- ARIA labels
- Color contrast

### Phase 6: Performance
- Optimized asset loading
- Efficient queries
- Responsive images

### Phase 7: Testing
- Theme Check plugin
- Multiple content types
- Responsive testing
- Browser compatibility

Tell me which type of theme you want to build and I'll guide you through it!
"""

@mcp.prompt()
def woocommerce_development():
    """WooCommerce development and customization workflow"""
    return """I'm developing a WooCommerce extension or customization. Let's work through it:

## What Are You Building?

1. **Payment Gateway** - Custom payment processor integration
2. **Shipping Method** - Custom shipping calculation logic
3. **Product Type** - New product variations (subscriptions, rentals, etc.)
4. **Custom Product Fields** - Additional product data and options
5. **Checkout Customization** - Custom checkout fields and validation
6. **Order Management** - Custom order statuses and workflows
7. **Email Templates** - Custom transactional emails
8. **Third-Party Integration** - Connect with external services

## I'll Help You With:

### Phase 1: WooCommerce Hooks & Filters
- Product hooks (pricing, add to cart, display)
- Cart & checkout hooks (fields, validation, processing)
- Order hooks (status changes, emails, meta data)
- Admin hooks (product panels, order details)
- Email hooks (content, recipients, triggers)

### Phase 2: Security & Data Handling
- Payment data security (PCI considerations)
- Order data sanitization and validation
- Customer data protection
- WooCommerce-specific nonces and capabilities

### Phase 3: Testing Requirements
- Test with different product types (simple, variable, grouped)
- Test complete checkout flow
- Test with various payment methods
- Test order status transitions
- Test refunds and cancellations
- Test with different shipping zones

### Phase 4: WooCommerce Standards
- Follow WooCommerce coding standards
- Use WooCommerce template structure
- Proper action/filter priorities
- Translation-ready with WooCommerce text domains

Tell me what you're building and I'll provide complete WooCommerce-specific code!
"""

@mcp.prompt()
def gutenberg_block_development():
    """Modern Gutenberg block development with React"""
    return """Let's build a professional Gutenberg block with React!

## Tell Me About Your Block

1. What does your block do?
2. Does it need:
   - **Inspector controls** (sidebar settings panel)?
   - **Toolbar controls** (formatting options)?
   - **InnerBlocks** (nest other blocks inside)?
   - **Dynamic rendering** (server-side PHP)?
   - **Custom attributes** (what data to store)?

## Modern Block Development Setup

### Option A: Quick Start with @wordpress/create-block

```bash
npx @wordpress/create-block@latest my-custom-block
cd my-custom-block
npm start
```

### Option B: Manual Setup (Full Control)

I'll help you create:
- `block.json` - Block configuration
- `index.js` - Block registration
- `edit.js` - React edit component with hooks
- `save.js` - Frontend save function
- `style.scss` - Frontend styles
- `editor.scss` - Editor-only styles
- `package.json` - Build configuration
- `webpack.config.js` - Custom build setup

## Modern React Patterns I'll Show You

- `useBlockProps()` - Block wrapper props
- `InspectorControls` - Settings sidebar
- `BlockControls` - Toolbar controls
- `RichText` - Editable text
- `MediaUpload` - Image selection
- `ColorPalette` - Color picker
- `@wordpress/data` - State management
- `useSelect` and `useDispatch` - Data hooks

## Advanced Features

- Block variations (different starting states)
- Block patterns (reusable layouts)
- Block transforms (convert between types)
- Dynamic blocks (server-side rendering)
- Parent/child block relationships
- Block templates (predefined structures)

Describe your block idea and I'll generate complete React code with all the modern patterns!
"""

@mcp.prompt()
def rest_api_development():
    """Complete WordPress REST API development workflow"""
    return """Let's build a comprehensive WordPress REST API!

## API Design Phase

### Tell Me About Your API:

1. **What resources?** (posts, products, users, custom data, etc.)
2. **What operations?**
   - GET (read/list)
   - POST (create)
   - PUT/PATCH (update)
   - DELETE (remove)
3. **Who can access?** (public, authenticated, specific roles)
4. **What data format?** (JSON schema, response structure)

## I'll Help You Build:

### Complete REST Endpoints

```php
// Namespace: myplugin/v1
// Endpoints:
//   GET  /items
//   GET  /items/{id}
//   POST /items
//   PUT  /items/{id}
//   DELETE /items/{id}
```

### Security Implementation
- Authentication methods (Application Passwords, OAuth, JWT, custom)
- Permission callbacks for each endpoint
- Input validation and sanitization
- Rate limiting considerations
- CORS configuration if needed

### Schema Definition
- Request parameter schemas
- Response data structures
- Error response formats
- Validation rules
- Type definitions

### Documentation
- OpenAPI/Swagger spec
- Example requests with cURL
- Example responses
- Error codes and messages
- Authentication examples

### Advanced Features
- Pagination and filtering
- Embedding related data
- Custom fields in responses
- Batch operations
- Webhooks integration

Tell me what data you need to expose and I'll provide complete REST API code with security, validation, and best practices!
"""

@mcp.prompt()
def multisite_development():
    """WordPress Multisite development and network management"""
    return """Working with WordPress Multisite - let's build it right!

## What Are You Building?

1. **Network Plugin** - Works across all sites
2. **Network Admin Feature** - Super admin tools
3. **Cross-Site Functionality** - Share data between sites
4. **Site-Specific Feature** - Different per site
5. **Network Theme** - Theme for all sites

## Multisite Concepts I'll Explain:

### Network vs Site
- Global tables (users, usermeta) vs site tables (posts, options)
- Network activation vs site activation
- Super Admin vs Site Admin capabilities
- Network-wide settings vs site-specific settings

### Essential Functions
- `switch_to_blog()` / `restore_current_blog()` - Site switching
- `get_sites()` - List all sites
- `get_current_blog_id()` - Current site ID
- `is_main_site()` - Check if main site
- `get_site_option()` / `update_site_option()` - Network options

### Common Patterns

**Network Admin Pages:**
```php
add_action( 'network_admin_menu', 'add_network_page' );
```

**Cross-Site Queries:**
```php
$sites = get_sites();
foreach ( $sites as $site ) {
    switch_to_blog( $site->blog_id );
    // Do something
    restore_current_blog();
}
```

**Network-Wide Settings:**
```php
update_site_option( 'network_setting', $value );
```

### Security Considerations
- Use `manage_network_options` capability
- Validate blog IDs before switching
- Isolate site data properly
- Escape cross-site data

What multisite feature do you need? I'll provide complete working code!
"""

@mcp.prompt()
def database_optimization():
    """WordPress database performance optimization and troubleshooting"""
    return """Let's optimize your WordPress database for better performance!

## What's Your Issue?

1. **Slow Queries** - Pages taking too long to load
2. **High Database Load** - Too many queries
3. **Large Database** - Database growing too large
4. **N+1 Query Problems** - Queries in loops
5. **Missing Indexes** - Slow searches
6. **Transient Buildup** - Old transients not cleaned

## Diagnostic Tools We'll Use:

- **Query Monitor** - See all database queries
- **EXPLAIN** - Analyze query execution
- **wp_queries** - Count queries per page
- **Transient Manager** - View cached data
- **Debug Bar** - Performance profiling

## I'll Help You:

### Optimize Slow Queries
- Analyze with EXPLAIN
- Add proper indexes
- Rewrite inefficient queries
- Use WordPress functions when available

### Reduce Query Count
- Fix N+1 problems
- Batch operations
- Pre-fetch related data
- Use transients for expensive queries

### Clean Up Database
- Remove post revisions
- Delete spam comments
- Clean expired transients
- Optimize tables
- Remove orphaned meta

### Add Indexes
```sql
ALTER TABLE wp_postmeta ADD INDEX meta_key_value (meta_key, meta_value(10));
```

Share your slow queries or describe your performance issue and I'll provide specific optimizations!
"""

@mcp.prompt()
def accessibility_compliance():
    """WCAG 2.1 Level AA accessibility compliance guide"""
    return """Let's make your WordPress site fully accessible (WCAG 2.1 Level AA)!

## What Are You Making Accessible?

1. **Theme** - Complete theme accessibility
2. **Plugin** - Accessible plugin features
3. **Custom Block** - Accessible Gutenberg block
4. **Admin Interface** - Accessible admin pages
5. **Specific Feature** - Forms, navigation, etc.

## WCAG 2.1 Level AA Requirements:

### 1. Perceivable
- **Text Alternatives**: Alt text for all images
- **Captions**: Video/audio captions
- **Adaptable**: Proper heading hierarchy (H1, H2, H3)
- **Distinguishable**: 4.5:1 color contrast ratio minimum

### 2. Operable
- **Keyboard Accessible**: All functionality via keyboard
- **No Keyboard Traps**: Can navigate away from everything
- **Skip Links**: Jump to main content
- **Focus Indicators**: Visible focus states
- **Timing**: No time limits or adjustable

### 3. Understandable
- **Clear Labels**: Form fields properly labeled
- **Error Identification**: Clear error messages
- **Consistent Navigation**: Same navigation everywhere
- **Predictable**: Consistent behavior

### 4. Robust
- **Valid HTML**: Proper semantic markup
- **ARIA Attributes**: When needed for complex widgets
- **Screen Reader Compatible**: Works with assistive tech

## I'll Audit Your Code For:

- Missing alt attributes
- Insufficient color contrast
- Missing form labels
- Keyboard navigation issues
- Invalid HTML structure
- Missing ARIA attributes
- Focus management problems
- Screen reader compatibility

## Testing Tools I'll Recommend:

- WAVE browser extension
- axe DevTools
- Lighthouse accessibility audit
- Keyboard-only navigation test
- Screen reader testing (NVDA, JAWS, VoiceOver)

Share your code or describe what you're building and I'll make it fully accessible!
"""

@mcp.prompt()
def deployment_workflow():
    """WordPress deployment, DevOps, and CI/CD workflow"""
    return """Let's set up a professional WordPress deployment pipeline!

## Current Setup?

1. **Manual deployment** - FTP uploads
2. **Basic Git** - Git push but manual steps
3. **Partial automation** - Some scripts
4. **No automation** - Starting from scratch

## I'll Help You Build:

### Three-Environment Strategy
- **Development** (local) - WP_DEBUG enabled, test data
- **Staging** (server) - Production mirror, testing
- **Production** (live) - Optimized, monitored

### Git Workflow
```bash
main (production)
  ├── develop (staging)
  │    ├── feature/new-feature
  │    └── bugfix/fix-issue
  └── hotfix/critical-fix
```

### CI/CD Pipeline (GitHub Actions Example)
```yaml
# Automated:
- Run PHPUnit tests
- Run PHPCS (coding standards)
- Run ESLint (JavaScript)
- Build assets (compile SCSS, minify JS)
- Deploy to staging on develop branch
- Deploy to production on main branch merge
```

### Deployment Automation
- Database migrations (safe schema changes)
- Search-replace URLs
- Clear caches
- Flush permalinks
- Asset compilation
- Dependency installation (Composer, npm)

### Rollback Strategy
- Database backups before deployment
- Code backups (Git tags)
- Quick rollback procedures
- Health checks after deployment

### Environment Configuration
```php
// Different settings per environment
if ( WP_ENVIRONMENT_TYPE === 'development' ) {
    // Dev settings
} elseif ( WP_ENVIRONMENT_TYPE === 'staging' ) {
    // Staging settings  
} else {
    // Production settings
}
```

Tell me your current deployment process and I'll create an automated pipeline for you!
"""

@mcp.prompt()
def troubleshooting_guide():
    """WordPress debugging, error diagnosis, and troubleshooting"""
    return """Let's debug your WordPress issue! Tell me what's happening:

## Common WordPress Issues:

### 1. White Screen of Death (WSOD)
**Symptoms:** Blank white screen, no error message
**Diagnosis:**
- Enable WP_DEBUG in wp-config.php
- Check error logs
- Check .htaccess file
- Disable plugins/theme

### 2. Error Establishing Database Connection
**Symptoms:** Can't connect to database
**Check:**
- Database credentials in wp-config.php
- Database server is running
- Database name is correct
- User has proper permissions

### 3. 500 Internal Server Error
**Symptoms:** Generic 500 error
**Check:**
- PHP error logs
- .htaccess syntax
- PHP memory limit
- File permissions

### 4. Plugin Conflicts
**Symptoms:** Site breaks after plugin activation
**Solution:**
- Deactivate all plugins
- Reactivate one by one
- Find conflicting plugin
- Check for JavaScript errors

### 5. Theme Issues
**Symptoms:** Layout broken, features not working
**Check:**
- Switch to default theme
- Check theme errors
- Review template files
- Check for theme updates

### 6. Performance Problems
**Symptoms:** Slow page loads
**Diagnose:**
- Use Query Monitor
- Check slow queries
- Review plugin overhead
- Analyze page size

## Debugging Tools I'll Recommend:

**Enable Debug Mode:**
```php
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
define( 'SCRIPT_DEBUG', true );
define( 'SAVEQUERIES', true );
```

**Essential Plugins:**
- Query Monitor (performance analysis)
- Debug Bar (general debugging)
- Log Deprecated Notices (code quality)

**Browser Tools:**
- Console (JavaScript errors)
- Network tab (HTTP requests)
- Elements inspector (DOM issues)

## Systematic Debugging Process:

1. **Reproduce** the issue reliably
2. **Enable debugging** (WP_DEBUG)
3. **Check logs** (debug.log, error_log)
4. **Isolate** (disable plugins/theme)
5. **Test** each component
6. **Fix** the root cause
7. **Verify** the solution

Tell me what error or issue you're seeing and I'll help you diagnose and fix it!
"""

@mcp.prompt()
def migration_workflow():
    """WordPress site migration complete guide"""
    return """Let's migrate your WordPress site safely and efficiently!

## Migration Details

**From:** Where are you migrating from?
**To:** Where are you migrating to?
**Type:** Local to live? Hosting to hosting? Development to production?

## Complete Migration Checklist:

### Phase 1: Pre-Migration (CRITICAL)
- [ ] **Full backup** of source site (database + files)
- [ ] **Test backup** restore locally
- [ ] **Document** active plugins and themes
- [ ] **Check** PHP/MySQL version compatibility
- [ ] **List** custom code and configurations
- [ ] **Screenshot** current site (for reference)

### Phase 2: Prepare Target Environment
- [ ] Install WordPress (same or newer version)
- [ ] Configure wp-config.php (database credentials)
- [ ] Set correct file permissions (755 directories, 644 files)
- [ ] Test database connection
- [ ] Verify PHP extensions

### Phase 3: Migration Process

**Database Migration:**
```bash
# Export from source
wp db export source-backup.sql

# Import to target
wp db import source-backup.sql

# Search-replace URLs
wp search-replace 'oldsite.com' 'newsite.com' --dry-run
wp search-replace 'oldsite.com' 'newsite.com'

# Search-replace paths if needed
wp search-replace '/old/path' '/new/path'
```

**File Migration:**
- Copy wp-content/uploads (media files)
- Copy wp-content/themes (custom themes)
- Copy wp-content/plugins (if not using managed plugins)
- DON'T copy wp-config.php (create new)

### Phase 4: Post-Migration Tasks
- [ ] **Flush permalinks** (Settings > Permalinks > Save)
- [ ] **Regenerate thumbnails** if needed
- [ ] **Test all forms** (contact, search, etc.)
- [ ] **Verify media files** are accessible
- [ ] **Check SSL/HTTPS** configuration
- [ ] **Test email** sending
- [ ] **Update DNS** when ready
- [ ] **Test on mobile** devices

### Phase 5: Verification
- [ ] All pages load correctly
- [ ] All plugins activated and working
- [ ] Theme displays properly
- [ ] Forms submit successfully
- [ ] Media displays correctly
- [ ] Search works
- [ ] Comments work (if enabled)
- [ ] User login works

## I'll Generate For You:

- WP-CLI migration script
- Manual migration checklist
- Troubleshooting guide for common issues
- Rollback procedures

Tell me about your migration and I'll create a custom migration plan!
"""

@mcp.prompt()
def security_hardening():
    """WordPress security hardening and best practices"""
    return """Let's harden your WordPress site security!

## Current Security Assessment

What's your current security setup?
1. WordPress version up to date?
2. Security plugins installed?
3. SSL/HTTPS configured?
4. File permissions set correctly?
5. Admin username changed from 'admin'?

## Complete Security Hardening:

### Layer 1: File System Security
- Proper file permissions (755/644)
- Disable file editing in admin
- Remove default WordPress files (readme.html, license.txt)
- Secure wp-config.php (move outside public_html)
- Add .htaccess security rules

### Layer 2: Authentication Security
- Limit login attempts
- Two-factor authentication (2FA)
- Strong password enforcement
- Change admin username
- Hide login page URL
- Application passwords for API access

### Layer 3: Database Security
- Change database table prefix from 'wp_'
- Secure database credentials
- Regular database backups
- Limit database user privileges
- Use SSL for database connections

### Layer 4: WordPress Configuration
```php
// Disable file editing
define( 'DISALLOW_FILE_EDIT', true );

// Force SSL admin
define( 'FORCE_SSL_ADMIN', true );

// Security keys (generate unique)
// https://api.wordpress.org/secret-key/1.1/salt/

// Disable XML-RPC if not needed
add_filter( 'xmlrpc_enabled', '__return_false' );

// Disable REST API for non-authenticated
add_filter( 'rest_authentication_errors', function( $result ) {
    if ( ! is_user_logged_in() ) {
        return new WP_Error( 'rest_disabled', 'REST API disabled', array( 'status' => 401 ) );
    }
    return $result;
});
```

### Layer 5: Monitoring & Response
- Security scanning (Wordfence, Sucuri)
- Activity logging
- Uptime monitoring
- File integrity monitoring
- Malware scanning

### Layer 6: Updates & Maintenance
- Auto-update WordPress core
- Auto-update plugins (carefully)
- Remove inactive plugins
- Keep themes updated
- Regular security audits

I'll provide specific hardening steps for your site. What's your current security concern?
"""

# === MCP TOOLS IMPLEMENTATION ===

@mcp.tool()
def wordpress_installer(target_dir: str, version: str = "latest", site_url: str = "http://localhost", 
                       site_title: str = "My WordPress Site", admin_user: str = "admin", 
                       admin_pass: str = "admin", admin_email: str = "admin@example.com",
                       db_host: str = "localhost", db_name: str = "wordpress", 
                       db_user: str = "root", db_pass: str = "", plugins: list = None, 
                       themes: list = None) -> str:
    """Install WordPress with custom configuration and optional plugins/themes"""
    import subprocess
    import sys
    
    try:
        # Run the WordPress installer tool
        cmd = [
            sys.executable, "tools/wordpress_installer.py", target_dir,
            "--version", version,
            "--site-url", site_url,
            "--site-title", site_title,
            "--admin-user", admin_user,
            "--admin-pass", admin_pass,
            "--admin-email", admin_email,
            "--db-host", db_host,
            "--db-name", db_name,
            "--db-user", db_user,
            "--db-pass", db_pass
        ]
        
        if plugins:
            cmd.extend(["--plugins"] + plugins)
        if themes:
            cmd.extend(["--themes"] + themes)
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            return f"WordPress installed successfully in {target_dir}\nOutput: {result.stdout}"
        else:
            return f"WordPress installation failed: {result.stderr}"
            
    except Exception as e:
        return f"Error running WordPress installer: {str(e)}"

@mcp.tool()
def plugin_manager(wp_path: str, action: str, plugin: str = None, plugins: list = None, 
                  activate: bool = False, status: str = "all", limit: int = 10, 
                  query: str = None) -> str:
    """Manage WordPress plugins - install, activate, deactivate, search, list"""
    import subprocess
    import sys
    
    try:
        cmd = [sys.executable, "tools/plugin_manager.py", "--wp-path", wp_path, action]
        
        if action == "list":
            cmd.extend(["--status", status])
        elif action == "search":
            if not query:
                return "Search query is required for search action"
            cmd.extend([query, "--limit", str(limit)])
        elif action in ["install", "activate", "deactivate", "uninstall", "update"]:
            if plugin:
                cmd.append(plugin)
                if action == "install" and activate:
                    cmd.append("--activate")
            elif plugins:
                cmd.extend(plugins)
                if action == "install" and activate:
                    cmd.append("--activate")
            else:
                return f"Plugin name or list is required for {action} action"
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            return f"Plugin management completed successfully\nOutput: {result.stdout}"
        else:
            return f"Plugin management failed: {result.stderr}"
            
    except Exception as e:
        return f"Error running plugin manager: {str(e)}"

@mcp.tool()
def theme_customizer(wp_path: str, action: str, theme: str = None, themes: list = None,
                    parent: str = None, child_name: str = None, child_slug: str = None,
                    status: str = "all", limit: int = 10, query: str = None,
                    mod_key: str = None, mod_value: str = None, content: str = None,
                    output: str = None) -> str:
    """Manage WordPress themes - install, activate, create child themes, customize"""
    import subprocess
    import sys
    
    try:
        cmd = [sys.executable, "tools/theme_customizer.py", "--wp-path", wp_path, action]
        
        if action == "list":
            cmd.extend(["--status", status])
        elif action == "search":
            if not query:
                return "Search query is required for search action"
            cmd.extend([query, "--limit", str(limit)])
        elif action in ["install", "activate", "delete", "update"]:
            if theme:
                cmd.append(theme)
            elif themes:
                cmd.extend(themes)
            else:
                return f"Theme name or list is required for {action} action"
        elif action == "child":
            if not parent or not child_name:
                return "Parent theme and child name are required for child theme creation"
            cmd.extend([parent, child_name])
            if child_slug:
                cmd.extend(["--slug", child_slug])
        elif action == "mod":
            if mod_key and mod_value:
                cmd.extend(["set", mod_key, mod_value])
            elif mod_key:
                cmd.extend(["get", mod_key])
            else:
                cmd.append("list")
        elif action == "css":
            if not content:
                return "CSS content is required for css action"
            cmd.append(content)
            if output:
                cmd.extend(["--output", output])
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            return f"Theme management completed successfully\nOutput: {result.stdout}"
        else:
            return f"Theme management failed: {result.stderr}"
            
    except Exception as e:
        return f"Error running theme customizer: {str(e)}"

@mcp.tool()
def database_manager(wp_path: str, action: str, table: str = None, output: str = None,
                    backup: str = None, compress: bool = False, search: str = None,
                    replace: str = None, execute: bool = False, sql: str = None) -> str:
    """Manage WordPress database - backup, restore, optimize, query, search-replace"""
    import subprocess
    import sys
    
    try:
        cmd = [sys.executable, "tools/database_manager.py", "--wp-path", wp_path, action]
        
        if action == "table-info":
            if not table:
                return "Table name is required for table-info action"
            cmd.append(table)
        elif action == "backup":
            if not output:
                return "Output file path is required for backup action"
            cmd.append(output)
            if compress:
                cmd.append("--compress")
        elif action == "restore":
            if not backup:
                return "Backup file path is required for restore action"
            cmd.append(backup)
        elif action == "search-replace":
            if not search or not replace:
                return "Search and replace strings are required for search-replace action"
            cmd.extend([search, replace])
            if execute:
                cmd.append("--execute")
        elif action == "query":
            if not sql:
                return "SQL query is required for query action"
            cmd.append(sql)
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            return f"Database management completed successfully\nOutput: {result.stdout}"
        else:
            return f"Database management failed: {result.stderr}"
            
    except Exception as e:
        return f"Error running database manager: {str(e)}"

@mcp.tool()
def backup_tool(wp_path: str, action: str, output: str = None, backup: str = None,
               target: str = None, directory: str = None, compress: bool = False) -> str:
    """Manage WordPress backups - create, restore, list, verify backups"""
    import subprocess
    import sys
    
    try:
        cmd = [sys.executable, "tools/backup_tool.py", "--wp-path", wp_path, action]
        
        if action == "backup":
            if not output:
                return "Output file path is required for backup action"
            cmd.append(output)
            if compress:
                cmd.append("--compress")
        elif action == "restore":
            if not backup:
                return "Backup file path is required for restore action"
            cmd.append(backup)
            if target:
                cmd.extend(["--target", target])
        elif action == "list":
            if not directory:
                return "Directory path is required for list action"
            cmd.append(directory)
        elif action == "verify":
            if not backup:
                return "Backup file path is required for verify action"
            cmd.append(backup)
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            return f"Backup operation completed successfully\nOutput: {result.stdout}"
        else:
            return f"Backup operation failed: {result.stderr}"
            
    except Exception as e:
        return f"Error running backup tool: {str(e)}"

# === WORDPRESS HOSTING AND DEPLOYMENT ===

@mcp.resource("wordpress://hosting/wordpress-hosting-providers")
def get_wordpress_hosting_providers() -> str:
    """WordPress Hosting Providers - Comprehensive guide to hosting options, features, and selection criteria"""
    return load_resource_content("hosting", "wordpress-hosting-providers")
@mcp.resource("wordpress://hosting/deployment-strategies")
def get_deployment_strategies() -> str:
    """WordPress Deployment Strategies - Modern deployment methodologies, tools, and best practices"""
    return load_resource_content("hosting", "deployment-strategies")
@mcp.resource("wordpress://hosting/server-configuration")
def get_server_configuration() -> str:
    """WordPress Server Configuration - Web server, PHP, database, and infrastructure optimization"""
    return load_resource_content("hosting", "server-configuration")
@mcp.resource("wordpress://hosting/ssl-security")
def get_ssl_security() -> str:
    """WordPress SSL and Security Configuration - SSL/TLS setup, security headers, and hardening"""
    return load_resource_content("hosting", "ssl-security")
@mcp.resource("wordpress://hosting/monitoring-logging")
def get_monitoring_logging() -> str:
    """WordPress Monitoring and Logging - Comprehensive monitoring, logging, and alerting strategies"""
    return load_resource_content("hosting", "monitoring-logging")
# === WORDPRESS COMMUNITY AND ECOSYSTEM ===

@mcp.resource("wordpress://ecosystem/wordpress-community")
def get_wordpress_community() -> str:
    """WordPress Community and Ecosystem - Comprehensive guide to the WordPress community, events, and contribution opportunities"""
    return load_resource_content("ecosystem", "wordpress-community")
@mcp.resource("wordpress://ecosystem/plugin-ecosystem")
def get_plugin_ecosystem() -> str:
    """WordPress Plugin Ecosystem - Complete guide to plugin development, marketplace, and business opportunities"""
    return load_resource_content("ecosystem", "plugin-ecosystem")
@mcp.resource("wordpress://ecosystem/theme-ecosystem")
def get_theme_ecosystem() -> str:
    """WordPress Theme Ecosystem - Comprehensive guide to theme development, marketplace, and design trends"""
    return load_resource_content("ecosystem", "theme-ecosystem")
@mcp.resource("wordpress://ecosystem/marketplace-resources")
def get_marketplace_resources() -> str:
    """WordPress Marketplace and Commercial Resources - Complete guide to commercial products, services, and business opportunities"""
    return load_resource_content("ecosystem", "marketplace-resources")
@mcp.resource("wordpress://ecosystem/industry-tools")
def get_industry_tools() -> str:
    """WordPress Industry Tools and Services - Comprehensive guide to development tools, services, and professional resources"""
    return load_resource_content("ecosystem", "industry-tools")
# === MCP SERVER SECURITY ===

import time
import hashlib
import hmac
from typing import Optional, Dict, Any
from functools import wraps

class MCPSecurityManager:
    """Security manager for MCP server operations."""
    
    def __init__(self):
        self.rate_limits: Dict[str, Dict[str, Any]] = {}
        self.api_keys: Dict[str, str] = {}  # In production, use secure storage
        self.blocked_ips: set = set()
        self.request_log: list = []
        
    def validate_request(self, request_data: Dict[str, Any]) -> bool:
        """Validate incoming MCP requests."""
        # Check for required fields
        required_fields = ['method', 'params']
        if not all(field in request_data for field in required_fields):
            self.log_security_event('invalid_request', request_data)
            return False
            
        # Validate method
        allowed_methods = ['resources/list', 'resources/read']
        if request_data.get('method') not in allowed_methods:
            self.log_security_event('invalid_method', request_data)
            return False
            
        return True
    
    def check_rate_limit(self, client_id: str, limit: int = 100, window: int = 3600) -> bool:
        """Check if client has exceeded rate limit."""
        current_time = time.time()
        
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = {'count': 0, 'window_start': current_time}
        
        rate_data = self.rate_limits[client_id]
        
        # Reset window if expired
        if current_time - rate_data['window_start'] > window:
            rate_data['count'] = 0
            rate_data['window_start'] = current_time
        
        # Check limit
        if rate_data['count'] >= limit:
            self.log_security_event('rate_limit_exceeded', {'client_id': client_id})
            return False
        
        rate_data['count'] += 1
        return True
    
    def authenticate_request(self, api_key: Optional[str] = None) -> bool:
        """Authenticate API requests."""
        # For public MCP servers, authentication might be optional
        if not api_key:
            return True  # Allow public access
            
        # Validate API key format
        if not api_key or len(api_key) < 32:
            self.log_security_event('invalid_api_key', {'api_key': api_key[:10] if api_key else None})
            return False
            
        # Check against stored keys (in production, use secure database)
        if api_key in self.api_keys:
            return True
            
        self.log_security_event('unauthorized_access', {'api_key': api_key[:10]})
        return False
    
    def sanitize_input(self, input_data: Any) -> Any:
        """Sanitize input data to prevent injection attacks."""
        if isinstance(input_data, str):
            # Remove potentially dangerous characters
            dangerous_chars = ['<', '>', '"', "'", '&', '\\', '/', ';', '(', ')']
            for char in dangerous_chars:
                input_data = input_data.replace(char, '')
            return input_data.strip()
        elif isinstance(input_data, dict):
            return {k: self.sanitize_input(v) for k, v in input_data.items()}
        elif isinstance(input_data, list):
            return [self.sanitize_input(item) for item in input_data]
        return input_data
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events for monitoring."""
        log_entry = {
            'timestamp': time.time(),
            'event_type': event_type,
            'details': details,
            'ip': details.get('ip', 'unknown')
        }
        self.request_log.append(log_entry)
        
        # Keep only last 1000 entries
        if len(self.request_log) > 1000:
            self.request_log = self.request_log[-1000:]
        
        logger.warning(f"Security event: {event_type} - {details}")
    
    def secure_error_response(self, error_type: str) -> str:
        """Return secure error responses without exposing internals."""
        secure_errors = {
            'invalid_request': 'Invalid request format',
            'rate_limit_exceeded': 'Rate limit exceeded. Please try again later.',
            'unauthorized_access': 'Authentication required',
            'resource_not_found': 'Resource not found',
            'internal_error': 'Internal server error'
        }
        return secure_errors.get(error_type, 'An error occurred')

# Initialize security manager
security_manager = MCPSecurityManager()

def secure_mcp_resource(rate_limit: int = 100, require_auth: bool = False):
    """Decorator to add security to MCP resources."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get client identifier (in production, use proper client identification)
            client_id = kwargs.get('client_id', 'anonymous')
            
            # Check rate limiting
            if not security_manager.check_rate_limit(client_id, rate_limit):
                raise Exception(security_manager.secure_error_response('rate_limit_exceeded'))
            
            # Check authentication if required
            api_key = kwargs.get('api_key')
            if require_auth and not security_manager.authenticate_request(api_key):
                raise Exception(security_manager.secure_error_response('unauthorized_access'))
            
            # Sanitize inputs
            sanitized_args = [security_manager.sanitize_input(arg) for arg in args]
            sanitized_kwargs = {k: security_manager.sanitize_input(v) for k, v in kwargs.items()}
            
            try:
                # Execute the original function
                result = func(*sanitized_args, **sanitized_kwargs)
                return result
            except Exception as e:
                # Log error securely
                security_manager.log_security_event('resource_error', {
                    'function': func.__name__,
                    'error': str(e)
                })
                raise Exception(security_manager.secure_error_response('internal_error'))
        
        return wrapper
    return decorator

# Apply security to critical resources
@mcp.resource("wordpress://security/mcp-server-security")
@secure_mcp_resource(rate_limit=50, require_auth=False)
def get_mcp_server_security() -> str:
    """MCP Server Security - Authentication, rate limiting, input validation, and security best practices"""
    return load_resource_content("security", "mcp-server-security")
@mcp.resource("wordpress://security/security-monitoring")
@secure_mcp_resource(rate_limit=30, require_auth=False)
def get_security_monitoring() -> str:
    """Security Monitoring and Alerting - Real-time security monitoring, logging, and incident response"""
    return load_resource_content("security", "security-monitoring")
# === ADDITIONAL WORDPRESS DEVELOPMENT RESOURCES ===

# Custom Post Types and Fields
@mcp.resource("wordpress://advanced/custom-post-types")
def get_custom_post_types() -> str:
    """WordPress Custom Post Types - Registration, capabilities, templates, and advanced usage"""
    return load_resource_content("advanced", "custom-post-types")


@mcp.resource("wordpress://advanced/meta-boxes")
def get_meta_boxes() -> str:
    """WordPress Meta Boxes - Creating custom admin interfaces and data management"""
    return load_resource_content("advanced", "meta-boxes")


@mcp.resource("wordpress://advanced/taxonomies")
def get_taxonomies() -> str:
    """WordPress Taxonomies - Custom taxonomies, terms, and hierarchical organization"""
    return load_resource_content("advanced", "taxonomies")


@mcp.resource("wordpress://advanced/wordpress-hooks")
def get_wordpress_hooks() -> str:
    """WordPress Hooks System - Actions, filters, and custom hook development"""
    return load_resource_content("advanced", "wordpress-hooks")


@mcp.resource("wordpress://advanced/ajax-development")
def get_ajax_development() -> str:
    """WordPress AJAX Development - Frontend and admin AJAX, security, and best practices"""
    return load_resource_content("advanced", "ajax-development")


@mcp.resource("wordpress://advanced/wordpress-cron")
def get_wordpress_cron() -> str:
    """WordPress Cron System - Scheduled tasks, wp-cron, and background processing"""
    return load_resource_content("advanced", "wordpress-cron")


@mcp.resource("wordpress://integrations/payment-gateways")
def get_payment_gateways() -> str:
    """WordPress Payment Gateway Integration - Stripe, PayPal, WooCommerce payments"""
    return load_resource_content("integrations", "payment-gateways")


@mcp.resource("wordpress://integrations/analytics-tracking")
def get_analytics_tracking() -> str:
    """WordPress Analytics and Tracking Integration - Google Analytics, Facebook Pixel, custom tracking"""
    return load_resource_content("integrations", "analytics-tracking")


@mcp.resource("wordpress://workflows/development-workflow")
def get_development_workflow() -> str:
    """WordPress Development Workflow - Git, deployment, testing, and automation best practices"""
    return load_resource_content("workflows", "development-workflow")