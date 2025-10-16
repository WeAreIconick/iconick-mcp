# MCP Server Best Practices

## 📊 Current Server Status

**WordPress Development MCP Server**
- **Resources**: 78 (✅ Excellent coverage)
- **Tools**: 5 (✅ Good for WordPress management)
- **Prompts**: 0 (⚠️ Opportunity for improvement)

---

## 🎯 MCP Best Practices Overview

### 1. **Server Architecture** ✅

#### Current Implementation
```python
from fastmcp import FastMCP

mcp = FastMCP("WordPress Development Resources")
```

**✅ What you're doing right:**
- Clear, descriptive server name
- Using FastMCP framework for simplified development
- Proper resource organization

**🔄 Recommended improvements:**
- Add server metadata and version information
- Implement health check mechanism
- Add capability declarations

#### Enhanced Implementation

```python
from fastmcp import FastMCP
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server metadata
SERVER_VERSION = "2.0.0"
SERVER_NAME = "WordPress Development Resources"

mcp = FastMCP(
    name=SERVER_NAME,
    version=SERVER_VERSION
)

# Add server info endpoint
@mcp.resource("mcp://server/info")
def get_server_info() -> str:
    """MCP Server information and capabilities"""
    return f"""
# {SERVER_NAME} v{SERVER_VERSION}

## Capabilities
- 78 WordPress development resources
- 5 WordPress management tools
- Comprehensive documentation coverage

## Categories
- Core APIs, Security, Standards
- Blocks, Themes, Plugins
- Testing, Hosting, Performance
- Tools, Frameworks, Ecosystem
"""
```

---

### 2. **Security Best Practices** 🔒

#### Critical Security Measures

**A. Secrets Management** (if adding API features)

```python
# ❌ NEVER DO THIS
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "mypassword"

# ✅ DO THIS
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WORDPRESS_API_KEY")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")

# For your WordPress tools
@mcp.tool()
def wordpress_installer(target_dir: str, db_pass: str = None, **kwargs):
    """Install WordPress with secure credential handling"""
    # Get password from environment if not provided
    db_password = db_pass or os.getenv("WP_DB_PASSWORD", "")
    
    # Validate inputs
    if not target_dir or ".." in target_dir:
        return "Error: Invalid target directory"
    
    # Use secure subprocess call
    # ... implementation
```

**B. Input Validation** (for your current tools)

```python
import re
from pathlib import Path

def validate_wp_path(wp_path: str) -> bool:
    """Validate WordPress installation path"""
    if not wp_path:
        return False
    
    # Check for path traversal
    if ".." in wp_path:
        return False
    
    # Verify it's a real directory
    path = Path(wp_path)
    if not path.exists() or not path.is_dir():
        return False
    
    # Check for wp-config.php
    if not (path / "wp-config.php").exists():
        return False
    
    return True

@mcp.tool()
def plugin_manager(wp_path: str, action: str, **kwargs) -> str:
    """Manage WordPress plugins with validated inputs"""
    # Validate path
    if not validate_wp_path(wp_path):
        return "Error: Invalid WordPress installation path"
    
    # Validate action
    allowed_actions = ["list", "install", "activate", "deactivate", "search"]
    if action not in allowed_actions:
        return f"Error: Invalid action. Allowed: {', '.join(allowed_actions)}"
    
    # Validate plugin names (prevent command injection)
    if "plugin" in kwargs and kwargs["plugin"]:
        plugin = kwargs["plugin"]
        if not re.match(r'^[a-z0-9\-]+$', plugin):
            return "Error: Invalid plugin name format"
    
    # Safe to proceed
    # ... rest of implementation
```

**C. Sandbox Tool Execution**

