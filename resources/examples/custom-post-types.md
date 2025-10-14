# WordPress Custom Post Types - Complete Examples

## Basic Custom Post Type

```php
function register_book_post_type() {
    $labels = array(
        'name'                  => _x( 'Books', 'Post type general name', 'textdomain' ),
        'singular_name'         => _x( 'Book', 'Post type singular name', 'textdomain' ),
        'menu_name'             => _x( 'Books', 'Admin Menu text', 'textdomain' ),
        'name_admin_bar'        => _x( 'Book', 'Add New on Toolbar', 'textdomain' ),
        'add_new'               => __( 'Add New', 'textdomain' ),
        'add_new_item'          => __( 'Add New Book', 'textdomain' ),
        'new_item'              => __( 'New Book', 'textdomain' ),
        'edit_item'             => __( 'Edit Book', 'textdomain' ),
        'view_item'             => __( 'View Book', 'textdomain' ),
        'all_items'             => __( 'All Books', 'textdomain' ),
        'search_items'          => __( 'Search Books', 'textdomain' ),
        'not_found'             => __( 'No books found.', 'textdomain' ),
        'not_found_in_trash'    => __( 'No books found in Trash.', 'textdomain' ),
    );

    $args = array(
        'labels'             => $labels,
        'public'             => true,
        'publicly_queryable' => true,
        'show_ui'            => true,
        'show_in_menu'       => true,
        'query_var'          => true,
        'rewrite'            => array( 'slug' => 'books' ),
        'capability_type'    => 'post',
        'has_archive'        => true,
        'hierarchical'       => false,
        'menu_position'      => 20,
        'menu_icon'          => 'dashicons-book',
        'supports'           => array( 'title', 'editor', 'author', 'thumbnail', 'excerpt' ),
        'show_in_rest'       => true, // Enable Gutenberg
    );

    register_post_type( 'book', $args );
}
add_action( 'init', 'register_book_post_type' );
```

## Advanced CPT with Custom Capabilities

```php
function register_product_post_type() {
    $labels = array(
        'name'          => 'Products',
        'singular_name' => 'Product',
        'menu_name'     => 'Products',
        // ... other labels
    );

    $args = array(
        'labels'              => $labels,
        'public'              => true,
        'has_archive'         => true,
        'rewrite'             => array( 'slug' => 'products', 'with_front' => false ),
        'supports'            => array( 'title', 'editor', 'thumbnail', 'custom-fields' ),
        'show_in_rest'        => true,
        'rest_base'           => 'products',
        'rest_controller_class' => 'WP_REST_Posts_Controller',
        
        // Custom capabilities
        'capability_type'     => 'product',
        'capabilities' => array(
            'edit_post'          => 'edit_product',
            'read_post'          => 'read_product',
            'delete_post'        => 'delete_product',
            'edit_posts'         => 'edit_products',
            'edit_others_posts'  => 'edit_others_products',
            'publish_posts'      => 'publish_products',
            'read_private_posts' => 'read_private_products',
        ),
        'map_meta_cap'        => true,
    );

    register_post_type( 'product', $args );
    
    // Add capabilities to administrator
    $admin_role = get_role( 'administrator' );
    $admin_role->add_cap( 'edit_product' );
    $admin_role->add_cap( 'edit_products' );
    $admin_role->add_cap( 'edit_others_products' );
    $admin_role->add_cap( 'publish_products' );
    $admin_role->add_cap( 'read_private_products' );
    $admin_role->add_cap( 'delete_product' );
}
add_action( 'init', 'register_product_post_type' );
```

## CPT with Custom Taxonomy

```php
// Register CPT
function register_movie_post_type() {
    register_post_type( 'movie', array(
        'labels' => array(
            'name'          => 'Movies',
            'singular_name' => 'Movie',
        ),
        'public'      => true,
        'has_archive' => true,
        'rewrite'     => array( 'slug' => 'movies' ),
        'supports'    => array( 'title', 'editor', 'thumbnail' ),
        'show_in_rest' => true,
        'menu_icon'   => 'dashicons-video-alt3',
        'taxonomies'  => array( 'genre' ),  // Connect to genre taxonomy
    ) );
}
add_action( 'init', 'register_movie_post_type' );

// Register Taxonomy
function register_genre_taxonomy() {
    register_taxonomy( 'genre', 'movie', array(
        'labels' => array(
            'name'          => 'Genres',
            'singular_name' => 'Genre',
        ),
        'public'       => true,
        'hierarchical' => true,  // Like categories
        'show_in_rest' => true,
        'rewrite'      => array( 'slug' => 'genre' ),
    ) );
}
add_action( 'init', 'register_genre_taxonomy' );
```

