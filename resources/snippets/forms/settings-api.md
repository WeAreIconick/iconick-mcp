# WordPress Settings API

```php
// Register setting
add_action( 'admin_init', 'my_register_settings' );
function my_register_settings() {
    register_setting(
        'my_options_group',
        'my_option_name',
        array(
            'type' => 'string',
            'sanitize_callback' => 'sanitize_text_field',
            'default' => ''
        )
    );
    
    add_settings_section(
        'my_section',
        __( 'General Settings', 'textdomain' ),
        'my_section_callback',
        'my-plugin'
    );
    
    add_settings_field(
        'my_field',
        __( 'API Key', 'textdomain' ),
        'my_field_callback',
        'my-plugin',
        'my_section'
    );
}

function my_field_callback() {
    $value = get_option( 'my_option_name' );
    echo '<input type="text" name="my_option_name" value="' . esc_attr( $value ) . '" class="regular-text">';
}

// Settings page
<form method="post" action="options.php">
    <?php
    settings_fields( 'my_options_group' );
    do_settings_sections( 'my-plugin' );
    submit_button();
    ?>
</form>
```
