# Custom WooCommerce Checkout Field

```php
// Add checkout field
add_action( 'woocommerce_after_order_notes', 'add_custom_checkout_field' );
function add_custom_checkout_field( $checkout ) {
    woocommerce_form_field( 'delivery_notes', array(
        'type' => 'textarea',
        'class' => array( 'form-row-wide' ),
        'label' => __( 'Delivery Notes', 'textdomain' ),
        'placeholder' => __( 'Special delivery instructions', 'textdomain' ),
        'required' => false
    ), $checkout->get_value( 'delivery_notes' ));
}

// Validate field
add_action( 'woocommerce_checkout_process', 'validate_custom_field' );
function validate_custom_field() {
    if ( isset( $_POST['delivery_notes'] ) && empty( $_POST['delivery_notes'] ) ) {
        // Only if you want to make it required
        // wc_add_notice( __( 'Please enter delivery notes', 'textdomain' ), 'error' );
    }
}

// Save field to order meta
add_action( 'woocommerce_checkout_update_order_meta', 'save_custom_checkout_field' );
function save_custom_checkout_field( $order_id ) {
    if ( ! empty( $_POST['delivery_notes'] ) ) {
        update_post_meta(
            $order_id,
            '_delivery_notes',
            sanitize_textarea_field( $_POST['delivery_notes'] )
        );
    }
}

// Display in admin order page
add_action( 'woocommerce_admin_order_data_after_billing_address', 'display_delivery_notes_admin' );
function display_delivery_notes_admin( $order ) {
    $notes = get_post_meta( $order->get_id(), '_delivery_notes', true );
    
    if ( $notes ) {
        echo '<p><strong>' . __( 'Delivery Notes:', 'textdomain' ) . '</strong><br>' . esc_html( $notes ) . '</p>';
    }
}

// Display in order emails
add_action( 'woocommerce_email_order_meta', 'display_delivery_notes_email', 10, 3 );
function display_delivery_notes_email( $order, $sent_to_admin, $plain_text ) {
    $notes = get_post_meta( $order->get_id(), '_delivery_notes', true );
    
    if ( $notes ) {
        echo '<p><strong>' . __( 'Delivery Notes:', 'textdomain' ) . '</strong><br>' . esc_html( $notes ) . '</p>';
    }
}
```
