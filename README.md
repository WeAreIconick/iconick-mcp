# WordPress Development MCP Server

A comprehensive Model Context Protocol (MCP) server providing extensive WordPress development resources, tools, and guided workflows for AI assistants.

## 🚀 Current Features (v2.1.0)

- **81 WordPress Development Resources** across 20+ categories
- **8 Powerful Tools** for WordPress management and automation
- **15 Guided Workflow Prompts** for complex development tasks
- **62 Code Snippets** with metadata and examples
- **WordPress Playground Blueprint Generator** for instant WordPress environments
- **Advanced Search & Filtering** across all resources and snippets
- **Enterprise-grade Security** with comprehensive validation
- **Production Ready** with version tracking and health monitoring

## 📊 Server Statistics

- **Total Resources**: 81 comprehensive WordPress development resources
- **Management Tools**: 8 tools for WordPress operations
- **Workflow Prompts**: 15 guided development workflows
- **Code Snippets**: 62 ready-to-use code examples
- **Total Files**: 146 files in the resource library
- **Categories**: 20+ organized categories covering all WordPress development areas
- **Security Level**: Enterprise-grade with advanced features
- **Performance**: Optimized for fast access with caching
- **Status**: Production ready and deployed

## 🏗️ Architecture

This server uses FastMCP with comprehensive WordPress development capabilities:

```
FastMCP Server (wordpress_mcp.py)
├── 81 Resources (documentation + catalog)
├── 8 Tools (management + search + blueprints)
├── 15 Prompts (guided workflows)
├── 62 Code Snippets (with metadata)
└── Version Tracking & Health Monitoring
```

### Key Components:

