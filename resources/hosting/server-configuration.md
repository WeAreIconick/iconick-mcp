# WordPress Server Configuration

## Overview

WordPress server configuration involves setting up and optimizing web servers, databases, and supporting infrastructure to deliver optimal performance, security, and reliability for WordPress applications.

## Web Server Configuration

### Apache Configuration

**Virtual Host Setup**
```apache
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/html/wordpress
    DirectoryIndex index.php index.html
    
    <Directory /var/www/html/wordpress>
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/wordpress_error.log
    CustomLog ${APACHE_LOG_DIR}/wordpress_access.log combined
</VirtualHost>
```

**WordPress-Specific Directives**
- mod_rewrite for permalinks
- .htaccess configuration
- Directory permissions
- File upload limits
- Memory limits

**Performance Optimization**
- Enable compression (mod_deflate)
- Browser caching headers
- KeepAlive settings
- Worker configuration
- SSL/TLS optimization

### Nginx Configuration

**Basic WordPress Configuration**
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html/wordpress;
    index index.php index.html;
    
    location / {
        try_files $uri $uri/ /index.php?$args;
    }
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.0-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
    
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Advanced Nginx Features**
- FastCGI caching
- Gzip compression
- Browser caching
- Security headers
- Rate limiting

### LiteSpeed Configuration

**WordPress Optimization**
- LiteSpeed Cache integration
- ESI (Edge Side Includes)
- Object caching
- Image optimization
- Database optimization

**Configuration Files**
- .htaccess compatibility
- Virtual host setup
- SSL configuration
- Performance tuning

## PHP Configuration

### PHP-FPM Setup

**Process Manager Configuration**
```ini
[www]
user = www-data
group = www-data
listen = /var/run/php/php8.0-fpm.sock
listen.owner = www-data
listen.group = www-data
pm = dynamic
pm.max_children = 50
pm.start_servers = 5
pm.min_spare_servers = 5
pm.max_spare_servers = 35
pm.max_requests = 1000
```

**Performance Tuning**
- Process pool sizing
- Memory limits
- Execution time limits
- Opcode caching
- Session handling

### PHP.ini Optimization

**WordPress-Specific Settings**
```ini
memory_limit = 256M
max_execution_time = 300
max_input_time = 300
post_max_size = 64M
upload_max_filesize = 64M
max_file_uploads = 20
```

**Security Settings**
- Disable dangerous functions
- Restrict file uploads
- Hide PHP version
- Secure session handling
- Error reporting control

**Performance Settings**
- Opcode caching (OPcache)
- Realpath cache
- Memory management
- Garbage collection
- Extension optimization

## Database Configuration

### MySQL/MariaDB Setup

**Basic Configuration**
```ini
[mysqld]
bind-address = 127.0.0.1
port = 3306
socket = /var/run/mysqld/mysqld.sock
datadir = /var/lib/mysql
tmpdir = /tmp
```

**Performance Optimization**
- InnoDB settings
- Buffer pool sizing
- Query cache configuration
- Connection limits
- Logging configuration

**Security Configuration**
- User privileges
- Network access
- SSL configuration
- Audit logging
- Backup procedures

### Database Optimization

**WordPress-Specific Tuning**
- Table optimization
- Index management
- Query optimization
- Connection pooling
- Replication setup

**Maintenance Tasks**
- Regular optimization
- Index rebuilding
- Log rotation
- Performance monitoring
- Capacity planning

## SSL/TLS Configuration

### SSL Certificate Setup

**Let's Encrypt Integration**
```bash
# Install Certbot
apt-get install certbot python3-certbot-apache

# Obtain certificate
certbot --apache -d example.com -d www.example.com

# Auto-renewal
crontab -e
0 12 * * * /usr/bin/certbot renew --quiet
```

**Certificate Management**
- Automated renewal
- Multiple domain support
- Wildcard certificates
- Certificate monitoring
- Backup procedures

### SSL Configuration

**Security Headers**
```apache
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
Header always set X-Content-Type-Options nosniff
Header always set X-Frame-Options DENY
Header always set X-XSS-Protection "1; mode=block"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```

**TLS Configuration**
- Protocol versions
- Cipher suites
- Perfect Forward Secrecy
- OCSP stapling
- HSTS implementation

## Caching Configuration

### Object Caching

**Redis Configuration**
```ini
# Redis configuration
port 6379
bind 127.0.0.1
timeout 0
tcp-keepalive 300
maxmemory 256mb
maxmemory-policy allkeys-lru
```

**WordPress Integration**
- Object cache plugins
- Transient API optimization
- Session storage
- Page caching integration
- Performance monitoring

### Page Caching

**Nginx FastCGI Cache**
```nginx
fastcgi_cache_path /var/cache/nginx levels=1:2 keys_zone=WORDPRESS:100m inactive=60m;
fastcgi_cache_key "$scheme$request_method$host$request_uri";

location ~ \.php$ {
    fastcgi_cache WORDPRESS;
    fastcgi_cache_valid 200 60m;
    fastcgi_cache_bypass $skip_cache;
    fastcgi_no_cache $skip_cache;
}
```

**Browser Caching**
- Cache-Control headers
- ETag implementation
- Last-Modified headers
- Compression settings
- Cache invalidation

## Security Configuration

### Server Hardening

