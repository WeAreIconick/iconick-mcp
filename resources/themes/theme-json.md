# WordPress theme.json

theme.json is the configuration file for block themes, providing global settings, styles, and block configurations.

## Basic theme.json Structure

### Minimal theme.json

```json
{
    "$schema": "https://schemas.wp.org/trunk/theme.json",
    "version": 3,
    "title": "My Block Theme",
    "settings": {
        "appearanceTools": true,
        "color": {
            "palette": [
                {
                    "color": "#ffffff",
                    "name": "White",
                    "slug": "white"
                },
                {
                    "color": "#000000",
                    "name": "Black",
                    "slug": "black"
                },
                {
                    "color": "#0073aa",
                    "name": "WordPress Blue",
                    "slug": "wp-blue"
                }
            ]
        },
        "typography": {
            "fontSizes": [
                {
                    "name": "Small",
                    "size": "14px",
                    "slug": "small"
                },
                {
                    "name": "Medium",
                    "size": "16px",
                    "slug": "medium"
                },
                {
                    "name": "Large",
                    "size": "20px",
                    "slug": "large"
                }
            ]
        }
    },
    "styles": {
        "color": {
            "background": "var(--wp--preset--color--white)",
            "text": "var(--wp--preset--color--black)"
        },
        "typography": {
            "fontSize": "var(--wp--preset--font-size--medium)"
        }
    }
}
```

## Advanced Settings Configuration

### Color Configuration

```json
{
    "settings": {
        "color": {
            "palette": [
                {
                    "color": "#1a1a1a",
                    "name": "Dark Gray",
                    "slug": "dark-gray"
                },
                {
                    "color": "#666666",
                    "name": "Medium Gray",
                    "slug": "medium-gray"
                },
                {
                    "color": "#f7f7f7",
                    "name": "Light Gray",
                    "slug": "light-gray"
                },
                {
                    "color": "#0073aa",
                    "name": "Primary Blue",
                    "slug": "primary-blue"
                },
                {
                    "color": "#005177",
                    "name": "Dark Blue",
                    "slug": "dark-blue"
                },
                {
                    "color": "#00a0d2",
                    "name": "Light Blue",
                    "slug": "light-blue"
                }
            ],
            "gradients": [
                {
                    "gradient": "linear-gradient(135deg,rgb(255,255,255) 0%,rgb(247,247,247) 100%)",
                    "name": "Light to Dark Gray",
                    "slug": "light-to-dark-gray"
                },
                {
                    "gradient": "linear-gradient(135deg,rgb(0,115,170) 0%,rgb(0,161,210) 100%)",
                    "name": "Blue Gradient",
                    "slug": "blue-gradient"
                }
            ],
            "custom": true,
            "customGradient": true,
            "duotone": [
                {
                    "colors": ["#000000", "#ffffff"],
                    "name": "Black and White",
                    "slug": "black-and-white"
                }
            ]
        }
    }
}
```

### Typography Configuration

```json
{
    "settings": {
        "typography": {
            "fontSizes": [
                {
                    "name": "Extra Small",
                    "size": "12px",
                    "slug": "extra-small"
                },
                {
                    "name": "Small",
                    "size": "14px",
                    "slug": "small"
                },
                {
                    "name": "Medium",
                    "size": "16px",
                    "slug": "medium"
                },
                {
                    "name": "Large",
                    "size": "20px",
                    "slug": "large"
                },
                {
                    "name": "Extra Large",
                    "size": "24px",
                    "slug": "extra-large"
                },
                {
                    "name": "Huge",
                    "size": "32px",
                    "slug": "huge"
                }
            ],
            "fontFamilies": [
                {
                    "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen-Sans, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif",
                    "name": "System Font",
                    "slug": "system-font"
                },
                {
                    "fontFamily": "'Helvetica Neue', Helvetica, Arial, sans-serif",
                    "name": "Helvetica",
                    "slug": "helvetica"
                },
                {
                    "fontFamily": "Georgia, 'Times New Roman', serif",
                    "name": "Georgia",
                    "slug": "georgia"
                }
            ],
            "fontStyle": true,
            "fontWeight": true,
            "letterSpacing": true,
            "textDecoration": true,
            "textTransform": true
        }
    }
}
```

### Spacing Configuration

```json
{
    "settings": {
        "spacing": {
            "spacingScale": {
                "steps": 0
            },
            "spacingSizes": [
                {
                    "name": "None",
                    "size": "0px",
                    "slug": "none"
                },
                {
                    "name": "Small",
                    "size": "0.5rem",
                    "slug": "small"
                },
                {
                    "name": "Medium",
                    "size": "1rem",
                    "slug": "medium"
                },
                {
                    "name": "Large",
                    "size": "2rem",
                    "slug": "large"
                },
                {
                    "name": "Extra Large",
                    "size": "4rem",
                    "slug": "extra-large"
                }
            ],
            "units": ["px", "em", "rem", "vh", "vw", "%"],
            "padding": true,
            "margin": true,
            "blockGap": true
        }
    }
}
```

