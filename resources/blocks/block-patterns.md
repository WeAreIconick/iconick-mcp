---
difficulty: Beginner
tags: [blocks, patterns, templates, reusable]
related: [blocks/gutenberg-basics, themes/block-themes]
wp_version: 5.5+
---

# WordPress Block Patterns

Block patterns are predefined block layouts that users can insert with one click.

## Basic Block Pattern Registration

### PHP Pattern Registration

```php
// Register a simple block pattern
function register_custom_patterns() {
    register_block_pattern(
        'my-plugin/hero-section',
        array(
            'title' => 'Hero Section',
            'description' => 'A hero section with title, subtitle, and call-to-action button',
            'content' => '<!-- wp:group {"className":"hero-section"} -->
<div class="wp-block-group hero-section">
    <!-- wp:heading {"level":1,"className":"hero-title"} -->
    <h1 class="hero-title">Welcome to Our Site</h1>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph {"className":"hero-subtitle"} -->
    <p class="hero-subtitle">Discover amazing content and connect with our community</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:buttons -->
    <div class="wp-block-buttons">
        <!-- wp:button {"className":"hero-button"} -->
        <div class="wp-block-button hero-button">
            <a class="wp-block-button__link">Get Started</a>
        </div>
        <!-- /wp:button -->
    </div>
    <!-- /wp:buttons -->
</div>
<!-- /wp:group -->',
            'categories' => array( 'hero' ),
            'keywords' => array( 'hero', 'section', 'welcome', 'cta' )
        )
    );
}
add_action( 'init', 'register_custom_patterns' );
```

### Advanced Pattern with Dynamic Content

```php
// Register pattern with dynamic content
function register_dynamic_pattern() {
    register_block_pattern(
        'my-plugin/featured-posts',
        array(
            'title' => 'Featured Posts Grid',
            'description' => 'A grid layout showcasing featured posts',
            'content' => '<!-- wp:group {"className":"featured-posts-section"} -->
<div class="wp-block-group featured-posts-section">
    <!-- wp:heading {"level":2,"className":"section-title"} -->
    <h2 class="section-title">Featured Posts</h2>
    <!-- /wp:heading -->
    
    <!-- wp:columns {"className":"posts-grid"} -->
    <div class="wp-block-columns posts-grid">
        <!-- wp:column -->
        <div class="wp-block-column">
            <!-- wp:post-featured-image /-->
            <!-- wp:post-title {"level":3} /-->
            <!-- wp:post-excerpt /-->
            <!-- wp:post-date /-->
        </div>
        <!-- /wp:column -->
        
        <!-- wp:column -->
        <div class="wp-block-column">
            <!-- wp:post-featured-image /-->
            <!-- wp:post-title {"level":3} /-->
            <!-- wp:post-excerpt /-->
            <!-- wp:post-date /-->
        </div>
        <!-- /wp:column -->
        
        <!-- wp:column -->
        <div class="wp-block-column">
            <!-- wp:post-featured-image /-->
            <!-- wp:post-title {"level":3} /-->
            <!-- wp:post-excerpt /-->
            <!-- wp:post-date /-->
        </div>
        <!-- /wp:column -->
    </div>
    <!-- /wp:columns -->
</div>
<!-- /wp:group -->',
            'categories' => array( 'posts', 'grid' ),
            'keywords' => array( 'posts', 'grid', 'featured', 'layout' )
        )
    );
}
add_action( 'init', 'register_dynamic_pattern' );
```

## Pattern Categories

### Custom Pattern Categories

```php
// Register custom pattern categories
function register_pattern_categories() {
    register_block_pattern_category(
        'hero',
        array(
            'label' => 'Hero Sections',
            'description' => 'Eye-catching hero sections and banners'
        )
    );
    
    register_block_pattern_category(
        'features',
        array(
            'label' => 'Feature Sections',
            'description' => 'Feature highlights and service sections'
        )
    );
    
    register_block_pattern_category(
        'testimonials',
        array(
            'label' => 'Testimonials',
            'description' => 'Customer testimonials and reviews'
        )
    );
    
    register_block_pattern_category(
        'cta',
        array(
            'label' => 'Call to Action',
            'description' => 'Call-to-action sections and buttons'
        )
    );
}
add_action( 'init', 'register_pattern_categories' );
```

