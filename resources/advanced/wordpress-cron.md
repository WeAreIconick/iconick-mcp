# WordPress Cron System

## Understanding WordPress Cron

WordPress has its own cron system called `wp-cron` that handles scheduled tasks. Unlike system cron, it's triggered by website visits.

## Basic Cron Jobs

### Scheduling a Single Event
```php
// Schedule a one-time event
function schedule_cleanup_task() {
    if (!wp_next_scheduled('my_cleanup_task')) {
        wp_schedule_single_event(time() + 3600, 'my_cleanup_task'); // Run in 1 hour
    }
}
add_action('init', 'schedule_cleanup_task');

// Handle the scheduled task
add_action('my_cleanup_task', 'perform_cleanup');
function perform_cleanup() {
    // Your cleanup logic here
    error_log('Cleanup task executed at ' . current_time('mysql'));
}
```

### Recurring Events
```php
// Schedule a recurring event
function schedule_daily_task() {
    if (!wp_next_scheduled('daily_maintenance')) {
        wp_schedule_event(time(), 'daily', 'daily_maintenance');
    }
}
add_action('init', 'schedule_daily_task');

// Handle the daily task
add_action('daily_maintenance', 'perform_daily_maintenance');
function perform_daily_maintenance() {
    // Daily maintenance tasks
    cleanup_expired_transients();
    update_statistics();
    send_daily_reports();
}

// Clean up on deactivation
register_deactivation_hook(__FILE__, 'clear_scheduled_events');
function clear_scheduled_events() {
    wp_clear_scheduled_hook('daily_maintenance');
}
```

## Custom Cron Intervals

```php
// Add custom cron intervals
function add_custom_cron_intervals($schedules) {
    $schedules['every_15_minutes'] = array(
        'interval' => 900, // 15 minutes
        'display' => __('Every 15 Minutes')
    );
    
    $schedules['every_hour'] = array(
        'interval' => 3600, // 1 hour
        'display' => __('Every Hour')
    );
    
    $schedules['weekly'] = array(
        'interval' => 604800, // 1 week
        'display' => __('Weekly')
    );
    
    return $schedules;
}
add_filter('cron_schedules', 'add_custom_cron_intervals');

// Use custom interval
function schedule_custom_interval_task() {
    if (!wp_next_scheduled('hourly_task')) {
        wp_schedule_event(time(), 'every_hour', 'hourly_task');
    }
}
add_action('init', 'schedule_custom_interval_task');
```

## Advanced Cron Management

### Cron Job Manager Class
```php
class CronJobManager {
    private $jobs = array();
    
    public function __construct() {
        add_action('init', array($this, 'schedule_jobs'));
        add_action('wp_ajax_manual_cron_run', array($this, 'manual_cron_run'));
    }
    
    public function add_job($hook, $interval, $args = array()) {
        $this->jobs[] = array(
            'hook' => $hook,
            'interval' => $interval,
            'args' => $args
        );
    }
    
    public function schedule_jobs() {
        foreach ($this->jobs as $job) {
            if (!wp_next_scheduled($job['hook'], $job['args'])) {
                wp_schedule_event(time(), $job['interval'], $job['hook'], $job['args']);
            }
        }
    }
    
    public function manual_cron_run() {
        check_ajax_referer('manual_cron_nonce', 'nonce');
        
        if (!current_user_can('manage_options')) {
            wp_die('Unauthorized');
        }
        
        $hook = sanitize_text_field($_POST['hook']);
        
        if (has_action($hook)) {
            do_action($hook);
            wp_send_json_success('Cron job executed successfully');
        } else {
            wp_send_json_error('Cron job not found');
        }
    }
}

// Initialize and add jobs
$cron_manager = new CronJobManager();
$cron_manager->add_job('backup_database', 'daily');
$cron_manager->add_job('cleanup_logs', 'weekly');
$cron_manager->add_job('update_statistics', 'every_hour');
```

