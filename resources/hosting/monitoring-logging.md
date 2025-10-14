# WordPress Monitoring and Logging

## Overview

Monitoring and logging are essential components of WordPress hosting, providing visibility into system performance, security events, user behavior, and application health for proactive management and troubleshooting.

## Monitoring Fundamentals

### Monitoring Types

**Infrastructure Monitoring**
- Server resources (CPU, memory, disk)
- Network performance
- Database performance
- Web server metrics
- System health

**Application Monitoring**
- WordPress performance
- Plugin and theme monitoring
- Database queries
- API responses
- User experience metrics

**Security Monitoring**
- Login attempts
- File changes
- Malware detection
- Vulnerability scanning
- Access control violations

**Business Monitoring**
- Website uptime
- Traffic analytics
- Conversion rates
- Revenue metrics
- User engagement

### Key Performance Indicators (KPIs)

**Performance Metrics**
- Page load times
- Time to First Byte (TTFB)
- Largest Contentful Paint (LCP)
- First Input Delay (FID)
- Cumulative Layout Shift (CLS)

**Availability Metrics**
- Uptime percentage
- Response time
- Error rates
- Throughput
- Concurrent users

**Security Metrics**
- Failed login attempts
- Security incidents
- Vulnerability count
- Patch compliance
- Access violations

## Infrastructure Monitoring

### Server Monitoring

**System Resources**
```bash
# CPU monitoring
top -p $(pgrep nginx)
htop
iostat -c 1 5

# Memory monitoring
free -h
vmstat 1 5
cat /proc/meminfo

# Disk monitoring
df -h
iostat -d 1 5
iotop
```

**Network Monitoring**
```bash
# Network statistics
netstat -i
ss -tuln
iftop
nethogs

# Connection monitoring
netstat -an | grep :80 | wc -l
ss -s
```

### Web Server Monitoring

**Apache Monitoring**
```apache
# Enable mod_status
LoadModule status_module modules/mod_status.so

<Location "/server-status">
    SetHandler server-status
    Require local
</Location>

ExtendedStatus On
```

**Nginx Monitoring**
```nginx
# Status module configuration
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    deny all;
}
```

**PHP-FPM Monitoring**
```ini
; PHP-FPM status page
pm.status_path = /fpm-status
ping.path = /fpm-ping

; Status page configuration
[www]
pm.status_path = /status
ping.path = /ping
```

### Database Monitoring

**MySQL/MariaDB Monitoring**
```sql
-- Show process list
SHOW PROCESSLIST;

-- Show status variables
SHOW STATUS LIKE 'Connections';
SHOW STATUS LIKE 'Uptime';
SHOW STATUS LIKE 'Questions';

-- Slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow.log';
```

**Database Performance Metrics**
- Query execution time
- Connection count
- Buffer pool usage
- Lock waits
- Replication lag

## Application Monitoring

### WordPress Performance Monitoring

**Core Web Vitals**
- Largest Contentful Paint (LCP)
- First Input Delay (FID)
- Cumulative Layout Shift (CLS)
- First Contentful Paint (FCP)
- Time to Interactive (TTI)

**WordPress-Specific Metrics**
- Plugin performance impact
- Theme performance
- Database query performance
- Memory usage
- Execution time

### Plugin and Theme Monitoring

**Performance Impact Assessment**
```php
// Plugin performance monitoring
function monitor_plugin_performance() {
    $start_time = microtime(true);
    $start_memory = memory_get_usage();
    
    // Plugin execution
    
    $end_time = microtime(true);
    $end_memory = memory_get_usage();
    
    $execution_time = $end_time - $start_time;
    $memory_usage = $end_memory - $start_memory;
    
    error_log("Plugin performance: {$execution_time}s, {$memory_usage} bytes");
}
```

