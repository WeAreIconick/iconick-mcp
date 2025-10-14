# WordPress InnerBlocks

InnerBlocks allow creating nested block structures and complex layouts within custom blocks.

## Basic InnerBlocks Implementation

### Simple InnerBlocks Block

```javascript
// JavaScript: Basic InnerBlocks block
registerBlockType('my-plugin/container-block', {
    title: 'Container Block',
    icon: 'layout',
    category: 'layout',
    
    attributes: {
        className: {
            type: 'string',
            default: ''
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { className } = attributes;
        
        return (
            <div className={`container-block ${className}`}>
                <h3>Container Block</h3>
                <InnerBlocks
                    allowedBlocks={['core/paragraph', 'core/heading', 'core/image']}
                    template={[
                        ['core/heading', { level: 2, placeholder: 'Enter heading...' }],
                        ['core/paragraph', { placeholder: 'Enter content...' }]
                    ]}
                    templateLock={false}
                />
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { className } = attributes;
        
        return (
            <div className={`container-block ${className}`}>
                <InnerBlocks.Content />
            </div>
        );
    }
});
```

### InnerBlocks with Template Lock

```javascript
// JavaScript: InnerBlocks with locked template
registerBlockType('my-plugin/hero-section', {
    title: 'Hero Section',
    icon: 'cover-image',
    category: 'layout',
    
    edit: ({ attributes, setAttributes }) => {
        return (
            <div className="hero-section">
                <InnerBlocks
                    allowedBlocks={['core/heading', 'core/paragraph', 'core/button']}
                    template={[
                        ['core/heading', { 
                            level: 1, 
                            placeholder: 'Hero Title',
                            textAlign: 'center'
                        }],
                        ['core/paragraph', { 
                            placeholder: 'Hero description...',
                            textAlign: 'center'
                        }],
                        ['core/buttons', {}, [
                            ['core/button', { 
                                text: 'Call to Action',
                                backgroundColor: '#0073aa'
                            }]
                        ]]
                    ]}
                    templateLock="all" // Prevents adding/removing/reordering
                />
            </div>
        );
    },
    
    save: () => {
        return (
            <div className="hero-section">
                <InnerBlocks.Content />
            </div>
        );
    }
});
```

## Advanced InnerBlocks Patterns

### Conditional InnerBlocks

```javascript
// JavaScript: Conditional InnerBlocks based on attributes
registerBlockType('my-plugin/tabs-block', {
    title: 'Tabs Block',
    icon: 'admin-page',
    category: 'widgets',
    
    attributes: {
        tabs: {
            type: 'array',
            default: [
                { id: 'tab1', title: 'Tab 1', active: true },
                { id: 'tab2', title: 'Tab 2', active: false }
            ]
        },
        activeTab: {
            type: 'string',
            default: 'tab1'
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { tabs, activeTab } = attributes;
        
        const addTab = () => {
            const newTab = {
                id: `tab${tabs.length + 1}`,
                title: `Tab ${tabs.length + 1}`,
                active: false
            };
            setAttributes({
                tabs: [...tabs, newTab]
            });
        };
        
        const removeTab = (tabId) => {
            const newTabs = tabs.filter(tab => tab.id !== tabId);
            const newActiveTab = newTabs.length > 0 ? newTabs[0].id : '';
            setAttributes({
                tabs: newTabs,
                activeTab: newActiveTab
            });
        };
        
        const setActiveTab = (tabId) => {
            setAttributes({ activeTab: tabId });
        };
        
        return (
            <div className="tabs-block">
                <InspectorControls>
                    <PanelBody title="Tab Settings">
                        {tabs.map((tab, index) => (
                            <div key={tab.id} className="tab-control">
                                <TextControl
                                    label={`Tab ${index + 1} Title`}
                                    value={tab.title}
                                    onChange={(value) => {
                                        const newTabs = [...tabs];
                                        newTabs[index].title = value;
                                        setAttributes({ tabs: newTabs });
                                    }}
                                />
                                <Button 
                                    isDestructive 
                                    onClick={() => removeTab(tab.id)}
                                    disabled={tabs.length <= 1}
                                >
                                    Remove Tab
                                </Button>
                            </div>
                        ))}
                        <Button onClick={addTab}>Add Tab</Button>
                    </PanelBody>
                </InspectorControls>
                
                <div className="tabs-navigation">
                    {tabs.map(tab => (
                        <button
                            key={tab.id}
                            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                            onClick={() => setActiveTab(tab.id)}
                        >
                            {tab.title}
                        </button>
                    ))}
                </div>
                
                <div className="tabs-content">
                    {tabs.map(tab => (
                        <div 
                            key={tab.id}
                            className={`tab-panel ${activeTab === tab.id ? 'active' : ''}`}
                        >
                            <InnerBlocks
                                allowedBlocks={['core/paragraph', 'core/heading', 'core/image']}
                                template={[
                                    ['core/paragraph', { placeholder: 'Tab content...' }]
                                ]}
                                templateLock={false}
                            />
                        </div>
                    ))}
                </div>
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { tabs, activeTab } = attributes;
        
        return (
            <div className="tabs-block">
                <div className="tabs-navigation">
                    {tabs.map(tab => (
                        <button
                            key={tab.id}
                            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                            data-tab={tab.id}
                        >
                            {tab.title}
                        </button>
                    ))}
                </div>
                
                <div className="tabs-content">
                    {tabs.map(tab => (
                        <div 
                            key={tab.id}
                            className={`tab-panel ${activeTab === tab.id ? 'active' : ''}`}
                            data-tab={tab.id}
                        >
                            <InnerBlocks.Content />
                        </div>
                    ))}
                </div>
            </div>
        );
    }
});
```

