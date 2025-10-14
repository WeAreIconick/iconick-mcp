# WordPress REST API Schema

Comprehensive schema definition and validation for WordPress REST API endpoints.

## Basic Schema Structure

### Simple Schema Definition

```php
// PHP: Basic schema for custom endpoint
function get_post_schema() {
    return array(
        '$schema' => 'http://json-schema.org/draft-04/schema#',
        'title' => 'Post',
        'type' => 'object',
        'properties' => array(
            'id' => array(
                'description' => 'Unique identifier for the post',
                'type' => 'integer',
                'context' => array('view', 'edit', 'embed'),
                'readonly' => true
            ),
            'title' => array(
                'description' => 'The title for the post',
                'type' => 'object',
                'context' => array('view', 'edit', 'embed'),
                'properties' => array(
                    'raw' => array(
                        'description' => 'Title for the post, as it exists in the database',
                        'type' => 'string',
                        'context' => array('edit')
                    ),
                    'rendered' => array(
                        'description' => 'HTML title for the post, transformed for display',
                        'type' => 'string',
                        'context' => array('view', 'edit', 'embed'),
                        'readonly' => true
                    )
                )
            ),
            'content' => array(
                'description' => 'The content for the post',
                'type' => 'object',
                'context' => array('view', 'edit'),
                'properties' => array(
                    'raw' => array(
                        'description' => 'Content for the post, as it exists in the database',
                        'type' => 'string',
                        'context' => array('edit')
                    ),
                    'rendered' => array(
                        'description' => 'HTML content for the post, transformed for display',
                        'type' => 'string',
                        'context' => array('view', 'edit'),
                        'readonly' => true
                    )
                )
            ),
            'excerpt' => array(
                'description' => 'The excerpt for the post',
                'type' => 'object',
                'context' => array('view', 'edit', 'embed'),
                'properties' => array(
                    'raw' => array(
                        'description' => 'Excerpt for the post, as it exists in the database',
                        'type' => 'string',
                        'context' => array('edit')
                    ),
                    'rendered' => array(
                        'description' => 'HTML excerpt for the post, transformed for display',
                        'type' => 'string',
                        'context' => array('view', 'edit', 'embed'),
                        'readonly' => true
                    )
                )
            ),
            'date' => array(
                'description' => 'The date the post was published',
                'type' => 'string',
                'format' => 'date-time',
                'context' => array('view', 'edit', 'embed')
            ),
            'status' => array(
                'description' => 'A named status for the post',
                'type' => 'string',
                'enum' => array('publish', 'future', 'draft', 'pending', 'private', 'trash'),
                'context' => array('view', 'edit')
            )
        )
    );
}
```

### Advanced Schema with Validation

