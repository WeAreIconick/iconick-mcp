# WordPress Block Transforms

Block transforms allow converting between different block types, enabling seamless content migration and block type conversions.

## Basic Block Transforms

### Simple Transform Implementation

```javascript
// JavaScript: Basic block transform
registerBlockType('my-plugin/quote-block', {
    title: 'Quote Block',
    icon: 'format-quote',
    category: 'text',
    
    attributes: {
        content: {
            type: 'string',
            source: 'html',
            selector: 'blockquote'
        },
        citation: {
            type: 'string',
            source: 'html',
            selector: 'cite'
        }
    },
    
    transforms: {
        from: [
            {
                type: 'block',
                blocks: ['core/paragraph'],
                transform: (attributes) => {
                    return createBlock('my-plugin/quote-block', {
                        content: attributes.content
                    });
                }
            }
        ],
        to: [
            {
                type: 'block',
                blocks: ['core/paragraph'],
                transform: (attributes) => {
                    return createBlock('core/paragraph', {
                        content: attributes.content
                    });
                }
            }
        ]
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { content, citation } = attributes;
        
        return (
            <div className="quote-block">
                <RichText
                    tagName="blockquote"
                    value={content}
                    onChange={(value) => setAttributes({ content: value })}
                    placeholder="Enter quote..."
                />
                <RichText
                    tagName="cite"
                    value={citation}
                    onChange={(value) => setAttributes({ citation: value })}
                    placeholder="Citation (optional)"
                />
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { content, citation } = attributes;
        
        return (
            <blockquote className="quote-block">
                <RichText.Content value={content} />
                {citation && <cite><RichText.Content value={citation} /></cite>}
            </blockquote>
        );
    }
});
```

### Multi-Block Transforms

```javascript
// JavaScript: Transform multiple blocks into one
registerBlockType('my-plugin/hero-section', {
    title: 'Hero Section',
    icon: 'cover-image',
    category: 'layout',
    
    attributes: {
        title: {
            type: 'string',
            source: 'html',
            selector: 'h1'
        },
        subtitle: {
            type: 'string',
            source: 'html',
            selector: 'p'
        }
    },
    
    transforms: {
        from: [
            {
                type: 'block',
                blocks: ['core/heading', 'core/paragraph'],
                transform: (attributes, innerBlocks) => {
                    // Transform heading + paragraph into hero section
                    const headingBlock = innerBlocks.find(block => block.name === 'core/heading');
                    const paragraphBlock = innerBlocks.find(block => block.name === 'core/paragraph');
                    
                    return createBlock('my-plugin/hero-section', {
                        title: headingBlock?.attributes?.content || '',
                        subtitle: paragraphBlock?.attributes?.content || ''
                    });
                }
            }
        ]
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { title, subtitle } = attributes;
        
        return (
            <div className="hero-section">
                <RichText
                    tagName="h1"
                    value={title}
                    onChange={(value) => setAttributes({ title: value })}
                    placeholder="Hero Title"
                />
                <RichText
                    tagName="p"
                    value={subtitle}
                    onChange={(value) => setAttributes({ subtitle: value })}
                    placeholder="Hero Subtitle"
                />
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { title, subtitle } = attributes;
        
        return (
            <div className="hero-section">
                <h1><RichText.Content value={title} /></h1>
                <p><RichText.Content value={subtitle} /></p>
            </div>
        );
    }
});
```

## Advanced Transform Patterns

### Raw HTML Transforms

```javascript
// JavaScript: Transform from raw HTML
registerBlockType('my-plugin/alert-block', {
    title: 'Alert Block',
    icon: 'warning',
    category: 'widgets',
    
    attributes: {
        type: {
            type: 'string',
            default: 'info'
        },
        message: {
            type: 'string',
            source: 'html',
            selector: '.alert-message'
        }
    },
    
    transforms: {
        from: [
            {
                type: 'raw',
                isMatch: (node) => {
                    return node.nodeName === 'DIV' && 
                           node.classList.contains('alert');
                },
                transform: (node) => {
                    const type = node.classList.contains('alert-danger') ? 'danger' :
                                node.classList.contains('alert-warning') ? 'warning' :
                                node.classList.contains('alert-success') ? 'success' : 'info';
                    
                    const message = node.querySelector('.alert-message')?.innerHTML || node.innerHTML;
                    
                    return createBlock('my-plugin/alert-block', {
                        type: type,
                        message: message
                    });
                }
            }
        ]
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { type, message } = attributes;
        
        return (
            <div className={`alert-block alert-${type}`}>
                <SelectControl
                    value={type}
                    options={[
                        { label: 'Info', value: 'info' },
                        { label: 'Success', value: 'success' },
                        { label: 'Warning', value: 'warning' },
                        { label: 'Danger', value: 'danger' }
                    ]}
                    onChange={(value) => setAttributes({ type: value })}
                />
                
                <RichText
                    className="alert-message"
                    value={message}
                    onChange={(value) => setAttributes({ message: value })}
                    placeholder="Enter alert message..."
                />
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { type, message } = attributes;
        
        return (
            <div className={`alert alert-${type}`}>
                <div className="alert-message">
                    <RichText.Content value={message} />
                </div>
            </div>
        );
    }
});
```

