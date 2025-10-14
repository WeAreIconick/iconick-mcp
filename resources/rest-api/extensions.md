# WordPress REST API Extensions

Extending and modifying existing WordPress REST API endpoints.

## Basic Endpoint Extensions

### Adding Fields to Existing Endpoints

```php
// PHP: Add custom fields to posts endpoint
function add_custom_fields_to_posts() {
    // Add custom field to posts
    register_rest_field('post', 'custom_meta', array(
        'get_callback' => function($object, $field_name, $request) {
            return get_post_meta($object['id'], 'custom_meta', true);
        },
        'update_callback' => function($value, $object, $field_name) {
            return update_post_meta($object->ID, 'custom_meta', $value);
        },
        'schema' => array(
            'description' => 'Custom meta field',
            'type' => 'string',
            'context' => array('view', 'edit')
        )
    ));
    
    // Add multiple custom fields
    register_rest_field('post', 'featured_image_url', array(
        'get_callback' => function($object, $field_name, $request) {
            $thumbnail_id = get_post_thumbnail_id($object['id']);
            return $thumbnail_id ? wp_get_attachment_image_url($thumbnail_id, 'full') : null;
        },
        'schema' => array(
            'description' => 'Featured image URL',
            'type' => 'string',
            'format' => 'uri',
            'context' => array('view', 'edit', 'embed')
        )
    ));
    
    // Add computed field
    register_rest_field('post', 'reading_time', array(
        'get_callback' => function($object, $field_name, $request) {
            $content = get_post_field('post_content', $object['id']);
            $word_count = str_word_count(strip_tags($content));
            return ceil($word_count / 200); // Assume 200 words per minute
        },
        'schema' => array(
            'description' => 'Estimated reading time in minutes',
            'type' => 'integer',
            'context' => array('view', 'edit', 'embed')
        )
    ));
}
add_action('rest_api_init', 'add_custom_fields_to_posts');
```

### Adding Fields to Custom Post Types

```php
// PHP: Add fields to custom post type
function add_fields_to_products() {
    register_rest_field('product', 'price', array(
        'get_callback' => function($object, $field_name, $request) {
            return floatval(get_post_meta($object['id'], 'price', true));
        },
        'update_callback' => function($value, $object, $field_name) {
            return update_post_meta($object->ID, 'price', floatval($value));
        },
        'schema' => array(
            'description' => 'Product price',
            'type' => 'number',
            'context' => array('view', 'edit')
        )
    ));
    
    register_rest_field('product', 'sku', array(
        'get_callback' => function($object, $field_name, $request) {
            return get_post_meta($object['id'], 'sku', true);
        },
        'update_callback' => function($value, $object, $field_name) {
            return update_post_meta($object->ID, 'sku', sanitize_text_field($value));
        },
        'schema' => array(
            'description' => 'Product SKU',
            'type' => 'string',
            'context' => array('view', 'edit')
        )
    ));
    
    register_rest_field('product', 'categories', array(
        'get_callback' => function($object, $field_name, $request) {
            $terms = get_the_terms($object['id'], 'product_category');
            if (is_wp_error($terms) || !$terms) {
                return array();
            }
            
            return array_map(function($term) {
                return array(
                    'id' => $term->term_id,
                    'name' => $term->name,
                    'slug' => $term->slug
                );
            }, $terms);
        },
        'schema' => array(
            'description' => 'Product categories',
            'type' => 'array',
            'items' => array(
                'type' => 'object',
                'properties' => array(
                    'id' => array('type' => 'integer'),
                    'name' => array('type' => 'string'),
                    'slug' => array('type' => 'string')
                )
            ),
            'context' => array('view', 'edit')
        )
    ));
}
add_action('rest_api_init', 'add_fields_to_products');
```

## Advanced Endpoint Modifications

### Modifying Existing Endpoint Behavior

