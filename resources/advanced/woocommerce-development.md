# WooCommerce Development

Comprehensive guide to WooCommerce development, customization, and extension.

## WooCommerce Fundamentals

### Basic WooCommerce Setup

```php
// Check if WooCommerce is active
if (class_exists('WooCommerce')) {
    // WooCommerce is active
    $woocommerce = WC();
}

// Check if WooCommerce functions are available
if (function_exists('wc_get_product')) {
    $product = wc_get_product($product_id);
}

// Initialize WooCommerce in custom code
function init_woocommerce() {
    if (!class_exists('WooCommerce')) {
        add_action('admin_notices', function() {
            echo '<div class="error"><p>WooCommerce is required for this plugin.</p></div>';
        });
        return;
    }
    
    // WooCommerce is available, proceed with initialization
    add_action('woocommerce_init', 'my_woocommerce_init');
}

function my_woocommerce_init() {
    // WooCommerce has been initialized
    // Your WooCommerce-specific code here
}
```

### Product Management

```php
// Create a simple product programmatically
function create_simple_product($product_data) {
    $product = new WC_Product_Simple();
    
    $product->set_name($product_data['name']);
    $product->set_description($product_data['description']);
    $product->set_short_description($product_data['short_description']);
    $product->set_sku($product_data['sku']);
    $product->set_regular_price($product_data['price']);
    $product->set_sale_price($product_data['sale_price']);
    $product->set_manage_stock(true);
    $product->set_stock_quantity($product_data['stock']);
    $product->set_status('publish');
    
    // Set product categories
    if (!empty($product_data['categories'])) {
        $product->set_category_ids($product_data['categories']);
    }
    
    // Set product tags
    if (!empty($product_data['tags'])) {
        $product->set_tag_ids($product_data['tags']);
    }
    
    // Save the product
    $product_id = $product->save();
    
    return $product_id;
}

// Create a variable product
function create_variable_product($product_data) {
    $product = new WC_Product_Variable();
    
    $product->set_name($product_data['name']);
    $product->set_description($product_data['description']);
    $product->set_status('publish');
    
    $product_id = $product->save();
    
    // Create product attributes
    $attributes = array();
    foreach ($product_data['attributes'] as $attribute_name => $attribute_options) {
        $attribute = new WC_Product_Attribute();
        $attribute->set_name($attribute_name);
        $attribute->set_options($attribute_options);
        $attribute->set_visible(true);
        $attribute->set_variation(true);
        
        $attributes[] = $attribute;
    }
    
    $product->set_attributes($attributes);
    $product->save();
    
    // Create variations
    foreach ($product_data['variations'] as $variation_data) {
        create_product_variation($product_id, $variation_data);
    }
    
    return $product_id;
}

// Create product variation
function create_product_variation($parent_id, $variation_data) {
    $variation = new WC_Product_Variation();
    
    $variation->set_parent_id($parent_id);
    $variation->set_regular_price($variation_data['price']);
    $variation->set_sku($variation_data['sku']);
    $variation->set_manage_stock(true);
    $variation->set_stock_quantity($variation_data['stock']);
    
    // Set variation attributes
    $attributes = array();
    foreach ($variation_data['attributes'] as $attribute_name => $attribute_value) {
        $attributes[strtolower($attribute_name)] = $attribute_value;
    }
    $variation->set_attributes($attributes);
    
    $variation->save();
    
    return $variation->get_id();
}

// Get product data
function get_product_info($product_id) {
    $product = wc_get_product($product_id);
    
    if (!$product) {
        return false;
    }
    
    $product_data = array(
        'id' => $product->get_id(),
        'name' => $product->get_name(),
        'type' => $product->get_type(),
        'status' => $product->get_status(),
        'featured' => $product->get_featured(),
        'description' => $product->get_description(),
        'short_description' => $product->get_short_description(),
        'sku' => $product->get_sku(),
        'price' => $product->get_price(),
        'regular_price' => $product->get_regular_price(),
        'sale_price' => $product->get_sale_price(),
        'stock_status' => $product->get_stock_status(),
        'stock_quantity' => $product->get_stock_quantity(),
        'weight' => $product->get_weight(),
        'dimensions' => array(
            'length' => $product->get_length(),
            'width' => $product->get_width(),
            'height' => $product->get_height()
        ),
        'categories' => wp_get_post_terms($product_id, 'product_cat', array('fields' => 'names')),
        'tags' => wp_get_post_terms($product_id, 'product_tag', array('fields' => 'names')),
        'gallery_image_ids' => $product->get_gallery_image_ids(),
        'featured_image_id' => $product->get_image_id()
    );
    
    return $product_data;
}
```