## Query Custom Post Types

### Basic Query

```php
$args = array(
    'post_type'      => 'book',
    'posts_per_page' => 10,
    'orderby'        => 'date',
    'order'          => 'DESC',
);

$books = new WP_Query( $args );

if ( $books->have_posts() ) {
    while ( $books->have_posts() ) {
        $books->the_post();
        the_title();
        the_content();
    }
    wp_reset_postdata();
}
```

### Query with Meta

```php
$args = array(
    'post_type'  => 'product',
    'meta_query' => array(
        array(
            'key'     => 'price',
            'value'   => 100,
            'compare' => '<=',
            'type'    => 'NUMERIC',
        ),
    ),
);

$products = new WP_Query( $args );
```

### Query with Taxonomy

```php
$args = array(
    'post_type' => 'movie',
    'tax_query' => array(
        array(
            'taxonomy' => 'genre',
            'field'    => 'slug',
            'terms'    => 'action',
        ),
    ),
);

$movies = new WP_Query( $args );
```

## Custom Archive Template

Create file: `archive-book.php`

```php
<?php get_header(); ?>

<div class="book-archive">
    <h1><?php post_type_archive_title(); ?></h1>
    
    <?php if ( have_posts() ) : ?>
        <div class="books-grid">
            <?php while ( have_posts() ) : the_post(); ?>
                <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                    <?php the_post_thumbnail( 'medium' ); ?>
                    <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                    <?php the_excerpt(); ?>
                    
                    <?php
                    // Display custom meta
                    $author = get_post_meta( get_the_ID(), 'book_author', true );
                    $isbn = get_post_meta( get_the_ID(), 'isbn', true );
                    ?>
                    
                    <?php if ( $author ) : ?>
                        <p class="book-author">By: <?php echo esc_html( $author ); ?></p>
                    <?php endif; ?>
                    
                    <?php if ( $isbn ) : ?>
                        <p class="book-isbn">ISBN: <?php echo esc_html( $isbn ); ?></p>
                    <?php endif; ?>
                </article>
            <?php endwhile; ?>
        </div>
        
        <?php the_posts_pagination(); ?>
    <?php else : ?>
        <p>No books found.</p>
    <?php endif; ?>
</div>

<?php get_footer(); ?>
```

## Custom Single Template

Create file: `single-book.php`

```php
<?php get_header(); ?>

<?php while ( have_posts() ) : the_post(); ?>
    <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
        <h1><?php the_title(); ?></h1>
        
        <?php the_post_thumbnail( 'large' ); ?>
        
        <div class="book-meta">
            <?php
            $author = get_post_meta( get_the_ID(), 'book_author', true );
            $isbn = get_post_meta( get_the_ID(), 'isbn', true );
            $published = get_post_meta( get_the_ID(), 'published_date', true );
            ?>
            
            <?php if ( $author ) : ?>
                <p><strong>Author:</strong> <?php echo esc_html( $author ); ?></p>
            <?php endif; ?>
            
            <?php if ( $isbn ) : ?>
                <p><strong>ISBN:</strong> <?php echo esc_html( $isbn ); ?></p>
            <?php endif; ?>
            
            <?php if ( $published ) : ?>
                <p><strong>Published:</strong> <?php echo esc_html( $published ); ?></p>
            <?php endif; ?>
        </div>
        
        <div class="book-content">
            <?php the_content(); ?>
        </div>
    </article>
<?php endwhile; ?>

<?php get_footer(); ?>
```

## Add to Main Query

```php
// Show CPT in main query
function add_books_to_query( $query ) {
    if ( ! is_admin() && $query->is_main_query() && $query->is_home() ) {
        $query->set( 'post_type', array( 'post', 'book' ) );
    }
}
add_action( 'pre_get_posts', 'add_books_to_query' );
```

## Official Documentation

https://developer.wordpress.org/plugins/post-types/registering-custom-post-types/
https://developer.wordpress.org/reference/functions/register_post_type/
