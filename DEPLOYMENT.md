# Deployment Guide - Iconick MCP

## Quick Start (5 minutes)

### 1. Create GitHub Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: WordPress Development MCP Server"

# Create repo on GitHub, then:
git remote add origin https://github.com/yourusername/iconick-mcp.git
git branch -M main
git push -u origin main
```

### 2. Deploy to FastMCP Cloud

1. **Visit FastMCP Cloud**
   - Go to [https://fastmcp.cloud](https://fastmcp.cloud)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select your `iconick-mcp` repository
   - Or use the quickstart template

3. **Configure Project**
   ```
   Name: iconick-mcp (or your preferred name)
   Entrypoint: wordpress_mcp.py:mcp
   Authentication: Enable (recommended) or Disable (public)
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (~30 seconds)
   - Your server will be live at: `https://your-project-name.fastmcp.app/mcp`

### 3. Connect to AI Assistants

#### Claude Desktop

Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "wordpress-dev": {
      "url": "https://your-project-name.fastmcp.app/mcp"
    }
  }
}
```

Restart Claude Desktop.

#### Cursor

Add to Cursor MCP settings:

```json
{
  "wordpress-dev": {
    "url": "https://your-project-name.fastmcp.app/mcp"
  }
}
```

## Local Development & Testing

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Run Locally

```bash
# Run MCP server
fastmcp run wordpress_mcp.py:mcp

# Inspect server
fastmcp inspect wordpress_mcp.py:mcp

# Test resources
fastmcp test wordpress_mcp.py:mcp
```

### Code Quality

```bash
# Format code
black .

# Lint
ruff check .

# Type check
mypy wordpress_mcp.py

# Security scan
bandit -r . -c pyproject.toml

# Run all checks
pre-commit run --all-files
```

## Automatic Updates

The server automatically updates WordPress documentation weekly via GitHub Actions.

### Manual Update

```bash
python scripts/update_resources.py
git add resources/
git commit -m "chore: update WordPress resources"
git push
```

FastMCP Cloud will auto-deploy the changes.

## Environment Variables (Optional)

For production deployments with API access:

```bash
# .env file (never commit this)
WP_API_KEY=your_api_key_here
DEBUG=false
```

## Monitoring

- **GitHub Actions**: Check workflow runs for update status
- **FastMCP Cloud Dashboard**: Monitor deployment status and logs
- **Resource Updates**: Automatic weekly on Mondays at 2 AM UTC

## Troubleshooting

### Server won't start
- Check `wordpress_mcp.py` for syntax errors
- Ensure `requirements.txt` has correct dependencies
- Run `fastmcp inspect wordpress_mcp.py:mcp`

### Resources not loading
- Verify `.md` files exist in `resources/` directories
- Check file paths in `wordpress_mcp.py`
- Ensure files are committed to git

### Authentication issues
- Enable/disable authentication in FastMCP Cloud settings
- Check MCP configuration in AI assistant
- Verify URL is correct

## Next Steps

1. ✅ Deploy to FastMCP Cloud
2. ✅ Connect to Claude/Cursor
3. ✅ Test resources
4. 📝 Add more WordPress documentation
5. 🔄 Configure automatic updates
6. 🎨 Customize for your needs

## Support

- FastMCP Documentation: https://gofastmcp.com
- WordPress Developer Docs: https://developer.wordpress.org
- MCP Protocol: https://modelcontextprotocol.io

---

**Happy WordPress Development! 🚀**