### Database Backup Cron Job
```php
add_action('backup_database', 'perform_database_backup');
function perform_database_backup() {
    global $wpdb;
    
    $backup_dir = WP_CONTENT_DIR . '/backups/';
    if (!file_exists($backup_dir)) {
        wp_mkdir_p($backup_dir);
    }
    
    $backup_file = $backup_dir . 'backup_' . date('Y-m-d_H-i-s') . '.sql';
    
    // Get database credentials
    $host = DB_HOST;
    $username = DB_USER;
    $password = DB_PASSWORD;
    $database = DB_NAME;
    
    // Create mysqldump command
    $command = "mysqldump -h{$host} -u{$username} -p{$password} {$database} > {$backup_file}";
    
    // Execute backup
    exec($command, $output, $return_var);
    
    if ($return_var === 0) {
        error_log('Database backup created: ' . $backup_file);
        
        // Clean up old backups (keep last 7 days)
        cleanup_old_backups($backup_dir, 7);
    } else {
        error_log('Database backup failed');
    }
}

function cleanup_old_backups($backup_dir, $days_to_keep) {
    $files = glob($backup_dir . 'backup_*.sql');
    $cutoff_time = time() - ($days_to_keep * 24 * 60 * 60);
    
    foreach ($files as $file) {
        if (filemtime($file) < $cutoff_time) {
            unlink($file);
        }
    }
}
```

## Cron with Background Processing

### Background Task Processor
```php
class BackgroundTaskProcessor {
    private $queue_table;
    
    public function __construct() {
        global $wpdb;
        $this->queue_table = $wpdb->prefix . 'background_tasks';
        
        add_action('init', array($this, 'create_queue_table'));
        add_action('process_background_tasks', array($this, 'process_queue'));
        
        // Schedule processing every 5 minutes
        if (!wp_next_scheduled('process_background_tasks')) {
            wp_schedule_event(time(), 'every_5_minutes', 'process_background_tasks');
        }
    }
    
    public function create_queue_table() {
        global $wpdb;
        
        $charset_collate = $wpdb->get_charset_collate();
        
        $sql = "CREATE TABLE IF NOT EXISTS {$this->queue_table} (
            id bigint(20) NOT NULL AUTO_INCREMENT,
            task_type varchar(100) NOT NULL,
            task_data longtext,
            status varchar(20) DEFAULT 'pending',
            attempts int(11) DEFAULT 0,
            created_at datetime DEFAULT CURRENT_TIMESTAMP,
            processed_at datetime NULL,
            PRIMARY KEY (id),
            KEY status (status),
            KEY task_type (task_type)
        ) $charset_collate;";
        
        require_once(ABSPATH . 'wp-admin/includes/upgrade.php');
        dbDelta($sql);
    }
    
    public function add_task($task_type, $task_data) {
        global $wpdb;
        
        $wpdb->insert(
            $this->queue_table,
            array(
                'task_type' => $task_type,
                'task_data' => json_encode($task_data),
                'status' => 'pending'
            ),
            array('%s', '%s', '%s')
        );
        
        return $wpdb->insert_id;
    }
    
    public function process_queue() {
        global $wpdb;
        
        // Get pending tasks (limit to 10 per run)
        $tasks = $wpdb->get_results(
            "SELECT * FROM {$this->queue_table} 
             WHERE status = 'pending' AND attempts < 3 
             ORDER BY created_at ASC 
             LIMIT 10"
        );
        
        foreach ($tasks as $task) {
            $this->process_task($task);
        }
    }
    
    private function process_task($task) {
        global $wpdb;
        
        // Update attempt count
        $wpdb->update(
            $this->queue_table,
            array('attempts' => $task->attempts + 1),
            array('id' => $task->id),
            array('%d'),
            array('%d')
        );
        
        try {
            $task_data = json_decode($task->task_data, true);
            
            // Process based on task type
            switch ($task->task_type) {
                case 'send_email':
                    $this->send_email($task_data);
                    break;
                case 'process_image':
                    $this->process_image($task_data);
                    break;
                case 'generate_report':
                    $this->generate_report($task_data);
                    break;
                default:
                    throw new Exception('Unknown task type: ' . $task->task_type);
            }
            
            // Mark as completed
            $wpdb->update(
                $this->queue_table,
                array(
                    'status' => 'completed',
                    'processed_at' => current_time('mysql')
                ),
                array('id' => $task->id),
                array('%s', '%s'),
                array('%d')
            );
            
        } catch (Exception $e) {
            // Mark as failed if max attempts reached
            if ($task->attempts >= 2) {
                $wpdb->update(
                    $this->queue_table,
                    array(
                        'status' => 'failed',
                        'processed_at' => current_time('mysql')
                    ),
                    array('id' => $task->id),
                    array('%s', '%s'),
                    array('%d')
                );
            }
            
            error_log('Background task failed: ' . $e->getMessage());
        }
    }
    
    private function send_email($data) {
        wp_mail($data['to'], $data['subject'], $data['message']);
    }
    
    private function process_image($data) {
        // Image processing logic
    }
    
    private function generate_report($data) {
        // Report generation logic
    }
}

new BackgroundTaskProcessor();
```

