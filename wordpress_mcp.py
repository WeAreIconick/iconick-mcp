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
