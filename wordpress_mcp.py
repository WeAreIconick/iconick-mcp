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
    return """# MCP Server Security Implementation

## Overview

This MCP server implements comprehensive security measures to protect against common attacks and ensure safe operation in production environments.

## Security Features Implemented

### 1. Input Validation and Sanitization

**Request Validation**
- Validates all incoming MCP requests
- Checks required fields and data types
- Prevents malformed requests

**Input Sanitization**
- Removes potentially dangerous characters
- Sanitizes strings, objects, and arrays
- Prevents injection attacks

### 2. Rate Limiting

**Per-Client Rate Limiting**
- Default: 100 requests per hour per client
- Configurable limits per resource
- Automatic window resets

**Implementation**
```python
# Rate limiting example
if not security_manager.check_rate_limit(client_id, limit=100, window=3600):
    raise Exception('Rate limit exceeded')
```

### 3. Authentication and Authorization

**API Key Authentication**
- Optional API key validation
- Secure key storage (in production)
- Unauthorized access logging

**Access Control**
- Resource-level permissions
- Client identification
- Audit trail maintenance

### 4. Security Logging and Monitoring

**Event Logging**
- All security events logged
- Detailed audit trails
- Suspicious activity detection

**Monitored Events**
- Invalid requests
- Rate limit violations
- Authentication failures
- Resource access attempts

### 5. Error Handling

**Secure Error Responses**
- No internal details exposed
- Standardized error messages
- Safe error logging

**Error Types**
- Invalid request format
- Rate limit exceeded
- Authentication required
- Resource not found
- Internal server error

## Security Best Practices

### Request Validation
```python
def validate_request(request_data):
    required_fields = ['method', 'params']
    if not all(field in request_data for field in required_fields):
        return False
    return True
```

### Input Sanitization
```python
def sanitize_input(input_data):
    if isinstance(input_data, str):
        dangerous_chars = ['<', '>', '"', "'", '&', '\\']
        for char in dangerous_chars:
            input_data = input_data.replace(char, '')
    return input_data
```

### Rate Limiting
```python
def check_rate_limit(client_id, limit=100, window=3600):
    current_time = time.time()
    # Check and update rate limit counters
    return rate_limit_check
```

## Production Security Considerations

### 1. Secure Configuration
- Use environment variables for sensitive data
- Implement proper secret management
- Enable HTTPS/TLS encryption

### 2. Monitoring and Alerting
- Real-time security monitoring
- Automated alerting for suspicious activity
- Regular security audits

### 3. Access Control
- Implement proper authentication
- Use role-based access control
- Regular access reviews

### 4. Data Protection
- Encrypt sensitive data at rest
- Use secure communication protocols
- Implement data retention policies

## Security Testing

### Automated Security Tests
- Input validation testing
- Rate limiting verification
- Authentication flow testing
- Error handling validation

### Security Audits
- Regular penetration testing
- Code security reviews
- Dependency vulnerability scanning
- Configuration security checks

## Compliance and Standards

### Security Standards
- OWASP security guidelines
- MCP protocol security requirements
- Industry best practices
- Regulatory compliance (as applicable)

### Documentation
- Security policy documentation
- Incident response procedures
- Security training materials
- Audit trail requirements

## Future Security Enhancements

### Advanced Features
- Machine learning-based threat detection
- Advanced authentication methods
- Real-time security analytics
- Automated security responses

### Integration
- SIEM system integration
- Security orchestration platforms
- Threat intelligence feeds
- Compliance monitoring tools
"""

@mcp.resource("wordpress://security/security-monitoring")
@secure_mcp_resource(rate_limit=30, require_auth=False)
def get_security_monitoring() -> str:
    """Security Monitoring and Alerting - Real-time security monitoring, logging, and incident response"""
    return """# Security Monitoring and Alerting

## Overview

Comprehensive security monitoring system for WordPress MCP servers, providing real-time threat detection, logging, and automated incident response.

## Monitoring Components

### 1. Real-Time Monitoring

**Request Monitoring**
- All incoming requests logged
- Response times tracked
- Error rates monitored
- Anomaly detection

**Security Event Detection**
- Failed authentication attempts
- Rate limit violations
- Suspicious request patterns
- Resource access anomalies

### 2. Logging and Audit Trails

**Security Logs**
- Authentication events
- Authorization failures
- Rate limiting events
- Resource access logs

**Audit Trail Features**
- Immutable log storage
- Tamper-proof logging
- Detailed request tracking
- User activity monitoring

### 3. Alerting System

**Real-Time Alerts**
- Immediate threat notifications
- Escalation procedures
- Alert correlation
- False positive reduction

**Alert Types**
- Security violations
- Performance anomalies
- System errors
- Configuration changes

## Implementation Examples

### Security Event Logging
```python
def log_security_event(event_type, details):
    log_entry = {
        'timestamp': time.time(),
        'event_type': event_type,
        'details': details,
        'severity': get_severity_level(event_type)
    }
    security_log.append(log_entry)
    send_alert_if_critical(log_entry)
```

### Rate Limiting Monitoring
```python
def monitor_rate_limits():
    for client_id, data in rate_limits.items():
        if data['count'] > threshold:
            send_rate_limit_alert(client_id, data)
```

### Anomaly Detection
```python
def detect_anomalies():
    recent_requests = get_recent_requests(time_window=300)
    patterns = analyze_request_patterns(recent_requests)
    anomalies = identify_anomalies(patterns)
    for anomaly in anomalies:
        handle_anomaly(anomaly)
```

## Monitoring Dashboards

### Security Dashboard
- Real-time threat indicators
- Security event timeline
- Attack pattern analysis
- Response status tracking

### Performance Dashboard
- Request volume trends
- Response time metrics
- Error rate monitoring
- Resource utilization

### Compliance Dashboard
- Security policy compliance
- Audit trail completeness
- Incident response metrics
- Regulatory compliance status

## Incident Response

### Automated Response
- Automatic threat blocking
- Rate limiting enforcement
- Resource access restrictions
- Notification escalation

### Manual Response
- Incident investigation
- Threat analysis
- Response coordination
- Recovery procedures

## Best Practices

### Log Management
- Centralized logging
- Log retention policies
- Secure log storage
- Regular log analysis

### Alert Tuning
- Reduce false positives
- Optimize alert thresholds
- Implement alert fatigue prevention
- Regular alert testing

### Monitoring Coverage
- Comprehensive coverage
- Multiple detection methods
- Cross-reference validation
- Continuous improvement
"""



# === HOMEPAGE ROUTE ===

import os



# === HOMEPAGE RESOURCE ===