### Pattern with Custom Category

```php
// Register pattern in custom category
function register_cta_pattern() {
    register_block_pattern(
        'my-plugin/cta-banner',
        array(
            'title' => 'CTA Banner',
            'description' => 'A prominent call-to-action banner with background image',
            'content' => '<!-- wp:cover {"url":"","id":0,"dimRatio":50,"overlayColor":"primary","className":"cta-banner"} -->
<div class="wp-block-cover cta-banner">
    <span aria-hidden="true" class="wp-block-cover__background has-primary-background-color has-background-dim"></span>
    <div class="wp-block-cover__inner-container">
        <!-- wp:heading {"textAlign":"center","textColor":"white","level":2} -->
        <h2 class="has-text-align-center has-white-color has-text-color">Ready to Get Started?</h2>
        <!-- /wp:heading -->
        
        <!-- wp:paragraph {"align":"center","textColor":"white"} -->
        <p class="has-text-align-center has-white-color has-text-color">Join thousands of satisfied customers today</p>
        <!-- /wp:paragraph -->
        
        <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
        <div class="wp-block-buttons">
            <!-- wp:button {"textColor":"white","style":{"border":{"radius":"0px"},"color":{"background":"#ff6b35"}}} -->
            <div class="wp-block-button">
                <a class="wp-block-button__link has-white-color has-text-color has-background" style="background-color:#ff6b35;border-radius:0px">Sign Up Now</a>
            </div>
            <!-- /wp:button -->
        </div>
        <!-- /wp:buttons -->
    </div>
</div>
<!-- /wp:cover -->',
            'categories' => array( 'cta', 'banner' ),
            'keywords' => array( 'cta', 'banner', 'call-to-action', 'signup' )
        )
    );
}
add_action( 'init', 'register_cta_pattern' );
```

## Complex Layout Patterns

### Multi-Column Layout

```php
// Register complex multi-column pattern
function register_complex_layout_pattern() {
    register_block_pattern(
        'my-plugin/services-layout',
        array(
            'title' => 'Services Layout',
            'description' => 'A comprehensive services section with icons and descriptions',
            'content' => '<!-- wp:group {"className":"services-section","layout":{"type":"constrained"}} -->
<div class="wp-block-group services-section">
    <!-- wp:heading {"textAlign":"center","level":2,"className":"section-title"} -->
    <h2 class="wp-block-heading has-text-align-center section-title">Our Services</h2>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph {"align":"center","className":"section-subtitle"} -->
    <p class="has-text-align-center section-subtitle">We provide comprehensive solutions for your business needs</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:columns {"className":"services-grid"} -->
    <div class="wp-block-columns services-grid">
        <!-- wp:column {"className":"service-item"} -->
        <div class="wp-block-column service-item">
            <!-- wp:html -->
            <div class="service-icon">🚀</div>
            <!-- /wp:html -->
            
            <!-- wp:heading {"level":3,"className":"service-title"} -->
            <h3 class="wp-block-heading service-title">Web Development</h3>
            <!-- /wp:heading -->
            
            <!-- wp:paragraph {"className":"service-description"} -->
            <p class="service-description">Custom web applications built with modern technologies and best practices.</p>
            <!-- /wp:paragraph -->
            
            <!-- wp:buttons -->
            <div class="wp-block-buttons">
                <!-- wp:button {"className":"service-button"} -->
                <div class="wp-block-button service-button">
                    <a class="wp-block-button__link">Learn More</a>
                </div>
                <!-- /wp:button -->
            </div>
            <!-- /wp:buttons -->
        </div>
        <!-- /wp:column -->
        
        <!-- wp:column {"className":"service-item"} -->
        <div class="wp-block-column service-item">
            <!-- wp:html -->
            <div class="service-icon">📱</div>
            <!-- /wp:html -->
            
            <!-- wp:heading {"level":3,"className":"service-title"} -->
            <h3 class="wp-block-heading service-title">Mobile Apps</h3>
            <!-- /wp:heading -->
            
            <!-- wp:paragraph {"className":"service-description"} -->
            <p class="service-description">Native and cross-platform mobile applications for iOS and Android.</p>
            <!-- /wp:paragraph -->
            
            <!-- wp:buttons -->
            <div class="wp-block-buttons">
                <!-- wp:button {"className":"service-button"} -->
                <div class="wp-block-button service-button">
                    <a class="wp-block-button__link">Learn More</a>
                </div>
                <!-- /wp:button -->
            </div>
            <!-- /wp:buttons -->
        </div>
        <!-- /wp:column -->
        
        <!-- wp:column {"className":"service-item"} -->
        <div class="wp-block-column service-item">
            <!-- wp:html -->
            <div class="service-icon">☁️</div>
            <!-- /wp:html -->
            
            <!-- wp:heading {"level":3,"className":"service-title"} -->
            <h3 class="wp-block-heading service-title">Cloud Solutions</h3>
            <!-- /wp:heading -->
            
            <!-- wp:paragraph {"className":"service-description"} -->
            <p class="service-description">Scalable cloud infrastructure and deployment solutions.</p>
            <!-- /wp:paragraph -->
            
            <!-- wp:buttons -->
            <div class="wp-block-buttons">
                <!-- wp:button {"className":"service-button"} -->
                <div class="wp-block-button service-button">
                    <a class="wp-block-button__link">Learn More</a>
                </div>
                <!-- /wp:button -->
            </div>
            <!-- /wp:buttons -->
        </div>
        <!-- /wp:column -->
    </div>
    <!-- /wp:columns -->
</div>
<!-- /wp:group -->',
            'categories' => array( 'features', 'services' ),
            'keywords' => array( 'services', 'features', 'grid', 'layout' )
        )
    );
}
add_action( 'init', 'register_complex_layout_pattern' );
```

