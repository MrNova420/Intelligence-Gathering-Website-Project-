#!/usr/bin/env python3
"""
Comprehensive API Documentation System
Generates OpenAPI/Swagger documentation with enhanced features
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from typing import Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

def create_enhanced_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """Create enhanced OpenAPI schema with comprehensive documentation"""
    
    if app.openapi_schema:
        return app.openapi_schema
    
    # Base OpenAPI schema
    openapi_schema = get_openapi(
        title="Intelligence Gathering Platform API",
        version="2.0.0",
        description="""
# Intelligence Gathering Platform API

## Overview
The Intelligence Gathering Platform provides comprehensive intelligence collection and analysis capabilities through a RESTful API. This platform enables users to gather intelligence from various sources including email addresses, phone numbers, and social media profiles.

## Features
- **Multi-source Intelligence**: Gather data from email, phone, and social media sources
- **Advanced Analytics**: Comprehensive analysis and reporting capabilities  
- **Security-First**: Enterprise-grade security with authentication and authorization
- **Real-time Processing**: Live intelligence gathering and processing
- **Comprehensive Reporting**: Generate detailed reports in multiple formats
- **Performance Monitoring**: Built-in performance metrics and monitoring
- **Error Tracking**: Advanced error tracking and logging capabilities

## Authentication
This API uses JWT-based authentication. Include the Bearer token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Rate Limiting
API requests are rate-limited to ensure fair usage:
- **Free Tier**: 100 requests per hour
- **Premium Tier**: 1,000 requests per hour  
- **Enterprise Tier**: 10,000 requests per hour

