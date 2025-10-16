---
difficulty: Intermediate
tags: [blocks, registration, gutenberg, api]
related: [blocks/gutenberg-basics, blocks/block-patterns]
wp_version: 5.0+
---

# WordPress Block Registration

Creating custom blocks for the WordPress Block Editor (Gutenberg).

## Basic Block Registration

### JavaScript Block Registration

```javascript
// register-block.js
import { registerBlockType } from '@wordpress/blocks';
import { useBlockProps } from '@wordpress/block-editor';

registerBlockType('my-plugin/my-block', {
    title: 'My Custom Block',
    icon: 'smiley',
    category: 'common',
    attributes: {
        content: {
            type: 'string',
            default: 'Hello, World!'
        }
    },
    edit: ({ attributes, setAttributes }) => {
        return (
            <div {...useBlockProps()}>
                <input
                    value={attributes.content}
                    onChange={(e) => setAttributes({ content: e.target.value })}
                />
            </div>
        );
    },
    save: ({ attributes }) => {
        return (
            <div {...useBlockProps.save()}>
                {attributes.content}
            </div>
        );
    }
});
```

### Block.json Registration

```json
{
    "$schema": "https://schemas.wp.org/trunk/block.json",
    "apiVersion": 3,
    "name": "my-plugin/my-block",
    "version": "1.0.0",
    "title": "My Custom Block",
    "category": "common",
    "icon": "smiley",
    "description": "A custom block example",
    "keywords": ["custom", "example"],
    "textdomain": "my-plugin",
    "editorScript": "file:./build/index.js",
    "editorStyle": "file:./build/index.css",
    "style": "file:./build/style-index.css",
    "attributes": {
        "content": {
            "type": "string",
            "default": "Hello, World!"
        }
    },
    "supports": {
        "html": false,
        "align": true,
        "spacing": {
            "margin": true,
            "padding": true
        }
    },
    "providesContext": {
        "my-plugin/theme": "theme"
    },
    "usesContext": ["postId", "postType"]
}
```

### PHP Block Registration

```php
// Register block in PHP
function register_my_block() {
    register_block_type( __DIR__ . '/blocks/my-block' );
}
add_action( 'init', 'register_my_block' );

// Or register with custom data
function register_my_block_with_data() {
    register_block_type( 'my-plugin/my-block', array(
        'attributes' => array(
            'content' => array(
                'type' => 'string',
                'default' => 'Hello, World!'
            )
        ),
        'render_callback' => 'render_my_block'
    ) );
}
add_action( 'init', 'register_my_block_with_data' );
```

## Block Attributes

### Attribute Types

```javascript
attributes: {
    // String
    title: {
        type: 'string',
        default: 'Default Title'
    },
    
    // Number
    count: {
        type: 'number',
        default: 5
    },
    
    // Boolean
    showTitle: {
        type: 'boolean',
        default: true
    },
    
    // Array
    items: {
        type: 'array',
        default: []
    },
    
    // Object
    settings: {
        type: 'object',
        default: {
            color: 'blue',
            size: 'medium'
        }
    },
    
    // HTML
    content: {
        type: 'string',
        source: 'html',
        selector: '.content'
    },
    
    // Text
    excerpt: {
        type: 'string',
        source: 'text',
        selector: '.excerpt'
    },
    
    // Attribute
    className: {
        type: 'string',
        source: 'attribute',
        attribute: 'class',
        selector: 'div'
    },
    
    // Children
    children: {
        type: 'array',
        source: 'children',
        selector: '.content'
    },
    
    // Query
    posts: {
        type: 'array',
        query: {
            perPage: {
                type: 'number',
                default: 10
            },
            categories: {
                type: 'array',
                default: []
            }
        }
    }
}
```

### Attribute Sources

```javascript
// HTML source
title: {
    type: 'string',
    source: 'html',
    selector: 'h2.title'
},

// Attribute source
linkUrl: {
    type: 'string',
    source: 'attribute',
    attribute: 'href',
    selector: 'a'
},

// Text source
excerpt: {
    type: 'string',
    source: 'text',
    selector: '.excerpt'
},

// Children source
content: {
    type: 'array',
    source: 'children',
    selector: '.content'
}
```

## Block Editor Components

### InspectorControls

```javascript
import { InspectorControls } from '@wordpress/block-editor';
import { PanelBody, TextControl, ToggleControl } from '@wordpress/components';

edit: ({ attributes, setAttributes }) => {
    const { title, showTitle } = attributes;
    
    return (
        <>
            <InspectorControls>
                <PanelBody title="Settings">
                    <TextControl
                        label="Title"
                        value={title}
                        onChange={(value) => setAttributes({ title: value })}
                    />
                    <ToggleControl
                        label="Show Title"
                        checked={showTitle}
                        onChange={(value) => setAttributes({ showTitle: value })}
                    />
                </PanelBody>
            </InspectorControls>
            
            <div {...useBlockProps()}>
                {showTitle && <h2>{title}</h2>}
                <p>Block content goes here</p>
            </div>
        </>
    );
}
```

### BlockControls