@mcp.resource("data://homepage")
def get_homepage() -> str:
    """WordPress MCP Server Homepage - Landing page with server information and resource overview"""
    homepage_path = Path(__file__).parent / "index.html"
    if homepage_path.exists():
        with open(homepage_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # Fallback homepage if index.html is not found
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WordPress Development MCP Server</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 2em; 
            line-height: 1.6; 
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 2em;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 1em; }
        h2 { color: #34495e; margin-top: 2em; }
        p { margin-bottom: 1em; }
        .highlight { background: #f8f9fa; padding: 1em; border-left: 4px solid #007cba; margin: 1em 0; }
        .resource-count { font-size: 1.2em; font-weight: bold; color: #007cba; }
        ul { margin-left: 2em; }
        a { color: #007cba; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 WordPress Development MCP Server</h1>
        
        <div class="highlight">
            <p><strong>Welcome to the most comprehensive WordPress development resource hub!</strong></p>
            <p>This Model Context Protocol (MCP) server provides AI assistants with extensive WordPress development documentation, coding standards, best practices, and code examples.</p>
        </div>

        <h2>📊 Server Statistics</h2>
        <p><span class="resource-count">68 WordPress Resources</span> across 17 comprehensive categories</p>
        <p><strong>Server Version:</strong> 1.17.0</p>
        <p><strong>Protocol:</strong> MCP 2024-11-05</p>
        <p><strong>Status:</strong> Production Ready ✅</p>

        <h2>🎯 What's Available</h2>
        <ul>
            <li><strong>Core APIs:</strong> Database, HTTP, Options, Transients, Rewrite, Settings, Shortcode, Metadata, Filesystem</li>
            <li><strong>Security & Best Practices:</strong> Data validation, sanitization, escaping, nonces, capabilities</li>
            <li><strong>Theme Development:</strong> Template hierarchy, block themes, child themes, navigation</li>
            <li><strong>Block Editor:</strong> Block registration, components, dynamic blocks, patterns</li>
            <li><strong>REST API:</strong> Endpoints, authentication, schema, extensions</li>
            <li><strong>Coding Standards:</strong> PHP, JavaScript, CSS, HTML, SQL, accessibility</li>
            <li><strong>Development Tools:</strong> WP_DEBUG, Query Monitor, WP-CLI</li>
            <li><strong>Advanced Topics:</strong> Multisite, WooCommerce, performance optimization</li>
            <li><strong>WordPress Frameworks:</strong> Timber, Sage, Underscores</li>
            <li><strong>Testing & QA:</strong> WordPress testing, PHPUnit, quality assurance</li>
            <li><strong>Hosting & Deployment:</strong> Hosting providers, deployment strategies, server configuration</li>
            <li><strong>Community & Ecosystem:</strong> WordPress community, plugin ecosystem, theme ecosystem</li>
        </ul>

        <h2>🔧 How to Use</h2>
        <p>This MCP server is designed for AI assistants like Claude and Cursor. To access resources:</p>
        <ul>
            <li>Use MCP-compatible clients to connect to this server</li>
            <li>Request specific resources by URI (e.g., <code>wordpress://core/database</code>)</li>
            <li>Browse available resources using the MCP protocol</li>
        </ul>

        <h2>📚 Resource Categories</h2>
        <p>All resources follow the <code>wordpress://{category}/{topic}</code> URI pattern:</p>
        <ul>
            <li><code>wordpress://core/*</code> - WordPress core APIs</li>
            <li><code>wordpress://security/*</code> - Security best practices</li>
            <li><code>wordpress://themes/*</code> - Theme development</li>
            <li><code>wordpress://blocks/*</code> - Block editor development</li>
            <li><code>wordpress://rest-api/*</code> - REST API development</li>
            <li><code>wordpress://standards/*</code> - Coding standards</li>
            <li><code>wordpress://tools/*</code> - Development tools</li>
            <li><code>wordpress://advanced/*</code> - Advanced topics</li>
            <li><code>wordpress://frameworks/*</code> - WordPress frameworks</li>
            <li><code>wordpress://testing/*</code> - Testing and QA</li>
            <li><code>wordpress://hosting/*</code> - Hosting and deployment</li>
            <li><code>wordpress://ecosystem/*</code> - Community and ecosystem</li>
            <li><code>wordpress://system/*</code> - System resources</li>
        </ul>

        <h2>🚀 Getting Started</h2>
        <div class="highlight">
            <p><strong>For AI Assistants:</strong></p>
            <ul>
                <li>Connect to this MCP server using your client's configuration</li>
                <li>Request the <code>wordpress://system/resource-index</code> resource for a complete overview</li>
                <li>Use specific resource URIs for targeted information</li>
                <li>Cache frequently accessed resources for better performance</li>
            </ul>
        </div>

        <h2>📞 Support & Updates</h2>
        <p>This server is automatically maintained and updated with the latest WordPress development best practices. All resources are based on official WordPress documentation and community standards.</p>
        
        <p style="text-align: center; margin-top: 2em; color: #666;">
            <strong>WordPress Development MCP Server</strong><br>
            Powered by FastMCP • Built for AI Assistants
        </p>
    </div>
</body>
</html>
        """



# === ADDITIONAL WORDPRESS DEVELOPMENT RESOURCES ===

# Custom Post Types and Fields
@mcp.resource("wordpress://advanced/custom-post-types")
def get_custom_post_types() -> str:
    """WordPress Custom Post Types - Registration, capabilities, templates, and advanced usage"""
    return """# WordPress Custom Post Types

## Basic Registration

```php
function register_custom_post_type() {
    $args = array(
        'label'  => 'Products',
        'public' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'query_var' => true,
        'rewrite' => array('slug' => 'products'),
        'capability_type' => 'post',
        'has_archive' => true,
        'hierarchical' => false,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-cart',
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
        'show_in_rest' => true, // Enable Gutenberg editor
    );
    
    register_post_type('product', $args);
}
add_action('init', 'register_custom_post_type');
```

## Advanced Registration with Capabilities

```php
function register_advanced_cpt() {
    $labels = array(
        'name' => 'Portfolio Items',
        'singular_name' => 'Portfolio Item',
        'menu_name' => 'Portfolio',
        'add_new' => 'Add New Item',
        'add_new_item' => 'Add New Portfolio Item',
        'edit_item' => 'Edit Portfolio Item',
        'new_item' => 'New Portfolio Item',
        'view_item' => 'View Portfolio Item',
        'search_items' => 'Search Portfolio',
        'not_found' => 'No portfolio items found',
        'not_found_in_trash' => 'No portfolio items found in trash'
    );

    $args = array(
        'labels' => $labels,
        'public' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_admin_bar' => true,
        'show_in_nav_menus' => true,
        'can_export' => true,
        'delete_with_user' => false,
        'hierarchical' => false,
        'has_archive' => true,
        'exclude_from_search' => false,
        'publicly_queryable' => true,
        'capability_type' => array('portfolio_item', 'portfolio_items'),
        'map_meta_cap' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'comments', 'revisions', 'custom-fields'),
        'taxonomies' => array('portfolio_category', 'portfolio_tag'),
        'show_in_rest' => true,
        'rest_base' => 'portfolio',
        'rest_controller_class' => 'WP_REST_Posts_Controller',
    );

    register_post_type('portfolio', $args);
}
```

## Custom Fields and Meta Boxes

```php
// Add meta box for custom fields
function add_product_meta_box() {
    add_meta_box(
        'product_details',
        'Product Details',
        'product_meta_box_callback',
        'product',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes', 'add_product_meta_box');

function product_meta_box_callback($post) {
    wp_nonce_field('product_meta_box', 'product_meta_box_nonce');
    
    $price = get_post_meta($post->ID, '_product_price', true);
    $sku = get_post_meta($post->ID, '_product_sku', true);
    $stock = get_post_meta($post->ID, '_product_stock', true);
    ?>
    <table class="form-table">
        <tr>
            <th><label for="product_price">Price</label></th>
            <td><input type="text" id="product_price" name="product_price" value="<?php echo esc_attr($price); ?>" /></td>
        </tr>
        <tr>
            <th><label for="product_sku">SKU</label></th>
            <td><input type="text" id="product_sku" name="product_sku" value="<?php echo esc_attr($sku); ?>" /></td>
        </tr>
        <tr>
            <th><label for="product_stock">Stock Quantity</label></th>
            <td><input type="number" id="product_stock" name="product_stock" value="<?php echo esc_attr($stock); ?>" /></td>
        </tr>
    </table>
    <?php
}

// Save meta box data
function save_product_meta_box($post_id) {
    if (!isset($_POST['product_meta_box_nonce']) || 
        !wp_verify_nonce($_POST['product_meta_box_nonce'], 'product_meta_box')) {
        return;
    }

    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    if (!current_user_can('edit_post', $post_id)) {
        return;
    }

    if (isset($_POST['product_price'])) {
        update_post_meta($post_id, '_product_price', sanitize_text_field($_POST['product_price']));
    }

    if (isset($_POST['product_sku'])) {
        update_post_meta($post_id, '_product_sku', sanitize_text_field($_POST['product_sku']));
    }

    if (isset($_POST['product_stock'])) {
        update_post_meta($post_id, '_product_stock', absint($_POST['product_stock']));
    }
}
add_action('save_post', 'save_product_meta_box');
```

## Template Files

### Single Template
```php
// single-product.php
get_header(); ?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <header class="entry-header">
        <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
    </header>

    <div class="entry-content">
        <?php
        the_content();
        
        $price = get_post_meta(get_the_ID(), '_product_price', true);
        $sku = get_post_meta(get_the_ID(), '_product_sku', true);
        $stock = get_post_meta(get_the_ID(), '_product_stock', true);
        
        if ($price) {
            echo '<p><strong>Price:</strong> $' . esc_html($price) . '</p>';
        }
        if ($sku) {
            echo '<p><strong>SKU:</strong> ' . esc_html($sku) . '</p>';
        }
        if ($stock) {
            echo '<p><strong>Stock:</strong> ' . esc_html($stock) . '</p>';
        }
        ?>
    </div>
</article>

<?php get_footer(); ?>
```

### Archive Template
```php
// archive-product.php
get_header(); ?>

<div class="products-archive">
    <header class="page-header">
        <h1 class="page-title">Our Products</h1>
    </header>

    <div class="products-grid">
        <?php if (have_posts()) : ?>
            <?php while (have_posts()) : the_post(); ?>
                <div class="product-item">
                    <?php if (has_post_thumbnail()) : ?>
                        <div class="product-image">
                            <?php the_post_thumbnail('medium'); ?>
                        </div>
                    <?php endif; ?>
                    
                    <div class="product-info">
                        <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                        <div class="product-excerpt">
                            <?php the_excerpt(); ?>
                        </div>
                        
                        <?php
                        $price = get_post_meta(get_the_ID(), '_product_price', true);
                        if ($price) {
                            echo '<div class="product-price">$' . esc_html($price) . '</div>';
                        }
                        ?>
                        
                        <a href="<?php the_permalink(); ?>" class="product-link">View Details</a>
                    </div>
                </div>
            <?php endwhile; ?>
        <?php else : ?>
            <p>No products found.</p>
        <?php endif; ?>
    </div>
    
    <?php the_posts_navigation(); ?>
</div>

<?php get_footer(); ?>
```

## Query Custom Post Types

```php
// Query products with meta query
$args = array(
    'post_type' => 'product',
    'posts_per_page' => 10,
    'meta_query' => array(
        array(
            'key' => '_product_stock',
            'value' => 0,
            'compare' => '>'
        ),
        array(
            'key' => '_product_price',
            'value' => array(10, 100),
            'type' => 'NUMERIC',
            'compare' => 'BETWEEN'
        )
    ),
    'orderby' => 'meta_value_num',
    'meta_key' => '_product_price',
    'order' => 'ASC'
);

$products = new WP_Query($args);
```

## Custom Post Type with Custom Fields (Advanced)

```php
// Using ACF-style approach
class ProductCPT {
    public function __construct() {
        add_action('init', array($this, 'register_post_type'));
        add_action('add_meta_boxes', array($this, 'add_meta_boxes'));
        add_action('save_post', array($this, 'save_meta_fields'));
        add_action('rest_api_init', array($this, 'add_custom_fields_to_rest'));
    }

    public function register_post_type() {
        register_post_type('product', array(
            'labels' => array(
                'name' => 'Products',
                'singular_name' => 'Product'
            ),
            'public' => true,
            'show_in_rest' => true,
            'supports' => array('title', 'editor', 'thumbnail', 'excerpt'),
            'has_archive' => true,
        ));
    }

    public function add_meta_boxes() {
        add_meta_box(
            'product_details',
            'Product Details',
            array($this, 'render_meta_box'),
            'product'
        );
    }

    public function render_meta_box($post) {
        wp_nonce_field('product_meta', 'product_meta_nonce');
        
        $fields = array(
            'price' => 'Price',
            'sku' => 'SKU',
            'stock' => 'Stock Quantity',
            'weight' => 'Weight',
            'dimensions' => 'Dimensions'
        );

        echo '<table class="form-table">';
        foreach ($fields as $field => $label) {
            $value = get_post_meta($post->ID, '_product_' . $field, true);
            echo '<tr>';
            echo '<th><label for="product_' . $field . '">' . $label . '</label></th>';
            echo '<td><input type="text" id="product_' . $field . '" name="product_' . $field . '" value="' . esc_attr($value) . '" /></td>';
            echo '</tr>';
        }
        echo '</table>';
    }

    public function save_meta_fields($post_id) {
        if (!isset($_POST['product_meta_nonce']) || 
            !wp_verify_nonce($_POST['product_meta_nonce'], 'product_meta')) {
            return;
        }

        $fields = array('price', 'sku', 'stock', 'weight', 'dimensions');
        
        foreach ($fields as $field) {
            if (isset($_POST['product_' . $field])) {
                update_post_meta($post_id, '_product_' . $field, sanitize_text_field($_POST['product_' . $field]));
            }
        }
    }

    public function add_custom_fields_to_rest() {
        register_rest_field('product', 'product_details', array(
            'get_callback' => array($this, 'get_custom_fields'),
            'update_callback' => array($this, 'update_custom_fields'),
            'schema' => array(
                'description' => 'Product details',
                'type' => 'object',
                'properties' => array(
                    'price' => array('type' => 'string'),
                    'sku' => array('type' => 'string'),
                    'stock' => array('type' => 'string'),
                )
            )
        ));
    }

    public function get_custom_fields($post) {
        return array(
            'price' => get_post_meta($post['id'], '_product_price', true),
            'sku' => get_post_meta($post['id'], '_product_sku', true),
            'stock' => get_post_meta($post['id'], '_product_stock', true),
        );
    }

    public function update_custom_fields($value, $post) {
        update_post_meta($post->ID, '_product_price', $value['price']);
        update_post_meta($post->ID, '_product_sku', $value['sku']);
        update_post_meta($post->ID, '_product_stock', $value['stock']);
    }
}

new ProductCPT();
```

## Best Practices

1. **Use descriptive names** for post types and fields
2. **Always sanitize and validate** custom field data
3. **Use nonces** for security in meta boxes
4. **Create proper templates** for single and archive views
5. **Use meta queries** for filtering and sorting
6. **Enable REST API** support for modern applications
7. **Set proper capabilities** for security
8. **Use hooks** for extending functionality
9. **Cache expensive queries** with transients
10. **Test thoroughly** with different user roles

## Resources

- [WordPress Custom Post Types Documentation](https://developer.wordpress.org/reference/functions/register_post_type/)
- [Custom Fields Documentation](https://developer.wordpress.org/plugins/metadata/custom-meta-boxes/)
- [Template Hierarchy](https://developer.wordpress.org/themes/basics/template-hierarchy/)
"""


@mcp.resource("wordpress://advanced/meta-boxes")
def get_meta_boxes() -> str:
    """WordPress Meta Boxes - Creating custom admin interfaces and data management"""
    return """# WordPress Meta Boxes

## Basic Meta Box Creation

```php
function add_custom_meta_box() {
    add_meta_box(
        'custom_meta_box',           // Meta box ID
        'Custom Meta Box',           // Meta box title
        'custom_meta_box_callback',  // Callback function
        'post',                      // Post type
        'normal',                    // Context (normal, side, advanced)
        'high'                       // Priority (high, core, default, low)
    );
}
add_action('add_meta_boxes', 'add_custom_meta_box');

function custom_meta_box_callback($post) {
    // Add nonce field for security
    wp_nonce_field('custom_meta_box', 'custom_meta_box_nonce');
    
    // Get existing meta values
    $custom_field = get_post_meta($post->ID, '_custom_field', true);
    ?>
    <table class="form-table">
        <tr>
            <th><label for="custom_field">Custom Field</label></th>
            <td><input type="text" id="custom_field" name="custom_field" value="<?php echo esc_attr($custom_field); ?>" /></td>
        </tr>
    </table>
    <?php
}
```

## Advanced Meta Box with Multiple Fields

```php
class AdvancedMetaBox {
    private $fields = array(
        'text_field' => 'Text Field',
        'textarea_field' => 'Textarea Field',
        'select_field' => 'Select Field',
        'checkbox_field' => 'Checkbox Field',
        'radio_field' => 'Radio Field',
        'date_field' => 'Date Field',
        'color_field' => 'Color Field',
        'number_field' => 'Number Field'
    );

    public function __construct() {
        add_action('add_meta_boxes', array($this, 'add_meta_box'));
        add_action('save_post', array($this, 'save_meta_box'));
    }

    public function add_meta_box() {
        add_meta_box(
            'advanced_meta_box',
            'Advanced Meta Box',
            array($this, 'render_meta_box'),
            array('post', 'page'),
            'normal',
            'high'
        );
    }

    public function render_meta_box($post) {
        wp_nonce_field('advanced_meta_box', 'advanced_meta_box_nonce');
        
        echo '<div class="meta-box-container">';
        
        // Text Field
        $text_value = get_post_meta($post->ID, '_text_field', true);
        echo '<p>';
        echo '<label for="text_field"><strong>Text Field:</strong></label><br>';
        echo '<input type="text" id="text_field" name="text_field" value="' . esc_attr($text_value) . '" class="widefat" />';
        echo '</p>';

        // Textarea Field
        $textarea_value = get_post_meta($post->ID, '_textarea_field', true);
        echo '<p>';
        echo '<label for="textarea_field"><strong>Textarea Field:</strong></label><br>';
        echo '<textarea id="textarea_field" name="textarea_field" rows="4" class="widefat">' . esc_textarea($textarea_value) . '</textarea>';
        echo '</p>';

        // Select Field
        $select_value = get_post_meta($post->ID, '_select_field', true);
        $options = array('option1' => 'Option 1', 'option2' => 'Option 2', 'option3' => 'Option 3');
        echo '<p>';
        echo '<label for="select_field"><strong>Select Field:</strong></label><br>';
        echo '<select id="select_field" name="select_field" class="widefat">';
        echo '<option value="">Choose an option</option>';
        foreach ($options as $value => $label) {
            $selected = selected($select_value, $value, false);
            echo '<option value="' . esc_attr($value) . '" ' . $selected . '>' . esc_html($label) . '</option>';
        }
        echo '</select>';
        echo '</p>';

        // Checkbox Field
        $checkbox_value = get_post_meta($post->ID, '_checkbox_field', true);
        $checked = checked($checkbox_value, '1', false);
        echo '<p>';
        echo '<label for="checkbox_field">';
        echo '<input type="checkbox" id="checkbox_field" name="checkbox_field" value="1" ' . $checked . ' />';
        echo ' Checkbox Field';
        echo '</label>';
        echo '</p>';

        // Radio Fields
        $radio_value = get_post_meta($post->ID, '_radio_field', true);
        $radio_options = array('radio1' => 'Radio Option 1', 'radio2' => 'Radio Option 2');
        echo '<p>';
        echo '<label><strong>Radio Field:</strong></label><br>';
        foreach ($radio_options as $value => $label) {
            $checked = checked($radio_value, $value, false);
            echo '<label>';
            echo '<input type="radio" name="radio_field" value="' . esc_attr($value) . '" ' . $checked . ' />';
            echo ' ' . esc_html($label);
            echo '</label><br>';
        }
        echo '</p>';

        // Date Field
        $date_value = get_post_meta($post->ID, '_date_field', true);
        echo '<p>';
        echo '<label for="date_field"><strong>Date Field:</strong></label><br>';
        echo '<input type="date" id="date_field" name="date_field" value="' . esc_attr($date_value) . '" class="widefat" />';
        echo '</p>';

        // Color Field
        $color_value = get_post_meta($post->ID, '_color_field', true);
        echo '<p>';
        echo '<label for="color_field"><strong>Color Field:</strong></label><br>';
        echo '<input type="color" id="color_field" name="color_field" value="' . esc_attr($color_value) . '" />';
        echo '</p>';

        // Number Field
        $number_value = get_post_meta($post->ID, '_number_field', true);
        echo '<p>';
        echo '<label for="number_field"><strong>Number Field:</strong></label><br>';
        echo '<input type="number" id="number_field" name="number_field" value="' . esc_attr($number_value) . '" min="0" max="100" class="widefat" />';
        echo '</p>';

        echo '</div>';
    }

    public function save_meta_box($post_id) {
        // Security checks
        if (!isset($_POST['advanced_meta_box_nonce']) || 
            !wp_verify_nonce($_POST['advanced_meta_box_nonce'], 'advanced_meta_box')) {
            return;
        }

        if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
            return;
        }

        if (!current_user_can('edit_post', $post_id)) {
            return;
        }

        // Save each field
        $fields = array_keys($this->fields);
        
        foreach ($fields as $field) {
            if (isset($_POST[$field])) {
                $value = $_POST[$field];
                
                // Sanitize based on field type
                switch ($field) {
                    case 'text_field':
                    case 'select_field':
                    case 'radio_field':
                    case 'date_field':
                    case 'color_field':
                        $value = sanitize_text_field($value);
                        break;
                    case 'textarea_field':
                        $value = sanitize_textarea_field($value);
                        break;
                    case 'number_field':
                        $value = absint($value);
                        break;
                    case 'checkbox_field':
                        $value = isset($_POST[$field]) ? '1' : '0';
                        break;
                }
                
                update_post_meta($post_id, '_' . $field, $value);
            } else {
                // Handle unchecked checkboxes
                if ($field === 'checkbox_field') {
                    update_post_meta($post_id, '_' . $field, '0');
                }
            }
        }
    }
}

new AdvancedMetaBox();
```

## Conditional Meta Boxes

```php
function conditional_meta_box() {
    // Only show on specific post types
    $screen = get_current_screen();
    if ($screen->post_type === 'product') {
        add_meta_box(
            'product_details',
            'Product Details',
            'product_details_callback',
            'product',
            'normal',
            'high'
        );
    }
}
add_action('add_meta_boxes', 'conditional_meta_box');

function product_details_callback($post) {
    // Only show if post is published
    if ($post->post_status === 'publish') {
        echo '<p>This meta box only appears for published products.</p>';
        
        $price = get_post_meta($post->ID, '_product_price', true);
        echo '<p>Current Price: $' . esc_html($price) . '</p>';
    } else {
        echo '<p>Publish the post to see product details.</p>';
    }
}
```

## Meta Box with AJAX

```php
class AjaxMetaBox {
    public function __construct() {
        add_action('add_meta_boxes', array($this, 'add_meta_box'));
        add_action('save_post', array($this, 'save_meta_box'));
        add_action('wp_ajax_get_meta_data', array($this, 'ajax_get_meta_data'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_scripts'));
    }

    public function add_meta_box() {
        add_meta_box(
            'ajax_meta_box',
            'AJAX Meta Box',
            array($this, 'render_meta_box'),
            'post'
        );
    }

    public function render_meta_box($post) {
        wp_nonce_field('ajax_meta_box', 'ajax_meta_box_nonce');
        ?>
        <div id="ajax-meta-box">
            <button type="button" id="load-data" class="button">Load Data</button>
            <div id="meta-data-container"></div>
            
            <script>
            jQuery(document).ready(function($) {
                $('#load-data').click(function() {
                    var postId = <?php echo $post->ID; ?>;
                    
                    $.ajax({
                        url: ajaxurl,
                        type: 'POST',
                        data: {
                            action: 'get_meta_data',
                            post_id: postId,
                            nonce: '<?php echo wp_create_nonce('ajax_meta_box'); ?>'
                        },
                        success: function(response) {
                            $('#meta-data-container').html(response.data);
                        }
                    });
                });
            });
            </script>
        </div>
        <?php
    }

    public function ajax_get_meta_data() {
        check_ajax_referer('ajax_meta_box', 'nonce');
        
        $post_id = intval($_POST['post_id']);
        $meta_data = get_post_meta($post_id);
        
        wp_send_json_success('<pre>' . print_r($meta_data, true) . '</pre>');
    }

    public function enqueue_scripts() {
        wp_enqueue_script('jquery');
    }

    public function save_meta_box($post_id) {
        // Save logic here
    }
}

new AjaxMetaBox();
```

## Best Practices

1. **Always use nonces** for security
2. **Sanitize all input** based on expected data type
3. **Validate user capabilities** before saving
4. **Use descriptive field names** and labels
5. **Handle autosave** appropriately
6. **Use conditional logic** to show/hide fields
7. **Implement AJAX** for dynamic content
8. **Style your meta boxes** for better UX
9. **Group related fields** logically
10. **Test with different user roles**

## Resources

- [WordPress Meta Boxes Documentation](https://developer.wordpress.org/plugins/metadata/custom-meta-boxes/)
- [WordPress Nonces Documentation](https://developer.wordpress.org/plugins/security/nonces/)
- [WordPress Capabilities Documentation](https://developer.wordpress.org/plugins/users/roles-and-capabilities/)
"""



# WordPress Taxonomies and Terms
@mcp.resource("wordpress://advanced/taxonomies")
def get_taxonomies() -> str:
    """WordPress Taxonomies - Custom taxonomies, terms, and hierarchical organization"""
    return """# WordPress Taxonomies

## Basic Custom Taxonomy Registration

```php
function register_custom_taxonomy() {
    $labels = array(
        'name' => 'Product Categories',
        'singular_name' => 'Product Category',
        'menu_name' => 'Product Categories',
        'all_items' => 'All Product Categories',
        'edit_item' => 'Edit Product Category',
        'view_item' => 'View Product Category',
        'update_item' => 'Update Product Category',
        'add_new_item' => 'Add New Product Category',
        'new_item_name' => 'New Product Category Name',
        'search_items' => 'Search Product Categories',
        'popular_items' => 'Popular Product Categories',
        'separate_items_with_commas' => 'Separate product categories with commas',
        'add_or_remove_items' => 'Add or remove product categories',
        'choose_from_most_used' => 'Choose from most used product categories',
        'not_found' => 'No product categories found'
    );

    $args = array(
        'labels' => $labels,
        'hierarchical' => true,  // Like categories
        'public' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_tagcloud' => true,
        'show_in_quick_edit' => true,
        'show_admin_column' => true,
        'show_in_rest' => true,
        'rest_base' => 'product-categories',
        'rest_controller_class' => 'WP_REST_Terms_Controller',
        'query_var' => true,
        'rewrite' => array('slug' => 'product-category'),
        'capabilities' => array(
            'manage_terms' => 'manage_product_categories',
            'edit_terms' => 'edit_product_categories',
            'delete_terms' => 'delete_product_categories',
            'assign_terms' => 'assign_product_categories'
        )
    );

    register_taxonomy('product_category', array('product'), $args);
}
add_action('init', 'register_custom_taxonomy');
```

## Non-Hierarchical Taxonomy (Tags)

```php
function register_product_tags() {
    $labels = array(
        'name' => 'Product Tags',
        'singular_name' => 'Product Tag',
        'menu_name' => 'Product Tags',
        'all_items' => 'All Product Tags',
        'edit_item' => 'Edit Product Tag',
        'view_item' => 'View Product Tag',
        'update_item' => 'Update Product Tag',
        'add_new_item' => 'Add New Product Tag',
        'new_item_name' => 'New Product Tag Name',
        'search_items' => 'Search Product Tags',
        'popular_items' => 'Popular Product Tags',
        'separate_items_with_commas' => 'Separate product tags with commas',
        'add_or_remove_items' => 'Add or remove product tags',
        'choose_from_most_used' => 'Choose from most used product tags',
        'not_found' => 'No product tags found'
    );

    $args = array(
        'labels' => $labels,
        'hierarchical' => false,  // Like tags
        'public' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_tagcloud' => true,
        'show_in_quick_edit' => true,
        'show_admin_column' => true,
        'show_in_rest' => true,
        'query_var' => true,
        'rewrite' => array('slug' => 'product-tag'),
    );

    register_taxonomy('product_tag', array('product'), $args);
}
add_action('init', 'register_product_tags');
```

## Advanced Taxonomy with Meta Fields

```php
class AdvancedTaxonomy {
    public function __construct() {
        add_action('init', array($this, 'register_taxonomy'));
        add_action('product_category_add_form_fields', array($this, 'add_taxonomy_meta_fields'));
        add_action('product_category_edit_form_fields', array($this, 'edit_taxonomy_meta_fields'));
        add_action('edited_product_category', array($this, 'save_taxonomy_meta_fields'));
        add_action('created_product_category', array($this, 'save_taxonomy_meta_fields'));
    }

    public function register_taxonomy() {
        register_taxonomy('product_category', array('product'), array(
            'labels' => array(
                'name' => 'Product Categories',
                'singular_name' => 'Product Category'
            ),
            'hierarchical' => true,
            'public' => true,
            'show_in_rest' => true,
            'show_admin_column' => true,
        ));
    }

    public function add_taxonomy_meta_fields($taxonomy) {
        ?>
        <div class="form-field">
            <label for="category_color"><?php _e('Category Color', 'textdomain'); ?></label>
            <input type="color" name="category_color" id="category_color" value="#000000" />
            <p class="description"><?php _e('Color for this category', 'textdomain'); ?></p>
        </div>

        <div class="form-field">
            <label for="category_icon"><?php _e('Category Icon', 'textdomain'); ?></label>
            <input type="text" name="category_icon" id="category_icon" value="" />
            <p class="description"><?php _e('Icon class for this category (e.g., fa-heart)', 'textdomain'); ?></p>
        </div>

        <div class="form-field">
            <label for="category_description_short"><?php _e('Short Description', 'textdomain'); ?></label>
            <textarea name="category_description_short" id="category_description_short" rows="3" cols="50"></textarea>
            <p class="description"><?php _e('Short description for this category', 'textdomain'); ?></p>
        </div>
        <?php
    }

    public function edit_taxonomy_meta_fields($term) {
        $color = get_term_meta($term->term_id, 'category_color', true);
        $icon = get_term_meta($term->term_id, 'category_icon', true);
        $short_desc = get_term_meta($term->term_id, 'category_description_short', true);
        ?>
        <tr class="form-field">
            <th scope="row" valign="top">
                <label for="category_color"><?php _e('Category Color', 'textdomain'); ?></label>
            </th>
            <td>
                <input type="color" name="category_color" id="category_color" value="<?php echo esc_attr($color); ?>" />
                <p class="description"><?php _e('Color for this category', 'textdomain'); ?></p>
            </td>
        </tr>

        <tr class="form-field">
            <th scope="row" valign="top">
                <label for="category_icon"><?php _e('Category Icon', 'textdomain'); ?></label>
            </th>
            <td>
                <input type="text" name="category_icon" id="category_icon" value="<?php echo esc_attr($icon); ?>" />
                <p class="description"><?php _e('Icon class for this category (e.g., fa-heart)', 'textdomain'); ?></p>
            </td>
        </tr>

        <tr class="form-field">
            <th scope="row" valign="top">
                <label for="category_description_short"><?php _e('Short Description', 'textdomain'); ?></label>
            </th>
            <td>
                <textarea name="category_description_short" id="category_description_short" rows="3" cols="50"><?php echo esc_textarea($short_desc); ?></textarea>
                <p class="description"><?php _e('Short description for this category', 'textdomain'); ?></p>
            </td>
        </tr>
        <?php
    }

    public function save_taxonomy_meta_fields($term_id) {
        if (isset($_POST['category_color'])) {
            update_term_meta($term_id, 'category_color', sanitize_hex_color($_POST['category_color']));
        }
        
        if (isset($_POST['category_icon'])) {
            update_term_meta($term_id, 'category_icon', sanitize_text_field($_POST['category_icon']));
        }
        
        if (isset($_POST['category_description_short'])) {
            update_term_meta($term_id, 'category_description_short', sanitize_textarea_field($_POST['category_description_short']));
        }
    }
}

new AdvancedTaxonomy();
```

## Query Posts by Taxonomy

```php
// Query posts by taxonomy term
function get_posts_by_category($category_slug, $post_type = 'product') {
    $args = array(
        'post_type' => $post_type,
        'posts_per_page' => -1,
        'tax_query' => array(
            array(
                'taxonomy' => 'product_category',
                'field' => 'slug',
                'terms' => $category_slug,
            ),
        ),
    );

    return new WP_Query($args);
}

// Query posts by multiple taxonomy terms
function get_posts_by_multiple_taxonomies($categories, $tags) {
    $args = array(
        'post_type' => 'product',
        'posts_per_page' => 10,
        'tax_query' => array(
            'relation' => 'AND',
            array(
                'taxonomy' => 'product_category',
                'field' => 'slug',
                'terms' => $categories,
                'operator' => 'IN'
            ),
            array(
                'taxonomy' => 'product_tag',
                'field' => 'slug',
                'terms' => $tags,
                'operator' => 'IN'
            )
        ),
    );

    return new WP_Query($args);
}

// Get taxonomy terms with meta
function get_taxonomy_terms_with_meta($taxonomy = 'product_category') {
    $terms = get_terms(array(
        'taxonomy' => $taxonomy,
        'hide_empty' => false,
    ));

    foreach ($terms as $term) {
        $term->color = get_term_meta($term->term_id, 'category_color', true);
        $term->icon = get_term_meta($term->term_id, 'category_icon', true);
        $term->short_description = get_term_meta($term->term_id, 'category_description_short', true);
    }

    return $terms;
}
```

## Taxonomy Templates

### Taxonomy Archive Template
```php
// taxonomy-product_category.php
get_header(); ?>

<div class="product-category-archive">
    <?php
    $current_term = get_queried_object();
    $category_color = get_term_meta($current_term->term_id, 'category_color', true);
    $category_icon = get_term_meta($current_term->term_id, 'category_icon', true);
    ?>

    <header class="page-header" style="background-color: <?php echo esc_attr($category_color); ?>;">
        <div class="container">
            <?php if ($category_icon) : ?>
                <i class="<?php echo esc_attr($category_icon); ?>"></i>
            <?php endif; ?>
            
            <h1 class="page-title"><?php single_term_title(); ?></h1>
            
            <?php if (term_description()) : ?>
                <div class="term-description">
                    <?php echo term_description(); ?>
                </div>
            <?php endif; ?>
        </div>
    </header>

    <div class="products-grid">
        <?php if (have_posts()) : ?>
            <?php while (have_posts()) : the_post(); ?>
                <div class="product-item">
                    <?php if (has_post_thumbnail()) : ?>
                        <div class="product-image">
                            <?php the_post_thumbnail('medium'); ?>
                        </div>
                    <?php endif; ?>
                    
                    <div class="product-info">
                        <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                        <div class="product-excerpt">
                            <?php the_excerpt(); ?>
                        </div>
                    </div>
                </div>
            <?php endwhile; ?>
        <?php else : ?>
            <p>No products found in this category.</p>
        <?php endif; ?>
    </div>
</div>

<?php get_footer(); ?>
```

## Best Practices

1. **Use descriptive names** for taxonomies and terms
2. **Choose hierarchical vs non-hierarchical** based on your needs
3. **Set proper capabilities** for security
4. **Use meta fields** to extend taxonomy functionality
5. **Create proper templates** for taxonomy archives
6. **Use tax_query** for complex filtering
7. **Enable REST API** for modern applications
8. **Cache taxonomy queries** for performance
9. **Use term meta** for additional data
10. **Test with different user roles**

## Resources

- [WordPress Taxonomies Documentation](https://developer.wordpress.org/reference/functions/register_taxonomy/)
- [Taxonomy Templates](https://developer.wordpress.org/themes/basics/template-hierarchy/#custom-taxonomies)
- [Term Meta Documentation](https://developer.wordpress.org/reference/functions/get_term_meta/)
"""


@mcp.resource("wordpress://advanced/wordpress-hooks")
def get_wordpress_hooks() -> str:
    """WordPress Hooks System - Actions, filters, and custom hook development"""
    return """# WordPress Hooks System

## Understanding WordPress Hooks

WordPress hooks allow you to modify or extend functionality without editing core files. There are two types:

1. **Actions** - Execute code at specific points
2. **Filters** - Modify data before it's used

## Common Action Hooks

### Post Actions
```php
// After post is published
add_action('publish_post', 'send_notification_email');
function send_notification_email($post_id) {
    $post = get_post($post_id);
    $author = get_userdata($post->post_author);
    
    wp_mail(
        $author->user_email,
        'Post Published',
        'Your post "' . $post->post_title . '" has been published.'
    );
}

// Before post is deleted
add_action('before_delete_post', 'backup_post_before_delete');
function backup_post_before_delete($post_id) {
    $post = get_post($post_id);
    // Create backup logic here
}

// After post is saved
add_action('save_post', 'update_post_meta_on_save');
function update_post_meta_on_save($post_id) {
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }
    
    if (!current_user_can('edit_post', $post_id)) {
        return;
    }
    
    // Update custom meta fields
    if (isset($_POST['custom_field'])) {
        update_post_meta($post_id, '_custom_field', sanitize_text_field($_POST['custom_field']));
    }
}
```

### User Actions
```php
// After user registration
add_action('user_register', 'send_welcome_email');
function send_welcome_email($user_id) {
    $user = get_userdata($user_id);
    
    wp_mail(
        $user->user_email,
        'Welcome!',
        'Welcome to our site, ' . $user->display_name . '!'
    );
}

// After user login
add_action('wp_login', 'log_user_login', 10, 2);
function log_user_login($user_login, $user) {
    update_user_meta($user->ID, 'last_login', current_time('mysql'));
}

// Before user logout
add_action('wp_logout', 'clear_user_session_data');
function clear_user_session_data() {
    // Clear any temporary user data
}
```

### Admin Actions
```php
// Add custom admin menu
add_action('admin_menu', 'add_custom_admin_menu');
function add_custom_admin_menu() {
    add_menu_page(
        'Custom Page',
        'Custom Menu',
        'manage_options',
        'custom-page',
        'custom_admin_page_callback',
        'dashicons-admin-tools',
        30
    );
}

// Add admin notices
add_action('admin_notices', 'display_admin_notices');
function display_admin_notices() {
    if (get_option('show_custom_notice')) {
        echo '<div class="notice notice-success is-dismissible">';
        echo '<p>This is a custom admin notice!</p>';
        echo '</div>';
    }
}

// Add admin footer text
add_action('admin_footer_text', 'custom_admin_footer');
function custom_admin_footer($text) {
    return 'Custom footer text';
}
```

## Common Filter Hooks

### Content Filters
```php
// Modify post content
add_filter('the_content', 'add_custom_content_to_posts');
function add_custom_content_to_posts($content) {
    if (is_single() && get_post_type() === 'post') {
        $custom_content = '<div class="custom-content">Custom content here</div>';
        $content .= $custom_content;
    }
    return $content;
}

// Modify post title
add_filter('the_title', 'modify_post_title');
function modify_post_title($title) {
    if (is_single()) {
        $title = '📖 ' . $title;
    }
    return $title;
}

// Modify excerpt length
add_filter('excerpt_length', 'custom_excerpt_length');
function custom_excerpt_length($length) {
    return 30; // 30 words
}

// Modify excerpt more text
add_filter('excerpt_more', 'custom_excerpt_more');
function custom_excerpt_more($more) {
    return '... <a href="' . get_permalink() . '">Read more</a>';
}
```

### Query Filters
```php
// Modify main query
add_action('pre_get_posts', 'modify_main_query');
function modify_main_query($query) {
    if (!is_admin() && $query->is_main_query()) {
        if (is_home()) {
            $query->set('posts_per_page', 5);
            $query->set('post_type', array('post', 'custom_post_type'));
        }
    }
}

// Modify post query args
add_filter('posts_where', 'modify_posts_where');
function modify_posts_where($where) {
    if (is_admin()) {
        return $where;
    }
    
    // Add custom WHERE clause
    $where .= " AND post_title NOT LIKE '%spam%'";
    return $where;
}

// Modify post query order
add_filter('posts_orderby', 'modify_posts_orderby');
function modify_posts_orderby($orderby) {
    if (is_home()) {
        $orderby = 'post_date DESC, post_title ASC';
    }
    return $orderby;
}
```

## Custom Hooks

### Creating Custom Actions
```php
// Define custom action
function process_custom_data($data) {
    // Do some processing
    $processed_data = sanitize_text_field($data);
    
    // Fire custom action
    do_action('custom_data_processed', $processed_data, $data);
    
    return $processed_data;
}

// Use custom action
add_action('custom_data_processed', 'log_custom_data_processing', 10, 2);
function log_custom_data_processing($processed_data, $original_data) {
    error_log('Custom data processed: ' . $original_data . ' -> ' . $processed_data);
}

add_action('custom_data_processed', 'send_custom_data_notification');
function send_custom_data_notification($processed_data) {
    // Send notification logic
}
```

### Creating Custom Filters
```php
// Define custom filter
function get_custom_data($data) {
    // Apply custom filters
    $filtered_data = apply_filters('custom_data_filter', $data);
    
    return $filtered_data;
}

// Use custom filter
add_filter('custom_data_filter', 'add_custom_prefix');
function add_custom_prefix($data) {
    return 'CUSTOM: ' . $data;
}

add_filter('custom_data_filter', 'add_timestamp', 20);
function add_timestamp($data) {
    return $data . ' [' . current_time('Y-m-d H:i:s') . ']';
}
```

## Hook Priority and Arguments

### Priority System
```php
// Default priority is 10
add_action('init', 'function_one'); // Priority 10
add_action('init', 'function_two', 5); // Priority 5 (runs first)
add_action('init', 'function_three', 15); // Priority 15 (runs last)
add_action('init', 'function_four', 10, 2); // Priority 10, 2 arguments
```

### Multiple Arguments
```php
// Action with multiple arguments
add_action('save_post', 'save_post_with_arguments', 10, 3);
function save_post_with_arguments($post_id, $post, $update) {
    if ($update) {
        // Post was updated
        error_log('Post updated: ' . $post->post_title);
    } else {
        // Post was created
        error_log('Post created: ' . $post->post_title);
    }
}

// Filter with multiple arguments
add_filter('post_link', 'modify_post_link', 10, 3);
function modify_post_link($post_link, $post, $leavename) {
    if ($post->post_type === 'custom_post_type') {
        $post_link = home_url('/custom/' . $post->post_name . '/');
    }
    return $post_link;
}
```

## Advanced Hook Usage

### Conditional Hooks
```php
// Only run on specific pages
add_action('wp_head', 'add_custom_meta_tags');
function add_custom_meta_tags() {
    if (is_single() && get_post_type() === 'product') {
        $product_price = get_post_meta(get_the_ID(), '_product_price', true);
        if ($product_price) {
            echo '<meta property="product:price" content="' . esc_attr($product_price) . '">';
        }
    }
}

// Only run for specific user roles
add_action('admin_init', 'add_custom_capabilities');
function add_custom_capabilities() {
    if (current_user_can('manage_options')) {
        // Add custom capabilities
    }
}
```

### Hook Removal
```php
// Remove default hooks
remove_action('wp_head', 'wp_generator');
remove_filter('the_content', 'wpautop');

// Remove hooks with priority
remove_action('save_post', 'save_post_function', 10);

// Remove all hooks for a specific action
remove_all_actions('wp_footer');

// Check if hook exists before removing
if (has_action('wp_head', 'some_function')) {
    remove_action('wp_head', 'some_function');
}
```

## Best Practices

1. **Use descriptive function names** for hook callbacks
2. **Always check conditions** before executing hook code
3. **Use proper priority** to control execution order
4. **Sanitize and validate** data in hooks
5. **Use nonces** for security in admin hooks
6. **Remove hooks** when no longer needed
7. **Document custom hooks** for other developers
8. **Test hooks thoroughly** in different scenarios
9. **Use conditional logic** to prevent conflicts
10. **Follow WordPress coding standards**

## Resources

- [WordPress Plugin API Documentation](https://developer.wordpress.org/plugins/hooks/)
- [Action Reference](https://codex.wordpress.org/Plugin_API/Action_Reference)
- [Filter Reference](https://codex.wordpress.org/Plugin_API/Filter_Reference)
- [Hook Priority Documentation](https://developer.wordpress.org/plugins/hooks/priority/)
"""



# WordPress AJAX Development
@mcp.resource("wordpress://advanced/ajax-development")
def get_ajax_development() -> str:
    """WordPress AJAX Development - Frontend and admin AJAX, security, and best practices"""
    return """# WordPress AJAX Development

## Admin AJAX

### Basic Admin AJAX Setup
```php
// Add AJAX actions for logged-in users
add_action('wp_ajax_my_action', 'my_ajax_handler');
// Add AJAX actions for non-logged-in users
add_action('wp_ajax_nopriv_my_action', 'my_ajax_handler');

function my_ajax_handler() {
    // Verify nonce for security
    check_ajax_referer('my_ajax_nonce', 'nonce');
    
    // Check user capabilities
    if (!current_user_can('edit_posts')) {
        wp_die('Unauthorized');
    }
    
    $data = $_POST['data'];
    $result = process_data($data);
    
    wp_send_json_success($result);
}
```

### Admin AJAX with Nonce Security
```php
class SecureAjaxHandler {
    public function __construct() {
        add_action('wp_ajax_secure_action', array($this, 'handle_secure_action'));
        add_action('wp_ajax_nopriv_secure_action', array($this, 'handle_secure_action'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_scripts'));
    }

    public function enqueue_scripts() {
        wp_enqueue_script('jquery');
        
        wp_localize_script('jquery', 'ajax_object', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'nonce' => wp_create_nonce('secure_ajax_nonce')
        ));
    }

    public function handle_secure_action() {
        // Verify nonce
        if (!wp_verify_nonce($_POST['nonce'], 'secure_ajax_nonce')) {
            wp_send_json_error('Invalid nonce');
        }

        // Check user capabilities
        if (!current_user_can('manage_options')) {
            wp_send_json_error('Insufficient permissions');
        }

        // Validate and sanitize input
        $input_data = sanitize_text_field($_POST['data']);
        
        if (empty($input_data)) {
            wp_send_json_error('Data is required');
        }

        // Process the data
        $result = $this->process_data($input_data);
        
        wp_send_json_success($result);
    }

    private function process_data($data) {
        // Your processing logic here
        return array('processed' => $data, 'timestamp' => current_time('mysql'));
    }
}

new SecureAjaxHandler();
```

### Frontend AJAX with JavaScript
```php
// Enqueue scripts for frontend AJAX
function enqueue_frontend_ajax_scripts() {
    wp_enqueue_script('jquery');
    
    wp_localize_script('jquery', 'frontend_ajax', array(
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('frontend_ajax_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'enqueue_frontend_ajax_scripts');

// Handle frontend AJAX
add_action('wp_ajax_frontend_action', 'handle_frontend_ajax');
add_action('wp_ajax_nopriv_frontend_action', 'handle_frontend_ajax');

function handle_frontend_ajax() {
    check_ajax_referer('frontend_ajax_nonce', 'nonce');
    
    $action = sanitize_text_field($_POST['action_type']);
    
    switch ($action) {
        case 'get_posts':
            $posts = get_posts(array('numberposts' => 5));
            wp_send_json_success($posts);
            break;
            
        case 'update_meta':
            $post_id = intval($_POST['post_id']);
            $meta_value = sanitize_text_field($_POST['meta_value']);
            update_post_meta($post_id, '_custom_meta', $meta_value);
            wp_send_json_success('Meta updated');
            break;
            
        default:
            wp_send_json_error('Invalid action');
    }
}
```

### JavaScript AJAX Implementation
```javascript
// Frontend AJAX with jQuery
jQuery(document).ready(function($) {
    $('#ajax-button').click(function(e) {
        e.preventDefault();
        
        var button = $(this);
        var postId = button.data('post-id');
        
        // Disable button during request
        button.prop('disabled', true).text('Processing...');
        
        $.ajax({
            url: frontend_ajax.ajax_url,
            type: 'POST',
            data: {
                action: 'frontend_action',
                action_type: 'update_meta',
                post_id: postId,
                meta_value: 'new_value',
                nonce: frontend_ajax.nonce
            },
            success: function(response) {
                if (response.success) {
                    $('#result').html('<div class="success">' + response.data + '</div>');
                } else {
                    $('#result').html('<div class="error">' + response.data + '</div>');
                }
            },
            error: function() {
                $('#result').html('<div class="error">Request failed</div>');
            },
            complete: function() {
                // Re-enable button
                button.prop('disabled', false).text('Update Meta');
            }
        });
    });
});
```

## Advanced AJAX Patterns

### AJAX with REST API
```php
// Register REST API endpoint for AJAX
add_action('rest_api_init', function () {
    register_rest_route('myplugin/v1', '/ajax-action', array(
        'methods' => 'POST',
        'callback' => 'handle_rest_ajax',
        'permission_callback' => function () {
            return current_user_can('edit_posts');
        },
        'args' => array(
            'data' => array(
                'required' => true,
                'sanitize_callback' => 'sanitize_text_field'
            )
        )
    ));
});

function handle_rest_ajax($request) {
    $data = $request->get_param('data');
    $result = process_ajax_data($data);
    
    return new WP_REST_Response($result, 200);
}
```

### AJAX with File Upload
```php
// Handle file upload via AJAX
add_action('wp_ajax_upload_file', 'handle_file_upload');
function handle_file_upload() {
    check_ajax_referer('upload_nonce', 'nonce');
    
    if (!current_user_can('upload_files')) {
        wp_send_json_error('Insufficient permissions');
    }
    
    if (!isset($_FILES['file'])) {
        wp_send_json_error('No file uploaded');
    }
    
    $file = $_FILES['file'];
    
    // Validate file type
    $allowed_types = array('image/jpeg', 'image/png', 'image/gif');
    if (!in_array($file['type'], $allowed_types)) {
        wp_send_json_error('Invalid file type');
    }
    
    // Validate file size (2MB limit)
    if ($file['size'] > 2 * 1024 * 1024) {
        wp_send_json_error('File too large');
    }
    
    // Upload file
    $upload = wp_handle_upload($file, array('test_form' => false));
    
    if ($upload && !isset($upload['error'])) {
        wp_send_json_success(array(
            'url' => $upload['url'],
            'file' => $upload['file']
        ));
    } else {
        wp_send_json_error($upload['error']);
    }
}
```

### AJAX with Database Operations
```php
// AJAX database operations
add_action('wp_ajax_db_operation', 'handle_db_operation');
function handle_db_operation() {
    check_ajax_referer('db_ajax_nonce', 'nonce');
    
    global $wpdb;
    
    $operation = sanitize_text_field($_POST['operation']);
    $table_name = $wpdb->prefix . 'custom_table';
    
    switch ($operation) {
        case 'insert':
            $name = sanitize_text_field($_POST['name']);
            $email = sanitize_email($_POST['email']);
            
            $result = $wpdb->insert(
                $table_name,
                array(
                    'name' => $name,
                    'email' => $email,
                    'created_at' => current_time('mysql')
                ),
                array('%s', '%s', '%s')
            );
            
            if ($result) {
                wp_send_json_success('Record inserted successfully');
            } else {
                wp_send_json_error('Failed to insert record');
            }
            break;
            
        case 'update':
            $id = intval($_POST['id']);
            $name = sanitize_text_field($_POST['name']);
            
            $result = $wpdb->update(
                $table_name,
                array('name' => $name),
                array('id' => $id),
                array('%s'),
                array('%d')
            );
            
            if ($result !== false) {
                wp_send_json_success('Record updated successfully');
            } else {
                wp_send_json_error('Failed to update record');
            }
            break;
            
        case 'delete':
            $id = intval($_POST['id']);
            
            $result = $wpdb->delete(
                $table_name,
                array('id' => $id),
                array('%d')
            );
            
            if ($result) {
                wp_send_json_success('Record deleted successfully');
            } else {
                wp_send_json_error('Failed to delete record');
            }
            break;
            
        default:
            wp_send_json_error('Invalid operation');
    }
}
```

## AJAX Security Best Practices

### Input Validation and Sanitization
```php
class SecureAjaxValidator {
    public static function validate_email($email) {
        if (!is_email($email)) {
            wp_send_json_error('Invalid email address');
        }
        return sanitize_email($email);
    }
    
    public static function validate_text($text, $max_length = 255) {
        if (strlen($text) > $max_length) {
            wp_send_json_error('Text too long');
        }
        return sanitize_text_field($text);
    }
    
    public static function validate_number($number, $min = null, $max = null) {
        if (!is_numeric($number)) {
            wp_send_json_error('Invalid number');
        }
        
        $number = floatval($number);
        
        if ($min !== null && $number < $min) {
            wp_send_json_error('Number too small');
        }
        
        if ($max !== null && $number > $max) {
            wp_send_json_error('Number too large');
        }
        
        return $number;
    }
}
```

### Rate Limiting for AJAX
```php
class AjaxRateLimiter {
    private static $limit = 10; // requests per minute
    private static $window = 60; // seconds
    
    public static function check_rate_limit($user_id = null) {
        if (!$user_id) {
            $user_id = get_current_user_id();
        }
        
        $transient_key = 'ajax_rate_limit_' . $user_id;
        $requests = get_transient($transient_key);
        
        if ($requests === false) {
            set_transient($transient_key, 1, self::$window);
            return true;
        }
        
        if ($requests >= self::$limit) {
            wp_send_json_error('Rate limit exceeded');
        }
        
        set_transient($transient_key, $requests + 1, self::$window);
        return true;
    }
}
```

## Best Practices

1. **Always use nonces** for security
2. **Validate and sanitize** all input data
3. **Check user capabilities** before processing
4. **Use proper error handling** and user feedback
5. **Implement rate limiting** to prevent abuse
6. **Use REST API** for complex operations
7. **Handle file uploads** securely
8. **Provide loading states** in JavaScript
9. **Test with different user roles**
10. **Log AJAX requests** for debugging

## Resources

- [WordPress AJAX Documentation](https://developer.wordpress.org/plugins/javascript/ajax/)
- [WordPress Nonces Documentation](https://developer.wordpress.org/plugins/security/nonces/)
- [WordPress REST API Documentation](https://developer.wordpress.org/rest-api/)
"""


@mcp.resource("wordpress://advanced/wordpress-cron")
def get_wordpress_cron() -> str:
    """WordPress Cron System - Scheduled tasks, wp-cron, and background processing"""
    return """# WordPress Cron System

## Understanding WordPress Cron

WordPress has its own cron system called `wp-cron` that handles scheduled tasks. Unlike system cron, it's triggered by website visits.

## Basic Cron Jobs

### Scheduling a Single Event
```php
// Schedule a one-time event
function schedule_cleanup_task() {
    if (!wp_next_scheduled('my_cleanup_task')) {
        wp_schedule_single_event(time() + 3600, 'my_cleanup_task'); // Run in 1 hour
    }
}
add_action('init', 'schedule_cleanup_task');

// Handle the scheduled task
add_action('my_cleanup_task', 'perform_cleanup');
function perform_cleanup() {
    // Your cleanup logic here
    error_log('Cleanup task executed at ' . current_time('mysql'));
}
```

### Recurring Events
```php
// Schedule a recurring event
function schedule_daily_task() {
    if (!wp_next_scheduled('daily_maintenance')) {
        wp_schedule_event(time(), 'daily', 'daily_maintenance');
    }
}
add_action('init', 'schedule_daily_task');

// Handle the daily task
add_action('daily_maintenance', 'perform_daily_maintenance');
function perform_daily_maintenance() {
    // Daily maintenance tasks
    cleanup_expired_transients();
    update_statistics();
    send_daily_reports();
}

// Clean up on deactivation
register_deactivation_hook(__FILE__, 'clear_scheduled_events');
function clear_scheduled_events() {
    wp_clear_scheduled_hook('daily_maintenance');
}
```

## Custom Cron Intervals

```php
// Add custom cron intervals
function add_custom_cron_intervals($schedules) {
    $schedules['every_15_minutes'] = array(
        'interval' => 900, // 15 minutes
        'display' => __('Every 15 Minutes')
    );
    
    $schedules['every_hour'] = array(
        'interval' => 3600, // 1 hour
        'display' => __('Every Hour')
    );
    
    $schedules['weekly'] = array(
        'interval' => 604800, // 1 week
        'display' => __('Weekly')
    );
    
    return $schedules;
}
add_filter('cron_schedules', 'add_custom_cron_intervals');

// Use custom interval
function schedule_custom_interval_task() {
    if (!wp_next_scheduled('hourly_task')) {
        wp_schedule_event(time(), 'every_hour', 'hourly_task');
    }
}
add_action('init', 'schedule_custom_interval_task');
```

## Advanced Cron Management

### Cron Job Manager Class
```php
class CronJobManager {
    private $jobs = array();
    
    public function __construct() {
        add_action('init', array($this, 'schedule_jobs'));
        add_action('wp_ajax_manual_cron_run', array($this, 'manual_cron_run'));
    }
    
    public function add_job($hook, $interval, $args = array()) {
        $this->jobs[] = array(
            'hook' => $hook,
            'interval' => $interval,
            'args' => $args
        );
    }
    
    public function schedule_jobs() {
        foreach ($this->jobs as $job) {
            if (!wp_next_scheduled($job['hook'], $job['args'])) {
                wp_schedule_event(time(), $job['interval'], $job['hook'], $job['args']);
            }
        }
    }
    
    public function manual_cron_run() {
        check_ajax_referer('manual_cron_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        $hook = sanitize_text_field($_POST['hook']);
        
        if (has_action($hook)) {
            do_action($hook);
            wp_send_json_success('Cron job executed successfully');
        } else {
            wp_send_json_error('Cron job not found');
        }
    }
}

// Initialize and add jobs
$cron_manager = new CronJobManager();
$cron_manager->add_job('backup_database', 'daily');
$cron_manager->add_job('cleanup_logs', 'weekly');
$cron_manager->add_job('update_statistics', 'every_hour');
```

### Database Backup Cron Job
```php
add_action('backup_database', 'perform_database_backup');
function perform_database_backup() {
    global $wpdb;
    
    $backup_dir = WP_CONTENT_DIR . '/backups/';
    if (!file_exists($backup_dir)) {
        wp_mkdir_p($backup_dir);
    }
    
    $backup_file = $backup_dir . 'backup_' . date('Y-m-d_H-i-s') . '.sql';
    
    // Get database credentials
    $host = DB_HOST;
    $username = DB_USER;
    $password = DB_PASSWORD;
    $database = DB_NAME;
    
    // Create mysqldump command
    $command = "mysqldump -h{$host} -u{$username} -p{$password} {$database} > {$backup_file}";
    
    // Execute backup
    exec($command, $output, $return_var);
    
    if ($return_var === 0) {
        error_log('Database backup created: ' . $backup_file);
        
        // Clean up old backups (keep last 7 days)
        cleanup_old_backups($backup_dir, 7);
    } else {
        error_log('Database backup failed');
    }
}

function cleanup_old_backups($backup_dir, $days_to_keep) {
    $files = glob($backup_dir . 'backup_*.sql');
    $cutoff_time = time() - ($days_to_keep * 24 * 60 * 60);
    
    foreach ($files as $file) {
        if (filemtime($file) < $cutoff_time) {
            unlink($file);
        }
    }
}
```

## Cron with Background Processing

### Background Task Processor
```php
class BackgroundTaskProcessor {
    private $queue_table;
    
    public function __construct() {
        global $wpdb;
        $this->queue_table = $wpdb->prefix . 'background_tasks';
        
        add_action('init', array($this, 'create_queue_table'));
        add_action('process_background_tasks', array($this, 'process_queue'));
        
        // Schedule processing every 5 minutes
        if (!wp_next_scheduled('process_background_tasks')) {
            wp_schedule_event(time(), 'every_5_minutes', 'process_background_tasks');
        }
    }
    
    public function create_queue_table() {
        global $wpdb;
        
        $charset_collate = $wpdb->get_charset_collate();
        
        $sql = "CREATE TABLE IF NOT EXISTS {$this->queue_table} (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            task_type varchar(100) NOT NULL,
            task_data longtext,
            status varchar(20) DEFAULT 'pending',
            attempts int(11) DEFAULT 0,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            processed_at datetime NULL,
            PRIMARY KEY (id),
            KEY status (status),
            KEY task_type (task_type)
        ) $charset_collate;";
        
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql);
    }
    
    public function add_task($task_type, $task_data) {
        global $wpdb;
        
        $wpdb->insert(
            $this->queue_table,
            array(
                'task_type' => $task_type,
                'task_data' => json_encode($task_data),
                'status' => 'pending'
            ),
            array('%s', '%s', '%s')
        );
        
        return $wpdb->insert_id;
    }
    
    public function process_queue() {
        global $wpdb;
        
        // Get pending tasks (limit to 10 per run)
        $tasks = $wpdb->get_results(
            "SELECT * FROM {$this->queue_table} 
             WHERE status = 'pending' AND attempts < 3 
             ORDER BY created_at ASC 
             LIMIT 10"
        );
        
        foreach ($tasks as $task) {
            $this->process_task($task);
        }
    }
    
    private function process_task($task) {
        global $wpdb;
        
        // Update attempt count
        $wpdb->update(
            $this->queue_table,
            array('attempts' => $task->attempts + 1),
            array('id' => $task->id),
            array('%d'),
            array('%d')
        );
        
        try {
            $task_data = json_decode($task->task_data, true);
            
            // Process based on task type
            switch ($task->task_type) {
                case 'send_email':
                    $this->send_email($task_data);
                    break;
                case 'process_image':
                    $this->process_image($task_data);
                    break;
                case 'generate_report':
                    $this->generate_report($task_data);
                    break;
                default:
                    throw new Exception('Unknown task type: ' . $task->task_type);
            }
            
            // Mark as completed
            $wpdb->update(
                $this->queue_table,
                array(
                    'status' => 'completed',
                    'processed_at' => current_time('mysql')
                ),
                array('id' => $task->id),
                array('%s', '%s'),
                array('%d')
            );
            
        } catch (Exception $e) {
            // Mark as failed if max attempts reached
            if ($task->attempts >= 2) {
                $wpdb->update(
                    $this->queue_table,
                    array(
                        'status' => 'failed',
                        'processed_at' => current_time('mysql')
                    ),
                    array('id' => $task->id),
                    array('%s', '%s'),
                    array('%d')
                );
            }
            
            error_log('Background task failed: ' . $e->getMessage());
        }
    }
    
    private function send_email($data) {
        wp_mail($data['to'], $data['subject'], $data['message']);
    }
    
    private function process_image($data) {
        // Image processing logic
    }
    
    private function generate_report($data) {
        // Report generation logic
    }
}

new BackgroundTaskProcessor();
```

## Cron Monitoring and Debugging

### Cron Status Dashboard
```php
class CronStatusDashboard {
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
    }
    
    public function add_admin_menu() {
        add_management_page(
            'Cron Status',
            'Cron Status',
            'manage_options',
            'cron-status',
            array($this, 'display_cron_status')
        );
    }
    
    public function display_cron_status() {
        $cron_jobs = _get_cron_array();
        ?>
        <div class="wrap">
            <h1>Cron Status</h1>
            
            <h2>Scheduled Events</h2>
            <table class="widefat">
                <thead>
                    <tr>
                        <th>Hook</th>
                        <th>Next Run</th>
                        <th>Recurrence</th>
                        <th>Args</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($cron_jobs as $timestamp => $hooks) : ?>
                        <?php foreach ($hooks as $hook => $events) : ?>
                            <?php foreach ($events as $key => $event) : ?>
                                <tr>
                                    <td><?php echo esc_html($hook); ?></td>
                                    <td><?php echo date('Y-m-d H:i:s', $timestamp); ?></td>
                                    <td><?php echo esc_html($event['schedule'] ?? 'Single'); ?></td>
                                    <td><?php echo esc_html(json_encode($event['args'])); ?></td>
                                </tr>
                            <?php endforeach; ?>
                        <?php endforeach; ?>
                    <?php endforeach; ?>
                </tbody>
            </table>
            
            <h2>Cron Health Check</h2>
            <?php $this->display_health_check(); ?>
        </div>
        <?php
    }
    
    private function display_health_check() {
        $last_cron = get_option('_transient_doing_cron');
        $cron_disabled = defined('DISABLE_WP_CRON') && DISABLE_WP_CRON;
        
        echo '<div class="notice notice-info">';
        echo '<p><strong>WP Cron Status:</strong> ' . ($cron_disabled ? 'Disabled' : 'Enabled') . '</p>';
        echo '<p><strong>Last Cron Run:</strong> ' . ($last_cron ? date('Y-m-d H:i:s', $last_cron) : 'Never') . '</p>';
        echo '<p><strong>Server Time:</strong> ' . date('Y-m-d H:i:s') . '</p>';
        echo '</div>';
    }
}

new CronStatusDashboard();
```

## Best Practices

1. **Always clean up** scheduled events on plugin deactivation
2. **Use proper intervals** for different types of tasks
3. **Implement error handling** and retry logic
4. **Monitor cron health** regularly
5. **Use background processing** for heavy tasks
6. **Consider system cron** for critical tasks
7. **Log cron activities** for debugging
8. **Test cron jobs** in development
9. **Handle timezone** considerations
10. **Optimize database queries** in cron jobs

## Resources

- [WordPress Cron Documentation](https://developer.wordpress.org/plugins/cron/)
- [wp_schedule_event Documentation](https://developer.wordpress.org/reference/functions/wp_schedule_event/)
- [WordPress Background Processing](https://github.com/A5hleyRich/wp-background-processing)
"""



# WordPress Third-Party Integrations
@mcp.resource("wordpress://integrations/payment-gateways")
def get_payment_gateways() -> str:
    """WordPress Payment Gateway Integration - Stripe, PayPal, WooCommerce payments"""
    return """# WordPress Payment Gateway Integration

## Stripe Integration

### Basic Stripe Setup
```php
// Enqueue Stripe.js
function enqueue_stripe_scripts() {
    wp_enqueue_script('stripe-js', 'https://js.stripe.com/v3/', array(), null, true);
    wp_enqueue_script('stripe-custom', get_template_directory_uri() . '/js/stripe.js', array('stripe-js'), '1.0.0', true);
    
    wp_localize_script('stripe-custom', 'stripe_vars', array(
        'publishable_key' => get_option('stripe_publishable_key'),
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('stripe_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'enqueue_stripe_scripts');

// Handle Stripe payment
add_action('wp_ajax_process_stripe_payment', 'process_stripe_payment');
add_action('wp_ajax_nopriv_process_stripe_payment', 'process_stripe_payment');

function process_stripe_payment() {
    check_ajax_referer('stripe_nonce', 'nonce');
    
    require_once('stripe-php/init.php');
    
    \Stripe\Stripe::setApiKey(get_option('stripe_secret_key'));
    
    $amount = intval($_POST['amount']) * 100; // Convert to cents
    $currency = sanitize_text_field($_POST['currency']);
    
    try {
        $payment_intent = \Stripe\PaymentIntent::create([
            'amount' => $amount,
            'currency' => $currency,
            'metadata' => [
                'user_id' => get_current_user_id(),
                'order_id' => uniqid()
            ]
        ]);
        
        wp_send_json_success(array(
            'client_secret' => $payment_intent->client_secret
        ));
    } catch (Exception $e) {
        wp_send_json_error($e->getMessage());
    }
}
```

### Stripe Webhook Handler
```php
// Handle Stripe webhooks
add_action('wp_ajax_stripe_webhook', 'handle_stripe_webhook');
add_action('wp_ajax_nopriv_stripe_webhook', 'handle_stripe_webhook');

function handle_stripe_webhook() {
    $payload = file_get_contents('php://input');
    $sig_header = $_SERVER['HTTP_STRIPE_SIGNATURE'];
    $endpoint_secret = get_option('stripe_webhook_secret');
    
    try {
        $event = \Stripe\Webhook::constructEvent($payload, $sig_header, $endpoint_secret);
    } catch (Exception $e) {
        http_response_code(400);
        exit();
    }
    
    switch ($event->type) {
        case 'payment_intent.succeeded':
            $payment_intent = $event->data->object;
            handle_payment_success($payment_intent);
            break;
            
        case 'payment_intent.payment_failed':
            $payment_intent = $event->data->object;
            handle_payment_failure($payment_intent);
            break;
            
        default:
            error_log('Unhandled event type: ' . $event->type);
    }
    
    http_response_code(200);
}

function handle_payment_success($payment_intent) {
    $order_id = $payment_intent->metadata->order_id;
    $amount = $payment_intent->amount / 100;
    
    // Update order status
    update_post_meta($order_id, '_payment_status', 'completed');
    update_post_meta($order_id, '_payment_intent_id', $payment_intent->id);
    
    // Send confirmation email
    send_payment_confirmation_email($order_id);
}

function handle_payment_failure($payment_intent) {
    $order_id = $payment_intent->metadata->order_id;
    
    // Update order status
    update_post_meta($order_id, '_payment_status', 'failed');
    update_post_meta($order_id, '_payment_error', $payment_intent->last_payment_error->message);
}
```

## PayPal Integration

### PayPal REST API Integration
```php
class PayPalIntegration {
    private $client_id;
    private $client_secret;
    private $sandbox;
    
    public function __construct() {
        $this->client_id = get_option('paypal_client_id');
        $this->client_secret = get_option('paypal_client_secret');
        $this->sandbox = get_option('paypal_sandbox') === 'yes';
        
        add_action('wp_ajax_create_paypal_payment', array($this, 'create_payment'));
        add_action('wp_ajax_nopriv_create_paypal_payment', array($this, 'create_payment'));
        
        add_action('wp_ajax_execute_paypal_payment', array($this, 'execute_payment'));
        add_action('wp_ajax_nopriv_execute_paypal_payment', array($this, 'execute_payment'));
    }
    
    public function create_payment() {
        check_ajax_referer('paypal_nonce', 'nonce');
        
        $amount = floatval($_POST['amount']);
        $currency = sanitize_text_field($_POST['currency']);
        $return_url = esc_url($_POST['return_url']);
        $cancel_url = esc_url($_POST['cancel_url']);
        
        $access_token = $this->get_access_token();
        
        $payment_data = array(
            'intent' => 'sale',
            'redirect_urls' => array(
                'return_url' => $return_url,
                'cancel_url' => $cancel_url
            ),
            'payer' => array(
                'payment_method' => 'paypal'
            ),
            'transactions' => array(
                array(
                    'amount' => array(
                        'total' => number_format($amount, 2),
                        'currency' => strtoupper($currency)
                    ),
                    'description' => 'Payment for services'
                )
            )
        );
        
        $response = wp_remote_post($this->get_api_url() . '/v1/payments/payment', array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $access_token,
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode($payment_data)
        ));
        
        if (is_wp_error($response)) {
            wp_send_json_error('Failed to create payment');
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if (isset($data['links'])) {
            foreach ($data['links'] as $link) {
                if ($link['rel'] === 'approval_url') {
                    wp_send_json_success(array(
                        'approval_url' => $link['href'],
                        'payment_id' => $data['id']
                    ));
                }
            }
        }
        
        wp_send_json_error('Invalid response from PayPal');
    }
    
    public function execute_payment() {
        check_ajax_referer('paypal_nonce', 'nonce');
        
        $payment_id = sanitize_text_field($_POST['payment_id']);
        $payer_id = sanitize_text_field($_POST['payer_id']);
        
        $access_token = $this->get_access_token();
        
        $execute_data = array(
            'payer_id' => $payer_id
        );
        
        $response = wp_remote_post($this->get_api_url() . '/v1/payments/payment/' . $payment_id . '/execute', array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $access_token,
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode($execute_data)
        ));
        
        if (is_wp_error($response)) {
            wp_send_json_error('Failed to execute payment');
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if ($data['state'] === 'approved') {
            wp_send_json_success(array(
                'transaction_id' => $data['transactions'][0]['related_resources'][0]['sale']['id'],
                'amount' => $data['transactions'][0]['amount']['total']
            ));
        } else {
            wp_send_json_error('Payment not approved');
        }
    }
    
    private function get_access_token() {
        $response = wp_remote_post($this->get_api_url() . '/v1/oauth2/token', array(
            'headers' => array(
                'Accept' => 'application/json',
                'Accept-Language' => 'en_US',
                'Content-Type' => 'application/x-www-form-urlencoded'
            ),
            'body' => array(
                'grant_type' => 'client_credentials'
            ),
            'httpversion' => '1.1'
        ));
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        return $data['access_token'];
    }
    
    private function get_api_url() {
        return $this->sandbox ? 'https://api.sandbox.paypal.com' : 'https://api.paypal.com';
    }
}

new PayPalIntegration();
```

## Email Service Integration

### Mailchimp Integration
```php
class MailchimpIntegration {
    private $api_key;
    private $list_id;
    
    public function __construct() {
        $this->api_key = get_option('mailchimp_api_key');
        $this->list_id = get_option('mailchimp_list_id');
        
        add_action('wp_ajax_subscribe_to_mailchimp', array($this, 'subscribe_user'));
        add_action('wp_ajax_nopriv_subscribe_to_mailchimp', array($this, 'subscribe_user'));
    }
    
    public function subscribe_user() {
        check_ajax_referer('mailchimp_nonce', 'nonce');
        
        $email = sanitize_email($_POST['email']);
        $first_name = sanitize_text_field($_POST['first_name']);
        $last_name = sanitize_text_field($_POST['last_name']);
        
        if (!is_email($email)) {
            wp_send_json_error('Invalid email address');
        }
        
        $data_center = substr($this->api_key, strpos($this->api_key, '-') + 1);
        $url = 'https://' . $data_center . '.api.mailchimp.com/3.0/lists/' . $this->list_id . '/members';
        
        $member_data = array(
            'email_address' => $email,
            'status' => 'subscribed',
            'merge_fields' => array(
                'FNAME' => $first_name,
                'LNAME' => $last_name
            )
        );
        
        $response = wp_remote_post($url, array(
            'headers' => array(
                'Authorization' => 'Basic ' . base64_encode('user:' . $this->api_key),
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode($member_data)
        ));
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if (is_wp_error($response)) {
            wp_send_json_error('Failed to subscribe user');
        }
        
        if (isset($data['id'])) {
            wp_send_json_success('Successfully subscribed to newsletter');
        } else {
            wp_send_json_error($data['detail'] ?? 'Unknown error');
        }
    }
}
```

## Social Media Integration

### Twitter API Integration
```php
class TwitterIntegration {
    private $consumer_key;
    private $consumer_secret;
    private $access_token;
    private $access_token_secret;
    
    public function __construct() {
        $this->consumer_key = get_option('twitter_consumer_key');
        $this->consumer_secret = get_option('twitter_consumer_secret');
        $this->access_token = get_option('twitter_access_token');
        $this->access_token_secret = get_option('twitter_access_token_secret');
        
        add_action('publish_post', array($this, 'tweet_new_post'));
    }
    
    public function tweet_new_post($post_id) {
        $post = get_post($post_id);
        
        if ($post->post_status !== 'publish' || $post->post_type !== 'post') {
            return;
        }
        
        $title = $post->post_title;
        $permalink = get_permalink($post_id);
        
        // Shorten URL and create tweet
        $short_url = $this->shorten_url($permalink);
        $tweet_text = $title . ' ' . $short_url;
        
        // Ensure tweet is under 280 characters
        if (strlen($tweet_text) > 280) {
            $max_title_length = 280 - strlen($short_url) - 1;
            $title = substr($title, 0, $max_title_length - 3) . '...';
            $tweet_text = $title . ' ' . $short_url;
        }
        
        $this->post_tweet($tweet_text);
    }
    
    private function post_tweet($status) {
        require_once('twitteroauth/autoload.php');
        
        $connection = new \Abraham\TwitterOAuth\TwitterOAuth(
            $this->consumer_key,
            $this->consumer_secret,
            $this->access_token,
            $this->access_token_secret
        );
        
        $result = $connection->post('statuses/update', array('status' => $status));
        
        if ($connection->getLastHttpCode() === 200) {
            error_log('Tweet posted successfully: ' . $status);
        } else {
            error_log('Failed to post tweet: ' . json_encode($result));
        }
    }
    
    private function shorten_url($url) {
        // Use bit.ly or similar service to shorten URL
        $bitly_token = get_option('bitly_access_token');
        
        $response = wp_remote_post('https://api-ssl.bitly.com/v4/shorten', array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $bitly_token,
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode(array('long_url' => $url))
        ));
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        return $data['link'] ?? $url;
    }
}
```

## Best Practices

1. **Always validate and sanitize** input data
2. **Use HTTPS** for all API communications
3. **Store API keys securely** using WordPress options
4. **Implement proper error handling** and logging
5. **Use webhooks** for real-time updates
6. **Test in sandbox mode** before going live
7. **Follow rate limits** for API calls
8. **Cache API responses** when appropriate
9. **Use nonces** for security
10. **Document API integrations** thoroughly

## Resources

- [Stripe PHP Library](https://github.com/stripe/stripe-php)
- [PayPal REST API Documentation](https://developer.paypal.com/docs/api/)
- [Mailchimp API Documentation](https://mailchimp.com/developer/)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [WordPress HTTP API](https://developer.wordpress.org/reference/functions/wp_remote_post/)
"""


@mcp.resource("wordpress://integrations/analytics-tracking")
def get_analytics_tracking() -> str:
    """WordPress Analytics and Tracking Integration - Google Analytics, Facebook Pixel, custom tracking"""
    return """# WordPress Analytics and Tracking Integration

## Google Analytics 4 Integration

### Basic GA4 Setup
```php
function add_google_analytics() {
    $ga_measurement_id = get_option('ga_measurement_id');
    
    if (!$ga_measurement_id) {
        return;
    }
    ?>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($ga_measurement_id); ?>"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '<?php echo esc_attr($ga_measurement_id); ?>', {
            'custom_map': {
                'custom_parameter_1': 'user_type',
                'custom_parameter_2': 'post_category'
            }
        });
    </script>
    <?php
}
add_action('wp_head', 'add_google_analytics');
```

### Enhanced GA4 with Custom Events
```php
class GoogleAnalytics4 {
    private $measurement_id;
    
    public function __construct() {
        $this->measurement_id = get_option('ga_measurement_id');
        
        if ($this->measurement_id) {
            add_action('wp_head', array($this, 'add_ga4_script'));
            add_action('wp_footer', array($this, 'add_custom_events'));
            add_action('wp_enqueue_scripts', array($this, 'enqueue_analytics_scripts'));
        }
    }
    
    public function add_ga4_script() {
        ?>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($this->measurement_id); ?>"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '<?php echo esc_attr($this->measurement_id); ?>', {
                'send_page_view': false
            });
            
            // Enhanced ecommerce
            gtag('config', '<?php echo esc_attr($this->measurement_id); ?>', {
                'custom_map': {
                    'custom_parameter_1': 'user_type',
                    'custom_parameter_2': 'content_category'
                }
            });
        </script>
        <?php
    }
    
    public function enqueue_analytics_scripts() {
        wp_enqueue_script('ga4-custom', get_template_directory_uri() . '/js/ga4-custom.js', array(), '1.0.0', true);
        
        wp_localize_script('ga4-custom', 'ga4_vars', array(
            'measurement_id' => $this->measurement_id,
            'user_type' => $this->get_user_type(),
            'content_category' => $this->get_content_category()
        ));
    }
    
    public function add_custom_events() {
        ?>
        <script>
        // Track page views
        gtag('event', 'page_view', {
            page_title: document.title,
            page_location: window.location.href,
            user_type: '<?php echo esc_js($this->get_user_type()); ?>',
            content_category: '<?php echo esc_js($this->get_content_category()); ?>'
        });
        
        // Track custom events
        document.addEventListener('DOMContentLoaded', function() {
            // Track newsletter signup
            const newsletterForm = document.getElementById('newsletter-form');
            if (newsletterForm) {
                newsletterForm.addEventListener('submit', function() {
                    gtag('event', 'newsletter_signup', {
                        event_category: 'engagement',
                        event_label: 'footer_newsletter'
                    });
                });
            }
            
            // Track file downloads
            const downloadLinks = document.querySelectorAll('a[href$=".pdf"], a[href$=".zip"], a[href$=".doc"]');
            downloadLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    gtag('event', 'file_download', {
                        event_category: 'engagement',
                        event_label: this.href.split('/').pop(),
                        value: 1
                    });
                });
            });
            
            // Track video plays
            const videos = document.querySelectorAll('video');
            videos.forEach(function(video) {
                video.addEventListener('play', function() {
                    gtag('event', 'video_play', {
                        event_category: 'engagement',
                        event_label: this.src.split('/').pop()
                    });
                });
            });
        });
        </script>
        <?php
    }
    
    private function get_user_type() {
        if (is_user_logged_in()) {
            $user = wp_get_current_user();
            return in_array('administrator', $user->roles) ? 'admin' : 'logged_in';
        }
        return 'guest';
    }
    
    private function get_content_category() {
        if (is_single()) {
            $categories = get_the_category();
            return !empty($categories) ? $categories[0]->name : 'uncategorized';
        } elseif (is_page()) {
            return 'page';
        } elseif (is_home()) {
            return 'blog';
        }
        return 'other';
    }
}

new GoogleAnalytics4();
```

## Facebook Pixel Integration

### Basic Facebook Pixel Setup
```php
function add_facebook_pixel() {
    $pixel_id = get_option('facebook_pixel_id');
    
    if (!$pixel_id) {
        return;
    }
    ?>
    <!-- Facebook Pixel Code -->
    <script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '<?php echo esc_js($pixel_id); ?>');
    fbq('track', 'PageView');
    </script>
    <noscript>
        <img height="1" width="1" style="display:none"
             src="https://www.facebook.com/tr?id=<?php echo esc_attr($pixel_id); ?>&ev=PageView&noscript=1" />
    </noscript>
    <!-- End Facebook Pixel Code -->
    <?php
}
add_action('wp_head', 'add_facebook_pixel');
```

### Enhanced Facebook Pixel with Custom Events
```php
class FacebookPixelIntegration {
    private $pixel_id;
    
    public function __construct() {
        $this->pixel_id = get_option('facebook_pixel_id');
        
        if ($this->pixel_id) {
            add_action('wp_head', array($this, 'add_pixel_code'));
            add_action('wp_footer', array($this, 'add_custom_events'));
        }
    }
    
    public function add_pixel_code() {
        ?>
        <!-- Facebook Pixel Code -->
        <script>
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '<?php echo esc_js($this->pixel_id); ?>');
        fbq('track', 'PageView');
        </script>
        <noscript>
            <img height="1" width="1" style="display:none"
                 src="https://www.facebook.com/tr?id=<?php echo esc_attr($this->pixel_id); ?>&ev=PageView&noscript=1" />
        </noscript>
        <?php
    }
    
    public function add_custom_events() {
        ?>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Track newsletter signup
            const newsletterForm = document.getElementById('newsletter-form');
            if (newsletterForm) {
                newsletterForm.addEventListener('submit', function() {
                    fbq('track', 'Lead', {
                        content_name: 'Newsletter Signup',
                        content_category: 'Email'
                    });
                });
            }
            
            // Track contact form submissions
            const contactForms = document.querySelectorAll('.contact-form, .wpcf7-form');
            contactForms.forEach(function(form) {
                form.addEventListener('submit', function() {
                    fbq('track', 'Lead', {
                        content_name: 'Contact Form',
                        content_category: 'Contact'
                    });
                });
            });
            
            // Track button clicks
            const ctaButtons = document.querySelectorAll('.cta-button, .btn-primary');
            ctaButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    fbq('track', 'ViewContent', {
                        content_name: this.textContent.trim(),
                        content_category: 'CTA'
                    });
                });
            });
        });
        </script>
        <?php
    }
}

new FacebookPixelIntegration();
```

## Custom Analytics Dashboard

### WordPress Analytics Dashboard
```php
class WordPressAnalyticsDashboard {
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('wp_dashboard_setup', array($this, 'add_dashboard_widget'));
    }
    
    public function add_admin_menu() {
        add_dashboard_page(
            'Analytics Dashboard',
            'Analytics',
            'manage_options',
            'analytics-dashboard',
            array($this, 'display_dashboard')
        );
    }
    
    public function add_dashboard_widget() {
        wp_add_dashboard_widget(
            'analytics_widget',
            'Site Analytics',
            array($this, 'display_dashboard_widget')
        );
    }
    
    public function display_dashboard() {
        ?>
        <div class="wrap">
            <h1>Analytics Dashboard</h1>
            
            <div class="analytics-grid">
                <div class="analytics-card">
                    <h3>Page Views (Last 30 Days)</h3>
                    <div class="analytics-number"><?php echo $this->get_page_views(); ?></div>
                </div>
                
                <div class="analytics-card">
                    <h3>Unique Visitors</h3>
                    <div class="analytics-number"><?php echo $this->get_unique_visitors(); ?></div>
                </div>
                
                <div class="analytics-card">
                    <h3>Top Pages</h3>
                    <ul>
                        <?php foreach ($this->get_top_pages() as $page) : ?>
                            <li><?php echo esc_html($page['title']); ?> (<?php echo $page['views']; ?>)</li>
                        <?php endforeach; ?>
                    </ul>
                </div>
                
                <div class="analytics-card">
                    <h3>Traffic Sources</h3>
                    <ul>
                        <?php foreach ($this->get_traffic_sources() as $source) : ?>
                            <li><?php echo esc_html($source['name']); ?> (<?php echo $source['percentage']; ?>%)</li>
                        <?php endforeach; ?>
                    </ul>
                </div>
            </div>
        </div>
        
        <style>
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .analytics-card {
            background: white;
            padding: 20px;
            border: 1px solid #ccd0d4;
            border-radius: 4px;
        }
        .analytics-number {
            font-size: 2em;
            font-weight: bold;
            color: #0073aa;
        }
        </style>
        <?php
    }
    
    private function get_page_views() {
        global $wpdb;
        
        $result = $wpdb->get_var("
            SELECT SUM(meta_value) 
            FROM {$wpdb->postmeta} 
            WHERE meta_key = '_page_views' 
            AND post_id IN (
                SELECT post_id 
                FROM {$wpdb->postmeta} 
                WHERE meta_key = '_page_views_date' 
                AND meta_value >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            )
        ");
        
        return $result ?: 0;
    }
    
    private function get_unique_visitors() {
        // Implementation for unique visitors tracking
        return 0;
    }
    
    private function get_top_pages() {
        global $wpdb;
        
        $results = $wpdb->get_results("
            SELECT p.post_title as title, pm.meta_value as views
            FROM {$wpdb->posts} p
            JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id
            WHERE pm.meta_key = '_page_views'
            AND p.post_status = 'publish'
            ORDER BY CAST(pm.meta_value AS UNSIGNED) DESC
            LIMIT 5
        ");
        
        return $results ?: array();
    }
    
    private function get_traffic_sources() {
        // Implementation for traffic sources
        return array(
            array('name' => 'Direct', 'percentage' => 45),
            array('name' => 'Google', 'percentage' => 30),
            array('name' => 'Social Media', 'percentage' => 15),
            array('name' => 'Other', 'percentage' => 10)
        );
    }
}

new WordPressAnalyticsDashboard();
```

## Best Practices

1. **Respect user privacy** and GDPR compliance
2. **Use proper data sanitization** for all tracking data
3. **Implement cookie consent** mechanisms
4. **Test tracking implementations** thoroughly
5. **Use Google Tag Manager** for complex setups
6. **Monitor tracking accuracy** regularly
7. **Implement error handling** for failed tracking
8. **Use server-side tracking** for critical events
9. **Document tracking implementations** clearly
10. **Regularly audit tracking** for accuracy

## Resources

- [Google Analytics 4 Documentation](https://developers.google.com/analytics/devguides/collection/ga4)
- [Facebook Pixel Documentation](https://developers.facebook.com/docs/facebook-pixel/)
- [Google Tag Manager Documentation](https://developers.google.com/tag-manager)
- [WordPress Privacy and GDPR](https://developer.wordpress.org/plugins/privacy/)
"""



# WordPress Development Workflows
@mcp.resource("wordpress://workflows/development-workflow")
def get_development_workflow() -> str:
    """WordPress Development Workflow - Git, deployment, testing, and automation best practices"""
    return """# WordPress Development Workflow

## Git Workflow for WordPress

### Branching Strategy
```bash
# Main branches
main                    # Production-ready code
develop                 # Integration branch for features
release/*              # Release preparation branches
feature/*              # Feature development branches
hotfix/*               # Critical bug fixes
bugfix/*               # Bug fixes

# Example workflow
git checkout develop
git pull origin develop
git checkout -b feature/new-plugin-feature
# ... develop feature ...
git add .
git commit -m "Add new plugin feature"
git push origin feature/new-plugin-feature
# Create pull request to develop
```

### WordPress-Specific Git Configuration
```bash
# .gitignore for WordPress
# WordPress core files
/wp-admin/
/wp-includes/
/wp-*.php
/xmlrpc.php
/readme.html
/license.txt

# WordPress uploads
/wp-content/uploads/

# WordPress cache
/wp-content/cache/

# WordPress config
/wp-config.php
/.htaccess

# Dependencies
/node_modules/
/vendor/
/composer.lock

# IDE files
/.vscode/
/.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
error_log
debug.log
```

## Development Environment Setup

### Docker WordPress Development
```dockerfile
# Dockerfile
FROM wordpress:latest

# Install additional PHP extensions
RUN docker-php-ext-install mysqli pdo_mysql

# Install Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

# Copy custom configuration
COPY docker/php.ini /usr/local/etc/php/conf.d/custom.ini
COPY docker/000-default.conf /etc/apache2/sites-available/000-default.conf

# Install WordPress CLI
RUN curl -O https://raw.githubusercontent.com/wp-cli/wp-cli/master/php/wp-cli.phar
RUN chmod +x wp-cli.phar
RUN mv wp-cli.phar /usr/local/bin/wp
```

### Docker Compose Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  wordpress:
    build: .
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - ./wp-content:/var/www/html/wp-content
      - ./wp-config.php:/var/www/html/wp-config.php
    depends_on:
      - db

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - db_data:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    ports:
      - "8081:80"
    environment:
      PMA_HOST: db
    depends_on:
      - db

volumes:
  db_data:
```

## Automated Testing Workflow

### PHPUnit Testing Setup
```php
// tests/bootstrap.php
<?php
/**
 * PHPUnit bootstrap file for WordPress plugin testing
 */

// Load WordPress test environment
$_tests_dir = getenv('WP_TESTS_DIR');

if (!$_tests_dir) {
    $_tests_dir = rtrim(sys_get_temp_dir(), '/\\') . '/wordpress-tests-lib';
}

if (!file_exists($_tests_dir . '/includes/functions.php')) {
    echo "Could not find $_tests_dir/includes/functions.php, have you run bin/install-wp-tests.sh ?" . PHP_EOL;
    exit(1);
}

require_once $_tests_dir . '/includes/functions.php';

function _manually_load_plugin() {
    require dirname(dirname(__FILE__)) . '/your-plugin.php';
}
tests_add_filter('muplugins_loaded', '_manually_load_plugin');

require $_tests_dir . '/includes/bootstrap.php';
```

### Test Case Example
```php
// tests/test-plugin.php
<?php
/**
 * Test cases for WordPress plugin
 */

class TestPlugin extends WP_UnitTestCase {
    
    public function setUp() {
        parent::setUp();
        $this->plugin = new YourPlugin();
    }
    
    public function test_plugin_activation() {
        $this->assertTrue(is_plugin_active('your-plugin/your-plugin.php'));
    }
    
    public function test_database_tables_created() {
        global $wpdb;
        
        $table_name = $wpdb->prefix . 'your_table';
        $this->assertNotFalse($wpdb->get_var("SHOW TABLES LIKE '$table_name'"));
    }
    
    public function test_custom_post_type_registration() {
        $post_types = get_post_types();
        $this->assertArrayHasKey('your_post_type', $post_types);
    }
    
    public function test_shortcode_registration() {
        global $shortcode_tags;
        $this->assertArrayHasKey('your_shortcode', $shortcode_tags);
    }
    
    public function test_shortcode_output() {
        $output = do_shortcode('[your_shortcode]');
        $this->assertContains('expected_output', $output);
    }
}
```

### Automated Testing Script
```bash
#!/bin/bash
# scripts/run-tests.sh

echo "Starting WordPress plugin tests..."

# Install WordPress test environment
bash bin/install-wp-tests.sh wordpress_test root '' localhost latest

# Run PHPUnit tests
vendor/bin/phpunit

# Run PHPCS (PHP CodeSniffer)
vendor/bin/phpcs --standard=WordPress .

# Run PHPStan (Static analysis)
vendor/bin/phpstan analyse

echo "Tests completed!"
```

## Deployment Workflow

### GitHub Actions for WordPress
```yaml
# .github/workflows/deploy.yml
name: Deploy WordPress Plugin

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.1'
        extensions: mbstring, xml, ctype, iconv, intl, pdo_mysql
        
    - name: Setup WordPress
      run: |
        bash bin/install-wp-tests.sh wordpress_test root '' localhost latest
        
    - name: Install dependencies
      run: composer install --prefer-dist --no-progress
      
    - name: Run tests
      run: vendor/bin/phpunit
      
    - name: Run PHPCS
      run: vendor/bin/phpcs --standard=WordPress .
      
    - name: Run PHPStan
      run: vendor/bin/phpstan analyse

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to staging
      run: |
        rsync -avz --delete \
          --exclude='.git' \
          --exclude='node_modules' \
          --exclude='vendor' \
          ./ user@staging-server:/var/www/html/wp-content/plugins/your-plugin/
          
    - name: Run database migrations
      run: |
        ssh user@staging-server "cd /var/www/html && wp plugin activate your-plugin"
```

### WP-CLI Deployment Script
```bash
#!/bin/bash
# scripts/deploy.sh

echo "Deploying WordPress plugin..."

# Set deployment variables
PLUGIN_DIR="/var/www/html/wp-content/plugins/your-plugin"
BACKUP_DIR="/var/www/html/wp-content/backups/$(date +%Y%m%d_%H%M%S)"

# Create backup
echo "Creating backup..."
mkdir -p $BACKUP_DIR
cp -r $PLUGIN_DIR $BACKUP_DIR/

# Deploy new version
echo "Deploying new version..."
rsync -avz --delete \
  --exclude='.git' \
  --exclude='node_modules' \
  --exclude='vendor' \
  ./ $PLUGIN_DIR/

# Activate plugin
echo "Activating plugin..."
cd /var/www/html
wp plugin activate your-plugin

# Run database migrations
echo "Running migrations..."
wp plugin activate your-plugin --activate-network

# Clear caches
echo "Clearing caches..."
wp cache flush
wp rewrite flush

echo "Deployment completed!"
```

## Code Quality Workflow

### Pre-commit Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running pre-commit checks..."

# Run PHPCS
vendor/bin/phpcs --standard=WordPress .
if [ $? -ne 0 ]; then
    echo "PHPCS failed. Please fix coding standards issues."
    exit 1
fi

# Run PHPStan
vendor/bin/phpstan analyse
if [ $? -ne 0 ]; then
    echo "PHPStan failed. Please fix static analysis issues."
    exit 1
fi

# Run tests
vendor/bin/phpunit
if [ $? -ne 0 ]; then
    echo "Tests failed. Please fix failing tests."
    exit 1
fi

echo "All pre-commit checks passed!"
```

### Composer Scripts
```json
{
    "scripts": {
        "test": "vendor/bin/phpunit",
        "test:coverage": "vendor/bin/phpunit --coverage-html coverage",
        "cs": "vendor/bin/phpcs --standard=WordPress .",
        "cs:fix": "vendor/bin/phpcbf --standard=WordPress .",
        "stan": "vendor/bin/phpstan analyse",
        "quality": [
            "@cs",
            "@stan",
            "@test"
        ],
        "build": [
            "composer install --no-dev --optimize-autoloader",
            "npm run build"
        ]
    }
}
```

## Best Practices

1. **Use version control** for all code and configurations
2. **Implement automated testing** for all features
3. **Follow WordPress coding standards** consistently
4. **Use dependency management** (Composer, npm)
5. **Implement CI/CD pipelines** for automated deployment
6. **Use staging environments** for testing
7. **Document all workflows** and processes
8. **Implement code reviews** for all changes
9. **Use feature branches** for development
10. **Regularly update dependencies** and WordPress core

## Resources

- [WordPress Plugin Development Handbook](https://developer.wordpress.org/plugins/)
- [Git Flow Workflow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Docker WordPress Development](https://docs.docker.com/samples/wordpress/)
- [GitHub Actions for WordPress](https://github.com/features/actions)
- [WP-CLI Documentation](https://wp-cli.org/)
"""

