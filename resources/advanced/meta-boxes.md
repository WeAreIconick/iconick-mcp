---
difficulty: Intermediate
tags: [meta-boxes, custom-fields, admin, ui]
related: [advanced/custom-post-types, core/database-api]
wp_version: 2.5+
---

# WordPress Meta Boxes

## Basic Meta Box Creation

```php
function add_custom_meta_box() {
    add_meta_box(
        'custom_meta_box',           // Meta box ID
        'Custom Meta Box',           // Meta box title
        'custom_meta_box_callback',  // Callback function
        'post',                      // Post type
        'normal',                    // Context (normal, side, advanced)
        'high'                       // Priority (high, core, default, low)
    );
}
add_action('add_meta_boxes', 'add_custom_meta_box');

function custom_meta_box_callback($post) {
    // Add nonce field for security
    wp_nonce_field('custom_meta_box', 'custom_meta_box_nonce');
    
    // Get existing meta values
    $custom_field = get_post_meta($post->ID, '_custom_field', true);
    ?>
    <table class="form-table">
        <tr>
            <th><label for="custom_field">Custom Field</label></th>
            <td><input type="text" id="custom_field" name="custom_field" value="<?php echo esc_attr($custom_field); ?>" /></td>
        </tr>
    </table>
    <?php
}
```

## Advanced Meta Box with Multiple Fields

```php
class AdvancedMetaBox {
    private $fields = array(
        'text_field' => 'Text Field',
        'textarea_field' => 'Textarea Field',
        'select_field' => 'Select Field',
        'checkbox_field' => 'Checkbox Field',
        'radio_field' => 'Radio Field',
        'date_field' => 'Date Field',
        'color_field' => 'Color Field',
        'number_field' => 'Number Field'
    );

    public function __construct() {
        add_action('add_meta_boxes', array($this, 'add_meta_box'));
        add_action('save_post', array($this, 'save_meta_box'));
    }

    public function add_meta_box() {
        add_meta_box(
            'advanced_meta_box',
            'Advanced Meta Box',
            array($this, 'render_meta_box'),
            array('post', 'page'),
            'normal',
            'high'
        );
    }

    public function render_meta_box($post) {
        wp_nonce_field('advanced_meta_box', 'advanced_meta_box_nonce');
        
        echo '<div class="meta-box-container">';
        
        // Text Field
        $text_value = get_post_meta($post->ID, '_text_field', true);
        echo '<p>';
        echo '<label for="text_field"><strong>Text Field:</strong></label><br>';
        echo '<input type="text" id="text_field" name="text_field" value="' . esc_attr($text_value) . '" class="widefat" />';
        echo '</p>';

        // Textarea Field
        $textarea_value = get_post_meta($post->ID, '_textarea_field', true);
        echo '<p>';
        echo '<label for="textarea_field"><strong>Textarea Field:</strong></label><br>';
        echo '<textarea id="textarea_field" name="textarea_field" rows="4" class="widefat">' . esc_textarea($textarea_value) . '</textarea>';
        echo '</p>';

        // Select Field
        $select_value = get_post_meta($post->ID, '_select_field', true);
        $options = array('option1' => 'Option 1', 'option2' => 'Option 2', 'option3' => 'Option 3');
        echo '<p>';
        echo '<label for="select_field"><strong>Select Field:</strong></label><br>';
        echo '<select id="select_field" name="select_field" class="widefat">';
        echo '<option value="">Choose an option</option>';
        foreach ($options as $value => $label) {
            $selected = selected($select_value, $value, false);
            echo '<option value="' . esc_attr($value) . '" ' . $selected . '>' . esc_html($label) . '</option>';
        }
        echo '</select>';
        echo '</p>';

        // Checkbox Field
        $checkbox_value = get_post_meta($post->ID, '_checkbox_field', true);
        $checked = checked($checkbox_value, '1', false);
        echo '<p>';
        echo '<label for="checkbox_field">';
        echo '<input type="checkbox" id="checkbox_field" name="checkbox_field" value="1" ' . $checked . ' />';
        echo ' Checkbox Field';
        echo '</label>';
        echo '</p>';

        // Radio Fields
        $radio_value = get_post_meta($post->ID, '_radio_field', true);
        $radio_options = array('radio1' => 'Radio Option 1', 'radio2' => 'Radio Option 2');
        echo '<p>';
        echo '<label><strong>Radio Field:</strong></label><br>';
        foreach ($radio_options as $value => $label) {
            $checked = checked($radio_value, $value, false);
            echo '<label>';
            echo '<input type="radio" name="radio_field" value="' . esc_attr($value) . '" ' . $checked . ' />';
            echo ' ' . esc_html($label);
            echo '</label><br>';
        }
        echo '</p>';

        // Date Field
        $date_value = get_post_meta($post->ID, '_date_field', true);
        echo '<p>';
        echo '<label for="date_field"><strong>Date Field:</strong></label><br>';
        echo '<input type="date" id="date_field" name="date_field" value="' . esc_attr($date_value) . '" class="widefat" />';
        echo '</p>';

        // Color Field
        $color_value = get_post_meta($post->ID, '_color_field', true);
        echo '<p>';
        echo '<label for="color_field"><strong>Color Field:</strong></label><br>';
        echo '<input type="color" id="color_field" name="color_field" value="' . esc_attr($color_value) . '" />';
        echo '</p>';

        // Number Field
        $number_value = get_post_meta($post->ID, '_number_field', true);
        echo '<p>';
        echo '<label for="number_field"><strong>Number Field:</strong></label><br>';
        echo '<input type="number" id="number_field" name="number_field" value="' . esc_attr($number_value) . '" min="0" max="100" class="widefat" />';
        echo '</p>';

        echo '</div>';
    }

    public function save_meta_box($post_id) {
        // Security checks
        if (!isset($_POST['advanced_meta_box_nonce']) || 
            !wp_verify_nonce($_POST['advanced_meta_box_nonce'], 'advanced_meta_box')) {
            return;
        }

        if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) {
            return;
        }

        if (!current_user_can('edit_post', $post_id)) {
            return;
        }

        // Save each field
        $fields = array_keys($this->fields);
        
        foreach ($fields as $field) {
            if (isset($_POST[$field])) {
                $value = $_POST[$field];
                
                // Sanitize based on field type
                switch ($field) {
                    case 'text_field':
                    case 'select_field':
                    case 'radio_field':
                    case 'date_field':
                    case 'color_field':
                        $value = sanitize_text_field($value);
                        break;
                    case 'textarea_field':
                        $value = sanitize_textarea_field($value);
                        break;
                    case 'number_field':
                        $value = absint($value);
                        break;
                    case 'checkbox_field':
                        $value = isset($_POST[$field]) ? '1' : '0';
                        break;
                }
                
                update_post_meta($post_id, '_' . $field, $value);
            } else {
                // Handle unchecked checkboxes
                if ($field === 'checkbox_field') {
                    update_post_meta($post_id, '_' . $field, '0');
                }
            }
        }
    }
}

new AdvancedMetaBox();
```