**Query Monitoring**
```php
// Database query monitoring
function log_slow_queries($query, $query_time) {
    if ($query_time > 0.5) { // Log queries over 500ms
        error_log("Slow query ({$query_time}s): {$query}");
    }
}
```

## Logging Systems

### Log Types

**Access Logs**
- Web server access logs
- User activity logs
- API access logs
- CDN logs
- Load balancer logs

**Error Logs**
- Application errors
- PHP errors
- Database errors
- Web server errors
- System errors

**Security Logs**
- Authentication logs
- Authorization failures
- File access logs
- Network access logs
- Malware detection logs

**Performance Logs**
- Response time logs
- Resource usage logs
- Database query logs
- Cache hit/miss logs
- User experience logs

### Log Configuration

**Apache Logging**
```apache
# Custom log format
LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\" %D" combined_with_time

# Virtual host logging
CustomLog ${APACHE_LOG_DIR}/wordpress_access.log combined_with_time
ErrorLog ${APACHE_LOG_DIR}/wordpress_error.log
```

**Nginx Logging**
```nginx
# Custom log format
log_format wordpress '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    '$request_time $upstream_response_time';

# Access and error logs
access_log /var/log/nginx/wordpress_access.log wordpress;
error_log /var/log/nginx/wordpress_error.log warn;
```

**PHP Error Logging**
```ini
; PHP error logging
log_errors = On
error_log = /var/log/php/error.log
error_reporting = E_ALL
display_errors = Off
```

### WordPress Logging

**WordPress Debug Logging**
```php
// wp-config.php debug settings
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
define('SCRIPT_DEBUG', true);

// Custom logging function
function custom_log($message, $level = 'info') {
    $timestamp = date('Y-m-d H:i:s');
    $log_entry = "[{$timestamp}] [{$level}] {$message}" . PHP_EOL;
    error_log($log_entry, 3, WP_CONTENT_DIR . '/debug.log');
}
```

**Plugin Logging**
```php
// Plugin-specific logging
class PluginLogger {
    private $log_file;
    
    public function __construct($log_file) {
        $this->log_file = $log_file;
    }
    
    public function log($message, $level = 'INFO') {
        $timestamp = date('Y-m-d H:i:s');
        $log_entry = "[{$timestamp}] [{$level}] {$message}" . PHP_EOL;
        file_put_contents($this->log_file, $log_entry, FILE_APPEND | LOCK_EX);
    }
}
```

## Monitoring Tools

### System Monitoring Tools

**Nagios**
- Infrastructure monitoring
- Service monitoring
- Alert management
- Performance tracking
- Custom plugins

**Zabbix**
- Real-time monitoring
- Historical data
- Custom metrics
- Alerting system
- Web interface

**Prometheus**
- Time-series database
- Metrics collection
- Alerting rules
- Service discovery
- Grafana integration

### Application Performance Monitoring

**New Relic**
- Application performance
- Database monitoring
- Error tracking
- User experience
- Custom dashboards

**Datadog**
- Infrastructure monitoring
- Application performance
- Log management
- Security monitoring
- Custom metrics

**AppDynamics**
- Application monitoring
- Business transaction tracking
- Performance analytics
- Root cause analysis
- Custom dashboards

### WordPress-Specific Tools

**Query Monitor**
- Database query monitoring
- Plugin performance
- Theme performance
- Memory usage
- HTTP requests

**P3 (Plugin Performance Profiler)**
- Plugin performance analysis
- Execution time tracking
- Memory usage monitoring
- Performance recommendations
- Comparison reports

**Debug Bar**
- WordPress debugging
- Query monitoring
- Performance metrics
- Memory usage
- Template information

## Log Management

### Log Aggregation

**ELK Stack (Elasticsearch, Logstash, Kibana)**
- Centralized logging
- Log parsing and analysis
- Real-time dashboards
- Search capabilities
- Alert management

**Fluentd**
- Log collection
- Data processing
- Output routing
- Plugin ecosystem
- High performance

