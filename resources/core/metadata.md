# WordPress Metadata API

The Metadata API allows you to store custom data associated with posts, users, terms, and comments.

## Basic Metadata Functions

### Adding Metadata

```php
// Add post meta
add_post_meta( $post_id, 'custom_field', 'custom_value' );

// Add user meta
add_user_meta( $user_id, 'phone_number', '555-1234' );

// Add term meta (WordPress 4.4+)
add_term_meta( $term_id, 'featured_color', 'blue' );

// Add comment meta
add_comment_meta( $comment_id, 'rating', 5 );
```

### Getting Metadata

```php
// Get post meta
$value = get_post_meta( $post_id, 'custom_field', true ); // Single value
$values = get_post_meta( $post_id, 'custom_field', false ); // All values

// Get user meta
$phone = get_user_meta( $user_id, 'phone_number', true );

// Get term meta
$color = get_term_meta( $term_id, 'featured_color', true );

// Get comment meta
$rating = get_comment_meta( $comment_id, 'rating', true );
```

### Updating Metadata

```php
// Update post meta (adds if doesn't exist)
update_post_meta( $post_id, 'custom_field', 'new_value' );

// Update user meta
update_user_meta( $user_id, 'phone_number', '555-5678' );

// Update term meta
update_term_meta( $term_id, 'featured_color', 'red' );

// Update comment meta
update_comment_meta( $comment_id, 'rating', 4 );
```

### Deleting Metadata

```php
// Delete post meta
delete_post_meta( $post_id, 'custom_field', 'specific_value' ); // Delete specific value
delete_post_meta( $post_id, 'custom_field' ); // Delete all values

// Delete user meta
delete_user_meta( $user_id, 'phone_number' );

// Delete term meta
delete_term_meta( $term_id, 'featured_color' );

// Delete comment meta
delete_comment_meta( $comment_id, 'rating' );
```

## Advanced Metadata Usage

### Multiple Values (Arrays)

```php
// Add multiple values for the same key
add_post_meta( $post_id, 'tags', 'wordpress' );
add_post_meta( $post_id, 'tags', 'development' );
add_post_meta( $post_id, 'tags', 'tutorial' );

// Get all values
$tags = get_post_meta( $post_id, 'tags', false );
// Returns: array( 'wordpress', 'development', 'tutorial' )

// Store array as single value
$tags_array = array( 'wordpress', 'development', 'tutorial' );
update_post_meta( $post_id, 'tags_array', $tags_array );

// Retrieve array
$stored_tags = get_post_meta( $post_id, 'tags_array', true );
```

### Complex Data Structures

```php
// Store complex data as JSON
$product_data = array(
    'price' => 29.99,
    'currency' => 'USD',
    'in_stock' => true,
    'dimensions' => array(
        'width' => 10,
        'height' => 5,
        'depth' => 2
    ),
    'features' => array( 'feature1', 'feature2', 'feature3' )
);

update_post_meta( $post_id, 'product_data', $product_data );

// Retrieve and use
$product = get_post_meta( $post_id, 'product_data', true );
if ( $product && is_array( $product ) ) {
    echo 'Price: $' . esc_html( $product['price'] );
    echo 'In Stock: ' . ( $product['in_stock'] ? 'Yes' : 'No' );
}
```

## Meta Boxes

### Registering Meta Boxes

```php
function add_custom_meta_boxes() {
    add_meta_box(
        'product_details',           // Meta box ID
        'Product Details',           // Meta box title
        'product_details_callback',  // Callback function
        'product',                   // Post type
        'normal',                    // Context (normal, side, advanced)
        'high'                       // Priority (high, core, default, low)
    );
}
add_action( 'add_meta_boxes', 'add_custom_meta_boxes' );
```

### Meta Box Callback Function

