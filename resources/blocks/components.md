# WordPress Block Editor Components

Comprehensive guide to using Block Editor components for building custom blocks.

## Core Components

### InspectorControls

```javascript
import { InspectorControls } from '@wordpress/block-editor';
import { PanelBody, TextControl, ToggleControl, RangeControl } from '@wordpress/components';

edit: ({ attributes, setAttributes }) => {
    const { title, showTitle, fontSize } = attributes;
    
    return (
        <>
            <InspectorControls>
                <PanelBody title="Block Settings" initialOpen={true}>
                    <TextControl
                        label="Title"
                        value={title}
                        onChange={(value) => setAttributes({ title: value })}
                        help="Enter the block title"
                    />
                    
                    <ToggleControl
                        label="Show Title"
                        checked={showTitle}
                        onChange={(value) => setAttributes({ showTitle: value })}
                    />
                    
                    <RangeControl
                        label="Font Size"
                        value={fontSize}
                        onChange={(value) => setAttributes({ fontSize: value })}
                        min={12}
                        max={48}
                        step={1}
                    />
                </PanelBody>
            </InspectorControls>
            
            <div {...useBlockProps()}>
                {showTitle && <h2 style={{ fontSize: fontSize + 'px' }}>{title}</h2>}
                <p>Block content goes here</p>
            </div>
        </>
    );
}
```

### BlockControls

```javascript
import { BlockControls } from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton, ToolbarDropdownMenu } from '@wordpress/components';

edit: ({ attributes, setAttributes }) => {
    const { alignment, textColor } = attributes;
    
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
                    <ToolbarButton
                        icon="editor-alignright"
                        title="Align Right"
                        onClick={() => setAttributes({ alignment: 'right' })}
                        isActive={alignment === 'right'}
                    />
                </ToolbarGroup>
                
                <ToolbarGroup>
                    <ToolbarDropdownMenu
                        icon="admin-customizer"
                        label="Text Color"
                        controls={[
                            {
                                title: 'Red',
                                onClick: () => setAttributes({ textColor: 'red' }),
                                isActive: textColor === 'red'
                            },
                            {
                                title: 'Blue',
                                onClick: () => setAttributes({ textColor: 'blue' }),
                                isActive: textColor === 'blue'
                            },
                            {
                                title: 'Green',
                                onClick: () => setAttributes({ textColor: 'green' }),
                                isActive: textColor === 'green'
                            }
                        ]}
                    />
                </ToolbarGroup>
            </BlockControls>
            
            <div 
                {...useBlockProps({ 
                    className: `align-${alignment}`,
                    style: { color: textColor }
                })}
            >
                Block content with alignment and color
            </div>
        </>
    );
}
```

## Form Components

### TextControl

```javascript
import { TextControl, TextareaControl } from '@wordpress/components';

function MyBlockEdit({ attributes, setAttributes }) {
    const { title, description } = attributes;
    
    return (
        <InspectorControls>
            <PanelBody title="Content Settings">
                <TextControl
                    label="Title"
                    value={title}
                    onChange={(value) => setAttributes({ title: value })}
                    placeholder="Enter title..."
                    help="This will be displayed as the main heading"
                />
                
                <TextareaControl
                    label="Description"
                    value={description}
                    onChange={(value) => setAttributes({ description: value })}
                    placeholder="Enter description..."
                    rows={4}
                    help="Provide a detailed description"
                />
            </PanelBody>
        </InspectorControls>
    );
}
```

### SelectControl

```javascript
import { SelectControl } from '@wordpress/components';

function LayoutSelect({ attributes, setAttributes }) {
    const { layout } = attributes;
    
    const layoutOptions = [
        { label: 'Grid', value: 'grid' },
        { label: 'List', value: 'list' },
        { label: 'Carousel', value: 'carousel' },
        { label: 'Masonry', value: 'masonry' }
    ];
    
    return (
        <SelectControl
            label="Layout Style"
            value={layout}
            options={layoutOptions}
            onChange={(value) => setAttributes({ layout: value })}
            help="Choose how content should be displayed"
        />
    );
}
```

### ToggleControl and CheckboxControl

```javascript
import { ToggleControl, CheckboxControl } from '@wordpress/components';

function DisplayOptions({ attributes, setAttributes }) {
    const { showTitle, showExcerpt, showDate, showAuthor } = attributes;
    
    return (
        <PanelBody title="Display Options">
            <ToggleControl
                label="Show Title"
                checked={showTitle}
                onChange={(value) => setAttributes({ showTitle: value })}
            />
            
            <ToggleControl
                label="Show Excerpt"
                checked={showExcerpt}
                onChange={(value) => setAttributes({ showExcerpt: value })}
            />
            
            <div className="checkbox-group">
                <CheckboxControl
                    label="Show Date"
                    checked={showDate}
                    onChange={(value) => setAttributes({ showDate: value })}
                />
                
                <CheckboxControl
                    label="Show Author"
                    checked={showAuthor}
                    onChange={(value) => setAttributes({ showAuthor: value })}
                />
            </div>
        </PanelBody>
    );
}
```

