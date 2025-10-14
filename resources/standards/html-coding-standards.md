# WordPress HTML Coding Standards

Comprehensive HTML coding standards and best practices for WordPress development.

## Basic HTML Standards

### Document Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="profile" href="https://gmpg.org/xfn/11">
    <link rel="pingback" href="<?php bloginfo('pingback_url'); ?>">
    
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
    <?php wp_body_open(); ?>
    
    <div id="page" class="site">
        <a class="skip-link screen-reader-text" href="#primary">
            <?php esc_html_e('Skip to content', 'textdomain'); ?>
        </a>
        
        <header id="masthead" class="site-header">
            <!-- Header content -->
        </header>
        
        <main id="primary" class="site-main">
            <!-- Main content -->
        </main>
        
        <footer id="colophon" class="site-footer">
            <!-- Footer content -->
        </footer>
    </div>
    
    <?php wp_footer(); ?>
</body>
</html>
```

### Semantic HTML Elements

```html
<!-- Use semantic HTML5 elements -->
<article class="post">
    <header class="entry-header">
        <h1 class="entry-title">
            <a href="<?php the_permalink(); ?>" rel="bookmark">
                <?php the_title(); ?>
            </a>
        </h1>
        
        <div class="entry-meta">
            <span class="posted-on">
                <time class="entry-date published" datetime="<?php echo esc_attr(get_the_date('c')); ?>">
                    <?php echo esc_html(get_the_date()); ?>
                </time>
            </span>
            
            <span class="byline">
                <?php esc_html_e('by', 'textdomain'); ?>
                <span class="author vcard">
                    <a class="url fn n" href="<?php echo esc_url(get_author_posts_url(get_the_author_meta('ID'))); ?>">
                        <?php echo esc_html(get_the_author()); ?>
                    </a>
                </span>
            </span>
        </div>
    </header>
    
    <?php if (has_post_thumbnail()) : ?>
        <div class="post-thumbnail">
            <?php the_post_thumbnail(); ?>
        </div>
    <?php endif; ?>
    
    <div class="entry-content">
        <?php
        the_content(sprintf(
            wp_kses(
                __('Continue reading<span class="screen-reader-text"> "%s"</span>', 'textdomain'),
                array(
                    'span' => array(
                        'class' => array(),
                    ),
                )
            ),
            get_the_title()
        ));
        
        wp_link_pages(array(
            'before' => '<div class="page-links">' . esc_html__('Pages:', 'textdomain'),
            'after'  => '</div>',
        ));
        ?>
    </div>
    
    <footer class="entry-footer">
        <?php if (has_tag()) : ?>
            <div class="tags-links">
                <?php esc_html_e('Tagged', 'textdomain'); ?>: <?php the_tags('', ', ', ''); ?>
            </div>
        <?php endif; ?>
    </footer>
</article>
```

### Form Elements

```html
<!-- Properly structured forms -->
<form method="post" action="<?php echo esc_url(admin_url('admin-post.php')); ?>" class="contact-form">
    <?php wp_nonce_field('contact_form_action', 'contact_form_nonce'); ?>
    
    <div class="form-group">
        <label for="contact-name" class="form-label">
            <?php esc_html_e('Name', 'textdomain'); ?>
            <span class="required" aria-label="<?php esc_attr_e('Required field', 'textdomain'); ?>">*</span>
        </label>
        <input 
            type="text" 
            id="contact-name" 
            name="contact_name" 
            class="form-input" 
            required 
            aria-describedby="contact-name-error"
            value="<?php echo esc_attr(wp_unslash($_POST['contact_name'] ?? '')); ?>"
        >
        <div id="contact-name-error" class="form-error" role="alert" aria-live="polite"></div>
    </div>
    
    <div class="form-group">
        <label for="contact-email" class="form-label">
            <?php esc_html_e('Email', 'textdomain'); ?>
            <span class="required" aria-label="<?php esc_attr_e('Required field', 'textdomain'); ?>">*</span>
        </label>
        <input 
            type="email" 
            id="contact-email" 
            name="contact_email" 
            class="form-input" 
            required 
            aria-describedby="contact-email-error"
            value="<?php echo esc_attr(wp_unslash($_POST['contact_email'] ?? '')); ?>"
        >
        <div id="contact-email-error" class="form-error" role="alert" aria-live="polite"></div>
    </div>
    
    <div class="form-group">
        <label for="contact-message" class="form-label">
            <?php esc_html_e('Message', 'textdomain'); ?>
            <span class="required" aria-label="<?php esc_attr_e('Required field', 'textdomain'); ?>">*</span>
        </label>
        <textarea 
            id="contact-message" 
            name="contact_message" 
            class="form-textarea" 
            rows="5" 
            required 
            aria-describedby="contact-message-error"
        ><?php echo esc_textarea(wp_unslash($_POST['contact_message'] ?? '')); ?></textarea>
        <div id="contact-message-error" class="form-error" role="alert" aria-live="polite"></div>
    </div>
    
    <div class="form-actions">
        <button type="submit" class="button button-primary">
            <?php esc_html_e('Send Message', 'textdomain'); ?>
        </button>
    </div>