### Shortcode Transforms

```javascript
// JavaScript: Transform from shortcode
registerBlockType('my-plugin/gallery-block', {
    title: 'Gallery Block',
    icon: 'format-gallery',
    category: 'media',
    
    attributes: {
        images: {
            type: 'array',
            default: []
        },
        columns: {
            type: 'number',
            default: 3
        }
    },
    
    transforms: {
        from: [
            {
                type: 'shortcode',
                tag: 'gallery',
                transform: (attributes) => {
                    const ids = attributes.ids ? attributes.ids.split(',').map(id => parseInt(id)) : [];
                    const columns = parseInt(attributes.columns) || 3;
                    
                    return createBlock('my-plugin/gallery-block', {
                        images: ids.map(id => ({ id: id })),
                        columns: columns
                    });
                }
            }
        ],
        to: [
            {
                type: 'shortcode',
                tag: 'gallery',
                transform: (attributes) => {
                    const ids = attributes.images.map(img => img.id).join(',');
                    return `[gallery ids="${ids}" columns="${attributes.columns}"]`;
                }
            }
        ]
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { images, columns } = attributes;
        
        const addImages = () => {
            // Open media library
            const mediaLibrary = wp.media({
                multiple: true,
                library: { type: 'image' }
            });
            
            mediaLibrary.on('select', () => {
                const selectedImages = mediaLibrary.state().get('selection').toJSON();
                const newImages = selectedImages.map(img => ({ id: img.id, url: img.url }));
                setAttributes({ images: [...images, ...newImages] });
            });
            
            mediaLibrary.open();
        };
        
        return (
            <div className="gallery-block">
                <InspectorControls>
                    <PanelBody title="Gallery Settings">
                        <RangeControl
                            label="Columns"
                            value={columns}
                            onChange={(value) => setAttributes({ columns: value })}
                            min={1}
                            max={6}
                        />
                    </PanelBody>
                </InspectorControls>
                
                <div className="gallery-images" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
                    {images.map((image, index) => (
                        <div key={index} className="gallery-image">
                            <img src={image.url} alt="" />
                            <Button
                                icon="trash"
                                onClick={() => {
                                    const newImages = images.filter((_, i) => i !== index);
                                    setAttributes({ images: newImages });
                                }}
                                className="remove-image"
                            />
                        </div>
                    ))}
                </div>
                
                <Button onClick={addImages}>Add Images</Button>
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { images, columns } = attributes;
        
        return (
            <div className="gallery-block" data-columns={columns}>
                {images.map((image, index) => (
                    <div key={index} className="gallery-image">
                        <img src={image.url} alt="" />
                    </div>
                ))}
            </div>
        );
    }
});
```

### Files Transforms

