# Custom Post Type Templates

```php
// Single template for CPT
// Create: single-{post-type}.php
// Example: single-portfolio.php

<?php get_header(); ?>

<main>
    <?php
    while ( have_posts() ) : the_post();
        ?>
        <article <?php post_class(); ?>>
            <h1><?php the_title(); ?></h1>
            
            <?php if ( has_post_thumbnail() ) : ?>
                <div class="featured-image">
                    <?php the_post_thumbnail( 'large' ); ?>
                </div>
            <?php endif; ?>
            
            <div class="content">
                <?php the_content(); ?>
            </div>
            
            <?php
            // Display custom meta
            $client = get_post_meta( get_the_ID(), '_client_name', true );
            if ( $client ) :
                ?>
                <div class="meta">
                    <strong>Client:</strong> <?php echo esc_html( $client ); ?>
                </div>
            <?php endif; ?>
        </article>
        <?php
    endwhile;
    ?>
</main>

<?php get_footer(); ?>

// Archive template for CPT
// Create: archive-{post-type}.php
// Example: archive-portfolio.php

<?php get_header(); ?>

<main>
    <h1><?php post_type_archive_title(); ?></h1>
    
    <?php if ( have_posts() ) : ?>
        <div class="portfolio-grid">
            <?php
            while ( have_posts() ) : the_post();
                ?>
                <article>
                    <a href="<?php the_permalink(); ?>">
                        <?php the_post_thumbnail( 'medium' ); ?>
                        <h2><?php the_title(); ?></h2>
                    </a>
                </article>
                <?php
            endwhile;
            ?>
        </div>
        
        <?php the_posts_pagination(); ?>
    <?php endif; ?>
</main>

<?php get_footer(); ?>
```
