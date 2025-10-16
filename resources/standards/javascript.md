---
difficulty: Beginner
tags: [standards, javascript, coding, style]
related: [standards/php, blocks/gutenberg-basics]
wp_version: All
---

# WordPress JavaScript Coding Standards

Official WordPress JavaScript coding standards and best practices.

## Modern JavaScript (ES6+)

WordPress supports modern JavaScript with transpilation via `@wordpress/scripts`.

### Variables

```javascript
// Use const for unchanging values
const API_URL = 'https://api.example.com';

// Use let for changing values
let count = 0;

// Avoid var
var oldStyle = 'avoid';  // ❌
```

### Functions

```javascript
// Arrow functions
const add = ( a, b ) => a + b;

// Function declarations
function calculateTotal( items ) {
	return items.reduce( ( sum, item ) => sum + item.price, 0 );
}

// Async/await
async function fetchData() {
	const response = await fetch( API_URL );
	const data = await response.json();
	return data;
}
```

### Template Literals

```javascript
// Use template literals for strings
const message = `Hello, ${ userName }!`;

// Multi-line strings
const html = `
	<div class="message">
		<h2>${ title }</h2>
		<p>${ content }</p>
	</div>
`;
```

### Destructuring

```javascript
// Object destructuring
const { title, content, author } = post;

// Array destructuring
const [ first, second, ...rest ] = items;

// Function parameters
function renderPost( { title, content, date } ) {
	// ...
}
```

### Spread Operator

```javascript
// Copy array
const newItems = [ ...items ];

// Merge objects
const settings = {
	...defaultSettings,
	...userSettings,
};
```

## WordPress JavaScript Patterns

### @wordpress/scripts

```javascript
// Import WordPress packages
import { __ } from '@wordpress/i18n';
import { useSelect } from '@wordpress/data';
import { Button } from '@wordpress/components';

// Use translation
const message = __( 'Hello World', 'textdomain' );
```

### jQuery (Legacy)

```javascript
// Wrap in ready
jQuery( document ).ready( function( $ ) {
	// Use $ safely
	$( '.button' ).on( 'click', function() {
		// Handle click
	} );
} );

// Or use IIFE
( function( $ ) {
	$( '.element' ).hide();
} )( jQuery );
```

### AJAX

```javascript
// Modern approach with fetch
async function saveData( data ) {
	const response = await fetch( ajaxurl, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded',
		},
		body: new URLSearchParams( {
			action: 'save_data',
			nonce: myData.nonce,
			data: JSON.stringify( data ),
		} ),
	} );
	
	return response.json();
}

// jQuery approach
jQuery.ajax( {
	url: ajaxurl,
	type: 'POST',
	data: {
		action: 'save_data',
		nonce: myData.nonce,
		data: formData,
	},
	success: function( response ) {
		console.log( response );
	},
} );
```

### wp.apiFetch (REST API)

```javascript
import apiFetch from '@wordpress/api-fetch';

// GET request
const posts = await apiFetch( { path: '/wp/v2/posts' } );

// POST request
const newPost = await apiFetch( {
	path: '/wp/v2/posts',
	method: 'POST',
	data: {
		title: 'My Post',
		content: 'Content here',
		status: 'publish',
	},
} );
```

## React Best Practices

### Functional Components

```javascript
import { useState } from '@wordpress/element';

function MyComponent( { initialValue } ) {
	const [ value, setValue ] = useState( initialValue );
	
	return (
		<div>
			<input
				type="text"
				value={ value }
				onChange={ ( e ) => setValue( e.target.value ) }
			/>
		</div>
	);
}
```

### Hooks

```javascript
import { useState, useEffect } from '@wordpress/element';

function DataComponent() {
	const [ data, setData ] = useState( null );
	
	useEffect( () => {
		fetchData().then( setData );
	}, [] );
	
	if ( ! data ) {
		return <Spinner />;
	}
	
	return <div>{ data.title }</div>;
}
```

## Code Style

### Indentation

```javascript
// Use tabs for indentation
function myFunction() {
	if ( condition ) {
		// code
	}
}
```

### Spacing

```javascript
// Space after keywords
if ( condition ) {
	// code
}

// Space around operators
const sum = a + b;

// No space after function name
myFunction( arg );

// Space after comma
const arr = [ 'one', 'two', 'three' ];
```

### Quotes

```javascript
// Use single quotes
const message = 'Hello World';

// Unless string contains single quote
const text = "It's a nice day";

// Or use template literals
const text = `It's a nice day`;
```

### Semicolons

```javascript
// Always use semicolons
const value = 123;
doSomething();
```

## Event Handling

### Event Listeners

```javascript
// Modern
element.addEventListener( 'click', handleClick );

function handleClick( event ) {
	event.preventDefault();
	// Handle click
}

// Remove listener
element.removeEventListener( 'click', handleClick );
```

### Event Delegation

```javascript
// Delegate to parent
document.addEventListener( 'click', function( event ) {
	if ( event.target.matches( '.button' ) ) {
		// Handle button click
	}
} );
```

## Error Handling

```javascript
// Try/catch
try {
	const data = JSON.parse( jsonString );
} catch ( error ) {
	console.error( 'Parse error:', error );
}

// Async/await error handling
async function fetchData() {
	try {
		const response = await fetch( url );
		if ( ! response.ok ) {
			throw new Error( 'Network error' );
		}
		return response.json();
	} catch ( error ) {
		console.error( 'Fetch error:', error );
		return null;
	}
}
```

## Performance

### Debouncing

```javascript
import { debounce } from '@wordpress/compose';

const debouncedSearch = debounce( ( value ) => {
	// Perform search
}, 300 );

<input onChange={ ( e ) => debouncedSearch( e.target.value ) } />
```

### Memoization

```javascript
import { useMemo } from '@wordpress/element';

const expensiveValue = useMemo( () => {
	return computeExpensiveValue( a, b );
}, [ a, b ] );
```

## ESLint Configuration

### .eslintrc.js

```javascript
module.exports = {
	extends: [ 'plugin:@wordpress/eslint-plugin/recommended' ],
	rules: {
		'@wordpress/no-unused-vars-before-return': 'error',
		'@wordpress/dependency-group': 'error',
	},
};
```

### Package Scripts

```json
{
	"scripts": {
		"lint:js": "wp-scripts lint-js",
		"format:js": "wp-scripts format-js"
	}
}
```

## Security

### XSS Prevention

```javascript
// Escape HTML
import { escapeHTML } from '@wordpress/escape-html';

const safe = escapeHTML( userInput );

// Create elements safely
const div = document.createElement( 'div' );
div.textContent = userInput;  // Safe
div.innerHTML = userInput;    // Unsafe!
```

### Nonce Verification

```javascript
// Include nonce in AJAX
wp_localize_script( 'my-script', 'myData', {
	ajaxurl: admin_url( 'admin-ajax.php' ),
	nonce: wp_create_nonce( 'my_action' ),
} );

// Use in request
fetch( myData.ajaxurl, {
	method: 'POST',
	body: new URLSearchParams( {
		action: 'my_action',
		nonce: myData.nonce,
	} ),
} );
```

## Official Resources

- https://developer.wordpress.org/coding-standards/wordpress-coding-standards/javascript/
- https://developer.wordpress.org/block-editor/reference-guides/packages/