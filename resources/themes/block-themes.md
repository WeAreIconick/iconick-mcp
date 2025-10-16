---
difficulty: Advanced
tags: [themes, blocks, fse, full-site-editing]
related: [blocks/gutenberg-basics, themes/theme-development]
wp_version: 5.9+
---

# WordPress Block Themes

Block themes are the modern approach to WordPress theming, using HTML templates and block patterns.

## Block Theme Structure

### Basic Block Theme Files

```
my-block-theme/
├── style.css
├── index.html
├── theme.json
├── templates/
│   ├── index.html
│   ├── single.html
│   ├── page.html
│   ├── archive.html
│   ├── search.html
│   ├── 404.html
│   └── front-page.html
├── template-parts/
│   ├── header.html
│   ├── footer.html
│   └── post-meta.html
└── parts/
    ├── header.html
    ├── footer.html
    └── sidebar.html
```

### Style.css Header

```css
/*
Theme Name: My Block Theme
Description: A modern block theme built with WordPress full site editing.
Version: 1.0.0
Requires at least: 6.0
Tested up to: 6.4
Requires PHP: 7.4
License: GPL-2.0-or-later
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: my-block-theme
Tags: block-theme, full-site-editing, accessibility-ready
*/
```

## Template Files

### Index Template (index.html)

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
    <!-- wp:query {"queryId":0,"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"","inherit":true}} -->
    <div class="wp-block-query">
        <!-- wp:post-template -->
        <!-- wp:group {"style":{"spacing":{"blockGap":"1rem"}}} -->
        <div class="wp-block-group">
            <!-- wp:post-title {"level":2,"isLink":true} /-->
            <!-- wp:post-featured-image {"isLink":true} /-->
            <!-- wp:post-excerpt /-->
            <!-- wp:template-part {"slug":"post-meta","tagName":"footer"} /-->
        </div>
        <!-- /wp:group -->
        <!-- /wp:post-template -->
        
        <!-- wp:query-pagination -->
        <!-- wp:query-pagination-previous /-->
        <!-- wp:query-pagination-numbers /-->
        <!-- wp:query-pagination-next /-->
        <!-- /wp:query-pagination -->
    </div>
    <!-- /wp:query -->
</div>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

### Single Post Template (single.html)

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
    <!-- wp:post-title {"level":1} /-->
    
    <!-- wp:group {"style":{"spacing":{"blockGap":"1rem"}},"layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between"}} -->
    <div class="wp-block-group">
        <!-- wp:post-date /-->
        <!-- wp:post-author {"showAvatar":false} /-->
        <!-- wp:post-terms {"term":"category"} /-->
    </div>
    <!-- /wp:group -->
    
    <!-- wp:post-featured-image {"align":"wide"} /-->
    
    <!-- wp:post-content {"align":"wide"} /-->
    
    <!-- wp:group {"style":{"spacing":{"blockGap":"1rem"}},"layout":{"type":"flex","flexWrap":"wrap"}} -->
    <div class="wp-block-group">
        <!-- wp:post-terms {"term":"post_tag"} /-->
        <!-- wp:post-navigation-link {"type":"previous","label":"Previous Post"} /-->
        <!-- wp:post-navigation-link {"type":"next","label":"Next Post"} /-->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

### Page Template (page.html)

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
    <!-- wp:post-title {"level":1} /-->
    <!-- wp:post-content /-->
</div>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

### Archive Template (archive.html)

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
    <!-- wp:query-title {"type":"archive"} /-->
    
    <!-- wp:term-description /-->
    
    <!-- wp:query {"queryId":0,"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","author":"","search":"","exclude":[],"sticky":"","inherit":true}} -->
    <div class="wp-block-query">
        <!-- wp:post-template -->
        <!-- wp:group {"style":{"spacing":{"blockGap":"1rem"}}} -->
        <div class="wp-block-group">
            <!-- wp:post-title {"level":2,"isLink":true} /-->
            <!-- wp:post-featured-image {"isLink":true} /-->
            <!-- wp:post-excerpt /-->
            <!-- wp:post-date /-->
        </div>
        <!-- /wp:group -->
        <!-- /wp:post-template -->
        
        <!-- wp:query-pagination -->
        <!-- wp:query-pagination-previous /-->
        <!-- wp:query-pagination-numbers /-->
        <!-- wp:query-pagination-next /-->
        <!-- /wp:query-pagination -->
    </div>
    <!-- /wp:query -->
