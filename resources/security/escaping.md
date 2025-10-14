# WordPress Output Escaping

Escaping makes data safe for output by encoding special characters.

## When to Escape

**ALWAYS escape data when outputting to:**
- HTML
- HTML attributes
- JavaScript
- URLs
- SQL queries (use $wpdb->prepare instead)

## Core Escaping Functions

### HTML Context

```php
// Escape HTML output
echo esc_html( $text );

// Example
<h1><?php echo esc_html( $page_title ); ?></h1>
<p><?php echo esc_html( get_the_title() ); ?></p>
```

### HTML Attributes

```php
// Escape for attributes
echo '<div class="' . esc_attr( $class_name ) . '">';
echo '<input type="text" value="' . esc_attr( $value ) . '">';

// For data attributes
<div data-id="<?php echo esc_attr( $post_id ); ?>">
```

### URLs

```php
// Escape URL
<a href="<?php echo esc_url( $link ); ?>">Link</a>

// For use in code (raw)
$redirect = esc_url_raw( $_GET['redirect_to'] );
wp_redirect( $redirect );
```

### JavaScript

```php
// Escape for JS
<script>
var data = '<?php echo esc_js( $data ); ?>';
</script>

// Better: use wp_localize_script
wp_localize_script( 'my-script', 'myData', array(
    'value' => $data, // Auto-escaped
) );
```

### SQL (Use wpdb->prepare)

```php
// ❌ NEVER

$wpdb->query( "DELETE FROM table WHERE id = " . $id );

// ✅ ALWAYS
$wpdb->query( $wpdb->prepare(
    "DELETE FROM {$wpdb->prefix}table WHERE id = %d",
    $id
) );
```

### Translation with Escaping

```php
// Escape translated text
esc_html_e( 'Hello World', 'textdomain' );
esc_attr_e( 'Placeholder', 'textdomain' );

// Return escaped translated string
$text = esc_html__( 'Hello World', 'textdomain' );
$attr = esc_attr__( 'Placeholder', 'textdomain' );
```

## Advanced Escaping

### wp_kses (Allow Specific HTML)

```php
$allowed_html = array(
    'a' => array(
        'href' => array(),
        'title' => array(),
    ),
    'br' => array(),
    'strong' => array(),
);

echo wp_kses( $content, $allowed_html );

// For post content (allows standard post HTML)
echo wp_kses_post( $content );
```

### JSON Encoding

```php
<script>
var config = <?php echo wp_json_encode( $config_array ); ?>;
</script>
```

## Context-Specific Examples

### Form Output

```php
<form method="post">
    <?php wp_nonce_field( 'my_action', 'my_nonce' ); ?>
    
    <input type="text" 
           name="title" 
           value="<?php echo esc_attr( $title ); ?>" 
           placeholder="<?php esc_attr_e( 'Enter title', 'textdomain' ); ?>">
    
    <textarea name="content"><?php echo esc_textarea( $content ); ?></textarea>
    
    <select name="category">
        <?php foreach ( $categories as $cat_id => $cat_name ) : ?>
            <option value="<?php echo esc_attr( $cat_id ); ?>"
                    <?php selected( $selected_cat, $cat_id ); ?>>
                <?php echo esc_html( $cat_name ); ?>
            </option>
        <?php endforeach; ?>
    </select>
</form>
```

### Link Output

```php
<a href="<?php echo esc_url( $external_link ); ?>" 
   target="_blank"
   rel="noopener noreferrer">
    <?php echo esc_html( $link_text ); ?>
</a>
```

### Style Attributes

```php
<div style="background-color: <?php echo esc_attr( $color ); ?>; 
            width: <?php echo esc_attr( $width ); ?>px;">
```

## Best Practices

1. **Escape late** - Escape at output, not storage
2. **Use correct function** for context (HTML vs attribute vs URL)
3. **wp_kses for rich content** - Allow specific HTML safely
4. **Never trust user data** - Even from admins
5. **Escape translation strings** - Use esc_html__(), esc_attr__()
6. **Use wp_json_encode()** for JavaScript data
7. **Don't double-escape** - Escape once at output

## Quick Reference

| Context | Function | Example |
|---------|----------|---------|
| HTML | `esc_html()` | `<p><?php echo esc_html( $text ); ?></p>` |
| Attribute | `esc_attr()` | `<div class="<?php echo esc_attr( $class ); ?>">` |
| URL | `esc_url()` | `<a href="<?php echo esc_url( $link ); ?>">` |
| JavaScript | `esc_js()` | `var x = '<?php echo esc_js( $val ); ?>';` |
| Textarea | `esc_textarea()` | `<textarea><?php echo esc_textarea( $val ); ?></textarea>` |
| Rich HTML | `wp_kses_post()` | `<?php echo wp_kses_post( $content ); ?>` |
| SQL | `$wpdb->prepare()` | `$wpdb->prepare( "... %s", $val )` |

## Official Documentation

https://developer.wordpress.org/apis/security/escaping/
https://developer.wordpress.org/reference/functions/esc_html/