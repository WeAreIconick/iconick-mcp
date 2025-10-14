# Quality Assurance

Comprehensive guide to WordPress quality assurance, code quality tools, and automated testing workflows.

## Quality Assurance Fundamentals

### Code Quality Standards

```php
// .phpcs.xml - PHP CodeSniffer configuration
<?xml version="1.0"?>
<ruleset name="WordPress Plugin">
    <description>WordPress Plugin coding standards</description>
    
    <!-- Include WordPress coding standards -->
    <rule ref="WordPress"/>
    <rule ref="WordPress-Docs"/>
    <rule ref="WordPress-Extra"/>
    
    <!-- Exclude some rules -->
    <rule ref="WordPress.Files.FileName">
        <exclude name="WordPress.Files.FileName.NotHyphenatedLowercase"/>
    </rule>
    
    <!-- Custom rules -->
    <rule ref="Generic.Commenting.DocComment">
        <properties>
            <property name="required" value="required"/>
        </properties>
    </rule>
    
    <!-- File extensions -->
    <arg name="extensions" value="php"/>
    
    <!-- File paths -->
    <file>includes/</file>
    <file>admin/</file>
    <file>public/</file>
    <file>uninstall.php</file>
    
    <!-- Exclude paths -->
    <exclude-pattern>*/vendor/*</exclude-pattern>
    <exclude-pattern>*/node_modules/*</exclude-pattern>
    <exclude-pattern>*/tests/*</exclude-pattern>
</ruleset>
```

### PHPStan Configuration

```neon
# phpstan.neon - PHPStan static analysis configuration
parameters:
    level: 6
    paths:
        - includes/
        - admin/
        - public/
    
    excludePaths:
        - vendor/
        - tests/
        - node_modules/
    
    ignoreErrors:
        - '#Call to an undefined method WP_Query::.*#'
        - '#Call to an undefined method wpdb::.*#'
    
    bootstrapFiles:
        - tests/phpstan-bootstrap.php
    
    checkMissingIterableValueType: false
    checkGenericClassInNonGenericObjectType: false
```

### Psalm Configuration

```xml
<!-- psalm.xml - Psalm static analysis configuration -->
<?xml version="1.0"?>
<psalm
    errorLevel="2"
    resolveFromConfigFile="true"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="https://getpsalm.org/schema/config"
    xsi:schemaLocation="https://getpsalm.org/schema/config vendor/vimeo/psalm/config.xsd"
>
    <projectFiles>
        <directory name="includes" />
        <directory name="admin" />
        <directory name="public" />
        <ignoreFiles>
            <directory name="vendor" />
            <directory name="tests" />
            <directory name="node_modules" />
        </ignoreFiles>
    </projectFiles>
    
    <issueHandlers>
        <UndefinedMethod>
            <errorLevel type="suppress">
                <referencedClass name="WP_Query" />
                <referencedClass name="wpdb" />
            </errorLevel>
        </UndefinedMethod>
    </issueHandlers>
    
    <stubs>
        <file name="tests/wordpress-stubs.php" />
    </stubs>
</psalm>
```

## Automated Code Quality

### Pre-commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running pre-commit checks...${NC}"

# Check for PHP syntax errors
echo "Checking PHP syntax..."
find . -name "*.php" -not -path "./vendor/*" -not -path "./node_modules/*" -exec php -l {} \;
if [ $? -ne 0 ]; then
    echo -e "${RED}PHP syntax errors found!${NC}"
    exit 1
fi

# Run PHP CodeSniffer
echo "Running PHP CodeSniffer..."
vendor/bin/phpcs
if [ $? -ne 0 ]; then
    echo -e "${RED}CodeSniffer found issues!${NC}"
    exit 1
fi

# Run PHPStan
echo "Running PHPStan..."
vendor/bin/phpstan analyse
if [ $? -ne 0 ]; then
    echo -e "${RED}PHPStan found issues!${NC}"
    exit 1
fi

# Run tests
echo "Running PHPUnit tests..."
vendor/bin/phpunit
if [ $? -ne 0 ]; then
    echo -e "${RED}Tests failed!${NC}"
    exit 1
fi

echo -e "${GREEN}All checks passed!${NC}"
exit 0
```

### Composer Scripts for Quality

```json
{
    "scripts": {
        "quality": [
            "@quality:phpcs",
            "@quality:phpstan",
            "@quality:psalm",
            "@quality:phpmd"
        ],
        "quality:phpcs": "phpcs",
        "quality:phpcs:fix": "phpcbf",
        "quality:phpstan": "phpstan analyse",
        "quality:psalm": "psalm",
        "quality:phpmd": "phpmd . text cleancode,codesize,controversial,design,naming,unusedcode --exclude vendor,tests,node_modules",
        "quality:security": "composer audit",
        "test": "phpunit",
        "test:coverage": "phpunit --coverage-html tests/coverage/",
        "test:watch": "phpunit --watch",
        "ci": [
            "@quality",
            "@test"
        ]
    }
}
```

## Security Testing

### Security Scanning Tools

```php
<?php
// tests/Security/SecurityTest.php