```javascript
// JavaScript: Transform from files (drag and drop)
registerBlockType('my-plugin/image-slider', {
    title: 'Image Slider',
    icon: 'images-alt2',
    category: 'media',
    
    attributes: {
        images: {
            type: 'array',
            default: []
        },
        autoplay: {
            type: 'boolean',
            default: false
        }
    },
    
    transforms: {
        from: [
            {
                type: 'files',
                isMatch: (files) => {
                    return files.length > 0 && files.every(file => file.type.startsWith('image/'));
                },
                transform: async (files) => {
                    const imagePromises = files.map(file => {
                        return new Promise((resolve) => {
                            const reader = new FileReader();
                            reader.onload = (e) => {
                                resolve({
                                    url: e.target.result,
                                    name: file.name
                                });
                            };
                            reader.readAsDataURL(file);
                        });
                    });
                    
                    const images = await Promise.all(imagePromises);
                    
                    return createBlock('my-plugin/image-slider', {
                        images: images
                    });
                }
            }
        ]
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { images, autoplay } = attributes;
        
        return (
            <div className="image-slider-block">
                <InspectorControls>
                    <PanelBody title="Slider Settings">
                        <ToggleControl
                            label="Autoplay"
                            checked={autoplay}
                            onChange={(value) => setAttributes({ autoplay: value })}
                        />
                    </PanelBody>
                </InspectorControls>
                
                <div className="slider-images">
                    {images.map((image, index) => (
                        <div key={index} className="slider-image">
                            <img src={image.url} alt={image.name} />
                            <Button
                                icon="trash"
                                onClick={() => {
                                    const newImages = images.filter((_, i) => i !== index);
                                    setAttributes({ images: newImages });
                                }}
                                className="remove-image"
                            />
                        </div>
                    ))}
                </div>
                
                <Button onClick={() => {
                    const input = document.createElement('input');
                    input.type = 'file';
                    input.multiple = true;
                    input.accept = 'image/*';
                    input.onchange = (e) => {
                        const files = Array.from(e.target.files);
                        // Handle file upload logic
                    };
                    input.click();
                }}>
                    Add Images
                </Button>
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { images, autoplay } = attributes;
        
        return (
            <div className="image-slider" data-autoplay={autoplay}>
                {images.map((image, index) => (
                    <div key={index} className="slider-image">
                        <img src={image.url} alt={image.name} />
                    </div>
                ))}
            </div>
        );
    }
});
```

## Complex Transform Examples

### Group Transform

```javascript
// JavaScript: Transform group of blocks
registerBlockType('my-plugin/testimonial-block', {
    title: 'Testimonial Block',
    icon: 'format-quote',
    category: 'widgets',
    
    attributes: {
        quote: {
            type: 'string',
            source: 'html',
            selector: '.testimonial-quote'
        },
        author: {
            type: 'string',
            source: 'html',
            selector: '.testimonial-author'
        },
        position: {
            type: 'string',
            source: 'html',
            selector: '.testimonial-position'
        }
    },
    
    transforms: {
        from: [
            {
                type: 'group',
                blocks: ['core/quote', 'core/paragraph'],
                transform: (blocks) => {
                    const quoteBlock = blocks.find(block => block.name === 'core/quote');
                    const paragraphBlock = blocks.find(block => block.name === 'core/paragraph');
                    
                    return createBlock('my-plugin/testimonial-block', {
                        quote: quoteBlock?.attributes?.value || '',
                        author: paragraphBlock?.attributes?.content || ''
                    });
                }
            }
        ]
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { quote, author, position } = attributes;
        
        return (
            <div className="testimonial-block">
                <RichText
                    tagName="blockquote"
                    className="testimonial-quote"
                    value={quote}
                    onChange={(value) => setAttributes({ quote: value })}
                    placeholder="Testimonial quote..."
                />
                
                <div className="testimonial-meta">
                    <RichText
                        tagName="cite"
                        className="testimonial-author"
                        value={author}
                        onChange={(value) => setAttributes({ author: value })}
                        placeholder="Author name"
                    />
                    
                    <RichText
                        tagName="span"
                        className="testimonial-position"
                        value={position}
                        onChange={(value) => setAttributes({ position: value })}
                        placeholder="Position/Company"
                    />
                </div>
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { quote, author, position } = attributes;
        
        return (
            <div className="testimonial-block">
                <blockquote className="testimonial-quote">
                    <RichText.Content value={quote} />
                </blockquote>
                
                <div className="testimonial-meta">
                    <cite className="testimonial-author">
                        <RichText.Content value={author} />
                    </cite>
                    {position && (
                        <span className="testimonial-position">
                            <RichText.Content value={position} />
                        </span>
                    )}
                </div>
            </div>
        );
    }
});
```

### Entry Transforms