```javascript
import { BlockControls } from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';

edit: ({ attributes, setAttributes }) => {
    const { alignment } = attributes;
    
    return (
        <>
            <BlockControls>
                <ToolbarGroup>
                    <ToolbarButton
                        icon="editor-alignleft"
                        title="Align Left"
                        onClick={() => setAttributes({ alignment: 'left' })}
                        isActive={alignment === 'left'}
                    />
                    <ToolbarButton
                        icon="editor-aligncenter"
                        title="Align Center"
                        onClick={() => setAttributes({ alignment: 'center' })}
                        isActive={alignment === 'center'}
                    />
                </ToolbarGroup>
            </BlockControls>
            
            <div {...useBlockProps({ className: `align-${alignment}` })}>
                Block content
            </div>
        </>
    );
}
```

## Dynamic Blocks

### Server-Side Rendering

```php
// PHP render callback
function render_my_dynamic_block( $attributes, $content ) {
    $title = $attributes['title'] ?? 'Default Title';
    $count = $attributes['count'] ?? 5;
    
    // Query posts
    $posts = get_posts( array(
        'posts_per_page' => $count,
        'post_status' => 'publish'
    ) );
    
    ob_start();
    ?>
    <div class="my-dynamic-block">
        <h2><?php echo esc_html( $title ); ?></h2>
        <ul>
            <?php foreach ( $posts as $post ) : ?>
                <li>
                    <a href="<?php echo get_permalink( $post->ID ); ?>">
                        <?php echo esc_html( $post->post_title ); ?>
                    </a>
                </li>
            <?php endforeach; ?>
        </ul>
    </div>
    <?php
    return ob_get_clean();
}

// Register dynamic block
register_block_type( 'my-plugin/dynamic-block', array(
    'render_callback' => 'render_my_dynamic_block'
) );
```

### JavaScript Dynamic Block

```javascript
// Dynamic block with server-side rendering
registerBlockType('my-plugin/dynamic-block', {
    edit: ({ attributes }) => {
        return (
            <div {...useBlockProps()}>
                <p>This block renders dynamically on the frontend</p>
                <p>Title: {attributes.title}</p>
            </div>
        );
    },
    save: () => {
        return null; // Return null for dynamic blocks
    }
});
```

## Block Patterns

### Register Block Pattern

```php
// Register block pattern
function register_my_pattern() {
    register_block_pattern(
        'my-plugin/hero-section',
        array(
            'title' => 'Hero Section',
            'description' => 'A hero section with title and button',
            'content' => '<!-- wp:group {"className":"hero-section"} -->
<div class="wp-block-group hero-section"><!-- wp:heading {"level":1,"className":"hero-title"} -->
<h1 class="hero-title">Welcome to Our Site</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"hero-description"} -->
<p class="hero-description">This is a sample hero section pattern.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons -->
<div class="wp-block-buttons"><!-- wp:button {"className":"hero-button"} -->
<div class="wp-block-button hero-button"><a class="wp-block-button__link">Get Started</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div>
<!-- /wp:group -->',
            'categories' => array( 'hero' ),
            'keywords' => array( 'hero', 'section', 'welcome' )
        )
    );
}
add_action( 'init', 'register_my_pattern' );
```

## Block Variations

### Create Block Variation

```javascript
// Add variation to existing block
import { addFilter } from '@wordpress/hooks';

addFilter(
    'blocks.registerBlockType',
    'my-plugin/add-button-variations',
    (settings, name) => {
        if (name === 'core/button') {
            return {
                ...settings,
                variations: [
                    ...settings.variations,
                    {
                        name: 'primary-button',
                        title: 'Primary Button',
                        description: 'A primary action button',
                        attributes: {
                            className: 'is-style-primary'
                        },
                        scope: ['block']
                    }
                ]
            };
        }
        return settings;
    }
);
```

## InnerBlocks

### Using InnerBlocks

```javascript
import { InnerBlocks } from '@wordpress/block-editor';

registerBlockType('my-plugin/container-block', {
    edit: () => {
        const ALLOWED_BLOCKS = ['core/paragraph', 'core/heading', 'core/image'];
        const TEMPLATE = [
            ['core/heading', { level: 2, placeholder: 'Enter title...' }],
            ['core/paragraph', { placeholder: 'Enter content...' }]
        ];
        
        return (
            <div {...useBlockProps()}>
                <InnerBlocks
                    allowedBlocks={ALLOWED_BLOCKS}
                    template={TEMPLATE}
                    templateLock="all"
                />
            </div>
        );
    },
    save: () => {
        return (
            <div {...useBlockProps.save()}>
                <InnerBlocks.Content />
            </div>
        );
    }
});
```

## Best Practices

### Performance

```javascript
// Use useMemo for expensive calculations
import { useMemo } from '@wordpress/element';

edit: ({ attributes }) => {
    const processedData = useMemo(() => {
        return expensiveCalculation(attributes.data);
    }, [attributes.data]);
    
    return <div>{processedData}</div>;
};
```

### Accessibility

```javascript
// Include proper ARIA labels and roles
edit: ({ attributes }) => {
    return (
        <div 
            {...useBlockProps({ 
                role: 'region',
                'aria-label': 'Custom block content'
            })}
        >
            <h2 id="block-title">Block Title</h2>
            <div aria-labelledby="block-title">
                Block content
            </div>
        </div>
    );
};
```

## Official Documentation

https://developer.wordpress.org/block-editor/reference-guides/block-api/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-registration/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-attributes/
