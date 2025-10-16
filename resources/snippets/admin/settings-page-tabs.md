# Settings Page with Tabs

```php
function render_settings_page() {
    $active_tab = isset( $_GET['tab'] ) ? sanitize_text_field( $_GET['tab'] ) : 'general';
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        
        <h2 class="nav-tab-wrapper">
            <a href="?page=my-plugin&tab=general" class="nav-tab <?php echo $active_tab === 'general' ? 'nav-tab-active' : ''; ?>">
                <?php esc_html_e( 'General', 'textdomain' ); ?>
            </a>
            <a href="?page=my-plugin&tab=advanced" class="nav-tab <?php echo $active_tab === 'advanced' ? 'nav-tab-active' : ''; ?>">
                <?php esc_html_e( 'Advanced', 'textdomain' ); ?>
            </a>
            <a href="?page=my-plugin&tab=tools" class="nav-tab <?php echo $active_tab === 'tools' ? 'nav-tab-active' : ''; ?>">
                <?php esc_html_e( 'Tools', 'textdomain' ); ?>
            </a>
        </h2>
        
        <form method="post" action="options.php">
            <?php
            switch ( $active_tab ) {
                case 'general':
                    settings_fields( 'myplugin_general' );
                    do_settings_sections( 'myplugin_general' );
                    break;
                case 'advanced':
                    settings_fields( 'myplugin_advanced' );
                    do_settings_sections( 'myplugin_advanced' );
                    break;
                case 'tools':
                    // Custom tools tab content
                    include 'tools-tab.php';
                    break;
            }
            
            submit_button();
            ?>
        </form>
    </div>
    <?php
}
```