```javascript
// JavaScript: Transform on block entry
registerBlockType('my-plugin/contact-form', {
    title: 'Contact Form',
    icon: 'email',
    category: 'widgets',
    
    attributes: {
        fields: {
            type: 'array',
            default: [
                { type: 'text', label: 'Name', required: true },
                { type: 'email', label: 'Email', required: true },
                { type: 'textarea', label: 'Message', required: true }
            ]
        }
    },
    
    transforms: {
        from: [
            {
                type: 'entry',
                transform: (attributes) => {
                    // Transform when block is inserted
                    return createBlock('my-plugin/contact-form', {
                        fields: [
                            { type: 'text', label: 'Name', required: true },
                            { type: 'email', label: 'Email', required: true },
                            { type: 'textarea', label: 'Message', required: true }
                        ]
                    });
                }
            }
        ]
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { fields } = attributes;
        
        const addField = () => {
            const newField = {
                type: 'text',
                label: 'New Field',
                required: false
            };
            setAttributes({
                fields: [...fields, newField]
            });
        };
        
        const removeField = (index) => {
            const newFields = fields.filter((_, i) => i !== index);
            setAttributes({ fields: newFields });
        };
        
        const updateField = (index, updates) => {
            const newFields = fields.map((field, i) => 
                i === index ? { ...field, ...updates } : field
            );
            setAttributes({ fields: newFields });
        };
        
        return (
            <div className="contact-form-block">
                <InspectorControls>
                    <PanelBody title="Form Fields">
                        {fields.map((field, index) => (
                            <div key={index} className="field-control">
                                <SelectControl
                                    label="Field Type"
                                    value={field.type}
                                    options={[
                                        { label: 'Text', value: 'text' },
                                        { label: 'Email', value: 'email' },
                                        { label: 'Textarea', value: 'textarea' },
                                        { label: 'Number', value: 'number' }
                                    ]}
                                    onChange={(value) => updateField(index, { type: value })}
                                />
                                
                                <TextControl
                                    label="Field Label"
                                    value={field.label}
                                    onChange={(value) => updateField(index, { label: value })}
                                />
                                
                                <ToggleControl
                                    label="Required"
                                    checked={field.required}
                                    onChange={(value) => updateField(index, { required: value })}
                                />
                                
                                <Button
                                    isDestructive
                                    onClick={() => removeField(index)}
                                    disabled={fields.length <= 1}
                                >
                                    Remove Field
                                </Button>
                            </div>
                        ))}
                        
                        <Button onClick={addField}>Add Field</Button>
                    </PanelBody>
                </InspectorControls>
                
                <div className="form-preview">
                    <h3>Contact Form Preview</h3>
                    <form>
                        {fields.map((field, index) => (
                            <div key={index} className="form-field">
                                <label>
                                    {field.label}
                                    {field.required && <span className="required">*</span>}
                                </label>
                                {field.type === 'textarea' ? (
                                    <textarea placeholder={`Enter ${field.label.toLowerCase()}...`} />
                                ) : (
                                    <input
                                        type={field.type}
                                        placeholder={`Enter ${field.label.toLowerCase()}...`}
                                    />
                                )}
                            </div>
                        ))}
                        <button type="submit">Send Message</button>
                    </form>
                </div>
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { fields } = attributes;
        
        return (
            <div className="contact-form-block">
                <form className="contact-form">
                    {fields.map((field, index) => (
                        <div key={index} className="form-field">
                            <label>
                                {field.label}
                                {field.required && <span className="required">*</span>}
                            </label>
                            {field.type === 'textarea' ? (
                                <textarea 
                                    name={field.label.toLowerCase()}
                                    required={field.required}
                                    placeholder={`Enter ${field.label.toLowerCase()}...`}
                                />
                            ) : (
                                <input
                                    type={field.type}
                                    name={field.label.toLowerCase()}
                                    required={field.required}
                                    placeholder={`Enter ${field.label.toLowerCase()}...`}
                                />
                            )}
                        </div>
                    ))}
                    <button type="submit">Send Message</button>
                </form>
            </div>
        );
    }
});
```

## Best Practices

### Performance Optimization

```javascript
// Optimize transform performance
registerBlockType('my-plugin/optimized-block', {
    transforms: {
        from: [
            {
                type: 'block',
                blocks: ['core/paragraph'],
                transform: (attributes) => {
                    // Use createBlock for better performance
                    return createBlock('my-plugin/optimized-block', {
                        content: attributes.content
                    });
                },
                priority: 10 // Higher priority for preferred transforms
            }
        ]
    }
});
```

### Transform Validation

```javascript
// Validate transform conditions
registerBlockType('my-plugin/validated-block', {
    transforms: {
        from: [
            {
                type: 'block',
                blocks: ['core/paragraph'],
                isMatch: (attributes, block) => {
                    // Only transform if paragraph has specific content
                    return attributes.content && attributes.content.includes('@');
                },
                transform: (attributes) => {
                    return createBlock('my-plugin/validated-block', {
                        content: attributes.content
                    });
                }
            }
        ]
    }
});
```

## Official Documentation

https://developer.wordpress.org/block-editor/reference-guides/block-api/block-registration/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-transforms/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-supports/
