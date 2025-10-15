# WordPress Custom Post Types

## Basic Registration

```php
function register_custom_post_type() {
    $args = array(
        'label'  => 'Products',
        'public' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'query_var' => true,
        'rewrite' => array('slug' => 'products'),
        'capability_type' => 'post',
        'has_archive' => true,
        'hierarchical' => false,
        'menu_position' => 5,
        'menu_icon' => 'dashicons-cart',
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'),
        'show_in_rest' => true, // Enable Gutenberg editor
    );
    
    register_post_type('product', $args);
}
add_action('init', 'register_custom_post_type');
```

## Advanced Registration with Capabilities

```php
function register_advanced_cpt() {
    $labels = array(
        'name' => 'Portfolio Items',
        'singular_name' => 'Portfolio Item',
        'menu_name' => 'Portfolio',
        'add_new' => 'Add New Item',
        'add_new_item' => 'Add New Portfolio Item',
        'edit_item' => 'Edit Portfolio Item',
        'new_item' => 'New Portfolio Item',
        'view_item' => 'View Portfolio Item',
        'search_items' => 'Search Portfolio',
        'not_found' => 'No portfolio items found',
        'not_found_in_trash' => 'No portfolio items found in trash'
    );

    $args = array(
        'labels' => $labels,
        'public' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_admin_bar' => true,
        'show_in_nav_menus' => true,
        'can_export' => true,
        'delete_with_user' => false,
        'hierarchical' => false,
        'has_archive' => true,
        'exclude_from_search' => false,
        'publicly_queryable' => true,
        'capability_type' => array('portfolio_item', 'portfolio_items'),
        'map_meta_cap' => true,
        'supports' => array('title', 'editor', 'thumbnail', 'excerpt', 'comments', 'revisions', 'custom-fields'),
        'taxonomies' => array('portfolio_category', 'portfolio_tag'),
        'show_in_rest' => true,
        'rest_base' => 'portfolio',
        'rest_controller_class' => 'WP_REST_Posts_Controller',
    );

    register_post_type('portfolio', $args);
}
```

## Custom Fields and Meta Boxes

```php
// Add meta box for custom fields
function add_product_meta_box() {
    add_meta_box(
        'product_details',
        'Product Details',
        'product_meta_box_callback',
        'product',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes', 'add_product_meta_box');

function product_meta_box_callback($post) {
    wp_nonce_field('product_meta_box', 'product_meta_box_nonce');
    
    $price = get_post_meta($post->ID, '_product_price', true);
    $sku = get_post_meta($post->ID, '_product_sku', true);
    $stock = get_post_meta($post->ID, '_product_stock', true);
    ?>
    <table class="form-table">
        <tr>
            <th><label for="product_price">Price</label></th>
            <td><input type="text" id="product_price" name="product_price" value="<?php echo esc_attr($price); ?>" /></td>
        </tr>
        <tr>
            <th><label for="product_sku">SKU</label></th>
            <td><input type="text" id="product_sku" name="product_sku" value="<?php echo esc_attr($sku); ?>" /></td>
        </tr>
        <tr>
            <th><label for="product_stock">Stock Quantity</label></th>
            <td><input type="number" id="product_stock" name="product_stock" value="<?php echo esc_attr($stock); ?>" /></td>
        </tr>
    </table>
    <?php
}

// Save meta box data
function save_product_meta_box($post_id) {
    if (!isset($_POST['product_meta_box_nonce']) || 
        !wp_verify_nonce($_POST['product_meta_box_nonce'], 'product_meta_box')) {
        return;
    }

    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
        return;
    }

    if (!current_user_can('edit_post', $post_id)) {
        return;
    }

    if (isset($_POST['product_price'])) {
        update_post_meta($post_id, '_product_price', sanitize_text_field($_POST['product_price']));
    }

    if (isset($_POST['product_sku'])) {
        update_post_meta($post_id, '_product_sku', sanitize_text_field($_POST['product_sku']));
    }

    if (isset($_POST['product_stock'])) {
        update_post_meta($post_id, '_product_stock', absint($_POST['product_stock']));
    }
}
add_action('save_post', 'save_product_meta_box');
```

## Template Files

### Single Template
```php
// single-product.php
get_header(); ?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <header class="entry-header">
        <?php the_title('<h1 class="entry-title">', '</h1>'); ?>
    </header>

    <div class="entry-content">
        <?php
        the_content();
        
        $price = get_post_meta(get_the_ID(), '_product_price', true);
        $sku = get_post_meta(get_the_ID(), '_product_sku', true);
        $stock = get_post_meta(get_the_ID(), '_product_stock', true);
        
        if ($price) {
            echo '<p><strong>Price:</strong> $' . esc_html($price) . '</p>';
        }
        if ($sku) {
            echo '<p><strong>SKU:</strong> ' . esc_html($sku) . '</p>';
        }
        if ($stock) {
            echo '<p><strong>Stock:</strong> ' . esc_html($stock) . '</p>';
        }
        ?>
    </div>
</article>

<?php get_footer(); ?>
```