</form>
```

## Accessibility Standards

### ARIA Labels and Roles

```html
<!-- Navigation with proper ARIA -->
<nav role="navigation" aria-label="<?php esc_attr_e('Primary navigation', 'textdomain'); ?>">
    <ul class="main-menu">
        <li class="menu-item">
            <a href="<?php echo esc_url(home_url('/')); ?>" aria-current="<?php echo is_front_page() ? 'page' : 'false'; ?>">
                <?php esc_html_e('Home', 'textdomain'); ?>
            </a>
        </li>
        <li class="menu-item menu-item-has-children">
            <a href="<?php echo esc_url(get_permalink(get_option('page_for_posts'))); ?>" aria-expanded="false" aria-haspopup="true">
                <?php esc_html_e('Blog', 'textdomain'); ?>
                <span class="dropdown-toggle" aria-hidden="true"></span>
            </a>
            <ul class="sub-menu" role="menu">
                <li class="menu-item" role="none">
                    <a href="#" role="menuitem"><?php esc_html_e('Category 1', 'textdomain'); ?></a>
                </li>
                <li class="menu-item" role="none">
                    <a href="#" role="menuitem"><?php esc_html_e('Category 2', 'textdomain'); ?></a>
                </li>
            </ul>
        </li>
    </ul>
</nav>

<!-- Search form with ARIA -->
<form role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>" class="search-form">
    <label for="search-field" class="screen-reader-text">
        <?php esc_html_e('Search for:', 'textdomain'); ?>
    </label>
    <input 
        type="search" 
        id="search-field" 
        class="search-field" 
        placeholder="<?php esc_attr_e('Search...', 'textdomain'); ?>" 
        value="<?php echo get_search_query(); ?>" 
        name="s"
        aria-describedby="search-help"
    >
    <button type="submit" class="search-submit" aria-label="<?php esc_attr_e('Search', 'textdomain'); ?>">
        <span class="screen-reader-text"><?php esc_html_e('Search', 'textdomain'); ?></span>
        <svg aria-hidden="true" focusable="false" width="16" height="16" viewBox="0 0 24 24">
            <!-- Search icon SVG -->
        </svg>
    </button>
    <div id="search-help" class="screen-reader-text">
        <?php esc_html_e('Press Enter to search or ESC to close', 'textdomain'); ?>
    </div>
</form>
```

### Skip Links and Focus Management

```html
<!-- Skip links for keyboard navigation -->
<a class="skip-link screen-reader-text" href="#primary">
    <?php esc_html_e('Skip to content', 'textdomain'); ?>
</a>

<a class="skip-link screen-reader-text" href="#secondary">
    <?php esc_html_e('Skip to sidebar', 'textdomain'); ?>
</a>

<!-- Focus management for modals -->
<div id="modal" class="modal" role="dialog" aria-labelledby="modal-title" aria-hidden="true">
    <div class="modal-content">
        <button class="modal-close" aria-label="<?php esc_attr_e('Close modal', 'textdomain'); ?>">
            <span aria-hidden="true">&times;</span>
        </button>
        
        <h2 id="modal-title" class="modal-title">
            <?php esc_html_e('Modal Title', 'textdomain'); ?>
        </h2>
        
        <div class="modal-body">
            <!-- Modal content -->
        </div>
        
        <div class="modal-footer">
            <button type="button" class="button button-secondary modal-cancel">
                <?php esc_html_e('Cancel', 'textdomain'); ?>
            </button>
            <button type="button" class="button button-primary modal-confirm">
                <?php esc_html_e('Confirm', 'textdomain'); ?>
            </button>
        </div>
    </div>
</div>
```

## WordPress-Specific HTML

### Template Hierarchy Structure

```html
<!-- index.php - Main template -->
<?php get_header(); ?>