## Block-Specific Settings

### Core Block Customization

```json
{
    "settings": {
        "blocks": {
            "core/paragraph": {
                "color": {
                    "palette": [
                        {
                            "color": "#333333",
                            "name": "Dark Text",
                            "slug": "dark-text"
                        }
                    ]
                },
                "typography": {
                    "fontSizes": [
                        {
                            "name": "Body Text",
                            "size": "16px",
                            "slug": "body-text"
                        }
                    ]
                }
            },
            "core/heading": {
                "color": {
                    "palette": [
                        {
                            "color": "#1a1a1a",
                            "name": "Heading Color",
                            "slug": "heading-color"
                        }
                    ]
                },
                "typography": {
                    "fontSizes": [
                        {
                            "name": "H1",
                            "size": "2.5rem",
                            "slug": "h1"
                        },
                        {
                            "name": "H2",
                            "size": "2rem",
                            "slug": "h2"
                        },
                        {
                            "name": "H3",
                            "size": "1.75rem",
                            "slug": "h3"
                        }
                    ]
                }
            },
            "core/button": {
                "border": {
                    "radius": true,
                    "color": true,
                    "style": true,
                    "width": true
                },
                "color": {
                    "palette": [
                        {
                            "color": "#0073aa",
                            "name": "Button Primary",
                            "slug": "button-primary"
                        },
                        {
                            "color": "#ffffff",
                            "name": "Button Text",
                            "slug": "button-text"
                        }
                    ]
                }
            }
        }
    }
}
```

### Custom Block Settings

```json
{
    "settings": {
        "blocks": {
            "my-plugin/my-custom-block": {
                "color": {
                    "palette": [
                        {
                            "color": "#ff6b35",
                            "name": "Custom Orange",
                            "slug": "custom-orange"
                        }
                    ]
                },
                "typography": {
                    "fontSizes": [
                        {
                            "name": "Custom Large",
                            "size": "28px",
                            "slug": "custom-large"
                        }
                    ]
                },
                "spacing": {
                    "padding": true,
                    "margin": true
                }
            }
        }
    }
}
```

## Styles Configuration

### Global Styles

```json
{
    "styles": {
        "color": {
            "background": "var(--wp--preset--color--white)",
            "text": "var(--wp--preset--color--dark-gray)"
        },
        "typography": {
            "fontFamily": "var(--wp--preset--font-family--system-font)",
            "fontSize": "var(--wp--preset--font-size--medium)",
            "lineHeight": "1.6"
        },
        "spacing": {
            "padding": {
                "top": "var(--wp--preset--spacing--medium)",
                "bottom": "var(--wp--preset--spacing--medium)",
                "left": "var(--wp--preset--spacing--medium)",
                "right": "var(--wp--preset--spacing--medium)"
            }
        }
    }
}
```

### Block-Specific Styles

```json
{
    "styles": {
        "blocks": {
            "core/heading": {
                "typography": {
                    "fontWeight": "600",
                    "lineHeight": "1.2"
                },
                "spacing": {
                    "margin": {
                        "top": "var(--wp--preset--spacing--large)",
                        "bottom": "var(--wp--preset--spacing--medium)"
                    }
                }
            },
            "core/paragraph": {
                "typography": {
                    "lineHeight": "1.7"
                },
                "spacing": {
                    "margin": {
                        "bottom": "var(--wp--preset--spacing--medium)"
                    }
                }
            },
            "core/button": {
                "color": {
                    "background": "var(--wp--preset--color--primary-blue)",
                    "text": "var(--wp--preset--color--white)"
                },
                "border": {
                    "radius": "4px"
                },
                "spacing": {
                    "padding": {
                        "top": "var(--wp--preset--spacing--small)",
                        "bottom": "var(--wp--preset--spacing--small)",
                        "left": "var(--wp--preset--spacing--medium)",
                        "right": "var(--wp--preset--spacing--medium)"
                    }
                }
            }
        }
    }
}
```

### Element Styles

```json
{
    "styles": {
        "elements": {
            "link": {
                "color": {
                    "text": "var(--wp--preset--color--primary-blue)"
                },
                "typography": {
                    "textDecoration": "underline"
                },
                ":hover": {
                    "color": {
                        "text": "var(--wp--preset--color--dark-blue)"
                    }
                }
            },
            "h1": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--h1)",
                    "fontWeight": "700"
                },
                "spacing": {
                    "margin": {
                        "top": "0",
                        "bottom": "var(--wp--preset--spacing--large)"
                    }
                }
            },
            "h2": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--h2)",
                    "fontWeight": "600"
                },
                "spacing": {
                    "margin": {
                        "top": "var(--wp--preset--spacing--large)",
                        "bottom": "var(--wp--preset--spacing--medium)"
                    }
                }
            }
        }
    }
}
```

## Template Parts Configuration

### Header Template Part