### Dynamic InnerBlocks with Controls

```javascript
// JavaScript: Dynamic InnerBlocks with block controls
registerBlockType('my-plugin/accordion-block', {
    title: 'Accordion Block',
    icon: 'list-view',
    category: 'widgets',
    
    attributes: {
        items: {
            type: 'array',
            default: [
                { id: 'item1', title: 'Accordion Item 1', open: true },
                { id: 'item2', title: 'Accordion Item 2', open: false }
            ]
        },
        allowMultiple: {
            type: 'boolean',
            default: false
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { items, allowMultiple } = attributes;
        
        const addItem = () => {
            const newItem = {
                id: `item${items.length + 1}`,
                title: `Accordion Item ${items.length + 1}`,
                open: false
            };
            setAttributes({
                items: [...items, newItem]
            });
        };
        
        const removeItem = (itemId) => {
            const newItems = items.filter(item => item.id !== itemId);
            setAttributes({ items: newItems });
        };
        
        const toggleItem = (itemId) => {
            const newItems = items.map(item => {
                if (allowMultiple) {
                    return item.id === itemId ? { ...item, open: !item.open } : item;
                } else {
                    return {
                        ...item,
                        open: item.id === itemId ? !item.open : false
                    };
                }
            });
            setAttributes({ items: newItems });
        };
        
        return (
            <div className="accordion-block">
                <InspectorControls>
                    <PanelBody title="Accordion Settings">
                        <ToggleControl
                            label="Allow Multiple Open"
                            checked={allowMultiple}
                            onChange={(value) => setAttributes({ allowMultiple: value })}
                        />
                        <Button onClick={addItem}>Add Accordion Item</Button>
                    </PanelBody>
                </InspectorControls>
                
                <div className="accordion-items">
                    {items.map((item, index) => (
                        <div key={item.id} className="accordion-item">
                            <div className="accordion-header">
                                <TextControl
                                    value={item.title}
                                    onChange={(value) => {
                                        const newItems = [...items];
                                        newItems[index].title = value;
                                        setAttributes({ items: newItems });
                                    }}
                                    className="accordion-title-input"
                                />
                                <ButtonGroup>
                                    <Button
                                        icon={item.open ? 'arrow-up-alt2' : 'arrow-down-alt2'}
                                        onClick={() => toggleItem(item.id)}
                                        label={item.open ? 'Collapse' : 'Expand'}
                                    />
                                    <Button
                                        icon="trash"
                                        onClick={() => removeItem(item.id)}
                                        isDestructive
                                        disabled={items.length <= 1}
                                    />
                                </ButtonGroup>
                            </div>
                            
                            {item.open && (
                                <div className="accordion-content">
                                    <InnerBlocks
                                        allowedBlocks={['core/paragraph', 'core/heading', 'core/list']}
                                        template={[
                                            ['core/paragraph', { placeholder: 'Accordion content...' }]
                                        ]}
                                        templateLock={false}
                                    />
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        );
    },
    
    save: ({ attributes }) => {
        const { items, allowMultiple } = attributes;
        
        return (
            <div className="accordion-block" data-allow-multiple={allowMultiple}>
                <div className="accordion-items">
                    {items.map(item => (
                        <div key={item.id} className="accordion-item">
                            <div className="accordion-header">
                                <h3 className="accordion-title">{item.title}</h3>
                                <button className="accordion-toggle">
                                    <span className="accordion-icon"></span>
                                </button>
                            </div>
                            <div className="accordion-content">
                                <InnerBlocks.Content />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }
});
```

## InnerBlocks with Custom Controls

### Block Toolbar Integration