```php
// PHP: Advanced schema with validation rules
function get_product_schema() {
    return array(
        '$schema' => 'http://json-schema.org/draft-04/schema#',
        'title' => 'Product',
        'type' => 'object',
        'properties' => array(
            'id' => array(
                'description' => 'Unique identifier for the product',
                'type' => 'integer',
                'minimum' => 1,
                'context' => array('view', 'edit'),
                'readonly' => true
            ),
            'name' => array(
                'description' => 'Product name',
                'type' => 'string',
                'minLength' => 1,
                'maxLength' => 255,
                'context' => array('view', 'edit', 'embed'),
                'arg_options' => array(
                    'sanitize_callback' => 'sanitize_text_field'
                )
            ),
            'description' => array(
                'description' => 'Product description',
                'type' => 'string',
                'context' => array('view', 'edit'),
                'arg_options' => array(
                    'sanitize_callback' => 'wp_kses_post'
                )
            ),
            'price' => array(
                'description' => 'Product price',
                'type' => 'number',
                'minimum' => 0,
                'multipleOf' => 0.01,
                'context' => array('view', 'edit'),
                'arg_options' => array(
                    'validate_callback' => function($param, $request, $key) {
                        return is_numeric($param) && $param >= 0;
                    }
                )
            ),
            'sku' => array(
                'description' => 'Product SKU',
                'type' => 'string',
                'pattern' => '^[A-Z0-9-]+$',
                'maxLength' => 50,
                'context' => array('view', 'edit'),
                'arg_options' => array(
                    'sanitize_callback' => 'sanitize_text_field',
                    'validate_callback' => function($param, $request, $key) {
                        return preg_match('/^[A-Z0-9-]+$/', $param);
                    }
                )
            ),
            'in_stock' => array(
                'description' => 'Whether the product is in stock',
                'type' => 'boolean',
                'context' => array('view', 'edit'),
                'default' => true
            ),
            'categories' => array(
                'description' => 'Product categories',
                'type' => 'array',
                'items' => array(
                    'type' => 'object',
                    'properties' => array(
                        'id' => array(
                            'type' => 'integer',
                            'minimum' => 1
                        ),
                        'name' => array(
                            'type' => 'string'
                        ),
                        'slug' => array(
                            'type' => 'string'
                        )
                    ),
                    'required' => array('id', 'name', 'slug')
                ),
                'context' => array('view', 'edit')
            ),
            'images' => array(
                'description' => 'Product images',
                'type' => 'array',
                'items' => array(
                    'type' => 'object',
                    'properties' => array(
                        'id' => array(
                            'type' => 'integer',
                            'minimum' => 1
                        ),
                        'src' => array(
                            'type' => 'string',
                            'format' => 'uri'
                        ),
                        'alt' => array(
                            'type' => 'string'
                        ),
                        'position' => array(
                            'type' => 'integer',
                            'minimum' => 0
                        )
                    ),
                    'required' => array('id', 'src')
                ),
                'context' => array('view', 'edit')
            ),
            'meta' => array(
                'description' => 'Meta fields',
                'type' => 'object',
                'additionalProperties' => true,
                'context' => array('view', 'edit')
            )
        ),
        'required' => array('name', 'price'),
        'additionalProperties' => false
    );
}
```

## Complex Schema Patterns

### Nested Object Schema

```php
// PHP: Nested object schema
function get_user_profile_schema() {
    return array(
        '$schema' => 'http://json-schema.org/draft-04/schema#',
        'title' => 'User Profile',
        'type' => 'object',
        'properties' => array(
            'id' => array(
                'type' => 'integer',
                'readonly' => true
            ),
            'basic_info' => array(
                'type' => 'object',
                'properties' => array(
                    'first_name' => array(
                        'type' => 'string',
                        'maxLength' => 50,
                        'arg_options' => array(
                            'sanitize_callback' => 'sanitize_text_field'
                        )
                    ),
                    'last_name' => array(
                        'type' => 'string',
                        'maxLength' => 50,
                        'arg_options' => array(
                            'sanitize_callback' => 'sanitize_text_field'
                        )
                    ),
                    'email' => array(
                        'type' => 'string',
                        'format' => 'email',
                        'arg_options' => array(
                            'sanitize_callback' => 'sanitize_email',
                            'validate_callback' => 'is_email'
                        )
                    ),
                    'phone' => array(
                        'type' => 'string',
                        'pattern' => '^\+?[1-9]\d{1,14}$',
                        'arg_options' => array(
                            'sanitize_callback' => 'sanitize_text_field'
                        )
                    )
                ),
                'required' => array('first_name', 'last_name', 'email')
            ),
            'address' => array(
                'type' => 'object',
                'properties' => array(
                    'street' => array(
                        'type' => 'string',
                        'maxLength' => 100
                    ),
                    'city' => array(
                        'type' => 'string',
                        'maxLength' => 50
                    ),
                    'state' => array(
                        'type' => 'string',
                        'maxLength' => 50
                    ),
                    'zip' => array(
                        'type' => 'string',
                        'pattern' => '^\d{5}(-\d{4})?$'
                    ),
                    'country' => array(
                        'type' => 'string',
                        'maxLength' => 2,
                        'pattern' => '^[A-Z]{2}$'
                    )
                )
            ),
            'preferences' => array(
                'type' => 'object',
                'properties' => array(
                    'newsletter' => array(
                        'type' => 'boolean',
                        'default' => false
                    ),
                    'notifications' => array(
                        'type' => 'object',
                        'properties' => array(
                            'email' => array(
                                'type' => 'boolean',
                                'default' => true
                            ),
                            'sms' => array(
                                'type' => 'boolean',
                                'default' => false
                            ),
                            'push' => array(
                                'type' => 'boolean',
                                'default' => true
                            )
                        )
                    ),
                    'timezone' => array(
                        'type' => 'string',
                        'default' => 'UTC'
                    )
                )
            )
        )
    );
}
```