## Cron Monitoring and Debugging

### Cron Status Dashboard
```php
class CronStatusDashboard {
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
    }
    
    public function add_admin_menu() {
        add_management_page(
            'Cron Status',
            'Cron Status',
            'manage_options',
            'cron-status',
            array($this, 'display_cron_status')
        );
    }
    
    public function display_cron_status() {
        $cron_jobs = _get_cron_array();
        ?>
        <div class="wrap">
            <h1>Cron Status</h1>
            
            <h2>Scheduled Events</h2>
            <table class="widefat">
                <thead>
                    <tr>
                        <th>Hook</th>
                        <th>Next Run</th>
                        <th>Recurrence</th>
                        <th>Args</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($cron_jobs as $timestamp => $hooks) : ?>
                        <?php foreach ($hooks as $hook => $events) : ?>
                            <?php foreach ($events as $key => $event) : ?>
                                <tr>
                                    <td><?php echo esc_html($hook); ?></td>
                                    <td><?php echo date('Y-m-d H:i:s', $timestamp); ?></td>
                                    <td><?php echo esc_html($event['schedule'] ?? 'Single'); ?></td>
                                    <td><?php echo esc_html(json_encode($event['args'])); ?></td>
                                </tr>
                            <?php endforeach; ?>
                        <?php endforeach; ?>
                    <?php endforeach; ?>
                </tbody>
            </table>
            
            <h2>Cron Health Check</h2>
            <?php $this->display_health_check(); ?>
        </div>
        <?php
    }
    
    private function display_health_check() {
        $last_cron = get_option('_transient_doing_cron');
        $cron_disabled = defined('DISABLE_WP_CRON') && DISABLE_WP_CRON;
        
        echo '<div class="notice notice-info">';
        echo '<p><strong>WP Cron Status:</strong> ' . ($cron_disabled ? 'Disabled' : 'Enabled') . '</p>';
        echo '<p><strong>Last Cron Run:</strong> ' . ($last_cron ? date('Y-m-d H:i:s', $last_cron) : 'Never') . '</p>';
        echo '<p><strong>Server Time:</strong> ' . date('Y-m-d H:i:s') . '</p>';
        echo '</div>';
    }
}

new CronStatusDashboard();
```

## Best Practices

1. **Always clean up** scheduled events on plugin deactivation
2. **Use proper intervals** for different types of tasks
3. **Implement error handling** and retry logic
4. **Monitor cron health** regularly
5. **Use background processing** for heavy tasks
6. **Consider system cron** for critical tasks
7. **Log cron activities** for debugging
8. **Test cron jobs** in development
9. **Handle timezone** considerations
10. **Optimize database queries** in cron jobs

## Resources

- [WordPress Cron Documentation](https://developer.wordpress.org/plugins/cron/)
- [wp_schedule_event Documentation](https://developer.wordpress.org/reference/functions/wp_schedule_event/)
- [WordPress Background Processing](https://github.com/A5hleyRich/wp-background-processing)