```php
function product_details_callback( $post ) {
    // Add nonce for security
    wp_nonce_field( 'save_product_details', 'product_details_nonce' );
    
    // Get existing values
    $price = get_post_meta( $post->ID, '_product_price', true );
    $sku = get_post_meta( $post->ID, '_product_sku', true );
    $stock = get_post_meta( $post->ID, '_product_stock', true );
    $featured = get_post_meta( $post->ID, '_product_featured', true );
    
    ?>
    <table class="form-table">
        <tr>
            <th scope="row">
                <label for="product_price">Price</label>
            </th>
            <td>
                <input type="number" 
                       id="product_price" 
                       name="product_price" 
                       value="<?php echo esc_attr( $price ); ?>" 
                       step="0.01" 
                       min="0" />
            </td>
        </tr>
        <tr>
            <th scope="row">
                <label for="product_sku">SKU</label>
            </th>
            <td>
                <input type="text" 
                       id="product_sku" 
                       name="product_sku" 
                       value="<?php echo esc_attr( $sku ); ?>" 
                       maxlength="50" />
            </td>
        </tr>
        <tr>
            <th scope="row">
                <label for="product_stock">Stock Quantity</label>
            </th>
            <td>
                <input type="number" 
                       id="product_stock" 
                       name="product_stock" 
                       value="<?php echo esc_attr( $stock ); ?>" 
                       min="0" />
            </td>
        </tr>
        <tr>
            <th scope="row">
                <label for="product_featured">Featured Product</label>
            </th>
            <td>
                <input type="checkbox" 
                       id="product_featured" 
                       name="product_featured" 
                       value="1" 
                       <?php checked( $featured, '1' ); ?> />
                <label for="product_featured">Mark as featured product</label>
            </td>
        </tr>
    </table>
    <?php
}
```

### Saving Meta Box Data

```php
function save_product_details( $post_id ) {
    // Check if nonce is valid
    if ( ! isset( $_POST['product_details_nonce'] ) || 
         ! wp_verify_nonce( $_POST['product_details_nonce'], 'save_product_details' ) ) {
        return;
    }
    
    // Check if user has permission to edit this post
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }
    
    // Check if this is an autosave
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    
    // Check post type
    if ( get_post_type( $post_id ) !== 'product' ) {
        return;
    }
    
    // Sanitize and save data
    if ( isset( $_POST['product_price'] ) ) {
        $price = floatval( $_POST['product_price'] );
        update_post_meta( $post_id, '_product_price', $price );
    }
    
    if ( isset( $_POST['product_sku'] ) ) {
        $sku = sanitize_text_field( $_POST['product_sku'] );
        update_post_meta( $post_id, '_product_sku', $sku );
    }
    
    if ( isset( $_POST['product_stock'] ) ) {
        $stock = intval( $_POST['product_stock'] );
        update_post_meta( $post_id, '_product_stock', $stock );
    }
    
    // Handle checkbox (only saves if checked)
    if ( isset( $_POST['product_featured'] ) ) {
        update_post_meta( $post_id, '_product_featured', '1' );
    } else {
        delete_post_meta( $post_id, '_product_featured' );
    }
}
add_action( 'save_post', 'save_product_details' );
```

## Meta Box with Multiple Fields

```php
function advanced_meta_box_callback( $post ) {
    wp_nonce_field( 'save_advanced_meta', 'advanced_meta_nonce' );
    
    $meta_data = get_post_meta( $post->ID, '_advanced_data', true );
    $defaults = array(
        'title' => '',
        'description' => '',
        'category' => '',
        'tags' => array(),
        'settings' => array(
            'featured' => false,
            'priority' => 'normal',
            'expiry_date' => ''
        )
    );
    
    $data = wp_parse_args( $meta_data, $defaults );
    
    ?>
    <div class="advanced-meta-box">
        <h4>Basic Information</h4>
        <p>
            <label for="advanced_title">Title:</label><br>
            <input type="text" 
                   id="advanced_title" 
                   name="advanced_title" 
                   value="<?php echo esc_attr( $data['title'] ); ?>" 
                   class="widefat" />
        </p>
        
        <p>
            <label for="advanced_description">Description:</label><br>
            <textarea id="advanced_description" 
                      name="advanced_description" 
                      class="widefat" 
                      rows="4"><?php echo esc_textarea( $data['description'] ); ?></textarea>
        </p>
        
        <h4>Categories and Tags</h4>
        <p>
            <label for="advanced_category">Category:</label><br>
            <select id="advanced_category" name="advanced_category" class="widefat">
                <option value="">Select Category</option>
                <option value="news" <?php selected( $data['category'], 'news' ); ?>>News</option>
                <option value="tutorial" <?php selected( $data['category'], 'tutorial' ); ?>>Tutorial</option>
                <option value="review" <?php selected( $data['category'], 'review' ); ?>>Review</option>
            </select>
        </p>
        
        <p>
            <label for="advanced_tags">Tags (comma-separated):</label><br>
            <input type="text" 
                   id="advanced_tags" 
                   name="advanced_tags" 
                   value="<?php echo esc_attr( implode( ', ', $data['tags'] ) ); ?>" 
                   class="widefat" />
        </p>
        
        <h4>Settings</h4>
        <p>
            <label>
                <input type="checkbox" 
                       name="advanced_featured" 
                       value="1" 
                       <?php checked( $data['settings']['featured'], true ); ?> />
                Featured Item
            </label>
        </p>
        
        <p>
            <label for="advanced_priority">Priority:</label><br>
            <select id="advanced_priority" name="advanced_priority" class="widefat">
                <option value="low" <?php selected( $data['settings']['priority'], 'low' ); ?>>Low</option>
                <option value="normal" <?php selected( $data['settings']['priority'], 'normal' ); ?>>Normal</option>
                <option value="high" <?php selected( $data['settings']['priority'], 'high' ); ?>>High</option>
            </select>
        </p>
        
        <p>
            <label for="advanced_expiry">Expiry Date:</label><br>
            <input type="date" 
                   id="advanced_expiry" 
                   name="advanced_expiry" 
                   value="<?php echo esc_attr( $data['settings']['expiry_date'] ); ?>" 
                   class="widefat" />
        </p>
    </div>
    <?php
}
```

