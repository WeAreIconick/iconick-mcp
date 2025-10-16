---
difficulty: Advanced
tags: [database, batch, bulk, performance]
related: [database/wpdb-queries]
use_case: Bulk database operations
---

# Batch Database Operations

```php
// Batch update posts
function batch_update_posts( $post_ids, $meta_key, $meta_value ) {
    global $wpdb;
    
    // Validate IDs
    $post_ids = array_map( 'absint', $post_ids );
    $post_ids = array_filter( $post_ids );
    
    if ( empty( $post_ids ) ) {
        return false;
    }
    
    // Prepare placeholders
    $placeholders = implode( ',', array_fill( 0, count( $post_ids ), '%d' ) );
    
    // Build query
    $query = $wpdb->prepare(
        "UPDATE {$wpdb->postmeta} 
        SET meta_value = %s 
        WHERE meta_key = %s 
        AND post_id IN ($placeholders)",
        $meta_value,
        $meta_key,
        ...$post_ids
    );
    
    return $wpdb->query( $query );
}

// Batch insert
function batch_insert_meta( $data_array ) {
    global $wpdb;
    
    $values = array();
    $placeholders = array();
    
    foreach ( $data_array as $data ) {
        $placeholders[] = '(%d, %s, %s)';
        $values[] = $data['post_id'];
        $values[] = $data['meta_key'];
        $values[] = $data['meta_value'];
    }
    
    $query = "INSERT INTO {$wpdb->postmeta} (post_id, meta_key, meta_value) VALUES ";
    $query .= implode( ', ', $placeholders );
    
    return $wpdb->query( $wpdb->prepare( $query, $values ) );
}

// Batch delete with transaction
function batch_delete_with_transaction( $post_ids ) {
    global $wpdb;
    
    $wpdb->query( 'START TRANSACTION' );
    
    try {
        foreach ( $post_ids as $post_id ) {
            wp_delete_post( $post_id, true );
        }
        
        $wpdb->query( 'COMMIT' );
        return true;
    } catch ( Exception $e ) {
        $wpdb->query( 'ROLLBACK' );
        return false;
    }
}
```