## Order Management

### Order Processing

```php
// Create an order programmatically
function create_woocommerce_order($order_data) {
    $order = wc_create_order();
    
    if (is_wp_error($order)) {
        return $order;
    }
    
    // Set customer information
    if (!empty($order_data['customer_id'])) {
        $order->set_customer_id($order_data['customer_id']);
    }
    
    // Set billing address
    if (!empty($order_data['billing'])) {
        $order->set_billing_first_name($order_data['billing']['first_name']);
        $order->set_billing_last_name($order_data['billing']['last_name']);
        $order->set_billing_company($order_data['billing']['company']);
        $order->set_billing_address_1($order_data['billing']['address_1']);
        $order->set_billing_address_2($order_data['billing']['address_2']);
        $order->set_billing_city($order_data['billing']['city']);
        $order->set_billing_state($order_data['billing']['state']);
        $order->set_billing_postcode($order_data['billing']['postcode']);
        $order->set_billing_country($order_data['billing']['country']);
        $order->set_billing_email($order_data['billing']['email']);
        $order->set_billing_phone($order_data['billing']['phone']);
    }
    
    // Set shipping address
    if (!empty($order_data['shipping'])) {
        $order->set_shipping_first_name($order_data['shipping']['first_name']);
        $order->set_shipping_last_name($order_data['shipping']['last_name']);
        $order->set_shipping_company($order_data['shipping']['company']);
        $order->set_shipping_address_1($order_data['shipping']['address_1']);
        $order->set_shipping_address_2($order_data['shipping']['address_2']);
        $order->set_shipping_city($order_data['shipping']['city']);
        $order->set_shipping_state($order_data['shipping']['state']);
        $order->set_shipping_postcode($order_data['shipping']['postcode']);
        $order->set_shipping_country($order_data['shipping']['country']);
    }
    
    // Add products to order
    foreach ($order_data['items'] as $item_data) {
        $product = wc_get_product($item_data['product_id']);
        
        if ($product) {
            $order->add_product($product, $item_data['quantity'], array(
                'variation' => $item_data['variation'] ?? array(),
                'totals' => array(
                    'subtotal' => $item_data['subtotal'] ?? $product->get_price() * $item_data['quantity'],
                    'total' => $item_data['total'] ?? $product->get_price() * $item_data['quantity']
                )
            ));
        }
    }
    
    // Set shipping method
    if (!empty($order_data['shipping_method'])) {
        $shipping_item = new WC_Order_Item_Shipping();
        $shipping_item->set_method_title($order_data['shipping_method']['title']);
        $shipping_item->set_method_id($order_data['shipping_method']['id']);
        $shipping_item->set_total($order_data['shipping_method']['cost']);
        $order->add_item($shipping_item);
    }
    
    // Set payment method
    if (!empty($order_data['payment_method'])) {
        $order->set_payment_method($order_data['payment_method']);
        $order->set_payment_method_title($order_data['payment_method_title'] ?? '');
    }
    
    // Calculate totals
    $order->calculate_totals();
    
    // Set order status
    $order->set_status($order_data['status'] ?? 'pending');
    
    // Save the order
    $order->save();
    
    return $order->get_id();
}

// Update order status
function update_order_status($order_id, $new_status, $note = '') {
    $order = wc_get_order($order_id);
    
    if (!$order) {
        return new WP_Error('order_not_found', 'Order not found');
    }
    
    $order->update_status($new_status, $note);
    
    return true;
}

// Get order information
function get_order_details($order_id) {
    $order = wc_get_order($order_id);
    
    if (!$order) {
        return false;
    }
    
    $order_data = array(
        'id' => $order->get_id(),
        'number' => $order->get_order_number(),
        'status' => $order->get_status(),
        'date_created' => $order->get_date_created()->format('Y-m-d H:i:s'),
        'date_modified' => $order->get_date_modified()->format('Y-m-d H:i:s'),
        'total' => $order->get_total(),
        'subtotal' => $order->get_subtotal(),
        'shipping_total' => $order->get_shipping_total(),
        'tax_total' => $order->get_total_tax(),
        'currency' => $order->get_currency(),
        'payment_method' => $order->get_payment_method(),
        'payment_method_title' => $order->get_payment_method_title(),
        'customer_id' => $order->get_customer_id(),
        'billing' => $order->get_billing(),
        'shipping' => $order->get_shipping(),
        'items' => array()
    );
    
    // Get order items
    foreach ($order->get_items() as $item_id => $item) {
        $order_data['items'][] = array(
            'id' => $item_id,
            'product_id' => $item->get_product_id(),
            'variation_id' => $item->get_variation_id(),
            'name' => $item->get_name(),
            'quantity' => $item->get_quantity(),
            'subtotal' => $item->get_subtotal(),
            'total' => $item->get_total(),
            'meta_data' => $item->get_meta_data()
        );
    }
    
    return $order_data;
}
```