### Saving Complex Meta Box Data

```php
function save_advanced_meta( $post_id ) {
    if ( ! isset( $_POST['advanced_meta_nonce'] ) || 
         ! wp_verify_nonce( $_POST['advanced_meta_nonce'], 'save_advanced_meta' ) ) {
        return;
    }
    
    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }
    
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }
    
    // Prepare data array
    $meta_data = array();
    
    // Basic fields
    if ( isset( $_POST['advanced_title'] ) ) {
        $meta_data['title'] = sanitize_text_field( $_POST['advanced_title'] );
    }
    
    if ( isset( $_POST['advanced_description'] ) ) {
        $meta_data['description'] = sanitize_textarea_field( $_POST['advanced_description'] );
    }
    
    if ( isset( $_POST['advanced_category'] ) ) {
        $allowed_categories = array( 'news', 'tutorial', 'review' );
        $category = sanitize_text_field( $_POST['advanced_category'] );
        if ( in_array( $category, $allowed_categories ) ) {
            $meta_data['category'] = $category;
        }
    }
    
    // Tags (convert comma-separated to array)
    if ( isset( $_POST['advanced_tags'] ) ) {
        $tags_string = sanitize_text_field( $_POST['advanced_tags'] );
        $tags = array_map( 'trim', explode( ',', $tags_string ) );
        $tags = array_filter( $tags ); // Remove empty values
        $meta_data['tags'] = $tags;
    }
    
    // Settings
    $meta_data['settings'] = array(
        'featured' => isset( $_POST['advanced_featured'] ),
        'priority' => sanitize_text_field( $_POST['advanced_priority'] ?? 'normal' ),
        'expiry_date' => sanitize_text_field( $_POST['advanced_expiry'] ?? '' )
    );
    
    // Save all data as single meta field
    update_post_meta( $post_id, '_advanced_data', $meta_data );
}
add_action( 'save_post', 'save_advanced_meta' );
```

## Meta Queries

### Query Posts by Meta Values

```php
// Query posts with specific meta value
$posts = get_posts( array(
    'post_type' => 'product',
    'meta_key' => '_product_featured',
    'meta_value' => '1',
    'posts_per_page' => 10
) );

// Query posts with meta value greater than
$expensive_products = get_posts( array(
    'post_type' => 'product',
    'meta_key' => '_product_price',
    'meta_value' => 100,
    'meta_compare' => '>',
    'posts_per_page' => 10
) );

// Complex meta query
$featured_products = get_posts( array(
    'post_type' => 'product',
    'meta_query' => array(
        'relation' => 'AND',
        array(
            'key' => '_product_featured',
            'value' => '1',
            'compare' => '='
        ),
        array(
            'key' => '_product_price',
            'value' => array( 50, 200 ),
            'compare' => 'BETWEEN',
            'type' => 'NUMERIC'
        ),
        array(
            'key' => '_product_stock',
            'value' => 0,
            'compare' => '>',
            'type' => 'NUMERIC'
        )
    ),
    'posts_per_page' => 10
) );
```

### Meta Query with Multiple Conditions