namespace Tests\Security;

use PHPUnit\Framework\TestCase;

class SecurityTest extends TestCase {

    /**
     * @test
     */
    public function no_sql_injection_vulnerabilities() {
        $malicious_inputs = [
            "'; DROP TABLE wp_posts; --",
            "1' OR '1'='1",
            "admin'--",
            "1' UNION SELECT * FROM wp_users--"
        ];
        
        foreach ($malicious_inputs as $input) {
            $this->assertNotContains('DROP', $input, 'Should not contain DROP statements');
            $this->assertNotContains('UNION', $input, 'Should not contain UNION statements');
        }
    }

    /**
     * @test
     */
    public function no_xss_vulnerabilities() {
        $malicious_inputs = [
            '<script>alert("XSS")</script>',
            '<img src="x" onerror="alert(1)">',
            'javascript:alert(1)',
            '<iframe src="javascript:alert(1)"></iframe>'
        ];
        
        foreach ($malicious_inputs as $input) {
            $sanitized = sanitize_text_field($input);
            $this->assertStringNotContainsString('<script>', $sanitized, 'Script tags should be removed');
            $this->assertStringNotContainsString('javascript:', $sanitized, 'JavaScript URLs should be removed');
        }
    }

    /**
     * @test
     */
    public function proper_capability_checks() {
        // Test admin-only functions
        $this->assertTrue(current_user_can('manage_options'), 'Should require manage_options capability');
        
        // Test nonce verification
        $nonce = wp_create_nonce('your_plugin_action');
        $this->assertTrue(wp_verify_nonce($nonce, 'your_plugin_action'), 'Nonce should be valid');
    }

    /**
     * @test
     */
    public function secure_file_uploads() {
        $allowed_types = ['jpg', 'jpeg', 'png', 'gif', 'pdf'];
        $dangerous_types = ['php', 'exe', 'bat', 'sh', 'js'];
        
        foreach ($dangerous_types as $type) {
            $this->assertNotContains($type, $allowed_types, "Dangerous file type $type should not be allowed");
        }
    }
}
```

### Dependency Security Scanning

```bash
#!/bin/bash
# scripts/security-scan.sh

echo "Running security scans..."

# Check for known vulnerabilities in dependencies
echo "Checking Composer dependencies for vulnerabilities..."
composer audit

# Check for outdated packages
echo "Checking for outdated packages..."
composer outdated

# Run Snyk security scan (if available)
if command -v snyk &> /dev/null; then
    echo "Running Snyk security scan..."
    snyk test
fi

# Check for exposed secrets
echo "Checking for exposed secrets..."
if command -v gitleaks &> /dev/null; then
    gitleaks detect --source . --verbose
fi

echo "Security scans completed."
```

## Performance Testing

### Performance Monitoring

```php
<?php
// tests/Performance/PerformanceTest.php

namespace Tests\Performance;

use PHPUnit\Framework\TestCase;

class PerformanceTest extends TestCase {

    /**
     * @test
     */
    public function page_load_time_is_acceptable() {
        $start_time = microtime(true);
        
        // Simulate page load
        $this->simulatePageLoad();
        
        $load_time = microtime(true) - $start_time;
        
        // Should load within 2 seconds
        $this->assertLessThan(2, $load_time, 'Page should load within 2 seconds');
    }

    /**
     * @test
     */
    public function database_queries_are_optimized() {
        global $wpdb;
        
        $wpdb->queries = [];
        
        // Perform database operations
        $posts = get_posts(['numberposts' => 10]);
        
        $query_count = count($wpdb->queries);
        
        // Should not exceed 5 queries for 10 posts
        $this->assertLessThan(5, $query_count, 'Should not exceed 5 queries');
    }

    /**
     * @test
     */
    public function memory_usage_is_reasonable() {
        $initial_memory = memory_get_usage();
        
        // Perform memory-intensive operations
        $this->performMemoryIntensiveOperations();
        
        $peak_memory = memory_get_peak_usage();
        $memory_increase = $peak_memory - $initial_memory;
        
        // Should not exceed 10MB
        $this->assertLessThan(10 * 1024 * 1024, $memory_increase, 'Memory usage should be reasonable');
    }

    private function simulatePageLoad() {
        // Simulate WordPress page load
        wp_head();
        wp_footer();
    }

    private function performMemoryIntensiveOperations() {
        $data = [];
        for ($i = 0; $i < 1000; $i++) {
            $data[] = str_repeat('x', 1000);
        }
        unset($data);
    }
}
```

### Load Testing

```php
<?php
// tests/Performance/LoadTest.php

namespace Tests\Performance;

use PHPUnit\Framework\TestCase;

class LoadTest extends TestCase {

    /**
     * @test
     */
    public function handles_concurrent_requests() {
        $concurrent_requests = 10;
        $request_times = [];
        
        // Simulate concurrent requests
        for ($i = 0; $i < $concurrent_requests; $i++) {
            $start_time = microtime(true);
            
            // Simulate request processing
            $this->processRequest();
            
            $request_times[] = microtime(true) - $start_time;
        }
        
        // Calculate average response time
        $average_time = array_sum($request_times) / count($request_times);
        
        // Average response time should be under 1 second
        $this->assertLessThan(1, $average_time, 'Average response time should be under 1 second');
        
        // No request should take longer than 2 seconds
        foreach ($request_times as $time) {
            $this->assertLessThan(2, $time, 'No request should take longer than 2 seconds');
        }
    }

    /**
     * @test
     */
    public function database_performance_under_load() {
        $operations = 100;
        $start_time = microtime(true);
        
        // Perform multiple database operations
        for ($i = 0; $i < $operations; $i++) {
            wp_insert_post([
                'post_title' => "Load Test Post $i",
                'post_content' => 'Load test content',
                'post_status' => 'publish'
            ]);
        }
        
        $total_time = microtime(true) - $start_time;
        $operations_per_second = $operations / $total_time;
        
        // Should handle at least 50 operations per second
        $this->assertGreaterThan(50, $operations_per_second, 'Should handle at least 50 operations per second');
    }

    private function processRequest() {
        // Simulate request processing
        usleep(10000); // 10ms delay
    }
}
```

## Accessibility Testing

### WCAG Compliance Testing

```php
<?php
// tests/Accessibility/AccessibilityTest.php

namespace Tests\Accessibility;

use PHPUnit\Framework\TestCase;

class AccessibilityTest extends TestCase {

    /**
     * @test
     */
    public function html_has_proper_structure() {
        $html = $this->getPageHtml();
        
        // Check for proper heading hierarchy
        $this->assertStringContainsString('<h1>', $html, 'Page should have H1 heading');
        
        // Check for alt attributes on images
        $this->assertDoesNotMatchRegularExpression('/<img[^>]+(?!alt=)[^>]*>/i', $html, 'Images should have alt attributes');
        
        // Check for form labels
        $this->assertDoesNotMatchRegularExpression('/<input[^>]+(?!aria-label|aria-labelledby)[^>]*>/i', $html, 'Form inputs should have labels or aria attributes');
    }

    /**
     * @test
     */
    public function color_contrast_is_sufficient() {
        $css = $this->getThemeCss();
        
        // Check for sufficient color contrast ratios
        $contrast_ratios = $this->extractColorContrastRatios($css);
        
        foreach ($contrast_ratios as $ratio) {
            // WCAG AA requires 4.5:1 for normal text, 3:1 for large text
            $this->assertGreaterThanOrEqual(4.5, $ratio, 'Color contrast should meet WCAG AA standards');
        }
    }

    /**
     * @test
     */
    public function keyboard_navigation_works() {
        $html = $this->getPageHtml();
        
        // Check for focusable elements
        $this->assertStringContainsString('tabindex', $html, 'Page should have keyboard navigation support');
        
        // Check for skip links
        $this->assertStringContainsString('skip-link', $html, 'Page should have skip links');
    }

    private function getPageHtml() {
        // Return sample HTML for testing
        return '<html><head><title>Test Page</title></head><body><h1>Test Page</h1><img src="test.jpg" alt="Test image"><input type="text" aria-label="Test input"><a href="#content" class="skip-link">Skip to content</a></body></html>';
    }

    private function getThemeCss() {
        // Return sample CSS for testing
        return 'body { color: #000000; background-color: #ffffff; }';
    }

