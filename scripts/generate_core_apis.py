#!/usr/bin/env python3
"""
Generate WordPress Core API resources
"""

from pathlib import Path

RESOURCES_DIR = Path(__file__).parent.parent / "resources"

CORE_APIS = {
    "core/options.md": """# WordPress Options API

The Options API provides a simple way to store and retrieve configuration data in the WordPress database.

## Basic Usage

```php
// Get an option
$value = get_option( 'my_option', 'default_value' );

// Update an option
update_option( 'my_option', 'new_value' );

// Add an option (only if it doesn't exist)
add_option( 'my_option', 'initial_value' );

// Delete an option
delete_option( 'my_option' );
```

## Important Considerations

### Autoload Behavior

```php
// Option will be autoloaded (cached in memory)
update_option( 'my_option', 'value', 'yes' );

// Option will NOT be autoloaded (loaded on demand)
update_option( 'my_option', 'value', 'no' );

// Check if option should be autoloaded
$autoload = get_option( 'my_option' ) !== false ? 'yes' : 'no';
```

### Array Options

```php
// Store array data
$settings = array(
    'color' => 'blue',
    'size'  => 'large',
    'active' => true
);
update_option( 'my_settings', $settings );

// Retrieve array data
$settings = get_option( 'my_settings', array() );
$color = $settings['color'] ?? 'default';
```

## Common Patterns

### Plugin Settings

```php
class My_Plugin_Settings {
    
    private $option_name = 'my_plugin_settings';
    private $defaults = array(
        'api_key' => '',
        'debug_mode' => false,
        'cache_duration' => 3600
    );
    
    public function get_settings() {
        $settings = get_option( $this->option_name, array() );
        return wp_parse_args( $settings, $this->defaults );
    }
    
    public function update_settings( $new_settings ) {
        $current = $this->get_settings();
        $updated = wp_parse_args( $new_settings, $current );
        return update_option( $this->option_name, $updated );
    }
    
    public function reset_settings() {
        return delete_option( $this->option_name );
    }
}
```

## Best Practices

1. **Use descriptive names** - Prefix with your plugin/theme name
2. **Provide defaults** - Always specify a default value
3. **Consider autoload** - Use 'no' for large or infrequently accessed options
4. **Validate data** - Sanitize before storing
5. **Use arrays sparingly** - Consider separate options for complex data

## Performance Tips

1. **Autoload consideration** - Options with 'yes' autoload are loaded on every page
2. **Batch operations** - Use get_options() for multiple options
3. **Transients for cache** - Use transients for temporary data
4. **Clean up** - Delete unused options on uninstall

## Official Documentation

https://developer.wordpress.org/apis/options/
https://developer.wordpress.org/reference/functions/get_option/
https://developer.wordpress.org/reference/functions/update_option/
""",

    "core/transients.md": """# WordPress Transients API

Transients provide temporary, cached data storage with automatic expiration.

## Basic Usage

```php
// Set a transient (expires in 1 hour)
set_transient( 'my_cache_key', $data, HOUR_IN_SECONDS );

// Get a transient
$data = get_transient( 'my_cache_key' );

// Delete a transient
delete_transient( 'my_cache_key' );
```

## Time Constants

```php
// WordPress time constants
MINUTE_IN_SECONDS = 60
HOUR_IN_SECONDS = 3600
DAY_IN_SECONDS = 86400
WEEK_IN_SECONDS = 604800
MONTH_IN_SECONDS = 2592000
YEAR_IN_SECONDS = 31536000

// Usage
set_transient( 'api_data', $response, HOUR_IN_SECONDS );
set_transient( 'daily_report', $report, DAY_IN_SECONDS );
```

## Common Patterns

### API Response Caching

```php
function get_weather_data( $city ) {
    $cache_key = 'weather_' . sanitize_key( $city );
    
    // Try to get cached data
    $data = get_transient( $cache_key );
    
    if ( false === $data ) {
        // Cache miss - fetch from API
        $response = wp_remote_get( "https://api.weather.com/{$city}" );
        
        if ( ! is_wp_error( $response ) ) {
            $data = json_decode( wp_remote_retrieve_body( $response ), true );
            
            // Cache for 30 minutes
            set_transient( $cache_key, $data, 30 * MINUTE_IN_SECONDS );
        }
    }
    
    return $data;
}
```

## Best Practices

### Naming Conventions

```php
// Good naming patterns
$cache_key = 'plugin_name_data_' . $identifier;
$cache_key = 'user_' . $user_id . '_posts';
$cache_key = 'api_response_' . md5( $url . serialize( $params ) );

// Bad naming (too generic)
$cache_key = 'data';
$cache_key = 'cache';
```

## Official Documentation

https://developer.wordpress.org/apis/transients/
https://developer.wordpress.org/reference/functions/set_transient/
https://developer.wordpress.org/reference/functions/get_transient/
"""
}

# Create resources
for filepath, content in CORE_APIS.items():
    full_path = RESOURCES_DIR / filepath
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text(content.strip())
    print(f"Created: {filepath}")

print(f"\nGenerated {len(CORE_APIS)} core API resources")
