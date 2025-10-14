# WordPress @wordpress Packages

The @wordpress packages provide essential utilities and components for building WordPress blocks and applications.

## Core @wordpress Packages

### @wordpress/blocks

Essential block utilities and registration functions.

```javascript
// JavaScript: Using @wordpress/blocks
import { registerBlockType, createBlock } from '@wordpress/blocks';
import { useBlockProps } from '@wordpress/block-editor';

registerBlockType('my-plugin/example-block', {
    title: 'Example Block',
    icon: 'smiley',
    category: 'widgets',
    
    edit: ({ attributes, setAttributes }) => {
        const blockProps = useBlockProps();
        
        return (
            <div {...blockProps}>
                <p>Example Block Content</p>
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const blockProps = useBlockProps.save();
        
        return (
            <div {...blockProps}>
                <p>Example Block Content</p>
            </div>
        );
    }
});

// Creating blocks programmatically
const newBlock = createBlock('my-plugin/example-block', {
    content: 'Hello World'
});
```

### @wordpress/components

UI components for building block interfaces.

```javascript
// JavaScript: Using @wordpress/components
import { 
    Button, 
    TextControl, 
    SelectControl, 
    ToggleControl,
    PanelBody,
    InspectorControls,
    RangeControl,
    ColorPicker,
    MediaUpload,
    MediaUploadCheck
} from '@wordpress/components';

registerBlockType('my-plugin/media-block', {
    title: 'Media Block',
    icon: 'format-image',
    category: 'media',
    
    attributes: {
        mediaId: {
            type: 'number',
            default: 0
        },
        mediaUrl: {
            type: 'string',
            default: ''
        },
        title: {
            type: 'string',
            default: ''
        },
        showTitle: {
            type: 'boolean',
            default: true
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { mediaId, mediaUrl, title, showTitle } = attributes;
        
        const onSelectMedia = (media) => {
            setAttributes({
                mediaId: media.id,
                mediaUrl: media.url,
                title: media.title
            });
        };
        
        return (
            <>
                <InspectorControls>
                    <PanelBody title="Media Settings">
                        <ToggleControl
                            label="Show Title"
                            checked={showTitle}
                            onChange={(value) => setAttributes({ showTitle: value })}
                        />
                        
                        <MediaUploadCheck>
                            <MediaUpload
                                onSelect={onSelectMedia}
                                allowedTypes={['image']}
                                value={mediaId}
                                render={({ open }) => (
                                    <Button onClick={open}>
                                        {mediaId ? 'Change Image' : 'Select Image'}
                                    </Button>
                                )}
                            />
                        </MediaUploadCheck>
                        
                        {mediaId && (
                            <Button 
                                onClick={() => setAttributes({ mediaId: 0, mediaUrl: '', title: '' })}
                                isDestructive
                            >
                                Remove Image
                            </Button>
                        )}
                    </PanelBody>
                </InspectorControls>
                
                <div className="media-block">
                    {mediaUrl ? (
                        <>
                            <img src={mediaUrl} alt={title} />
                            {showTitle && title && <p className="media-title">{title}</p>}
                        </>
                    ) : (
                        <div className="media-placeholder">
                            <p>No image selected</p>
                            <MediaUploadCheck>
                                <MediaUpload
                                    onSelect={onSelectMedia}
                                    allowedTypes={['image']}
                                    render={({ open }) => (
                                        <Button onClick={open}>Select Image</Button>
                                    )}
                                />
                            </MediaUploadCheck>
                        </div>
                    )}
                </div>
            </>
        );
    },
    
    save: ({ attributes }) => {
        const { mediaUrl, title, showTitle } = attributes;
        
        return (
            <div className="media-block">
                {mediaUrl && (
                    <>
                        <img src={mediaUrl} alt={title} />
                        {showTitle && title && <p className="media-title">{title}</p>}
                    </>
                )}
            </div>
        );
    }
});
```

