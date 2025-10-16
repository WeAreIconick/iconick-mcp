# Register Custom Taxonomy

```php
// Non-hierarchical taxonomy (like tags)
function register_project_tags() {
    $labels = array(
        'name' => 'Project Tags',
        'singular_name' => 'Project Tag',
        'search_items' => 'Search Tags',
        'all_items' => 'All Tags',
        'edit_item' => 'Edit Tag',
        'update_item' => 'Update Tag',
        'add_new_item' => 'Add New Tag'
    );
    
    register_taxonomy( 'project_tag', array( 'portfolio' ), array(
        'labels' => $labels,
        'hierarchical' => false,
        'public' => true,
        'show_in_rest' => true,
        'rewrite' => array( 'slug' => 'project-tag' )
    ));
}
add_action( 'init', 'register_project_tags' );

// Hierarchical taxonomy (like categories)
function register_portfolio_category() {
    $labels = array(
        'name' => 'Portfolio Categories',
        'singular_name' => 'Portfolio Category',
        'parent_item' => 'Parent Category',
        'parent_item_colon' => 'Parent Category:',
        'all_items' => 'All Categories',
        'edit_item' => 'Edit Category',
        'update_item' => 'Update Category',
        'add_new_item' => 'Add New Category'
    );
    
    register_taxonomy( 'portfolio_category', array( 'portfolio' ), array(
        'labels' => $labels,
        'hierarchical' => true,
        'public' => true,
        'show_in_rest' => true,
        'show_admin_column' => true,
        'rewrite' => array( 'slug' => 'portfolio-category' )
    ));
}
add_action( 'init', 'register_portfolio_category' );

// Query by taxonomy
$args = array(
    'post_type' => 'portfolio',
    'tax_query' => array(
        array(
            'taxonomy' => 'portfolio_category',
            'field' => 'slug',
            'terms' => 'web-design'
        )
    )
);
```
