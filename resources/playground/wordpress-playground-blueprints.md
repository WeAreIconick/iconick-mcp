---
difficulty: Intermediate
tags: [playground, blueprints, wordpress, development, testing, sandbox]
use_case: Setting up WordPress Playground instances with custom configurations
related: [tools/wordpress-installer, testing/wordpress-testing]
wp_version: 6.0+
php_version: 8.0+
---

# WordPress Playground Blueprints Complete Guide

WordPress Playground Blueprints are JSON files that define how to set up a WordPress Playground instance. This comprehensive guide covers everything from basic setup to advanced configurations with working examples.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Blueprint Data Format](#blueprint-data-format)
3. [Core Steps Reference](#core-steps-reference)
4. [Working Examples](#working-examples)
5. [Blueprint Bundles](#blueprint-bundles)
6. [Advanced Configurations](#advanced-configurations)
7. [Troubleshooting](#troubleshooting)

## Getting Started

### What are Blueprints?

Blueprints are JSON configuration files that define:
- WordPress version to load
- Themes and plugins to install
- User accounts and permissions
- File operations
- Database setup
- Custom PHP code execution

### Basic Blueprint Structure

```json
{
  "landingPage": "/wp-admin/",
  "steps": [
    {
      "step": "login",
      "username": "admin",
      "password": "password"
    }
  ]
}
```

## Blueprint Data Format

### Core Properties

```json
{
  "landingPage": "/wp-admin/",
  "phpExtensionBundles": ["kitchen-sink"],
  "features": {
    "networking": true,
    "networkingMode": "enabled"
  },
  "steps": []
}
```

### Available Properties

- `landingPage`: Where to redirect after setup
- `phpExtensionBundles`: PHP extensions to include
- `features`: Enable/disable features
- `steps`: Array of setup steps
- `blueprintType`: Type of blueprint
- `preferredVersions`: WordPress/PHP version preferences

## Core Steps Reference

### Authentication Steps

#### Login Step
```json
{
  "step": "login",
  "username": "admin",
  "password": "password"
}
```

#### Create User Step
```json
{
  "step": "createUser",
  "user": {
    "user_login": "editor",
    "user_email": "editor@example.com",
    "user_pass": "password123",
    "role": "editor"
  }
}
```

### WordPress Installation Steps

#### Install WordPress
```json
{
  "step": "installWordPress",
  "options": {
    "admin_user": "admin",
    "admin_password": "password",
    "admin_email": "admin@example.com",
    "site_title": "My Playground Site"
  }
}
```

#### Install Plugin
```json
{
  "step": "installPlugin",
  "pluginZipFile": {
    "resource": "url",
    "url": "https://downloads.wordpress.org/plugin/contact-form-7.5.7.zip"
  }
}
```

#### Install Theme
```json
{
  "step": "installTheme",
  "themeZipFile": {
    "resource": "url",
    "url": "https://downloads.wordpress.org/theme/twentytwentyfour.1.0.zip"
  }
}
```

### File Operations

#### Write File
```json
{
  "step": "writeFile",
  "path": "/wp-content/themes/custom/style.css",
  "data": "body { background: #f0f0f0; }"
}
```

#### Run PHP Code
```json
{
  "step": "runPHP",
  "code": "<?php\necho 'Hello from Playground!';\n?>"
}
```

### Database Operations

#### SQL Query
```json
{
  "step": "sql",
  "query": "INSERT INTO wp_options (option_name, option_value) VALUES ('custom_option', 'custom_value')"
}
```

## Working Examples

### Example 1: Basic WordPress Setup

```json
{
  "landingPage": "/wp-admin/",
  "steps": [
    {
      "step": "installWordPress",
      "options": {
        "admin_user": "admin",
        "admin_password": "password",
        "admin_email": "admin@example.com",
        "site_title": "My Playground Site"
      }
    },
    {
      "step": "login",
      "username": "admin",
      "password": "password"
    }
  ]
}
```

### Example 2: Plugin Development Environment

```json
{
  "landingPage": "/wp-admin/plugins.php",
  "steps": [
    {
      "step": "installWordPress",
      "options": {
        "admin_user": "developer",
        "admin_password": "dev123",
        "admin_email": "dev@example.com",
        "site_title": "Plugin Dev Environment"
      }
    },
    {
      "step": "installPlugin",
      "pluginZipFile": {
        "resource": "url",
        "url": "https://downloads.wordpress.org/plugin/query-monitor.3.15.0.zip"
      }
    },
    {
      "step": "installPlugin",
      "pluginZipFile": {
        "resource": "url",
        "url": "https://downloads.wordpress.org/plugin/debug-bar.1.1.4.zip"
      }
    },
    {
      "step": "writeFile",
      "path": "/wp-content/plugins/my-custom-plugin/my-custom-plugin.php",
      "data": "<?php\n/**\n * Plugin Name: My Custom Plugin\n * Description: A custom plugin for development\n * Version: 1.0.0\n */\n\n// Prevent direct access\nif (!defined('ABSPATH')) {\n    exit;\n}\n\n// Plugin initialization\nadd_action('init', function() {\n    // Your plugin code here\n});"
    },
    {
      "step": "login",
      "username": "developer",
      "password": "dev123"
    }
  ]
}
```

### Example 3: Theme Development Setup

```json
{
  "landingPage": "/wp-admin/themes.php",
  "steps": [
    {
      "step": "installWordPress",
      "options": {
        "admin_user": "designer",
        "admin_password": "design123",
        "admin_email": "designer@example.com",
        "site_title": "Theme Development"
      }
    },
    {
      "step": "writeFile",
      "path": "/wp-content/themes/my-custom-theme/style.css",
      "data": "/*\nTheme Name: My Custom Theme\nDescription: A custom theme for development\nVersion: 1.0.0\nAuthor: Developer\n*/\n\nbody {\n    font-family: Arial, sans-serif;\n    margin: 0;\n    padding: 20px;\n    background-color: #f5f5f5;\n}\n\n.container {\n    max-width: 1200px;\n    margin: 0 auto;\n    background: white;\n    padding: 20px;\n    border-radius: 8px;\n    box-shadow: 0 2px 10px rgba(0,0,0,0.1);\n}"
    },
    {
      "step": "writeFile",
      "path": "/wp-content/themes/my-custom-theme/index.php",
      "data": "<?php get_header(); ?>\n\n<div class=\"container\">\n    <h1><?php bloginfo('name'); ?></h1>\n    <p><?php bloginfo('description'); ?></p>\n    \n    <?php if (have_posts()) : ?>\n        <?php while (have_posts()) : the_post(); ?>\n            <article>\n                <h2><a href=\"<?php the_permalink(); ?>\"><?php the_title(); ?></a></h2>\n                <div class=\"content\">\n                    <?php the_content(); ?>\n                </div>\n            </article>\n        <?php endwhile; ?>\n    <?php endif; ?>\n</div>\n\n<?php get_footer(); ?>"
    },
    {
      "step": "writeFile",
      "path": "/wp-content/themes/my-custom-theme/functions.php",
      "data": "<?php\n// Theme setup\nfunction my_custom_theme_setup() {\n    add_theme_support('post-thumbnails');\n    add_theme_support('title-tag');\n    add_theme_support('html5', array('search-form', 'comment-form', 'comment-list', 'gallery', 'caption'));\n}\nadd_action('after_setup_theme', 'my_custom_theme_setup');\n\n// Enqueue styles\nfunction my_custom_theme_styles() {\n    wp_enqueue_style('theme-style', get_stylesheet_uri());\n}\nadd_action('wp_enqueue_scripts', 'my_custom_theme_styles');"
    },
    {
      "step": "login",
      "username": "designer",
      "password": "design123"
    }
  ]
}
```

### Example 4: WooCommerce Development Environment

```json
{
  "landingPage": "/wp-admin/admin.php?page=wc-admin",
  "steps": [
    {
      "step": "installWordPress",
      "options": {
        "admin_user": "store_admin",
        "admin_password": "store123",
        "admin_email": "admin@store.com",
        "site_title": "WooCommerce Development Store"
      }
    },
    {
      "step": "installPlugin",
      "pluginZipFile": {
        "resource": "url",
        "url": "https://downloads.wordpress.org/plugin/woocommerce.8.5.2.zip"
      }
    },
    {
      "step": "runPHP",
      "code": "<?php\n// Activate WooCommerce\nactivate_plugin('woocommerce/woocommerce.php');\n\n// Set up WooCommerce pages\nWC_Install::create_pages();\n\n// Configure basic WooCommerce settings\nupdate_option('woocommerce_store_address', '123 Store Street');\nupdate_option('woocommerce_store_city', 'Store City');\nupdate_option('woocommerce_store_postcode', '12345');\nupdate_option('woocommerce_default_country', 'US:CA');\nupdate_option('woocommerce_currency', 'USD');\n?>"
    },
    {
      "step": "runPHP",
      "code": "<?php\n// Create sample products\n$product1 = new WC_Product_Simple();\n$product1->set_name('Sample Product 1');\n$product1->set_regular_price(29.99);\n$product1->set_description('This is a sample product for testing.');\n$product1->set_short_description('Sample Product 1');\n$product1->set_status('publish');\n$product1->save();\n\n$product2 = new WC_Product_Simple();\n$product2->set_name('Sample Product 2');\n$product2->set_regular_price(49.99);\n$product2->set_description('Another sample product for testing.');\n$product2->set_short_description('Sample Product 2');\n$product2->set_status('publish');\n$product2->save();\n?>"
    },
    {
      "step": "login",
      "username": "store_admin",
      "password": "store123"
    }
  ]
}
```

### Example 5: Multisite Development Setup

```json
{
  "landingPage": "/wp-admin/network/",
  "steps": [
    {
      "step": "installWordPress",
      "options": {
        "admin_user": "super_admin",
        "admin_password": "super123",
        "admin_email": "super@network.com",
        "site_title": "Multisite Network"
      }
    },
    {
      "step": "runPHP",
      "code": "<?php\n// Enable multisite\nupdate_option('MULTISITE', true);\nupdate_option('SUBDOMAIN_INSTALL', false);\nupdate_option('DOMAIN_CURRENT_SITE', 'localhost');\nupdate_option('PATH_CURRENT_SITE', '/');\nupdate_option('SITE_ID_CURRENT_SITE', 1);\nupdate_option('BLOG_ID_CURRENT_SITE', 1);\n\n// Add multisite constants to wp-config\n$wp_config = file_get_contents(ABSPATH . 'wp-config.php');\n$multisite_config = \"\n// Multisite Configuration\ndefine('MULTISITE', true);\ndefine('SUBDOMAIN_INSTALL', false);\ndefine('DOMAIN_CURRENT_SITE', 'localhost');\ndefine('PATH_CURRENT_SITE', '/');\ndefine('SITE_ID_CURRENT_SITE', 1);\ndefine('BLOG_ID_CURRENT_SITE', 1);\n\";\n\n$wp_config = str_replace('/* That\\'s all, stop editing! */', $multisite_config . '/* That\\'s all, stop editing! */', $wp_config);\nfile_put_contents(ABSPATH . 'wp-config.php', $wp_config);\n?>"
    },
    {
      "step": "runPHP",
      "code": "<?php\n// Create additional sites\n$site2 = wpmu_create_blog('localhost', '/site2', 'Site 2', 'admin@site2.com');\n$site3 = wpmu_create_blog('localhost', '/site3', 'Site 3', 'admin@site3.com');\n\nif ($site2 && $site3) {\n    echo 'Multisite setup complete with 3 sites';\n}\n?>"
    },
    {
      "step": "login",
      "username": "super_admin",
      "password": "super123"
    }
  ]
}
```

## Blueprint Bundles

### Creating Blueprint Bundles

Blueprint bundles are self-contained packages that include:
- Blueprint JSON file
- All required resources (themes, plugins, files)
- Dependencies

### Bundle Structure

```
my-blueprint-bundle/
├── blueprint.json
├── resources/
│   ├── themes/
│   │   └── custom-theme.zip
│   ├── plugins/
│   │   └── custom-plugin.zip
│   └── files/
│       └── custom-config.php
└── README.md
```

### Bundle Blueprint Example

```json
{
  "landingPage": "/wp-admin/",
  "steps": [
    {
      "step": "installWordPress",
      "options": {
        "admin_user": "admin",
        "admin_password": "password",
        "admin_email": "admin@example.com",
        "site_title": "Bundle Demo"
      }
    },
    {
      "step": "installTheme",
      "themeZipFile": {
        "resource": "vfs",
        "path": "/resources/themes/custom-theme.zip"
      }
    },
    {
      "step": "installPlugin",
      "pluginZipFile": {
        "resource": "vfs",
        "path": "/resources/plugins/custom-plugin.zip"
      }
    },
    {
      "step": "writeFile",
      "path": "/wp-content/mu-plugins/custom-config.php",
      "data": {
        "resource": "vfs",
        "path": "/resources/files/custom-config.php"
      }
    }
  ]
}
```

## Advanced Configurations

### Custom PHP Extensions

```json
{
  "phpExtensionBundles": ["kitchen-sink"],
  "steps": [
    {
      "step": "runPHP",
      "code": "<?php\n// Check available extensions\n$extensions = get_loaded_extensions();\necho 'Available extensions: ' . implode(', ', $extensions);\n?>"
    }
  ]
}
```

### Networking Configuration

```json
{
  "features": {
    "networking": true,
    "networkingMode": "enabled"
  },
  "steps": [
    {
      "step": "runPHP",
      "code": "<?php\n// Test external connectivity\n$response = wp_remote_get('https://api.wordpress.org/core/version-check/1.7/');\nif (!is_wp_error($response)) {\n    echo 'External connectivity working';\n} else {\n    echo 'External connectivity failed';\n}\n?>"
    }
  ]
}
```

### Custom Database Setup

```json
{
  "steps": [
    {
      "step": "sql",
      "query": "CREATE TABLE custom_table (\n    id INT AUTO_INCREMENT PRIMARY KEY,\n    name VARCHAR(255) NOT NULL,\n    value TEXT,\n    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n)"
    },
    {
      "step": "sql",
      "query": "INSERT INTO custom_table (name, value) VALUES ('test', 'sample data')"
    },
    {
      "step": "runPHP",
      "code": "<?php\nglobal $wpdb;\n$results = $wpdb->get_results('SELECT * FROM custom_table');\necho 'Custom table has ' . count($results) . ' records';\n?>"
    }
  ]
}
```

## Troubleshooting

### Common Issues

#### Blueprint Validation Errors
```json
{
  "error": "Invalid step type",
  "solution": "Check step names against official documentation"
}
```

#### File Permission Issues
```json
{
  "step": "runPHP",
  "code": "<?php\n// Check file permissions\n$upload_dir = wp_upload_dir();\necho 'Upload directory: ' . $upload_dir['path'];\necho 'Writable: ' . (is_writable($upload_dir['path']) ? 'Yes' : 'No');\n?>"
}
```

#### Plugin Activation Issues
```json
{
  "step": "runPHP",
  "code": "<?php\n// Check plugin status\n$active_plugins = get_option('active_plugins');\necho 'Active plugins: ' . implode(', ', $active_plugins);\n\n// Check for plugin errors\n$errors = get_option('plugin_error_log');\nif ($errors) {\n    echo 'Plugin errors: ' . $errors;\n}\n?>"
}
```

### Debugging Tips

1. **Use runPHP steps** to debug issues
2. **Check file permissions** before file operations
3. **Validate JSON syntax** before deployment
4. **Test step by step** for complex blueprints
5. **Use networking mode** for external resources

### Performance Optimization

```json
{
  "steps": [
    {
      "step": "runPHP",
      "code": "<?php\n// Optimize WordPress for Playground\nupdate_option('blog_public', 0);\nupdate_option('default_pingback_flag', 0);\nupdate_option('default_ping_status', 'closed');\nupdate_option('default_comment_status', 'closed');\nupdate_option('comments_notify', 0);\nupdate_option('moderation_notify', 0);\nupdate_option('comment_registration', 0);\nupdate_option('close_comments_for_old_posts', 1);\nupdate_option('close_comments_days_old', 1);\n?>"
    }
  ]
}
```

## Best Practices

### 1. Always Include Login Step
```json
{
  "step": "login",
  "username": "admin",
  "password": "password"
}
```

### 2. Use Descriptive Landing Pages
```json
{
  "landingPage": "/wp-admin/themes.php"
}
```

### 3. Validate External Resources
```json
{
  "step": "runPHP",
  "code": "<?php\n// Validate plugin installation\nif (is_plugin_active('plugin-name/plugin-name.php')) {\n    echo 'Plugin activated successfully';\n} else {\n    echo 'Plugin activation failed';\n}\n?>"
}
```

### 4. Handle Errors Gracefully
```json
{
  "step": "runPHP",
  "code": "<?php\n// Error handling example\ntry {\n    // Your code here\n    $result = some_function();\n    echo 'Success: ' . $result;\n} catch (Exception $e) {\n    echo 'Error: ' . $e->getMessage();\n}\n?>"
}
```

## Resources and References

- [WordPress Playground Blueprints Documentation](https://wordpress.github.io/wordpress-playground/blueprints/)
- [Blueprint Gallery](https://wordpress.github.io/wordpress-playground/blueprints/gallery/)
- [API Reference](https://wordpress.github.io/wordpress-playground/api-reference/)
- [GitHub Repository](https://github.com/WordPress/wordpress-playground)

## Conclusion

WordPress Playground Blueprints provide a powerful way to create reproducible WordPress environments for development, testing, and demonstration purposes. With the examples and configurations provided in this guide, you can create sophisticated WordPress setups tailored to your specific needs.

Remember to always test your blueprints thoroughly and follow WordPress best practices for security and performance.
