---
difficulty: Intermediate
tags: [automation, cron, scheduled, tasks]
related: [automation/background-processing]
use_case: Scheduled background tasks
---

# WordPress Cron Jobs

```php
// Register cron event
register_activation_hook( __FILE__, 'schedule_my_cron' );
function schedule_my_cron() {
    if ( ! wp_next_scheduled( 'my_daily_task' ) ) {
        wp_schedule_event( time(), 'daily', 'my_daily_task' );
    }
}

// Unschedule on deactivation
register_deactivation_hook( __FILE__, 'unschedule_my_cron' );
function unschedule_my_cron() {
    wp_clear_scheduled_hook( 'my_daily_task' );
}

// Hook the task
add_action( 'my_daily_task', 'do_daily_task' );
function do_daily_task() {
    // Run daily task
    $posts = get_posts( array( 'post_status' => 'draft', 'date_query' => array( array( 'after' => '30 days ago' ) ) ) );
    
    foreach ( $posts as $post ) {
        // Auto-delete old drafts
        wp_delete_post( $post->ID, true );
    }
}

// Custom schedule
add_filter( 'cron_schedules', 'add_custom_cron_schedule' );
function add_custom_cron_schedule( $schedules ) {
    $schedules['weekly'] = array(
        'interval' => 604800,  // 7 days in seconds
        'display' => __( 'Once Weekly', 'textdomain' )
    );
    
    $schedules['every_5_minutes'] = array(
        'interval' => 300,
        'display' => __( 'Every 5 Minutes', 'textdomain' )
    );
    
    return $schedules;
}

// Check if cron is working
function check_cron_status() {
    $crons = _get_cron_array();
    
    if ( empty( $crons ) ) {
        return 'No cron jobs scheduled';
    }
    
    $next_run = array_keys( $crons )[0];
    $time_until = $next_run - time();
    
    return sprintf( 'Next cron in %d seconds', $time_until );
}
```