### RangeControl

```javascript
import { RangeControl } from '@wordpress/components';

function SpacingControls({ attributes, setAttributes }) {
    const { padding, margin, fontSize } = attributes;
    
    return (
        <PanelBody title="Spacing & Sizing">
            <RangeControl
                label="Padding"
                value={padding}
                onChange={(value) => setAttributes({ padding: value })}
                min={0}
                max={100}
                step={5}
                help="Internal spacing"
            />
            
            <RangeControl
                label="Margin"
                value={margin}
                onChange={(value) => setAttributes({ margin: value })}
                min={0}
                max={100}
                step={5}
                help="External spacing"
            />
            
            <RangeControl
                label="Font Size"
                value={fontSize}
                onChange={(value) => setAttributes({ fontSize: value })}
                min={12}
                max={72}
                step={1}
                help="Text size in pixels"
            />
        </PanelBody>
    );
}
```

## Color and Style Components

### ColorPalette

```javascript
import { ColorPalette } from '@wordpress/block-editor';

function ColorSettings({ attributes, setAttributes }) {
    const { backgroundColor, textColor } = attributes;
    
    return (
        <PanelBody title="Colors">
            <p>
                <strong>Background Color</strong>
            </p>
            <ColorPalette
                value={backgroundColor}
                onChange={(value) => setAttributes({ backgroundColor: value })}
                disableCustomColors={false}
            />
            
            <p>
                <strong>Text Color</strong>
            </p>
            <ColorPalette
                value={textColor}
                onChange={(value) => setAttributes({ textColor: value })}
                disableCustomColors={false}
            />
        </PanelBody>
    );
}
```

### FontSizePicker

```javascript
import { FontSizePicker } from '@wordpress/block-editor';

function TypographySettings({ attributes, setAttributes }) {
    const { fontSize } = attributes;
    
    const fontSizes = [
        { name: 'Small', size: 14, slug: 'small' },
        { name: 'Medium', size: 16, slug: 'medium' },
        { name: 'Large', size: 20, slug: 'large' },
        { name: 'Extra Large', size: 24, slug: 'extra-large' }
    ];
    
    return (
        <PanelBody title="Typography">
            <FontSizePicker
                value={fontSize}
                onChange={(value) => setAttributes({ fontSize: value })}
                fontSizes={fontSizes}
                withSlider={true}
            />
        </PanelBody>
    );
}
```

## Media Components

### MediaUpload

```javascript
import { MediaUpload, MediaUploadCheck } from '@wordpress/block-editor';

function ImageUpload({ attributes, setAttributes }) {
    const { imageId, imageUrl } = attributes;
    
    const onSelectImage = (media) => {
        setAttributes({
            imageId: media.id,
            imageUrl: media.url,
            imageAlt: media.alt
        });
    };
    
    return (
        <MediaUploadCheck>
            <MediaUpload
                onSelect={onSelectImage}
                allowedTypes={['image']}
                value={imageId}
                render={({ open }) => (
                    <div className="image-upload">
                        {imageUrl ? (
                            <div className="image-preview">
                                <img src={imageUrl} alt="Preview" />
                                <button 
                                    className="remove-image"
                                    onClick={() => setAttributes({ imageId: null, imageUrl: '' })}
                                >
                                    Remove
                                </button>
                            </div>
                        ) : (
                            <button 
                                className="upload-button"
                                onClick={open}
                            >
                                Upload Image
                            </button>
                        )}
                    </div>
                )}
            />
        </MediaUploadCheck>
    );
}
```

### URLInput

```javascript
import { URLInput } from '@wordpress/block-editor';

function LinkSettings({ attributes, setAttributes }) {
    const { linkUrl, linkText } = attributes;
    
    return (
        <PanelBody title="Link Settings">
            <TextControl
                label="Link Text"
                value={linkText}
                onChange={(value) => setAttributes({ linkText: value })}
            />
            
            <URLInput
                value={linkUrl}
                onChange={(value) => setAttributes({ linkUrl: value })}
                placeholder="Enter URL..."
            />
        </PanelBody>
    );
}
```

## Advanced Components

### ServerSideRender