### Pricing Table Pattern

```php
// Register pricing table pattern
function register_pricing_pattern() {
    register_block_pattern(
        'my-plugin/pricing-table',
        array(
            'title' => 'Pricing Table',
            'description' => 'A three-column pricing table with different plan options',
            'content' => '<!-- wp:group {"className":"pricing-section"} -->
<div class="wp-block-group pricing-section">
    <!-- wp:heading {"textAlign":"center","level":2} -->
    <h2 class="wp-block-heading has-text-align-center">Choose Your Plan</h2>
    <!-- /wp:heading -->
    
    <!-- wp:columns {"className":"pricing-grid"} -->
    <div class="wp-block-columns pricing-grid">
        <!-- wp:column {"className":"pricing-card"} -->
        <div class="wp-block-column pricing-card">
            <!-- wp:group {"className":"pricing-header"} -->
            <div class="wp-block-group pricing-header">
                <!-- wp:heading {"level":3,"className":"plan-name"} -->
                <h3 class="wp-block-heading plan-name">Basic</h3>
                <!-- /wp:heading -->
                
                <!-- wp:paragraph {"className":"plan-price"} -->
                <p class="plan-price"><span class="currency">$</span><span class="amount">19</span><span class="period">/month</span></p>
                <!-- /wp:paragraph -->
            </div>
            <!-- /wp:group -->
            
            <!-- wp:list {"className":"plan-features"} -->
            <ul class="plan-features">
                <!-- wp:list-item -->
                <li>Up to 5 projects</li>
                <!-- /wp:list-item -->
                
                <!-- wp:list-item -->
                <li>Basic support</li>
                <!-- /wp:list-item -->
                
                <!-- wp:list-item -->
                <li>Standard templates</li>
                <!-- /wp:list-item -->
            </ul>
            <!-- /wp:list -->
            
            <!-- wp:buttons -->
            <div class="wp-block-buttons">
                <!-- wp:button {"className":"pricing-button"} -->
                <div class="wp-block-button pricing-button">
                    <a class="wp-block-button__link">Get Started</a>
                </div>
                <!-- /wp:button -->
            </div>
            <!-- /wp:buttons -->
        </div>
        <!-- /wp:column -->
        
        <!-- wp:column {"className":"pricing-card featured"} -->
        <div class="wp-block-column pricing-card featured">
            <!-- wp:group {"className":"pricing-header"} -->
            <div class="wp-block-group pricing-header">
                <!-- wp:paragraph {"className":"popular-badge"} -->
                <p class="popular-badge">Most Popular</p>
                <!-- /wp:paragraph -->
                
                <!-- wp:heading {"level":3,"className":"plan-name"} -->
                <h3 class="wp-block-heading plan-name">Pro</h3>
                <!-- /wp:heading -->
                
                <!-- wp:paragraph {"className":"plan-price"} -->
                <p class="plan-price"><span class="currency">$</span><span class="amount">49</span><span class="period">/month</span></p>
                <!-- /wp:paragraph -->
            </div>
            <!-- /wp:group -->
            
            <!-- wp:list {"className":"plan-features"} -->
            <ul class="plan-features">
                <!-- wp:list-item -->
                <li>Unlimited projects</li>
                <!-- /wp:list-item -->
                
                <!-- wp:list-item -->
                <li>Priority support</li>
                <!-- /wp:list-item -->
                
                <!-- wp:list-item -->
                <li>Premium templates</li>
                <!-- /wp:list-item -->
                
                <!-- wp:list-item -->
                <li>Advanced analytics</li>
                <!-- /wp:list-item -->
            </ul>
            <!-- /wp:list -->
            
            <!-- wp:buttons -->
            <div class="wp-block-buttons">
                <!-- wp:button {"className":"pricing-button"} -->
                <div class="wp-block-button pricing-button">
                    <a class="wp-block-button__link">Get Started</a>
                </div>
                <!-- /wp:button -->
            </div>
            <!-- /wp:buttons -->
        </div>
        <!-- /wp:column -->
        
        <!-- wp:column {"className":"pricing-card"} -->
        <div class="wp-block-column pricing-card">
            <!-- wp:group {"className":"pricing-header"} -->
            <div class="wp-block-group pricing-header">
                <!-- wp:heading {"level":3,"className":"plan-name"} -->
                <h3 class="wp-block-heading plan-name">Enterprise</h3>
                <!-- /wp:heading -->
                
                <!-- wp:paragraph {"className":"plan-price"} -->
                <p class="plan-price"><span class="currency">$</span><span class="amount">99</span><span class="period">/month</span></p>
                <!-- /wp:paragraph -->
            </div>
            <!-- /wp:group -->
            
            <!-- wp:list {"className":"plan-features"} -->
            <ul class="plan-features">
                <!-- wp:list-item -->
                <li>Unlimited everything</li>
                <!-- /wp:list-item -->
                
                <!-- wp:list-item -->
                <li>24/7 dedicated support</li>
                <!-- /wp:list-item -->
                
                <!-- wp:list-item -->
                <li>Custom integrations</li>
                <!-- /wp:list-item -->
                
                <!-- wp:list-item -->
                <li>White-label options</li>
                <!-- /wp:list-item -->
            </ul>
            <!-- /wp:list -->
            
            <!-- wp:buttons -->
            <div class="wp-block-buttons">
                <!-- wp:button {"className":"pricing-button"} -->
                <div class="wp-block-button pricing-button">
                    <a class="wp-block-button__link">Contact Sales</a>
                </div>
                <!-- /wp:button -->
            </div>
            <!-- /wp:buttons -->
        </div>
        <!-- /wp:column -->
    </div>
    <!-- /wp:columns -->
</div>
<!-- /wp:group -->',
            'categories' => array( 'pricing', 'tables' ),
            'keywords' => array( 'pricing', 'table', 'plans', 'subscription' )
        )
    );
}
add_action( 'init', 'register_pricing_pattern' );
```

