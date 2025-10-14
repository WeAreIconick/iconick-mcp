# Contributing to Iconick MCP

Thank you for considering contributing to the WordPress Development MCP Server!

## How to Contribute

### Adding New Resources

1. **Create Resource File**
   ```bash
   # Add new markdown file in appropriate category
   resources/{category}/{topic}.md
   ```

2. **Add Resource Endpoint**
   Edit `wordpress_mcp.py`:
   ```python
   @mcp.resource("wordpress://{category}/{topic}")
   def get_{topic}() -> str:
       """Description of the resource"""
       return load_resource_content("{category}", "{topic}")
   ```

3. **Test Resource**
   ```bash
   python -c "from wordpress_mcp import mcp; print('OK')"
   ```

### Resource Guidelines

- **Accurate**: Verify against official WordPress documentation
- **Practical**: Include code examples
- **Secure**: Emphasize security best practices
- **Current**: Use latest WordPress versions (6.x+)
- **Well-formatted**: Use markdown properly

### Code Quality

Before submitting:

```bash
# Format
black .

# Lint
ruff check .

# Type check
mypy wordpress_mcp.py

# Test
python -m pytest
```

### Commit Messages

Follow conventional commits:

```
feat: add REST API authentication resource
fix: correct SQL injection example
docs: update README deployment steps
chore: update dependencies
```

### Pull Request Process

1. Fork the repository
2. Create feature branch (`git checkout -b feat/new-resource`)
3. Make changes
4. Run quality checks
5. Commit changes
6. Push to fork
7. Open Pull Request

### Resource Categories

- `core/` - WordPress Core APIs
- `security/` - Security best practices
- `standards/` - Coding standards
- `themes/` - Theme development
- `plugins/` - Plugin development
- `blocks/` - Gutenberg/Block development
- `hooks/` - Actions and filters
- `examples/` - Code examples
- `performance/` - Optimization
- `testing/` - Testing guides
- `accessibility/` - WCAG compliance
- `i18n/` - Internationalization

## Development Setup

```bash
git clone https://github.com/yourusername/iconick-mcp.git
cd iconick-mcp
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pre-commit install
```

## Questions?

Open an issue for discussion before major changes.

Thank you! 🙏
