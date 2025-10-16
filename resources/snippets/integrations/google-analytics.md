# Google Analytics Integration

```php
// Add GA4 tracking code
add_action( 'wp_head', 'add_google_analytics' );
function add_google_analytics() {
    $ga_id = get_option( 'google_analytics_id' );
    
    if ( ! $ga_id ) {
        return;
    }
    
    // Exclude admin users
    if ( current_user_can( 'manage_options' ) ) {
        return;
    }
    ?>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr( $ga_id ); ?>"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '<?php echo esc_js( $ga_id ); ?>');
    </script>
    <?php
}

// Track custom events
function track_custom_event( $event_name, $event_params = array() ) {
    ?>
    <script>
    gtag('event', '<?php echo esc_js( $event_name ); ?>', <?php echo json_encode( $event_params ); ?>);
    </script>
    <?php
}

// Track downloads
add_action( 'wp_footer', 'track_downloads' );
function track_downloads() {
    ?>
    <script>
    jQuery('a[href$=".pdf"], a[href$=".zip"]').on('click', function() {
        var fileUrl = jQuery(this).attr('href');
        gtag('event', 'file_download', {
            'file_name': fileUrl.split('/').pop(),
            'file_url': fileUrl
        });
    });
    </script>
    <?php
}
```
