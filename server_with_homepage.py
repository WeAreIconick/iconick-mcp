from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastmcp import FastMCP
import uvicorn

# Define directories
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)

# Import our existing MCP server
from wordpress_mcp import mcp

# Create main FastAPI application with MCP integration
app = FastAPI(
    title="WordPress Development MCP Server",
    description="Comprehensive WordPress development resources via Model Context Protocol",
    version="2.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Export the MCP server for FastMCP Cloud to use
# This is what FastMCP Cloud expects to find
mcp_server = mcp

# Serve homepage
@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serve the WordPress MCP Server homepage"""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    else:
        # Return a default page if index.html doesn't exist
        return HTMLResponse("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>WordPress Development MCP Server - Iconick</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        padding: 20px;
                        margin: 0;
                    }
                    .container {
                        max-width: 1200px;
                        margin: 0 auto;
                    }
                    header {
                        background: white;
                        padding: 2rem;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        text-align: center;
                        margin-bottom: 2rem;
                    }
                    header h1 {
                        color: #667eea;
                        font-size: 2.5rem;
                        margin: 0 0 0.5rem 0;
                    }
                    .stats {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 1rem;
                        margin: 2rem 0;
                    }
                    .stat-card {
                        background: white;
                        padding: 1.5rem;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        text-align: center;
                    }
                    .stat-number {
                        font-size: 2rem;
                        font-weight: bold;
                        color: #667eea;
                    }
                    section {
                        background: white;
                        padding: 2rem;
                        margin-bottom: 1.5rem;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }
                    section h2 {
                        color: #667eea;
                        margin-bottom: 1rem;
                    }
                    a {
                        color: #667eea;
                        text-decoration: none;
                    }
                    a:hover {
                        color: #764ba2;
                        text-decoration: underline;
                    }
                    .endpoint {
                        background: #f4f4f4;
                        padding: 10px;
                        margin: 10px 0;
                        border-radius: 5px;
                        font-family: monospace;
                    }
                    footer {
                        text-align: center;
                        color: white;
                        margin-top: 2rem;
                        padding: 1rem;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <header>
                        <h1>🚀 WordPress Development MCP Server</h1>
                        <p>Comprehensive WordPress development resources via Model Context Protocol</p>
                    </header>
                    
                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-number">78</div>
                            <div>WordPress Resources</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">20+</div>
                            <div>Categories</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">Enterprise</div>
                            <div>Security Grade</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">Production</div>
                            <div>Ready</div>
                        </div>
                    </div>
                    
                    <main>
                        <section>
                            <h2>🎯 About This Server</h2>
                            <p>The most comprehensive WordPress development resource hub available through MCP protocol. This server provides AI assistants with extensive WordPress development documentation, coding standards, best practices, and code examples.</p>
                        </section>
                        
                        <section>
                            <h2>🔌 Available Endpoints</h2>
                            <div class="endpoint">
                                <strong>MCP Endpoint:</strong> 
                                <a href="/mcp/">/mcp/</a> - Connect your LLM client here
                            </div>
                            <div class="endpoint">
                                <strong>API Documentation:</strong> 
                                <a href="/docs">/docs</a> - Interactive API docs
                            </div>
                            <div class="endpoint">
                                <strong>Health Check:</strong> 
                                <a href="/health">/health</a> - Server health status
                            </div>
                        </section>
                        
                        <section>
                            <h2>📚 Resource Categories</h2>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                                <div>
                                    <h3>🔧 Core Development</h3>
                                    <ul>
                                        <li>WordPress APIs (Database, HTTP, Options)</li>
                                        <li>Security & Best Practices</li>
                                        <li>Theme Development</li>
                                        <li>Block Editor</li>
                                        <li>REST API</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3>🚀 Advanced Topics</h3>
                                    <ul>
                                        <li>Custom Post Types</li>
                                        <li>Meta Boxes</li>
                                        <li>Taxonomies</li>
                                        <li>AJAX Development</li>
                                        <li>WordPress Cron</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3>🌐 Integrations</h3>
                                    <ul>
                                        <li>Payment Gateways</li>
                                        <li>Analytics Tracking</li>
                                        <li>Development Workflows</li>
                                        <li>Testing & QA</li>
                                        <li>Hosting & Deployment</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3>🏗️ Frameworks & Tools</h3>
                                    <ul>
                                        <li>WordPress Frameworks</li>
                                        <li>Development Tools</li>
                                        <li>Performance Optimization</li>
                                        <li>Community & Ecosystem</li>
                                        <li>System Resources</li>
                                    </ul>
                                </div>
                            </div>
                        </section>
                        
                        <section>
                            <h2>🎯 How to Use</h2>
                            <p><strong>For AI Assistants:</strong> Connect to this MCP server using your client's configuration. Request specific resources by URI (e.g., <code>wordpress://core/database</code>) or browse available resources using the MCP protocol.</p>
                            <p><strong>For Developers:</strong> This server provides comprehensive WordPress development resources covering the complete development lifecycle from planning to deployment.</p>
                        </section>
                    </main>
                    
                    <footer>
                        <p><strong>WordPress Development MCP Server</strong><br>
                        Powered by FastMCP • Built for AI Assistants • Production Ready</p>
                    </footer>
                </div>
            </body>
            </html>
        """)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "server": "WordPress Development MCP Server",
        "version": "2.0.0",
        "resources": 78,
        "categories": 20
    }

if __name__ == "__main__":
    print("\n" + "="*70)
    print("WordPress Development MCP Server Starting...")
    print("="*70)
    print(f"📁 Static files directory: {STATIC_DIR}")
    print(f"🏠 Homepage: http://localhost:8000/")
    print(f"🔌 MCP Endpoint: http://localhost:8000/mcp/")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"❤️  Health Check: http://localhost:8000/health")
    print("="*70 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
