# WordPress CLI (WP-CLI)

WP-CLI is the command-line interface for WordPress, providing powerful tools for managing WordPress sites from the terminal.

## Installation

### Basic Installation

```bash
# Download and install WP-CLI
curl -O https://raw.githubusercontent.com/wp-cli/wp-cli/v2.8.1/phar/wp-cli.phar

# Make it executable
chmod +x wp-cli.phar

# Move to system path
sudo mv wp-cli.phar /usr/local/bin/wp

# Verify installation
wp --info
```

### Alternative Installation Methods

```bash
# Install via Composer
composer global require wp-cli/wp-cli

# Install via Homebrew (macOS)
brew install wp-cli

# Install via package manager (Ubuntu/Debian)
sudo apt-get install wp-cli

# Install via package manager (CentOS/RHEL)
sudo yum install wp-cli
```

## Basic Commands

### Site Management

```bash
# Get WordPress version and site information
wp --info

# Check WordPress core version
wp core version

# Update WordPress core
wp core update

# Download WordPress core
wp core download

# Install WordPress
wp core install --url=example.com --title="My Site" --admin_user=admin --admin_password=password --admin_email=admin@example.com

# Check for WordPress updates
wp core check-update

# Update WordPress database
wp core update-db
```

### Plugin Management

```bash
# List installed plugins
wp plugin list

# Install a plugin
wp plugin install akismet

# Activate a plugin
wp plugin activate akismet

# Deactivate a plugin
wp plugin deactivate akismet

# Delete a plugin
wp plugin delete akismet

# Update all plugins
wp plugin update-all

# Update specific plugin
wp plugin update akismet

# Search for plugins
wp plugin search "contact form"

# Get plugin information
wp plugin get akismet
```

### Theme Management

```bash
# List installed themes
wp theme list

# Install a theme
wp theme install twentytwentythree

# Activate a theme
wp theme activate twentytwentythree

# Delete a theme
wp theme delete twentytwentythree

# Update all themes
wp theme update-all

# Search for themes
wp theme search "business"

# Get theme information
wp theme get twentytwentythree
```

### User Management

```bash
# List users
wp user list

# Create a new user
wp user create john john@example.com --role=editor --user_pass=password

# Update user information
wp user update john --display_name="John Doe" --user_email=john.doe@example.com

# Delete a user
wp user delete john

# Change user role
wp user update john --role=administrator

# Reset user password
wp user update john --user_pass=newpassword

# Get user information
wp user get john
```

## Content Management

### Post Management

```bash
# List posts
wp post list

# Create a new post
wp post create --post_title="My Post" --post_content="Post content here" --post_status=publish

# Update a post
wp post update 123 --post_title="Updated Title"

# Delete a post
wp post delete 123

# Get post information
wp post get 123

# Search posts
wp post search "keyword"

# Generate sample posts
wp post generate --count=10
```

### Page Management

```bash
# List pages
wp post list --post_type=page

# Create a new page
wp post create --post_type=page --post_title="About Us" --post_content="About us content" --post_status=publish

# Update a page
wp post update 456 --post_content="Updated content"

# Delete a page
wp post delete 456
```

### Media Management

```bash
# List media files
wp media list

# Import media from URL
wp media import https://example.com/image.jpg --title="My Image"

# Import media from file
wp media import /path/to/image.jpg

# Regenerate thumbnails
wp media regenerate

# Get media information
wp media get 789
```

## Database Operations

### Database Management

```bash
# Check database connection
wp db check

# Optimize database
wp db optimize

# Repair database
wp db repair

# Export database
wp db export backup.sql

# Import database
wp db import backup.sql

# Reset database (WARNING: destructive)
wp db reset

# Search and replace in database
wp search-replace old-url.com new-url.com

# Run SQL query
wp db query "SELECT * FROM wp_posts LIMIT 5"
```

### Custom Database Operations

```bash
# Export specific tables
wp db export --tables=wp_posts,wp_users backup.sql

# Import with different prefix
wp db import backup.sql --prefix=new_wp_

# Search and replace with dry run
wp search-replace old-url.com new-url.com --dry-run

# Search and replace with regex
wp search-replace 'old-pattern' 'new-pattern' --regex
```

## Configuration Management

### wp-config.php Operations

```bash
# Get configuration values
wp config get WP_DEBUG

# Set configuration values
wp config set WP_DEBUG true --type=constant

# Delete configuration values
wp config delete WP_DEBUG

# List all configuration
wp config list

# Create wp-config.php
wp config create --dbname=wordpress --dbuser=root --dbpass=password --dbhost=localhost
```

### Environment Management

```bash
# Set environment variables
wp config set WP_ENV production --type=constant

# Get environment information
wp config get WP_ENV

# List all constants
wp config list --type=constant
```

## Advanced Features

### Custom Commands

```bash
# Create custom WP-CLI command
wp scaffold package my-command

# This creates a package structure for custom commands
```

### Custom Command Example

```php
<?php
// wp-cli-commands.php

if ( ! class_exists( 'WP_CLI' ) ) {
    return;
}

class My_Custom_Command {
    
    /**
     * Custom command to clean up old posts
     *
     * @param array $args
     * @param array $assoc_args
     */
    public function cleanup_old_posts( $args, $assoc_args ) {
        $days = isset( $assoc_args['days'] ) ? intval( $assoc_args['days'] ) : 30;
        
        $posts = get_posts( array(
            'post_type' => 'post',
            'posts_per_page' => -1,
            'date_query' => array(
                array(
                    'before' => $days . ' days ago'
                )
            )
        ) );
        
        $deleted = 0;
        foreach ( $posts as $post ) {
            if ( wp_delete_post( $post->ID, true ) ) {
                $deleted++;
            }
        }
        
        WP_CLI::success( "Deleted {$deleted} old posts" );
    }
}

WP_CLI::add_command( 'my-command', 'My_Custom_Command' );
```

### Batch Operations

```bash
# Process posts in batches
wp post list --format=ids | xargs -I {} wp post update {} --post_status=draft

# Update all posts with specific meta
wp post list --format=ids | xargs -I {} wp post meta update {} featured "1"

# Delete all posts of specific type
wp post list --post_type=revision --format=ids | xargs -I {} wp post delete {} --force
```

## Plugin Development

### Plugin Scaffolding

```bash
# Create a new plugin
wp scaffold plugin my-plugin --plugin_name="My Plugin" --plugin_description="A custom plugin"

# Create plugin boilerplate
wp scaffold plugin my-plugin --plugin_name="My Plugin" --plugin_author="John Doe" --plugin_author_uri="https://example.com" --plugin_uri="https://example.com/my-plugin"
```

### Plugin Testing

```bash
# Test plugin functionality
wp plugin activate my-plugin
wp eval "echo 'Plugin loaded successfully';"

# Check plugin dependencies
wp plugin list --status=active --format=table
```

## Theme Development

### Theme Scaffolding

```bash
# Create a new theme
wp scaffold theme my-theme --theme_name="My Theme" --theme_description="A custom theme"

# Create child theme
wp scaffold child-theme my-child-theme --parent_theme=twentytwentythree
```

### Theme Testing

```bash
# Switch to test theme
wp theme activate my-theme

# Test theme functionality
wp eval "echo get_template_directory();"
```

## Automation and Scripting

### Backup Script

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
SITE_DIR="/var/www/html"

# Create backup directory
mkdir -p $BACKUP_DIR

# Export database
wp db export $BACKUP_DIR/db_backup_$DATE.sql

# Create files backup
tar -czf $BACKUP_DIR/files_backup_$DATE.tar.gz $SITE_DIR

# Clean old backups (older than 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### Deployment Script

```bash
#!/bin/bash
# deploy.sh

# Pull latest code
git pull origin main

# Update WordPress core
wp core update

# Update plugins
wp plugin update-all

# Update themes
wp theme update-all

# Update database
wp core update-db

# Clear cache (if using caching plugin)
wp cache flush

echo "Deployment completed"
```

## Troubleshooting

### Common Issues

```bash
# Fix file permissions
wp core install --url=example.com --title="Test" --admin_user=admin --admin_password=password --admin_email=admin@example.com

# Reset admin password
wp user update admin --user_pass=newpassword

# Check WordPress installation
wp core is-installed

# Verify WordPress installation
wp core verify-checksums
```

### Debug Mode

```bash
# Enable debug mode
wp config set WP_DEBUG true --type=constant
wp config set WP_DEBUG_LOG true --type=constant
wp config set WP_DEBUG_DISPLAY false --type=constant

# Check debug log
wp eval "echo file_get_contents(WP_CONTENT_DIR . '/debug.log');"
```

## Best Practices

### Security

```bash
# Use strong passwords
wp user update admin --user_pass=$(openssl rand -base64 32)

# Limit login attempts (requires plugin)
wp plugin install limit-login-attempts-reloaded

# Regular updates
wp core update
wp plugin update-all
wp theme update-all
```

### Performance

```bash
# Optimize database regularly
wp db optimize

# Clean up revisions
wp post delete $(wp post list --post_type=revision --format=ids)

# Clear transients
wp transient delete --all
```

### Maintenance

```bash
# Regular backups
wp db export backup_$(date +%Y%m%d).sql

# Monitor disk usage
wp eval "echo 'Disk usage: ' . disk_free_space('/') . ' bytes free';"

# Check for updates
wp core check-update
wp plugin check-update
wp theme check-update
```

## Official Documentation

https://wp-cli.org/
https://developer.wordpress.org/cli/commands/
https://github.com/wp-cli/wp-cli