### @wordpress/data

State management and data access utilities.

```javascript
// JavaScript: Using @wordpress/data
import { useSelect, useDispatch } from '@wordpress/data';
import { store as editorStore } from '@wordpress/editor';

registerBlockType('my-plugin/post-meta-block', {
    title: 'Post Meta Block',
    icon: 'info',
    category: 'widgets',
    
    attributes: {
        metaKey: {
            type: 'string',
            default: ''
        },
        showLabel: {
            type: 'boolean',
            default: true
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { metaKey, showLabel } = attributes;
        
        // Get current post data
        const { post, meta } = useSelect((select) => {
            const { getCurrentPost, getEditedPostAttribute } = select(editorStore);
            const post = getCurrentPost();
            
            return {
                post: post,
                meta: post ? getEditedPostAttribute('meta') : {}
            };
        }, []);
        
        // Get available meta keys
        const availableMetaKeys = useSelect((select) => {
            const { getCurrentPost } = select(editorStore);
            const post = getCurrentPost();
            return post ? Object.keys(post.meta || {}) : [];
        }, []);
        
        const metaValue = metaKey ? meta[metaKey] : '';
        
        return (
            <>
                <InspectorControls>
                    <PanelBody title="Meta Settings">
                        <SelectControl
                            label="Meta Key"
                            value={metaKey}
                            options={[
                                { label: 'Select meta key...', value: '' },
                                ...availableMetaKeys.map(key => ({
                                    label: key,
                                    value: key
                                }))
                            ]}
                            onChange={(value) => setAttributes({ metaKey: value })}
                        />
                        
                        <ToggleControl
                            label="Show Label"
                            checked={showLabel}
                            onChange={(value) => setAttributes({ showLabel: value })}
                        />
                    </PanelBody>
                </InspectorControls>
                
                <div className="post-meta-block">
                    {metaKey ? (
                        <>
                            {showLabel && <strong>{metaKey}: </strong>}
                            <span>{metaValue || 'No value set'}</span>
                        </>
                    ) : (
                        <p>Select a meta key to display</p>
                    )}
                </div>
            </>
        );
    },
    
    save: ({ attributes }) => {
        const { metaKey, showLabel } = attributes;
        
        return (
            <div className="post-meta-block">
                {metaKey && (
                    <>
                        {showLabel && <strong>{metaKey}: </strong>}
                        <span className="meta-value"></span>
                    </>
                )}
            </div>
        );
    }
});
```

### @wordpress/block-editor

Block editor specific utilities and hooks.

