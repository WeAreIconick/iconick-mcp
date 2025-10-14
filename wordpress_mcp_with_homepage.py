"""
WordPress MCP Server with Homepage Integration
- Extends the original wordpress_mcp.py to include homepage serving
- Designed to work with FastMCP Cloud
"""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastmcp import FastMCP
import uvicorn

# Define directories
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)

# Import the original MCP server
from wordpress_mcp import mcp

# Create a new FastAPI app that extends the MCP functionality
app = FastAPI(
    title="WordPress Development MCP Server",
    description="Comprehensive WordPress development resources via Model Context Protocol",
    version="2.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Serve homepage at root
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
                </style>
            </head>
            <body>
                <div class="container">
                    <header>
                        <h1>🚀 WordPress Development MCP Server</h1>
                        <p>Comprehensive WordPress development resources via Model Context Protocol</p>
                    </header>
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

# Export the original MCP server for FastMCP Cloud
# This is what FastMCP Cloud expects to find
mcp_server = mcp

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
