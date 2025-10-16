# Mailchimp Integration

```php
// Subscribe user to Mailchimp
function subscribe_to_mailchimp( $email, $first_name = '', $last_name = '' ) {
    $api_key = get_option( 'mailchimp_api_key' );
    $list_id = get_option( 'mailchimp_list_id' );
    
    if ( ! $api_key || ! $list_id ) {
        return new WP_Error( 'missing_config', 'Mailchimp not configured' );
    }
    
    $data_center = substr( $api_key, strpos( $api_key, '-' ) + 1 );
    $url = "https://{$data_center}.api.mailchimp.com/3.0/lists/{$list_id}/members";
    
    $response = wp_remote_post( $url, array(
        'headers' => array(
            'Authorization' => 'Basic ' . base64_encode( 'user:' . $api_key ),
            'Content-Type' => 'application/json'
        ),
        'body' => json_encode( array(
            'email_address' => $email,
            'status' => 'subscribed',
            'merge_fields' => array(
                'FNAME' => $first_name,
                'LNAME' => $last_name
            )
        ))
    ));
    
    if ( is_wp_error( $response ) ) {
        return $response;
    }
    
    $body = json_decode( wp_remote_retrieve_body( $response ), true );
    
    if ( wp_remote_retrieve_response_code( $response ) === 200 ) {
        return true;
    }
    
    return new WP_Error( 'api_error', $body['title'] ?? 'Subscription failed' );
}

// Add subscription form
function mailchimp_subscription_form() {
    ?>
    <form id="mailchimp-form" method="post">
        <?php wp_nonce_field( 'mailchimp_subscribe', 'mailchimp_nonce' ); ?>
        <input type="email" name="email" placeholder="Email" required>
        <button type="submit">Subscribe</button>
    </form>
    
    <script>
    jQuery('#mailchimp-form').on('submit', function(e) {
        e.preventDefault();
        jQuery.post(ajaxurl, {
            action: 'mailchimp_subscribe',
            nonce: jQuery('[name="mailchimp_nonce"]').val(),
            email: jQuery('[name="email"]').val()
        }, function(response) {
            alert(response.data);
        });
    });
    </script>
    <?php
}

add_action( 'wp_ajax_mailchimp_subscribe', 'handle_mailchimp_ajax' );
add_action( 'wp_ajax_nopriv_mailchimp_subscribe', 'handle_mailchimp_ajax' );

function handle_mailchimp_ajax() {
    check_ajax_referer( 'mailchimp_subscribe', 'nonce' );
    
    $email = sanitize_email( $_POST['email'] );
    
    if ( ! is_email( $email ) ) {
        wp_send_json_error( 'Invalid email' );
    }
    
    $result = subscribe_to_mailchimp( $email );
    
    if ( is_wp_error( $result ) ) {
        wp_send_json_error( $result->get_error_message() );
    }
    
    wp_send_json_success( 'Successfully subscribed!' );
}
```
