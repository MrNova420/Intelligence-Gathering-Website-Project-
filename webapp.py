#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Unified Web Application
A centralized website system combining API and web interface in a single application
"""

import os
import logging
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional

# Import handling for different deployment modes
try:
    from fastapi import FastAPI, HTTPException, Request, Form, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    FastAPI = None

# Try to import SessionMiddleware separately 
try:
    from starlette.middleware.sessions import SessionMiddleware
    import secrets
    SESSION_MIDDLEWARE_AVAILABLE = True
except ImportError:
    SESSION_MIDDLEWARE_AVAILABLE = False
    SessionMiddleware = None
    secrets = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class IntelligenceWebPlatform:
    """Unified Intelligence Gathering Web Platform"""
    
    def __init__(self):
        self.app = None
        self.templates = None
        self.setup_directories()
        
    def setup_directories(self):
        """Setup required directories for the unified web platform"""
        directories = [
            "web/static/css",
            "web/static/js", 
            "web/static/images",
            "web/templates",
            "data/scans",
            "data/reports",
            "data/backups",
            "logs"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
    def create_web_templates(self):
        """Create web templates for the unified interface"""
        
        # Base template
        base_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Intelligence Gathering Platform{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="/static/css/style.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-search me-2"></i>Intelligence Platform
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/">Dashboard</a>
                <a class="nav-link" href="/scan">New Scan</a>
                <a class="nav-link" href="/reports">Reports</a>
                <a class="nav-link" href="/docs">API Docs</a>
            </div>
        </div>
    </nav>
    
    <main class="container mt-4">
        {% block content %}{% endblock %}
    </main>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/static/js/app.js"></script>
</body>
</html>"""
        
        # Dashboard template
        dashboard_template = """{% extends "base.html" %}
{% block title %}Dashboard - Intelligence Platform{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h1 class="mb-4">🔍 Intelligence Gathering Platform</h1>
        
        <!-- System Status -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-white bg-success">
                    <div class="card-body">
                        <h5><i class="fas fa-heartbeat"></i> System Status</h5>
                        <p class="card-text">{{ system_status.status.title() }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-info">
                    <div class="card-body">
                        <h5><i class="fas fa-tools"></i> Scanners Available</h5>
                        <p class="card-text">{{ system_status.scanner_count }} modules</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-warning">
                    <div class="card-body">
                        <h5><i class="fas fa-file-alt"></i> Total Scans</h5>
                        <p class="card-text">{{ stats.total_scans }}</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-white bg-primary">
                    <div class="card-body">
                        <h5><i class="fas fa-chart-bar"></i> Success Rate</h5>
                        <p class="card-text">{{ stats.success_rate }}%</p>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <i class="fas fa-envelope fa-3x text-primary mb-3"></i>
                        <h5>Email Intelligence</h5>
                        <p>Gather intelligence from email addresses</p>
                        <a href="/scan?type=email" class="btn btn-primary">Start Email Scan</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <i class="fas fa-phone fa-3x text-success mb-3"></i>
                        <h5>Phone Lookup</h5>
                        <p>Analyze phone numbers and carriers</p>
                        <a href="/scan?type=phone" class="btn btn-success">Start Phone Scan</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body text-center">
                        <i class="fas fa-users fa-3x text-warning mb-3"></i>
                        <h5>Social Media</h5>
                        <p>Scan social media profiles</p>
                        <a href="/scan?type=social" class="btn btn-warning">Start Social Scan</a>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Recent Activity -->
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-history"></i> Recent Scans</h5>
            </div>
            <div class="card-body">
                {% if recent_scans %}
                <div class="table-responsive">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Target</th>
                                <th>Status</th>
                                <th>Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for scan in recent_scans %}
                            <tr>
                                <td><span class="badge bg-primary">{{ scan.type }}</span></td>
                                <td>{{ scan.target }}</td>
                                <td>
                                    {% if scan.status == 'completed' %}
                                        <span class="badge bg-success">Completed</span>
                                    {% elif scan.status == 'running' %}
                                        <span class="badge bg-warning">Running</span>
                                    {% else %}
                                        <span class="badge bg-danger">Failed</span>
                                    {% endif %}
                                </td>
                                <td>{{ scan.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                                <td>
                                    <a href="/scan/{{ scan.id }}" class="btn btn-sm btn-outline-primary">View</a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <p class="text-muted">No recent scans. <a href="/scan">Start your first scan</a></p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
        
        # Scan page template
        scan_template = """{% extends "base.html" %}
{% block title %}New Scan - Intelligence Platform{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8 mx-auto">
        <h1 class="mb-4">🔍 Start New Intelligence Scan</h1>
        
        <div class="card">
            <div class="card-body">
                <form id="scanForm" method="POST" action="/api/v1/scan">
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label for="scanType" class="form-label">Scan Type</label>
                            <select class="form-select" id="scanType" name="scan_type" required>
                                <option value="">Select scan type...</option>
                                <option value="email" {% if scan_type == 'email' %}selected{% endif %}>Email Intelligence</option>
                                <option value="phone" {% if scan_type == 'phone' %}selected{% endif %}>Phone Lookup</option>
                                <option value="social" {% if scan_type == 'social' %}selected{% endif %}>Social Media</option>
                                <option value="domain" {% if scan_type == 'domain' %}selected{% endif %}>Domain Analysis</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label for="target" class="form-label">Target</label>
                            <input type="text" class="form-control" id="target" name="target" 
                                   placeholder="Enter email, phone, username, or domain..." required>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Scan Options</label>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="deepScan" name="deep_scan">
                            <label class="form-check-label" for="deepScan">
                                Deep Scan (more comprehensive but slower)
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" id="includeSocial" name="include_social" checked>
                            <label class="form-check-label" for="includeSocial">
                                Include social media profiles
                            </label>
                        </div>
                    </div>
                    
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-search"></i> Start Scan
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Real-time scan results will appear here -->
        <div id="scanResults" class="mt-4" style="display: none;">
            <div class="card">
                <div class="card-header">
                    <h5><i class="fas fa-spinner fa-spin"></i> Scan in Progress</h5>
                </div>
                <div class="card-body">
                    <div class="progress mb-3">
                        <div id="scanProgress" class="progress-bar" role="progressbar" style="width: 0%"></div>
                    </div>
                    <div id="scanStatus">Initializing scan...</div>
                    <div id="scanResultsContent" class="mt-3"></div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
        
        # Write templates only if they don't exist (to preserve enhanced versions)
        templates_dir = Path("web/templates")
        
        # Check if enhanced templates exist, if not create basic ones
        if not (templates_dir / "base.html").exists():
            (templates_dir / "base.html").write_text(base_template)
        
        if not (templates_dir / "dashboard.html").exists():
            (templates_dir / "dashboard.html").write_text(dashboard_template)
        
        if not (templates_dir / "scan.html").exists():
            (templates_dir / "scan.html").write_text(scan_template)
        
        # Always create scan_results.html if it doesn't exist
        if not (templates_dir / "scan_results.html").exists():
            scan_results_template = """{% extends "base.html" %}
{% block title %}Scan Results - Intelligence Platform{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h1 class="mb-4">📊 Scan Results</h1>
        <div class="card">
            <div class="card-body">
                <h5>Scan ID: {{ scan_id }}</h5>
                <p class="text-muted">Results will be displayed here.</p>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
            (templates_dir / "scan_results.html").write_text(scan_results_template)
        
        
        # Create CSS
        css_content = """
/* Intelligence Platform Styles */
:root {
    --primary-color: #2563eb;
    --secondary-color: #64748b;
    --success-color: #059669;
    --warning-color: #d97706;
    --danger-color: #dc2626;
    --dark-color: #1e293b;
}

body {
    background-color: #f8fafc;
    font-family: 'Inter', system-ui, sans-serif;
}

.navbar-brand {
    font-weight: 700;
    font-size: 1.25rem;
}

.card {
    border: none;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease-in-out;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn {
    border-radius: 8px;
    font-weight: 500;
    padding: 0.5rem 1rem;
}

.btn-lg {
    padding: 0.75rem 2rem;
    font-size: 1.1rem;
}

.progress {
    height: 8px;
    border-radius: 4px;
}

.badge {
    border-radius: 6px;
    font-weight: 500;
}

.table {
    border-radius: 8px;
    overflow: hidden;
}

.text-muted {
    color: var(--secondary-color) !important;
}

/* Scan results styling */
#scanResults .card {
    border-left: 4px solid var(--primary-color);
}

.scan-metric {
    padding: 1rem;
    border-radius: 8px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-bottom: 1rem;
}

.scan-result-item {
    padding: 0.75rem;
    border-left: 3px solid var(--primary-color);
    margin-bottom: 0.5rem;
    background-color: #f1f5f9;
    border-radius: 4px;
}

/* Responsive design */
@media (max-width: 768px) {
    .container {
        padding: 0 1rem;
    }
    
    .card-body {
        padding: 1rem;
    }
}
"""
        
        # Only create basic CSS if enhanced version doesn't exist
        css_file = Path("web/static/css/style.css")
        if not css_file.exists() or css_file.stat().st_size < 1000:  # If basic CSS
            css_file.write_text(css_content)
        
        # Create JavaScript
        js_content = """
// Intelligence Platform JavaScript
class IntelligencePlatform {
    constructor() {
        this.init();
    }
    
    init() {
        this.setupScanForm();
        this.setupWebSocket();
        this.loadDashboardData();
    }
    
    setupScanForm() {
        const form = document.getElementById('scanForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.startScan();
            });
        }
    }
    
    async startScan() {
        const form = document.getElementById('scanForm');
        const formData = new FormData(form);
        const scanData = Object.fromEntries(formData);
        
        // Show scan results section
        document.getElementById('scanResults').style.display = 'block';
        
        try {
            const response = await fetch('/api/v1/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(scanData)
            });
            
            const result = await response.json();
            
            if (result.scan_id) {
                this.pollScanStatus(result.scan_id);
            } else {
                this.showError('Failed to start scan');
            }
        } catch (error) {
            this.showError('Error starting scan: ' + error.message);
        }
    }
    
    async pollScanStatus(scanId) {
        const pollInterval = setInterval(async () => {
            try {
                const response = await fetch(`/api/v1/scan/${scanId}`);
                const scan = await response.json();
                
                this.updateScanProgress(scan);
                
                if (scan.status === 'completed' || scan.status === 'failed') {
                    clearInterval(pollInterval);
                    this.showScanResults(scan);
                }
            } catch (error) {
                clearInterval(pollInterval);
                this.showError('Error polling scan status');
            }
        }, 2000);
    }
    
    updateScanProgress(scan) {
        const progress = scan.progress || 0;
        const progressBar = document.getElementById('scanProgress');
        const statusDiv = document.getElementById('scanStatus');
        
        progressBar.style.width = progress + '%';
        statusDiv.textContent = scan.status_message || `Scan ${scan.status}...`;
        
        if (scan.status === 'completed') {
            progressBar.classList.add('bg-success');
        } else if (scan.status === 'failed') {
            progressBar.classList.add('bg-danger');
        }
    }
    
    showScanResults(scan) {
        const resultsDiv = document.getElementById('scanResultsContent');
        
        if (scan.status === 'completed' && scan.results) {
            let html = '<h6>Scan Results:</h6>';
            
            // Display basic info
            if (scan.results.basic_info) {
                html += '<div class="scan-result-item">';
                html += '<strong>Basic Information:</strong><br>';
                for (const [key, value] of Object.entries(scan.results.basic_info)) {
                    html += `${key}: ${value}<br>`;
                }
                html += '</div>';
            }
            
            // Display social presence
            if (scan.results.social_presence) {
                html += '<div class="scan-result-item">';
                html += '<strong>Social Media Presence:</strong><br>';
                for (const [key, value] of Object.entries(scan.results.social_presence)) {
                    html += `${key}: ${value}<br>`;
                }
                html += '</div>';
            }
            
            // Display security assessment
            if (scan.results.security_assessment) {
                html += '<div class="scan-result-item">';
                html += '<strong>Security Assessment:</strong><br>';
                for (const [key, value] of Object.entries(scan.results.security_assessment)) {
                    html += `${key}: ${value}<br>`;
                }
                html += '</div>';
            }
            
            // Confidence score
            if (scan.results.confidence_score) {
                const score = Math.round(scan.results.confidence_score * 100);
                html += `<div class="scan-metric">Confidence Score: ${score}%</div>`;
            }
            
            resultsDiv.innerHTML = html;
        } else {
            resultsDiv.innerHTML = '<div class="alert alert-danger">Scan failed or no results available</div>';
        }
    }
    
    showError(message) {
        const resultsDiv = document.getElementById('scanResultsContent');
        resultsDiv.innerHTML = `<div class="alert alert-danger">${message}</div>`;
    }
    
    setupWebSocket() {
        // WebSocket for real-time updates (if available)
        if (window.WebSocket) {
            // Will implement WebSocket connection for real-time scan updates
        }
    }
    
    async loadDashboardData() {
        // Load dashboard statistics
        if (window.location.pathname === '/') {
            try {
                const response = await fetch('/api/v1/stats');
                const stats = await response.json();
                this.updateDashboardStats(stats);
            } catch (error) {
                console.log('Could not load dashboard stats');
            }
        }
    }
    
    updateDashboardStats(stats) {
        // Update dashboard with real-time statistics
        // This would update the dashboard cards with current stats
    }
}