```javascript
// JavaScript: Using @wordpress/block-editor
import { 
    useBlockProps,
    InspectorControls,
    BlockControls,
    MediaUpload,
    MediaUploadCheck,
    URLInput,
    BlockIcon
} from '@wordpress/block-editor';
import { ToolbarGroup, ToolbarButton } from '@wordpress/components';

registerBlockType('my-plugin/image-link-block', {
    title: 'Image Link Block',
    icon: 'format-image',
    category: 'media',
    
    attributes: {
        mediaId: {
            type: 'number',
            default: 0
        },
        mediaUrl: {
            type: 'string',
            default: ''
        },
        linkUrl: {
            type: 'string',
            default: ''
        },
        altText: {
            type: 'string',
            default: ''
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { mediaId, mediaUrl, linkUrl, altText } = attributes;
        const blockProps = useBlockProps();
        
        const onSelectMedia = (media) => {
            setAttributes({
                mediaId: media.id,
                mediaUrl: media.url,
                altText: media.alt || ''
            });
        };
        
        return (
            <>
                <BlockControls>
                    <ToolbarGroup>
                        <ToolbarButton
                            icon="edit"
                            label="Edit Link"
                            onClick={() => {
                                // Focus URL input
                            }}
                        />
                        {linkUrl && (
                            <ToolbarButton
                                icon="editor-unlink"
                                label="Remove Link"
                                onClick={() => setAttributes({ linkUrl: '' })}
                            />
                        )}
                    </ToolbarGroup>
                </BlockControls>
                
                <InspectorControls>
                    <PanelBody title="Image Settings">
                        <MediaUploadCheck>
                            <MediaUpload
                                onSelect={onSelectMedia}
                                allowedTypes={['image']}
                                value={mediaId}
                                render={({ open }) => (
                                    <Button onClick={open}>
                                        {mediaId ? 'Change Image' : 'Select Image'}
                                    </Button>
                                )}
                            />
                        </MediaUploadCheck>
                        
                        <TextControl
                            label="Alt Text"
                            value={altText}
                            onChange={(value) => setAttributes({ altText: value })}
                            help="Describe the image for screen readers"
                        />
                        
                        <TextControl
                            label="Link URL"
                            value={linkUrl}
                            onChange={(value) => setAttributes({ linkUrl: value })}
                            help="Optional link destination"
                        />
                    </PanelBody>
                </InspectorControls>
                
                <div {...blockProps}>
                    {mediaUrl ? (
                        <div className="image-link-block">
                            {linkUrl ? (
                                <a href={linkUrl}>
                                    <img src={mediaUrl} alt={altText} />
                                </a>
                            ) : (
                                <img src={mediaUrl} alt={altText} />
                            )}
                        </div>
                    ) : (
                        <div className="image-placeholder">
                            <BlockIcon icon="format-image" />
                            <p>Select an image</p>
                        </div>
                    )}
                </div>
            </>
        );
    },
    
    save: ({ attributes }) => {
        const { mediaUrl, linkUrl, altText } = attributes;
        const blockProps = useBlockProps.save();
        
        return (
            <div {...blockProps}>
                {mediaUrl && (
                    <div className="image-link-block">
                        {linkUrl ? (
                            <a href={linkUrl}>
                                <img src={mediaUrl} alt={altText} />
                            </a>
                        ) : (
                            <img src={mediaUrl} alt={altText} />
                        )}
                    </div>
                )}
            </div>
        );
    }
});
```

## Advanced Package Usage

### @wordpress/i18n

Internationalization utilities.

```javascript
// JavaScript: Using @wordpress/i18n
import { __, _x, _n, sprintf } from '@wordpress/i18n';

registerBlockType('my-plugin/internationalized-block', {
    title: __('Internationalized Block', 'my-plugin'),
    description: __('A block that supports multiple languages', 'my-plugin'),
    icon: 'translation',
    category: 'widgets',
    
    attributes: {
        message: {
            type: 'string',
            default: __('Hello World', 'my-plugin')
        },
        count: {
            type: 'number',
            default: 1
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { message, count } = attributes;
        
        return (
            <>
                <InspectorControls>
                    <PanelBody title={__('Settings', 'my-plugin')}>
                        <TextControl
                            label={__('Message', 'my-plugin')}
                            value={message}
                            onChange={(value) => setAttributes({ message: value })}
                        />
                        
                        <RangeControl
                            label={__('Count', 'my-plugin')}
                            value={count}
                            onChange={(value) => setAttributes({ count: value })}
                            min={1}
                            max={10}
                        />
                    </PanelBody>
                </InspectorControls>
                
                <div className="internationalized-block">
                    <p>{message}</p>
                    <p>{sprintf(
                        _n(
                            'This block has been used %d time.',
                            'This block has been used %d times.',
                            count,
                            'my-plugin'
                        ),
                        count
                    )}</p>
                </div>
            </>
        );
    },
    
    save: ({ attributes }) => {
        const { message, count } = attributes;
        
        return (
            <div className="internationalized-block">
                <p>{message}</p>
                <p>{sprintf(
                    _n(
                        'This block has been used %d time.',
                        'This block has been used %d times.',
                        count,
                        'my-plugin'
                    ),
                    count
                )}</p>
            </div>
        );
    }
});
```