```javascript
// JavaScript: InnerBlocks with custom block toolbar
registerBlockType('my-plugin/column-layout', {
    title: 'Column Layout',
    icon: 'columns',
    category: 'layout',
    
    attributes: {
        columns: {
            type: 'number',
            default: 2
        },
        gap: {
            type: 'string',
            default: 'medium'
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { columns, gap } = attributes;
        
        const updateColumns = (newColumns) => {
            setAttributes({ columns: newColumns });
        };
        
        const updateGap = (newGap) => {
            setAttributes({ gap: newGap });
        };
        
        return (
            <>
                <BlockControls>
                    <ToolbarGroup>
                        <ToolbarButton
                            icon="minus"
                            label="Remove Column"
                            onClick={() => updateColumns(Math.max(2, columns - 1))}
                            disabled={columns <= 2}
                        />
                        <ToolbarButton
                            icon="plus"
                            label="Add Column"
                            onClick={() => updateColumns(Math.min(4, columns + 1))}
                            disabled={columns >= 4}
                        />
                    </ToolbarGroup>
                    
                    <ToolbarDropdownMenu
                        icon="editor-alignleft"
                        label="Column Gap"
                        controls={[
                            {
                                title: 'No Gap',
                                icon: 'minus',
                                onClick: () => updateGap('none')
                            },
                            {
                                title: 'Small Gap',
                                icon: 'editor-alignleft',
                                onClick: () => updateGap('small')
                            },
                            {
                                title: 'Medium Gap',
                                icon: 'editor-aligncenter',
                                onClick: () => updateGap('medium')
                            },
                            {
                                title: 'Large Gap',
                                icon: 'editor-alignright',
                                onClick: () => updateGap('large')
                            }
                        ]}
                    />
                </BlockControls>
                
                <InspectorControls>
                    <PanelBody title="Layout Settings">
                        <RangeControl
                            label="Number of Columns"
                            value={columns}
                            onChange={updateColumns}
                            min={2}
                            max={4}
                        />
                        
                        <SelectControl
                            label="Column Gap"
                            value={gap}
                            options={[
                                { label: 'No Gap', value: 'none' },
                                { label: 'Small Gap', value: 'small' },
                                { label: 'Medium Gap', value: 'medium' },
                                { label: 'Large Gap', value: 'large' }
                            ]}
                            onChange={updateGap}
                        />
                    </PanelBody>
                </InspectorControls>
                
                <div className={`column-layout columns-${columns} gap-${gap}`}>
                    {Array.from({ length: columns }, (_, index) => (
                        <div key={index} className="column">
                            <InnerBlocks
                                allowedBlocks={['core/paragraph', 'core/heading', 'core/image', 'core/button']}
                                template={[
                                    ['core/paragraph', { placeholder: `Column ${index + 1} content...` }]
                                ]}
                                templateLock={false}
                            />
                        </div>
                    ))}
                </div>
            </>
        );
    },
    
    save: ({ attributes }) => {
        const { columns, gap } = attributes;
        
        return (
            <div className={`column-layout columns-${columns} gap-${gap}`}>
                {Array.from({ length: columns }, (_, index) => (
                    <div key={index} className="column">
                        <InnerBlocks.Content />
                    </div>
                ))}
            </div>
        );
    }
});
```

## InnerBlocks with Sidebar Controls

### Inspector Controls Integration