### Order Hooks and Filters

```php
// Order status change hooks
add_action('woocommerce_order_status_changed', 'handle_order_status_change', 10, 4);

function handle_order_status_change($order_id, $old_status, $new_status, $order) {
    switch ($new_status) {
        case 'processing':
            // Order is being processed
            send_order_confirmation_email($order);
            break;
            
        case 'completed':
            // Order is completed
            send_order_completion_email($order);
            grant_digital_products($order);
            break;
            
        case 'cancelled':
            // Order is cancelled
            restore_stock_levels($order);
            send_cancellation_email($order);
            break;
    }
}

// Custom order status
add_action('init', 'register_custom_order_status');

function register_custom_order_status() {
    register_post_status('wc-custom-status', array(
        'label' => 'Custom Status',
        'public' => true,
        'exclude_from_search' => false,
        'show_in_admin_all_list' => true,
        'show_in_admin_status_list' => true,
        'label_count' => _n_noop('Custom Status <span class="count">(%s)</span>', 'Custom Status <span class="count">(%s)</span>')
    ));
}

add_filter('wc_order_statuses', 'add_custom_order_status');

function add_custom_order_status($order_statuses) {
    $order_statuses['wc-custom-status'] = 'Custom Status';
    return $order_statuses;
}

// Order item meta
add_action('woocommerce_checkout_create_order_line_item', 'add_custom_order_item_meta', 10, 4);

function add_custom_order_item_meta($item, $cart_item_key, $values, $order) {
    if (!empty($values['custom_field'])) {
        $item->add_meta_data('Custom Field', $values['custom_field']);
    }
}

// Order totals modification
add_action('woocommerce_cart_calculate_fees', 'add_custom_cart_fee');

function add_custom_cart_fee() {
    if (is_admin() && !defined('DOING_AJAX')) {
        return;
    }
    
    $cart = WC()->cart;
    
    if ($cart->get_cart_contents_count() > 5) {
        $cart->add_fee('Bulk Discount', -10); // $10 discount
    }
}
```

## Payment Gateway Development

### Custom Payment Gateway