### Array Schema with Constraints

```php
// PHP: Array schema with constraints
function get_order_schema() {
    return array(
        '$schema' => 'http://json-schema.org/draft-04/schema#',
        'title' => 'Order',
        'type' => 'object',
        'properties' => array(
            'id' => array(
                'type' => 'integer',
                'readonly' => true
            ),
            'order_number' => array(
                'type' => 'string',
                'pattern' => '^ORD-\d{8}$',
                'readonly' => true
            ),
            'items' => array(
                'description' => 'Order items',
                'type' => 'array',
                'minItems' => 1,
                'maxItems' => 100,
                'items' => array(
                    'type' => 'object',
                    'properties' => array(
                        'product_id' => array(
                            'type' => 'integer',
                            'minimum' => 1
                        ),
                        'quantity' => array(
                            'type' => 'integer',
                            'minimum' => 1,
                            'maximum' => 999
                        ),
                        'price' => array(
                            'type' => 'number',
                            'minimum' => 0,
                            'multipleOf' => 0.01
                        ),
                        'discount' => array(
                            'type' => 'number',
                            'minimum' => 0,
                            'maximum' => 100
                        )
                    ),
                    'required' => array('product_id', 'quantity', 'price')
                )
            ),
            'shipping' => array(
                'type' => 'object',
                'properties' => array(
                    'method' => array(
                        'type' => 'string',
                        'enum' => array('standard', 'express', 'overnight')
                    ),
                    'address' => array(
                        '$ref' => '#/definitions/address'
                    )
                ),
                'required' => array('method', 'address')
            ),
            'payment' => array(
                'type' => 'object',
                'properties' => array(
                    'method' => array(
                        'type' => 'string',
                        'enum' => array('credit_card', 'paypal', 'bank_transfer')
                    ),
                    'transaction_id' => array(
                        'type' => 'string',
                        'maxLength' => 100
                    )
                ),
                'required' => array('method')
            )
        ),
        'definitions' => array(
            'address' => array(
                'type' => 'object',
                'properties' => array(
                    'street' => array('type' => 'string'),
                    'city' => array('type' => 'string'),
                    'state' => array('type' => 'string'),
                    'zip' => array('type' => 'string'),
                    'country' => array('type' => 'string')
                ),
                'required' => array('street', 'city', 'state', 'zip', 'country')
            )
        ),
        'required' => array('items', 'shipping', 'payment')
    );
}
```

## Schema Registration

### Endpoint Schema Integration

