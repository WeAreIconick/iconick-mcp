# WordPress Analytics and Tracking Integration

## Google Analytics 4 Integration

### Basic GA4 Setup
```php
function add_google_analytics() {
    $ga_measurement_id = get_option('ga_measurement_id');
    
    if (!$ga_measurement_id) {
        return;
    }
    ?>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($ga_measurement_id); ?>"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '<?php echo esc_attr($ga_measurement_id); ?>', {
            'custom_map': {
                'custom_parameter_1': 'user_type',
                'custom_parameter_2': 'post_category'
            }
        });
    </script>
    <?php
}
add_action('wp_head', 'add_google_analytics');
```

### Enhanced GA4 with Custom Events
```php
class GoogleAnalytics4 {
    private $measurement_id;
    
    public function __construct() {
        $this->measurement_id = get_option('ga_measurement_id');
        
        if ($this->measurement_id) {
            add_action('wp_head', array($this, 'add_ga4_script'));
            add_action('wp_footer', array($this, 'add_custom_events'));
            add_action('wp_enqueue_scripts', array($this, 'enqueue_analytics_scripts'));
        }
    }
    
    public function add_ga4_script() {
        ?>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=<?php echo esc_attr($this->measurement_id); ?>"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', '<?php echo esc_attr($this->measurement_id); ?>', {
                'send_page_view': false
            });
            
            // Enhanced ecommerce
            gtag('config', '<?php echo esc_attr($this->measurement_id); ?>', {
                'custom_map': {
                    'custom_parameter_1': 'user_type',
                    'custom_parameter_2': 'content_category'
                }
            });
        </script>
        <?php
    }
    
    public function enqueue_analytics_scripts() {
        wp_enqueue_script('ga4-custom', get_template_directory_uri() . '/js/ga4-custom.js', array(), '1.0.0', true);
        
        wp_localize_script('ga4-custom', 'ga4_vars', array(
            'measurement_id' => $this->measurement_id,
            'user_type' => $this->get_user_type(),
            'content_category' => $this->get_content_category()
        ));
    }
    
    public function add_custom_events() {
        ?>
        <script>
        // Track page views
        gtag('event', 'page_view', {
            page_title: document.title,
            page_location: window.location.href,
            user_type: '<?php echo esc_js($this->get_user_type()); ?>',
            content_category: '<?php echo esc_js($this->get_content_category()); ?>'
        });
        
        // Track custom events
        document.addEventListener('DOMContentLoaded', function() {
            // Track newsletter signup
            const newsletterForm = document.getElementById('newsletter-form');
            if (newsletterForm) {
                newsletterForm.addEventListener('submit', function() {
                    gtag('event', 'newsletter_signup', {
                        event_category: 'engagement',
                        event_label: 'footer_newsletter'
                    });
                });
            }
            
            // Track file downloads
            const downloadLinks = document.querySelectorAll('a[href$=".pdf"], a[href$=".zip"], a[href$=".doc"]');
            downloadLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    gtag('event', 'file_download', {
                        event_category: 'engagement',
                        event_label: this.href.split('/').pop(),
                        value: 1
                    });
                });
            });
            
            // Track video plays
            const videos = document.querySelectorAll('video');
            videos.forEach(function(video) {
                video.addEventListener('play', function() {
                    gtag('event', 'video_play', {
                        event_category: 'engagement',
                        event_label: this.src.split('/').pop()
                    });
                });
            });
        });
        </script>
        <?php
    }
    
    private function get_user_type() {
        if (is_user_logged_in()) {
            $user = wp_get_current_user();
            return in_array('administrator', $user->roles) ? 'admin' : 'logged_in';
        }
        return 'guest';
    }
    
    private function get_content_category() {
        if (is_single()) {
            $categories = get_the_category();
            return !empty($categories) ? $categories[0]->name : 'uncategorized';
        } elseif (is_page()) {
            return 'page';
        } elseif (is_home()) {
            return 'blog';
        }
        return 'other';
    }
}

new GoogleAnalytics4();
```

## Facebook Pixel Integration

### Basic Facebook Pixel Setup
```php
function add_facebook_pixel() {
    $pixel_id = get_option('facebook_pixel_id');
    
    if (!$pixel_id) {
        return;
    }
    ?>
    <!-- Facebook Pixel Code -->
    <script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '<?php echo esc_js($pixel_id); ?>');
    fbq('track', 'PageView');
    </script>
    <noscript>
        <img height="1" width="1" style="display:none"
             src="https://www.facebook.com/tr?id=<?php echo esc_attr($pixel_id); ?>&ev=PageView&noscript=1" />
    </noscript>
    <!-- End Facebook Pixel Code -->
    <?php
}
add_action('wp_head', 'add_facebook_pixel');
```