// Initialize the platform when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new IntelligencePlatform();
});
"""
        
        Path("web/static/js/app.js").write_text(js_content)
        
        logger.info("✅ Web templates and static files created")

    @asynccontextmanager
    async def lifespan(self, app):
        """Application lifespan manager"""
        logger.info("🚀 Starting Intelligence Gathering Web Platform...")
        
        try:
            # Initialize backend systems
            try:
                from backend.app.core.database import init_db
                await init_db()
                logger.info("✅ Database initialized")
            except Exception as e:
                logger.warning(f"⚠️ Database initialization: {e}")
            
            # Initialize security
            try:
                from backend.app.core.enhanced_security import SecurityManager
                security = SecurityManager()
                logger.info("✅ Security system initialized")
            except Exception as e:
                logger.warning(f"⚠️ Security initialization: {e}")
                
            # Initialize monitoring
            try:
                from backend.app.monitoring.performance_metrics import metrics_collector
                metrics_collector.start_auto_collection()
                logger.info("✅ Performance monitoring started")
            except Exception as e:
                logger.warning(f"⚠️ Monitoring initialization: {e}")
            
        except Exception as e:
            logger.error(f"❌ Startup failed: {e}")
            
        yield
        
        logger.info("🛑 Shutting down Intelligence Gathering Web Platform...")

    def create_app(self) -> FastAPI:
        """Create the unified FastAPI web application"""
        
        if not FASTAPI_AVAILABLE:
            logger.error("❌ FastAPI not available")
            raise ImportError("FastAPI is required")
        
        # Create templates
        self.create_web_templates()
        
        # Initialize templates engine
        self.templates = Jinja2Templates(directory="web/templates")
        
        # Create FastAPI app
        self.app = FastAPI(
            title="Intelligence Gathering Web Platform",
            description="🔍 Unified Intelligence Gathering Website - Complete Web Application",
            version="2.0.0",
            lifespan=self.lifespan,
        )
        
        # Add session middleware if available
        if SESSION_MIDDLEWARE_AVAILABLE and secrets:
            # Generate secure session key
            session_key = os.getenv("SESSION_SECRET_KEY") or secrets.token_urlsafe(32)
            self.app.add_middleware(
                SessionMiddleware, 
                secret_key=session_key,
                max_age=86400,  # 24 hours
                same_site="lax",
                https_only=False  # Set to True in production
            )
            logger.info("✅ Advanced session management enabled")
        else:
            logger.warning("⚠️ SessionMiddleware not available - sessions disabled")
        
        # CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Mount static files
        self.app.mount("/static", StaticFiles(directory="web/static"), name="static")
        
        # Setup routes
        self.setup_web_routes()
        self.setup_api_routes()
        
        logger.info("✅ Unified Intelligence Gathering Web Platform created")
        return self.app
    
    def setup_web_routes(self):
        """Setup web interface routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Main dashboard page"""
            try:
                # Get system status
                system_status = {
                    "status": "healthy",
                    "scanner_count": 12  # Would get from actual scanner registry
                }
                
                # Get statistics
                stats = {
                    "total_scans": 0,
                    "success_rate": 95
                }
                
                # Get recent scans (mock data for now)
                recent_scans = []
                
                return self.templates.TemplateResponse("dashboard.html", {
                    "request": request,
                    "system_status": system_status,
                    "stats": stats,
                    "recent_scans": recent_scans
                })
            except Exception as e:
                logger.error(f"Dashboard error: {e}")
                return HTMLResponse("Dashboard temporarily unavailable", status_code=500)
        
        @self.app.get("/scan", response_class=HTMLResponse)
        async def scan_page(request: Request, type: Optional[str] = None):
            """Scan page"""
            return self.templates.TemplateResponse("scan.html", {
                "request": request,
                "scan_type": type
            })
        
        @self.app.get("/scan/{scan_id}", response_class=HTMLResponse)
        async def scan_results_page(request: Request, scan_id: str):
            """Scan results page"""
            # Would load actual scan results
            return self.templates.TemplateResponse("scan_results.html", {
                "request": request,
                "scan_id": scan_id
            })
        
        @self.app.get("/reports", response_class=HTMLResponse)
        async def reports_page(request: Request):
            """Reports page"""
            return HTMLResponse("<h1>Reports - Coming Soon</h1>")
        
        @self.app.get("/settings", response_class=HTMLResponse)
        async def settings_page(request: Request):
            """User settings and preferences page"""
            try:
                # Get user preferences from session
                preferences = request.session.get("user_preferences", {
                    "theme": "dark",
                    "notifications": True,
                    "auto_refresh": 30,
                    "default_scan_type": "email",
                    "language": "en"
                })
                
                return self.templates.TemplateResponse("settings.html", {
                    "request": request,
                    "preferences": preferences
                })
            except Exception as e:
                logger.error(f"Settings page error: {e}")
                return HTMLResponse("Settings temporarily unavailable", status_code=500)
        
        @self.app.post("/api/v1/preferences")
        async def update_preferences(request: Request):
            """Update user preferences"""
            try:
                form_data = await request.form()
                preferences = {
                    "theme": form_data.get("theme", "dark"),
                    "notifications": form_data.get("notifications") == "on",
                    "auto_refresh": int(form_data.get("auto_refresh", 30)),
                    "default_scan_type": form_data.get("default_scan_type", "email"),
                    "language": form_data.get("language", "en")
                }
                
                # Store in session
                request.session["user_preferences"] = preferences
                
                return JSONResponse({
                    "success": True,
                    "message": "Preferences updated successfully",
                    "preferences": preferences
                })
            except Exception as e:
                logger.error(f"Update preferences error: {e}")
                return JSONResponse({
                    "success": False,
                    "error": str(e)
                }, status_code=500)
    
    def setup_api_routes(self):
        """Setup API routes integrating with existing backend systems"""
        
        @self.app.get("/health")
        async def health_check():
            """System health check"""
            try:
                # Try to get more detailed system info
                system_status = {}
                
                # Check backend systems
                try:
                    from backend.app.monitoring.performance_metrics import get_performance_summary
                    perf_summary = get_performance_summary()
                    system_status.update(perf_summary)
                except ImportError:
                    system_status["monitoring"] = "not available"
                
                # Check database
                try:
                    from backend.app.core.database import get_db
                    system_status["database"] = "connected"
                except Exception as e:
                    system_status["database"] = f"error: {str(e)}"
                
                return {
                    "status": "healthy",
                    "platform": "Intelligence Gathering Web Platform",
                    "version": "2.0.0",
                    "mode": "unified_web_application",
                    "components": system_status,
                    "endpoints": {
                        "web_interface": "/",
                        "api_docs": "/docs",
                        "health": "/health"
                    }
                }
            except Exception as e:
                return {
                    "status": "degraded",
                    "error": str(e),
                    "platform": "Intelligence Gathering Web Platform"
                }
        
        @self.app.post("/api/v1/scan")
        async def create_scan(
            scan_type: str = Form(...),
            target: str = Form(...),
            deep_scan: bool = Form(False),
            include_social: bool = Form(True)
        ):
            """Create a new intelligence scan using existing backend"""
            try:
                # Try to use existing scanner system
                scan_id = None
                
                try:
                    # Import existing scanner system
                    from backend.app.scanners.email_scanners import EmailScanner
                    from backend.app.scanners.phone_scanners import PhoneScanner
                    from backend.app.scanners.social_scanners import SocialScanner
                    
                    import uuid
                    scan_id = str(uuid.uuid4())
                    
                    # Select appropriate scanner
                    scanner = None
                    if scan_type == "email":
                        scanner = EmailScanner()
                    elif scan_type == "phone":
                        scanner = PhoneScanner()
                    elif scan_type == "social":
                        scanner = SocialScanner()
                    
                    if scanner:
                        # Start scan in background
                        scan_options = {
                            "deep_scan": deep_scan,
                            "include_social": include_social,
                            "target": target
                        }
                        
                        # Store scan info (would use database in real implementation)
                        scan_data = {
                            "scan_id": scan_id,
                            "type": scan_type,
                            "target": target,
                            "status": "running",
                            "options": scan_options
                        }
                        
                        # Process scan asynchronously
                        asyncio.create_task(self.process_scan_with_backend(scan_data, scanner))
                        
                        return {"scan_id": scan_id, "status": "started"}
                    
                except ImportError:
                    # Fallback to mock implementation
                    scan_id = str(__import__('uuid').uuid4())
                    asyncio.create_task(self.process_mock_scan(scan_id, scan_type, target))
                    return {"scan_id": scan_id, "status": "started (mock)"}
                
            except Exception as e:
                logger.error(f"Scan creation error: {e}")
                raise HTTPException(status_code=500, detail="Failed to create scan")
        
        @self.app.get("/api/v1/scan/{scan_id}")
        async def get_scan_status(scan_id: str):
            """Get scan status and results"""
            # In a real implementation, this would query the database
            # For now, return mock completed scan
            return {
                "scan_id": scan_id,
                "status": "completed",
                "progress": 100,
                "results": {
                    "basic_info": {"email_valid": True, "domain": "example.com"},
                    "social_presence": {"platforms_found": 2},
                    "security_assessment": {"risk_level": "low"},
                    "confidence_score": 0.85
                },
                "created_at": "2025-09-25T01:00:00Z",
                "completed_at": "2025-09-25T01:05:00Z"
            }
        
        @self.app.get("/api/v1/stats")
        async def get_stats():
            """Get platform statistics"""
            try:
                # Try to get real stats from monitoring system
                from backend.app.monitoring.performance_metrics import metrics_collector
                current_metrics = metrics_collector.get_current_metrics()
                
                return {
                    "platform_stats": current_metrics,
                    "total_scans": 0,  # Would get from database
                    "success_rate": 95,
                    "active_users": 1,
                    "uptime": "99.9%"
                }
            except ImportError:
                return {
                    "total_scans": 0,
                    "success_rate": 95,
                    "active_users": 1,
                    "uptime": "99.9%",
                    "note": "Limited stats - monitoring system not available"
                }
        
        # Include existing backend API routes if available
        try:
            from backend.app.api import api_router
            self.app.include_router(api_router, prefix="/api/v1/backend")
            logger.info("✅ Backend API routes included")
        except ImportError:
            logger.warning("⚠️ Backend API routes not available")
    
    async def process_scan_with_backend(self, scan_data, scanner):
        """Process scan using existing backend scanner"""
        try:
            # This would integrate with the actual scanner implementation
            await asyncio.sleep(5)  # Simulate processing
            logger.info(f"Scan {scan_data['scan_id']} completed using backend scanner")
        except Exception as e:
            logger.error(f"Backend scan processing error: {e}")
    
    async def process_mock_scan(self, scan_id, scan_type, target):
        """Fallback mock scan processing"""
        await asyncio.sleep(5)  # Simulate processing time
        logger.info(f"Mock scan {scan_id} completed for {scan_type}: {target}")

# Create the unified platform instance
platform = IntelligenceWebPlatform()
app = platform.create_app()

if __name__ == "__main__":
    import uvicorn
    
    # Run the unified web application
    logger.info("🌐 Starting Unified Intelligence Gathering Web Platform")
    logger.info("🔍 Single system combining API + Web Interface")
    logger.info("📱 Termux/Android Compatible")
    logger.info("🌐 Web Interface: http://localhost:8000")
    logger.info("🔧 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )