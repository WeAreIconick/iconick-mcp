# WordPress Accessibility Standards

Comprehensive accessibility standards and WCAG 2.1 AA compliance guidelines for WordPress development.

## WCAG 2.1 AA Compliance Overview

### The Four Principles of Accessibility

```html
<!-- POUR Principles Implementation -->

<!-- 1. Perceivable - Information must be presentable to users in ways they can perceive -->
<img src="image.jpg" 
     alt="Descriptive text explaining what the image shows"
     width="300" 
     height="200">

<!-- Audio content with transcripts -->
<audio controls>
    <source src="audio.mp3" type="audio/mpeg">
    <p>Your browser doesn't support audio. <a href="transcript.txt">Read the transcript</a>.</p>
</audio>

<!-- 2. Operable - Interface components must be operable -->
<button type="button" 
        onclick="toggleMenu()" 
        aria-expanded="false" 
        aria-controls="navigation-menu">
    Menu
</button>

<!-- 3. Understandable - Information and UI operation must be understandable -->
<label for="email-input">
    Email Address
    <span class="required" aria-label="Required field">*</span>
</label>
<input type="email" 
       id="email-input" 
       name="email" 
       required 
       aria-describedby="email-help">

<!-- 4. Robust - Content must be robust enough for various assistive technologies -->
<div role="main" aria-label="Main content">
    <h1>Page Title</h1>
    <p>Content goes here.</p>
</div>
```

## Semantic HTML Structure

### Proper Heading Hierarchy

```html
<!-- ✅ CORRECT: Proper heading hierarchy -->
<body>
    <header role="banner">
        <h1>Site Title</h1>
        <nav role="navigation" aria-label="Primary navigation">
            <h2 class="screen-reader-text">Main Menu</h2>
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/contact">Contact</a></li>
            </ul>
        </nav>
    </header>
    
    <main role="main">
        <article>
            <header>
                <h1>Article Title</h1>
                <p class="article-meta">Published on <time datetime="2024-01-15">January 15, 2024</time></p>
            </header>
            
            <section>
                <h2>Section Heading</h2>
                <p>Section content...</p>
                
                <h3>Subsection Heading</h3>
                <p>Subsection content...</p>
            </section>
        </article>
    </main>
    
    <aside role="complementary" aria-label="Sidebar">
        <h2>Related Content</h2>
        <!-- Sidebar content -->
    </aside>
    
    <footer role="contentinfo">
        <p>&copy; 2024 Your Site</p>
    </footer>
</body>

<!-- ❌ WRONG: Skipping heading levels -->
<h1>Page Title</h1>
<h3>Skipped h2 - This is wrong</h3>
<h2>This should come before h3</h2>
```

### Landmark Roles and Regions

```html
<!-- Proper landmark implementation -->
<div id="page" class="site">
    <!-- Skip links -->
    <a href="#main-content" class="skip-link screen-reader-text">
        Skip to main content
    </a>
    
    <header id="masthead" class="site-header" role="banner">
        <div class="site-branding">
            <h1 class="site-title">
                <a href="<?php echo esc_url(home_url('/')); ?>" rel="home">
                    <?php bloginfo('name'); ?>
                </a>
            </h1>
        </div>
        
        <nav id="site-navigation" class="main-navigation" role="navigation" aria-label="Primary Menu">
            <button class="menu-toggle" aria-controls="primary-menu" aria-expanded="false">
                <span class="screen-reader-text">Primary Menu</span>
                <span class="menu-icon" aria-hidden="true"></span>
            </button>
            
            <?php
            wp_nav_menu(array(
                'theme_location' => 'primary',
                'menu_id' => 'primary-menu',
                'container' => false,
                'fallback_cb' => false
            ));
            ?>
        </nav>
    </header>
    
    <main id="primary" class="site-main" role="main" aria-label="Main content">
        <section id="main-content" class="content-area">
            <!-- Main content -->
        </section>
    </main>
    
    <aside id="secondary" class="widget-area" role="complementary" aria-label="Sidebar">
        <!-- Sidebar content -->
    </aside>
    
    <footer id="colophon" class="site-footer" role="contentinfo">
        <!-- Footer content -->
    </footer>
</div>
```

