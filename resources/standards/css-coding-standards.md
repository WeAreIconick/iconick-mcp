# WordPress CSS Coding Standards

Comprehensive CSS coding standards and best practices for WordPress development.

## Basic CSS Standards

### Formatting and Structure

```css
/* WordPress CSS Coding Standards */

/* Use 4 spaces for indentation, no tabs */
.selector {
    property: value;
    another-property: value;
}

/* Use lowercase for selectors and properties */
.class-name {
    background-color: #ffffff;
    font-size: 16px;
    line-height: 1.5;
}

/* Use single quotes for strings */
.selector {
    content: 'Hello World';
    font-family: 'Helvetica Neue', Arial, sans-serif;
}

/* Use shorthand properties when possible */
.box {
    margin: 0 10px 20px 10px;
    padding: 10px 20px;
    border: 1px solid #ccc;
}

/* Group related properties */
.card {
    /* Positioning */
    position: relative;
    top: 0;
    left: 0;
    
    /* Box Model */
    width: 100%;
    height: auto;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    
    /* Typography */
    font-size: 14px;
    line-height: 1.6;
    color: #333;
    
    /* Visual */
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

### Selector Naming Conventions

```css
/* Use BEM (Block Element Modifier) methodology */

/* Block */
.card { }

/* Element */
.card__header { }
.card__title { }
.card__content { }
.card__footer { }

/* Modifier */
.card--featured { }
.card--large { }
.card--dark { }

/* Nested elements */
.card__header--compact { }
.card__title--primary { }

/* WordPress specific naming */
.wp-block-quote { }
.wp-block-image { }
.wp-block-gallery { }

/* Plugin specific naming */
.my-plugin-container { }
.my-plugin-button { }
.my-plugin-input { }

/* Theme specific naming */
.twenty-twenty-three-header { }
.twenty-twenty-three-footer { }
.twenty-twenty-three-sidebar { }
```

### CSS Organization

```css
/* 1. Reset/Normalize */
* {
    box-sizing: border-box;
}

/* 2. Base styles */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}

/* 3. Layout components */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.grid {
    display: grid;
    gap: 20px;
}