## Dynamic Patterns

### Pattern with Custom Fields

```php
// Register pattern that uses custom fields
function register_dynamic_pattern_with_fields() {
    register_block_pattern(
        'my-plugin/testimonial-slider',
        array(
            'title' => 'Testimonial Slider',
            'description' => 'A testimonial slider with customer reviews',
            'content' => '<!-- wp:group {"className":"testimonial-section"} -->
<div class="wp-block-group testimonial-section">
    <!-- wp:heading {"textAlign":"center","level":2} -->
    <h2 class="wp-block-heading has-text-align-center">What Our Customers Say</h2>
    <!-- /wp:heading -->
    
    <!-- wp:group {"className":"testimonial-slider"} -->
    <div class="wp-block-group testimonial-slider">
        <!-- wp:group {"className":"testimonial-item"} -->
        <div class="wp-block-group testimonial-item">
            <!-- wp:paragraph {"className":"testimonial-text"} -->
            <p class="testimonial-text">"This service has completely transformed our business. The results exceeded our expectations."</p>
            <!-- /wp:paragraph -->
            
            <!-- wp:group {"className":"testimonial-author"} -->
            <div class="wp-block-group testimonial-author">
                <!-- wp:image {"className":"author-avatar"} -->
                <figure class="wp-block-image author-avatar">
                    <img alt="Customer Avatar" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMzIiIGN5PSIzMiIgcj0iMzIiIGZpbGw9IiNmM2Y0ZjYiLz4KPHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4PSIyMCIgeT0iMjAiPgo8cGF0aCBkPSJNMTIgMTJDMTQuMjA5MSAxMiAxNiAxMC4yMDkxIDE2IDhDMTYgNS43OTA5IDE0LjIwOTEgNCAxMiA0QzkuNzkwODYgNCA4IDUuNzkwOSA4IDhDOCAxMC4yMDkxIDkuNzkwODYgMTIgMTIgMTJaIiBmaWxsPSIjOWM5Yzk5Ii8+CjxwYXRoIGQ9Ik0xMiAxNEM3LjU4MTcyIDE0IDQgMTcuNTgxNyA0IDIySDEwVjE2QzEwIDE0Ljg5NTQgMTAuODk1NCAxNCAxMiAxNFoiIGZpbGw9IiM5YzljOTkiLz4KPC9zdmc+Cjwvc3ZnPgo=" />
                </figure>
                <!-- /wp:image -->
                
                <!-- wp:group {"className":"author-info"} -->
                <div class="wp-block-group author-info">
                    <!-- wp:paragraph {"className":"author-name"} -->
                    <p class="author-name">John Smith</p>
                    <!-- /wp:paragraph -->
                    
                    <!-- wp:paragraph {"className":"author-title"} -->
                    <p class="author-title">CEO, Company Inc.</p>
                    <!-- /wp:paragraph -->
                </div>
                <!-- /wp:group -->
            </div>
            <!-- /wp:group -->
        </div>
        <!-- /wp:group -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->',
            'categories' => array( 'testimonials', 'slider' ),
            'keywords' => array( 'testimonial', 'review', 'customer', 'slider' )
        )
    );
}
add_action( 'init', 'register_dynamic_pattern_with_fields' );
```

