# WordPress Options API

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