### Archive Template
```php
// archive-product.php
get_header(); ?>

<div class="products-archive">
    <header class="page-header">
        <h1 class="page-title">Our Products</h1>
    </header>

    <div class="products-grid">
        <?php if (have_posts()) : ?>
            <?php while (have_posts()) : the_post(); ?>
                <div class="product-item">
                    <?php if (has_post_thumbnail()) : ?>
                        <div class="product-image">
                            <?php the_post_thumbnail('medium'); ?>
                        </div>
                    <?php endif; ?>
                    
                    <div class="product-info">
                        <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
                        <div class="product-excerpt">
                            <?php the_excerpt(); ?>
                        </div>
                        
                        <?php
                        $price = get_post_meta(get_the_ID(), '_product_price', true);
                        if ($price) {
                            echo '<div class="product-price">$' . esc_html($price) . '</div>';
                        }
                        ?>
                        
                        <a href="<?php the_permalink(); ?>" class="product-link">View Details</a>
                    </div>
                </div>
            <?php endwhile; ?>
        <?php else : ?>
            <p>No products found.</p>
        <?php endif; ?>
    </div>
    
    <?php the_posts_navigation(); ?>
</div>

<?php get_footer(); ?>
```

## Query Custom Post Types

```php
// Query products with meta query
$args = array(
    'post_type' => 'product',
    'posts_per_page' => 10,
    'meta_query' => array(
        array(
            'key' => '_product_stock',
            'value' => 0,
            'compare' => '>'
        ),
        array(
            'key' => '_product_price',
            'value' => array(10, 100),
            'type' => 'NUMERIC',
            'compare' => 'BETWEEN'
        )
    ),
    'orderby' => 'meta_value_num',
    'meta_key' => '_product_price',
    'order' => 'ASC'
);

$products = new WP_Query($args);
```

## Custom Post Type with Custom Fields (Advanced)

```php
// Using ACF-style approach
class ProductCPT {
    public function __construct() {
        add_action('init', array($this, 'register_post_type'));
        add_action('add_meta_boxes', array($this, 'add_meta_boxes'));
        add_action('save_post', array($this, 'save_meta_fields'));
        add_action('rest_api_init', array($this, 'add_custom_fields_to_rest'));
    }

    public function register_post_type() {
        register_post_type('product', array(
            'labels' => array(
                'name' => 'Products',
                'singular_name' => 'Product'
            ),
            'public' => true,
            'show_in_rest' => true,
            'supports' => array('title', 'editor', 'thumbnail', 'excerpt'),
            'has_archive' => true,
        ));
    }

    public function add_meta_boxes() {
        add_meta_box(
            'product_details',
            'Product Details',
            array($this, 'render_meta_box'),
            'product'
        );
    }

    public function render_meta_box($post) {
        wp_nonce_field('product_meta', 'product_meta_nonce');
        
        $fields = array(
            'price' => 'Price',
            'sku' => 'SKU',
            'stock' => 'Stock Quantity',
            'weight' => 'Weight',
            'dimensions' => 'Dimensions'
        );

        echo '<table class="form-table">';
        foreach ($fields as $field => $label) {
            $value = get_post_meta($post->ID, '_product_' . $field, true);
            echo '<tr>';
            echo '<th><label for="product_' . $field . '">' . $label . '</label></th>';
            echo '<td><input type="text" id="product_' . $field . '" name="product_' . $field . '" value="' . esc_attr($value) . '" /></td>';
            echo '</tr>';
        }
        echo '</table>';
    }

    public function save_meta_fields($post_id) {
        if (!isset($_POST['product_meta_nonce']) || 
            !wp_verify_nonce($_POST['product_meta_nonce'], 'product_meta')) {
            return;
        }

        $fields = array('price', 'sku', 'stock', 'weight', 'dimensions');
        
        foreach ($fields as $field) {
            if (isset($_POST['product_' . $field])) {
                update_post_meta($post_id, '_product_' . $field, sanitize_text_field($_POST['product_' . $field]));
            }
        }
    }

    public function add_custom_fields_to_rest() {
        register_rest_field('product', 'product_details', array(
            'get_callback' => array($this, 'get_custom_fields'),
            'update_callback' => array($this, 'update_custom_fields'),
            'schema' => array(
                'description' => 'Product details',
                'type' => 'object',
                'properties' => array(
                    'price' => array('type' => 'string'),
                    'sku' => array('type' => 'string'),
                    'stock' => array('type' => 'string'),
                )
            )
        ));
    }

    public function get_custom_fields($post) {
        return array(
            'price' => get_post_meta($post['id'], '_product_price', true),
            'sku' => get_post_meta($post['id'], '_product_sku', true),
            'stock' => get_post_meta($post['id'], '_product_stock', true),
        );
    }

    public function update_custom_fields($value, $post) {
        update_post_meta($post->ID, '_product_price', $value['price']);
        update_post_meta($post->ID, '_product_sku', $value['sku']);
        update_post_meta($post->ID, '_product_stock', $value['stock']);
    }
}

new ProductCPT();
```

## Best Practices

1. **Use descriptive names** for post types and fields
2. **Always sanitize and validate** custom field data
3. **Use nonces** for security in meta boxes
4. **Create proper templates** for single and archive views
5. **Use meta queries** for filtering and sorting
6. **Enable REST API** support for modern applications
7. **Set proper capabilities** for security
8. **Use hooks** for extending functionality
9. **Cache expensive queries** with transients
10. **Test thoroughly** with different user roles

## Resources

- [WordPress Custom Post Types Documentation](https://developer.wordpress.org/reference/functions/register_post_type/)
- [Custom Fields Documentation](https://developer.wordpress.org/plugins/metadata/custom-meta-boxes/)
- [Template Hierarchy](https://developer.wordpress.org/themes/basics/template-hierarchy/)