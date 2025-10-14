# WordPress Template Tags

Template tags are PHP functions that retrieve and display data in WordPress themes.

## Loop Functions

### The Loop Basics

```php
<?php if ( have_posts() ) : ?>
    <?php while ( have_posts() ) : the_post(); ?>
        <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
            <header class="entry-header">
                <h1 class="entry-title">
                    <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                </h1>
                
                <div class="entry-meta">
                    <span class="posted-on">
                        <a href="<?php the_permalink(); ?>" rel="bookmark">
                            <time class="entry-date published" datetime="<?php echo esc_attr( get_the_date( 'c' ) ); ?>">
                                <?php the_date(); ?>
                            </time>
                        </a>
                    </span>
                    
                    <span class="byline">
                        <span class="author vcard">
                            <a class="url fn n" href="<?php echo esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ); ?>">
                                <?php the_author(); ?>
                            </a>
                        </span>
                    </span>
                </div>
            </header>
            
            <div class="entry-content">
                <?php the_content(); ?>
            </div>
            
            <footer class="entry-footer">
                <?php the_tags( '<span class="tags-links">', ', ', '</span>' ); ?>
            </footer>
        </article>
    <?php endwhile; ?>
<?php else : ?>
    <p><?php _e( 'Sorry, no posts matched your criteria.' ); ?></p>
<?php endif; ?>
```

### Custom Query Loop

```php
<?php
// Custom query
$custom_query = new WP_Query( array(
    'post_type' => 'product',
    'posts_per_page' => 6,
    'meta_key' => 'featured',
    'meta_value' => '1'
) );

if ( $custom_query->have_posts() ) :
    while ( $custom_query->have_posts() ) : $custom_query->the_post();
        ?>
        <div class="product-item">
            <h3><?php the_title(); ?></h3>
            <div class="product-content">
                <?php the_excerpt(); ?>
            </div>
            <div class="product-meta">
                <?php
                $price = get_post_meta( get_the_ID(), 'price', true );
                if ( $price ) {
                    echo '<span class="price">$' . esc_html( $price ) . '</span>';
                }
                ?>
            </div>
        </div>
        <?php
    endwhile;
    wp_reset_postdata();
else :
    echo '<p>No featured products found.</p>';
endif;
?>
```

## Post Data Functions

### Title Functions

```php
// Basic title functions
the_title();                    // Display title
the_title_attribute();          // Display title for attributes (escaped)
get_the_title();               // Return title
get_the_title( $post_id );     // Get title of specific post

// Title with link
the_title( '<h1 class="entry-title"><a href="' . get_permalink() . '">', '</a></h1>' );

// Conditional title display
if ( get_the_title() ) {
    the_title( '<h1 class="entry-title">', '</h1>' );
} else {
    echo '<h1 class="entry-title">' . __( '(no title)' ) . '</h1>';
}
```

### Content Functions

```php
// Content display
the_content();                 // Display full content
the_excerpt();                 // Display excerpt
get_the_content();             // Return content
get_the_excerpt();             // Return excerpt

// Content with custom formatting
the_content( sprintf(
    wp_kses(
        __( 'Continue reading<span class="screen-reader-text"> "%s"</span>', 'textdomain' ),
        array(
            'span' => array(
                'class' => array(),
            ),
        )
    ),
    get_the_title()
) );

// Custom excerpt length
function custom_excerpt_length( $length ) {
    return 20;
}
add_filter( 'excerpt_length', 'custom_excerpt_length' );

// Custom excerpt more
function custom_excerpt_more( $more ) {
    return '...';
}
add_filter( 'excerpt_more', 'custom_excerpt_more' );
```

### Date and Time Functions

