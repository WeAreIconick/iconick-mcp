---
difficulty: Advanced
tags: [ajax, heartbeat, realtime, polling]
related: [ajax/admin-ajax]
use_case: Real-time communication with server
---

# WordPress Heartbeat API

```php
// Modify heartbeat settings
add_action( 'admin_enqueue_scripts', 'modify_heartbeat' );
function modify_heartbeat() {
    wp_enqueue_script( 'heartbeat' );
}

// Add data to heartbeat
add_filter( 'heartbeat_send', 'mytheme_heartbeat_send', 10, 2 );
function mytheme_heartbeat_send( $response, $data ) {
    if ( isset( $data['my_plugin_check'] ) ) {
        $response['my_plugin_data'] = array(
            'status' => 'active',
            'count' => get_comment_count()
        );
    }
    return $response;
}

// JavaScript
jQuery(document).on('heartbeat-send', function(e, data) {
    data.my_plugin_check = true;
});

jQuery(document).on('heartbeat-tick', function(e, data) {
    if (data.my_plugin_data) {
        console.log('Status:', data.my_plugin_data.status);
    }
});
```
