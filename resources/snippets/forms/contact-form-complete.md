---
difficulty: Advanced
tags: [forms, contact, email, validation]
related: [forms/ajax-form, security/validate-user-input]
use_case: Complete contact form implementation
---

# Complete Contact Form

```php
// Shortcode for contact form
function contact_form_shortcode() {
    ob_start();
    ?>
    <form id="contact-form" method="post" class="contact-form">
        <?php wp_nonce_field( 'submit_contact', 'contact_nonce' ); ?>
        
        <div class="form-row">
            <label for="contact-name"><?php esc_html_e( 'Name', 'textdomain' ); ?> *</label>
            <input type="text" id="contact-name" name="name" required>
        </div>
        
        <div class="form-row">
            <label for="contact-email"><?php esc_html_e( 'Email', 'textdomain' ); ?> *</label>
            <input type="email" id="contact-email" name="email" required>
        </div>
        
        <div class="form-row">
            <label for="contact-subject"><?php esc_html_e( 'Subject', 'textdomain' ); ?></label>
            <input type="text" id="contact-subject" name="subject">
        </div>
        
        <div class="form-row">
            <label for="contact-message"><?php esc_html_e( 'Message', 'textdomain' ); ?> *</label>
            <textarea id="contact-message" name="message" rows="5" required></textarea>
        </div>
        
        <button type="submit"><?php esc_html_e( 'Send Message', 'textdomain' ); ?></button>
        
        <div id="form-messages"></div>
    </form>
    
    <script>
    jQuery('#contact-form').on('submit', function(e) {
        e.preventDefault();
        
        var formData = jQuery(this).serialize();
        formData += '&action=submit_contact_form';
        
        jQuery.ajax({
            url: '<?php echo admin_url( "admin-ajax.php" ); ?>',
            type: 'POST',
            data: formData,
            beforeSend: function() {
                jQuery('#form-messages').html('<p>Sending...</p>');
            },
            success: function(response) {
                if (response.success) {
                    jQuery('#form-messages').html('<p class="success">' + response.data.message + '</p>');
                    jQuery('#contact-form')[0].reset();
                } else {
                    jQuery('#form-messages').html('<p class="error">' + response.data + '</p>');
                }
            }
        });
    });
    </script>
    <?php
    return ob_get_clean();
}
add_shortcode( 'contact_form', 'contact_form_shortcode' );

// AJAX handler
add_action( 'wp_ajax_submit_contact_form', 'process_contact_form' );
add_action( 'wp_ajax_nopriv_submit_contact_form', 'process_contact_form' );

function process_contact_form() {
    check_ajax_referer( 'submit_contact', 'contact_nonce' );
    
    // Sanitize inputs
    $name = sanitize_text_field( $_POST['name'] );
    $email = sanitize_email( $_POST['email'] );
    $subject = sanitize_text_field( $_POST['subject'] );
    $message = sanitize_textarea_field( $_POST['message'] );
    
    // Validate
    if ( empty( $name ) || empty( $email ) || empty( $message ) ) {
        wp_send_json_error( 'Please fill all required fields' );
    }
    
    if ( ! is_email( $email ) ) {
        wp_send_json_error( 'Invalid email address' );
    }
    
    // Send email
    $to = get_option( 'admin_email' );
    $email_subject = $subject ? $subject : 'Contact Form Submission';
    $email_body = "From: $name <$email>\n\n$message";
    $headers = array( 'Reply-To: ' . $email );
    
    if ( wp_mail( $to, $email_subject, $email_body, $headers ) ) {
        // Save to database
        wp_insert_post( array(
            'post_type' => 'contact_submission',
            'post_title' => $subject,
            'post_content' => $message,
            'post_status' => 'private',
            'meta_input' => array(
                '_contact_name' => $name,
                '_contact_email' => $email
            )
        ));
        
        wp_send_json_success( array( 'message' => 'Thank you! Your message has been sent.' ) );
    } else {
        wp_send_json_error( 'Failed to send message. Please try again.' );
    }
}
```
