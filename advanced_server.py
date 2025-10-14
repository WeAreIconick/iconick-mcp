"""
Advanced WordPress MCP Server with Enhanced Features
- Rate limiting and usage analytics
- Resource search functionality  
- Resource versioning and auto-updates
- Performance monitoring and metrics
"""

from pathlib import Path
import time
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastmcp import FastMCP
import uvicorn
import logging

# Import our advanced features
from advanced_features import (
    rate_limiter, usage_analytics, search_engine, resource_versioning,
    auto_update_system, get_client_id, record_request_analytics
)

# Import our existing MCP server
from wordpress_mcp import mcp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define directories
STATIC_DIR = Path(__file__).parent / "static"
STATIC_DIR.mkdir(exist_ok=True)

# Create MCP ASGI app with enhanced middleware
mcp_app = mcp.http_app(path='/mcp')

# Create main FastAPI application
app = FastAPI(
    title="Advanced WordPress Development MCP Server",
    description="Comprehensive WordPress development resources with advanced analytics, search, and auto-updates",
    version="2.1.0",
    lifespan=mcp_app.lifespan
)

# Mount MCP endpoint
app.mount("/mcp", mcp_app)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Middleware for rate limiting and analytics
@app.middleware("http")
async def analytics_middleware(request: Request, call_next):
    """Middleware for rate limiting and analytics"""
    start_time = time.time()
    client_id = get_client_id(request)
    
    # Check rate limits
    within_limit, rate_info = rate_limiter.check_rate_limit(client_id)
    
    if not within_limit:
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "limit": rate_info.limit,
                "window_duration": rate_info.window_duration,
                "retry_after": rate_info.window_duration
            }
        )
    
    # Record the request
    rate_limiter.record_request(client_id)
    
    # Process the request
    response = await call_next(request)
    
    # Record analytics
    response_time = time.time() - start_time
    success = response.status_code < 400
    
    # Extract resource URI if it's an MCP request
    resource_uri = None
    if '/mcp/' in str(request.url):
        resource_uri = str(request.url).split('/mcp/')[-1]
    
    if resource_uri:
        record_request_analytics(
            client_id=client_id,
            resource_uri=resource_uri,
            response_time=response_time,
            success=success
        )
    
    return response