<main id="primary" class="site-main">
    <?php if (have_posts()) : ?>
        <header class="page-header">
            <?php if (is_home() && !is_front_page()) : ?>
                <h1 class="page-title"><?php single_post_title(); ?></h1>
            <?php endif; ?>
        </header>
        
        <div class="posts-container">
            <?php while (have_posts()) : the_post(); ?>
                <?php get_template_part('template-parts/content', get_post_type()); ?>
            <?php endwhile; ?>
        </div>
        
        <?php
        the_posts_navigation(array(
            'prev_text' => esc_html__('Older posts', 'textdomain'),
            'next_text' => esc_html__('Newer posts', 'textdomain'),
        ));
        ?>
    <?php else : ?>
        <section class="no-results not-found">
            <header class="page-header">
                <h1 class="page-title"><?php esc_html_e('Nothing here', 'textdomain'); ?></h1>
            </header>
            
            <div class="page-content">
                <?php if (is_home() && current_user_can('publish_posts')) : ?>
                    <p><?php
                    printf(
                        wp_kses(
                            __('Ready to publish your first post? <a href="%1$s">Get started here</a>.', 'textdomain'),
                            array(
                                'a' => array(
                                    'href' => array(),
                                ),
                            )
                        ),
                        esc_url(admin_url('post-new.php'))
                    );
                    ?></p>
                <?php elseif (is_search()) : ?>
                    <p><?php esc_html_e('Sorry, but nothing matched your search terms. Please try again with some different keywords.', 'textdomain'); ?></p>
                    <?php get_search_form(); ?>
                <?php else : ?>
                    <p><?php esc_html_e('It seems we can\'t find what you\'re looking for. Perhaps searching can help.', 'textdomain'); ?></p>
                    <?php get_search_form(); ?>
                <?php endif; ?>
            </div>
        </section>
    <?php endif; ?>
</main>

<?php get_sidebar(); ?>
<?php get_footer(); ?>
```

### Content Template Parts

```html
<!-- template-parts/content.php -->
<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <header class="entry-header">
        <?php
        if (is_singular()) :
            the_title('<h1 class="entry-title">', '</h1>');
        else :
            the_title('<h2 class="entry-title"><a href="' . esc_url(get_permalink()) . '" rel="bookmark">', '</a></h2>');
        endif;
        
        if ('post' === get_post_type()) :
            ?>
            <div class="entry-meta">
                <?php
                theme_name_posted_on();
                theme_name_posted_by();
                ?>
            </div>
            <?php
        endif;
        ?>
    </header>
    
    <?php theme_name_post_thumbnail(); ?>
    
    <div class="entry-content">
        <?php
        the_content(sprintf(
            wp_kses(
                __('Continue reading<span class="screen-reader-text"> "%s"</span>', 'textdomain'),
                array(
                    'span' => array(
                        'class' => array(),
                    ),
                )
            ),
            get_the_title()
        ));
        
        wp_link_pages(array(
            'before' => '<div class="page-links">' . esc_html__('Pages:', 'textdomain'),
            'after'  => '</div>',
        ));
        ?>
    </div>
    
    <footer class="entry-footer">
        <?php theme_name_entry_footer(); ?>
    </footer>
</article>
```

### Block Editor HTML Structure

```html
<!-- Block theme template structure -->
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

## Security Best Practices

### Data Sanitization and Escaping

```html
<!-- Proper data sanitization in HTML output -->
<?php
// Always escape output
$user_input = sanitize_text_field($_POST['user_input'] ?? '');
$user_url = esc_url_raw($_POST['user_url'] ?? '');
$user_email = sanitize_email($_POST['user_email'] ?? '');
?>

<!-- Escaped output examples -->
<h1><?php echo esc_html(get_the_title()); ?></h1>

<a href="<?php echo esc_url(get_permalink()); ?>">
    <?php echo esc_html(get_the_title()); ?>
</a>

<img src="<?php echo esc_url(get_the_post_thumbnail_url()); ?>" 
     alt="<?php echo esc_attr(get_post_meta(get_post_thumbnail_id(), '_wp_attachment_image_alt', true)); ?>">

<div class="content">
    <?php echo wp_kses_post(get_the_content()); ?>
</div>

<!-- Form field values -->
<input type="text" name="username" value="<?php echo esc_attr($username); ?>">
<textarea name="description"><?php echo esc_textarea($description); ?></textarea>

<!-- URLs and links -->
<a href="<?php echo esc_url($external_url); ?>" target="_blank" rel="noopener noreferrer">
    <?php echo esc_html($link_text); ?>
</a>
```

### Nonce Implementation

```html
<!-- Security nonces in forms -->
<form method="post" action="">
    <?php wp_nonce_field('my_action', 'my_nonce'); ?>
    
    <input type="hidden" name="action" value="my_action">
    <input type="text" name="data" value="">
    
    <button type="submit">Submit</button>
</form>

<!-- AJAX nonces -->
<script>
var ajaxData = {
    action: 'my_ajax_action',
    nonce: '<?php echo wp_create_nonce('my_ajax_action'); ?>',
    data: 'some_data'
};

jQuery.post(ajaxurl, ajaxData, function(response) {
    // Handle response
});
</script>
```

## Performance Optimization

### Lazy Loading and Resource Optimization

