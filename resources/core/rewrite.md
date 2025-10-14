# WordPress Rewrite API

The Rewrite API allows you to create custom URL structures and query variables.

## Basic Concepts

WordPress uses a rewrite system that converts "pretty" URLs into query parameters that WordPress can understand.

```php
// Pretty URL: /products/awesome-widget/
// Internal query: ?post_type=product&name=awesome-widget
```

## Adding Custom Rewrite Rules

```php
function add_custom_rewrite_rules() {
    // Add custom rewrite rule
    add_rewrite_rule(
        '^products/([^/]+)/?$',           // URL pattern
        'index.php?post_type=product&name=$matches[1]', // Query string
        'top'                             // Priority
    );
}
add_action( 'init', 'add_custom_rewrite_rules' );

// Flush rewrite rules (only when rules change)
flush_rewrite_rules();
```

## Query Variables

### Register Custom Query Variables

```php
function add_custom_query_vars( $vars ) {
    $vars[] = 'custom_param';
    $vars[] = 'filter_value';
    return $vars;
}
add_filter( 'query_vars', 'add_custom_query_vars' );
```

### Using Custom Query Variables

```php
function handle_custom_queries( $query ) {
    if ( ! is_admin() && $query->is_main_query() ) {
        
        if ( get_query_var( 'custom_param' ) ) {
            // Handle custom parameter
            $custom_value = get_query_var( 'custom_param' );
            
            // Modify query based on parameter
            $query->set( 'meta_key', 'custom_field' );
            $query->set( 'meta_value', $custom_value );
        }
    }
}
add_action( 'pre_get_posts', 'handle_custom_queries' );
```

## Best Practices

1. **Flush rules only when necessary** - Don't flush on every request
2. **Use specific patterns first** - More specific rules before general ones
3. **Test thoroughly** - Rewrite rules can be tricky to debug
4. **Document your rules** - Keep track of what each rule does
5. **Consider performance** - Too many rules can slow down URL parsing

## Official Documentation

https://developer.wordpress.org/apis/rewrite/
https://developer.wordpress.org/reference/functions/add_rewrite_rule/
https://developer.wordpress.org/reference/functions/flush_rewrite_rules/
