---
difficulty: Intermediate
tags: [deployment, git, devops, automation]
related: [deployment/environment-config, cli/wp-cli-commands]
use_case: Git-based deployment workflow
---

# Git-Based Deployment

```bash
#!/bin/bash
# deploy.sh - WordPress deployment script

set -e

echo "🚀 Starting deployment..."

# Pull latest code
git pull origin main

# Install/update dependencies
composer install --no-dev --optimize-autoloader
npm install
npm run build

# WordPress updates
wp core update
wp plugin update --all
wp theme update --all

# Database migrations
if [ -f "migrations.sql" ]; then
    wp db query < migrations.sql
    rm migrations.sql
fi

# Clear caches
wp cache flush
wp transient delete --all
wp rewrite flush

# Optimize database
wp db optimize

echo "✅ Deployment complete!"
```

```php
// deployment-config.php
// Prevent direct access to deployment files
if ( defined( 'DOING_CRON' ) || defined( 'WP_CLI' ) ) {
    // Allow WP-CLI and cron
} else {
    die( 'Access denied' );
}

// Run migrations
function run_database_migrations() {
    $current_version = get_option( 'my_plugin_db_version', '1.0' );
    $new_version = '1.1';
    
    if ( version_compare( $current_version, $new_version, '<' ) ) {
        global $wpdb;
        
        // Run migration
        $wpdb->query( "ALTER TABLE {$wpdb->prefix}my_table ADD COLUMN new_field VARCHAR(255)" );
        
        // Update version
        update_option( 'my_plugin_db_version', $new_version );
    }
}
```
