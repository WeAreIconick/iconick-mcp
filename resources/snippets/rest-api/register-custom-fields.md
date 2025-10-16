---
difficulty: Intermediate
tags: [rest, api, fields, meta]
related: [rest-api/custom-endpoint]
use_case: Exposing custom fields in REST API
---

# Register Custom REST Fields

```php
// Add custom field to REST response
add_action( 'rest_api_init', 'register_custom_rest_fields' );
function register_custom_rest_fields() {
    register_rest_field( 'post', 'reading_time', array(
        'get_callback' => 'get_reading_time',
        'update_callback' => null,
        'schema' => array(
            'description' => 'Estimated reading time in minutes',
            'type' => 'integer'
        )
    ));
    
    register_rest_field( 'post', 'author_info', array(
        'get_callback' => 'get_author_info',
        'schema' => array(
            'description' => 'Author information',
            'type' => 'object'
        )
    ));
}

function get_reading_time( $post ) {
    $content = $post['content']['rendered'];
    $word_count = str_word_count( strip_tags( $content ) );
    return ceil( $word_count / 200 ); // 200 words per minute
}

function get_author_info( $post ) {
    $author_id = $post['author'];
    return array(
        'name' => get_the_author_meta( 'display_name', $author_id ),
        'bio' => get_the_author_meta( 'description', $author_id ),
        'avatar' => get_avatar_url( $author_id )
    );
}
```
