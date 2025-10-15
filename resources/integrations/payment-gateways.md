# WordPress Payment Gateway Integration

## Stripe Integration

### Basic Stripe Setup
```php
// Enqueue Stripe.js
function enqueue_stripe_scripts() {
    wp_enqueue_script('stripe-js', 'https://js.stripe.com/v3/', array(), null, true);
    wp_enqueue_script('stripe-custom', get_template_directory_uri() . '/js/stripe.js', array('stripe-js'), '1.0.0', true);
    
    wp_localize_script('stripe-custom', 'stripe_vars', array(
        'publishable_key' => get_option('stripe_publishable_key'),
        'ajax_url' => admin_url('admin-ajax.php'),
        'nonce' => wp_create_nonce('stripe_nonce')
    ));
}
add_action('wp_enqueue_scripts', 'enqueue_stripe_scripts');

// Handle Stripe payment
add_action('wp_ajax_process_stripe_payment', 'process_stripe_payment');
add_action('wp_ajax_nopriv_process_stripe_payment', 'process_stripe_payment');

function process_stripe_payment() {
    check_ajax_referer('stripe_nonce', 'nonce');
    
    require_once('stripe-php/init.php');
    
    \Stripe\Stripe::setApiKey(get_option('stripe_secret_key'));
    
    $amount = intval($_POST['amount']) * 100; // Convert to cents
    $currency = sanitize_text_field($_POST['currency']);
    
    try {
        $payment_intent = \Stripe\PaymentIntent::create([
            'amount' => $amount,
            'currency' => $currency,
            'metadata' => [
                'user_id' => get_current_user_id(),
                'order_id' => uniqid()
            ]
        ]);
        
        wp_send_json_success(array(
            'client_secret' => $payment_intent->client_secret
        ));
    } catch (Exception $e) {
        wp_send_json_error($e->getMessage());
    }
}
```

### Stripe Webhook Handler
```php
// Handle Stripe webhooks
add_action('wp_ajax_stripe_webhook', 'handle_stripe_webhook');
add_action('wp_ajax_nopriv_stripe_webhook', 'handle_stripe_webhook');

function handle_stripe_webhook() {
    $payload = file_get_contents('php://input');
    $sig_header = $_SERVER['HTTP_STRIPE_SIGNATURE'];
    $endpoint_secret = get_option('stripe_webhook_secret');
    
    try {
        $event = \Stripe\Webhook::constructEvent($payload, $sig_header, $endpoint_secret);
    } catch (Exception $e) {
        http_response_code(400);
        exit();
    }
    
    switch ($event->type) {
        case 'payment_intent.succeeded':
            $payment_intent = $event->data->object;
            handle_payment_success($payment_intent);
            break;
            
        case 'payment_intent.payment_failed':
            $payment_intent = $event->data->object;
            handle_payment_failure($payment_intent);
            break;
            
        default:
            error_log('Unhandled event type: ' . $event->type);
    }
    
    http_response_code(200);
}

function handle_payment_success($payment_intent) {
    $order_id = $payment_intent->metadata->order_id;
    $amount = $payment_intent->amount / 100;
    
    // Update order status
    update_post_meta($order_id, '_payment_status', 'completed');
    update_post_meta($order_id, '_payment_intent_id', $payment_intent->id);
    
    // Send confirmation email
    send_payment_confirmation_email($order_id);
}

function handle_payment_failure($payment_intent) {
    $order_id = $payment_intent->metadata->order_id;
    
    // Update order status
    update_post_meta($order_id, '_payment_status', 'failed');
    update_post_meta($order_id, '_payment_error', $payment_intent->last_payment_error->message);
}
```

## PayPal Integration