```php
// PHP: Modify existing endpoint behavior
function modify_posts_endpoint() {
    // Add custom query parameters
    add_filter('rest_post_query', 'add_custom_post_query_params', 10, 2);
    
    // Modify response data
    add_filter('rest_prepare_post', 'modify_post_response', 10, 3);
    
    // Add custom headers
    add_filter('rest_post_dispatch', 'add_custom_headers', 10, 3);
}

function add_custom_post_query_params($args, $request) {
    // Add custom meta query parameter
    if ($request->get_param('meta_key')) {
        $args['meta_key'] = $request->get_param('meta_key');
        $args['meta_value'] = $request->get_param('meta_value');
    }
    
    // Add custom date range
    if ($request->get_param('date_from')) {
        $args['date_query'] = array(
            array(
                'after' => $request->get_param('date_from'),
                'inclusive' => true
            )
        );
        
        if ($request->get_param('date_to')) {
            $args['date_query'][0]['before'] = $request->get_param('date_to');
        }
    }
    
    // Add custom ordering
    if ($request->get_param('orderby') === 'custom_field') {
        $args['meta_key'] = $request->get_param('orderby_key');
        $args['orderby'] = 'meta_value';
        $args['meta_type'] = $request->get_param('orderby_type') ?: 'CHAR';
    }
    
    return $args;
}

function modify_post_response($response, $post, $request) {
    // Add custom data to response
    $data = $response->get_data();
    
    // Add view count
    $data['view_count'] = get_post_meta($post->ID, 'view_count', true) ?: 0;
    
    // Add related posts
    $related_posts = get_posts(array(
        'post_type' => 'post',
        'posts_per_page' => 3,
        'exclude' => array($post->ID),
        'category__in' => wp_get_post_categories($post->ID)
    ));
    
    $data['related_posts'] = array_map(function($related_post) {
        return array(
            'id' => $related_post->ID,
            'title' => $related_post->post_title,
            'link' => get_permalink($related_post->ID),
            'date' => $related_post->post_date
        );
    }, $related_posts);
    
    // Add custom headers
    $response->header('X-Post-ID', $post->ID);
    $response->header('X-Cache-Timestamp', time());
    
    return $response;
}

function add_custom_headers($result, $server, $request) {
    // Add custom headers to all responses
    $result->header('X-API-Version', '1.0');
    $result->header('X-Response-Time', microtime(true) - $_SERVER['REQUEST_TIME_FLOAT']);
    
    return $result;
}

add_action('rest_api_init', 'modify_posts_endpoint');
```

### Custom Query Parameters

```php
// PHP: Add custom query parameters
function add_custom_query_params() {
    // Add to posts endpoint
    add_filter('rest_post_collection_params', 'add_posts_collection_params');
    
    // Add to users endpoint
    add_filter('rest_user_collection_params', 'add_users_collection_params');
}

function add_posts_collection_params($params) {
    $params['featured'] = array(
        'description' => 'Limit result set to featured posts',
        'type' => 'boolean',
        'sanitize_callback' => 'rest_sanitize_boolean'
    );
    
    $params['meta_key'] = array(
        'description' => 'Limit result set to posts with specific meta key',
        'type' => 'string',
        'sanitize_callback' => 'sanitize_text_field'
    );
    
    $params['meta_value'] = array(
        'description' => 'Limit result set to posts with specific meta value',
        'type' => 'string',
        'sanitize_callback' => 'sanitize_text_field'
    );
    
    $params['date_from'] = array(
        'description' => 'Limit result set to posts from specific date',
        'type' => 'string',
        'format' => 'date',
        'sanitize_callback' => 'sanitize_text_field'
    );
    
    $params['date_to'] = array(
        'description' => 'Limit result set to posts until specific date',
        'type' => 'string',
        'format' => 'date',
        'sanitize_callback' => 'sanitize_text_field'
    );
    
    return $params;
}

function add_users_collection_params($params) {
    $params['role'] = array(
        'description' => 'Limit result set to users with specific role',
        'type' => 'string',
        'enum' => array_keys(get_editable_roles()),
        'sanitize_callback' => 'sanitize_text_field'
    );
    
    $params['registered_after'] = array(
        'description' => 'Limit result set to users registered after date',
        'type' => 'string',
        'format' => 'date',
        'sanitize_callback' => 'sanitize_text_field'
    );
    
    return $params;
}

add_action('rest_api_init', 'add_custom_query_params');
```

## Endpoint Overrides

### Completely Override Endpoint

```php
// PHP: Override existing endpoint
function override_posts_endpoint() {
    // Remove default posts endpoint
    remove_action('rest_api_init', 'create_initial_rest_routes', 99);
    
    // Register custom posts endpoint
    register_rest_route('wp/v2', '/posts', array(
        'methods' => 'GET',
        'callback' => 'custom_get_posts',
        'permission_callback' => '__return_true',
        'args' => array(
            'page' => array(
                'default' => 1,
                'sanitize_callback' => 'absint'
            ),
            'per_page' => array(
                'default' => 10,
                'sanitize_callback' => 'absint'
            ),
            'search' => array(
                'sanitize_callback' => 'sanitize_text_field'
            ),
            'featured' => array(
                'type' => 'boolean',
                'sanitize_callback' => 'rest_sanitize_boolean'
            )
        )
    ));
}

function custom_get_posts($request) {
    $args = array(
        'post_type' => 'post',
        'post_status' => 'publish',
        'posts_per_page' => $request->get_param('per_page'),
        'paged' => $request->get_param('page')
    );
    
    // Add search
    if ($request->get_param('search')) {
        $args['s'] = $request->get_param('search');
    }
    
    // Add featured filter
    if ($request->get_param('featured')) {
        $args['meta_query'] = array(
            array(
                'key' => 'featured',
                'value' => '1',
                'compare' => '='
            )
        );
    }
    
    $posts = get_posts($args);
    $total_posts = wp_count_posts('post')->publish;
    
    $formatted_posts = array_map(function($post) {
        return array(
            'id' => $post->ID,
            'title' => $post->post_title,
            'content' => $post->post_content,
            'excerpt' => $post->post_excerpt,
            'date' => $post->post_date,
            'featured' => get_post_meta($post->ID, 'featured', true),
            'view_count' => get_post_meta($post->ID, 'view_count', true) ?: 0
        );
    }, $posts);
    
    return rest_ensure_response(array(
        'posts' => $formatted_posts,
        'total' => $total_posts,
        'pages' => ceil($total_posts / $request->get_param('per_page'))
    ));
}

add_action('rest_api_init', 'override_posts_endpoint', 100);
```

