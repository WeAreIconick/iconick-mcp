---
difficulty: Beginner
tags: [blocks, patterns, templates, layouts]
related: [blocks/register-block]
use_case: Creating reusable block patterns
---

# Block Patterns

```php
// Register block pattern
function register_my_patterns() {
    register_block_pattern(
        'myplugin/hero-section',
        array(
            'title' => __( 'Hero Section', 'textdomain' ),
            'description' => _x( 'A hero section with heading and button', 'Block pattern description', 'textdomain' ),
            'content' => '<!-- wp:group {"align":"full","backgroundColor":"primary"} -->
            <div class="wp-block-group alignfull has-primary-background-color">
                <!-- wp:heading {"level":1} -->
                <h1>Welcome to Our Site</h1>
                <!-- /wp:heading -->
                
                <!-- wp:buttons -->
                <div class="wp-block-buttons">
                    <!-- wp:button -->
                    <div class="wp-block-button"><a class="wp-block-button__link">Learn More</a></div>
                    <!-- /wp:button -->
                </div>
                <!-- /wp:buttons -->
            </div>
            <!-- /wp:group -->',
            'categories' => array( 'featured' ),
            'keywords' => array( 'hero', 'banner', 'header' )
        )
    );
}
add_action( 'init', 'register_my_patterns' );

// Register pattern category
function register_pattern_categories() {
    register_block_pattern_category(
        'my-patterns',
        array( 'label' => __( 'My Patterns', 'textdomain' ) )
    );
}
add_action( 'init', 'register_pattern_categories' );
```