```python
import subprocess
import os

def run_safe_command(cmd: list, timeout: int = 30) -> dict:
    """Run command with safety measures"""
    try:
        # Set safe environment
        safe_env = os.environ.copy()
        safe_env["PATH"] = "/usr/local/bin:/usr/bin:/bin"
        
        # Run with timeout and resource limits
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=safe_env,
            check=False
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

---

### 3. **Resource Organization** ✅

**Current Structure: EXCELLENT**

```
resources/
├── core/           # Core WordPress APIs
├── security/       # Security documentation
├── standards/      # Coding standards
├── blocks/         # Block editor
├── themes/         # Theme development
├── plugins/        # Plugin development
├── testing/        # Testing frameworks
├── tools/          # Development tools
└── ecosystem/      # Community resources
```

**✅ Best practices you're following:**
- Clear categorical organization
- Descriptive folder names
- Consistent file naming (kebab-case)
- Separation of concerns

**💡 Enhancement suggestion:**

Add a resource catalog:

```python
@mcp.resource("wordpress://catalog")
def get_resource_catalog() -> str:
    """Complete catalog of available resources"""
    categories = {
        "Core APIs": [
            "database", "http", "options", "transients",
            "rewrite", "settings", "shortcode", "metadata", "filesystem"
        ],
        "Security": [
            "data-validation", "sanitization", "escaping", "nonces",
            "capabilities", "sql-injection"
        ],
        # ... etc
    }
    
    catalog = "# WordPress Development Resources Catalog\n\n"
    for category, resources in categories.items():
        catalog += f"## {category}\n\n"
        for resource in resources:
            catalog += f"- `wordpress://{category.lower()}/{resource}`\n"
        catalog += "\n"
    
    return catalog
```

---

### 4. **Prompts** ⚠️ **Missing - High Priority**

**Why prompts are important:**
- Guide AI assistants in using your server effectively
- Provide context-aware workflows
- Improve user experience

**Recommended prompts to add:**

```python
@mcp.prompt()
def plugin_development_workflow():
    """Complete WordPress plugin development workflow"""
    return """
I'm developing a WordPress plugin. Guide me through:

1. Plugin structure and organization
2. Required header fields and validation
3. Security best practices (sanitization, escaping, nonces)
4. WordPress coding standards
5. Internationalization setup
6. Testing approach
7. Pre-submission checklist for WordPress.org

For each step, provide:
- Best practices
- Code examples
- Common pitfalls to avoid
- Links to relevant resources

Ask me questions about:
- Plugin purpose and functionality
- Target WordPress version
- Required capabilities
- Database requirements
"""

@mcp.prompt()
def security_audit():
    """WordPress security audit workflow"""
    return """
I need to perform a security audit on WordPress code.

Check for:
1. Input validation issues
2. Output escaping problems
3. SQL injection vulnerabilities
4. XSS vulnerabilities
5. CSRF protection (nonces)
6. Capability checks
7. File upload security
8. API security

For each issue found:
- Explain the vulnerability
- Show the vulnerable code
- Provide the secure fix
- Reference WordPress documentation
"""

@mcp.prompt()
def theme_development_guide():
    """Complete theme development workflow"""
    return """
I'm developing a WordPress theme. Guide me through:

1. Theme structure (template hierarchy)
2. Required files and functions
3. Enqueuing styles and scripts
4. Custom post type templates
5. Block theme vs classic theme decision
6. Performance optimization
7. Accessibility requirements
8. Mobile responsiveness

Provide examples for:
- Template files
- Functions.php setup
- Custom template parts
- Navigation menus
"""

@mcp.prompt()
def performance_optimization():
    """WordPress performance optimization workflow"""
    return """
I need to optimize WordPress performance.

Analyze and provide recommendations for:

1. **Database Optimization**
   - Query optimization
   - Index usage
   - Caching strategies

2. **Asset Optimization**
   - Script/style minification
   - Loading strategies (defer/async)
   - Image optimization

3. **Caching**
   - Object caching
   - Page caching
   - Transients usage

4. **Code Quality**
   - Inefficient queries
   - N+1 query problems
   - Memory usage

For each area:
- Show current issues
- Provide optimized code
- Explain performance impact
"""

@mcp.prompt()
def plugin_check_preparation():
    """Prepare plugin for WordPress.org submission"""
    return """
I'm preparing my plugin for WordPress.org submission.

Run through the complete Plugin Check checklist:

1. **Required Headers**
   - Verify all required fields
   - Check license compatibility
   - Validate version numbers

2. **Readme.txt**
   - Verify structure
   - Check stable tag
   - Validate tested up to version

3. **Security**
   - Check all input validation
   - Verify output escaping
   - Confirm nonce usage
   - Check capability checks

4. **Code Quality**
   - Check for deprecated functions
   - Verify coding standards
   - Check internationalization

5. **Files**
   - Remove development files
   - Check file types
   - Remove localhost references

For each issue found:
- Show the problematic code
- Explain why it's an issue
- Provide the fix
"""
```

---

### 5. **Error Handling** 🔧

**Current Implementation:**

```python
def load_resource_content(category: str, topic: str) -> str:
    """Load resource content from markdown files."""
    resource_path = RESOURCES_DIR / category / f"{topic}.md"
    if not resource_path.exists():
        raise FileNotFoundError(f"Resource not found: {category}/{topic}")
    with open(resource_path, 'r', encoding='utf-8') as f:
        return f.read()