</div>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

## Template Parts

### Header Template Part (template-parts/header.html)

```html
<!-- wp:group {"style":{"spacing":{"padding":{"top":"1rem","bottom":"1rem"}}},"backgroundColor":"primary","textColor":"white","layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between","verticalAlignment":"center"}} -->
<div class="wp-block-group">
    <!-- wp:group {"style":{"spacing":{"blockGap":"1rem"}},"layout":{"type":"flex","flexWrap":"wrap","verticalAlignment":"center"}} -->
    <div class="wp-block-group">
        <!-- wp:site-logo {"width":60} /-->
        <!-- wp:site-title {"level":0,"style":{"typography":{"fontStyle":"normal","fontWeight":"700"}}} /-->
    </div>
    <!-- /wp:group -->
    
    <!-- wp:navigation {"ref":4,"overlayMenu":"mobile","layout":{"type":"flex","setCascadingProperties":true,"justifyContent":"right"}} -->
    <!-- wp:page-list /-->
    <!-- /wp:navigation -->
</div>
<!-- /wp:group -->
```

### Footer Template Part (template-parts/footer.html)

```html
<!-- wp:group {"style":{"spacing":{"padding":{"top":"2rem","bottom":"2rem"}}},"backgroundColor":"secondary","textColor":"white","layout":{"type":"constrained"}} -->
<div class="wp-block-group">
    <!-- wp:group {"style":{"spacing":{"blockGap":"2rem"}},"layout":{"type":"grid","columnCount":3}} -->
    <div class="wp-block-group">
        <!-- wp:group -->
        <div class="wp-block-group">
            <!-- wp:heading {"level":3} -->
            <h3>About</h3>
            <!-- /wp:heading -->
            <!-- wp:paragraph -->
            <p>This is a modern block theme built with WordPress full site editing capabilities.</p>
            <!-- /wp:paragraph -->
        </div>
        <!-- /wp:group -->
        
        <!-- wp:group -->
        <div class="wp-block-group">
            <!-- wp:heading {"level":3} -->
            <h3>Quick Links</h3>
            <!-- /wp:heading -->
            <!-- wp:navigation {"ref":5,"layout":{"type":"flex","orientation":"vertical"}} -->
            <!-- wp:page-list /-->
            <!-- /wp:navigation -->
        </div>
        <!-- /wp:group -->
        
        <!-- wp:group -->
        <div class="wp-block-group">
            <!-- wp:heading {"level":3} -->
            <h3>Contact</h3>
            <!-- /wp:heading -->
            <!-- wp:paragraph -->
            <p>Email: info@example.com<br>Phone: (555) 123-4567</p>
            <!-- /wp:paragraph -->
        </div>
        <!-- /wp:group -->
    </div>
    <!-- /wp:group -->
    
    <!-- wp:separator {"style":{"spacing":{"margin":{"top":"2rem","bottom":"1rem"}}}} -->
    <hr class="wp-block-separator"/>
    <!-- /wp:separator -->
    
    <!-- wp:group {"style":{"spacing":{"blockGap":"1rem"}},"layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between","verticalAlignment":"center"}} -->
    <div class="wp-block-group">
        <!-- wp:paragraph -->
        <p>&copy; 2024 My Block Theme. All rights reserved.</p>
        <!-- /wp:paragraph -->
        
        <!-- wp:social-links {"iconColor":"white","iconColorValue":"#ffffff","openInNewTab":true} -->
        <ul class="wp-block-social-links">
            <!-- wp:social-link {"url":"https://facebook.com","service":"facebook"} /-->
            <!-- wp:social-link {"url":"https://twitter.com","service":"twitter"} /-->
            <!-- wp:social-link {"url":"https://instagram.com","service":"instagram"} /-->
        </ul>
        <!-- /wp:social-links -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->
```