```php
// PHP: Register endpoint with schema
function register_product_endpoint() {
    register_rest_route('my-plugin/v1', '/products', array(
        'methods' => 'GET',
        'callback' => 'get_products',
        'permission_callback' => '__return_true',
        'args' => array(
            'page' => array(
                'description' => 'Current page of the collection',
                'type' => 'integer',
                'default' => 1,
                'minimum' => 1,
                'sanitize_callback' => 'absint'
            ),
            'per_page' => array(
                'description' => 'Maximum number of items to be returned',
                'type' => 'integer',
                'default' => 10,
                'minimum' => 1,
                'maximum' => 100,
                'sanitize_callback' => 'absint'
            ),
            'search' => array(
                'description' => 'Limit results to those matching a string',
                'type' => 'string',
                'sanitize_callback' => 'sanitize_text_field'
            ),
            'category' => array(
                'description' => 'Limit results to specific category',
                'type' => 'integer',
                'minimum' => 1,
                'sanitize_callback' => 'absint'
            ),
            'status' => array(
                'description' => 'Limit results to specific status',
                'type' => 'string',
                'enum' => array('active', 'inactive', 'draft'),
                'default' => 'active'
            )
        ),
        'schema' => 'get_product_schema'
    ));
    
    register_rest_route('my-plugin/v1', '/products', array(
        'methods' => 'POST',
        'callback' => 'create_product',
        'permission_callback' => 'check_user_can_create_product',
        'args' => array(
            'name' => array(
                'required' => true,
                'type' => 'string',
                'description' => 'Product name',
                'sanitize_callback' => 'sanitize_text_field',
                'validate_callback' => function($param, $request, $key) {
                    return !empty($param) && strlen($param) <= 255;
                }
            ),
            'price' => array(
                'required' => true,
                'type' => 'number',
                'description' => 'Product price',
                'minimum' => 0,
                'validate_callback' => function($param, $request, $key) {
                    return is_numeric($param) && $param >= 0;
                }
            ),
            'description' => array(
                'type' => 'string',
                'description' => 'Product description',
                'sanitize_callback' => 'wp_kses_post'
            ),
            'sku' => array(
                'type' => 'string',
                'description' => 'Product SKU',
                'pattern' => '^[A-Z0-9-]+$',
                'sanitize_callback' => 'sanitize_text_field'
            )
        ),
        'schema' => 'get_product_schema'
    ));
}
add_action('rest_api_init', 'register_product_endpoint');
```

### Schema Validation

```php
// PHP: Schema validation functions
function validate_product_schema($request) {
    $params = $request->get_params();
    $errors = array();
    
    // Validate required fields
    if (empty($params['name'])) {
        $errors['name'] = 'Product name is required';
    }
    
    if (!isset($params['price']) || !is_numeric($params['price'])) {
        $errors['price'] = 'Valid price is required';
    } elseif ($params['price'] < 0) {
        $errors['price'] = 'Price must be non-negative';
    }
    
    // Validate SKU format
    if (!empty($params['sku']) && !preg_match('/^[A-Z0-9-]+$/', $params['sku'])) {
        $errors['sku'] = 'SKU must contain only uppercase letters, numbers, and hyphens';
    }
    
    // Validate categories if provided
    if (!empty($params['categories']) && is_array($params['categories'])) {
        foreach ($params['categories'] as $index => $category) {
            if (!isset($category['id']) || !is_numeric($category['id'])) {
                $errors["categories.{$index}.id"] = 'Valid category ID required';
            }
        }
    }
    
    if (!empty($errors)) {
        return new WP_Error(
            'rest_invalid_param',
            'One or more parameters are invalid',
            array(
                'status' => 400,
                'params' => $errors
            )
        );
    }
    
    return true;
}

// Apply validation to endpoint
function create_product($request) {
    // Validate schema
    $validation_result = validate_product_schema($request);
    if (is_wp_error($validation_result)) {
        return $validation_result;
    }
    
    // Create product logic here
    $product_data = array(
        'post_title' => $request->get_param('name'),
        'post_content' => $request->get_param('description'),
        'post_status' => 'publish',
        'post_type' => 'product'
    );
    
    $product_id = wp_insert_post($product_data);
    
    if (is_wp_error($product_id)) {
        return $product_id;
    }
    
    // Save meta fields
    update_post_meta($product_id, 'price', $request->get_param('price'));
    update_post_meta($product_id, 'sku', $request->get_param('sku'));
    
    return rest_ensure_response(get_product($product_id), 201);
}
```

## Schema Documentation