## ARIA Implementation

### ARIA Labels and Descriptions

```html
<!-- ARIA labels for form controls -->
<form>
    <div class="form-group">
        <label for="username">Username</label>
        <input type="text" 
               id="username" 
               name="username" 
               aria-describedby="username-help"
               aria-required="true">
        <div id="username-help" class="form-help">
            Choose a unique username (3-20 characters)
        </div>
    </div>
    
    <div class="form-group">
        <label for="password">Password</label>
        <input type="password" 
               id="password" 
               name="password" 
               aria-describedby="password-requirements"
               aria-required="true">
        <div id="password-requirements" class="form-help">
            Password must be at least 8 characters long
        </div>
    </div>
</form>

<!-- ARIA labels for interactive elements -->
<button type="button" 
        aria-label="Close dialog" 
        aria-controls="modal-content">
    <span aria-hidden="true">&times;</span>
</button>

<!-- ARIA live regions for dynamic content -->
<div id="status-messages" 
     aria-live="polite" 
     aria-atomic="true" 
     class="screen-reader-text">
    <!-- Status messages will be announced here -->
</div>

<!-- ARIA expanded for collapsible content -->
<button type="button" 
        aria-expanded="false" 
        aria-controls="collapsible-content"
        onclick="toggleContent()">
    Show More Details
</button>
<div id="collapsible-content" 
     aria-hidden="true" 
     style="display: none;">
    <!-- Collapsible content -->
</div>
```

### ARIA Roles and States

```html
<!-- Navigation with proper ARIA -->
<nav role="navigation" aria-label="Breadcrumb">
    <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/category">Category</a></li>
        <li aria-current="page">Current Page</li>
    </ol>
</nav>

<!-- Search with ARIA -->
<form role="search" aria-label="Site search">
    <label for="search-input" class="screen-reader-text">
        Search this site
    </label>
    <input type="search" 
           id="search-input" 
           placeholder="Search..."
           aria-describedby="search-help">
    <button type="submit" aria-label="Submit search">
        Search
    </button>
    <div id="search-help" class="screen-reader-text">
        Press Enter to search or ESC to close
    </div>
</form>

<!-- Tab interface with ARIA -->
<div role="tablist" aria-label="Content sections">
    <button role="tab" 
            aria-selected="true" 
            aria-controls="tab-panel-1"
            id="tab-1">
        Overview
    </button>
    <button role="tab" 
            aria-selected="false" 
            aria-controls="tab-panel-2"
            id="tab-2">
        Details
    </button>
</div>

<div role="tabpanel" 
     aria-labelledby="tab-1" 
     id="tab-panel-1">
    <!-- Panel 1 content -->
</div>

<div role="tabpanel" 
     aria-labelledby="tab-2" 
     id="tab-panel-2"
     aria-hidden="true">
    <!-- Panel 2 content -->
</div>
```

## Focus Management

### Keyboard Navigation

```css
/* Focus indicators */
:focus {
    outline: 2px solid #0073aa;
    outline-offset: 2px;
}

.skip-link:focus {
    position: absolute;
    left: 6px;
    top: 7px;
    z-index: 999999;
    padding: 8px 16px;
    background: #000;
    color: #fff;
    text-decoration: none;
    border-radius: 4px;
}

/* Focus within containers */
.form-group:focus-within {
    border-color: #0073aa;
    box-shadow: 0 0 0 2px rgba(0, 115, 170, 0.2);
}

/* Custom focus styles for interactive elements */
.button:focus,
input:focus,
textarea:focus,
select:focus {
    outline: 2px solid #0073aa;
    outline-offset: 2px;
    box-shadow: 0 0 0 4px rgba(0, 115, 170, 0.2);
}

/* Remove default outline only when using custom focus */
.custom-focus:focus {
    outline: none;
    border: 2px solid #0073aa;
    box-shadow: 0 0 0 4px rgba(0, 115, 170, 0.2);
}
```

