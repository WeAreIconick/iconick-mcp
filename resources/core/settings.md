# WordPress Settings API

The Settings API provides a secure way to create admin settings pages with proper data validation, sanitization, and form handling.

## Basic Settings Page

```php
function my_settings_page() {
    ?>
    <div class="wrap">
        <h1>My Plugin Settings</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields( 'my_options_group' );
            do_settings_sections( 'my_options_page' );
            submit_button();
            ?>
        </form>
    </div>
    <?php
}

function add_my_admin_menu() {
    add_options_page(
        'My Plugin Settings',    // Page title
        'My Plugin',             // Menu title
        'manage_options',        // Capability
        'my-plugin-settings',    // Menu slug
        'my_settings_page'       // Callback
    );
}
add_action( 'admin_menu', 'add_my_admin_menu' );
```

## Register Settings

```php
function register_my_settings() {
    // Register setting
    register_setting(
        'my_options_group',      // Option group
        'my_option_name',        // Option name
        array(
            'type' => 'string',
            'sanitize_callback' => 'sanitize_my_option',
            'default' => 'default_value'
        )
    );
    
    // Add settings section
    add_settings_section(
        'my_section_id',         // Section ID
        'My Settings Section',   // Section title
        'my_section_callback',   // Callback function
        'my_options_page'        // Page slug
    );
    
    // Add settings field
    add_settings_field(
        'my_field_id',           // Field ID
        'My Field Label',        // Field label
        'my_field_callback',     // Callback function
        'my_options_page',       // Page slug
        'my_section_id'          // Section ID
    );
}
add_action( 'admin_init', 'register_my_settings' );
```

## Field Types and Callbacks

### Text Field

```php
function text_field_callback() {
    $value = get_option( 'my_text_option', 'default' );
    echo '<input type="text" name="my_text_option" value="' . esc_attr( $value ) . '" />';
}
```

### Checkbox Field

```php
function checkbox_field_callback() {
    $value = get_option( 'my_checkbox_option', false );
    $checked = checked( $value, true, false );
    echo '<input type="checkbox" name="my_checkbox_option" value="1" ' . $checked . ' />';
    echo '<label for="my_checkbox_option">Enable this feature</label>';
}
```

## Sanitization and Validation

### Custom Sanitization Function

```php
function sanitize_my_option( $input ) {
    // Validate and sanitize input
    $output = array();
    
    if ( isset( $input['text_field'] ) ) {
        $output['text_field'] = sanitize_text_field( $input['text_field'] );
    }
    
    if ( isset( $input['email_field'] ) ) {
        $email = sanitize_email( $input['email_field'] );
        if ( ! is_email( $email ) ) {
            add_settings_error( 'my_options_group', 'invalid_email', 'Please enter a valid email address.' );
        } else {
            $output['email_field'] = $email;
        }
    }
    
    return $output;
}
```

## Best Practices

### Security

```php
// Always use nonces (automatic with settings_fields())
// Always sanitize input
// Always validate data
// Always check capabilities

function secure_settings_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'You do not have permission to access this page.' );
    }
    
    // Rest of your settings page code
}
```

## Official Documentation

https://developer.wordpress.org/plugins/settings/
https://developer.wordpress.org/reference/functions/register_setting/
https://developer.wordpress.org/reference/functions/add_settings_section/
https://developer.wordpress.org/reference/functions/add_settings_field/