```php
// Custom payment gateway class
class WC_Custom_Payment_Gateway extends WC_Payment_Gateway {
    
    public function __construct() {
        $this->id = 'custom_payment';
        $this->icon = '';
        $this->has_fields = true;
        $this->method_title = 'Custom Payment Gateway';
        $this->method_description = 'Custom payment gateway for WooCommerce';
        
        // Load the settings
        $this->init_form_fields();
        $this->init_settings();
        
        // Define user set variables
        $this->title = $this->get_option('title');
        $this->description = $this->get_option('description');
        $this->enabled = $this->get_option('enabled');
        $this->testmode = 'yes' === $this->get_option('testmode');
        $this->api_key = $this->testmode ? $this->get_option('test_api_key') : $this->get_option('api_key');
        
        // Actions
        add_action('woocommerce_update_options_payment_gateways_' . $this->id, array($this, 'process_admin_options'));
        add_action('woocommerce_receipt_' . $this->id, array($this, 'receipt_page'));
    }
    
    public function init_form_fields() {
        $this->form_fields = array(
            'enabled' => array(
                'title' => 'Enable/Disable',
                'type' => 'checkbox',
                'label' => 'Enable Custom Payment Gateway',
                'default' => 'no'
            ),
            'title' => array(
                'title' => 'Title',
                'type' => 'text',
                'description' => 'This controls the title which the user sees during checkout.',
                'default' => 'Custom Payment',
                'desc_tip' => true,
            ),
            'description' => array(
                'title' => 'Description',
                'type' => 'textarea',
                'description' => 'This controls the description which the user sees during checkout.',
                'default' => 'Pay with your custom payment method.',
            ),
            'testmode' => array(
                'title' => 'Test mode',
                'type' => 'checkbox',
                'label' => 'Enable Test Mode',
                'default' => 'yes',
                'description' => 'Place the payment gateway in test mode using test API keys.',
            ),
            'test_api_key' => array(
                'title' => 'Test API Key',
                'type' => 'password',
            ),
            'api_key' => array(
                'title' => 'API Key',
                'type' => 'password',
            ),
        );
    }
    
    public function payment_fields() {
        if ($this->description) {
            echo wpautop(wp_kses_post($this->description));
        }
        
        echo '<fieldset id="wc-' . esc_attr($this->id) . '-cc-form" class="wc-credit-card-form wc-payment-form" style="background:transparent;">';
        
        // Add this action hook if you want your custom payment gateway to support it
        do_action('woocommerce_credit_card_form_start', $this->id);
        
        echo '<div class="form-row form-row-wide">
                <label>Card Number <span class="required">*</span></label>
                <input id="' . esc_attr($this->id) . '-card-number" name="' . esc_attr($this->id) . '-card-number" type="text" autocomplete="off" />
            </div>
            <div class="form-row form-row-first">
                <label>Expiry Date <span class="required">*</span></label>
                <input id="' . esc_attr($this->id) . '-card-expiry" name="' . esc_attr($this->id) . '-card-expiry" type="text" autocomplete="off" placeholder="MM / YY" />
            </div>
            <div class="form-row form-row-last">
                <label>Card Code (CVC) <span class="required">*</span></label>
                <input id="' . esc_attr($this->id) . '-card-cvc" name="' . esc_attr($this->id) . '-card-cvc" type="text" autocomplete="off" placeholder="CVC" />
            </div>
            <div class="clear"></div>';
        
        do_action('woocommerce_credit_card_form_end', $this->id);
        
        echo '<div class="clear"></div></fieldset>';
    }
    
    public function validate_fields() {
        if (empty($_POST[$this->id . '-card-number'])) {
            wc_add_notice('Card number is required!', 'error');
            return false;
        }
        
        if (empty($_POST[$this->id . '-card-expiry'])) {
            wc_add_notice('Card expiry is required!', 'error');
            return false;
        }
        
        if (empty($_POST[$this->id . '-card-cvc'])) {
            wc_add_notice('Card CVC is required!', 'error');
            return false;
        }
        
        return true;
    }
    
    public function process_payment($order_id) {
        global $woocommerce;
        
        $order = wc_get_order($order_id);
        
        // Validate fields
        if (!$this->validate_fields()) {
            return array('result' => 'fail');
        }
        
        // Process payment with external API
        $payment_result = $this->process_external_payment($order);
        
        if ($payment_result['success']) {
            // Payment successful
            $order->payment_complete();
            $order->reduce_order_stock();
            
            // Remove cart
            $woocommerce->cart->empty_cart();
            
            // Return success
            return array(
                'result' => 'success',
                'redirect' => $this->get_return_url($order)
            );
        } else {
            // Payment failed
            wc_add_notice('Payment failed: ' . $payment_result['message'], 'error');
            return array('result' => 'fail');
        }
    }
    
    private function process_external_payment($order) {
        // Simulate API call
        $card_number = sanitize_text_field($_POST[$this->id . '-card-number']);
        $card_expiry = sanitize_text_field($_POST[$this->id . '-card-expiry']);
        $card_cvc = sanitize_text_field($_POST[$this->id . '-card-cvc']);
        
        // Here you would make an actual API call to your payment processor
        // For demo purposes, we'll simulate a successful payment
        
        $api_response = array(
            'success' => true,
            'transaction_id' => 'TXN_' . time(),
            'message' => 'Payment processed successfully'
        );
        
        return $api_response;
    }
}

// Register the gateway
add_filter('woocommerce_payment_gateways', 'add_custom_payment_gateway');

function add_custom_payment_gateway($gateways) {
    $gateways[] = 'WC_Custom_Payment_Gateway';
    return $gateways;
}
```

## Shipping and Tax

### Custom Shipping Method