## Conditional Meta Boxes

```php
function conditional_meta_box() {
    // Only show on specific post types
    $screen = get_current_screen();
    if ($screen->post_type === 'product') {
        add_meta_box(
            'product_details',
            'Product Details',
            'product_details_callback',
            'product',
            'normal',
            'high'
        );
    }
}
add_action('add_meta_boxes', 'conditional_meta_box');

function product_details_callback($post) {
    // Only show if post is published
    if ($post->post_status === 'publish') {
        echo '<p>This meta box only appears for published products.</p>';
        
        $price = get_post_meta($post->ID, '_product_price', true);
        echo '<p>Current Price: $' . esc_html($price) . '</p>';
    } else {
        echo '<p>Publish the post to see product details.</p>';
    }
}
```

## Meta Box with AJAX

```php
class AjaxMetaBox {
    public function __construct() {
        add_action('add_meta_boxes', array($this, 'add_meta_box'));
        add_action('save_post', array($this, 'save_meta_box'));
        add_action('wp_ajax_get_meta_data', array($this, 'ajax_get_meta_data'));
        add_action('admin_enqueue_scripts', array($this, 'enqueue_scripts'));
    }

    public function add_meta_box() {
        add_meta_box(
            'ajax_meta_box',
            'AJAX Meta Box',
            array($this, 'render_meta_box'),
            'post'
        );
    }

    public function render_meta_box($post) {
        wp_nonce_field('ajax_meta_box', 'ajax_meta_box_nonce');
        ?>
        <div id="ajax-meta-box">
            <button type="button" id="load-data" class="button">Load Data</button>
            <div id="meta-data-container"></div>
            
            <script>
            jQuery(document).ready(function($) {
                $('#load-data').click(function() {
                    var postId = <?php echo $post->ID; ?>;
                    
                    $.ajax({
                        url: ajaxurl,
                        type: 'POST',
                        data: {
                            action: 'get_meta_data',
                            post_id: postId,
                            nonce: '<?php echo wp_create_nonce('ajax_meta_box'); ?>'
                        },
                        success: function(response) {
                            $('#meta-data-container').html(response.data);
                        }
                    });
                });
            });
            </script>
        </div>
        <?php
    }

    public function ajax_get_meta_data() {
        check_ajax_referer('ajax_meta_box', 'nonce');
        
        $post_id = intval($_POST['post_id']);
        $meta_data = get_post_meta($post_id);
        
        wp_send_json_success('<pre>' . print_r($meta_data, true) . '</pre>');
    }

    public function enqueue_scripts() {
        wp_enqueue_script('jquery');
    }

    public function save_meta_box($post_id) {
        // Save logic here
    }
}

new AjaxMetaBox();
```

## Best Practices

1. **Always use nonces** for security
2. **Sanitize all input** based on expected data type
3. **Validate user capabilities** before saving
4. **Use descriptive field names** and labels
5. **Handle autosave** appropriately
6. **Use conditional logic** to show/hide fields
7. **Implement AJAX** for dynamic content
8. **Style your meta boxes** for better UX
9. **Group related fields** logically
10. **Test with different user roles**

## Resources

- [WordPress Meta Boxes Documentation](https://developer.wordpress.org/plugins/metadata/custom-meta-boxes/)
- [WordPress Nonces Documentation](https://developer.wordpress.org/plugins/security/nonces/)
- [WordPress Capabilities Documentation](https://developer.wordpress.org/plugins/users/roles-and-capabilities/)