**Splunk**
- Log analysis
- Real-time monitoring
- Machine learning
- Security analytics
- Custom dashboards

### Log Rotation

**Logrotate Configuration**
```bash
# /etc/logrotate.d/wordpress
/var/log/apache2/wordpress_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        /bin/kill -HUP `cat /var/run/apache2.pid 2> /dev/null` 2> /dev/null || true
    endscript
}

/var/log/nginx/wordpress_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        /bin/kill -USR1 `cat /var/run/nginx.pid 2> /dev/null` 2> /dev/null || true
    endscript
}
```

**Manual Log Rotation**
```bash
#!/bin/bash
# Manual log rotation script
DATE=$(date +%Y%m%d)

# Rotate Apache logs
mv /var/log/apache2/wordpress_access.log /var/log/apache2/wordpress_access_$DATE.log
mv /var/log/apache2/wordpress_error.log /var/log/apache2/wordpress_error_$DATE.log

# Restart Apache
systemctl reload apache2

# Compress old logs
gzip /var/log/apache2/wordpress_*_$DATE.log
```

## Alerting Systems

### Alert Configuration

**Threshold-Based Alerts**
- CPU usage > 80%
- Memory usage > 90%
- Disk space < 10%
- Response time > 2 seconds
- Error rate > 5%

**Anomaly Detection**
- Unusual traffic patterns
- Performance degradation
- Security events
- Resource usage spikes
- User behavior changes

### Notification Methods

**Email Alerts**
- SMTP configuration
- HTML email templates
- Alert severity levels
- Escalation procedures
- Digest notifications

**SMS Alerts**
- SMS gateway integration
- Critical alerts only
- Rate limiting
- Delivery confirmation
- Cost management

**Slack/Teams Integration**
- Webhook configuration
- Channel routing
- Alert formatting
- User mentions
- Escalation policies

## Security Monitoring

### Security Event Monitoring

**Authentication Monitoring**
```php
// Login attempt monitoring
function monitor_login_attempts($username, $success) {
    $ip = $_SERVER['REMOTE_ADDR'];
    $user_agent = $_SERVER['HTTP_USER_AGENT'];
    $timestamp = current_time('mysql');
    
    $log_data = array(
        'username' => $username,
        'ip_address' => $ip,
        'user_agent' => $user_agent,
        'success' => $success,
        'timestamp' => $timestamp
    );
    
    // Log to database or file
    log_security_event('login_attempt', $log_data);
    
    // Check for suspicious activity
    check_brute_force_attempts($ip, $username);
}
```

**File Change Monitoring**
```bash
#!/bin/bash
# File integrity monitoring
find /var/www/html/wordpress -type f -name "*.php" -exec md5sum {} \; > /var/log/file_integrity_baseline.txt

# Compare with current state
find /var/www/html/wordpress -type f -name "*.php" -exec md5sum {} \; > /var/log/file_integrity_current.txt
diff /var/log/file_integrity_baseline.txt /var/log/file_integrity_current.txt
```

### Vulnerability Monitoring

**Plugin Vulnerability Scanning**
```php
// Check for plugin vulnerabilities
function check_plugin_vulnerabilities() {
    $plugins = get_plugins();
    $vulnerable_plugins = array();
    
    foreach ($plugins as $plugin_file => $plugin_data) {
        $plugin_slug = dirname($plugin_file);
        $plugin_version = $plugin_data['Version'];
        
        // Check vulnerability database
        $vulnerabilities = check_vulnerability_database($plugin_slug, $plugin_version);
        
        if (!empty($vulnerabilities)) {
            $vulnerable_plugins[] = array(
                'plugin' => $plugin_data['Name'],
                'version' => $plugin_version,
                'vulnerabilities' => $vulnerabilities
            );
        }
    }
    
    return $vulnerable_plugins;
}
```

## Performance Monitoring

### Real-Time Performance Monitoring