### @wordpress/api-fetch

API communication utilities.

```javascript
// JavaScript: Using @wordpress/api-fetch
import apiFetch from '@wordpress/api-fetch';

registerBlockType('my-plugin/api-block', {
    title: 'API Data Block',
    icon: 'cloud',
    category: 'widgets',
    
    attributes: {
        apiUrl: {
            type: 'string',
            default: ''
        },
        data: {
            type: 'object',
            default: {}
        },
        loading: {
            type: 'boolean',
            default: false
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { apiUrl, data, loading } = attributes;
        
        const fetchData = async () => {
            if (!apiUrl) return;
            
            setAttributes({ loading: true });
            
            try {
                const response = await apiFetch({
                    path: apiUrl,
                    method: 'GET'
                });
                
                setAttributes({
                    data: response,
                    loading: false
                });
            } catch (error) {
                console.error('API fetch error:', error);
                setAttributes({ loading: false });
            }
        };
        
        return (
            <>
                <InspectorControls>
                    <PanelBody title="API Settings">
                        <TextControl
                            label="API URL"
                            value={apiUrl}
                            onChange={(value) => setAttributes({ apiUrl: value })}
                            placeholder="/wp/v2/posts"
                        />
                        
                        <Button onClick={fetchData} isBusy={loading}>
                            {loading ? 'Loading...' : 'Fetch Data'}
                        </Button>
                    </PanelBody>
                </InspectorControls>
                
                <div className="api-block">
                    {loading ? (
                        <p>Loading data...</p>
                    ) : Object.keys(data).length > 0 ? (
                        <pre>{JSON.stringify(data, null, 2)}</pre>
                    ) : (
                        <p>No data loaded. Configure API URL and click "Fetch Data".</p>
                    )}
                </div>
            </>
        );
    },
    
    save: ({ attributes }) => {
        const { data } = attributes;
        
        return (
            <div className="api-block">
                {Object.keys(data).length > 0 && (
                    <pre>{JSON.stringify(data, null, 2)}</pre>
                )}
            </div>
        );
    }
});
```

### @wordpress/element

React utilities and hooks.

```javascript
// JavaScript: Using @wordpress/element
import { useState, useEffect, useCallback } from '@wordpress/element';

registerBlockType('my-plugin/interactive-block', {
    title: 'Interactive Block',
    icon: 'controls-play',
    category: 'widgets',
    
    attributes: {
        initialValue: {
            type: 'number',
            default: 0
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { initialValue } = attributes;
        const [count, setCount] = useState(initialValue);
        const [isRunning, setIsRunning] = useState(false);
        
        // Update block attribute when count changes
        useEffect(() => {
            setAttributes({ initialValue: count });
        }, [count, setAttributes]);
        
        // Auto-increment counter
        useEffect(() => {
            if (isRunning) {
                const interval = setInterval(() => {
                    setCount(prev => prev + 1);
                }, 1000);
                
                return () => clearInterval(interval);
            }
        }, [isRunning]);
        
        const toggleCounter = useCallback(() => {
            setIsRunning(prev => !prev);
        }, []);
        
        const resetCounter = useCallback(() => {
            setCount(0);
            setIsRunning(false);
        }, []);
        
        return (
            <div className="interactive-block">
                <InspectorControls>
                    <PanelBody title="Counter Settings">
                        <RangeControl
                            label="Initial Value"
                            value={initialValue}
                            onChange={(value) => {
                                setCount(value);
                                setAttributes({ initialValue: value });
                            }}
                            min={0}
                            max={100}
                        />
                    </PanelBody>
                </InspectorControls>
                
                <div className="counter-display">
                    <h3>Counter: {count}</h3>
                    
                    <div className="counter-controls">
                        <Button 
                            onClick={toggleCounter}
                            variant={isRunning ? 'secondary' : 'primary'}
                        >
                            {isRunning ? 'Stop' : 'Start'}
                        </Button>
                        
                        <Button onClick={resetCounter}>
                            Reset
                        </Button>
                        
                        <Button onClick={() => setCount(prev => prev + 1)}>
                            +1
                        </Button>
                        
                        <Button onClick={() => setCount(prev => Math.max(0, prev - 1))}>
                            -1
                        </Button>
                    </div>
                </div>
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { initialValue } = attributes;
        
        return (
            <div className="interactive-block">
                <div className="counter-display">
                    <h3>Counter: {initialValue}</h3>
                </div>
            </div>
        );
    }
});
```