```php
// Custom shipping method
class WC_Custom_Shipping_Method extends WC_Shipping_Method {
    
    public function __construct($instance_id = 0) {
        $this->id = 'custom_shipping';
        $this->instance_id = absint($instance_id);
        $this->method_title = 'Custom Shipping';
        $this->method_description = 'Custom shipping method for WooCommerce';
        
        $this->supports = array(
            'shipping-zones',
            'instance-settings',
            'instance-settings-modal',
        );
        
        $this->init();
        
        $this->enabled = isset($this->settings['enabled']) ? $this->settings['enabled'] : 'yes';
        $this->title = isset($this->settings['title']) ? $this->settings['title'] : 'Custom Shipping';
    }
    
    public function init() {
        $this->init_form_fields();
        $this->init_settings();
        
        add_action('woocommerce_update_options_shipping_' . $this->id, array($this, 'process_admin_options'));
    }
    
    public function init_form_fields() {
        $this->instance_form_fields = array(
            'title' => array(
                'title' => 'Method Title',
                'type' => 'text',
                'description' => 'This controls the title which the user sees during checkout.',
                'default' => 'Custom Shipping',
                'desc_tip' => true,
            ),
            'cost' => array(
                'title' => 'Cost',
                'type' => 'text',
                'description' => 'Cost for this shipping method.',
                'default' => '0',
                'desc_tip' => true,
            ),
            'free_shipping_threshold' => array(
                'title' => 'Free Shipping Threshold',
                'type' => 'text',
                'description' => 'Minimum order amount for free shipping.',
                'default' => '100',
                'desc_tip' => true,
            ),
        );
    }
    
    public function calculate_shipping($package = array()) {
        $cost = $this->get_option('cost', 0);
        $free_threshold = $this->get_option('free_shipping_threshold', 100);
        
        // Check if free shipping applies
        $cart_total = WC()->cart->get_cart_contents_total();
        
        if ($cart_total >= $free_threshold) {
            $cost = 0;
        }
        
        $rate = array(
            'id' => $this->get_rate_id(),
            'label' => $this->title,
            'cost' => $cost,
            'package' => $package,
        );
        
        $this->add_rate($rate);
    }
}

// Register the shipping method
add_action('woocommerce_shipping_init', 'custom_shipping_method_init');

function custom_shipping_method_init() {
    if (!class_exists('WC_Custom_Shipping_Method')) {
        // Include the shipping method class file
        // include_once plugin_dir_path(__FILE__) . 'class-wc-custom-shipping-method.php';
    }
}

add_filter('woocommerce_shipping_methods', 'add_custom_shipping_method');

function add_custom_shipping_method($methods) {
    $methods['custom_shipping'] = 'WC_Custom_Shipping_Method';
    return $methods;
}
```

### Tax Calculations

```php
// Custom tax calculations
add_filter('woocommerce_calc_tax', 'custom_tax_calculation', 10, 5);

function custom_tax_calculation($taxes, $price, $rates, $price_includes_tax, $suppress_rounding) {
    // Custom tax logic here
    if (is_product_category('digital-products')) {
        // Apply different tax rate for digital products
        $digital_tax_rate = 0.08; // 8% tax for digital products
        $tax_amount = $price * $digital_tax_rate;
        
        return array($tax_amount);
    }
    
    return $taxes;
}

// Add custom tax classes
add_filter('woocommerce_tax_classes', 'add_custom_tax_classes');

function add_custom_tax_classes($tax_classes) {
    $tax_classes[] = 'Reduced Rate';
    $tax_classes[] = 'Zero Rate';
    
    return $tax_classes;
}
```

## Product Customization

### Custom Product Fields

```php
// Add custom fields to product data tabs
add_filter('woocommerce_product_data_tabs', 'add_custom_product_tab');

function add_custom_product_tab($tabs) {
    $tabs['custom_tab'] = array(
        'label' => 'Custom Fields',
        'target' => 'custom_product_data',
        'class' => array('show_if_simple', 'show_if_variable'),
    );
    
    return $tabs;
}

// Add custom fields content
add_action('woocommerce_product_data_panels', 'add_custom_product_fields');

function add_custom_product_fields() {
    global $post;
    
    echo '<div id="custom_product_data" class="panel woocommerce_options_panel">';
    
    woocommerce_wp_text_input(array(
        'id' => '_custom_field',
        'label' => 'Custom Field',
        'placeholder' => 'Enter custom value',
        'desc_tip' => true,
        'description' => 'This is a custom field for the product.',
    ));
    
    woocommerce_wp_textarea_input(array(
        'id' => '_custom_description',
        'label' => 'Custom Description',
        'placeholder' => 'Enter custom description',
        'rows' => 5,
        'cols' => 20,
    ));
    
    echo '</div>';
}

// Save custom fields
add_action('woocommerce_process_product_meta', 'save_custom_product_fields');

function save_custom_product_fields($post_id) {
    $custom_field = $_POST['_custom_field'];
    if (!empty($custom_field)) {
        update_post_meta($post_id, '_custom_field', esc_attr($custom_field));
    }
    
    $custom_description = $_POST['_custom_description'];
    if (!empty($custom_description)) {
        update_post_meta($post_id, '_custom_description', esc_textarea($custom_description));
    }
}

// Display custom fields on frontend
add_action('woocommerce_single_product_summary', 'display_custom_product_fields', 25);

function display_custom_product_fields() {
    global $product;
    
    $custom_field = get_post_meta($product->get_id(), '_custom_field', true);
    $custom_description = get_post_meta($product->get_id(), '_custom_description', true);
    
    if (!empty($custom_field)) {
        echo '<div class="custom-field"><strong>Custom Field:</strong> ' . esc_html($custom_field) . '</div>';
    }
    
    if (!empty($custom_description)) {
        echo '<div class="custom-description"><strong>Custom Description:</strong><br>' . wp_kses_post($custom_description) . '</div>';
    }
}
```