```json
{
    "templateParts": [
        {
            "name": "header",
            "title": "Header",
            "area": "header"
        },
        {
            "name": "footer",
            "title": "Footer",
            "area": "footer"
        },
        {
            "name": "sidebar",
            "title": "Sidebar",
            "area": "uncategorized"
        }
    ]
}
```

### Custom Template Parts

```json
{
    "templateParts": [
        {
            "name": "header-main",
            "title": "Main Header",
            "area": "header"
        },
        {
            "name": "header-mobile",
            "title": "Mobile Header",
            "area": "header"
        },
        {
            "name": "footer-primary",
            "title": "Primary Footer",
            "area": "footer"
        },
        {
            "name": "footer-secondary",
            "title": "Secondary Footer",
            "area": "footer"
        }
    ]
}
```

## Advanced Features

### CSS Custom Properties

```json
{
    "styles": {
        "css": [
            "--my-theme-primary-color: #0073aa;",
            "--my-theme-secondary-color: #00a0d2;",
            "--my-theme-border-radius: 8px;",
            "--my-theme-spacing-unit: 1rem;"
        ]
    }
}
```

### Responsive Design

```json
{
    "styles": {
        "blocks": {
            "core/heading": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--large)"
                }
            }
        }
    },
    "styles": [
        {
            "selector": "h1",
            "elements": {
                "typography": {
                    "fontSize": "var(--wp--preset--font-size--huge)"
                }
            },
            "mediaQuery": "(min-width: 768px)"
        }
    ]
}
```

### Dark Mode Support

```json
{
    "styles": [
        {
            "selector": "body",
            "elements": {
                "color": {
                    "background": "#1a1a1a",
                    "text": "#ffffff"
                }
            },
            "mediaQuery": "(prefers-color-scheme: dark)"
        }
    ]
}
```

## Best Practices

### Performance Optimization

```json
{
    "settings": {
        "color": {
            "palette": [
                // Limit palette to essential colors
                {
                    "color": "#ffffff",
                    "name": "White",
                    "slug": "white"
                },
                {
                    "color": "#000000",
                    "name": "Black",
                    "slug": "black"
                },
                {
                    "color": "#0073aa",
                    "name": "Primary",
                    "slug": "primary"
                }
            ]
        },
        "typography": {
            "fontSizes": [
                // Use relative units when possible
                {
                    "name": "Small",
                    "size": "0.875rem",
                    "slug": "small"
                },
                {
                    "name": "Medium",
                    "size": "1rem",
                    "slug": "medium"
                },
                {
                    "name": "Large",
                    "size": "1.25rem",
                    "slug": "large"
                }
            ]
        }
    }
}
```

### Accessibility

```json
{
    "settings": {
        "color": {
            "palette": [
                // Ensure sufficient color contrast
                {
                    "color": "#1a1a1a",
                    "name": "Dark Text",
                    "slug": "dark-text"
                },
                {
                    "color": "#ffffff",
                    "name": "Light Background",
                    "slug": "light-background"
                }
            ]
        },
        "typography": {
            "fontSizes": [
                // Minimum readable font sizes
                {
                    "name": "Body Text",
                    "size": "16px",
                    "slug": "body-text"
                }
            ]
        }
    }
}
```

### Maintenance

```json
{
    "$schema": "https://schemas.wp.org/trunk/theme.json",
    "version": 3,
    "title": "My Theme",
    "description": "A modern block theme with custom styling",
    "author": "Your Name",
    "license": "GPL-2.0-or-later",
    "textdomain": "my-theme",
    "settings": {
        // Configuration here
    }
}
```

## Common Patterns

### E-commerce Theme

```json
{
    "settings": {
        "color": {
            "palette": [
                {
                    "color": "#2c5530",
                    "name": "Forest Green",
                    "slug": "forest-green"
                },
                {
                    "color": "#8b4513",
                    "name": "Brown",
                    "slug": "brown"
                },
                {
                    "color": "#ffd700",
                    "name": "Gold",
                    "slug": "gold"
                }
            ]
        },
        "blocks": {
            "woocommerce/cart": {
                "color": {
                    "palette": [
                        {
                            "color": "#2c5530",
                            "name": "Cart Primary",
                            "slug": "cart-primary"
                        }
                    ]
                }
            }
        }
    }
}
```

### Portfolio Theme

```json
{
    "settings": {
        "color": {
            "palette": [
                {
                    "color": "#000000",
                    "name": "Black",
                    "slug": "black"
                },
                {
                    "color": "#ffffff",
                    "name": "White",
                    "slug": "white"
                },
                {
                    "color": "#cccccc",
                    "name": "Light Gray",
                    "slug": "light-gray"
                }
            ]
        },
        "blocks": {
            "core/gallery": {
                "spacing": {
                    "blockGap": "var(--wp--preset--spacing--medium)"
                }
            }
        }
    }
}
```

## Official Documentation

https://developer.wordpress.org/themes/advanced-topics/theme-json/
https://developer.wordpress.org/themes/block-themes/
https://developer.wordpress.org/themes/advanced-topics/theme-json/data-driven-theme-creation/
