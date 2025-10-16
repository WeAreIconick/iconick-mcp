# Complete AJAX Form

```php
// HTML Form
<form id="ajax-contact-form">
    <?php wp_nonce_field( 'contact_form', 'contact_nonce' ); ?>
    
    <input type="text" name="name" placeholder="Name" required>
    <input type="email" name="email" placeholder="Email" required>
    <textarea name="message" placeholder="Message" required></textarea>
    <button type="submit">Send</button>
    <div id="form-response"></div>
</form>

// JavaScript
jQuery('#ajax-contact-form').on('submit', function(e) {
    e.preventDefault();
    
    var formData = {
        action: 'submit_contact',
        nonce: jQuery('#contact_nonce').val(),
        name: jQuery('[name="name"]').val(),
        email: jQuery('[name="email"]').val(),
        message: jQuery('[name="message"]').val()
    };
    
    jQuery.post(ajaxurl, formData, function(response) {
        if (response.success) {
            jQuery('#form-response').html('<p class="success">' + response.data.message + '</p>');
            jQuery('#ajax-contact-form')[0].reset();
        } else {
            jQuery('#form-response').html('<p class="error">' + response.data + '</p>');
        }
    });
});

// PHP Handler
add_action( 'wp_ajax_submit_contact', 'handle_contact_submission' );
add_action( 'wp_ajax_nopriv_submit_contact', 'handle_contact_submission' );

function handle_contact_submission() {
    check_ajax_referer( 'contact_form', 'nonce' );
    
    $name = sanitize_text_field( $_POST['name'] );
    $email = sanitize_email( $_POST['email'] );
    $message = sanitize_textarea_field( $_POST['message'] );
    
    if ( empty( $name ) || empty( $email ) || empty( $message ) ) {
        wp_send_json_error( 'All fields are required' );
    }
    
    if ( ! is_email( $email ) ) {
        wp_send_json_error( 'Invalid email address' );
    }
    
    // Send email
    $to = get_option( 'admin_email' );
    $subject = 'Contact Form: ' . $name;
    $body = "From: $name <$email>\n\n$message";
    
    if ( wp_mail( $to, $subject, $body ) ) {
        wp_send_json_success( array( 'message' => 'Thank you! Message sent.' ) );
    } else {
        wp_send_json_error( 'Failed to send message' );
    }
}
```
