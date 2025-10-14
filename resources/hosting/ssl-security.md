# WordPress SSL and Security Configuration

## Overview

SSL (Secure Sockets Layer) and security configuration are critical components of WordPress hosting, ensuring data encryption, authentication, and protection against various security threats.

## SSL/TLS Fundamentals

### SSL vs TLS

**SSL (Secure Sockets Layer)**
- Legacy protocol (SSL 1.0, 2.0, 3.0)
- Deprecated due to security vulnerabilities
- Still commonly referred to as "SSL"

**TLS (Transport Layer Security)**
- Modern successor to SSL
- Current versions: TLS 1.2, TLS 1.3
- Industry standard for secure communications

### Certificate Types

**Domain Validated (DV) Certificates**
- Basic validation
- Quick issuance
- Low cost
- Suitable for most websites

**Organization Validated (OV) Certificates**
- Extended validation
- Company information included
- Higher trust level
- Moderate cost

**Extended Validation (EV) Certificates**
- Highest validation level
- Green address bar (legacy browsers)
- Maximum trust
- Highest cost

**Wildcard Certificates**
- Covers subdomains
- Single certificate for *.example.com
- Cost-effective for multiple subdomains

**Multi-Domain (SAN) Certificates**
- Multiple domains in one certificate
- Subject Alternative Names
- Flexible domain coverage

## SSL Certificate Providers

### Free Certificate Authorities

**Let's Encrypt**
- Free SSL certificates
- 90-day validity period
- Automated renewal
- Wide browser support
- Community-driven

**Cloudflare**
- Free SSL for Cloudflare customers
- Universal SSL
- Flexible SSL options
- CDN integration
- DDoS protection

### Commercial Certificate Authorities

**DigiCert**
- Industry leader
- High trust level
- Extended validation options
- Wildcard certificates
- Premium support

**Comodo/Sectigo**
- Cost-effective options
- Wide range of certificates
- Good browser compatibility
- Rapid issuance
- 24/7 support

**GlobalSign**
- Enterprise focus
- High security standards
- Compliance certificates
- Global presence
- Advanced features

## SSL Implementation

### Apache SSL Configuration

**Virtual Host with SSL**
```apache
<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/html/wordpress
    
    SSLEngine on
    SSLCertificateFile /path/to/certificate.crt
    SSLCertificateKeyFile /path/to/private.key
    SSLCertificateChainFile /path/to/chain.crt
    
    # Security headers
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set X-XSS-Protection "1; mode=block"
</VirtualHost>
```

**HTTP to HTTPS Redirect**
```apache
<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / https://example.com/
</VirtualHost>
```

### Nginx SSL Configuration

**SSL Server Block**
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    root /var/www/html/wordpress;
    index index.php index.html;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

**HTTP Redirect**
```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## WordPress SSL Configuration

### wp-config.php Settings

**Force SSL Admin**
```php
// Force SSL for admin area
define('FORCE_SSL_ADMIN', true);

// Set SSL proxy headers (for load balancers)
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}
```

**Cookie Security**
```php
// Secure cookies
define('COOKIE_DOMAIN', '.example.com');
define('COOKIEPATH', '/');
define('SITECOOKIEPATH', '/');
define('COOKIEHASH', md5('your-unique-salt'));
```

### WordPress Database Updates

**Update URLs for HTTPS**
```sql
-- Update site URLs
UPDATE wp_options SET option_value = 'https://example.com' WHERE option_name = 'home';
UPDATE wp_options SET option_value = 'https://example.com' WHERE option_name = 'siteurl';

-- Update content URLs
UPDATE wp_posts SET post_content = REPLACE(post_content, 'http://example.com', 'https://example.com');
UPDATE wp_postmeta SET meta_value = REPLACE(meta_value, 'http://example.com', 'https://example.com');
```

**WP-CLI SSL Migration**
```bash
# Search and replace URLs
wp search-replace 'http://example.com' 'https://example.com' --dry-run
wp search-replace 'http://example.com' 'https://example.com'

# Update WordPress URLs
wp option update home 'https://example.com'
wp option update siteurl 'https://example.com'
```

## Security Headers

### Content Security Policy (CSP)

**Basic CSP Implementation**
```apache
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://fonts.googleapis.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self'"
```

**WordPress-Specific CSP**
```apache
Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.google-analytics.com https://www.googletagmanager.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; connect-src 'self' https://www.google-analytics.com"
```

### Additional Security Headers

**X-Frame-Options**
```apache
# Prevent clickjacking
Header always set X-Frame-Options "SAMEORIGIN"
```

**X-Content-Type-Options**
```apache
# Prevent MIME type sniffing
Header always set X-Content-Type-Options "nosniff"
```

**Referrer Policy**
```apache
# Control referrer information
Header always set Referrer-Policy "strict-origin-when-cross-origin"
```

**Permissions Policy**
```apache
# Control browser features
Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"
```

## WordPress Security Plugins

### Security Plugin Configuration

**Wordfence Security**
- Firewall protection
- Malware scanning
- Login security
- Two-factor authentication
- Real-time monitoring

**Sucuri Security**
- Website firewall
- Malware removal
- DDoS protection
- Performance optimization
- Security monitoring

**iThemes Security**
- Brute force protection
- File change detection
- Database security
- Two-factor authentication
- Security hardening

### Security Hardening

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

**Directory Protection**
```apache
# Protect wp-config.php
<files wp-config.php>
    order allow,deny
    deny from all