```

**✅ Good: Raises clear errors**

**💡 Enhanced Implementation:**

```python
def load_resource_content(category: str, topic: str) -> str:
    """Load resource content with enhanced error handling"""
    try:
        resource_path = RESOURCES_DIR / category / f"{topic}.md"
        
        if not resource_path.exists():
            # Provide helpful error with available resources
            available = list(RESOURCES_DIR.glob(f"{category}/*.md"))
            suggestions = [f.stem for f in available[:5]]
            
            error_msg = f"Resource not found: {category}/{topic}\n"
            if suggestions:
                error_msg += f"Available in {category}: {', '.join(suggestions)}"
            
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        with open(resource_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Validate content
        if not content.strip():
            logger.warning(f"Empty resource: {category}/{topic}")
            return f"# {topic}\n\nContent is currently empty."
        
        logger.info(f"Loaded resource: {category}/{topic}")
        return content
        
    except UnicodeDecodeError as e:
        logger.error(f"Encoding error in {category}/{topic}: {e}")
        raise ValueError(f"Invalid file encoding: {category}/{topic}")
    except Exception as e:
        logger.error(f"Unexpected error loading {category}/{topic}: {e}")
        raise
```

---

### 6. **Performance Optimization** ⚡

**A. Resource Caching**

```python
from functools import lru_cache
from typing import Dict
import time

# Cache for resource content
_resource_cache: Dict[str, tuple[str, float]] = {}
CACHE_TTL = 3600  # 1 hour

@lru_cache(maxsize=128)
def load_resource_content_cached(category: str, topic: str) -> str:
    """Load resource content with LRU caching"""
    cache_key = f"{category}/{topic}"
    
    # Check cache
    if cache_key in _resource_cache:
        content, timestamp = _resource_cache[cache_key]
        if time.time() - timestamp < CACHE_TTL:
            return content
    
    # Load fresh content
    content = load_resource_content(category, topic)
    _resource_cache[cache_key] = (content, time.time())
    
    return content
```

**B. Lazy Loading**

```python
class LazyResource:
    """Lazy load resource content only when needed"""
    def __init__(self, category: str, topic: str):
        self.category = category
        self.topic = topic
        self._content = None
    
    def __str__(self):
        if self._content is None:
            self._content = load_resource_content(self.category, self.topic)
        return self._content
```

**C. Batch Operations**

```python
@mcp.tool()
def batch_plugin_install(wp_path: str, plugins: list) -> str:
    """Install multiple plugins efficiently"""
    results = []
    
    # Validate all inputs first
    if not validate_wp_path(wp_path):
        return "Error: Invalid WordPress path"
    
    for plugin in plugins:
        if not re.match(r'^[a-z0-9\-]+$', plugin):
            results.append(f"❌ {plugin}: Invalid plugin name")
            continue
        
        # Process plugin
        result = install_single_plugin(wp_path, plugin)
        results.append(f"{'✅' if result['success'] else '❌'} {plugin}: {result['message']}")
    
    return "\n".join(results)
```

---

### 7. **Documentation** 📚

**Current: Good docstrings**

```python
@mcp.resource("wordpress://core/database")
def get_database_api() -> str:
    """WordPress Database API (wpdb) - Queries, prepared statements, custom tables"""
```

**💡 Enhanced with examples:**

```python
@mcp.resource("wordpress://core/database")
def get_database_api() -> str:
    """
    WordPress Database API (wpdb) - Queries, prepared statements, custom tables
    
    Provides comprehensive documentation on:
    - Safe database queries with prepared statements
    - Custom table creation and management
    - Transaction handling
    - Query optimization
    
    Example usage:
        Ask: "How do I safely query the database?"
        Ask: "Show me how to create a custom table"
        Ask: "What's the best way to handle transactions?"
    
    Related resources:
        - wordpress://security/sql-injection
        - wordpress://performance/database-optimization
    """
    return load_resource_content("core", "database")
```

---

### 8. **Testing & Validation** ✅

**Recommended test structure:**

```python
# tests/test_mcp_server.py
import pytest
from wordpress_mcp import mcp, load_resource_content

def test_server_initialization():
    """Test server initializes correctly"""
    assert mcp.name == "WordPress Development Resources"

def test_resource_loading():
    """Test all resources can be loaded"""
    categories = ["core", "security", "standards", "blocks"]
    
    for category in categories:
        path = RESOURCES_DIR / category
        if path.exists():
            for resource_file in path.glob("*.md"):
                topic = resource_file.stem
                content = load_resource_content(category, topic)
                assert content
                assert len(content) > 0

def test_tool_validation():
    """Test tool input validation"""
    # Test invalid wp_path
    result = plugin_manager(wp_path="../etc/passwd", action="list")
    assert "Error" in result

def test_error_handling():
    """Test error handling"""
    with pytest.raises(FileNotFoundError):
        load_resource_content("nonexistent", "resource")
```

---

### 9. **Monitoring & Logging** 📊

**Enhanced logging:**

```python
import logging
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)

