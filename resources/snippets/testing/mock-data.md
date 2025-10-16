# Create Mock/Test Data

```php
// Create test posts
function create_test_posts( $count = 10 ) {
    for ( $i = 1; $i <= $count; $i++ ) {
        wp_insert_post( array(
            'post_title' => 'Test Post ' . $i,
            'post_content' => 'This is test content for post ' . $i,
            'post_status' => 'publish',
            'post_type' => 'post'
        ));
    }
}

// Create test custom post types
function create_test_portfolio_items( $count = 5 ) {
    for ( $i = 1; $i <= $count; $i++ ) {
        $post_id = wp_insert_post( array(
            'post_title' => 'Portfolio Item ' . $i,
            'post_content' => 'Portfolio description',
            'post_status' => 'publish',
            'post_type' => 'portfolio'
        ));
        
        // Add meta
        update_post_meta( $post_id, '_client_name', 'Client ' . $i );
        update_post_meta( $post_id, '_project_year', 2020 + $i );
    }
}

// Create test users
function create_test_users( $count = 5 ) {
    for ( $i = 1; $i <= $count; $i++ ) {
        wp_insert_user( array(
            'user_login' => 'testuser' . $i,
            'user_pass' => 'password' . $i,
            'user_email' => 'test' . $i . '@example.com',
            'role' => 'subscriber'
        ));
    }
}

// Create test comments
function create_test_comments( $post_id, $count = 5 ) {
    for ( $i = 1; $i <= $count; $i++ ) {
        wp_insert_comment( array(
            'comment_post_ID' => $post_id,
            'comment_author' => 'Test User ' . $i,
            'comment_author_email' => 'test' . $i . '@example.com',
            'comment_content' => 'This is test comment ' . $i,
            'comment_approved' => 1
        ));
    }
}

// Clear all test data
function clear_test_data() {
    global $wpdb;
    
    // Delete test posts
    $test_posts = get_posts( array(
        'post_type' => 'any',
        's' => 'Test',
        'posts_per_page' => -1
    ));
    
    foreach ( $test_posts as $post ) {
        wp_delete_post( $post->ID, true );
    }
    
    // Delete test users
    $test_users = get_users( array( 'search' => 'testuser*' ) );
    foreach ( $test_users as $user ) {
        wp_delete_user( $user->ID );
    }
}
```