### Post Meta Template Part (template-parts/post-meta.html)

```html
<!-- wp:group {"style":{"spacing":{"blockGap":"0.5rem"}},"layout":{"type":"flex","flexWrap":"wrap"}} -->
<div class="wp-block-group">
    <!-- wp:post-date /-->
    <!-- wp:post-author {"showAvatar":false} /-->
    <!-- wp:post-terms {"term":"category"} /-->
    <!-- wp:post-terms {"term":"post_tag"} /-->
</div>
<!-- /wp:group -->
```

## Block Patterns

### Pattern Registration

```php
// functions.php - Register block patterns
function register_block_patterns() {
    register_block_pattern(
        'my-theme/hero-section',
        array(
            'title' => 'Hero Section',
            'description' => 'A hero section with title, subtitle, and call-to-action button',
            'content' => '<!-- wp:group {"style":{"spacing":{"padding":{"top":"4rem","bottom":"4rem"}}},"backgroundColor":"primary","textColor":"white","align":"full"} -->
<div class="wp-block-group alignfull">
    <!-- wp:group {"layout":{"type":"constrained","contentSize":"800px"}} -->
    <div class="wp-block-group">
        <!-- wp:heading {"textAlign":"center","level":1,"style":{"typography":{"fontSize":"3rem","fontWeight":"700"}}} -->
        <h1 class="wp-block-heading has-text-align-center">Welcome to Our Site</h1>
        <!-- /wp:heading -->
        
        <!-- wp:paragraph {"align":"center","style":{"typography":{"fontSize":"1.25rem"}}} -->
        <p class="has-text-align-center">Discover amazing content and connect with our community</p>
        <!-- /wp:paragraph -->
        
        <!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
        <div class="wp-block-buttons">
            <!-- wp:button {"style":{"border":{"radius":"50px"},"color":{"background":"#ff6b35"}}} -->
            <div class="wp-block-button">
                <a class="wp-block-button__link wp-element-button">Get Started</a>
            </div>
            <!-- /wp:button -->
        </div>
        <!-- /wp:buttons -->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->',
            'categories' => array('hero'),
            'keywords' => array('hero', 'section', 'welcome', 'cta')
        )
    );
}
add_action('init', 'register_block_patterns');
```

### Custom Pattern Categories

```php
// functions.php - Register pattern categories
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
}
add_action('init', 'register_pattern_categories');
```

## Block Styles

### Custom Block Styles

```php
// functions.php - Register custom block styles
function register_custom_block_styles() {
    // Add custom style to button block
    register_block_style(
        'core/button',
        array(
            'name' => 'outline',
            'label' => 'Outline',
            'style_handle' => 'my-theme-button-outline'
        )
    );
    
    // Add custom style to group block
    register_block_style(
        'core/group',
        array(
            'name' => 'card',
            'label' => 'Card',
            'style_handle' => 'my-theme-group-card'
        )
    );
}
add_action('init', 'register_custom_block_styles');
```

### Block Style CSS

```css
/* style.css - Custom block styles */
.wp-block-button.is-style-outline .wp-block-button__link {
    background-color: transparent;
    border: 2px solid var(--wp--preset--color--primary);
    color: var(--wp--preset--color--primary);
}

.wp-block-button.is-style-outline .wp-block-button__link:hover {
    background-color: var(--wp--preset--color--primary);
    color: var(--wp--preset--color--white);
}

.wp-block-group.is-style-card {
    border: 1px solid var(--wp--preset--color--border);
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 2rem;
}
```

## Template Variations

### Conditional Templates

