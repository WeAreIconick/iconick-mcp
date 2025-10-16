---
difficulty: Intermediate
tags: [taxonomies, terms, categories, tags]
related: [advanced/custom-post-types, core/database-api]
wp_version: 2.3+
---

# WordPress Taxonomies

## Basic Custom Taxonomy Registration

```php
function register_custom_taxonomy() {
    $labels = array(
        'name' => 'Product Categories',
        'singular_name' => 'Product Category',
        'menu_name' => 'Product Categories',
        'all_items' => 'All Product Categories',
        'edit_item' => 'Edit Product Category',
        'view_item' => 'View Product Category',
        'update_item' => 'Update Product Category',
        'add_new_item' => 'Add New Product Category',
        'new_item_name' => 'New Product Category Name',
        'search_items' => 'Search Product Categories',
        'popular_items' => 'Popular Product Categories',
        'separate_items_with_commas' => 'Separate product categories with commas',
        'add_or_remove_items' => 'Add or remove product categories',
        'choose_from_most_used' => 'Choose from most used product categories',
        'not_found' => 'No product categories found'
    );

    $args = array(
        'labels' => $labels,
        'hierarchical' => true,  // Like categories
        'public' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_tagcloud' => true,
        'show_in_quick_edit' => true,
        'show_admin_column' => true,
        'show_in_rest' => true,
        'rest_base' => 'product-categories',
        'rest_controller_class' => 'WP_REST_Terms_Controller',
        'query_var' => true,
        'rewrite' => array('slug' => 'product-category'),
        'capabilities' => array(
            'manage_terms' => 'manage_product_categories',
            'edit_terms' => 'edit_product_categories',
            'delete_terms' => 'delete_product_categories',
            'assign_terms' => 'assign_product_categories'
        )
    );

    register_taxonomy('product_category', array('product'), $args);
}
add_action('init', 'register_custom_taxonomy');
```

## Non-Hierarchical Taxonomy (Tags)

```php
function register_product_tags() {
    $labels = array(
        'name' => 'Product Tags',
        'singular_name' => 'Product Tag',
        'menu_name' => 'Product Tags',
        'all_items' => 'All Product Tags',
        'edit_item' => 'Edit Product Tag',
        'view_item' => 'View Product Tag',
        'update_item' => 'Update Product Tag',
        'add_new_item' => 'Add New Product Tag',
        'new_item_name' => 'New Product Tag Name',
        'search_items' => 'Search Product Tags',
        'popular_items' => 'Popular Product Tags',
        'separate_items_with_commas' => 'Separate product tags with commas',
        'add_or_remove_items' => 'Add or remove product tags',
        'choose_from_most_used' => 'Choose from most used product tags',
        'not_found' => 'No product tags found'
    );

    $args = array(
        'labels' => $labels,
        'hierarchical' => false,  // Like tags
        'public' => true,
        'publicly_queryable' => true,
        'show_ui' => true,
        'show_in_menu' => true,
        'show_in_nav_menus' => true,
        'show_tagcloud' => true,
        'show_in_quick_edit' => true,
        'show_admin_column' => true,
        'show_in_rest' => true,
        'query_var' => true,
        'rewrite' => array('slug' => 'product-tag'),
    );

    register_taxonomy('product_tag', array('product'), $args);
}
add_action('init', 'register_product_tags');
```

## Advanced Taxonomy with Meta Fields

```php
class AdvancedTaxonomy {
    public function __construct() {
        add_action('init', array($this, 'register_taxonomy'));
        add_action('product_category_add_form_fields', array($this, 'add_taxonomy_meta_fields'));
        add_action('product_category_edit_form_fields', array($this, 'edit_taxonomy_meta_fields'));
        add_action('edited_product_category', array($this, 'save_taxonomy_meta_fields'));
        add_action('created_product_category', array($this, 'save_taxonomy_meta_fields'));
    }

    public function register_taxonomy() {
        register_taxonomy('product_category', array('product'), array(
            'labels' => array(
                'name' => 'Product Categories',
                'singular_name' => 'Product Category'
            ),
            'hierarchical' => true,
            'public' => true,
            'show_in_rest' => true,
            'show_admin_column' => true,
        ));
    }

    public function add_taxonomy_meta_fields($taxonomy) {
        ?>
        <div class="form-field">
            <label for="category_color"><?php _e('Category Color', 'textdomain'); ?></label>
            <input type="color" name="category_color" id="category_color" value="#000000" />
            <p class="description"><?php _e('Color for this category', 'textdomain'); ?></p>
        </div>

        <div class="form-field">
            <label for="category_icon"><?php _e('Category Icon', 'textdomain'); ?></label>
            <input type="text" name="category_icon" id="category_icon" value="" />
            <p class="description"><?php _e('Icon class for this category (e.g., fa-heart)', 'textdomain'); ?></p>
        </div>

        <div class="form-field">
            <label for="category_description_short"><?php _e('Short Description', 'textdomain'); ?></label>
            <textarea name="category_description_short" id="category_description_short" rows="3" cols="50"></textarea>
            <p class="description"><?php _e('Short description for this category', 'textdomain'); ?></p>
        </div>
        <?php
    }

    public function edit_taxonomy_meta_fields($term) {
        $color = get_term_meta($term->term_id, 'category_color', true);
        $icon = get_term_meta($term->term_id, 'category_icon', true);
        $short_desc = get_term_meta($term->term_id, 'category_description_short', true);
        ?>
        <tr class="form-field">
            <th scope="row" valign="top">
                <label for="category_color"><?php _e('Category Color', 'textdomain'); ?></label>
            </th>
            <td>
                <input type="color" name="category_color" id="category_color" value="<?php echo esc_attr($color); ?>" />
                <p class="description"><?php _e('Color for this category', 'textdomain'); ?></p>
            </td>
        </tr>

        <tr class="form-field">
            <th scope="row" valign="top">
                <label for="category_icon"><?php _e('Category Icon', 'textdomain'); ?></label>
            </th>
            <td>
                <input type="text" name="category_icon" id="category_icon" value="<?php echo esc_attr($icon); ?>" />
                <p class="description"><?php _e('Icon class for this category (e.g., fa-heart)', 'textdomain'); ?></p>
            </td>
        </tr>

        <tr class="form-field">
            <th scope="row" valign="top">
                <label for="category_description_short"><?php _e('Short Description', 'textdomain'); ?></label>
            </th>
            <td>
                <textarea name="category_description_short" id="category_description_short" rows="3" cols="50"><?php echo esc_textarea($short_desc); ?></textarea>
                <p class="description"><?php _e('Short description for this category', 'textdomain'); ?></p>
            </td>
        </tr>
        <?php
    }

    public function save_taxonomy_meta_fields($term_id) {
        if (isset($_POST['category_color'])) {
            update_term_meta($term_id, 'category_color', sanitize_hex_color($_POST['category_color']));
        }
        
        if (isset($_POST['category_icon'])) {
            update_term_meta($term_id, 'category_icon', sanitize_text_field($_POST['category_icon']));
        }
        
        if (isset($_POST['category_description_short'])) {
            update_term_meta($term_id, 'category_description_short', sanitize_textarea_field($_POST['category_description_short']));
        }
    }
}

new AdvancedTaxonomy();
```