### PayPal REST API Integration
```php
class PayPalIntegration {
    private $client_id;
    private $client_secret;
    private $sandbox;
    
    public function __construct() {
        $this->client_id = get_option('paypal_client_id');
        $this->client_secret = get_option('paypal_client_secret');
        $this->sandbox = get_option('paypal_sandbox') === 'yes';
        
        add_action('wp_ajax_create_paypal_payment', array($this, 'create_payment'));
        add_action('wp_ajax_nopriv_create_paypal_payment', array($this, 'create_payment'));
        
        add_action('wp_ajax_execute_paypal_payment', array($this, 'execute_payment'));
        add_action('wp_ajax_nopriv_execute_paypal_payment', array($this, 'execute_payment'));
    }
    
    public function create_payment() {
        check_ajax_referer('paypal_nonce', 'nonce');
        
        $amount = floatval($_POST['amount']);
        $currency = sanitize_text_field($_POST['currency']);
        $return_url = esc_url($_POST['return_url']);
        $cancel_url = esc_url($_POST['cancel_url']);
        
        $access_token = $this->get_access_token();
        
        $payment_data = array(
            'intent' => 'sale',
            'redirect_urls' => array(
                'return_url' => $return_url,
                'cancel_url' => $cancel_url
            ),
            'payer' => array(
                'payment_method' => 'paypal'
            ),
            'transactions' => array(
                array(
                    'amount' => array(
                        'total' => number_format($amount, 2),
                        'currency' => strtoupper($currency)
                    ),
                    'description' => 'Payment for services'
                )
            )
        );
        
        $response = wp_remote_post($this->get_api_url() . '/v1/payments/payment', array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $access_token,
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode($payment_data)
        ));
        
        if (is_wp_error($response)) {
            wp_send_json_error('Failed to create payment');
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if (isset($data['links'])) {
            foreach ($data['links'] as $link) {
                if ($link['rel'] === 'approval_url') {
                    wp_send_json_success(array(
                        'approval_url' => $link['href'],
                        'payment_id' => $data['id']
                    ));
                }
            }
        }
        
        wp_send_json_error('Invalid response from PayPal');
    }
    
    public function execute_payment() {
        check_ajax_referer('paypal_nonce', 'nonce');
        
        $payment_id = sanitize_text_field($_POST['payment_id']);
        $payer_id = sanitize_text_field($_POST['payer_id']);
        
        $access_token = $this->get_access_token();
        
        $execute_data = array(
            'payer_id' => $payer_id
        );
        
        $response = wp_remote_post($this->get_api_url() . '/v1/payments/payment/' . $payment_id . '/execute', array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $access_token,
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode($execute_data)
        ));
        
        if (is_wp_error($response)) {
            wp_send_json_error('Failed to execute payment');
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if ($data['state'] === 'approved') {
            wp_send_json_success(array(
                'transaction_id' => $data['transactions'][0]['related_resources'][0]['sale']['id'],
                'amount' => $data['transactions'][0]['amount']['total']
            ));
        } else {
            wp_send_json_error('Payment not approved');
        }
    }
    
    private function get_access_token() {
        $response = wp_remote_post($this->get_api_url() . '/v1/oauth2/token', array(
            'headers' => array(
                'Accept' => 'application/json',
                'Accept-Language' => 'en_US',
                'Content-Type' => 'application/x-www-form-urlencoded'
            ),
            'body' => array(
                'grant_type' => 'client_credentials'
            ),
            'httpversion' => '1.1'
        ));
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        return $data['access_token'];
    }
    
    private function get_api_url() {
        return $this->sandbox ? 'https://api.sandbox.paypal.com' : 'https://api.paypal.com';
    }
}

new PayPalIntegration();
```

## Email Service Integration

