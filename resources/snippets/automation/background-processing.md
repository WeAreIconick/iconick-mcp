# Background Processing

```php
// Queue background task
function queue_background_task( $data ) {
    // Save task data
    $task_id = wp_insert_post( array(
        'post_type' => 'background_task',
        'post_title' => 'Task ' . time(),
        'post_status' => 'pending',
        'post_content' => json_encode( $data )
    ));
    
    // Schedule immediate processing
    wp_schedule_single_event( time(), 'process_background_task', array( $task_id ) );
    
    return $task_id;
}

// Process task
add_action( 'process_background_task', 'handle_background_task' );
function handle_background_task( $task_id ) {
    $task = get_post( $task_id );
    
    if ( ! $task || $task->post_status !== 'pending' ) {
        return;
    }
    
    $data = json_decode( $task->post_content, true );
    
    try {
        // Process task
        $result = do_heavy_processing( $data );
        
        // Mark as complete
        wp_update_post( array(
            'ID' => $task_id,
            'post_status' => 'publish',
            'post_excerpt' => json_encode( $result )
        ));
        
    } catch ( Exception $e ) {
        // Mark as failed
        wp_update_post( array(
            'ID' => $task_id,
            'post_status' => 'failed',
            'post_excerpt' => $e->getMessage()
        ));
    }
}

// Check task status
function get_task_status( $task_id ) {
    $task = get_post( $task_id );
    
    if ( ! $task ) {
        return 'not_found';
    }
    
    return $task->post_status;
}
```