```php
// Date functions
the_date();                    // Display date
the_time();                    // Display time
the_date( 'F j, Y' );          // Custom date format
the_time( 'g:i a' );           // Custom time format

// Get date/time data
get_the_date();                // Return date
get_the_date( 'Y-m-d' );       // Return formatted date
get_the_time();                // Return time
get_the_time( 'H:i:s' );       // Return formatted time

// Date with link
printf(
    '<span class="posted-on">%1$s <a href="%2$s" rel="bookmark">%3$s</a></span>',
    __( 'Posted on', 'textdomain' ),
    get_permalink(),
    get_the_date()
);

// Modified date
if ( get_the_time( 'U' ) !== get_the_modified_time( 'U' ) ) {
    printf(
        '<span class="updated">%1$s <time class="updated" datetime="%2$s">%3$s</time></span>',
        __( 'Updated on', 'textdomain' ),
        get_the_modified_date( 'c' ),
        get_the_modified_date()
    );
}
```

### Author Functions

```php
// Author display
the_author();                  // Display author name
the_author_posts_link();       // Display author with link to posts
get_the_author();              // Return author name
get_the_author_meta( 'display_name' );  // Get specific author meta

// Author with link
printf(
    '<span class="byline">%1$s <span class="author vcard"><a class="url fn n" href="%2$s">%3$s</a></span></span>',
    __( 'by', 'textdomain' ),
    esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ),
    get_the_author()
);

// Author bio
if ( get_the_author_meta( 'description' ) ) {
    ?>
    <div class="author-info">
        <div class="author-avatar">
            <?php echo get_avatar( get_the_author_meta( 'ID' ), 96 ); ?>
        </div>
        <div class="author-description">
            <h2 class="author-title"><?php printf( __( 'About %s', 'textdomain' ), get_the_author() ); ?></h2>
            <p class="author-bio">
                <?php the_author_meta( 'description' ); ?>
                <a class="author-link" href="<?php echo esc_url( get_author_posts_url( get_the_author_meta( 'ID' ) ) ); ?>" rel="author">
                    <?php printf( __( 'View all posts by %s', 'textdomain' ), get_the_author() ); ?>
                </a>
            </p>
        </div>
    </div>
    <?php
}
```

### Navigation Functions

```php
// Post navigation
the_post_navigation( array(
    'prev_text' => __( '<span class="nav-subtitle">Previous:</span> <span class="nav-title">%title</span>', 'textdomain' ),
    'next_text' => __( '<span class="nav-subtitle">Next:</span> <span class="nav-title">%title</span>', 'textdomain' ),
) );

// Posts pagination
the_posts_pagination( array(
    'mid_size'  => 2,
    'prev_text' => __( 'Previous', 'textdomain' ),
    'next_text' => __( 'Next', 'textdomain' ),
) );

// Comments pagination
the_comments_pagination( array(
    'prev_text' => __( 'Older comments', 'textdomain' ),
    'next_text' => __( 'Newer comments', 'textdomain' ),
) );
```

## Taxonomy Functions

### Categories

```php
// Display categories
the_category();                // Display categories as links
the_category( ', ' );          // Display with separator
get_the_category();            // Return category objects

// Category with custom formatting
$categories = get_the_category();
if ( $categories ) {
    echo '<div class="cat-links">';
    foreach ( $categories as $category ) {
        printf(
            '<a href="%1$s" class="cat-link cat-%2$s">%3$s</a>',
            esc_url( get_category_link( $category->term_id ) ),
            esc_attr( $category->slug ),
            esc_html( $category->name )
        );
    }
    echo '</div>';
}

// Primary category (if using Yoast SEO)
$primary_category = get_post_meta( get_the_ID(), '_yoast_wpseo_primary_category', true );
if ( $primary_category ) {
    $category = get_category( $primary_category );
    if ( $category ) {
        printf(
            '<a href="%1$s" class="primary-category">%2$s</a>',
            esc_url( get_category_link( $category->term_id ) ),
            esc_html( $category->name )
        );
    }
}
```

### Tags