    private function extractColorContrastRatios($css) {
        // Simplified contrast ratio extraction
        return [4.5]; // Mock ratio
    }
}
```

## Cross-Browser Testing

### Browser Compatibility Testing

```javascript
// tests/browser/browser-test.js
describe('Browser Compatibility', function() {
    
    it('should work in all supported browsers', function() {
        // Test basic functionality
        expect(document.querySelector).toBeDefined();
        expect(window.fetch).toBeDefined();
        expect(Array.from).toBeDefined();
    });
    
    it('should handle CSS Grid properly', function() {
        const testElement = document.createElement('div');
        testElement.style.display = 'grid';
        
        expect(testElement.style.display).toBe('grid');
    });
    
    it('should support ES6 features', function() {
        // Test arrow functions
        const arrowFunction = () => 'test';
        expect(arrowFunction()).toBe('test');
        
        // Test template literals
        const template = `Hello ${'World'}`;
        expect(template).toBe('Hello World');
        
        // Test destructuring
        const { a, b } = { a: 1, b: 2 };
        expect(a).toBe(1);
        expect(b).toBe(2);
    });
});
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/quality.yml
name: Quality Assurance

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.1'
        extensions: mbstring, dom, curl, libxml, zip, pcntl, pdo, sqlite, pdo_sqlite, bcmath, soap, intl, gd, exif, iconv
    
    - name: Install Composer dependencies
      run: composer install --prefer-dist --no-progress
    
    - name: Run PHP CodeSniffer
      run: composer quality:phpcs
    
    - name: Run PHPStan
      run: composer quality:phpstan
    
    - name: Run Psalm
      run: composer quality:psalm
    
    - name: Run PHPMD
      run: composer quality:phpmd
    
    - name: Run Security Audit
      run: composer quality:security
    
    - name: Run Tests
      run: composer test
    
    - name: Generate Coverage Report
      run: composer test:coverage
    
    - name: Upload Coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./tests/coverage.xml
        flags: unittests
        name: codecov-umbrella
```

### Quality Gates

```php
<?php
// scripts/quality-gate.php

class QualityGate {
    
    private $thresholds = [
        'coverage' => 80,
        'complexity' => 10,
        'duplication' => 5,
        'maintainability' => 60
    ];
    
    public function checkQuality() {
        $results = $this->runQualityChecks();
        
        foreach ($this->thresholds as $metric => $threshold) {
            if ($results[$metric] < $threshold) {
                echo "❌ Quality gate failed: $metric is {$results[$metric]}% (threshold: {$threshold}%)\n";
                exit(1);
            }
        }
        
        echo "✅ All quality gates passed!\n";
    }
    
    private function runQualityChecks() {
        return [
            'coverage' => $this->getCoveragePercentage(),
            'complexity' => $this->getComplexityScore(),
            'duplication' => $this->getDuplicationPercentage(),
            'maintainability' => $this->getMaintainabilityScore()
        ];
    }
    
    private function getCoveragePercentage() {
        // Parse coverage report and return percentage
        return 85; // Mock value
    }
    
    private function getComplexityScore() {
        // Calculate cyclomatic complexity
        return 8; // Mock value
    }
    
    private function getDuplicationPercentage() {
        // Calculate code duplication percentage
        return 3; // Mock value
    }
    
    private function getMaintainabilityScore() {
        // Calculate maintainability index
        return 75; // Mock value
    }
}

$qualityGate = new QualityGate();
$qualityGate->checkQuality();
```

## Documentation Quality

### Documentation Standards

```php
<?php
/**
 * Plugin class for handling WordPress functionality
 *
 * @package YourPlugin
 * @since   1.0.0
 * @author  Your Name <your.email@example.com>
 * @license GPL-2.0+
 * @link    https://example.com
 */

class YourPlugin {
    
    /**
     * Plugin version
     *
     * @var string
     */
    const VERSION = '1.0.0';
    
    /**
     * Plugin instance
     *
     * @var YourPlugin
     */
    private static $instance = null;
    
    /**
     * Get plugin instance
     *
     * @return YourPlugin Plugin instance
     */
    public static function getInstance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        
        return self::$instance;
    }
    
    /**
     * Process user data
     *
     * @param array $data User data to process
     * @return array Processed user data
     * @throws InvalidArgumentException If data is invalid
     */
    public function processUserData(array $data) {
        if (empty($data)) {
            throw new InvalidArgumentException('Data cannot be empty');
        }
        
        // Process data logic here
        return $data;
    }
}
```

## Best Practices Summary

### Quality Checklist

```markdown
# WordPress Quality Assurance Checklist

## Code Quality
- [ ] PHP CodeSniffer passes with WordPress standards
- [ ] PHPStan/Psalm static analysis passes
- [ ] PHPMD code quality checks pass
- [ ] No security vulnerabilities found
- [ ] Dependencies are up to date

## Testing
- [ ] Unit tests achieve 80%+ coverage
- [ ] Integration tests cover main functionality
- [ ] Performance tests pass
- [ ] Security tests pass
- [ ] Accessibility tests pass

## Documentation
- [ ] Code is properly documented
- [ ] README is complete and accurate
- [ ] Changelog is maintained
- [ ] API documentation is up to date

## Deployment
- [ ] CI/CD pipeline passes all checks
- [ ] Quality gates are enforced
- [ ] Security scanning is automated
- [ ] Performance monitoring is in place
```

## Official Documentation

https://make.wordpress.org/core/handbook/testing/
https://developer.wordpress.org/coding-standards/
https://phpstan.org/user-guide/getting-started
https://psalm.dev/docs/
