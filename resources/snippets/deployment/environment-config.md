---
difficulty: Intermediate
tags: [deployment, environment, config, devops]
related: [deployment/git-deployment]
use_case: Environment-specific configuration
---

# Environment-Specific Configuration

```php
// wp-config.php environment detection
define( 'WP_ENVIRONMENT_TYPE', getenv( 'WP_ENV' ) ?: 'production' );

// Development environment
if ( WP_ENVIRONMENT_TYPE === 'development' ) {
    define( 'WP_DEBUG', true );
    define( 'WP_DEBUG_LOG', true );
    define( 'WP_DEBUG_DISPLAY', true );
    define( 'SCRIPT_DEBUG', true );
    define( 'SAVEQUERIES', true );
}

// Staging environment
elseif ( WP_ENVIRONMENT_TYPE === 'staging' ) {
    define( 'WP_DEBUG', true );
    define( 'WP_DEBUG_LOG', true );
    define( 'WP_DEBUG_DISPLAY', false );
}

// Production environment
else {
    define( 'WP_DEBUG', false );
    ini_set( 'display_errors', 0 );
}

// Plugin: Load environment-specific settings
function get_env_setting( $key, $default = '' ) {
    $settings = array(
        'development' => array(
            'api_url' => 'http://localhost:8080/api',
            'debug_mode' => true
        ),
        'staging' => array(
            'api_url' => 'https://staging-api.example.com',
            'debug_mode' => true
        ),
        'production' => array(
            'api_url' => 'https://api.example.com',
            'debug_mode' => false
        )
    );
    
    $env = WP_ENVIRONMENT_TYPE;
    
    return $settings[$env][$key] ?? $default;
}

// Check environment
function is_production() {
    return WP_ENVIRONMENT_TYPE === 'production';
}

function is_development() {
    return WP_ENVIRONMENT_TYPE === 'development';
}
```
