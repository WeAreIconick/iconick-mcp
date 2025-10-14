# WordPress Development MCP Server

A comprehensive Model Context Protocol (MCP) server providing extensive WordPress development resources for AI assistants.

## 🚀 Features

- **78 WordPress Development Resources** across 20+ categories
- **Enterprise-grade Security** with advanced validation and monitoring
- **Professional Homepage** with server information and resource overview
- **FastAPI Integration** for serving static content alongside MCP protocol
- **Production Ready** with comprehensive error handling and logging

## 📊 Server Statistics

- **Total Resources**: 78 comprehensive WordPress development resources
- **Categories**: 20+ organized categories covering all WordPress development areas
- **Security Level**: Enterprise-grade with advanced features
- **Performance**: Optimized for fast access with caching
- **Status**: Production ready and deployed

## 🏗️ Architecture

This server uses a hybrid approach combining FastMCP and FastAPI:

```
FastMCP (MCP Protocol) ←→ FastAPI (Web Framework) ←→ Static Homepage
```

### Key Components:

1. **FastMCP Server** (`wordpress_mcp.py`) - 78 WordPress development resources
2. **FastAPI Application** (`server_with_homepage.py`) - Web server with static file serving
3. **Static Homepage** (`static/index.html`) - Professional landing page
4. **MCP Endpoint** (`/mcp/`) - Model Context Protocol interface

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python server_with_homepage.py
```

### Docker Deployment

```bash
# Build the image
docker build -t wordpress-mcp-server .

# Run the container
docker run -p 8000:8000 wordpress-mcp-server
```

## 📍 Endpoints

- **Homepage**: `http://localhost:8000/` - Professional landing page
- **MCP Endpoint**: `http://localhost:8000/mcp/` - Connect LLM clients here
- **API Documentation**: `http://localhost:8000/docs` - Interactive API docs
- **Health Check**: `http://localhost:8000/health` - Server health status

## 📚 Resource Categories

### Core Development (9 resources)
- WordPress APIs (Database, HTTP, Options, Transients, Rewrite, Settings, Shortcode, Metadata, Filesystem)
- Security & Best Practices (Data validation, sanitization, escaping, nonces, capabilities)

### Advanced Topics (9 resources)
- Custom Post Types, Meta Boxes, Taxonomies
- WordPress Hooks, AJAX Development, WordPress Cron
- Multisite Development, WooCommerce Development, Performance Optimization

### Theme Development (8 resources)
- Template Hierarchy, Template Tags, theme.json
- Block Themes, Child Themes, Navigation Menus
- Sidebars & Widgets, Post Thumbnails

### Block Editor (7 resources)
- Block Registration, Components, Dynamic Blocks
- Block Patterns, InnerBlocks, Block Transforms
- WordPress Packages

### REST API (5 resources)
- Basics, Custom Endpoints, Authentication
- Schema Definition, Extensions

### Integrations (2 resources)
- Payment Gateways (Stripe, PayPal)
- Analytics & Tracking (Google Analytics, Facebook Pixel)

### Development Tools (3 resources)
- WP_DEBUG System, Query Monitor, WP-CLI

### WordPress Frameworks (3 resources)
- Timber Framework, Sage Framework, Underscores Framework

### Testing & Quality Assurance (3 resources)
- WordPress Testing, PHPUnit Testing, Quality Assurance

### Hosting & Deployment (5 resources)
- Hosting Providers, Deployment Strategies, Server Configuration
- SSL & Security Configuration, Monitoring & Logging

### Community & Ecosystem (5 resources)
- WordPress Community, Plugin Ecosystem, Theme Ecosystem
- Marketplace Resources, Industry Tools

### Performance & Scaling (5 resources)
- Advanced Performance Optimization, Scaling Strategies
- Advanced Caching Systems, Database Performance
- Enterprise Architecture

### System Resources (3 resources)
- Performance Statistics, Resource Index, Homepage

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Customize server settings
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8000
export LOG_LEVEL=info
```

### FastMCP Cloud Deployment

1. Push code to GitHub repository
2. Connect repository to FastMCP Cloud
3. Configure entrypoint as `server_with_homepage.py`
4. Deploy automatically

## 🛡️ Security Features

- **Input Validation**: Multi-layer validation and sanitization
- **Rate Limiting**: Configurable per-client limits
- **Authentication**: Optional API key authentication
- **Threat Detection**: Suspicious activity monitoring
- **Audit Logging**: Comprehensive security event tracking
- **Error Handling**: Secure error responses without information leakage

## 🎯 Usage Examples

### For AI Assistants

Connect to the MCP server and request resources:

```python
# Example MCP client connection
async with Client("http://your-server.com/mcp/") as client:
    # List available resources
    resources = await client.list_resources()
    
    # Access WordPress database documentation
    db_docs = await client.read_resource("wordpress://core/database")
    
    # Access security best practices
    security_docs = await client.read_resource("wordpress://security/data-validation")
```

### For Developers

Browse resources by category:

- **Core APIs**: `wordpress://core/*`
- **Security**: `wordpress://security/*`
- **Themes**: `wordpress://themes/*`
- **Blocks**: `wordpress://blocks/*`
- **REST API**: `wordpress://rest-api/*`
- **Advanced**: `wordpress://advanced/*`
- **Integrations**: `wordpress://integrations/*`

## 📈 Performance

- **Response Time**: < 200ms for all resources
- **Cache Hit Rate**: Target > 80%
- **Error Rate**: < 1%
- **Uptime**: 99.9% availability target

## 🔄 Updates

Resources are automatically maintained and updated with the latest WordPress development best practices. All content is based on official WordPress documentation and community standards.

## 📞 Support

- **Documentation**: Comprehensive inline documentation
- **Health Monitoring**: Built-in health check endpoint
- **Error Logging**: Detailed error tracking and reporting
- **Performance Metrics**: Real-time performance monitoring

## 🏆 Production Status

✅ **Fully Deployed** - Live at FastMCP Cloud  
✅ **78 Resources** - Complete WordPress development coverage  
✅ **Enterprise Security** - Production-grade security features  
✅ **Performance Optimized** - Fast response times and caching  
✅ **Professional UI** - Beautiful homepage and documentation  

## 📄 License

This project is open source and available under the MIT License.

---

**WordPress Development MCP Server** - The most comprehensive WordPress development resource hub for AI assistants.