## Custom Endpoint Collections

### Bulk Operations Endpoint

```php
// PHP: Bulk operations endpoint
function register_bulk_operations_endpoint() {
    register_rest_route('my-plugin/v1', '/bulk/posts', array(
        'methods' => 'POST',
        'callback' => 'handle_bulk_posts_operation',
        'permission_callback' => 'check_user_can_edit_posts',
        'args' => array(
            'operation' => array(
                'required' => true,
                'type' => 'string',
                'enum' => array('update', 'delete', 'trash', 'untrash', 'publish', 'draft'),
                'sanitize_callback' => 'sanitize_text_field'
            ),
            'post_ids' => array(
                'required' => true,
                'type' => 'array',
                'items' => array(
                    'type' => 'integer'
                ),
                'validate_callback' => function($param, $request, $key) {
                    return is_array($param) && !empty($param);
                }
            ),
            'data' => array(
                'type' => 'object',
                'description' => 'Additional data for the operation'
            )
        )
    ));
}

function handle_bulk_posts_operation($request) {
    $operation = $request->get_param('operation');
    $post_ids = $request->get_param('post_ids');
    $data = $request->get_param('data');
    
    $results = array();
    $errors = array();
    
    foreach ($post_ids as $post_id) {
        // Check if user can edit this post
        if (!current_user_can('edit_post', $post_id)) {
            $errors[] = array(
                'post_id' => $post_id,
                'error' => 'Permission denied'
            );
            continue;
        }
        
        switch ($operation) {
            case 'update':
                if (isset($data['post_status'])) {
                    $result = wp_update_post(array(
                        'ID' => $post_id,
                        'post_status' => $data['post_status']
                    ));
                    $results[] = array(
                        'post_id' => $post_id,
                        'success' => !is_wp_error($result)
                    );
                }
                break;
                
            case 'delete':
                $result = wp_delete_post($post_id, true);
                $results[] = array(
                    'post_id' => $post_id,
                    'success' => !is_wp_error($result)
                );
                break;
                
            case 'trash':
                $result = wp_trash_post($post_id);
                $results[] = array(
                    'post_id' => $post_id,
                    'success' => !is_wp_error($result)
                );
                break;
                
            case 'untrash':
                $result = wp_untrash_post($post_id);
                $results[] = array(
                    'post_id' => $post_id,
                    'success' => !is_wp_error($result)
                );
                break;
        }
    }
    
    return rest_ensure_response(array(
        'results' => $results,
        'errors' => $errors,
        'total_processed' => count($post_ids),
        'successful' => count($results),
        'failed' => count($errors)
    ));
}

add_action('rest_api_init', 'register_bulk_operations_endpoint');
```

### Search Endpoint