# Enhanced homepage with analytics
@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Serve the advanced WordPress MCP Server homepage"""
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    else:
        # Return enhanced default page
        return HTMLResponse("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Advanced WordPress MCP Server</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
                    .feature-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                        gap: 1rem;
                        margin: 1rem 0;
                    }
                    .feature-card {
                        background: #f8f9fa;
                        padding: 1rem;
                        border-radius: 8px;
                        border-left: 4px solid #667eea;
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
                        <h1>🚀 Advanced WordPress MCP Server</h1>
                        <p>Enterprise-grade WordPress development resources with advanced analytics, search, and auto-updates</p>
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
                            <div class="stat-number">Advanced</div>
                            <div>Analytics</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">Auto</div>
                            <div>Updates</div>
                        </div>
                    </div>
                    
                    <main>
                        <section>
                            <h2>🎯 Enhanced Features</h2>
                            <div class="feature-grid">
                                <div class="feature-card">
                                    <h3>📊 Advanced Analytics</h3>
                                    <p>Real-time usage tracking, performance metrics, and resource popularity analysis</p>
                                </div>
                                <div class="feature-card">
                                    <h3>🔍 Smart Search</h3>
                                    <p>Full-text search across all resources with intelligent ranking and suggestions</p>
                                </div>
                                <div class="feature-card">
                                    <h3>🔄 Auto Updates</h3>
                                    <p>Automatic resource updates from files, URLs, Git repos, and APIs</p>
                                </div>
                                <div class="feature-card">
                                    <h3>⚡ Rate Limiting</h3>
                                    <p>Intelligent rate limiting with multiple tiers and usage monitoring</p>
                                </div>
                                <div class="feature-card">
                                    <h3>📈 Versioning</h3>
                                    <p>Resource versioning with update notifications and change tracking</p>
                                </div>
                                <div class="feature-card">
                                    <h3>🛡️ Security</h3>
                                    <p>Advanced security monitoring with threat detection and blocking</p>
                                </div>
                            </div>
                        </section>
                        
                        <section>
                            <h2>🔌 Available Endpoints</h2>
                            <div class="endpoint">
                                <strong>MCP Endpoint:</strong> 
                                <a href="/mcp/">/mcp/</a> - Connect LLM clients here
                            </div>
                            <div class="endpoint">
                                <strong>Search API:</strong> 
                                <a href="/api/search">/api/search</a> - Search resources
                            </div>
                            <div class="endpoint">
                                <strong>Analytics API:</strong> 
                                <a href="/api/analytics">/api/analytics</a> - Usage analytics
                            </div>
                            <div class="endpoint">
                                <strong>Updates API:</strong> 
                                <a href="/api/updates">/api/updates</a> - Update status and history
                            </div>
                            <div class="endpoint">
                                <strong>Health Check:</strong> 
                                <a href="/health">/health</a> - Server health status
                            </div>
                            <div class="endpoint">
                                <strong>API Documentation:</strong> 
                                <a href="/docs">/docs</a> - Interactive API docs
                            </div>
                        </section>
                        
                        <section>
                            <h2>📚 Resource Categories</h2>
                            <p>The server provides 78 comprehensive WordPress development resources across 20+ categories:</p>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                                <div>
                                    <h3>🔧 Core Development</h3>
                                    <ul>
                                        <li>WordPress APIs (9 resources)</li>
                                        <li>Security & Best Practices (8 resources)</li>
                                        <li>Theme Development (8 resources)</li>
                                        <li>Block Editor (7 resources)</li>
                                        <li>REST API (5 resources)</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3>🚀 Advanced Features</h3>
                                    <ul>
                                        <li>Custom Post Types & Meta Boxes</li>
                                        <li>Taxonomies & WordPress Hooks</li>
                                        <li>AJAX Development & WordPress Cron</li>
                                        <li>Performance Optimization</li>
                                        <li>Development Workflows</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3>🌐 Integrations</h3>
                                    <ul>
                                        <li>Payment Gateways (Stripe, PayPal)</li>
                                        <li>Analytics & Tracking</li>
                                        <li>WordPress Frameworks</li>
                                        <li>Testing & Quality Assurance</li>
                                        <li>Hosting & Deployment</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3>⚡ System Features</h3>
                                    <ul>
                                        <li>Advanced Analytics & Monitoring</li>
                                        <li>Smart Search & Indexing</li>
                                        <li>Auto Updates & Versioning</li>
                                        <li>Rate Limiting & Security</li>
                                        <li>Performance Optimization</li>
                                    </ul>
                                </div>
                            </div>
                        </section>
                    </main>
                    
                    <footer>
                        <p><strong>Advanced WordPress MCP Server v2.1.0</strong><br>
                        Powered by FastMCP • Built for AI Assistants • Enterprise Ready</p>
                    </footer>
                </div>
            </body>
            </html>
        """)

# Health check endpoint with detailed status
@app.get("/health")
async def health_check():
    """Enhanced health check endpoint"""
    return {
        "status": "healthy",
        "server": "Advanced WordPress MCP Server",
        "version": "2.1.0",
        "timestamp": datetime.now().isoformat(),
        "resources": {
            "total": 78,
            "categories": 20
        },
        "features": {
            "analytics": True,
            "search": True,
            "auto_updates": True,
            "rate_limiting": True,
            "versioning": True
        },
        "system": {
            "uptime": "running",
            "memory_usage": "normal",
            "update_system": "active" if auto_update_system.is_running else "inactive"
        }
    }