### Auto-Generated Documentation

```php
// PHP: Generate schema documentation
function generate_schema_documentation($schema) {
    $doc = array(
        'title' => $schema['title'] ?? 'API Endpoint',
        'description' => $schema['description'] ?? '',
        'type' => $schema['type'] ?? 'object',
        'properties' => array()
    );
    
    if (isset($schema['properties'])) {
        foreach ($schema['properties'] as $property => $definition) {
            $doc['properties'][$property] = array(
                'type' => $definition['type'] ?? 'string',
                'description' => $definition['description'] ?? '',
                'required' => in_array($property, $schema['required'] ?? array()),
                'readonly' => $definition['readonly'] ?? false,
                'example' => $definition['example'] ?? null
            );
            
            // Add validation rules
            if (isset($definition['minimum'])) {
                $doc['properties'][$property]['minimum'] = $definition['minimum'];
            }
            if (isset($definition['maximum'])) {
                $doc['properties'][$property]['maximum'] = $definition['maximum'];
            }
            if (isset($definition['minLength'])) {
                $doc['properties'][$property]['minLength'] = $definition['minLength'];
            }
            if (isset($definition['maxLength'])) {
                $doc['properties'][$property]['maxLength'] = $definition['maxLength'];
            }
            if (isset($definition['enum'])) {
                $doc['properties'][$property]['enum'] = $definition['enum'];
            }
            if (isset($definition['pattern'])) {
                $doc['properties'][$property]['pattern'] = $definition['pattern'];
            }
        }
    }
    
    return $doc;
}

// Endpoint to get schema documentation
function get_schema_documentation($request) {
    $endpoint = $request->get_param('endpoint');
    
    // Get schema for endpoint
    $schema = get_product_schema(); // Replace with dynamic lookup
    
    return rest_ensure_response(generate_schema_documentation($schema));
}

register_rest_route('my-plugin/v1', '/schema/(?P<endpoint>[a-zA-Z0-9-]+)', array(
    'methods' => 'GET',
    'callback' => 'get_schema_documentation',
    'permission_callback' => '__return_true'
));
```

## Best Practices

### Schema Design Guidelines

```php
// PHP: Schema design best practices
function get_well_designed_schema() {
    return array(
        '$schema' => 'http://json-schema.org/draft-04/schema#',
        'title' => 'Well Designed Schema',
        'description' => 'Example of well-designed schema following best practices',
        'type' => 'object',
        
        // Always include required fields
        'required' => array('id', 'name'),
        
        // Define properties with clear descriptions
        'properties' => array(
            'id' => array(
                'description' => 'Unique identifier for the resource',
                'type' => 'integer',
                'minimum' => 1,
                'readonly' => true,
                'context' => array('view', 'edit', 'embed')
            ),
            
            // Use appropriate types
            'name' => array(
                'description' => 'Human-readable name',
                'type' => 'string',
                'minLength' => 1,
                'maxLength' => 255,
                'context' => array('view', 'edit', 'embed')
            ),
            
            // Include validation rules
            'email' => array(
                'description' => 'Email address',
                'type' => 'string',
                'format' => 'email',
                'context' => array('view', 'edit')
            ),
            
            // Use enums for limited values
            'status' => array(
                'description' => 'Current status',
                'type' => 'string',
                'enum' => array('active', 'inactive', 'pending'),
                'default' => 'pending',
                'context' => array('view', 'edit')
            ),
            
            // Include examples
            'price' => array(
                'description' => 'Price in USD',
                'type' => 'number',
                'minimum' => 0,
                'multipleOf' => 0.01,
                'example' => 19.99,
                'context' => array('view', 'edit')
            )
        ),
        
        // Prevent additional properties unless needed
        'additionalProperties' => false
    );
}
```

## Official Documentation

https://developer.wordpress.org/rest-api/extending-the-rest-api/
https://developer.wordpress.org/reference/functions/register_rest_route/
https://json-schema.org/