```php
// Display tags
the_tags();                    // Display tags as links
the_tags( 'Tags: ', ', ', '' ); // Display with prefix and separator
get_the_tags();                // Return tag objects

// Tags with custom formatting
$tags = get_the_tags();
if ( $tags ) {
    echo '<div class="tags-links">';
    foreach ( $tags as $tag ) {
        printf(
            '<a href="%1$s" class="tag-link tag-%2$s">%3$s</a>',
            esc_url( get_tag_link( $tag->term_id ) ),
            esc_attr( $tag->slug ),
            esc_html( $tag->name )
        );
    }
    echo '</div>';
}
```

### Custom Taxonomies

```php
// Custom taxonomy terms
$terms = get_the_terms( get_the_ID(), 'product_category' );
if ( $terms && ! is_wp_error( $terms ) ) {
    echo '<div class="product-categories">';
    foreach ( $terms as $term ) {
        printf(
            '<a href="%1$s" class="product-category">%2$s</a>',
            esc_url( get_term_link( $term ) ),
            esc_html( $term->name )
        );
    }
    echo '</div>';
}

// Get term by slug
$term = get_term_by( 'slug', 'featured-products', 'product_category' );
if ( $term ) {
    echo '<h2>' . esc_html( $term->name ) . '</h2>';
    echo '<p>' . esc_html( $term->description ) . '</p>';
}
```

## Media Functions

### Featured Images

```php
// Featured image
if ( has_post_thumbnail() ) {
    the_post_thumbnail();              // Display featured image
    the_post_thumbnail( 'large' );     // Display specific size
    the_post_thumbnail( array( 300, 200 ) ); // Display custom size
}

// Featured image with link
if ( has_post_thumbnail() ) {
    ?>
    <div class="post-thumbnail">
        <a href="<?php the_permalink(); ?>">
            <?php the_post_thumbnail( 'medium' ); ?>
        </a>
    </div>
    <?php
}

// Get featured image data
$thumbnail_id = get_post_thumbnail_id();
if ( $thumbnail_id ) {
    $thumbnail_url = wp_get_attachment_image_url( $thumbnail_id, 'large' );
    $thumbnail_alt = get_post_meta( $thumbnail_id, '_wp_attachment_image_alt', true );
    
    printf(
        '<img src="%1$s" alt="%2$s" class="featured-image" />',
        esc_url( $thumbnail_url ),
        esc_attr( $thumbnail_alt )
    );
}
```

### Image Galleries

```php
// Display gallery
$gallery_images = get_post_meta( get_the_ID(), '_gallery_images', true );
if ( $gallery_images ) {
    echo '<div class="post-gallery">';
    foreach ( $gallery_images as $image_id ) {
        $image_url = wp_get_attachment_image_url( $image_id, 'medium' );
        $image_alt = get_post_meta( $image_id, '_wp_attachment_image_alt', true );
        
        printf(
            '<img src="%1$s" alt="%2$s" class="gallery-image" />',
            esc_url( $image_url ),
            esc_attr( $image_alt )
        );
    }
    echo '</div>';
}

// Gallery shortcode
$gallery_shortcode = get_post_meta( get_the_ID(), '_gallery_shortcode', true );
if ( $gallery_shortcode ) {
    echo do_shortcode( $gallery_shortcode );
}
```

## Conditional Tags

```php
// Page type conditions
if ( is_home() ) {
    // Blog posts page
} elseif ( is_front_page() ) {
    // Front page
} elseif ( is_single() ) {
    // Single post
} elseif ( is_page() ) {
    // Single page
} elseif ( is_archive() ) {
    // Archive page
} elseif ( is_search() ) {
    // Search results
} elseif ( is_404() ) {
    // 404 page
}

// Post type conditions
if ( is_singular( 'product' ) ) {
    // Single product page
} elseif ( is_post_type_archive( 'product' ) ) {
    // Product archive
}

// Taxonomy conditions
if ( is_category() ) {
    // Category archive
} elseif ( is_tag() ) {
    // Tag archive
} elseif ( is_tax( 'product_category' ) ) {
    // Custom taxonomy archive
}

// Author conditions
if ( is_author() ) {
    // Author archive
    $author = get_queried_object();
    echo '<h1>Posts by ' . esc_html( $author->display_name ) . '</h1>';
}
```