</files>

# Protect .htaccess
<files .htaccess>
    order allow,deny
    deny from all
</files>
```

## Advanced SSL Configuration

### OCSP Stapling

**Apache Configuration**
```apache
SSLUseStapling on
SSLStaplingCache "shmcb:logs/stapling-cache(150000)"
```

**Nginx Configuration**
```nginx
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /path/to/root_CA_cert_plus_intermediates;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

### HTTP/2 Configuration

**Apache HTTP/2**
```apache
LoadModule http2_module modules/mod_http2.so
Protocols h2 h2c http/1.1
```

**Nginx HTTP/2**
```nginx
listen 443 ssl http2;
```

### Perfect Forward Secrecy

**Cipher Suite Configuration**
```apache
SSLCipherSuite ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256
SSLHonorCipherOrder on
```

## SSL Testing and Validation

### SSL Testing Tools

**Online Testing Tools**
- SSL Labs SSL Test
- Qualys SSL Test
- SSL Shopper SSL Checker
- Why No Padlock
- Security Headers

**Command Line Tools**
```bash
# OpenSSL testing
openssl s_client -connect example.com:443 -servername example.com

# Certificate information
openssl x509 -in certificate.crt -text -noout

# Certificate chain verification
openssl verify -CAfile ca-bundle.crt certificate.crt
```

### SSL Monitoring

**Certificate Expiry Monitoring**
```bash
#!/bin/bash
# SSL certificate expiry check
echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
```

**Automated Monitoring**
- Certificate expiry alerts
- SSL grade monitoring
- Security header validation
- Performance impact assessment
- Compliance checking

## WordPress Security Best Practices

### Authentication Security

**Strong Passwords**
- Minimum 12 characters
- Mix of letters, numbers, symbols
- Unique passwords
- Regular password changes
- Password manager usage

**Two-Factor Authentication**
- TOTP (Time-based One-Time Password)
- SMS-based authentication
- Hardware tokens
- Backup codes
- Recovery procedures

### Login Security

**Login Protection**
- Limit login attempts
- CAPTCHA integration
- IP whitelisting
- Login monitoring
- Suspicious activity detection

**Admin Security**
- Custom admin URLs
- Strong admin passwords
- Regular admin access review
- Multi-user admin access
- Activity logging

### Database Security

**Database Hardening**
- Strong database passwords
- Limited database user privileges
- Regular database updates
- Database encryption
- Backup encryption

**WordPress Database Security**
- Table prefix changes
- Database user permissions
- Regular database optimization
- Database monitoring
- Access logging

## Compliance and Standards

### Security Standards

**PCI DSS Compliance**
- Payment card data protection
- Secure network architecture
- Regular security testing
- Access control measures
- Monitoring and logging

**GDPR Compliance**
- Data protection measures
- Privacy by design
- Consent management
- Data breach notification
- User rights implementation

### Security Auditing

**Regular Security Audits**
- Vulnerability assessments
- Penetration testing
- Code security reviews
- Configuration audits
- Compliance assessments

**Security Monitoring**
- Real-time threat detection
- Log analysis
- Incident response
- Security metrics
- Continuous improvement

## Troubleshooting SSL Issues

### Common SSL Problems

**Mixed Content Issues**
- HTTP resources on HTTPS pages
- Insecure images and scripts
- Plugin compatibility issues
- Theme compatibility problems
- Third-party service integration

**Certificate Issues**
- Certificate chain problems
- Expired certificates
- Wrong domain certificates
- Self-signed certificates
- Certificate authority issues

### SSL Debugging

**Browser Developer Tools**
- Console errors
- Network tab analysis
- Security tab information
- Certificate details
- Mixed content warnings

**Server Log Analysis**
- SSL handshake errors
- Certificate validation failures
- Configuration errors
- Performance issues
- Security violations

## Performance Considerations

### SSL Performance Impact

**Performance Optimization**
- SSL session caching
- HTTP/2 implementation
- Certificate optimization
- Cipher suite selection
- OCSP stapling

**Monitoring SSL Performance**
- SSL handshake times
- Certificate validation performance
- Cipher suite performance
- Browser compatibility
- User experience impact

### CDN and SSL

**CDN SSL Configuration**
- Origin server SSL
- CDN SSL certificates
- SSL termination
- End-to-end encryption
- Performance optimization

**Cloudflare SSL**
- Flexible SSL
- Full SSL
- Full SSL (Strict)
- Origin certificates
- SSL optimization

## Future Trends

### Emerging Security Technologies

**Quantum-Safe Cryptography**
- Post-quantum algorithms
- Future-proof encryption
- Migration strategies
- Performance considerations
- Implementation planning

**Zero Trust Architecture**
- Identity verification
- Continuous authentication
- Micro-segmentation
- Least privilege access
- Security monitoring

### SSL Evolution

**TLS 1.3 Adoption**
- Improved performance
- Enhanced security
- Simplified handshake
- Forward secrecy
- Browser support

**Certificate Transparency**
- Public certificate logs
- Certificate monitoring
- Transparency reports
- Compliance requirements
- Security benefits