## Query Posts by Taxonomy

```php
// Query posts by taxonomy term
function get_posts_by_category($category_slug, $post_type = 'product') {
    $args = array(
        'post_type' => $post_type,
        'posts_per_page' => -1,
        'tax_query' => array(
            array(
                'taxonomy' => 'product_category',
                'field' => 'slug',
                'terms' => $category_slug,
            ),
        ),
    );

    return new WP_Query($args);
}

// Query posts by multiple taxonomy terms
function get_posts_by_multiple_taxonomies($categories, $tags) {
    $args = array(
        'post_type' => 'product',
        'posts_per_page' => 10,
        'tax_query' => array(
            'relation' => 'AND',
            array(
                'taxonomy' => 'product_category',
                'field' => 'slug',
                'terms' => $categories,
                'operator' => 'IN'
            ),
            array(
                'taxonomy' => 'product_tag',
                'field' => 'slug',
                'terms' => $tags,
                'operator' => 'IN'
            )
        ),
    );

    return new WP_Query($args);
}

// Get taxonomy terms with meta
function get_taxonomy_terms_with_meta($taxonomy = 'product_category') {
    $terms = get_terms(array(
        'taxonomy' => $taxonomy,
        'hide_empty' => false,
    ));

    foreach ($terms as $term) {
        $term->color = get_term_meta($term->term_id, 'category_color', true);
        $term->icon = get_term_meta($term->term_id, 'category_icon', true);
        $term->short_description = get_term_meta($term->term_id, 'category_description_short', true);
    }

    return $terms;
}
```

## Taxonomy Templates

### Taxonomy Archive Template
```php
// taxonomy-product_category.php
get_header(); ?>

<div class="product-category-archive">
    <?php
    $current_term = get_queried_object();
    $category_color = get_term_meta($current_term->term_id, 'category_color', true);
    $category_icon = get_term_meta($current_term->term_id, 'category_icon', true);
    ?>

    <header class="page-header" style="background-color: <?php echo esc_attr($category_color); ?>;">
        <div class="container">
            <?php if ($category_icon) : ?>
                <i class="<?php echo esc_attr($category_icon); ?>"></i>
            <?php endif; ?>
            
            <h1 class="page-title"><?php single_term_title(); ?></h1>
            
            <?php if (term_description()) : ?>
                <div class="term-description">
                    <?php echo term_description(); ?>
                </div>
            <?php endif; ?>
        </div>
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
                    </div>
                </div>
            <?php endwhile; ?>
        <?php else : ?>
            <p>No products found in this category.</p>
        <?php endif; ?>
    </div>
</div>

<?php get_footer(); ?>
```

## Best Practices

1. **Use descriptive names** for taxonomies and terms
2. **Choose hierarchical vs non-hierarchical** based on your needs
3. **Set proper capabilities** for security
4. **Use meta fields** to extend taxonomy functionality
5. **Create proper templates** for taxonomy archives
6. **Use tax_query** for complex filtering
7. **Enable REST API** for modern applications
8. **Cache taxonomy queries** for performance
9. **Use term meta** for additional data
10. **Test with different user roles**

## Resources

- [WordPress Taxonomies Documentation](https://developer.wordpress.org/reference/functions/register_taxonomy/)
- [Taxonomy Templates](https://developer.wordpress.org/themes/basics/template-hierarchy/#custom-taxonomies)
- [Term Meta Documentation](https://developer.wordpress.org/reference/functions/get_term_meta/)