### Product Variations

```php
// Add custom fields to product variations
add_action('woocommerce_product_after_variable_attributes', 'add_custom_variation_fields', 10, 3);

function add_custom_variation_fields($loop, $variation_data, $variation) {
    woocommerce_wp_text_input(array(
        'id' => '_custom_variation_field[' . $loop . ']',
        'name' => '_custom_variation_field[' . $loop . ']',
        'label' => 'Custom Variation Field',
        'value' => get_post_meta($variation->ID, '_custom_variation_field', true),
        'wrapper_class' => 'form-row form-row-full',
    ));
}

// Save custom variation fields
add_action('woocommerce_save_product_variation', 'save_custom_variation_fields', 10, 2);

function save_custom_variation_fields($variation_id, $loop) {
    $custom_field = $_POST['_custom_variation_field'][$loop];
    if (isset($custom_field)) {
        update_post_meta($variation_id, '_custom_variation_field', esc_attr($custom_field));
    }
}

// Display custom variation fields on frontend
add_filter('woocommerce_available_variation', 'add_custom_variation_data', 10, 3);

function add_custom_variation_data($variation_data, $product, $variation) {
    $custom_field = get_post_meta($variation->get_id(), '_custom_variation_field', true);
    
    if (!empty($custom_field)) {
        $variation_data['custom_field'] = $custom_field;
    }
    
    return $variation_data;
}
```

## Cart and Checkout Customization

### Cart Modifications

```php
// Add custom cart item meta
add_filter('woocommerce_add_cart_item_data', 'add_custom_cart_item_data', 10, 3);

function add_custom_cart_item_data($cart_item_data, $product_id, $variation_id) {
    if (isset($_POST['custom_field'])) {
        $cart_item_data['custom_field'] = sanitize_text_field($_POST['custom_field']);
    }
    
    return $cart_item_data;
}

// Display custom cart item meta
add_filter('woocommerce_get_item_data', 'display_custom_cart_item_data', 10, 2);

function display_custom_cart_item_data($item_data, $cart_item) {
    if (isset($cart_item['custom_field'])) {
        $item_data[] = array(
            'name' => 'Custom Field',
            'value' => $cart_item['custom_field']
        );
    }
    
    return $item_data;
}

// Custom cart item price
add_action('woocommerce_before_calculate_totals', 'custom_cart_item_price', 10, 1);

function custom_cart_item_price($cart_object) {
    foreach ($cart_object->get_cart() as $cart_item) {
        if (isset($cart_item['custom_field']) && $cart_item['custom_field'] === 'special') {
            // Apply special pricing
            $original_price = $cart_item['data']->get_price();
            $special_price = $original_price * 0.9; // 10% discount
            $cart_item['data']->set_price($special_price);
        }
    }
}
```

### Checkout Customization

```php
// Add custom checkout fields
add_filter('woocommerce_checkout_fields', 'add_custom_checkout_fields');

function add_custom_checkout_fields($fields) {
    $fields['billing']['custom_field'] = array(
        'type' => 'text',
        'label' => 'Custom Field',
        'placeholder' => 'Enter custom value',
        'required' => true,
        'class' => array('form-row-wide'),
        'priority' => 25,
    );
    
    return $fields;
}

// Validate custom checkout fields
add_action('woocommerce_checkout_process', 'validate_custom_checkout_fields');

function validate_custom_checkout_fields() {
    if (empty($_POST['custom_field'])) {
        wc_add_notice('Custom field is required!', 'error');
    }
}

// Save custom checkout fields
add_action('woocommerce_checkout_update_order_meta', 'save_custom_checkout_fields');

function save_custom_checkout_fields($order_id) {
    if (!empty($_POST['custom_field'])) {
        update_post_meta($order_id, 'custom_field', sanitize_text_field($_POST['custom_field']));
    }
}

// Display custom fields in admin
add_action('woocommerce_admin_order_data_after_billing_address', 'display_custom_fields_in_admin');

function display_custom_fields_in_admin($order) {
    $custom_field = get_post_meta($order->get_id(), 'custom_field', true);
    
    if (!empty($custom_field)) {
        echo '<p><strong>Custom Field:</strong> ' . esc_html($custom_field) . '</p>';
    }
}
```

