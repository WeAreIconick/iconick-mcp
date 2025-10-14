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


if __name__ == "__main__":
    print("WordPress Development MCP Server - Expanded Edition")
    print(f"Resources directory: {RESOURCES_DIR}")
    resource_files = list(RESOURCES_DIR.rglob("*.md"))
    print(f"Total resource files: {len(resource_files)}")
    
    # List all available resources
    print("\nAvailable Resources:")
    for resource_file in sorted(resource_files):
        rel_path = resource_file.relative_to(RESOURCES_DIR)
        category = rel_path.parts[0]
        topic = rel_path.stem
        print(f"  wordpress://{category}/{topic}")


# === THEME DEVELOPMENT ===

@mcp.resource("wordpress://themes/template-hierarchy")
def get_template_hierarchy() -> str:
    """WordPress Template Hierarchy - Template selection, conditional tags (CRITICAL)"""
    return load_resource_content("themes", "template-hierarchy")


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
