# Available WordPress Resources

Complete list of all MCP resources available in the Iconick MCP server.

## 📋 Resource URI Format

```
wordpress://{category}/{topic}
```

## 🎯 Currently Available Resources

### Core WordPress APIs

| Resource URI | Description |
|--------------|-------------|
| `wordpress://core/database` | WordPress Database API (wpdb) - Queries, prepared statements, custom tables |
| `wordpress://core/http` | WordPress HTTP API - wp_remote_get/post, handling responses, error handling |

### Security Best Practices  

| Resource URI | Description |
|--------------|-------------|
| `wordpress://security/data-validation` | WordPress Data Validation - Validating all input data |
| `wordpress://security/sanitization` | WordPress Data Sanitization - sanitize_text_field, wp_kses, and more |
| `wordpress://security/escaping` | WordPress Output Escaping - esc_html, esc_attr, esc_url, esc_js |
| `wordpress://security/nonces` | WordPress Nonces - Creating, verifying, AJAX nonces, CSRF protection |
| `wordpress://security/capabilities` | WordPress User Capabilities - current_user_can, role management |
| `wordpress://security/sql-injection` | WordPress SQL Injection Prevention - Prepared statements, $wpdb->prepare |

### Coding Standards

| Resource URI | Description |
|--------------|-------------|
| `wordpress://standards/php` | WordPress PHP Coding Standards - Formatting, naming conventions, PHPCS |
| `wordpress://standards/javascript` | WordPress JavaScript Coding Standards - ESLint, modern JS, React |

### Hooks & Filters

| Resource URI | Description |
|--------------|-------------|
| `wordpress://hooks/actions` | WordPress Action Hooks - Common actions with examples |

### Plugin Development

| Resource URI | Description |
|--------------|-------------|
| `wordpress://plugins/structure` | WordPress Plugin Structure - File organization, naming conventions, best practices |

### Code Examples

| Resource URI | Description |
|--------------|-------------|
| `wordpress://examples/custom-post-types` | WordPress Custom Post Types - Complete registration and query examples |

## 🚧 Planned Resources (Categories Ready)

The following resource categories are available and ready for expansion:

### Core APIs (Planned)
- `wordpress://core/options` - Options API
- `wordpress://core/transients` - Transients API
- `wordpress://core/rewrite` - Rewrite API
- `wordpress://core/settings` - Settings API
- `wordpress://core/shortcode` - Shortcode API
- `wordpress://core/metadata` - Metadata API
- `wordpress://core/filesystem` - Filesystem API
- `wordpress://core/cron` - Cron API
- `wordpress://core/cache` - Cache API

### Theme Development (Planned)
- `wordpress://themes/template-hierarchy` - Template hierarchy
- `wordpress://themes/template-tags` - Template tags
- `wordpress://themes/theme-json` - theme.json configuration
- `wordpress://themes/block-themes` - Block themes
- `wordpress://themes/child-themes` - Child themes

### Block Development (Planned)
- `wordpress://blocks/registration` - Block registration
- `wordpress://blocks/attributes` - Block attributes
- `wordpress://blocks/dynamic` - Dynamic blocks
- `wordpress://blocks/patterns` - Block patterns

### REST API (Planned)
- `wordpress://rest-api/custom-endpoints` - Custom endpoints
- `wordpress://rest-api/authentication` - Authentication
- `wordpress://rest-api/schema` - Schema definition

### Performance (Planned)
- `wordpress://performance/caching` - Caching strategies
- `wordpress://performance/optimization` - Database and asset optimization

### Testing (Planned)
- `wordpress://testing/phpunit` - PHPUnit testing
- `wordpress://testing/e2e` - End-to-end testing

### Accessibility (Planned)
- `wordpress://accessibility/wcag` - WCAG compliance
- `wordpress://accessibility/keyboard-navigation` - Keyboard navigation

### Internationalization (Planned)
- `wordpress://i18n/text-domains` - Text domains
- `wordpress://i18n/translation-functions` - Translation functions

### Database Operations (Planned)
- `wordpress://database/wpdb` - wpdb class usage
- `wordpress://database/custom-tables` - Custom tables

### Additional Examples (Planned)
- `wordpress://examples/custom-taxonomies` - Custom taxonomies
- `wordpress://examples/meta-boxes` - Meta boxes
- `wordpress://examples/widgets` - Widgets

## 🔍 How to Use

### In Claude Desktop

Once connected, ask Claude:
- "Show me the WordPress database API documentation"
- "How do I sanitize user input in WordPress?"
- "What are WordPress nonces and how do I use them?"
- "Give me examples of custom post types"

Claude will automatically fetch the relevant resources.

### In Cursor

The resources are available when writing WordPress code. Cursor will use them for context-aware suggestions.

## 📝 Adding New Resources

See `CONTRIBUTING.md` for guidelines on adding new resources.

### Quick Steps:

1. Create markdown file: `resources/{category}/{topic}.md`
2. Add endpoint in `wordpress_mcp.py`:
   ```python
   @mcp.resource("wordpress://{category}/{topic}")
   def get_{topic}() -> str:
       """Description"""
       return load_resource_content("{category}", "{topic}")
   ```
3. Test and commit

## 📚 Official Documentation Sources

Resources are curated from:
- [WordPress Developer Handbook](https://developer.wordpress.org/)
- [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/)
- [WordPress Core GitHub](https://github.com/WordPress/WordPress)
- [Plugin Handbook](https://developer.wordpress.org/plugins/)
- [Theme Handbook](https://developer.wordpress.org/themes/)
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)

## 🔄 Update Schedule

Resources are automatically updated weekly via GitHub Actions, fetching the latest documentation from official WordPress sources.

---

**Last Updated**: October 14, 2025  
**Total Active Resources**: 13  
**Total Categories**: 17