## Package Integration Examples

### Complete Block with Multiple Packages

```javascript
// JavaScript: Complete block using multiple @wordpress packages
import { registerBlockType } from '@wordpress/blocks';
import { 
    useBlockProps,
    InspectorControls,
    BlockControls,
    MediaUpload,
    MediaUploadCheck
} from '@wordpress/block-editor';
import { 
    Button, 
    TextControl, 
    SelectControl,
    PanelBody,
    ToolbarGroup,
    ToolbarButton,
    RangeControl
} from '@wordpress/components';
import { useSelect, useDispatch } from '@wordpress/data';
import { __ } from '@wordpress/i18n';
import { useState } from '@wordpress/element';

registerBlockType('my-plugin/advanced-block', {
    title: __('Advanced Block', 'my-plugin'),
    icon: 'star-filled',
    category: 'widgets',
    
    attributes: {
        title: {
            type: 'string',
            default: ''
        },
        content: {
            type: 'string',
            default: ''
        },
        imageId: {
            type: 'number',
            default: 0
        },
        imageUrl: {
            type: 'string',
            default: ''
        },
        layout: {
            type: 'string',
            default: 'horizontal'
        },
        opacity: {
            type: 'number',
            default: 100
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { title, content, imageId, imageUrl, layout, opacity } = attributes;
        const blockProps = useBlockProps();
        
        // Get current post for context
        const currentPost = useSelect((select) => {
            return select('core/editor').getCurrentPost();
        }, []);
        
        const [isEditingTitle, setIsEditingTitle] = useState(false);
        
        const onSelectImage = (media) => {
            setAttributes({
                imageId: media.id,
                imageUrl: media.url
            });
        };
        
        return (
            <>
                <BlockControls>
                    <ToolbarGroup>
                        <ToolbarButton
                            icon="edit"
                            label={__('Edit Title', 'my-plugin')}
                            onClick={() => setIsEditingTitle(!isEditingTitle)}
                            isPressed={isEditingTitle}
                        />
                    </ToolbarGroup>
                </BlockControls>
                
                <InspectorControls>
                    <PanelBody title={__('Content Settings', 'my-plugin')}>
                        <TextControl
                            label={__('Title', 'my-plugin')}
                            value={title}
                            onChange={(value) => setAttributes({ title: value })}
                        />
                        
                        <TextControl
                            label={__('Content', 'my-plugin')}
                            value={content}
                            onChange={(value) => setAttributes({ content: value })}
                            multiline
                        />
                    </PanelBody>
                    
                    <PanelBody title={__('Layout Settings', 'my-plugin')}>
                        <SelectControl
                            label={__('Layout', 'my-plugin')}
                            value={layout}
                            options={[
                                { label: __('Horizontal', 'my-plugin'), value: 'horizontal' },
                                { label: __('Vertical', 'my-plugin'), value: 'vertical' },
                                { label: __('Overlay', 'my-plugin'), value: 'overlay' }
                            ]}
                            onChange={(value) => setAttributes({ layout: value })}
                        />
                        
                        <RangeControl
                            label={__('Image Opacity', 'my-plugin')}
                            value={opacity}
                            onChange={(value) => setAttributes({ opacity: value })}
                            min={0}
                            max={100}
                        />
                    </PanelBody>
                    
                    <PanelBody title={__('Image Settings', 'my-plugin')}>
                        <MediaUploadCheck>
                            <MediaUpload
                                onSelect={onSelectImage}
                                allowedTypes={['image']}
                                value={imageId}
                                render={({ open }) => (
                                    <Button onClick={open}>
                                        {imageId ? __('Change Image', 'my-plugin') : __('Select Image', 'my-plugin')}
                                    </Button>
                                )}
                            />
                        </MediaUploadCheck>
                        
                        {imageId && (
                            <Button 
                                onClick={() => setAttributes({ imageId: 0, imageUrl: '' })}
                                isDestructive
                            >
                                {__('Remove Image', 'my-plugin')}
                            </Button>
                        )}
                    </PanelBody>
                </InspectorControls>
                
                <div {...blockProps} className={`advanced-block layout-${layout}`}>
                    <div className="block-content" style={{ opacity: opacity / 100 }}>
                        {title && (
                            <h2 className="block-title">
                                {isEditingTitle ? (
                                    <TextControl
                                        value={title}
                                        onChange={(value) => setAttributes({ title: value })}
                                        onBlur={() => setIsEditingTitle(false)}
                                        autoFocus
                                    />
                                ) : (
                                    title
                                )}
                            </h2>
                        )}
                        
                        {content && (
                            <div className="block-text">
                                {content}
                            </div>
                        )}
                    </div>
                    
                    {imageUrl && (
                        <div className="block-image">
                            <img 
                                src={imageUrl} 
                                alt={title || __('Block Image', 'my-plugin')}
                                style={{ opacity: opacity / 100 }}
                            />
                        </div>
                    )}
                    
                    {!imageUrl && (
                        <div className="image-placeholder">
                            <MediaUploadCheck>
                                <MediaUpload
                                    onSelect={onSelectImage}
                                    allowedTypes={['image']}
                                    render={({ open }) => (
                                        <Button onClick={open}>
                                            {__('Select Image', 'my-plugin')}
                                        </Button>
                                    )}
                                />
                            </MediaUploadCheck>
                        </div>
                    )}
                </div>
            </>
        );
    },
    
    save: ({ attributes }) => {
        const { title, content, imageUrl, layout, opacity } = attributes;
        const blockProps = useBlockProps.save();
        
        return (
            <div {...blockProps} className={`advanced-block layout-${layout}`}>
                <div className="block-content" style={{ opacity: opacity / 100 }}>
                    {title && <h2 className="block-title">{title}</h2>}
                    {content && <div className="block-text">{content}</div>}
                </div>
                
                {imageUrl && (
                    <div className="block-image">
                        <img 
                            src={imageUrl} 
                            alt={title || __('Block Image', 'my-plugin')}
                            style={{ opacity: opacity / 100 }}
                        />
                    </div>
                )}
            </div>
        );
    }
});
```

## Best Practices

### Package Optimization

```javascript
// Optimize package imports
import { 
    // Import only what you need
    useBlockProps,
    InspectorControls 
} from '@wordpress/block-editor';

import { 
    Button,
    TextControl,
    PanelBody 
} from '@wordpress/components';

// Use dynamic imports for large packages
const loadHeavyPackage = async () => {
    const { heavyFunction } = await import('@wordpress/heavy-package');
    return heavyFunction();
};
```

### Error Handling

```javascript
// Handle package errors gracefully
try {
    const result = await apiFetch({
        path: '/wp/v2/posts',
        method: 'GET'
    });
} catch (error) {
    console.error('API fetch failed:', error);
    // Fallback behavior
}
```

## Official Documentation

https://developer.wordpress.org/block-editor/reference-guides/packages/
https://developer.wordpress.org/block-editor/reference-guides/packages/packages-blocks/
https://developer.wordpress.org/block-editor/reference-guides/packages/packages-components/
https://developer.wordpress.org/block-editor/reference-guides/packages/packages-data/