## Email Customization

### Custom Email Templates

```php
// Custom email for order completion
add_action('woocommerce_email_order_details', 'add_custom_email_content', 10, 4);

function add_custom_email_content($order, $sent_to_admin, $plain_text, $email) {
    if ($email->id === 'customer_completed_order') {
        echo '<h3>Thank you for your order!</h3>';
        echo '<p>We appreciate your business and hope you enjoy your purchase.</p>';
    }
}

// Add custom email fields
add_filter('woocommerce_email_order_meta_fields', 'add_custom_email_fields', 10, 3);

function add_custom_email_fields($fields, $sent_to_admin, $order) {
    $custom_field = get_post_meta($order->get_id(), 'custom_field', true);
    
    if (!empty($custom_field)) {
        $fields['custom_field'] = array(
            'label' => 'Custom Field',
            'value' => $custom_field,
        );
    }
    
    return $fields;
}

// Custom email template
class WC_Custom_Email extends WC_Email {
    
    public function __construct() {
        $this->id = 'custom_email';
        $this->title = 'Custom Email';
        $this->description = 'Custom email notification';
        
        $this->heading = 'Custom Email Heading';
        $this->subject = 'Custom Email Subject';
        
        $this->template_html = 'emails/custom-email.php';
        $this->template_plain = 'emails/plain/custom-email.php';
        
        parent::__construct();
    }
    
    public function trigger($order_id) {
        $this->object = wc_get_order($order_id);
        
        if (!$this->is_enabled() || !$this->get_recipient()) {
            $this->send($this->get_recipient(), $this->get_subject(), $this->get_content(), $this->get_headers(), $this->get_attachments());
        }
    }
    
    public function get_content_html() {
        return wc_get_template_html($this->template_html, array(
            'order' => $this->object,
            'email_heading' => $this->get_heading(),
            'additional_content' => $this->get_additional_content(),
            'sent_to_admin' => false,
            'plain_text' => false,
            'email' => $this,
        ), '', plugin_dir_path(__FILE__) . 'templates/');
    }
    
    public function get_content_plain() {
        return wc_get_template_html($this->template_plain, array(
            'order' => $this->object,
            'email_heading' => $this->get_heading(),
            'additional_content' => $this->get_additional_content(),
            'sent_to_admin' => false,
            'plain_text' => true,
            'email' => $this,
        ), '', plugin_dir_path(__FILE__) . 'templates/');
    }
}

// Register custom email
add_filter('woocommerce_email_classes', 'register_custom_email');

function register_custom_email($email_classes) {
    $email_classes['WC_Custom_Email'] = new WC_Custom_Email();
    return $email_classes;
}
```

## API Integration

### WooCommerce REST API

```php
// Custom REST API endpoints
add_action('rest_api_init', 'register_custom_woocommerce_endpoints');

function register_custom_woocommerce_endpoints() {
    register_rest_route('wc/v3', '/custom-products', array(
        'methods' => 'GET',
        'callback' => 'get_custom_products',
        'permission_callback' => 'check_api_permission',
    ));
    
    register_rest_route('wc/v3', '/custom-orders', array(
        'methods' => 'POST',
        'callback' => 'create_custom_order',
        'permission_callback' => 'check_api_permission',
        'args' => array(
            'customer_id' => array(
                'required' => true,
                'type' => 'integer',
            ),
            'products' => array(
                'required' => true,
                'type' => 'array',
            ),
        ),
    ));
}

function check_api_permission($request) {
    return current_user_can('manage_woocommerce');
}

function get_custom_products($request) {
    $products = wc_get_products(array(
        'limit' => 10,
        'status' => 'publish',
    ));
    
    $custom_products = array();
    
    foreach ($products as $product) {
        $custom_products[] = array(
            'id' => $product->get_id(),
            'name' => $product->get_name(),
            'price' => $product->get_price(),
            'sku' => $product->get_sku(),
            'custom_field' => get_post_meta($product->get_id(), '_custom_field', true),
        );
    }
    
    return rest_ensure_response($custom_products);
}

function create_custom_order($request) {
    $customer_id = $request->get_param('customer_id');
    $products = $request->get_param('products');
    
    $order_data = array(
        'customer_id' => $customer_id,
        'status' => 'pending',
        'items' => array(),
    );
    
    foreach ($products as $product_data) {
        $order_data['items'][] = array(
            'product_id' => $product_data['id'],
            'quantity' => $product_data['quantity'],
        );
    }
    
    $order_id = create_woocommerce_order($order_data);
    
    if (is_wp_error($order_id)) {
        return new WP_REST_Response(array('error' => $order_id->get_error_message()), 400);
    }
    
    return rest_ensure_response(array('order_id' => $order_id));
}
```