## Pattern Styling

### CSS for Patterns

```css
/* Hero Section Pattern Styles */
.hero-section {
    padding: 4rem 2rem;
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-button .wp-block-button__link {
    background-color: #ff6b35;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    border-radius: 50px;
    transition: transform 0.3s ease;
}

.hero-button .wp-block-button__link:hover {
    transform: translateY(-2px);
}

/* Services Grid Pattern Styles */
.services-section {
    padding: 4rem 2rem;
}

.services-grid {
    gap: 2rem;
    margin-top: 3rem;
}

.service-item {
    text-align: center;
    padding: 2rem;
    border: 1px solid #e1e5e9;
    border-radius: 8px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.service-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.service-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.service-title {
    margin-bottom: 1rem;
    color: #2c3e50;
}

.service-description {
    margin-bottom: 1.5rem;
    color: #7f8c8d;
}

/* Pricing Table Pattern Styles */
.pricing-section {
    padding: 4rem 2rem;
}

.pricing-grid {
    gap: 2rem;
    margin-top: 3rem;
}

.pricing-card {
    border: 2px solid #e1e5e9;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    position: relative;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.pricing-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
}

.pricing-card.featured {
    border-color: #3498db;
    transform: scale(1.05);
}

.popular-badge {
    background-color: #3498db;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: inline-block;
}

.plan-name {
    margin-bottom: 1rem;
    color: #2c3e50;
}

.plan-price {
    font-size: 2.5rem;
    font-weight: 700;
    color: #3498db;
    margin-bottom: 2rem;
}

.currency {
    font-size: 1.5rem;
    vertical-align: top;
}

.period {
    font-size: 1rem;
    font-weight: 400;
    color: #7f8c8d;
}

.plan-features {
    list-style: none;
    padding: 0;
    margin-bottom: 2rem;
}

.plan-features li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #f8f9fa;
}

.pricing-button .wp-block-button__link {
    width: 100%;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
}
```