```html
<!-- Lazy loading images -->
<img src="placeholder.jpg" 
     data-src="<?php echo esc_url(get_the_post_thumbnail_url()); ?>" 
     alt="<?php echo esc_attr(get_the_title()); ?>"
     class="lazy-load"
     loading="lazy">

<!-- Preload critical resources -->
<link rel="preload" href="<?php echo get_template_directory_uri(); ?>/assets/css/critical.css" as="style">
<link rel="preload" href="<?php echo get_template_directory_uri(); ?>/assets/fonts/font.woff2" as="font" type="font/woff2" crossorigin>

<!-- Defer non-critical JavaScript -->
<script src="<?php echo get_template_directory_uri(); ?>/assets/js/main.js" defer></script>

<!-- Conditional loading -->
<?php if (is_page_template('contact.php')) : ?>
    <script src="<?php echo get_template_directory_uri(); ?>/assets/js/contact-form.js" defer></script>
<?php endif; ?>
```

### Structured Data

```html
<!-- JSON-LD structured data -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "<?php echo esc_js(get_the_title()); ?>",
    "author": {
        "@type": "Person",
        "name": "<?php echo esc_js(get_the_author()); ?>"
    },
    "datePublished": "<?php echo esc_js(get_the_date('c')); ?>",
    "dateModified": "<?php echo esc_js(get_the_modified_date('c')); ?>",
    "publisher": {
        "@type": "Organization",
        "name": "<?php echo esc_js(get_bloginfo('name')); ?>",
        "logo": {
            "@type": "ImageObject",
            "url": "<?php echo esc_js(get_theme_mod('logo_url')); ?>"
        }
    }
}
</script>

<!-- Microdata for articles -->
<article itemscope itemtype="https://schema.org/Article">
    <h1 itemprop="headline"><?php echo esc_html(get_the_title()); ?></h1>
    
    <div itemprop="author" itemscope itemtype="https://schema.org/Person">
        <span itemprop="name"><?php echo esc_html(get_the_author()); ?></span>
    </div>
    
    <time itemprop="datePublished" datetime="<?php echo esc_attr(get_the_date('c')); ?>">
        <?php echo esc_html(get_the_date()); ?>
    </time>
    
    <div itemprop="articleBody">
        <?php the_content(); ?>
    </div>
</article>
```

## Validation and Testing

### HTML Validation

```html
<!-- Valid HTML5 structure -->
<!DOCTYPE html>
<html lang="<?php language_attributes(); ?>">
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    <!-- Preconnect to external domains -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
    <?php wp_body_open(); ?>
    
    <!-- Main content with proper landmarks -->
    <div id="page" class="site">
        <header id="masthead" class="site-header" role="banner">
            <!-- Header content -->
        </header>
        
        <main id="primary" class="site-main" role="main">
            <!-- Main content -->
        </main>
        
        <aside id="secondary" class="widget-area" role="complementary">
            <!-- Sidebar content -->
        </aside>
        
        <footer id="colophon" class="site-footer" role="contentinfo">
            <!-- Footer content -->
        </footer>
    </div>
    
    <?php wp_footer(); ?>
</body>
</html>
```

### Screen Reader Support

```html
<!-- Screen reader only text -->
<span class="screen-reader-text">
    <?php esc_html_e('This content is only visible to screen readers', 'textdomain'); ?>
</span>

<!-- Visually hidden but accessible -->
.visually-hidden {
    position: absolute !important;
    clip: rect(1px, 1px, 1px, 1px);
    width: 1px;
    height: 1px;
    overflow: hidden;
}

<!-- Skip links for keyboard navigation -->
<a href="#main-content" class="skip-link screen-reader-text">
    <?php esc_html_e('Skip to main content', 'textdomain'); ?>
</a>

<!-- ARIA live regions for dynamic content -->
<div id="status-messages" aria-live="polite" aria-atomic="true" class="screen-reader-text">
    <!-- Status messages will be inserted here -->
</div>
```

## Best Practices Summary

### Structure and Semantics
- Use semantic HTML5 elements
- Implement proper heading hierarchy (h1-h6)
- Use landmarks (main, nav, aside, footer)
- Include skip links for keyboard navigation
- Add ARIA labels and roles where needed

### Accessibility
- Provide alt text for all images
- Use descriptive link text
- Implement focus management
- Support screen readers
- Ensure keyboard navigation
- Maintain color contrast ratios

### Security
- Escape all output data
- Sanitize all input data
- Use nonces for forms
- Validate file uploads
- Prevent XSS attacks

### Performance
- Use lazy loading for images
- Minimize HTTP requests
- Compress and optimize assets
- Implement critical CSS
- Use proper caching headers

### SEO
- Use structured data markup
- Implement proper meta tags
- Create semantic URLs
- Optimize page titles
- Include meta descriptions

## Official Documentation

https://developer.wordpress.org/coding-standards/wordpress-coding-standards/html/
https://developer.wordpress.org/themes/basics/template-files/
https://developer.wordpress.org/themes/advanced-topics/accessibility/
