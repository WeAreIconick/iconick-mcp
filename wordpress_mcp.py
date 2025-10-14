"""
WordPress Development MCP Server - Comprehensive Edition

Provides complete WordPress development resources including documentation,
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
    print("WordPress Development MCP Server")
    print(f"Resources directory: {RESOURCES_DIR}")
    resource_files = list(RESOURCES_DIR.rglob("*.md"))
    print(f"Total resource files: {len(resource_files)}")