1. **FastMCP Server** (`wordpress_mcp.py`) - Main server with all capabilities
2. **Resource Library** (`resources/`) - 81 WordPress development resources
3. **Code Snippets** (`resources/snippets/`) - 62 categorized code examples
4. **Management Tools** - WordPress installation, plugin/theme management, database operations
5. **Search & Filtering** - Advanced resource and snippet discovery
6. **Blueprint Generator** - WordPress Playground environment creation

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python wordpress_mcp.py
```

### Connect Your AI Assistant

Connect to the MCP server endpoint:
```
http://localhost:8000/mcp/
```

## 🛠️ Available Tools

### WordPress Management Tools

1. **WordPress Installer** (`wordpress_installer`)
   - Install WordPress with custom configuration
   - Set up database, admin user, and site settings
   - Install plugins and themes during setup

2. **Plugin Manager** (`plugin_manager`)
   - Install, activate, deactivate plugins
   - Search WordPress repository
   - Bulk operations and status management

3. **Theme Customizer** (`theme_customizer`)
   - Install, activate themes
   - Create child themes
   - Customize theme settings

4. **Database Manager** (`database_manager`)
   - Backup and restore databases
   - Run SQL queries
   - Search and replace operations
   - Database optimization

5. **Backup Tool** (`backup_tool`)
   - Create full site backups
   - Restore from backups
   - Compress and manage backup files

### Advanced Tools

6. **Resource Search** (`search_resources`)
   - Search WordPress documentation by query, difficulty, tag, category
   - Filter by complexity level and use case
   - Find related resources

7. **Snippet Search** (`search_snippets`)
   - Search code snippets by query, difficulty, tag, category
   - Filter by complexity and use case
   - Get ready-to-use code examples

8. **Playground Blueprint Generator** (`generate_playground_blueprint`)
   - Generate WordPress Playground blueprints
   - Support for basic, plugin-dev, theme-dev, woocommerce, multisite setups
   - Custom file creation and PHP code execution
   - Plugin/theme installation with auto URL generation

## 📚 Resource Categories

### Core WordPress APIs (9 resources)
- Database API (wpdb) - Queries, prepared statements, custom tables
- HTTP API - wp_remote_get/post, handling responses, error handling
- Options API - get_option, update_option, autoload management
- Transients API - Caching with TTL, performance optimization
- Rewrite API - Custom URLs, permalinks, rewrite rules
- Settings API - register_setting, sections, fields
- Shortcode API - Creating secure shortcodes
- Metadata API - Custom fields, meta boxes, data management
- Filesystem API - WP_Filesystem operations, file handling

### Security & Best Practices (6 resources)
- Data Validation - Input validation and sanitization
- Data Sanitization - sanitize_text_field, wp_kses, and more
- Output Escaping - esc_html, esc_attr, esc_url, esc_js
- Nonces - Creating, verifying, AJAX nonces, CSRF protection
- User Capabilities - current_user_can, role management
- SQL Injection Prevention - Prepared statements, $wpdb->prepare

### Block Editor Development (7 resources)
- Block Registration - Complete block setup and configuration
- Block Components - React components and hooks
- Dynamic Blocks - Server-side rendering
- Block Patterns - Reusable layouts and designs
- InnerBlocks - Nested block structures
- Block Transforms - Converting between block types
- WordPress Packages - @wordpress packages and utilities

### Theme Development (8 resources)
- Template Hierarchy - WordPress template loading order
- Template Tags - Functions for theme development
- theme.json - Modern theme configuration
- Block Themes - Full-site editing themes
- Child Themes - Parent/child theme relationships
- Navigation Menus - Menu registration and display
- Sidebars & Widgets - Widget areas and custom widgets
- Post Thumbnails - Featured image management

### REST API Development (5 resources)
- REST API Basics - Endpoint structure and concepts
- Custom Endpoints - Creating custom REST endpoints
- Authentication - Application passwords, OAuth, JWT
- Schema Definition - Request/response schemas
- API Extensions - Extending existing endpoints

### Coding Standards (5 resources)
- PHP Coding Standards - WordPress PHP formatting and conventions
- JavaScript Standards - Modern JavaScript and React patterns
- CSS Coding Standards - WordPress CSS best practices
- HTML Coding Standards - Semantic HTML and accessibility
- SQL Best Practices - Database query optimization
- Accessibility Standards - WCAG compliance and best practices

### Development Tools (4 resources)
- WP_DEBUG System - Debugging WordPress applications
- Query Monitor - Database query analysis
- WP-CLI - Command-line WordPress management
- Plugin Check - Plugin compatibility and standards

### Advanced Topics (9 resources)
- Custom Post Types - Registration and management
- WordPress Hooks - Actions and filters
- Multisite Development - Network administration
- WooCommerce Development - E-commerce customization
- Performance Optimization - Speed and efficiency
- Enterprise Architecture - Large-scale deployments
- Scaling Strategies - High-traffic solutions
- Advanced Caching - Object caching and CDN
- Database Optimization - Query performance

### WordPress Playground (1 resource)
- Blueprint Documentation - Complete guide to WordPress Playground blueprints

## 🎯 Guided Workflow Prompts

### Development Workflows (15 prompts)

1. **Plugin Development** - Complete plugin creation workflow
2. **Theme Development** - Modern theme development process
3. **Custom Post Types** - CPT registration and management
4. **Security Implementation** - Security-first development approach
5. **Performance Optimization** - Speed and efficiency improvements
6. **WooCommerce Development** - E-commerce customization
7. **Gutenberg Block Development** - Modern block creation with React
8. **REST API Development** - Custom API endpoint creation
9. **Multisite Development** - Network administration
10. **Database Optimization** - Query performance and efficiency
11. **Accessibility Compliance** - WCAG standards implementation
12. **Deployment Workflow** - Production deployment process
13. **Troubleshooting Guide** - Debugging and problem resolution
14. **Migration Workflow** - Site migration and data transfer
15. **Security Hardening** - Advanced security implementation

## 🔍 Search & Discovery

### Resource Search
- **By Query**: Search documentation content
- **By Difficulty**: Beginner, Intermediate, Advanced
- **By Tag**: Security, Performance, API, etc.
- **By Category**: Core, Themes, Plugins, etc.

### Snippet Search
- **By Query**: Search code examples
- **By Difficulty**: Complexity level filtering
- **By Tag**: Specific functionality tags
- **By Category**: Organized by WordPress area

## 🎮 WordPress Playground Integration

### Blueprint Types Supported
- **Basic** - Standard WordPress installation
- **Plugin Development** - Development environment with tools
- **Theme Development** - Theme creation environment
- **WooCommerce** - E-commerce development setup
- **Multisite** - Network installation
- **Custom** - Fully customizable configuration

### Features
- **Dynamic Plugin/Theme Installation** - Auto URL generation
- **Custom File Creation** - PHP, CSS, JS files
- **PHP Code Execution** - Run custom PHP code
- **Networking Support** - External API access
- **PHP Extensions** - Required extensions included

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Customize server settings
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8000
export LOG_LEVEL=info
```

