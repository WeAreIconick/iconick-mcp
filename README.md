# Iconick MCP - WordPress Development Resources

A comprehensive Model Context Protocol (MCP) server providing WordPress development resources, documentation, coding standards, and best practices to help AI assistants write better WordPress code.

## 🚀 Features

- **Comprehensive WordPress Documentation**: Core APIs, themes, plugins, security, and more
- **Coding Standards**: PHP, JavaScript, CSS, HTML, and SQL best practices
- **Security Guidelines**: Validation, sanitization, escaping, nonces, and capabilities
- **Code Examples**: Real-world patterns for common WordPress development tasks
- **Auto-Updated Resources**: GitHub Actions automatically fetch latest WordPress documentation
- **FastMCP Cloud Ready**: Deploy instantly to FastMCP Cloud

## 📋 Available Resources

### Core WordPress APIs
- Database API (wpdb)
- HTTP API
- Options API
- Transients API
- Settings API
- Metadata API
- Filesystem API
- Cron API
- Cache API

### Security Best Practices
- Data Validation
- Data Sanitization  
- Output Escaping
- Nonces (CSRF Protection)
- User Capabilities
- SQL Injection Prevention

### Coding Standards
- PHP Coding Standards
- JavaScript/ES6+ Standards
- CSS Best Practices
- HTML Standards
- SQL Optimization

### Development Areas
- Theme Development
- Plugin Development
- Block Development (Gutenberg)
- REST API
- Custom Post Types & Taxonomies
- Hooks & Filters
- Performance Optimization
- Accessibility (WCAG)
- Internationalization (i18n)
- Testing (PHPUnit, E2E)

## 🛠️ Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/iconick-mcp.git
cd iconick-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt

# Run the server locally
fastmcp run wordpress_mcp.py:mcp
```

### Validate Server

```bash
# Inspect the MCP server
fastmcp inspect wordpress_mcp.py:mcp

# Check for issues
python -c "from wordpress_mcp import mcp; print(f'Server: {mcp.name}')"
```

## ☁️ Deploy to FastMCP Cloud

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/iconick-mcp.git
   git push -u origin main
   ```

2. **Deploy to FastMCP Cloud**
   - Visit [fastmcp.cloud](https://fastmcp.cloud)
   - Sign in with GitHub
   - Create new project
   - Select your repository
   - Configure:
     - **Entrypoint**: `wordpress_mcp.py:mcp`
     - **Name**: `iconick-mcp` (or your preferred name)
     - **Authentication**: Enable if needed
   - Deploy!

3. **Your server will be available at**:
   ```
   https://your-project-name.fastmcp.app/mcp
   ```

## 🔄 Automatic Updates

The server includes GitHub Actions workflows that automatically:

- **Weekly Updates**: Fetches latest WordPress documentation every Monday
- **CI/CD**: Runs code quality checks on every commit
- **Security Scans**: Checks for vulnerabilities in dependencies
- **Deployment Validation**: Ensures server starts correctly

### Manual Resource Update

```bash
python scripts/update_resources.py
```

## 🔌 Using with AI Assistants

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "wordpress-dev": {
      "url": "https://your-project-name.fastmcp.app/mcp"
    }
  }
}
```

### Cursor

Add to your MCP settings:

```json
{
  "wordpress-dev": {
    "url": "https://your-project-name.fastmcp.app/mcp"
  }
}
```

## 📚 Resource URI Scheme

Resources are accessed via URIs:

```
wordpress://{category}/{topic}
```

Examples:
- `wordpress://core/database` - Database API documentation
- `wordpress://security/nonces` - Nonce security guide
- `wordpress://standards/php` - PHP coding standards
- `wordpress://examples/custom-post-types` - CPT examples

## 🧪 Development

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy wordpress_mcp.py

# Security scan
bandit -r . -c pyproject.toml

# Run all checks
pre-commit run --all-files
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Hooks will run automatically on git commit
```

## 🏗️ Project Structure

```
iconick-mcp/
├── wordpress_mcp.py          # Main MCP server
├── resources/                 # Documentation resources
│   ├── core/                 # Core WordPress APIs
│   ├── security/             # Security best practices
│   ├── standards/            # Coding standards
│   ├── themes/               # Theme development
│   ├── plugins/              # Plugin development
│   ├── blocks/               # Block development
│   └── ...                   # Other categories
├── scripts/                   # Automation scripts
│   ├── update_resources.py   # Update documentation
│   └── ...
├── .github/workflows/         # GitHub Actions
│   ├── ci.yml                # CI/CD pipeline
│   ├── update-resources.yml  # Auto-update resources
│   └── deploy-check.yml      # Deployment validation
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
├── pyproject.toml            # Project configuration
├── .pre-commit-config.yaml   # Pre-commit hooks
└── README.md                 # This file
```

## 🔒 Security

This MCP server follows security best practices:

- ✅ Input validation on all resource URIs
- ✅ Path traversal prevention
- ✅ Dependency vulnerability scanning
- ✅ Security-focused code linting (Bandit)
- ✅ Type safety with mypy
- ✅ Regular dependency updates via Dependabot

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run quality checks: `pre-commit run --all-files`
5. Submit a pull request

## 📖 Official WordPress Resources

This MCP aggregates and curates content from:

- [WordPress Developer Handbook](https://developer.wordpress.org/)
- [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/)
- [WordPress Core GitHub](https://github.com/WordPress/WordPress)
- [Plugin Handbook](https://developer.wordpress.org/plugins/)
- [Theme Handbook](https://developer.wordpress.org/themes/)
- [Block Editor Handbook](https://developer.wordpress.org/block-editor/)

## 📄 License

MIT License - feel free to use this project as you wish.

## 🙏 Acknowledgments

- WordPress Core Team for excellent documentation
- FastMCP for the amazing MCP framework
- Model Context Protocol community

## 🔗 Links

- [FastMCP Documentation](https://gofastmcp.com)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [WordPress Developer Resources](https://developer.wordpress.org)

---

**Built with ❤️ for the WordPress development community**