```javascript
// Focus management for modals and dynamic content
function openModal() {
    const modal = document.getElementById('modal');
    const firstFocusable = modal.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    
    modal.setAttribute('aria-hidden', 'false');
    modal.style.display = 'block';
    
    // Trap focus within modal
    trapFocus(modal);
    
    // Focus first focusable element
    if (firstFocusable) {
        firstFocusable.focus();
    }
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.setAttribute('aria-hidden', 'true');
    modal.style.display = 'none';
    
    // Return focus to trigger element
    const trigger = document.activeElement;
    if (trigger) {
        trigger.focus();
    }
}

// Focus trap implementation
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];
    
    element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusable) {
                    lastFocusable.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusable) {
                    firstFocusable.focus();
                    e.preventDefault();
                }
            }
        }
        
        if (e.key === 'Escape') {
            closeModal();
        }
    });
}
```

### Skip Links

```html
<!-- Skip links for keyboard users -->
<a href="#main-content" class="skip-link screen-reader-text">
    Skip to main content
</a>

<a href="#site-navigation" class="skip-link screen-reader-text">
    Skip to navigation
</a>

<a href="#search" class="skip-link screen-reader-text">
    Skip to search
</a>
```

```css
/* Skip link styles */
.skip-link {
    position: absolute;
    left: -9999px;
    top: 0;
    z-index: 999999;
    padding: 8px 16px;
    background: #000;
    color: #fff;
    text-decoration: none;
    border-radius: 0 0 4px 0;
    font-weight: 600;
}

.skip-link:focus {
    left: 6px;
    top: 7px;
}
```

## Color and Contrast

### Color Contrast Requirements

```css
/* WCAG AA Color Contrast Ratios */

/* Normal text: 4.5:1 minimum */
.text-normal {
    color: #333; /* #333 on white = 12.63:1 ✅ */
}

.text-muted {
    color: #666; /* #666 on white = 5.74:1 ✅ */
}

.text-light {
    color: #999; /* #999 on white = 2.85:1 ❌ Too low */
}

/* Large text: 3:1 minimum */
.text-large {
    font-size: 18px;
    color: #555; /* #555 on white = 9.97:1 ✅ */
}

/* Link states */
a {
    color: #0073aa; /* #0073aa on white = 4.53:1 ✅ */
    text-decoration: underline;
}

a:visited {
    color: #6366f1; /* #6366f1 on white = 4.58:1 ✅ */
}

a:hover,
a:focus {
    color: #005177; /* #005177 on white = 7.43:1 ✅ */
}

/* High contrast mode support */
@media (prefers-contrast: high) {
    .button {
        border: 2px solid currentColor;
        background: ButtonFace;
        color: ButtonText;
    }
    
    .card {
        border: 2px solid currentColor;
        background: Canvas;
        color: CanvasText;
    }
}
```

### Color Independence

```css
/* Don't rely on color alone to convey information */
.status-indicator {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.status-success::before {
    content: "✓";
    color: #00a32a;
}

.status-error::before {
    content: "✗";
    color: #d63638;
}

.status-warning::before {
    content: "⚠";
    color: #dba617;
}

/* Alternative: Use icons and text */
.status-success::before {
    content: "✓ Success: ";
    color: #00a32a;
    font-weight: bold;
}

.status-error::before {
    content: "✗ Error: ";
    color: #d63638;
    font-weight: bold;
}
```

## Images and Media

### Alternative Text

