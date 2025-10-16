---
difficulty: Beginner
tags: [security, escaping, output, xss]
related: [security/sanitize-input, security/nonces]
use_case: Preventing XSS attacks when displaying data
---

# Escape Output for Display

## HTML Content

```php
// Escape plain text for HTML
echo esc_html( $user_input );

// In template
<h1><?php echo esc_html( $title ); ?></h1>
<p><?php echo esc_html( $description ); ?></p>
```

## HTML Attributes

```php
// Escape for HTML attributes
echo '<div class="' . esc_attr( $class_name ) . '">';
echo '<input type="text" value="' . esc_attr( $value ) . '">';

// In template
<div class="<?php echo esc_attr( $custom_class ); ?>">
    <input type="text" name="field" value="<?php echo esc_attr( $field_value ); ?>">
</div>
```

## URLs

```php
// Escape URLs for links
echo '<a href="' . esc_url( $link ) . '">Link</a>';

// In template
<a href="<?php echo esc_url( $homepage_url ); ?>">
    <?php echo esc_html( $site_name ); ?>
</a>
```

## JavaScript

```php
// Escape for JavaScript strings
echo '<script>';
echo 'var userName = "' . esc_js( $user_name ) . '";';
echo '</script>';

// Better: Use wp_localize_script
wp_localize_script( 'my-script', 'myData', array(
    'userName' => $user_name,  // Auto-escaped
    'apiUrl' => rest_url()
));
```

## Textarea Values

```php
// Escape for textarea
echo '<textarea>' . esc_textarea( $content ) . '</textarea>';

// In template
<textarea name="bio"><?php echo esc_textarea( $user_bio ); ?></textarea>
```

## Allowed HTML (Post Content)

```php
// Allow safe HTML (like post content)
echo wp_kses_post( $content );

// Example: Display user-submitted content safely
<div class="user-content">
    <?php echo wp_kses_post( $user_submitted_html ); ?>
</div>
```

## Custom Allowed HTML

```php
// Define custom allowed tags
$allowed_html = array(
    'a' => array(
        'href' => array(),
        'title' => array(),
        'class' => array()
    ),
    'br' => array(),
    'em' => array(),
    'strong' => array(),
    'p' => array(
        'class' => array()
    )
);

echo wp_kses( $content, $allowed_html );
```

## Translation Functions with Escaping

```php
// Escape translated strings
echo esc_html__( 'Hello World', 'textdomain' );
esc_html_e( 'Welcome', 'textdomain' );

echo esc_attr__( 'Placeholder text', 'textdomain' );

// With sprintf
echo esc_html( sprintf( 
    __( 'Hello %s', 'textdomain' ),
    $user_name  // Safe: sprintf doesn't execute, esc_html protects
));
```

## Complete Examples

### Display User Profile

```php
<div class="user-profile">
    <h2><?php echo esc_html( $user->display_name ); ?></h2>
    <p><?php echo esc_html( $user->description ); ?></p>
    <a href="<?php echo esc_url( $user->user_url ); ?>">
        <?php esc_html_e( 'Visit Website', 'textdomain' ); ?>
    </a>
</div>
```

### Display Post List

```php
<?php
$posts = get_posts( array( 'post_type' => 'post', 'numberposts' => 5 ) );
foreach ( $posts as $post ) : ?>
    <article>
        <h3>
            <a href="<?php echo esc_url( get_permalink( $post->ID ) ); ?>">
                <?php echo esc_html( $post->post_title ); ?>
            </a>
        </h3>
        <div class="excerpt">
            <?php echo wp_kses_post( $post->post_excerpt ); ?>
        </div>
    </article>
<?php endforeach; ?>
```

### Admin Settings Page

```php
<div class="wrap">
    <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
    
    <form method="post" action="options.php">
        <?php
        settings_fields( 'my_options_group' );
        do_settings_sections( 'my-plugin' );
        ?>
        
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="api_key">
                        <?php esc_html_e( 'API Key', 'textdomain' ); ?>
                    </label>
                </th>
                <td>
                    <input 
                        type="text" 
                        id="api_key" 
                        name="my_options[api_key]" 
                        value="<?php echo esc_attr( $options['api_key'] ); ?>" 
                        class="regular-text"
                    >
                </td>
            </tr>
        </table>
        
        <?php submit_button(); ?>
    </form>
</div>
```

## Escaping Function Quick Reference

| Context | Function | Example |
|---------|----------|---------|
| HTML content | `esc_html()` | `<p><?php echo esc_html($text); ?></p>` |
| HTML attribute | `esc_attr()` | `<div class="<?php echo esc_attr($class); ?>">` |
| URL | `esc_url()` | `<a href="<?php echo esc_url($url); ?>">` |
| JavaScript | `esc_js()` | `var x = "<?php echo esc_js($val); ?>";` |
| Textarea | `esc_textarea()` | `<textarea><?php echo esc_textarea($val); ?></textarea>` |
| Allow HTML | `wp_kses_post()` | `<?php echo wp_kses_post($content); ?>` |
| Custom HTML | `wp_kses()` | `<?php echo wp_kses($html, $allowed); ?>` |
| SQL | `esc_sql()` | `$wpdb->prepare()` preferred |

## Common Mistakes

```php
// ❌ WRONG - Not escaped
echo $user_input;
echo "<div>" . $variable . "</div>";

// ✅ CORRECT - Properly escaped
echo esc_html( $user_input );
echo "<div>" . esc_html( $variable ) . "</div>";

// ❌ WRONG - Double escaping
echo esc_html( esc_html( $text ) );

// ✅ CORRECT - Escape once at output
echo esc_html( $text );

// ❌ WRONG - Wrong context
echo '<a href="' . esc_html( $url ) . '">Link</a>';

// ✅ CORRECT - Right function for context
echo '<a href="' . esc_url( $url ) . '">Link</a>';
```

## Security Rules

1. **Escape ALL output** - No exceptions
2. **Right function for context** - HTML, attribute, URL, JS
3. **Escape late** - As close to output as possible
4. **One escape per output** - Don't double-escape
5. **Sanitize on input, escape on output** - Two different purposes