```php
function get_products_by_criteria( $args = array() ) {
    $defaults = array(
        'featured' => false,
        'min_price' => 0,
        'max_price' => 999999,
        'in_stock' => true,
        'category' => '',
        'posts_per_page' => 10
    );
    
    $args = wp_parse_args( $args, $defaults );
    
    $meta_query = array();
    
    if ( $args['featured'] ) {
        $meta_query[] = array(
            'key' => '_product_featured',
            'value' => '1',
            'compare' => '='
        );
    }
    
    if ( $args['min_price'] > 0 || $args['max_price'] < 999999 ) {
        $meta_query[] = array(
            'key' => '_product_price',
            'value' => array( $args['min_price'], $args['max_price'] ),
            'compare' => 'BETWEEN',
            'type' => 'NUMERIC'
        );
    }
    
    if ( $args['in_stock'] ) {
        $meta_query[] = array(
            'key' => '_product_stock',
            'value' => 0,
            'compare' => '>',
            'type' => 'NUMERIC'
        );
    }
    
    $query_args = array(
        'post_type' => 'product',
        'posts_per_page' => $args['posts_per_page'],
        'meta_query' => $meta_query
    );
    
    if ( $args['category'] ) {
        $query_args['meta_query'][] = array(
            'key' => '_product_category',
            'value' => $args['category'],
            'compare' => '='
        );
    }
    
    return get_posts( $query_args );
}

// Usage examples
$featured_products = get_products_by_criteria( array( 'featured' => true ) );
$affordable_products = get_products_by_criteria( array( 'max_price' => 50 ) );
$electronics = get_products_by_criteria( array( 'category' => 'electronics', 'in_stock' => true ) );
```

## Best Practices

### Security

```php
// Always sanitize input
function secure_meta_update( $post_id, $meta_key, $meta_value ) {
    // Validate post ID
    if ( ! is_numeric( $post_id ) || $post_id <= 0 ) {
        return false;
    }
    
    // Sanitize meta key
    $meta_key = sanitize_key( $meta_key );
    
    // Validate meta key format (prevent injection)
    if ( ! preg_match( '/^[a-zA-Z0-9_-]+$/', $meta_key ) ) {
        return false;
    }
    
    // Sanitize based on expected data type
    if ( is_string( $meta_value ) ) {
        $meta_value = sanitize_text_field( $meta_value );
    } elseif ( is_numeric( $meta_value ) ) {
        $meta_value = floatval( $meta_value );
    } elseif ( is_array( $meta_value ) ) {
        $meta_value = array_map( 'sanitize_text_field', $meta_value );
    }
    
    return update_post_meta( $post_id, $meta_key, $meta_value );
}
```

### Performance

```php
// Use single meta field for related data
function store_related_meta( $post_id ) {
    $related_data = array(
        'views' => 0,
        'likes' => 0,
        'shares' => 0,
        'last_viewed' => current_time( 'mysql' )
    );
    
    // Store as single meta field instead of multiple
    update_post_meta( $post_id, '_post_stats', $related_data );
    
    // Retrieve and update specific value
    $stats = get_post_meta( $post_id, '_post_stats', true );
    $stats['views']++;
    $stats['last_viewed'] = current_time( 'mysql' );
    update_post_meta( $post_id, '_post_stats', $stats );
}
```

### Data Validation

```php
function validate_meta_data( $meta_key, $meta_value ) {
    $validators = array(
        'email' => 'is_email',
        'url' => 'wp_http_validate_url',
        'numeric' => 'is_numeric',
        'date' => 'strtotime'
    );
    
    if ( isset( $validators[ $meta_key ] ) ) {
        $validator = $validators[ $meta_key ];
        
        if ( function_exists( $validator ) ) {
            return $validator( $meta_value );
        }
    }
    
    return true;
}

// Usage
if ( validate_meta_data( 'email', $email_value ) ) {
    update_post_meta( $post_id, 'contact_email', $email_value );
} else {
    add_settings_error( 'meta_validation', 'invalid_email', 'Invalid email address.' );
}
```

## Official Documentation

https://developer.wordpress.org/apis/metadata/
https://developer.wordpress.org/reference/functions/add_post_meta/
https://developer.wordpress.org/reference/functions/get_post_meta/
https://developer.wordpress.org/reference/functions/update_post_meta/
https://developer.wordpress.org/reference/functions/delete_post_meta/