### Server Status & Health

The server includes built-in monitoring:

- **Version Tracking** - Current version and change history
- **Health Checks** - Syntax validation and integrity checks
- **Statistics** - Real-time server metrics
- **Change Log** - Detailed update history

## 🛡️ Security Features

- **Input Validation** - Multi-layer validation and sanitization
- **Rate Limiting** - Configurable per-client limits
- **Authentication** - Secure WordPress integration
- **Threat Detection** - Suspicious activity monitoring
- **Audit Logging** - Comprehensive security event tracking
- **Error Handling** - Secure error responses without information leakage

## 🎯 Usage Examples

### For AI Assistants

Connect to the MCP server and access resources:

```python
# Example MCP client connection
async with Client("http://your-server.com/mcp/") as client:
    # Search for resources
    resources = await client.call_tool("search_resources", {
        "query": "security",
        "difficulty": "Intermediate"
    })
    
    # Generate WordPress Playground blueprint
    blueprint = await client.call_tool("generate_playground_blueprint", {
        "blueprint_type": "plugin-dev",
        "plugins": ["query-monitor", "debug-bar"]
    })
    
    # Access WordPress documentation
    db_docs = await client.read_resource("wordpress://core/database")
```

### For Developers

Access resources by category:

- **Core APIs**: `wordpress://core/*`
- **Security**: `wordpress://security/*`
- **Themes**: `wordpress://themes/*`
- **Blocks**: `wordpress://blocks/*`
- **REST API**: `wordpress://rest-api/*`
- **Advanced**: `wordpress://advanced/*`
- **Snippets**: `wordpress://snippets/{category}/{topic}`

## 📈 Performance

- **Response Time**: < 200ms for all resources
- **Cache Hit Rate**: Target > 80%
- **Error Rate**: < 1%
- **Uptime**: 99.9% availability target
- **Concurrent Users**: Supports multiple simultaneous connections

## 🔄 Updates & Version Management

### Current Version: 2.1.0 (2025-01-27)

**Recent Updates:**
- ✅ Added WordPress Playground Blueprint Generator
- ✅ Comprehensive blueprint templates (6 types)
- ✅ Dynamic plugin/theme installation
- ✅ Custom file creation and PHP execution
- ✅ Advanced search and filtering
- ✅ Metadata-rich resource organization
- ✅ 62 code snippets with examples
- ✅ 15 guided workflow prompts

### Change Tracking

The server includes comprehensive change tracking:
- **Version History** - Complete change log
- **Feature Tracking** - New capabilities and improvements
- **Statistics** - Real-time metrics and counts
- **Health Monitoring** - Automated integrity checks

## 📞 Support & Documentation

- **Comprehensive Documentation** - All resources include detailed examples
- **Health Monitoring** - Built-in health check and status tools
- **Error Logging** - Detailed error tracking and reporting
- **Performance Metrics** - Real-time performance monitoring
- **Change Log** - Complete version history and updates

## 🏆 Production Status

✅ **Fully Deployed** - Live and operational  
✅ **81 Resources** - Complete WordPress development coverage  
✅ **8 Tools** - Comprehensive WordPress management  
✅ **15 Prompts** - Guided development workflows  
✅ **62 Snippets** - Ready-to-use code examples  
✅ **Enterprise Security** - Production-grade security features  
✅ **Performance Optimized** - Fast response times and caching  
✅ **Version Tracking** - Complete change management  

## 📄 License

This project is open source and available under the MIT License.

---

**WordPress Development MCP Server v2.1.0** - The most comprehensive WordPress development resource hub for AI assistants, featuring 81 resources, 8 tools, 15 guided workflows, and 62 code snippets.