class MCPLogger:
    """Structured logger for MCP operations"""
    
    @staticmethod
    def log_resource_access(category: str, topic: str, success: bool):
        """Log resource access"""
        logger.info(
            "RESOURCE_ACCESS",
            extra={
                "category": category,
                "topic": topic,
                "success": success,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    @staticmethod
    def log_tool_execution(tool_name: str, args: dict, result: str):
        """Log tool execution"""
        logger.info(
            "TOOL_EXECUTION",
            extra={
                "tool": tool_name,
                "args": args,
                "result_length": len(result),
                "timestamp": datetime.now().isoformat()
            }
        )
```

---

### 10. **Rate Limiting** 🚦

**For tool operations:**

```python
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    """Simple rate limiter for tool operations"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed"""
        now = datetime.now()
        
        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Record request
        self.requests[client_id].append(now)
        return True

# Global rate limiter
rate_limiter = RateLimiter(max_requests=50, window_seconds=60)

@mcp.tool()
def plugin_manager_with_limit(wp_path: str, action: str, **kwargs) -> str:
    """Plugin manager with rate limiting"""
    client_id = "default"  # In production, get from context
    
    if not rate_limiter.is_allowed(client_id):
        return "Error: Rate limit exceeded. Please try again later."
    
    return plugin_manager(wp_path, action, **kwargs)
```

---

## 🎯 Priority Recommendations for Your Server

### High Priority (Implement Soon)

1. **✅ Add Prompts** (0 currently)
   - Plugin development workflow
   - Security audit workflow
   - Performance optimization workflow
   - Plugin Check preparation workflow

2. **🔒 Enhanced Input Validation**
   - Validate all tool inputs
   - Sanitize file paths
   - Prevent command injection

3. **📊 Add Logging**
   - Resource access tracking
   - Tool execution monitoring
   - Error tracking

### Medium Priority

4. **⚡ Performance Optimization**
   - Add resource caching
   - Implement batch operations
   - Optimize large resource loading

5. **📚 Enhanced Documentation**
   - Add usage examples in docstrings
   - Create resource catalog
   - Add cross-references between resources

6. **✅ Testing Framework**
   - Unit tests for all tools
   - Resource loading tests
   - Integration tests

### Low Priority (Nice to Have)

7. **🚦 Rate Limiting**
   - Prevent abuse of tools
   - Resource usage tracking

8. **📈 Analytics**
   - Track most used resources
   - Monitor tool usage patterns
   - Performance metrics

---

## 🔗 Implementation Checklist

### Immediate Actions

- [ ] Add 4-5 essential prompts (plugin dev, security, performance)
- [ ] Implement input validation for all tools
- [ ] Add structured logging
- [ ] Create server info resource
- [ ] Add resource catalog

### This Week

- [ ] Implement resource caching
- [ ] Add comprehensive error messages
- [ ] Write unit tests for tools
- [ ] Document all prompts
- [ ] Add usage examples

### This Month

- [ ] Add rate limiting
- [ ] Implement batch operations
- [ ] Create monitoring dashboard
- [ ] Performance profiling
- [ ] Security audit

---

## 📚 Additional Resources

- **MCP Specification**: https://modelcontextprotocol.io
- **FastMCP Documentation**: https://github.com/jlowin/fastmcp
- **Security Best Practices**: https://modelcontextprotocol.io/specification/draft/basic/security_best_practices
- **MCP Inspector**: https://github.com/modelcontextprotocol/inspector

---

## Summary

**Your server is already very strong** with 78 well-organized resources. The main improvements would be:

1. **Adding prompts** to guide AI assistants
2. **Enhanced security** for tool operations
3. **Better error handling** with helpful messages
4. **Performance optimization** through caching
5. **Monitoring** to track usage and issues

These improvements will make your MCP server production-ready and highly reliable! 🚀

