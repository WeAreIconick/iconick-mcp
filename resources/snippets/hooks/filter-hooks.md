# Common Filter Hooks

```php
// Modify title
add_filter( 'the_title', 'my_custom_title', 10, 2 );

// Modify content
add_filter( 'the_content', 'my_content_filter' );

// Modify excerpt
add_filter( 'the_excerpt', 'my_excerpt_filter' );

// Modify query
add_filter( 'pre_get_posts', 'my_modify_query' );

// Modify upload mime types
add_filter( 'upload_mimes', 'my_upload_mimes' );

// Modify admin columns
add_filter( 'manage_post_posts_columns', 'my_columns' );

// Modify menu items
add_filter( 'wp_nav_menu_items', 'my_menu_items', 10, 2 );
```
