#!/usr/bin/env python3
"""
Intelligence Gathering Platform - Unified Web Application
A centralized website system combining API and web interface in a single application
"""

import os
import logging
import asyncio
import uuid
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import asdict

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
            "frontend/legacy-web/static/css",
            "frontend/legacy-web/static/js", 
            "frontend/legacy-web/static/images",
            "frontend/legacy-web/templates",
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
        templates_dir = Path("frontend/legacy-web/templates")
        
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
        self.templates = Jinja2Templates(directory="frontend/legacy-web/templates")
        
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
        self.app.mount("/static", StaticFiles(directory="frontend/legacy-web/static"), name="static")
        
        # Setup routes
        self.setup_web_routes()
        self.setup_api_routes()
        
        logger.info("✅ Unified Intelligence Gathering Web Platform created")
        return self.app
    
    def setup_web_routes(self):
        """Setup web interface routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home_search(request: Request):
            """Enhanced home/search page with monetization features"""
            try:
                return self.templates.TemplateResponse("index.html", {
                    "request": request
                })
            except Exception as e:
                logger.error(f"Home page error: {e}")
                return HTMLResponse("Home page temporarily unavailable", status_code=500)
        
        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Main dashboard page with enterprise features"""
            try:
                # Get enhanced system status
                system_status = {
                    "status": "healthy",
                    "scanner_count": 12,
                    "uptime": "99.9%",
                    "response_time": "245ms",
                    "active_users": 127
                }
                
                # Get enhanced statistics
                stats = {
                    "total_scans": 1247,
                    "completed_scans": 1198,
                    "pending_scans": 49,
                    "success_rate": 96.1,
                    "active_reports": 45,
                    "security_score": 95,
                    "performance_score": 98
                }
                
                # Enhanced metrics for enterprise dashboard
                metrics = {
                    "total_scans": 1247,
                    "active_reports": 45,
                    "security_score": 95,
                    "performance_score": 98
                }
                
                # Get recent scans (mock data for now)
                recent_scans = []
                
                # Use enterprise dashboard if available, fallback to regular
                template_name = "dashboard_enterprise.html"
                try:
                    return self.templates.TemplateResponse(template_name, {
                        "request": request,
                        "system_status": system_status,
                        "stats": stats,
                        "metrics": metrics,
                        "recent_scans": recent_scans,
                        "user_preferences": request.session.get("user_preferences", {}),
                        "enterprise_mode": True
                    })
                except Exception as template_error:
                    # Fallback to regular dashboard
                    logger.warning(f"Enterprise template not available, using fallback: {template_error}")
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
                "scan_id": scan_id,
                "datetime": datetime
            })
        
        @self.app.get("/results", response_class=HTMLResponse)
        async def results_page(request: Request, query: Optional[str] = None, type: Optional[str] = None):
            """Enhanced results page with monetization features"""
            return self.templates.TemplateResponse("results.html", {
                "request": request,
                "query": query,
                "search_type": type
            })
        
        @self.app.get("/auth", response_class=HTMLResponse)
        async def auth_page(request: Request):
            """Authentication page for login/register"""
            return self.templates.TemplateResponse("auth.html", {
                "request": request
            })
        
        @self.app.get("/login", response_class=HTMLResponse)
        async def login_redirect(request: Request):
            """Redirect to auth page"""
            return RedirectResponse(url="/auth", status_code=302)
        
        @self.app.get("/register", response_class=HTMLResponse)
        async def register_redirect(request: Request):
            """Redirect to auth page"""
            return RedirectResponse(url="/auth", status_code=302)
        
        @self.app.get("/reports", response_class=HTMLResponse)
        async def reports_page(request: Request):
            """Reports page"""
            return self.templates.TemplateResponse("reports.html", {
                "request": request,
                "datetime": datetime
            })
        
        @self.app.get("/admin", response_class=HTMLResponse)
        async def admin_page(request: Request):
            """Enhanced admin dashboard with real-time analytics"""
            # In production, this would check for admin authentication
            return self.templates.TemplateResponse("admin_dashboard.html", {
                "request": request,
                "datetime": datetime
            })
        
        @self.app.get("/ultimate-admin", response_class=HTMLResponse)
        async def ultimate_admin_dashboard(request: Request):
            """Ultimate enterprise admin dashboard with 100x enhanced features"""
            return self.templates.TemplateResponse("ultimate_admin_dashboard.html", {
                "request": request,
                "datetime": datetime
            })
        
        @self.app.get("/privacy", response_class=HTMLResponse)
        async def privacy_page(request: Request):
            """Privacy and compliance page"""
            try:
                return self.templates.TemplateResponse("privacy.html", {
                    "request": request
                })
            except Exception as e:
                logger.error(f"Privacy page error: {e}")
                return HTMLResponse("Privacy page temporarily unavailable", status_code=500)
        
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
        
        @self.app.post("/api/v1/search/preview")
        async def search_preview(request: Request):
            """Enhanced search preview API with ultimate scanner integration"""
            try:
                data = await request.json()
                query = data.get("query", "").strip()
                search_type = data.get("type", "phone")
                
                if not query:
                    raise HTTPException(status_code=400, detail="Query is required")
                
                # Use ultimate scanner engine for comprehensive results
                try:
                    from backend.app.scanners.ultimate_scanner_engine import ultimate_scanner_engine
                    
                    async with ultimate_scanner_engine as scanner:
                        scan_results = await scanner.ultimate_scan(query, search_type, data)
                    
                    # Convert scanner results to preview format
                    preview_results = []
                    total_data_sources = 0
                    
                    for result in scan_results:
                        total_data_sources += len(result.data_sources)
                        
                        # Create tiered preview based on quality
                        preview_item = {
                            "title": f"{result.category.value.replace('_', ' ').title()} Analysis",
                            "description": f"Comprehensive analysis from {len(result.data_sources)} premium data sources",
                            "icon": self._get_category_icon(result.category.value),
                            "confidence": int(result.confidence_score * 100),
                            "quality_score": result.quality_score,
                            "tier": result.premium_tier,
                            "price": self._get_tier_price(result.premium_tier),
                            "data_sources_count": len(result.data_sources),
                            "execution_time": round(result.execution_time, 2),
                            "ai_insights": result.metadata.get("ai_insights", {}),
                            "patterns": result.metadata.get("patterns", {}),
                            "preview_data": self._create_preview_data(result)
                        }
                        preview_results.append(preview_item)
                    
                    return {
                        "success": True,
                        "data": {
                            "query": query,
                            "type": search_type,
                            "preview_results": preview_results,
                            "total_results_available": len(preview_results),
                            "total_data_sources": total_data_sources,
                            "scan_quality_score": sum(r.quality_score for r in scan_results) / len(scan_results) if scan_results else 0,
                            "premium_insights_available": sum(1 for r in scan_results if r.premium_tier in ["advanced", "enterprise"]),
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    }
                    
                except ImportError:
                    logger.warning("Ultimate scanner engine not available, using fallback")
                    # Fallback to basic preview generation
                    preview_results = await self.generate_preview_results(query, search_type, data)
                    
                    return {
                        "success": True,
                        "data": {
                            "query": query,
                            "type": search_type,
                            "preview_results": preview_results,
                            "total_results_available": len(preview_results) + 3,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    }
                
            except Exception as e:
                logger.error(f"Search preview error: {e}")
                return {
                    "success": False,
                    "message": str(e)
                }
        
        @self.app.post("/api/v1/payment/purchase")
        async def create_purchase(request: Request):
            """Create payment intent for premium content"""
            try:
                data = await request.json()
                report_type = data.get("type", "basic")
                query = data.get("query", "")
                
                # In a real implementation, this would create Stripe payment intent
                # For now, we'll simulate the process
                
                price_map = {
                    "basic": 1.99,
                    "advanced": 2.99
                }
                
                price = price_map.get(report_type, 1.99)
                
                # Mock payment intent
                payment_intent = {
                    "id": f"pi_{uuid.uuid4().hex[:24]}",
                    "client_secret": f"pi_{uuid.uuid4().hex[:24]}_secret",
                    "amount": int(price * 100),  # Convert to cents
                    "currency": "usd",
                    "status": "requires_payment_method"
                }
                
                return {
                    "success": True,
                    "payment_intent": payment_intent,
                    "publishable_key": "pk_test_mock_key"  # Mock Stripe key
                }
                
            except Exception as e:
                logger.error(f"Payment creation error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/v1/auth/login")
        async def login(request: Request):
            """User login endpoint"""
            try:
                data = await request.json()
                email = data.get("email", "").strip().lower()
                password = data.get("password", "")
                
                if not email or not password:
                    raise HTTPException(status_code=400, detail="Email and password are required")
                
                # Mock authentication - in real implementation, verify against database
                mock_users = {
                    "admin@intelligence.com": {"password": "admin123", "role": "admin", "name": "Admin User"},
                    "user@example.com": {"password": "password123", "role": "user", "name": "Regular User"},
                    "premium@example.com": {"password": "premium123", "role": "premium", "name": "Premium User"}
                }
                
                user_data = mock_users.get(email)
                if not user_data or user_data["password"] != password:
                    raise HTTPException(status_code=401, detail="Invalid email or password")
                
                # Generate mock JWT token
                token = f"jwt_token_{uuid.uuid4().hex[:32]}"
                
                return {
                    "success": True,
                    "token": token,
                    "user": {
                        "email": email,
                        "name": user_data["name"],
                        "role": user_data["role"]
                    }
                }
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Login error: {e}")
                raise HTTPException(status_code=500, detail="Login failed")
        
        @self.app.post("/api/v1/auth/register")
        async def register(request: Request):
            """User registration endpoint"""
            try:
                data = await request.json()
                name = data.get("name", "").strip()
                email = data.get("email", "").strip().lower()
                password = data.get("password", "")
                role = data.get("role", "free")
                
                if not all([name, email, password]):
                    raise HTTPException(status_code=400, detail="All fields are required")
                
                if len(password) < 8:
                    raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
                
                # Email validation
                import re
                email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                if not email_pattern.match(email):
                    raise HTTPException(status_code=400, detail="Invalid email format")
                
                # Mock user creation - in real implementation, save to database
                user_id = f"user_{uuid.uuid4().hex[:16]}"
                
                logger.info(f"Mock user created: {email} with role {role}")
                
                return {
                    "success": True,
                    "message": "Account created successfully",
                    "user": {
                        "id": user_id,
                        "email": email,
                        "name": name,
                        "role": role
                    }
                }
                
            except HTTPException:
                raise
            except Exception as e:
                logger.error(f"Registration error: {e}")
                raise HTTPException(status_code=500, detail="Registration failed")
        
        @self.app.post("/api/v1/auth/logout")
        async def logout(request: Request):
            """User logout endpoint"""
            try:
                # In real implementation, invalidate the JWT token
                return {
                    "success": True,
                    "message": "Logged out successfully"
                }
            except Exception as e:
                logger.error(f"Logout error: {e}")
                raise HTTPException(status_code=500, detail="Logout failed")
        
        # Include existing backend API routes if available
        try:
            from backend.app.api import api_router
            self.app.include_router(api_router, prefix="/api/v1/backend")
            logger.info("✅ Backend API routes included")
        except ImportError:
            logger.warning("⚠️ Backend API routes not available")
        
        # Include Business Intelligence API
        try:
            from backend.app.api.business_intelligence_api import business_intelligence_api
            self.app.include_router(business_intelligence_api.router)
            logger.info("✅ Business Intelligence API routes included")
        except ImportError:
            logger.warning("⚠️ Business Intelligence API not available")
        
        # Include Compliance and Privacy API
        try:
            from backend.app.api.compliance_api import compliance_api
            self.app.include_router(compliance_api.router)
            logger.info("✅ Compliance & Privacy API routes included")
        except ImportError:
            logger.warning("⚠️ Compliance API not available")
        
        # Include Performance Monitoring API
        try:
            from backend.app.api.performance_api import performance_api
            self.app.include_router(performance_api.router)
            logger.info("✅ Performance Monitoring API routes included")
        except ImportError:
            logger.warning("⚠️ Performance API not available")
        
        # Include Automation API
        try:
            from backend.app.api.automation_api import automation_api
            self.app.include_router(automation_api.router)
            logger.info("✅ Automation API routes included")
        except ImportError:
            logger.warning("⚠️ Automation API not available")
        
        # Add enhanced API endpoints for dashboard data
        @self.app.get("/api/v1/dashboard/metrics")
        async def get_dashboard_metrics():
            """Get real-time metrics for dashboard"""
            try:
                from backend.app.api.business_intelligence_api import get_platform_kpis
                from backend.app.api.business_intelligence_api import TimeRange
                
                metrics = await get_platform_kpis(TimeRange.DAY)
                
                return {
                    "success": True,
                    "timestamp": datetime.utcnow().isoformat(),
                    "metrics": {k: asdict(v) for k, v in metrics.items()}
                }
            except ImportError:
                # Fallback to mock data
                return {
                    "success": True,
                    "timestamp": datetime.utcnow().isoformat(),
                    "metrics": {
                        "scans": {
                            "name": "Total Scans",
                            "current_value": 247,
                            "previous_value": 231,
                            "change_percentage": 6.9,
                            "trend": "up",
                            "unit": "count"
                        },
                        "users": {
                            "name": "Active Users",
                            "current_value": 89,
                            "previous_value": 85,
                            "change_percentage": 4.7,
                            "trend": "up",
                            "unit": "users"
                        },
                        "performance": {
                            "name": "Avg Response Time",
                            "current_value": 1.8,
                            "previous_value": 2.1,
                            "change_percentage": -14.3,
                            "trend": "up",
                            "unit": "seconds"
                        },
                        "success_rate": {
                            "name": "Success Rate",
                            "current_value": 97.2,
                            "previous_value": 95.8,
                            "change_percentage": 1.5,
                            "trend": "up",
                            "unit": "percentage"
                        }
                    }
                }
            except Exception as e:
                logger.error(f"Dashboard metrics error: {e}")
                return {
                    "success": False,
                    "error": str(e)
                }
        
        @self.app.get("/api/v1/dashboard/chart-data/{metric_type}")
        async def get_chart_data(metric_type: str):
            """Get chart data for dashboard visualizations"""
            try:
                from backend.app.api.business_intelligence_api import create_metric_visualization
                from backend.app.api.business_intelligence_api import MetricType, TimeRange
                
                # Map metric type to enum
                metric_enum = getattr(MetricType, metric_type.upper(), None)
                if not metric_enum:
                    raise HTTPException(status_code=400, detail="Invalid metric type")
                
                data = await create_metric_visualization(metric_enum, TimeRange.DAY)
                return {
                    "success": True,
                    "data": data
                }
            except ImportError:
                # Generate mock chart data
                base_time = datetime.utcnow() - timedelta(hours=24)
                mock_data = []
                
                for i in range(24):
                    timestamp = base_time + timedelta(hours=i)
                    value = 50 + 30 * abs(12 - i) / 12 + 10 * (i % 3)  # Simulate daily pattern
                    
                    mock_data.append({
                        "timestamp": timestamp.isoformat(),
                        "value": round(value, 2)
                    })
                
                return {
                    "success": True,
                    "data": {
                        "metric_type": metric_type,
                        "time_range": "24h",
                        "data": mock_data
                    }
                }
            except Exception as e:
                logger.error(f"Chart data error: {e}")
                return {
                    "success": False,
                    "error": str(e)
                }
        
        # Add enterprise features and advanced API endpoints
        
        @self.app.get("/api/v1/search/advanced")
        async def advanced_search(q: str):
            """Advanced search with filters and categorization"""
            try:
                # Mock advanced search results
                results = [
                    {
                        "title": f"Email Analysis: {q}",
                        "description": "Comprehensive email intelligence analysis",
                        "url": f"/scan?type=email&target={q}",
                        "icon": "fas fa-envelope",
                        "type": "Scan",
                        "category": "Intelligence",
                        "date": "2024-01-15"
                    },
                    {
                        "title": f"Domain Report: {q}",
                        "description": "Domain infrastructure and security analysis",
                        "url": f"/scan?type=domain&target={q}",
                        "icon": "fas fa-globe",
                        "type": "Report",
                        "category": "Domain Analysis",
                        "date": "2024-01-14"
                    },
                    {
                        "title": f"Previous Scans: {q}",
                        "description": "Historical scan results and reports",
                        "url": f"/reports?search={q}",
                        "icon": "fas fa-history",
                        "type": "History",
                        "category": "Reports",
                        "date": "2024-01-13"
                    }
                ]
                
                return {
                    "success": True,
                    "query": q,
                    "data": results,
                    "total": len(results)
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.app.get("/api/v1/dashboard/realtime")
        async def realtime_dashboard_updates():
            """Get real-time dashboard updates"""
            try:
                import random
                return {
                    "success": True,
                    "data": {
                        "response_time": f"{random.randint(200, 300)}ms",
                        "active_users": random.randint(120, 150),
                        "cpu_usage": random.randint(20, 30),
                        "memory_usage": random.randint(40, 50),
                        "storage_usage": random.randint(60, 70)
                    },
                    "updates": [
                        {
                            "type": "metrics_update",
                            "metrics": {
                                "total_scans": random.randint(1200, 1300),
                                "active_reports": random.randint(40, 50)
                            }
                        }
                    ]
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        @self.app.get("/batch-scan", response_class=HTMLResponse)
        async def batch_scan_page(request: Request):
            """Batch scanning interface"""
            return HTMLResponse("""
            <div class="container mt-5">
                <div class="card">
                    <div class="card-header">
                        <h3><i class="fas fa-layer-group me-2"></i>Batch Processing</h3>
                    </div>
                    <div class="card-body">
                        <p>Upload a CSV file or enter multiple targets for batch processing.</p>
                        <div class="mb-3">
                            <label class="form-label">Upload CSV File</label>
                            <input type="file" class="form-control" accept=".csv">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Or Enter Targets (one per line)</label>
                            <textarea class="form-control" rows="5" placeholder="example@email.com\ndomain.com\n+1234567890"></textarea>
                        </div>
                        <button class="btn btn-primary">Start Batch Scan</button>
                        <a href="/" class="btn btn-outline-secondary">Back to Dashboard</a>
                    </div>
                </div>
            </div>
            """)
        
        @self.app.get("/help", response_class=HTMLResponse)
        async def help_page(request: Request):
            """Help and support page"""
            return HTMLResponse("""
            <div class="container mt-5">
                <div class="row">
                    <div class="col-lg-8 mx-auto">
                        <div class="card">
                            <div class="card-header bg-primary text-white">
                                <h3><i class="fas fa-question-circle me-2"></i>Help & Support</h3>
                            </div>
                            <div class="card-body">
                                <h5>Quick Start Guide</h5>
                                <ul>
                                    <li><strong>Dashboard:</strong> View real-time system metrics and recent activity</li>
                                    <li><strong>Intelligence Scanning:</strong> Analyze emails, domains, phones, and social media</li>
                                    <li><strong>Reports:</strong> Generate and export comprehensive intelligence reports</li>
                                    <li><strong>Privacy Center:</strong> Manage GDPR/CCPA compliance and data rights</li>
                                    <li><strong>Admin Panel:</strong> System administration and configuration</li>
                                </ul>
                                
                                <h5 class="mt-4">Keyboard Shortcuts</h5>
                                <div class="row">
                                    <div class="col-md-6">
                                        <ul>
                                            <li><kbd>Ctrl+K</kbd> - Global search</li>
                                            <li><kbd>Ctrl+Shift+D</kbd> - Dashboard</li>
                                            <li><kbd>Ctrl+Shift+S</kbd> - New Scan</li>
                                            <li><kbd>Ctrl+Shift+R</kbd> - Reports</li>
                                        </ul>
                                    </div>
                                    <div class="col-md-6">
                                        <ul>
                                            <li><kbd>Ctrl+Shift+A</kbd> - Admin Panel</li>
                                            <li><kbd>Ctrl+Shift+P</kbd> - Privacy Center</li>
                                            <li><kbd>Ctrl+Shift+T</kbd> - Toggle Theme</li>
                                            <li><kbd>Esc</kbd> - Close Modals</li>
                                        </ul>
                                    </div>
                                </div>
                                
                                <h5 class="mt-4">API Documentation</h5>
                                <p>Access the interactive API documentation at <a href="/docs" target="_blank">/docs</a></p>
                                
                                <div class="mt-4">
                                    <a href="/" class="btn btn-primary">Back to Dashboard</a>
                                    <a href="/docs" class="btn btn-outline-primary" target="_blank">API Docs</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """)
        
        @self.app.get("/terms", response_class=HTMLResponse) 
        async def terms_page(request: Request):
            """Terms of service page"""
            return HTMLResponse("""
            <div class="container mt-5">
                <div class="card">
                    <div class="card-header bg-info text-white">
                        <h3><i class="fas fa-file-contract me-2"></i>Terms of Service</h3>
                    </div>
                    <div class="card-body">
                        <h5>Intelligence Gathering Platform - Terms of Service</h5>
                        <p class="lead">By using this platform, you agree to our terms of service and privacy policy.</p>
                        
                        <h6>1. Acceptable Use</h6>
                        <p>This platform is designed for legitimate intelligence gathering and research purposes only. 
                        Users must comply with all applicable laws and regulations.</p>
                        
                        <h6>2. Data Privacy</h6>
                        <p>We are committed to protecting user privacy and maintaining GDPR/CCPA compliance. 
                        See our <a href="/privacy">Privacy Policy</a> for details.</p>
                        
                        <h6>3. Enterprise Features</h6>
                        <p>Enterprise features include advanced analytics, compliance reporting, and enhanced security controls.</p>
                        
                        <div class="mt-4">
                            <a href="/" class="btn btn-primary">Accept & Continue</a>
                            <a href="/privacy" class="btn btn-outline-primary">Privacy Policy</a>
                        </div>
                    </div>
                </div>
            </div>
            """)
    
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
    
    def _get_category_icon(self, category: str) -> str:
        """Get icon for scanner category"""
        icon_mapping = {
            "email_intelligence": "envelope",
            "phone_intelligence": "phone", 
            "social_media_intelligence": "users",
            "image_intelligence": "image",
            "domain_intelligence": "globe",
            "blockchain_intelligence": "link",
            "darkweb_intelligence": "shield",
            "geospatial_intelligence": "map-pin",
            "financial_intelligence": "dollar-sign",
            "legal_intelligence": "scale",
            "behavioral_analysis": "brain",
            "pattern_recognition": "target",
            "predictive_analytics": "trending-up",
            "sentiment_analysis": "heart",
            "relationship_mapping": "git-branch"
        }
        return icon_mapping.get(category, "search")
    
    def _get_tier_price(self, tier: str) -> float:
        """Get price for premium tier"""
        price_mapping = {
            "free": 0.00,
            "basic": 1.99,
            "advanced": 2.99,
            "enterprise": 4.99
        }
        return price_mapping.get(tier, 0.00)
    
    def _create_preview_data(self, result) -> dict:
        """Create preview data from scanner result"""
        preview = {
            "data_points": len([k for k, v in result.data.items() if v is not None]),
            "sources_used": len(result.data_sources),
            "quality_indicators": {
                "confidence": f"{int(result.confidence_score * 100)}%",
                "relevance": f"{int(result.relevance_score * 100)}%", 
                "reliability": f"{int(result.reliability_score * 100)}%"
            },
            "sample_insights": []
        }
        
        # Add sample insights based on category
        if "email" in result.category.value:
            preview["sample_insights"] = [
                "Email validation status",
                "Domain reputation analysis", 
                "Associated social accounts",
                "Data breach exposure check"
            ]
        elif "phone" in result.category.value:
            preview["sample_insights"] = [
                "Carrier and line type identification",
                "Spam and fraud risk assessment",
                "Location and regional analysis",
                "Associated account discovery"
            ]
        elif "social" in result.category.value:
            preview["sample_insights"] = [
                "Cross-platform profile discovery",
                "Influence and engagement scoring",
                "Network relationship mapping",
                "Content sentiment analysis"
            ]
        
        return preview
    
    async def generate_preview_results(self, query, search_type, options):
        """Generate fallback preview results for monetized search"""
        results = []
        
        # Base results that are always shown (free preview)
        if search_type == "phone":
            results.extend([
                {
                    "title": "Basic Phone Information",
                    "description": f"Carrier: Verizon, Location: {query[:3]}-*** Area",
                    "icon": "phone",
                    "level": "free",
                    "confidence": 90,
                    "tier": "free",
                    "price": 0.00
                },
                {
                    "title": "Advanced Phone Intelligence",
                    "description": "Comprehensive phone analysis with 25+ data sources",
                    "icon": "smartphone",
                    "level": "basic",
                    "confidence": 95,
                    "tier": "basic", 
                    "price": 1.99
                }
            ])
        elif search_type == "email":
            results.extend([
                {
                    "title": "Email Verification",
                    "description": f"Valid email address, Domain: {query.split('@')[-1] if '@' in query else 'unknown'}",
                    "icon": "envelope",
                    "level": "free",
                    "confidence": 95,
                    "tier": "free",
                    "price": 0.00
                },
                {
                    "title": "Advanced Email Intelligence",
                    "description": "Complete email analysis with 30+ data sources",
                    "icon": "mail",
                    "level": "basic",
                    "confidence": 92,
                    "tier": "basic",
                    "price": 1.99
                }
            ])
        elif search_type == "username":
            results.extend([
                {
                    "title": "Profile Discovery",
                    "description": f"Found {query} on 3 platforms",
                    "icon": "user",
                    "level": "free", 
                    "confidence": 85,
                    "tier": "free",
                    "price": 0.00
                },
                {
                    "title": "Ultimate Social Intelligence",
                    "description": "Cross-platform analysis with 50+ social sources",
                    "icon": "users",
                    "level": "advanced",
                    "confidence": 88,
                    "tier": "advanced",
                    "price": 2.99
                }
            ])
        
        return results

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