/* 4. Components */
.button {
    display: inline-block;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

.button--primary {
    background-color: #0073aa;
    color: white;
}

.button--secondary {
    background-color: #f0f0f0;
    color: #333;
}

/* 5. Utilities */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mb-1 { margin-bottom: 1rem; }
.mb-2 { margin-bottom: 2rem; }
.mb-3 { margin-bottom: 3rem; }

/* 6. Media queries */
@media (max-width: 768px) {
    .container {
        padding: 0 15px;
    }
    
    .grid {
        grid-template-columns: 1fr;
    }
}
```

## Advanced CSS Standards

### CSS Custom Properties (Variables)

```css
/* Define CSS custom properties at the root level */
:root {
    /* Colors */
    --color-primary: #0073aa;
    --color-secondary: #00a0d2;
    --color-success: #00a32a;
    --color-warning: #dba617;
    --color-error: #d63638;
    
    /* Typography */
    --font-size-base: 16px;
    --font-size-sm: 14px;
    --font-size-lg: 18px;
    --font-size-xl: 24px;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    
    /* Layout */
    --container-max-width: 1200px;
    --border-radius: 4px;
    --box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Use custom properties in components */
.button {
    background-color: var(--color-primary);
    font-size: var(--font-size-base);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
}

/* Override for dark theme */
@media (prefers-color-scheme: dark) {
    :root {
        --color-primary: #4f94cd;
        --color-secondary: #6bb6ff;
    }
}
```

### Responsive Design Patterns

```css
/* Mobile-first responsive design */

/* Base styles (mobile) */
.navigation {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.hero-section {
    padding: 2rem 1rem;
    text-align: center;
}

/* Tablet styles */
@media (min-width: 768px) {
    .navigation {
        flex-direction: row;
        justify-content: space-between;
    }
    
    .hero-section {
        padding: 4rem 2rem;
    }
}

/* Desktop styles */
@media (min-width: 1024px) {
    .navigation {
        gap: 2rem;
    }
    
    .hero-section {
        padding: 6rem 3rem;
    }
}

/* Large desktop */
@media (min-width: 1440px) {
    .hero-section {
        padding: 8rem 4rem;
    }
}

/* Container queries (modern approach) */
@container (min-width: 400px) {
    .card {
        display: flex;
        gap: 1rem;
    }
}
```

### CSS Grid and Flexbox

```css
/* CSS Grid for complex layouts */
.layout-grid {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    grid-template-rows: auto 1fr auto;
    grid-template-areas:
        "header header header"
        "sidebar main aside"
        "footer footer footer";
    gap: 2rem;
    min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

/* Responsive grid */
@media (max-width: 768px) {
    .layout-grid {
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "main"
            "sidebar"
            "aside"
            "footer";
    }
}

/* Flexbox for component layouts */
.card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.card__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card__content {
    flex: 1;
}

.card__footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
}
```

## WordPress-Specific CSS

### WordPress Admin Styles

```css
/* WordPress admin styling standards */
.wp-admin {
    /* Use WordPress admin color scheme */
    --wp-admin-theme-color: #0073aa;
    --wp-admin-theme-color-darker-10: #005a87;
    --wp-admin-theme-color-darker-20: #004a70;
}

/* Admin page styling */
.wrap {
    margin: 20px 20px 0 2px;
}

.form-table th {
    width: 200px;
    padding: 20px 10px 20px 0;
    font-weight: 600;
}

.form-table td {
    padding: 15px 10px;
}

/* WordPress buttons */
.button-primary {
    background: #0073aa;
    border-color: #0073aa;
    color: #fff;
    text-decoration: none;
    text-shadow: none;
    box-shadow: 0 1px 0 #006799;
}

.button-secondary {
    background: #f6f7f7;
    border-color: #ddd;
    color: #50575e;
}

/* WordPress form elements */
input[type="text"],
input[type="email"],
input[type="url"],
input[type="password"],
input[type="search"],
input[type="number"],
input[type="tel"],
input[type="range"],
input[type="date"],
input[type="month"],
input[type="week"],
input[type="time"],
input[type="datetime"],
input[type="datetime-local"],
input[type="color"],
textarea,
select {
    border: 1px solid #8c8f94;
    border-radius: 3px;
    color: #2c3338;
    font-size: 14px;
    line-height: 2;
    padding: 6px 8px;
}
```

### Block Editor Styles

```css
/* Block editor specific styles */
.wp-block {
    max-width: none;
}

.wp-block-quote {
    border-left: 4px solid #0073aa;
    margin: 0 0 1.75em 0;
    padding-left: 1em;
}

.wp-block-image {
    margin: 0 0 1em 0;
}

.wp-block-image img {
    height: auto;
    max-width: 100%;
}

.wp-block-gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
}

/* Block editor toolbar */
.block-editor-block-toolbar {
    background: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Block editor inspector */
.block-editor-block-inspector {
    background: #f9f9f9;
    border-left: 1px solid #ddd;
    padding: 1rem;
}
```

### Theme Customizer Styles

```css
/* Theme customizer specific styles */
.customize-control {
    margin-bottom: 1rem;
}

.customize-control-title {
    display: block;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.customize-control-description {
    color: #666;
    font-size: 0.9em;
    margin-top: 0.25rem;
}

/* Color picker */
.wp-color-picker {
    width: 80px;
    height: 30px;
    border: none;
    border-radius: 3px;
    cursor: pointer;
}

/* Range slider */
.customize-control-range input[type="range"] {
    width: 100%;
    margin: 0.5rem 0;
}

/* Typography controls */
.customize-control-typography select {
    width: 100%;
    margin-bottom: 0.5rem;
}
```

## Performance Optimization

### CSS Optimization Techniques

```css
/* Use efficient selectors */
/* Good - specific and fast */
.header .navigation .menu-item a { }

/* Bad - too generic */
div div div a { }

/* Use CSS containment */
.expensive-component {
    contain: layout style paint;
}

/* Use will-change sparingly */
.animated-element {
    will-change: transform;
}

.animated-element.animation-complete {
    will-change: auto;
}

/* Optimize animations */
@keyframes slideIn {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.animate-slide-in {
    animation: slideIn 0.3s ease-out;
    animation-fill-mode: both;
}

/* Use transform instead of changing layout properties */
.smooth-move {
    transition: transform 0.3s ease;
}

.smooth-move:hover {
    transform: translateY(-5px);
}
```

### Critical CSS

```css
/* Critical CSS for above-the-fold content */
/* Inline critical CSS in <head> */

/* Header styles */
.site-header {
    background: #fff;
    border-bottom: 1px solid #ddd;
    padding: 1rem 0;
}

.site-title {
    font-size: 1.5rem;
    font-weight: 700;
    color: #333;
    text-decoration: none;
}

/* Navigation */
.main-navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Hero section */
.hero-section {
    background: linear-gradient(135deg, #0073aa, #00a0d2);
    color: white;
    padding: 4rem 2rem;
    text-align: center;
}

.hero-title {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

/* Load non-critical CSS asynchronously */
<link rel="preload" href="non-critical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

## Accessibility Standards

### WCAG 2.1 AA Compliance

```css
/* Focus indicators */
.focusable:focus {
    outline: 2px solid #0073aa;
    outline-offset: 2px;
}

/* Skip links */
.skip-link {
    position: absolute;
    left: -9999px;
    top: 0;
    z-index: 999999;
    padding: 8px 16px;
    background: #000;
    color: #fff;
    text-decoration: none;
}

.skip-link:focus {
    left: 6px;
    top: 7px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    .button {
        border: 2px solid currentColor;
    }
    
    .card {
        border: 1px solid #000;
    }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Color contrast ratios */
/* Ensure 4.5:1 contrast ratio for normal text */
.text-normal {
    color: #333; /* #333 on white = 12.63:1 */
}

.text-muted {
    color: #666; /* #666 on white = 5.74:1 */
}

/* Ensure 3:1 contrast ratio for large text */
.text-large {
    font-size: 18px;
    color: #555; /* #555 on white = 9.97:1 */
}
```

## CSS Architecture Patterns

### Component-Based Architecture

```css
/* Base component styles */
.component {
    /* Component variables */
    --component-padding: 1rem;
    --component-border-radius: 4px;
    --component-background: #fff;
    --component-border: 1px solid #ddd;
    
    /* Component styles */
    padding: var(--component-padding);
    border-radius: var(--component-border-radius);
    background: var(--component-background);
    border: var(--component-border);
}

/* Component modifiers */
.component--large {
    --component-padding: 2rem;
}

.component--dark {
    --component-background: #333;
    --component-border: 1px solid #666;
    color: #fff;
}

/* Component elements */
.component__header {
    margin-bottom: 1rem;
    font-weight: 600;
}

.component__content {
    line-height: 1.6;
}

.component__footer {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
}

/* Component states */
.component.is-active {
    --component-background: #0073aa;
    color: #fff;
}

.component.is-disabled {
    opacity: 0.6;
    pointer-events: none;
}
```

### Utility-First Approach

```css
/* Utility classes */
.m-0 { margin: 0; }
.m-1 { margin: 0.25rem; }
.m-2 { margin: 0.5rem; }
.m-3 { margin: 1rem; }
.m-4 { margin: 1.5rem; }
.m-5 { margin: 3rem; }

.mt-0 { margin-top: 0; }
.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-3 { margin-top: 1rem; }
.mt-4 { margin-top: 1.5rem; }
.mt-5 { margin-top: 3rem; }

.p-0 { padding: 0; }
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 1rem; }
.p-4 { padding: 1.5rem; }
.p-5 { padding: 3rem; }

.text-xs { font-size: 0.75rem; }
.text-sm { font-size: 0.875rem; }
.text-base { font-size: 1rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }
.text-2xl { font-size: 1.5rem; }

.font-normal { font-weight: 400; }
.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }

.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.text-justify { text-align: justify; }

.flex { display: flex; }
.inline-flex { display: inline-flex; }
.grid { display: grid; }
.block { display: block; }
.inline-block { display: inline-block; }
.hidden { display: none; }

.justify-start { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-end { justify-content: flex-end; }
.justify-between { justify-content: space-between; }

.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.items-end { align-items: flex-end; }
.items-stretch { align-items: stretch; }
```

## Best Practices Summary

### Code Organization
- Use consistent indentation (4 spaces)
- Group related properties together
- Use meaningful class names (BEM methodology)
- Organize CSS in logical sections

### Performance
- Minimize CSS file size
- Use efficient selectors
- Leverage CSS custom properties
- Implement critical CSS
- Use CSS containment where appropriate

### Maintainability
- Use consistent naming conventions
- Document complex CSS with comments
- Use CSS custom properties for theming
- Follow component-based architecture
- Implement utility classes for common patterns

### Accessibility
- Ensure proper color contrast ratios
- Provide focus indicators
- Support reduced motion preferences
- Use semantic HTML with appropriate CSS
- Test with screen readers

### Browser Support
- Use progressive enhancement
- Provide fallbacks for modern CSS features
- Test across target browsers
- Use CSS prefixes when necessary
- Leverage feature queries (@supports)

## Official Documentation

https://developer.wordpress.org/coding-standards/wordpress-coding-standards/css/
https://developer.wordpress.org/themes/basics/main-stylesheet-style-css/
https://developer.wordpress.org/block-editor/how-to-guides/themes/theme-support/