```html
<!-- Descriptive alternative text -->
<img src="chart.jpg" 
     alt="Bar chart showing sales increased 25% from Q1 to Q2 2024"
     width="400" 
     height="300">

<!-- Decorative images -->
<img src="decorative-border.png" 
     alt="" 
     role="presentation"
     width="100" 
     height="10">

<!-- Complex images with long descriptions -->
<img src="infographic.jpg" 
     alt="Infographic showing website traffic statistics for 2024"
     width="600" 
     height="800"
     longdesc="traffic-stats-detailed.html">

<!-- Images with captions -->
<figure>
    <img src="team-photo.jpg" 
         alt="Our development team working together in the office"
         width="800" 
         height="600">
    <figcaption>
        The WordPress development team collaborating on a new project.
        From left to right: Sarah (Frontend Developer), Mike (Backend Developer), 
        and Lisa (UX Designer).
    </figcaption>
</figure>
```

### Video and Audio

```html
<!-- Video with captions and transcripts -->
<video controls width="800" height="450">
    <source src="tutorial.mp4" type="video/mp4">
    <source src="tutorial.webm" type="video/webm">
    
    <track kind="captions" 
           src="tutorial-captions.vtt" 
           srclang="en" 
           label="English Captions">
    
    <track kind="descriptions" 
           src="tutorial-descriptions.vtt" 
           srclang="en" 
           label="English Descriptions">
    
    <p>
        Your browser doesn't support the video tag. 
        <a href="tutorial-transcript.txt">Read the transcript</a> or 
        <a href="tutorial.mp4">download the video</a>.
    </p>
</video>

<!-- Audio with transcripts -->
<audio controls>
    <source src="podcast-episode.mp3" type="audio/mpeg">
    <source src="podcast-episode.ogg" type="audio/ogg">
    
    <p>
        Your browser doesn't support the audio element. 
        <a href="podcast-transcript.txt">Read the transcript</a> or 
        <a href="podcast-episode.mp3">download the audio file</a>.
    </p>
</audio>
```

## Forms and Interactive Elements

### Accessible Form Design

```html
<!-- Accessible form with proper labels and error handling -->
<form novalidate>
    <fieldset>
        <legend>Contact Information</legend>
        
        <div class="form-group">
            <label for="first-name">
                First Name
                <span class="required" aria-label="Required field">*</span>
            </label>
            <input type="text" 
                   id="first-name" 
                   name="first_name" 
                   required 
                   aria-describedby="first-name-error"
                   aria-invalid="false">
            <div id="first-name-error" 
                 class="form-error" 
                 role="alert" 
                 aria-live="polite"></div>
        </div>
        
        <div class="form-group">
            <label for="email">
                Email Address
                <span class="required" aria-label="Required field">*</span>
            </label>
            <input type="email" 
                   id="email" 
                   name="email" 
                   required 
                   aria-describedby="email-error email-help"
                   aria-invalid="false">
            <div id="email-error" 
                 class="form-error" 
                 role="alert" 
                 aria-live="polite"></div>
            <div id="email-help" class="form-help">
                We'll never share your email address
            </div>
        </div>
        
        <div class="form-group">
            <fieldset>
                <legend>Preferred Contact Method</legend>
                
                <div class="radio-group">
                    <input type="radio" 
                           id="contact-email" 
                           name="contact_method" 
                           value="email" 
                           checked>
                    <label for="contact-email">Email</label>
                </div>
                
                <div class="radio-group">
                    <input type="radio" 
                           id="contact-phone" 
                           name="contact_method" 
                           value="phone">
                    <label for="contact-phone">Phone</label>
                </div>
                
                <div class="radio-group">
                    <input type="radio" 
                           id="contact-sms" 
                           name="contact_method" 
                           value="sms">
                    <label for="contact-sms">SMS</label>
                </div>
            </fieldset>
        </div>
        
        <div class="form-group">
            <label for="message">
                Message
                <span class="required" aria-label="Required field">*</span>
            </label>
            <textarea id="message" 
                      name="message" 
                      rows="5" 
                      required 
                      aria-describedby="message-error"
                      aria-invalid="false"></textarea>
            <div id="message-error" 
                 class="form-error" 
                 role="alert" 
                 aria-live="polite"></div>
        </div>
        
        <div class="form-actions">
            <button type="submit" class="button button-primary">
                Send Message
            </button>
            <button type="reset" class="button button-secondary">
                Clear Form
            </button>
        </div>
    </fieldset>
</form>
```

