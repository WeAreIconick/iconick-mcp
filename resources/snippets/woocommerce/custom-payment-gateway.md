# Custom Payment Gateway

```php
add_action( 'plugins_loaded', 'init_custom_payment_gateway' );
function init_custom_payment_gateway() {
    class WC_Gateway_Custom extends WC_Payment_Gateway {
        
        public function __construct() {
            $this->id = 'custom_gateway';
            $this->icon = '';
            $this->has_fields = false;
            $this->method_title = 'Custom Payment';
            $this->method_description = 'Custom payment gateway';
            
            $this->init_form_fields();
            $this->init_settings();
            
            $this->title = $this->get_option( 'title' );
            $this->description = $this->get_option( 'description' );
            
            add_action( 'woocommerce_update_options_payment_gateways_' . $this->id, array( $this, 'process_admin_options' ) );
        }
        
        public function init_form_fields() {
            $this->form_fields = array(
                'enabled' => array(
                    'title' => 'Enable/Disable',
                    'type' => 'checkbox',
                    'label' => 'Enable Custom Payment',
                    'default' => 'yes'
                ),
                'title' => array(
                    'title' => 'Title',
                    'type' => 'text',
                    'default' => 'Custom Payment'
                ),
                'description' => array(
                    'title' => 'Description',
                    'type' => 'textarea',
                    'default' => 'Pay with custom method'
                )
            );
        }
        
        public function process_payment( $order_id ) {
            $order = wc_get_order( $order_id );
            
            // Process payment here
            // If successful:
            $order->payment_complete();
            
            return array(
                'result' => 'success',
                'redirect' => $this->get_return_url( $order )
            );
        }
    }
}

add_filter( 'woocommerce_payment_gateways', 'add_custom_gateway' );
function add_custom_gateway( $gateways ) {
    $gateways[] = 'WC_Gateway_Custom';
    return $gateways;
}
```
