---
difficulty: Intermediate
tags: [hooks, save-post, meta, custom-fields]
related: [hooks/action-hooks, admin/meta-box]
use_case: Running code when posts are saved
---

# Save Post Hook

```php
// Basic save post hook
add_action( 'save_post', 'my_save_post_function', 10, 3 );
function my_save_post_function( $post_id, $post, $update ) {
    // Check if it's an update (not new post)
    if ( ! $update ) {
        return;
    }
    
    // Check post type
    if ( $post->post_type !== 'post' ) {
        return;
    }
    
    // Check if it's not an autosave
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    
    // Check user has permission
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }
    
    // Your code here
    // Update post meta, trigger notifications, etc.
    update_post_meta( $post_id, '_last_modified_by', get_current_user_id() );
}

// Save post with meta box data
add_action( 'save_post', 'save_custom_meta', 10, 2 );
function save_custom_meta( $post_id, $post ) {
    // Verify nonce
    if ( ! isset( $_POST['meta_nonce'] ) || 
         ! wp_verify_nonce( $_POST['meta_nonce'], 'save_meta_' . $post_id ) ) {
        return;
    }
    
    // Check autosave
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    
    // Check permissions
    $post_type = get_post_type_object( $post->post_type );
    if ( ! current_user_can( $post_type->cap->edit_post, $post_id ) ) {
        return;
    }
    
    // Save meta
    if ( isset( $_POST['custom_field'] ) ) {
        update_post_meta(
            $post_id,
            '_custom_field',
            sanitize_text_field( $_POST['custom_field'] )
        );
    }
}
```