### Enhanced Facebook Pixel with Custom Events
```php
class FacebookPixelIntegration {
    private $pixel_id;
    
    public function __construct() {
        $this->pixel_id = get_option('facebook_pixel_id');
        
        if ($this->pixel_id) {
            add_action('wp_head', array($this, 'add_pixel_code'));
            add_action('wp_footer', array($this, 'add_custom_events'));
        }
    }
    
    public function add_pixel_code() {
        ?>
        <!-- Facebook Pixel Code -->
        <script>
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '<?php echo esc_js($this->pixel_id); ?>');
        fbq('track', 'PageView');
        </script>
        <noscript>
            <img height="1" width="1" style="display:none"
                 src="https://www.facebook.com/tr?id=<?php echo esc_attr($this->pixel_id); ?>&ev=PageView&noscript=1" />
        </noscript>
        <?php
    }
    
    public function add_custom_events() {
        ?>
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Track newsletter signup
            const newsletterForm = document.getElementById('newsletter-form');
            if (newsletterForm) {
                newsletterForm.addEventListener('submit', function() {
                    fbq('track', 'Lead', {
                        content_name: 'Newsletter Signup',
                        content_category: 'Email'
                    });
                });
            }
            
            // Track contact form submissions
            const contactForms = document.querySelectorAll('.contact-form, .wpcf7-form');
            contactForms.forEach(function(form) {
                form.addEventListener('submit', function() {
                    fbq('track', 'Lead', {
                        content_name: 'Contact Form',
                        content_category: 'Contact'
                    });
                });
            });
            
            // Track button clicks
            const ctaButtons = document.querySelectorAll('.cta-button, .btn-primary');
            ctaButtons.forEach(function(button) {
                button.addEventListener('click', function() {
                    fbq('track', 'ViewContent', {
                        content_name: this.textContent.trim(),
                        content_category: 'CTA'
                    });
                });
            });
        });
        </script>
        <?php
    }
}

new FacebookPixelIntegration();
```

## Custom Analytics Dashboard

### WordPress Analytics Dashboard
```php
class WordPressAnalyticsDashboard {
    public function __construct() {
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('wp_dashboard_setup', array($this, 'add_dashboard_widget'));
    }
    
    public function add_admin_menu() {
        add_dashboard_page(
            'Analytics Dashboard',
            'Analytics',
            'manage_options',
            'analytics-dashboard',
            array($this, 'display_dashboard')
        );
    }
    
    public function add_dashboard_widget() {
        wp_add_dashboard_widget(
            'analytics_widget',
            'Site Analytics',
            array($this, 'display_dashboard_widget')
        );
    }
    
    public function display_dashboard() {
        ?>
        <div class="wrap">
            <h1>Analytics Dashboard</h1>
            
            <div class="analytics-grid">
                <div class="analytics-card">
                    <h3>Page Views (Last 30 Days)</h3>
                    <div class="analytics-number"><?php echo $this->get_page_views(); ?></div>
                </div>
                
                <div class="analytics-card">
                    <h3>Unique Visitors</h3>
                    <div class="analytics-number"><?php echo $this->get_unique_visitors(); ?></div>
                </div>
                
                <div class="analytics-card">
                    <h3>Top Pages</h3>
                    <ul>
                        <?php foreach ($this->get_top_pages() as $page) : ?>
                            <li><?php echo esc_html($page['title']); ?> (<?php echo $page['views']; ?>)</li>
                        <?php endforeach; ?>
                    </ul>
                </div>
                
                <div class="analytics-card">
                    <h3>Traffic Sources</h3>
                    <ul>
                        <?php foreach ($this->get_traffic_sources() as $source) : ?>
                            <li><?php echo esc_html($source['name']); ?> (<?php echo $source['percentage']; ?>%)</li>
                        <?php endforeach; ?>
                    </ul>
                </div>
            </div>
        </div>
        
        <style>
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .analytics-card {
            background: white;
            padding: 20px;
            border: 1px solid #ccd0d4;
            border-radius: 4px;
        }
        .analytics-number {
            font-size: 2em;
            font-weight: bold;
            color: #0073aa;
        }
        </style>
        <?php
    }
    
    private function get_page_views() {
        global $wpdb;
        
        $result = $wpdb->get_var("
            SELECT SUM(meta_value) 
            FROM {$wpdb->postmeta} 
            WHERE meta_key = '_page_views' 
            AND post_id IN (
                SELECT post_id 
                FROM {$wpdb->postmeta} 
                WHERE meta_key = '_page_views_date' 
                AND meta_value >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            )
        ");
        
        return $result ?: 0;
    }
    
    private function get_unique_visitors() {
        // Implementation for unique visitors tracking
        return 0;
    }
    
    private function get_top_pages() {
        global $wpdb;
        
        $results = $wpdb->get_results("
            SELECT p.post_title as title, pm.meta_value as views
            FROM {$wpdb->posts} p
            JOIN {$wpdb->postmeta} pm ON p.ID = pm.post_id
            WHERE pm.meta_key = '_page_views'
            AND p.post_status = 'publish'
            ORDER BY CAST(pm.meta_value AS UNSIGNED) DESC
            LIMIT 5
        ");
        
        return $results ?: array();
    }
    
    private function get_traffic_sources() {
        // Implementation for traffic sources
        return array(
            array('name' => 'Direct', 'percentage' => 45),
            array('name' => 'Google', 'percentage' => 30),
            array('name' => 'Social Media', 'percentage' => 15),
            array('name' => 'Other', 'percentage' => 10)
        );
    }
}

new WordPressAnalyticsDashboard();
```

## Best Practices

1. **Respect user privacy** and GDPR compliance
2. **Use proper data sanitization** for all tracking data
3. **Implement cookie consent** mechanisms
4. **Test tracking implementations** thoroughly
5. **Use Google Tag Manager** for complex setups
6. **Monitor tracking accuracy** regularly
7. **Implement error handling** for failed tracking
8. **Use server-side tracking** for critical events
9. **Document tracking implementations** clearly
10. **Regularly audit tracking** for accuracy

## Resources

- [Google Analytics 4 Documentation](https://developers.google.com/analytics/devguides/collection/ga4)
- [Facebook Pixel Documentation](https://developers.facebook.com/docs/facebook-pixel/)
- [Google Tag Manager Documentation](https://developers.google.com/tag-manager)
- [WordPress Privacy and GDPR](https://developer.wordpress.org/plugins/privacy/)