## Response Format
All API responses follow a consistent format:
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful",
  "timestamp": "2025-09-25T01:30:00Z",
  "request_id": "req_123456789"
}
```

## Error Handling
Errors are returned with appropriate HTTP status codes and detailed error information:
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {...}
  },
  "timestamp": "2025-09-25T01:30:00Z",
  "request_id": "req_123456789"
}
```
        """,
        routes=app.routes,
        tags=[
            {
                "name": "Health & Status",
                "description": "System health and status endpoints"
            },
            {
                "name": "Authentication",
                "description": "User authentication and authorization"
            },
            {
                "name": "Intelligence Scanning",
                "description": "Core intelligence gathering operations"
            },
            {
                "name": "Reports & Analytics",
                "description": "Report generation and analytics"
            },
            {
                "name": "User Management",
                "description": "User account and profile management"
            },
            {
                "name": "Monitoring & Metrics",
                "description": "Performance monitoring and system metrics"
            },
            {
                "name": "Administration",
                "description": "Administrative functions and system management"
            }
        ]
    )
    
    # Enhanced schema customizations
    openapi_schema["info"]["contact"] = {
        "name": "Intelligence Platform Support",
        "email": "support@intelligence-platform.com",
        "url": "https://intelligence-platform.com/support"
    }
    
    openapi_schema["info"]["license"] = {
        "name": "Commercial License",
        "url": "https://intelligence-platform.com/license"
    }
    
    # Security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token obtained from /auth/login endpoint"
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key for service-to-service authentication"
        }
    }
    
    # Global security requirement
    openapi_schema["security"] = [
        {"BearerAuth": []},
        {"ApiKeyAuth": []}
    ]
    
    # Servers configuration
    openapi_schema["servers"] = [
        {
            "url": "https://api.intelligence-platform.com",
            "description": "Production server"
        },
        {
            "url": "https://staging-api.intelligence-platform.com", 
            "description": "Staging server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        }
    ]
    
    # Ensure components section exists
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}
    
    # Enhanced schemas for common data models
    openapi_schema["components"]["schemas"].update({
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": False},
                "error": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "example": "VALIDATION_ERROR"},
                        "message": {"type": "string", "example": "Invalid input data"},
                        "details": {"type": "object"}
                    }
                },
                "timestamp": {"type": "string", "format": "date-time"},
                "request_id": {"type": "string", "example": "req_123456789"}
            }
        },
        "SuccessResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "example": True},
                "data": {"type": "object"},
                "message": {"type": "string", "example": "Operation successful"},
                "timestamp": {"type": "string", "format": "date-time"},
                "request_id": {"type": "string", "example": "req_123456789"}
            }
        },
        "HealthStatus": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["healthy", "degraded", "unhealthy"]},
                "timestamp": {"type": "string", "format": "date-time"},
                "version": {"type": "string", "example": "2.0.0"},
                "uptime": {"type": "integer", "description": "Uptime in seconds"},
                "checks": {
                    "type": "object",
                    "properties": {
                        "database": {"type": "boolean"},
                        "cache": {"type": "boolean"},
                        "external_apis": {"type": "boolean"}
                    }
                }
            }
        },
        "ScanRequest": {
            "type": "object",
            "properties": {
                "target": {"type": "string", "description": "Target to scan (email, phone, username)"},
                "scan_type": {"type": "string", "enum": ["email", "phone", "social"], "description": "Type of scan to perform"},
                "options": {
                    "type": "object",
                    "properties": {
                        "deep_scan": {"type": "boolean", "default": False},
                        "include_social": {"type": "boolean", "default": True},
                        "timeout": {"type": "integer", "default": 30, "description": "Timeout in seconds"}
                    }
                }
            },
            "required": ["target", "scan_type"]
        },
        "ScanResult": {
            "type": "object",
            "properties": {
                "scan_id": {"type": "string", "example": "scan_123456789"},
                "target": {"type": "string"},
                "scan_type": {"type": "string"},
                "status": {"type": "string", "enum": ["queued", "running", "completed", "failed"]},
                "started_at": {"type": "string", "format": "date-time"},
                "completed_at": {"type": "string", "format": "date-time"},
                "results": {
                    "type": "object",
                    "properties": {
                        "basic_info": {"type": "object"},
                        "social_presence": {"type": "object"},
                        "security_assessment": {"type": "object"},
                        "confidence_score": {"type": "number", "minimum": 0, "maximum": 1}
                    }
                }
            }
        },
        "UserProfile": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "username": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "full_name": {"type": "string"},
                "role": {"type": "string", "enum": ["user", "premium", "admin"]},
                "created_at": {"type": "string", "format": "date-time"},
                "last_login": {"type": "string", "format": "date-time"},
                "preferences": {"type": "object"},
                "subscription": {
                    "type": "object",
                    "properties": {
                        "plan": {"type": "string"},
                        "expires_at": {"type": "string", "format": "date-time"},
                        "usage": {"type": "object"}
                    }
                }
            }
        },
        "SystemMetrics": {
            "type": "object",
            "properties": {
                "cpu_usage": {"type": "number", "minimum": 0, "maximum": 100},
                "memory_usage": {"type": "number", "minimum": 0, "maximum": 100},
                "disk_usage": {"type": "number", "minimum": 0, "maximum": 100},
                "active_connections": {"type": "integer"},
                "requests_per_minute": {"type": "number"},
                "average_response_time": {"type": "number"},
                "error_rate": {"type": "number", "minimum": 0, "maximum": 100},
                "timestamp": {"type": "string", "format": "date-time"}
            }
        }
    })
    
    # Add examples for common responses
    openapi_schema["components"]["examples"] = {
        "HealthyResponse": {
            "summary": "Healthy system status",
            "value": {
                "status": "healthy",
                "timestamp": "2025-09-25T01:30:00Z",
                "version": "2.0.0",
                "uptime": 86400,
                "checks": {
                    "database": True,
                    "cache": True, 
                    "external_apis": True
                }
            }
        },
        "EmailScanRequest": {
            "summary": "Email scan request",
            "value": {
                "target": "example@domain.com",
                "scan_type": "email",
                "options": {
                    "deep_scan": True,
                    "include_social": True,
                    "timeout": 60
                }
            }
        },
        "ScanResultExample": {
            "summary": "Completed scan result",
            "value": {
                "scan_id": "scan_abc123",
                "target": "example@domain.com", 
                "scan_type": "email",
                "status": "completed",
                "started_at": "2025-09-25T01:25:00Z",
                "completed_at": "2025-09-25T01:30:00Z",
                "results": {
                    "basic_info": {
                        "email_valid": True,
                        "domain": "domain.com",
                        "mx_records": ["mail.domain.com"]
                    },
                    "social_presence": {
                        "platforms": ["linkedin", "twitter"],
                        "profiles_found": 2
                    },
                    "security_assessment": {
                        "breach_count": 0,
                        "risk_level": "low"
                    },
                    "confidence_score": 0.85
                }
            }
        }
    }
    
    # Enhanced path operations with better documentation
    for path_name, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            if isinstance(operation, dict):
                # Add request ID to all responses
                if "responses" in operation:
                    for response_code, response in operation["responses"].items():
                        if "content" in response:
                            for content_type, content in response["content"].items():
                                if "schema" in content:
                                    # Add common response fields
                                    schema = content["schema"]
                                    if "properties" in schema:
                                        schema["properties"]["request_id"] = {
                                            "type": "string",
                                            "description": "Unique request identifier",
                                            "example": "req_123456789"
                                        }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def generate_api_documentation_file(app: FastAPI, output_path: str = "api_documentation.json"):
    """Generate API documentation file"""
    try:
        schema = create_enhanced_openapi_schema(app)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📄 API documentation generated: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate API documentation: {e}")
        return False

def create_redoc_html(openapi_url: str = "/openapi.json") -> str:
    """Create custom ReDoc HTML page"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Intelligence Gathering Platform API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Roboto', sans-serif;
        }}
        .custom-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }}
        .custom-header h1 {{
            margin: 0;
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
        }}
        .custom-header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="custom-header">
        <h1>🔍 Intelligence Gathering Platform</h1>
        <p>Comprehensive API Documentation</p>
    </div>
    <redoc spec-url='{openapi_url}' theme='theme' hide-download-button></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@2.1.5/bundles/redoc.standalone.js"></script>
</body>
</html>
"""

def create_swagger_html(openapi_url: str = "/openapi.json") -> str:
    """Create custom Swagger UI HTML page"""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Intelligence Gathering Platform API</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
    <style>
        html {{
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }}
        *, *:before, *:after {{
            box-sizing: inherit;
        }}
        body {{
            margin:0;
            background: #fafafa;
            font-family: 'Roboto', sans-serif;
        }}
        .custom-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .swagger-ui .topbar {{
            display: none;
        }}
    </style>
</head>
<body>
    <div class="custom-header">
        <h1>🔍 Intelligence Gathering Platform API</h1>
        <p>Interactive API Documentation & Testing</p>
    </div>
    <div id="swagger-ui"></div>
    
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
    window.onload = function() {{
        const ui = SwaggerUIBundle({{
            url: '{openapi_url}',
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            plugins: [
                SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout",
            theme: "dark",
            tryItOutEnabled: true,
            filter: true,
            displayOperationId: true,
            displayRequestDuration: true
        }})
    }}
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    # Test documentation generation
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    @app.post("/api/v1/scan")
    async def create_scan():
        return {"scan_id": "test"}
    
    schema = create_enhanced_openapi_schema(app)
    print("✅ OpenAPI schema generated successfully!")
    print(f"Schema has {len(schema['paths'])} paths defined")