# WordPress Development Workflow

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