### Error Handling and Validation

```javascript
// Accessible form validation
function validateForm(form) {
    let isValid = true;
    const errors = {};
    
    // Clear previous errors
    form.querySelectorAll('.form-error').forEach(error => {
        error.textContent = '';
        error.setAttribute('aria-hidden', 'true');
    });
    
    form.querySelectorAll('[aria-invalid="true"]').forEach(field => {
        field.setAttribute('aria-invalid', 'false');
    });
    
    // Validate required fields
    form.querySelectorAll('[required]').forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            const errorId = field.getAttribute('aria-describedby');
            const errorElement = document.getElementById(errorId);
            
            if (errorElement) {
                errorElement.textContent = `${field.labels[0].textContent.replace('*', '').trim()} is required`;
                errorElement.setAttribute('aria-hidden', 'false');
            }
            
            field.setAttribute('aria-invalid', 'true');
            field.focus();
            return false;
        }
    });
    
    // Validate email format
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailField.value)) {
            isValid = false;
            const errorId = emailField.getAttribute('aria-describedby');
            const errorElement = document.getElementById(errorId);
            
            if (errorElement) {
                errorElement.textContent = 'Please enter a valid email address';
                errorElement.setAttribute('aria-hidden', 'false');
            }
            
            emailField.setAttribute('aria-invalid', 'true');
        }
    }
    
    // Show success message
    if (isValid) {
        showSuccessMessage('Form submitted successfully!');
    }
    
    return isValid;
}

function showSuccessMessage(message) {
    const statusElement = document.getElementById('status-messages');
    if (statusElement) {
        statusElement.textContent = message;
        statusElement.setAttribute('aria-hidden', 'false');
        
        // Hide message after 5 seconds
        setTimeout(() => {
            statusElement.textContent = '';
            statusElement.setAttribute('aria-hidden', 'true');
        }, 5000);
    }
}
```

## Motion and Animation

### Respecting User Preferences

```css
/* Respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}

/* Provide alternative for motion-heavy content */
.parallax-container {
    transform: none;
}

@media (prefers-reduced-motion: no-preference) {
    .parallax-container {
        transform: translateY(var(--parallax-offset));
        transition: transform 0.1s ease-out;
    }
}

/* Safe animations that don't cause vestibular disorders */
.safe-animation {
    animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Avoid problematic animations */
.avoid-animation {
    /* Don't use: spinning, flashing, or rapid movement */
    /* animation: spin 1s linear infinite; ❌ */
    /* animation: flash 0.5s infinite; ❌ */
    
    /* Use: gentle opacity, scale, or position changes */
    animation: gentleSlide 0.5s ease-out; /* ✅ */
}

@keyframes gentleSlide {
    from { 
        opacity: 0; 
        transform: translateY(10px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}
```

## Testing and Validation

### Accessibility Testing Tools

```html
<!-- Screen reader testing markup -->
<div class="screen-reader-test">
    <!-- Test content that should be announced -->
    <h1>Page Title</h1>
    <p>This content should be announced by screen readers.</p>
    
    <!-- Hidden content that shouldn't be announced -->
    <div class="visually-hidden">
        This content is visually hidden but still accessible.
    </div>
    
    <!-- Content that should never be announced -->
    <div aria-hidden="true">
        This decorative content is hidden from screen readers.
    </div>
</div>
```

