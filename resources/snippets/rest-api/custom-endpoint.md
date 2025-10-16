---
difficulty: Advanced
tags: [rest, api, endpoints, json]
related: [rest-api/rest-authentication, security/nonces]
use_case: Creating custom REST endpoints
---

# Custom REST API Endpoint

```php
add_action( 'rest_api_init', function() {
    register_rest_route( 'myplugin/v1', '/items', array(
        'methods' => 'GET',
        'callback' => 'get_items',
        'permission_callback' => '__return_true',
        'args' => array(
            'per_page' => array(
                'default' => 10,
                'sanitize_callback' => 'absint'
            )
        )
    ));
    
    register_rest_route( 'myplugin/v1', '/items/(?P<id>\d+)', array(
        'methods' => 'GET',
        'callback' => 'get_item',
        'permission_callback' => '__return_true',
        'args' => array(
            'id' => array(
                'validate_callback' => function($param) {
                    return is_numeric( $param );
                }
            )
        )
    ));
    
    register_rest_route( 'myplugin/v1', '/items', array(
        'methods' => 'POST',
        'callback' => 'create_item',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        }
    ));
});

function get_items( $request ) {
    $per_page = $request['per_page'];
    
    $posts = get_posts( array(
        'post_type' => 'my_cpt',
        'posts_per_page' => $per_page
    ));
    
    $data = array();
    foreach ( $posts as $post ) {
        $data[] = array(
            'id' => $post->ID,
            'title' => $post->post_title,
            'link' => get_permalink( $post->ID )
        );
    }
    
    return rest_ensure_response( $data );
}
```