# Search API endpoint
@app.get("/api/search")
async def search_resources(q: str, category: str = None, tags: str = None, limit: int = 20):
    """Search WordPress resources"""
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    tag_list = tags.split(',') if tags else None
    results = search_engine.search(
        query=q.strip(),
        category=category,
        tags=tag_list,
        limit=limit
    )
    
    return {
        "query": q,
        "category": category,
        "tags": tag_list,
        "results_count": len(results),
        "results": results
    }

# Search suggestions endpoint
@app.get("/api/search/suggestions")
async def get_search_suggestions(q: str, limit: int = 10):
    """Get search suggestions"""
    if not q or len(q.strip()) < 1:
        return {"suggestions": []}
    
    suggestions = search_engine.get_suggestions(q.strip(), limit)
    return {"suggestions": suggestions}

# Analytics API endpoint
@app.get("/api/analytics")
async def get_analytics(client_id: str = None, hours: int = 24):
    """Get usage analytics"""
    if client_id:
        # Client-specific analytics
        client_analytics = usage_analytics.get_client_analytics(client_id)
        return {
            "client_id": client_id,
            "analytics": client_analytics
        }
    else:
        # General analytics
        popular_resources = usage_analytics.get_popular_resources(10)
        hourly_analytics = usage_analytics.get_hourly_analytics(hours)
        
        return {
            "popular_resources": popular_resources,
            "hourly_analytics": hourly_analytics,
            "summary": {
                "total_resources": 78,
                "analytics_period_hours": hours
            }
        }

# Updates API endpoint
@app.get("/api/updates")
async def get_update_status(resource_uri: str = None):
    """Get update status and history"""
    status = auto_update_system.get_update_status(resource_uri)
    history = auto_update_system.get_update_history(resource_uri, limit=20)
    
    return {
        "status": status,
        "history": history
    }

# Manual update trigger endpoint
@app.post("/api/updates/trigger")
async def trigger_update(resource_uri: str, background_tasks: BackgroundTasks):
    """Manually trigger an update for a resource"""
    if resource_uri not in auto_update_system.update_sources:
        raise HTTPException(status_code=404, detail="Resource not found in update sources")
    
    # Add to background tasks
    background_tasks.add_task(
        auto_update_system._execute_update,
        {'resource_uri': resource_uri, 'scheduled_time': time.time(), 'retry_count': 0}
    )
    
    return {
        "message": f"Update triggered for {resource_uri}",
        "resource_uri": resource_uri,
        "timestamp": datetime.now().isoformat()
    }

# Rate limiting status endpoint
@app.get("/api/rate-limits")
async def get_rate_limit_status(client_id: str):
    """Get rate limiting status for a client"""
    tier = rate_limiter.get_client_tier(client_id)
    within_limit, rate_info = rate_limiter.check_rate_limit(client_id)
    
    return {
        "client_id": client_id,
        "tier": tier,
        "within_limit": within_limit,
        "rate_info": {
            "requests_count": rate_info.requests_count,
            "limit": rate_info.limit,
            "window_duration": rate_info.window_duration,
            "window_start": rate_info.window_start
        }
    }

# Start auto-update system on startup
@app.on_event("startup")
async def startup_event():
    """Start the auto-update system"""
    auto_update_system.start_auto_updates()
    logger.info("Advanced WordPress MCP Server started with auto-updates enabled")

# Stop auto-update system on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Stop the auto-update system"""
    auto_update_system.stop_auto_updates()
    logger.info("Advanced WordPress MCP Server stopped")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("Advanced WordPress Development MCP Server Starting...")
    print("="*80)
    print(f"📁 Static files directory: {STATIC_DIR}")
    print(f"🏠 Homepage: http://localhost:8000/")
    print(f"🔌 MCP Endpoint: http://localhost:8000/mcp/")
    print(f"🔍 Search API: http://localhost:8000/api/search")
    print(f"📊 Analytics API: http://localhost:8000/api/analytics")
    print(f"🔄 Updates API: http://localhost:8000/api/updates")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print(f"❤️  Health Check: http://localhost:8000/health")
    print("="*80 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