```css
/* Screen reader only content */
.screen-reader-text {
    position: absolute !important;
    clip: rect(1px, 1px, 1px, 1px);
    width: 1px;
    height: 1px;
    overflow: hidden;
    word-wrap: normal;
}

/* Visually hidden but accessible */
.visually-hidden {
    position: absolute !important;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

/* Focusable visually hidden content */
.visually-hidden:focus {
    position: static !important;
    width: auto;
    height: auto;
    padding: inherit;
    margin: inherit;
    overflow: visible;
    clip: auto;
    white-space: inherit;
}
```

### WordPress-Specific Accessibility

```php
// WordPress accessibility functions
function theme_accessibility_features() {
    // Add theme support for accessibility features
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
        'style',
        'script'
    ));
    
    // Add skip link support
    add_theme_support('custom-logo', array(
        'height' => 100,
        'width' => 400,
        'flex-height' => true,
        'flex-width' => true,
    ));
}

add_action('after_setup_theme', 'theme_accessibility_features');

// Accessible navigation walker
class Accessible_Walker_Nav_Menu extends Walker_Nav_Menu {
    
    function start_el(&$output, $item, $depth = 0, $args = null, $id = 0) {
        $indent = ($depth) ? str_repeat("\t", $depth) : '';
        
        $classes = empty($item->classes) ? array() : (array) $item->classes;
        $classes[] = 'menu-item-' . $item->ID;
        
        $class_names = join(' ', apply_filters('nav_menu_css_class', array_filter($classes), $item, $args));
        $class_names = $class_names ? ' class="' . esc_attr($class_names) . '"' : '';
        
        $id = apply_filters('nav_menu_item_id', 'menu-item-'. $item->ID, $item, $args);
        $id = $id ? ' id="' . esc_attr($id) . '"' : '';
        
        $output .= $indent . '<li' . $id . $class_names .'>';
        
        $attributes = ! empty($item->attr_title) ? ' title="'  . esc_attr($item->attr_title) .'"' : '';
        $attributes .= ! empty($item->target)     ? ' target="' . esc_attr($item->target     ) .'"' : '';
        $attributes .= ! empty($item->xfn)        ? ' rel="'    . esc_attr($item->xfn        ) .'"' : '';
        $attributes .= ! empty($item->url)        ? ' href="'   . esc_attr($item->url        ) .'"' : '';
        
        // Add ARIA attributes
        if ($item->has_children) {
            $attributes .= ' aria-haspopup="true" aria-expanded="false"';
        }
        
        $item_output = isset($args->before) ? $args->before : '';
        $item_output .= '<a' . $attributes .'>';
        $item_output .= (isset($args->link_before) ? $args->link_before : '') . apply_filters('the_title', $item->title, $item->ID) . (isset($args->link_after) ? $args->link_after : '');
        $item_output .= '</a>';
        $item_output .= isset($args->after) ? $args->after : '';
        
        $output .= apply_filters('walker_nav_menu_start_el', $item_output, $item, $depth, $args);
    }
}
```

## Best Practices Summary

### Design and Development
- Use semantic HTML5 elements
- Implement proper heading hierarchy
- Provide alternative text for images
- Ensure keyboard navigation works
- Use sufficient color contrast
- Provide focus indicators

### Testing and Validation
- Test with screen readers (NVDA, JAWS, VoiceOver)
- Use keyboard-only navigation
- Validate with WAVE, axe, or similar tools
- Test with high contrast mode
- Verify with users who have disabilities

### WordPress Integration
- Use WordPress accessibility functions
- Implement skip links
- Add ARIA labels and roles
- Ensure forms are accessible
- Test with WordPress accessibility plugins

### Maintenance
- Regular accessibility audits
- User testing with disabled users
- Keep up with WCAG updates
- Train team on accessibility
- Document accessibility decisions

## Official Documentation

https://developer.wordpress.org/themes/advanced-topics/accessibility/
https://www.w3.org/WAI/WCAG21/quickref/
https://developer.mozilla.org/en-US/docs/Web/Accessibility
