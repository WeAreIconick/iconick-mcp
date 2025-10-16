# Network-Wide Settings

```php
// Add network admin menu
add_action( 'network_admin_menu', 'add_network_admin_page' );
function add_network_admin_page() {
    add_menu_page(
        'Network Settings',
        'My Plugin',
        'manage_network_options',
        'my-network-settings',
        'render_network_settings'
    );
}

function render_network_settings() {
    if ( ! current_user_can( 'manage_network_options' ) ) {
        return;
    }
    
    // Save settings
    if ( isset( $_POST['submit'] ) && check_admin_referer( 'network_settings' ) ) {
        update_site_option( 'my_network_option', sanitize_text_field( $_POST['my_option'] ) );
        echo '<div class="updated"><p>Settings saved!</p></div>';
    }
    
    $value = get_site_option( 'my_network_option', '' );
    ?>
    <div class="wrap">
        <h1>Network Settings</h1>
        <form method="post">
            <?php wp_nonce_field( 'network_settings' ); ?>
            <table class="form-table">
                <tr>
                    <th>Network Option</th>
                    <td>
                        <input type="text" name="my_option" value="<?php echo esc_attr( $value ); ?>" class="regular-text">
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

// Access in site context
function get_network_setting( $key, $default = '' ) {
    return get_site_option( $key, $default );
}
```