**Response Time Monitoring**
```php
// Response time measurement
function measure_response_time() {
    $start_time = microtime(true);
    
    // WordPress execution
    
    $end_time = microtime(true);
    $response_time = ($end_time - $start_time) * 1000; // Convert to milliseconds
    
    // Log response time
    if ($response_time > 1000) { // Log slow responses
        error_log("Slow response: {$response_time}ms");
    }
    
    return $response_time;
}
```

**Database Performance Monitoring**
```php
// Database query monitoring
function monitor_database_queries($query, $query_time) {
    global $wpdb;
    
    // Log slow queries
    if ($query_time > 0.5) {
        $log_data = array(
            'query' => $query,
            'execution_time' => $query_time,
            'timestamp' => current_time('mysql'),
            'url' => $_SERVER['REQUEST_URI']
        );
        
        log_slow_query($log_data);
    }
    
    // Track query count
    $wpdb->query_count++;
}
```

### User Experience Monitoring

**Core Web Vitals Tracking**
```javascript
// Core Web Vitals measurement
function measureCoreWebVitals() {
    // Largest Contentful Paint
    new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            console.log('LCP:', entry.startTime);
            // Send to analytics
        }
    }).observe({entryTypes: ['largest-contentful-paint']});
    
    // First Input Delay
    new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            console.log('FID:', entry.processingStart - entry.startTime);
            // Send to analytics
        }
    }).observe({entryTypes: ['first-input']});
    
    // Cumulative Layout Shift
    new PerformanceObserver((entryList) => {
        for (const entry of entryList.getEntries()) {
            if (!entry.hadRecentInput) {
                console.log('CLS:', entry.value);
                // Send to analytics
            }
        }
    }).observe({entryTypes: ['layout-shift']});
}
```

## Dashboard and Reporting

### Monitoring Dashboards

**Grafana Dashboards**
- Real-time metrics
- Historical data
- Custom visualizations
- Alert integration
- Multi-data source support

**Custom WordPress Dashboard**
```php
// WordPress admin dashboard widget
function monitoring_dashboard_widget() {
    $uptime = get_site_uptime();
    $response_time = get_average_response_time();
    $error_rate = get_error_rate();
    
    echo "<div class='monitoring-widget'>";
    echo "<h3>Site Performance</h3>";
    echo "<p>Uptime: {$uptime}%</p>";
    echo "<p>Avg Response Time: {$response_time}ms</p>";
    echo "<p>Error Rate: {$error_rate}%</p>";
    echo "</div>";
}
```

### Automated Reports

**Daily Performance Report**
```php
// Daily performance report
function generate_daily_report() {
    $report_data = array(
        'date' => date('Y-m-d'),
        'uptime' => calculate_daily_uptime(),
        'page_views' => get_daily_page_views(),
        'unique_visitors' => get_daily_unique_visitors(),
        'avg_response_time' => get_daily_avg_response_time(),
        'error_count' => get_daily_error_count(),
        'top_pages' => get_daily_top_pages()
    );
    
    // Send report via email
    send_performance_report($report_data);
}
```

## Best Practices

### Monitoring Strategy

**Comprehensive Coverage**
- Multi-layer monitoring
- End-to-end visibility
- Proactive alerting
- Historical analysis
- Trend identification

**Performance Optimization**
- Baseline establishment
- Continuous monitoring
- Performance regression detection
- Optimization validation
- Capacity planning

### Log Management

**Log Retention Policies**
- Legal requirements
- Storage costs
- Analysis needs
- Compliance standards
- Performance impact

**Log Security**
- Access control
- Encryption
- Integrity verification
- Secure transmission
- Audit trails

### Alert Management

**Alert Tuning**
- Threshold optimization
- Noise reduction
- Escalation procedures
- Response protocols
- Documentation

**Incident Response**
- Alert triage
- Response procedures
- Communication protocols
- Post-incident analysis
- Continuous improvement