## Pattern Best Practices

### Performance Considerations

```php
// Optimize pattern registration
function optimized_pattern_registration() {
    // Only register patterns if block editor is available
    if ( ! function_exists( 'register_block_pattern' ) ) {
        return;
    }
    
    // Register patterns conditionally
    if ( is_admin() || ( defined( 'REST_REQUEST' ) && REST_REQUEST ) ) {
        register_custom_patterns();
    }
}
add_action( 'init', 'optimized_pattern_registration' );

// Lazy load pattern content for large patterns
function register_large_pattern() {
    register_block_pattern(
        'my-plugin/large-layout',
        array(
            'title' => 'Large Layout Pattern',
            'description' => 'A comprehensive page layout',
            'content' => get_large_pattern_content(), // Load from file
            'categories' => array( 'layouts' ),
            'keywords' => array( 'layout', 'page', 'comprehensive' )
        )
    );
}

function get_large_pattern_content() {
    $pattern_file = plugin_dir_path( __FILE__ ) . 'patterns/large-layout.html';
    
    if ( file_exists( $pattern_file ) ) {
        return file_get_contents( $pattern_file );
    }
    
    return '<!-- Fallback content -->';
}
```

### Accessibility

```php
// Ensure patterns are accessible
function register_accessible_pattern() {
    register_block_pattern(
        'my-plugin/accessible-hero',
        array(
            'title' => 'Accessible Hero Section',
            'description' => 'A hero section with proper accessibility features',
            'content' => '<!-- wp:cover {"url":"","id":0,"dimRatio":50,"overlayColor":"primary","className":"accessible-hero"} -->
<div class="wp-block-cover accessible-hero">
    <span aria-hidden="true" class="wp-block-cover__background has-primary-background-color has-background-dim"></span>
    <div class="wp-block-cover__inner-container">
        <!-- wp:heading {"textAlign":"center","level":1,"textColor":"white"} -->
        <h1 class="wp-block-heading has-text-align-center has-white-color has-text-color">Welcome to Our Platform</h1>
        <!-- /wp:heading -->
        
        <!-- wp:paragraph {"align":"center","textColor":"white"} -->
        <p class="has-text-align-center has-white-color has-text-color">Building the future with innovative solutions</p>
        <!-- /wp:paragraph -->
        
        <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
        <div class="wp-block-buttons">
            <!-- wp:button {"textColor":"white","style":{"border":{"radius":"0px"},"color":{"background":"#ff6b35"}}} -->
            <div class="wp-block-button">
                <a class="wp-block-button__link has-white-color has-text-color has-background" style="background-color:#ff6b35;border-radius:0px" role="button" aria-label="Get started with our platform">Get Started</a>
            </div>
            <!-- /wp:button -->
        </div>
        <!-- /wp:buttons -->
    </div>
</div>
<!-- /wp:cover -->',
            'categories' => array( 'hero', 'accessible' ),
            'keywords' => array( 'hero', 'accessible', 'banner' )
        )
    );
}
```

## Official Documentation

https://developer.wordpress.org/block-editor/reference-guides/block-api/block-registration/
https://developer.wordpress.org/block-editor/reference-guides/block-patterns/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-supports/