```javascript
import ServerSideRender from '@wordpress/server-side-render';

registerBlockType('my-plugin/dynamic-block', {
    edit: ({ attributes, setAttributes }) => {
        return (
            <>
                <InspectorControls>
                    <PanelBody title="Settings">
                        <TextControl
                            label="Custom Parameter"
                            value={attributes.param}
                            onChange={(value) => setAttributes({ param: value })}
                        />
                    </PanelBody>
                </InspectorControls>
                
                <div {...useBlockProps()}>
                    <ServerSideRender
                        block="my-plugin/dynamic-block"
                        attributes={attributes}
                        LoadingResponsePlaceholder={() => (
                            <div>Loading...</div>
                        )}
                        ErrorResponsePlaceholder={({ response }) => (
                            <div>Error: {response.message}</div>
                        )}
                    />
                </div>
            </>
        );
    },
    save: () => null // Dynamic block
});
```

### InnerBlocks

```javascript
import { InnerBlocks } from '@wordpress/block-editor';

registerBlockType('my-plugin/container-block', {
    edit: () => {
        const ALLOWED_BLOCKS = [
            'core/paragraph',
            'core/heading',
            'core/image',
            'core/list'
        ];
        
        const TEMPLATE = [
            ['core/heading', { level: 2, placeholder: 'Enter title...' }],
            ['core/paragraph', { placeholder: 'Enter content...' }]
        ];
        
        return (
            <div {...useBlockProps()}>
                <InnerBlocks
                    allowedBlocks={ALLOWED_BLOCKS}
                    template={TEMPLATE}
                    templateLock="all" // or "insert" or false
                    orientation="vertical"
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

## Component Composition Patterns

### Reusable Component Groups

```javascript
// Create reusable component groups
function ContentSettings({ attributes, setAttributes }) {
    return (
        <PanelBody title="Content Settings">
            <TextControl
                label="Title"
                value={attributes.title}
                onChange={(value) => setAttributes({ title: value })}
            />
            <TextareaControl
                label="Description"
                value={attributes.description}
                onChange={(value) => setAttributes({ description: value })}
            />
        </PanelBody>
    );
}

function StyleSettings({ attributes, setAttributes }) {
    return (
        <PanelBody title="Style Settings">
            <ColorPalette
                value={attributes.backgroundColor}
                onChange={(value) => setAttributes({ backgroundColor: value })}
            />
            <RangeControl
                label="Padding"
                value={attributes.padding}
                onChange={(value) => setAttributes({ padding: value })}
                min={0}
                max={100}
            />
        </PanelBody>
    );
}

// Use in block edit function
edit: ({ attributes, setAttributes }) => {
    return (
        <>
            <InspectorControls>
                <ContentSettings attributes={attributes} setAttributes={setAttributes} />
                <StyleSettings attributes={attributes} setAttributes={setAttributes} />
            </InspectorControls>
            
            <div {...useBlockProps()}>
                {/* Block content */}
            </div>
        </>
    );
}
```

### Conditional Rendering

```javascript
function ConditionalControls({ attributes, setAttributes }) {
    const { showAdvanced, advancedSettings } = attributes;
    
    return (
        <PanelBody title="Settings">
            <ToggleControl
                label="Show Advanced Settings"
                checked={showAdvanced}
                onChange={(value) => setAttributes({ showAdvanced: value })}
            />
            
            {showAdvanced && (
                <>
                    <TextControl
                        label="Advanced Option 1"
                        value={advancedSettings.option1}
                        onChange={(value) => setAttributes({
                            advancedSettings: {
                                ...advancedSettings,
                                option1: value
                            }
                        })}
                    />
                    <TextControl
                        label="Advanced Option 2"
                        value={advancedSettings.option2}
                        onChange={(value) => setAttributes({
                            advancedSettings: {
                                ...advancedSettings,
                                option2: value
                            }
                        })}
                    />
                </>
            )}
        </PanelBody>
    );
}
```

## Best Practices

### Performance Optimization

```javascript
// Use useCallback for expensive operations
import { useCallback } from '@wordpress/element';

function OptimizedBlockEdit({ attributes, setAttributes }) {
    const handleAttributeChange = useCallback((key, value) => {
        setAttributes({ [key]: value });
    }, [setAttributes]);
    
    return (
        <InspectorControls>
            <TextControl
                label="Title"
                value={attributes.title}
                onChange={(value) => handleAttributeChange('title', value)}
            />
        </InspectorControls>
    );
}
```

### Accessibility

```javascript
function AccessibleControls({ attributes, setAttributes }) {
    return (
        <PanelBody title="Settings">
            <TextControl
                label="Title"
                value={attributes.title}
                onChange={(value) => setAttributes({ title: value })}
                help="This title will be used for screen readers"
                aria-describedby="title-help"
            />
            
            <ToggleControl
                label="Enable Feature"
                checked={attributes.enabled}
                onChange={(value) => setAttributes({ enabled: value })}
                help="Toggle this feature on or off"
            />
        </PanelBody>
    );
}
```

## Official Documentation

https://developer.wordpress.org/block-editor/reference-guides/components/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-edit-save/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-supports/
