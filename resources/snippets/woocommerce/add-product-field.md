# Add Custom Product Field

```php
// Add custom field to product
add_action( 'woocommerce_product_options_general_product_data', 'add_custom_product_field' );
function add_custom_product_field() {
    woocommerce_wp_text_input( array(
        'id' => '_custom_field',
        'label' => __( 'Custom Field', 'textdomain' ),
        'placeholder' => 'Enter value',
        'desc_tip' => true,
        'description' => __( 'Custom field description', 'textdomain' )
    ));
}

// Save custom field
add_action( 'woocommerce_process_product_meta', 'save_custom_product_field' );
function save_custom_product_field( $post_id ) {
    $custom_field = isset( $_POST['_custom_field'] ) ? sanitize_text_field( $_POST['_custom_field'] ) : '';
    update_post_meta( $post_id, '_custom_field', $custom_field );
}

// Display in frontend
add_action( 'woocommerce_single_product_summary', 'display_custom_field', 25 );
function display_custom_field() {
    global $product;
    
    $custom_value = get_post_meta( $product->get_id(), '_custom_field', true );
    
    if ( $custom_value ) {
        echo '<div class="custom-field">' . esc_html( $custom_value ) . '</div>';
    }
}
```
