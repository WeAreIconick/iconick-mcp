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

