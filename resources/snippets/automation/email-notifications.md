---
difficulty: Beginner
tags: [automation, email, notifications, alerts]
related: [automation/auto-publish, forms/contact-form-complete]
use_case: Automated email notifications
---

# Automated Email Notifications

```php
// Send admin notification on new post
add_action( 'publish_post', 'notify_admin_new_post', 10, 2 );
function notify_admin_new_post( $ID, $post ) {
    $to = get_option( 'admin_email' );
    $subject = 'New Post Published: ' . $post->post_title;
    
    $message = "A new post has been published:\n\n";
    $message .= "Title: {$post->post_title}\n";
    $message .= "Author: " . get_the_author_meta( 'display_name', $post->post_author ) . "\n";
    $message .= "Link: " . get_permalink( $ID ) . "\n";
    
    wp_mail( $to, $subject, $message );
}

// Send email on form submission
function send_contact_notification( $data ) {
    $to = get_option( 'admin_email' );
    $subject = 'Contact Form: ' . $data['subject'];
    
    $message = "New contact form submission:\n\n";
    $message .= "Name: {$data['name']}\n";
    $message .= "Email: {$data['email']}\n\n";
    $message .= "Message:\n{$data['message']}";
    
    $headers = array(
        'Reply-To: ' . $data['email'],
        'Content-Type: text/html; charset=UTF-8'
    );
    
    return wp_mail( $to, $subject, nl2br( $message ), $headers );
}

// Weekly digest email
add_action( 'my_weekly_digest', 'send_weekly_digest' );
function send_weekly_digest() {
    // Get posts from last week
    $posts = get_posts( array(
        'posts_per_page' => -1,
        'date_query' => array(
            array( 'after' => '7 days ago' )
        )
    ));
    
    if ( empty( $posts ) ) {
        return;
    }
    
    $message = '<h2>Weekly Digest</h2>';
    $message .= '<p>Posts published this week:</p><ul>';
    
    foreach ( $posts as $post ) {
        $message .= '<li><a href="' . get_permalink( $post->ID ) . '">' . esc_html( $post->post_title ) . '</a></li>';
    }
    
    $message .= '</ul>';
    
    // Send to subscribers
    $subscribers = get_users( array( 'meta_key' => 'newsletter_subscriber', 'meta_value' => '1' ) );
    
    foreach ( $subscribers as $user ) {
        wp_mail( $user->user_email, 'Weekly Digest', $message, array( 'Content-Type: text/html' ) );
    }
}
```
