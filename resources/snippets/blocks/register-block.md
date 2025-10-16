---
difficulty: Intermediate
tags: [blocks, gutenberg, registration, react]
related: [blocks/dynamic-block, blocks/block-patterns]
use_case: Creating Gutenberg blocks
---

# Register Gutenberg Block

```php
// Register block
function register_my_block() {
    register_block_type( __DIR__ . '/build' );
}
add_action( 'init', 'register_my_block' );

// block.json
{
    "apiVersion": 3,
    "name": "myplugin/my-block",
    "title": "My Custom Block",
    "category": "widgets",
    "icon": "smiley",
    "description": "A custom block",
    "supports": {
        "html": false,
        "align": true
    },
    "attributes": {
        "content": {
            "type": "string",
            "default": ""
        }
    },
    "editorScript": "file:./index.js",
    "editorStyle": "file:./editor.css",
    "style": "file:./style.css"
}
```
