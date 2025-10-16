---
difficulty: Beginner
tags: [cli, wp-cli, commands, terminal]
related: [cli/custom-wp-cli-command, deployment/git-deployment]
use_case: Common WP-CLI commands
---

# WP-CLI Common Commands

```bash
# Install WordPress
wp core download
wp config create --dbname=wordpress --dbuser=root --dbpass=password
wp core install --url=example.com --title="Site" --admin_user=admin --admin_email=admin@example.com

# Plugins
wp plugin install contact-form-7 --activate
wp plugin list
wp plugin update --all
wp plugin search seo

# Themes
wp theme install twentytwentyfour --activate
wp theme list
wp theme update --all

# Database
wp db export backup.sql
wp db import backup.sql
wp db optimize
wp db search-replace 'oldurl.com' 'newurl.com'

# Posts
wp post create --post_type=post --post_title='Title' --post_content='Content' --post_status=publish
wp post list --post_type=page
wp post delete 123 --force

# Users
wp user create john john@example.com --role=editor
wp user list
wp user update 1 --user_pass=newpassword

# Options
wp option get siteurl
wp option update blogname "New Site Name"
wp option list

# Cache
wp cache flush
wp transient delete --all

# Rewrite
wp rewrite flush
wp rewrite list

# Cron
wp cron event list
wp cron event run my_custom_hook

# Maintenance
wp maintenance-mode activate
wp maintenance-mode deactivate
```