```html
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
    <!-- wp:post-title {"level":1} /-->
    
    <!-- wp:group {"style":{"spacing":{"blockGap":"1rem"}},"layout":{"type":"flex","flexWrap":"wrap","justifyContent":"space-between"}} -->
    <div class="wp-block-group">
        <!-- wp:post-date /-->
        <!-- wp:post-author {"showAvatar":false} /-->
        <!-- wp:post-terms {"term":"category"} /-->
    </div>
    <!-- /wp:group -->
    
    <!-- wp:post-featured-image {"align":"wide"} /-->
    
    <!-- wp:post-content {"align":"wide"} /-->
    
    <!-- wp:group {"style":{"spacing":{"blockGap":"1rem"}},"layout":{"type":"flex","flexWrap":"wrap"}} -->
    <div class="wp-block-group">
        <!-- wp:post-terms {"term":"post_tag"} /-->
        <!-- wp:post-navigation-link {"type":"previous","label":"Previous Post"} /-->
        <!-- wp:post-navigation-link {"type":"next","label":"Next Post"} /-->
    </div>
    <!-- /wp:group -->
</div>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

## Advanced Block Theme Features

### Custom CSS Classes

```css
/* style.css - Custom CSS for block theme */
/* Hero section styles */
.hero-section {
    background: linear-gradient(135deg, var(--wp--preset--color--primary) 0%, var(--wp--preset--color--secondary) 100%);
    min-height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* Card styles */
.feature-card {
    background: var(--wp--preset--color--white);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

/* Navigation styles */
.main-navigation {
    background: var(--wp--preset--color--white);
    border-bottom: 1px solid var(--wp--preset--color--border);
    position: sticky;
    top: 0;
    z-index: 100;
}

/* Footer styles */
.site-footer {
    background: var(--wp--preset--color--dark);
    color: var(--wp--preset--color--white);
    padding: 3rem 0 1rem;
}
```

### JavaScript Functionality

```javascript
// assets/js/theme.js - Custom JavaScript for block theme
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Lazy loading for images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
});
```

## Best Practices

### Performance Optimization

```php
// functions.php - Performance optimizations
function block_theme_performance() {
    // Remove unnecessary scripts and styles
    remove_action('wp_head', 'wp_generator');
    remove_action('wp_head', 'wlwmanifest_link');
    remove_action('wp_head', 'rsd_link');
    
    // Optimize loading
    add_action('wp_enqueue_scripts', function() {
        // Only load theme styles on frontend
        if (!is_admin()) {
            wp_enqueue_style('block-theme-style', get_stylesheet_uri(), array(), wp_get_theme()->get('Version'));
        }
    });
    
    // Add preload for critical resources
    add_action('wp_head', function() {
        echo '<link rel="preload" href="' . get_stylesheet_uri() . '" as="style">';
    });
}
add_action('after_setup_theme', 'block_theme_performance');
```

### Accessibility

```html
<!-- Accessible template structure -->
<!-- wp:template-part {"slug":"header","tagName":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
    <!-- wp:post-title {"level":1} /-->
    <!-- wp:post-content /-->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","tagName":"footer"} /-->
```

### SEO Optimization

```php
// functions.php - SEO optimizations
function block_theme_seo() {
    // Add structured data
    add_action('wp_head', function() {
        if (is_single()) {
            global $post;
            $schema = array(
                '@context' => 'https://schema.org',
                '@type' => 'Article',
                'headline' => get_the_title(),
                'author' => array(
                    '@type' => 'Person',
                    'name' => get_the_author_meta('display_name')
                ),
                'datePublished' => get_the_date('c'),
                'dateModified' => get_the_modified_date('c')
            );
            
            echo '<script type="application/ld+json">' . json_encode($schema) . '</script>';
        }
    });
}
add_action('after_setup_theme', 'block_theme_seo');
```

## Official Documentation

https://developer.wordpress.org/themes/block-themes/
https://developer.wordpress.org/themes/advanced-topics/theme-json/
https://developer.wordpress.org/themes/block-themes/block-theme-examples/
