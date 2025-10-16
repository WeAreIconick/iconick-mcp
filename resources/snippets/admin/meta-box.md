# Add Meta Box

```php
add_action( 'add_meta_boxes', 'my_add_meta_box' );
function my_add_meta_box() {
    add_meta_box(
        'my_meta_box',                    // ID
        __( 'Additional Info', 'textdomain' ),  // Title
        'my_meta_box_html',               // Callback
        'post',                           // Post type
        'side',                           // Context (normal, side, advanced)
        'default'                         // Priority
    );
}

function my_meta_box_html( $post ) {
    wp_nonce_field( 'my_meta_box', 'my_meta_box_nonce' );
    
    $value = get_post_meta( $post->ID, '_my_meta_key', true );
    ?>
    <label for="my_field">
        <?php esc_html_e( 'Custom Field', 'textdomain' ); ?>
    </label>
    <input type="text" id="my_field" name="my_field" value="<?php echo esc_attr( $value ); ?>" class="widefat">
    <?php
}

add_action( 'save_post', 'my_save_meta_box' );
function my_save_meta_box( $post_id ) {
    if ( ! isset( $_POST['my_meta_box_nonce'] ) ||
         ! wp_verify_nonce( $_POST['my_meta_box_nonce'], 'my_meta_box' ) ) {
        return;
    }
    
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }
    
    if ( isset( $_POST['my_field'] ) ) {
        update_post_meta(
            $post_id,
            '_my_meta_key',
            sanitize_text_field( $_POST['my_field'] )
        );
    }
}
```