### Mailchimp Integration
```php
class MailchimpIntegration {
    private $api_key;
    private $list_id;
    
    public function __construct() {
        $this->api_key = get_option('mailchimp_api_key');
        $this->list_id = get_option('mailchimp_list_id');
        
        add_action('wp_ajax_subscribe_to_mailchimp', array($this, 'subscribe_user'));
        add_action('wp_ajax_nopriv_subscribe_to_mailchimp', array($this, 'subscribe_user'));
    }
    
    public function subscribe_user() {
        check_ajax_referer('mailchimp_nonce', 'nonce');
        
        $email = sanitize_email($_POST['email']);
        $first_name = sanitize_text_field($_POST['first_name']);
        $last_name = sanitize_text_field($_POST['last_name']);
        
        if (!is_email($email)) {
            wp_send_json_error('Invalid email address');
        }
        
        $data_center = substr($this->api_key, strpos($this->api_key, '-') + 1);
        $url = 'https://' . $data_center . '.api.mailchimp.com/3.0/lists/' . $this->list_id . '/members';
        
        $member_data = array(
            'email_address' => $email,
            'status' => 'subscribed',
            'merge_fields' => array(
                'FNAME' => $first_name,
                'LNAME' => $last_name
            )
        );
        
        $response = wp_remote_post($url, array(
            'headers' => array(
                'Authorization' => 'Basic ' . base64_encode('user:' . $this->api_key),
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode($member_data)
        ));
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        if (is_wp_error($response)) {
            wp_send_json_error('Failed to subscribe user');
        }
        
        if (isset($data['id'])) {
            wp_send_json_success('Successfully subscribed to newsletter');
        } else {
            wp_send_json_error($data['detail'] ?? 'Unknown error');
        }
    }
}
```

## Social Media Integration

### Twitter API Integration
```php
class TwitterIntegration {
    private $consumer_key;
    private $consumer_secret;
    private $access_token;
    private $access_token_secret;
    
    public function __construct() {
        $this->consumer_key = get_option('twitter_consumer_key');
        $this->consumer_secret = get_option('twitter_consumer_secret');
        $this->access_token = get_option('twitter_access_token');
        $this->access_token_secret = get_option('twitter_access_token_secret');
        
        add_action('publish_post', array($this, 'tweet_new_post'));
    }
    
    public function tweet_new_post($post_id) {
        $post = get_post($post_id);
        
        if ($post->post_status !== 'publish' || $post->post_type !== 'post') {
            return;
        }
        
        $title = $post->post_title;
        $permalink = get_permalink($post_id);
        
        // Shorten URL and create tweet
        $short_url = $this->shorten_url($permalink);
        $tweet_text = $title . ' ' . $short_url;
        
        // Ensure tweet is under 280 characters
        if (strlen($tweet_text) > 280) {
            $max_title_length = 280 - strlen($short_url) - 1;
            $title = substr($title, 0, $max_title_length - 3) . '...';
            $tweet_text = $title . ' ' . $short_url;
        }
        
        $this->post_tweet($tweet_text);
    }
    
    private function post_tweet($status) {
        require_once('twitteroauth/autoload.php');
        
        $connection = new \Abraham\TwitterOAuth\TwitterOAuth(
            $this->consumer_key,
            $this->consumer_secret,
            $this->access_token,
            $this->access_token_secret
        );
        
        $result = $connection->post('statuses/update', array('status' => $status));
        
        if ($connection->getLastHttpCode() === 200) {
            error_log('Tweet posted successfully: ' . $status);
        } else {
            error_log('Failed to post tweet: ' . json_encode($result));
        }
    }
    
    private function shorten_url($url) {
        // Use bit.ly or similar service to shorten URL
        $bitly_token = get_option('bitly_access_token');
        
        $response = wp_remote_post('https://api-ssl.bitly.com/v4/shorten', array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $bitly_token,
                'Content-Type' => 'application/json'
            ),
            'body' => json_encode(array('long_url' => $url))
        ));
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        return $data['link'] ?? $url;
    }
}
```

## Best Practices

1. **Always validate and sanitize** input data
2. **Use HTTPS** for all API communications
3. **Store API keys securely** using WordPress options
4. **Implement proper error handling** and logging
5. **Use webhooks** for real-time updates
6. **Test in sandbox mode** before going live
7. **Follow rate limits** for API calls
8. **Cache API responses** when appropriate
9. **Use nonces** for security
10. **Document API integrations** thoroughly

## Resources

- [Stripe PHP Library](https://github.com/stripe/stripe-php)
- [PayPal REST API Documentation](https://developer.paypal.com/docs/api/)
- [Mailchimp API Documentation](https://mailchimp.com/developer/)
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [WordPress HTTP API](https://developer.wordpress.org/reference/functions/wp_remote_post/)