```javascript
// JavaScript: InnerBlocks with sidebar controls
registerBlockType('my-plugin/card-grid', {
    title: 'Card Grid',
    icon: 'grid-view',
    category: 'layout',
    
    attributes: {
        cards: {
            type: 'array',
            default: [
                { id: 'card1', title: 'Card 1', featured: false },
                { id: 'card2', title: 'Card 2', featured: true },
                { id: 'card3', title: 'Card 3', featured: false }
            ]
        },
        columns: {
            type: 'number',
            default: 3
        },
        showImages: {
            type: 'boolean',
            default: true
        }
    },
    
    edit: ({ attributes, setAttributes }) => {
        const { cards, columns, showImages } = attributes;
        
        const addCard = () => {
            const newCard = {
                id: `card${cards.length + 1}`,
                title: `Card ${cards.length + 1}`,
                featured: false
            };
            setAttributes({
                cards: [...cards, newCard]
            });
        };
        
        const removeCard = (cardId) => {
            const newCards = cards.filter(card => card.id !== cardId);
            setAttributes({ cards: newCards });
        };
        
        const toggleFeatured = (cardId) => {
            const newCards = cards.map(card => 
                card.id === cardId ? { ...card, featured: !card.featured } : card
            );
            setAttributes({ cards: newCards });
        };
        
        return (
            <>
                <InspectorControls>
                    <PanelBody title="Grid Settings">
                        <RangeControl
                            label="Number of Columns"
                            value={columns}
                            onChange={(value) => setAttributes({ columns: value })}
                            min={1}
                            max={6}
                        />
                        
                        <ToggleControl
                            label="Show Images"
                            checked={showImages}
                            onChange={(value) => setAttributes({ showImages: value })}
                        />
                        
                        <Button onClick={addCard}>Add Card</Button>
                    </PanelBody>
                    
                    <PanelBody title="Card Management">
                        {cards.map((card, index) => (
                            <div key={card.id} className="card-control">
                                <TextControl
                                    label={`Card ${index + 1} Title`}
                                    value={card.title}
                                    onChange={(value) => {
                                        const newCards = [...cards];
                                        newCards[index].title = value;
                                        setAttributes({ cards: newCards });
                                    }}
                                />
                                
                                <ToggleControl
                                    label="Featured Card"
                                    checked={card.featured}
                                    onChange={() => toggleFeatured(card.id)}
                                />
                                
                                <Button 
                                    isDestructive 
                                    onClick={() => removeCard(card.id)}
                                    disabled={cards.length <= 1}
                                >
                                    Remove Card
                                </Button>
                            </div>
                        ))}
                    </PanelBody>
                </InspectorControls>
                
                <div className={`card-grid columns-${columns}`}>
                    {cards.map((card, index) => (
                        <div key={card.id} className={`card ${card.featured ? 'featured' : ''}`}>
                            <div className="card-header">
                                <h3 className="card-title">{card.title}</h3>
                                {card.featured && <span className="featured-badge">Featured</span>}
                            </div>
                            
                            <div className="card-content">
                                <InnerBlocks
                                    allowedBlocks={['core/paragraph', 'core/heading', 'core/image', 'core/button']}
                                    template={[
                                        showImages && ['core/image', { placeholder: 'Card image...' }],
                                        ['core/heading', { level: 3, placeholder: 'Card heading...' }],
                                        ['core/paragraph', { placeholder: 'Card content...' }]
                                    ].filter(Boolean)}
                                    templateLock={false}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            </>
        );
    },
    
    save: ({ attributes }) => {
        const { cards, columns, showImages } = attributes;
        
        return (
            <div className={`card-grid columns-${columns}`}>
                {cards.map(card => (
                    <div key={card.id} className={`card ${card.featured ? 'featured' : ''}`}>
                        <div className="card-header">
                            <h3 className="card-title">{card.title}</h3>
                            {card.featured && <span className="featured-badge">Featured</span>}
                        </div>
                        
                        <div className="card-content">
                            <InnerBlocks.Content />
                        </div>
                    </div>
                ))}
            </div>
        );
    }
});
```

## Best Practices

### Performance Optimization

```javascript
// Optimize InnerBlocks performance
registerBlockType('my-plugin/optimized-container', {
    edit: ({ attributes, setAttributes }) => {
        // Use useMemo for expensive calculations
        const memoizedTemplate = useMemo(() => [
            ['core/heading', { level: 2, placeholder: 'Title...' }],
            ['core/paragraph', { placeholder: 'Content...' }]
        ], []);
        
        // Use useCallback for event handlers
        const handleTemplateChange = useCallback((template) => {
            // Handle template changes efficiently
        }, []);
        
        return (
            <div className="optimized-container">
                <InnerBlocks
                    allowedBlocks={['core/paragraph', 'core/heading']}
                    template={memoizedTemplate}
                    onTemplateChange={handleTemplateChange}
                    templateLock={false}
                />
            </div>
        );
    },
    
    save: () => {
        return (
            <div className="optimized-container">
                <InnerBlocks.Content />
            </div>
        );
    }
});
```

### Accessibility

```javascript
// Accessible InnerBlocks implementation
registerBlockType('my-plugin/accessible-container', {
    edit: ({ attributes, setAttributes }) => {
        return (
            <div className="accessible-container" role="region" aria-label="Content Container">
                <InnerBlocks
                    allowedBlocks={['core/paragraph', 'core/heading', 'core/image']}
                    template={[
                        ['core/heading', { level: 2, placeholder: 'Section heading...' }],
                        ['core/paragraph', { placeholder: 'Section content...' }]
                    ]}
                    templateLock={false}
                />
            </div>
        );
    },
    
    save: () => {
        return (
            <div className="accessible-container" role="region" aria-label="Content Container">
                <InnerBlocks.Content />
            </div>
        );
    }
});
```

## Official Documentation

https://developer.wordpress.org/block-editor/reference-guides/block-api/block-registration/
https://developer.wordpress.org/block-editor/reference-guides/innerblocks/
https://developer.wordpress.org/block-editor/reference-guides/block-api/block-supports/