## Performance Optimization

### WooCommerce Performance

```php
// Optimize WooCommerce queries
add_action('pre_get_posts', 'optimize_woocommerce_queries');

function optimize_woocommerce_queries($query) {
    if (is_admin() || !$query->is_main_query()) {
        return;
    }
    
    // Optimize shop page queries
    if (is_shop() || is_product_category() || is_product_tag()) {
        $query->set('posts_per_page', 12);
        $query->set('meta_query', array(
            array(
                'key' => '_stock_status',
                'value' => 'instock',
                'compare' => '='
            )
        ));
    }
}

// Cache product data
function cache_product_data($product_id) {
    $cache_key = 'product_data_' . $product_id;
    $cached_data = get_transient($cache_key);
    
    if ($cached_data === false) {
        $product = wc_get_product($product_id);
        
        $product_data = array(
            'id' => $product->get_id(),
            'name' => $product->get_name(),
            'price' => $product->get_price(),
            'stock_status' => $product->get_stock_status(),
            'rating' => $product->get_average_rating(),
        );
        
        set_transient($cache_key, $product_data, HOUR_IN_SECONDS);
        return $product_data;
    }
    
    return $cached_data;
}

// Clear product cache when product is updated
add_action('woocommerce_update_product', 'clear_product_cache');

function clear_product_cache($product_id) {
    $cache_key = 'product_data_' . $product_id;
    delete_transient($cache_key);
}

// Optimize cart and checkout
add_action('wp_enqueue_scripts', 'optimize_woocommerce_scripts');

function optimize_woocommerce_scripts() {
    // Only load WooCommerce scripts on WooCommerce pages
    if (!is_woocommerce() && !is_cart() && !is_checkout() && !is_account_page()) {
        wp_dequeue_script('wc-add-to-cart');
        wp_dequeue_script('wc-cart-fragments');
        wp_dequeue_script('woocommerce');
    }
}
```

## Best Practices

### Development Guidelines

```php
// WooCommerce development best practices

// 1. Always check if WooCommerce is active
function my_woocommerce_function() {
    if (!class_exists('WooCommerce')) {
        return false;
    }
    
    // WooCommerce-specific code here
}

// 2. Use WooCommerce hooks and filters
add_action('woocommerce_thankyou', 'custom_thankyou_action');

function custom_thankyou_action($order_id) {
    // Custom action after order completion
}

// 3. Proper error handling
function safe_woocommerce_operation($product_id) {
    try {
        $product = wc_get_product($product_id);
        
        if (!$product) {
            throw new Exception('Product not found');
        }
        
        // Perform operation
        
    } catch (Exception $e) {
        error_log('WooCommerce Error: ' . $e->getMessage());
        return false;
    }
}

// 4. Use WooCommerce functions instead of WordPress functions
// Good
$price = $product->get_price();
$stock = $product->get_stock_quantity();

// Bad
$price = get_post_meta($product_id, '_price', true);
$stock = get_post_meta($product_id, '_stock', true);

// 5. Follow WooCommerce coding standards
// Use proper sanitization and validation
$clean_data = sanitize_text_field($_POST['data']);
$validated_data = wc_clean($clean_data);

// 6. Use WooCommerce transients for caching
$cache_key = 'woocommerce_data_' . $product_id;
$cached_data = get_transient($cache_key);

if ($cached_data === false) {
    $cached_data = expensive_operation();
    set_transient($cache_key, $cached_data, DAY_IN_SECONDS);
}
```

## Official Documentation

https://woocommerce.com/document/woocommerce-rest-api/
https://github.com/woocommerce/woocommerce/wiki
https://developer.woocommerce.com/