```php
// PHP: Advanced search endpoint
function register_search_endpoint() {
    register_rest_route('my-plugin/v1', '/search', array(
        'methods' => 'GET',
        'callback' => 'handle_advanced_search',
        'permission_callback' => '__return_true',
        'args' => array(
            'q' => array(
                'required' => true,
                'type' => 'string',
                'sanitize_callback' => 'sanitize_text_field'
            ),
            'type' => array(
                'type' => 'array',
                'items' => array(
                    'type' => 'string',
                    'enum' => array('post', 'page', 'product', 'user')
                ),
                'default' => array('post', 'page')
            ),
            'fields' => array(
                'type' => 'array',
                'items' => array(
                    'type' => 'string',
                    'enum' => array('title', 'content', 'excerpt', 'meta')
                ),
                'default' => array('title', 'content', 'excerpt')
            ),
            'limit' => array(
                'type' => 'integer',
                'default' => 10,
                'minimum' => 1,
                'maximum' => 100
            ),
            'page' => array(
                'type' => 'integer',
                'default' => 1,
                'minimum' => 1
            )
        )
    ));
}

function handle_advanced_search($request) {
    $query = $request->get_param('q');
    $types = $request->get_param('type');
    $fields = $request->get_param('fields');
    $limit = $request->get_param('limit');
    $page = $request->get_param('page');
    
    $results = array();
    
    foreach ($types as $type) {
        $args = array(
            'post_type' => $type,
            'posts_per_page' => $limit,
            'paged' => $page,
            'post_status' => 'publish'
        );
        
        // Build search query based on fields
        $search_query = array();
        foreach ($fields as $field) {
            switch ($field) {
                case 'title':
                    $search_query[] = $query;
                    break;
                case 'content':
                    // Add meta query for content search
                    $args['meta_query'] = array(
                        'relation' => 'OR',
                        array(
                            'key' => '_search_content',
                            'value' => $query,
                            'compare' => 'LIKE'
                        )
                    );
                    break;
                case 'meta':
                    $args['meta_query'] = array(
                        'relation' => 'OR',
                        array(
                            'key' => 'custom_meta',
                            'value' => $query,
                            'compare' => 'LIKE'
                        )
                    );
                    break;
            }
        }
        
        if (!empty($search_query)) {
            $args['s'] = implode(' ', $search_query);
        }
        
        $posts = get_posts($args);
        
        foreach ($posts as $post) {
            $results[] = array(
                'id' => $post->ID,
                'type' => $post->post_type,
                'title' => $post->post_title,
                'excerpt' => wp_trim_words($post->post_excerpt ?: $post->post_content, 20),
                'url' => get_permalink($post->ID),
                'date' => $post->post_date,
                'score' => calculate_search_score($post, $query, $fields)
            );
        }
    }
    
    // Sort by relevance score
    usort($results, function($a, $b) {
        return $b['score'] <=> $a['score'];
    });
    
    return rest_ensure_response(array(
        'results' => $results,
        'total' => count($results),
        'query' => $query,
        'types' => $types,
        'fields' => $fields
    ));
}

function calculate_search_score($post, $query, $fields) {
    $score = 0;
    $query_lower = strtolower($query);
    
    // Title match (highest score)
    if (strpos(strtolower($post->post_title), $query_lower) !== false) {
        $score += 10;
    }
    
    // Content match
    if (strpos(strtolower($post->post_content), $query_lower) !== false) {
        $score += 5;
    }
    
    // Excerpt match
    if (strpos(strtolower($post->post_excerpt), $query_lower) !== false) {
        $score += 3;
    }
    
    // Meta match
    $custom_meta = get_post_meta($post->ID, 'custom_meta', true);
    if (strpos(strtolower($custom_meta), $query_lower) !== false) {
        $score += 2;
    }
    
    return $score;
}

add_action('rest_api_init', 'register_search_endpoint');
```

## Best Practices

### Performance Optimization

```php
// PHP: Optimize endpoint performance
function optimize_endpoint_performance() {
    // Cache expensive queries
    add_filter('rest_post_query', 'cache_post_queries', 10, 2);
    
    // Limit response size
    add_filter('rest_prepare_post', 'limit_response_size', 10, 3);
    
    // Use efficient queries
    add_filter('rest_post_query', 'optimize_post_queries', 10, 2);
}

function cache_post_queries($args, $request) {
    // Add cache key based on request parameters
    $cache_key = 'rest_posts_' . md5(serialize($request->get_params()));
    
    $cached_result = get_transient($cache_key);
    if ($cached_result !== false) {
        return $cached_result;
    }
    
    // Store result in cache
    set_transient($cache_key, $args, 300); // 5 minutes
    
    return $args;
}

function limit_response_size($response, $post, $request) {
    // Limit content length for list views
    if ($request->get_route() === '/wp/v2/posts') {
        $data = $response->get_data();
        if (isset($data['content']['rendered'])) {
            $data['content']['rendered'] = wp_trim_words($data['content']['rendered'], 50);
            $response->set_data($data);
        }
    }
    
    return $response;
}

function optimize_post_queries($args, $request) {
    // Use specific fields to reduce memory usage
    $args['fields'] = 'ids';
    
    // Add proper indexing hints
    $args['meta_query'] = array(
        'relation' => 'AND',
        array(
            'key' => 'featured',
            'compare' => 'EXISTS'
        )
    );
    
    return $args;
}

add_action('rest_api_init', 'optimize_endpoint_performance');
```

## Official Documentation

https://developer.wordpress.org/rest-api/extending-the-rest-api/
https://developer.wordpress.org/reference/functions/register_rest_field/
https://developer.wordpress.org/reference/hooks/rest_prepare_post/