## Utility Functions

### Permalink Functions

```php
// Permalink functions
the_permalink();               // Display permalink
get_permalink();               // Return permalink
get_permalink( $post_id );     // Get permalink of specific post

// Permalink with title
printf(
    '<h2><a href="%1$s" rel="bookmark">%2$s</a></h2>',
    esc_url( get_permalink() ),
    get_the_title()
);

// External links
$external_url = get_post_meta( get_the_ID(), 'external_url', true );
if ( $external_url ) {
    printf(
        '<a href="%1$s" target="_blank" rel="noopener">%2$s</a>',
        esc_url( $external_url ),
        __( 'Read more', 'textdomain' )
    );
}
```

### Post Class Functions

```php
// Post classes
post_class();                  // Display post classes
post_class( 'custom-class' );  // Add custom classes
get_post_class();              // Return post classes

// Custom post classes
function add_custom_post_class( $classes, $class, $post_id ) {
    if ( is_single() ) {
        $classes[] = 'single-post';
    }
    
    // Add class based on post meta
    $featured = get_post_meta( $post_id, 'featured', true );
    if ( $featured ) {
        $classes[] = 'featured-post';
    }
    
    return $classes;
}
add_filter( 'post_class', 'add_custom_post_class', 10, 3 );
```

### Comment Functions

```php
// Comments template
comments_template();

// Comment count
$comment_count = get_comments_number();
if ( $comment_count > 0 ) {
    printf(
        _n(
            '%s comment',
            '%s comments',
            $comment_count,
            'textdomain'
        ),
        number_format_i18n( $comment_count )
    );
}

// Comments are open
if ( comments_open() || get_comments_number() ) {
    comments_template();
}
```

## Best Practices

### Security

```php
// Always escape output
the_title();                   // Already escaped
echo esc_html( get_the_title() ); // Manual escaping
echo esc_attr( get_the_title() );  // For attributes

// Escape URLs
printf(
    '<a href="%s">%s</a>',
    esc_url( get_permalink() ),
    esc_html( get_the_title() )
);

// Escape with context
printf(
    '<h1 class="entry-title"><a href="%1$s" rel="bookmark">%2$s</a></h1>',
    esc_url( get_permalink() ),
    get_the_title() // the_title() is already escaped
);
```

### Performance

```php
// Use specific functions instead of get_post()
$title = get_the_title();      // Faster
$content = get_the_content();  // Faster

// Cache expensive operations
function get_cached_post_meta( $post_id, $meta_key ) {
    static $cache = array();
    $cache_key = $post_id . '_' . $meta_key;
    
    if ( ! isset( $cache[ $cache_key ] ) ) {
        $cache[ $cache_key ] = get_post_meta( $post_id, $meta_key, true );
    }
    
    return $cache[ $cache_key ];
}
```

### Accessibility

```php
// Add proper ARIA labels
printf(
    '<article id="post-%1$s" %2$s aria-label="%3$s">',
    get_the_ID(),
    post_class(),
    esc_attr( get_the_title() )
);

// Screen reader text
printf(
    '<span class="screen-reader-text">%1$s</span>',
    __( 'Posted on', 'textdomain' )
);

// Semantic HTML
echo '<time datetime="' . esc_attr( get_the_date( 'c' ) ) . '">';
the_date();
echo '</time>';
```

## Official Documentation

https://developer.wordpress.org/themes/basics/template-tags/
https://developer.wordpress.org/reference/functions/the_title/
https://developer.wordpress.org/reference/functions/the_content/
https://developer.wordpress.org/reference/functions/the_excerpt/
