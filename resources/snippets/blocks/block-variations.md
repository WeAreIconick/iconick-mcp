# Block Variations

```php
// JavaScript (in block editor)
wp.blocks.registerBlockVariation('core/group', {
    name: 'card-layout',
    title: 'Card Layout',
    description: 'A card-style group block',
    attributes: {
        className: 'card-block',
        backgroundColor: 'white'
    },
    innerBlocks: [
        ['core/heading', { level: 3 }],
        ['core/paragraph'],
        ['core/button']
    ],
    scope: ['inserter']
});

// PHP registration
function register_block_variations() {
    wp_enqueue_script(
        'my-block-variations',
        plugins_url( 'js/block-variations.js', __FILE__ ),
        array( 'wp-blocks', 'wp-dom-ready', 'wp-edit-post' ),
        '1.0.0'
    );
}
add_action( 'enqueue_block_editor_assets', 'register_block_variations' );
```