**System Security**
- Firewall configuration
- SSH hardening
- User management
- Service configuration
- Log monitoring

**Application Security**
- File permissions
- Directory restrictions
- Input validation
- Output encoding
- Session security

### WordPress Security

**File Permissions**
```bash
# WordPress files
find /var/www/html -type f -exec chmod 644 {} \;
find /var/www/html -type d -exec chmod 755 {} \;

# wp-config.php
chmod 600 /var/www/html/wp-config.php

# wp-content/uploads
chmod 755 /var/www/html/wp-content/uploads
```

**Security Headers**
- Content Security Policy
- X-Frame-Options
- X-Content-Type-Options
- Referrer Policy
- Permissions Policy

## Monitoring Configuration

### System Monitoring

**Resource Monitoring**
- CPU usage
- Memory utilization
- Disk space
- Network traffic
- Process monitoring

**Application Monitoring**
- Web server logs
- PHP error logs
- Database logs
- WordPress logs
- Performance metrics

### Log Management

**Log Rotation**
```bash
# Logrotate configuration
/var/log/apache2/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 root adm
}
```

**Centralized Logging**
- Log aggregation
- Real-time monitoring
- Alert systems
- Log analysis
- Retention policies

## Performance Tuning

### Web Server Optimization

**Apache Optimization**
- MPM configuration
- KeepAlive settings
- Compression settings
- Module optimization
- Resource limits

**Nginx Optimization**
- Worker processes
- Connection handling
- Buffer sizes
- Timeout settings
- Load balancing

### Database Optimization

**Query Optimization**
- Slow query logging
- Index optimization
- Query analysis
- Performance profiling
- Optimization recommendations

**Resource Management**
- Connection pooling
- Memory allocation
- Disk I/O optimization
- CPU utilization
- Network optimization

## Backup Configuration

### Automated Backups

**Database Backups**
```bash
#!/bin/bash
# Database backup script
mysqldump -u root -p wordpress > /backups/wordpress_$(date +%Y%m%d_%H%M%S).sql
find /backups -name "wordpress_*.sql" -mtime +7 -delete
```

**File Backups**
```bash
#!/bin/bash
# File backup script
tar -czf /backups/wordpress_files_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/html/wordpress
find /backups -name "wordpress_files_*.tar.gz" -mtime +7 -delete
```

### Backup Strategies

**Backup Types**
- Full backups
- Incremental backups
- Differential backups
- Database-only backups
- File-only backups

**Storage Options**
- Local storage
- Cloud storage
- Remote servers
- Multiple locations
- Version control

## Load Balancing

### Load Balancer Configuration

**Nginx Load Balancing**
```nginx
upstream wordpress_backend {
    server 127.0.0.1:8080 weight=3;
    server 127.0.0.1:8081 weight=2;
    server 127.0.0.1:8082 weight=1;
    
    keepalive 32;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://wordpress_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

**Load Balancing Strategies**
- Round-robin
- Weighted round-robin
- Least connections
- IP hash
- Health checks

### Session Management

**Session Affinity**
- Sticky sessions
- Session clustering
- Database sessions
- Redis sessions
- Cookie-based sessions

## Container Configuration

### Docker Setup

**WordPress Container**
```dockerfile
FROM wordpress:latest

# Install additional PHP extensions
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Copy custom configuration
COPY wp-config.php /var/www/html/
COPY .htaccess /var/www/html/

# Set proper permissions
RUN chown -R www-data:www-data /var/www/html
```

**Docker Compose**
```yaml
version: '3.8'
services:
  wordpress:
    build: .
    ports:
      - "8080:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
    depends_on:
      - db
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

## Cloud Configuration

### AWS Configuration

**EC2 Setup**
- Instance sizing
- Security groups
- Elastic IP
- Load balancer
- Auto scaling

**RDS Configuration**
- Database instance
- Multi-AZ deployment
- Read replicas
- Backup configuration
- Security groups

### Google Cloud Configuration

**Compute Engine**
- VM instances
- Firewall rules
- Load balancing
- Auto scaling
- Networking

**Cloud SQL**
- Database instances
- High availability
- Read replicas
- Backup configuration
- Network configuration

## Troubleshooting

### Common Issues

**Performance Problems**
- Slow page loads
- High resource usage
- Database bottlenecks
- Memory issues
- Network latency

**Security Issues**
- Unauthorized access
- Malware infections
- Brute force attacks
- Vulnerabilities
- Data breaches

**Configuration Issues**
- SSL certificate problems
- Permalink issues
- File permission errors
- Database connection errors
- Plugin conflicts

### Diagnostic Tools

**System Monitoring**
- htop/top
- iotop
- netstat
- ss
- lsof

**Application Monitoring**
- Web server logs
- PHP error logs
- Database logs
- WordPress debug logs
- Performance profilers

## Best Practices

### Configuration Management

**Version Control**
- Configuration files in Git
- Environment-specific configs
- Change tracking
- Rollback procedures
- Documentation

**Automation**
- Configuration management tools
- Infrastructure as Code
- Automated deployment
- Monitoring and alerting
- Backup automation

### Maintenance

**Regular Tasks**
- Security updates
- Performance monitoring
- Log rotation
- Backup verification
- Capacity planning

**Monitoring**
- Uptime monitoring
- Performance metrics
- Security scanning
- Error tracking
- User experience monitoring