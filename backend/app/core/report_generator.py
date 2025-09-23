"""
Enhanced Report Generator with Preview/Full Split and Paywall Logic
Generates polished PDF/web/API exports with subscription-based access control.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import json
import hashlib
from enum import Enum
import base64
from io import BytesIO

# Mock imports for demonstration (would be real in production)
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import black, blue, red, green
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

logger = logging.getLogger(__name__)


class ReportType(str, Enum):
    """Types of reports that can be generated"""
    PREVIEW = "preview"
    FULL = "full"
    SUMMARY = "summary"
    DETAILED = "detailed"


class ExportFormat(str, Enum):
    """Export formats supported"""
    JSON = "json"
    PDF = "pdf"
    HTML = "html" 
    CSV = "csv"
    XML = "xml"


class SubscriptionPlan(str, Enum):
    """Subscription plans for access control"""
    FREE = "free"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class PaywallManager:
    """Manages subscription-based access control"""
    
    def __init__(self):
        # Feature access matrix
        self.access_matrix = {
            SubscriptionPlan.FREE: {
                "max_queries_per_day": 5,
                "max_scanners_per_query": 10,
                "report_types": [ReportType.PREVIEW],
                "export_formats": [ExportFormat.JSON, ExportFormat.HTML],
                "data_retention_days": 7,
                "api_access": False,
                "bulk_operations": False,
                "advanced_filters": False,
                "custom_branding": False
            },
            SubscriptionPlan.PROFESSIONAL: {
                "max_queries_per_day": 100,
                "max_scanners_per_query": 50,
                "report_types": [ReportType.PREVIEW, ReportType.FULL, ReportType.SUMMARY],
                "export_formats": [ExportFormat.JSON, ExportFormat.HTML, ExportFormat.PDF],
                "data_retention_days": 90,
                "api_access": True,
                "bulk_operations": True,
                "advanced_filters": True,
                "custom_branding": False
            },
            SubscriptionPlan.ENTERPRISE: {
                "max_queries_per_day": 1000,
                "max_scanners_per_query": 100,
                "report_types": list(ReportType),
                "export_formats": list(ExportFormat),
                "data_retention_days": 365,
                "api_access": True,
                "bulk_operations": True,
                "advanced_filters": True,
                "custom_branding": True
            }
        }
    
    def check_access(self, user_plan: SubscriptionPlan, feature: str, value: Any = None) -> Dict[str, Any]:
        """Check if user has access to specific feature"""
        if user_plan not in self.access_matrix:
            return {"allowed": False, "reason": "Invalid subscription plan"}
        
        plan_features = self.access_matrix[user_plan]
        
        if feature not in plan_features:
            return {"allowed": False, "reason": f"Feature '{feature}' not defined"}
        
        allowed_value = plan_features[feature]
        
        # Handle different types of checks
        if isinstance(allowed_value, bool):
            return {"allowed": allowed_value, "reason": None if allowed_value else f"Feature not available in {user_plan} plan"}
        
        elif isinstance(allowed_value, int) and value is not None:
            is_allowed = value <= allowed_value
            return {
                "allowed": is_allowed,
                "reason": None if is_allowed else f"Limit exceeded: {value} > {allowed_value} (max for {user_plan} plan)",
                "limit": allowed_value,
                "current": value
            }
        
        elif isinstance(allowed_value, list) and value is not None:
            is_allowed = value in allowed_value
            return {
                "allowed": is_allowed,
                "reason": None if is_allowed else f"'{value}' not available in {user_plan} plan",
                "allowed_values": allowed_value
            }
        
        else:
            return {"allowed": True, "value": allowed_value}
    
    def get_upgrade_recommendation(self, current_plan: SubscriptionPlan, requested_feature: str) -> Dict[str, Any]:
        """Get upgrade recommendation for accessing a feature"""
        recommendations = []
        
        for plan in [SubscriptionPlan.PROFESSIONAL, SubscriptionPlan.ENTERPRISE]:
            if plan == current_plan:
                continue
                
            access_check = self.check_access(plan, requested_feature)
            if access_check["allowed"]:
                plan_features = self.access_matrix[plan]
                recommendations.append({
                    "plan": plan,
                    "benefits": [
                        f"Access to {requested_feature}",
                        f"Up to {plan_features.get('max_queries_per_day', 'unlimited')} queries per day",
                        f"Use up to {plan_features.get('max_scanners_per_query', 'all')} scanners per query",
                        f"Export in {len(plan_features.get('export_formats', []))} formats",
                        f"Data retention for {plan_features.get('data_retention_days', 0)} days"
                    ]
                })
                break
        
        return {
            "current_plan": current_plan,
            "requested_feature": requested_feature,
            "recommendations": recommendations
        }


class ReportDataFilter:
    """Filters report data based on subscription level"""
    
    def __init__(self, paywall_manager: PaywallManager):
        self.paywall_manager = paywall_manager
    
    def filter_for_preview(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Filter data for preview report (free tier)"""
        filtered_data = {
            "query_info": data.get("query_info", {}),
            "summary": self._filter_summary_for_preview(data.get("summary", {})),
            "entities": self._filter_entities_for_preview(data.get("entities", [])),
            "scanner_results": self._filter_scanner_results_for_preview(data.get("scanner_results", [])),
            "report_metadata": {
                "report_type": "preview",
                "limitations": [
                    "Limited to top 5 results per category",
                    "Basic entity information only", 
                    "No detailed scanner outputs",
                    "No confidence score details",
                    "Upgrade for full report access"
                ]
            }
        }
        
        return filtered_data
    
    def filter_for_full(self, data: Dict[str, Any], user_plan: SubscriptionPlan) -> Dict[str, Any]:
        """Filter data for full report based on subscription level"""
        if user_plan == SubscriptionPlan.FREE:
            return self.filter_for_preview(data)
        
        # Professional and Enterprise get full data
        filtered_data = {
            "query_info": data.get("query_info", {}),
            "summary": data.get("summary", {}),
            "entities": data.get("entities", []),
            "relationships": data.get("relationships", {}),
            "scanner_results": data.get("scanner_results", []),
            "confidence_analysis": data.get("confidence_analysis", {}),
            "source_analysis": data.get("source_analysis", {}),
            "recommendations": data.get("recommendations", []),
            "report_metadata": {
                "report_type": "full",
                "plan_level": user_plan,
                "full_access": True
            }
        }
        
        # Enterprise gets additional data
        if user_plan == SubscriptionPlan.ENTERPRISE:
            filtered_data.update({
                "advanced_analytics": data.get("advanced_analytics", {}),
                "risk_assessment": data.get("risk_assessment", {}),
                "historical_data": data.get("historical_data", {}),
                "compliance_info": data.get("compliance_info", {})
            })
        
        return filtered_data
    
    def _filter_summary_for_preview(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        """Filter summary data for preview"""
        return {
            "total_entities": summary.get("total_entities", 0),
            "entity_types": {k: v for k, v in list(summary.get("entity_types", {}).items())[:3]},
            "confidence_distribution": summary.get("confidence_distribution", {}),
            "preview_note": "Upgrade to see complete summary"
        }
    
    def _filter_entities_for_preview(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter entities for preview - limit and redact sensitive info"""
        filtered_entities = []
        
        # Group by type and limit each type
        entity_groups = {}
        for entity in entities:
            entity_type = entity.get("type", "unknown")
            if entity_type not in entity_groups:
                entity_groups[entity_type] = []
            entity_groups[entity_type].append(entity)
        
        # Take top 2 from each type, max 5 total
        count = 0
        for entity_type, type_entities in entity_groups.items():
            if count >= 5:
                break
                
            # Sort by confidence and take top 2
            sorted_entities = sorted(type_entities, key=lambda x: x.get("final_confidence", 0), reverse=True)
            
            for entity in sorted_entities[:2]:
                if count >= 5:
                    break
                    
                # Redact sensitive information
                filtered_entity = {
                    "type": entity.get("type"),
                    "value": self._redact_value(entity.get("value", ""), entity.get("type")),
                    "confidence": entity.get("final_confidence", 0),
                    "source_count": len(entity.get("sources", [])),
                    "preview_note": "Upgrade to see complete details"
                }
                filtered_entities.append(filtered_entity)
                count += 1
        
        return filtered_entities
    
    def _filter_scanner_results_for_preview(self, scanner_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter scanner results for preview"""
        # Show only top 3 results with limited information
        filtered_results = []
        
        for i, result in enumerate(scanner_results[:3]):
            filtered_result = {
                "scanner": result.get("scanner", "unknown"),
                "status": result.get("status", "unknown"),
                "confidence": result.get("confidence", 0),
                "has_data": bool(result.get("data")),
                "preview_note": "Upgrade to see detailed results"
            }
            filtered_results.append(filtered_result)
        
        if len(scanner_results) > 3:
            filtered_results.append({
                "scanner": "additional_scanners",
                "status": "hidden",
                "count": len(scanner_results) - 3,
                "upgrade_note": f"Upgrade to see {len(scanner_results) - 3} more scanner results"
            })
        
        return filtered_results
    
    def _redact_value(self, value: str, entity_type: str) -> str:
        """Redact sensitive parts of entity values for preview"""
        if not value:
            return value
            
        if entity_type == "email":
            # Show first 2 chars and domain
            if "@" in value:
                local, domain = value.split("@", 1)
                if len(local) > 2:
                    return f"{local[:2]}***@{domain}"
            return value
        
        elif entity_type == "phone":
            # Show country code and first 3 digits
            if len(value) > 6:
                return f"{value[:4]}***{value[-2:]}"
            return value
        
        elif entity_type == "name":
            # Show first name and last initial
            parts = value.split()
            if len(parts) > 1:
                return f"{parts[0]} {parts[-1][0]}."
            return value
        
        else:
            # Generic redaction
            if len(value) > 6:
                return f"{value[:3]}***{value[-2:]}"
            return value


class ReportGenerator:
    """Main report generator with subscription-based access control"""
    
    def __init__(self):
        self.paywall_manager = PaywallManager()
        self.data_filter = ReportDataFilter(self.paywall_manager)
        self.templates = self._load_report_templates()
    
    def get_subscription_features(self) -> Dict[str, Any]:
        """Get all subscription features and their access matrix"""
        return {
            "plans": {
                "free": {
                    "max_queries_per_day": 5,
                    "max_scanners_per_query": 3,
                    "report_types": ["preview"],
                    "export_formats": ["json"],
                    "data_retention_days": 7,
                    "api_access": False,
                    "bulk_operations": False,
                    "priority_support": False,
                    "advanced_filters": False
                },
                "professional": {
                    "max_queries_per_day": 100,
                    "max_scanners_per_query": 10,
                    "report_types": ["preview", "full", "summary"],
                    "export_formats": ["json", "html", "csv"],
                    "data_retention_days": 30,
                    "api_access": True,
                    "bulk_operations": True,
                    "priority_support": False,
                    "advanced_filters": True
                },
                "enterprise": {
                    "max_queries_per_day": 1000,
                    "max_scanners_per_query": 25,
                    "report_types": ["preview", "full", "summary", "detailed"],
                    "export_formats": ["json", "html", "csv", "pdf", "xml"],
                    "data_retention_days": 365,
                    "api_access": True,
                    "bulk_operations": True,
                    "priority_support": True,
                    "advanced_filters": True
                }
            },
            "feature_matrix": self.paywall_manager.access_matrix
        }
    
    def filter_data_by_subscription(self, data: Dict[str, Any], subscription_plan: str) -> Dict[str, Any]:
        """Filter data based on subscription plan"""
        return self.data_filter.filter_for_full(data, SubscriptionPlan(subscription_plan))
    
    async def generate_report(
        self,
        data: Dict[str, Any],
        report_type: ReportType,
        export_format: ExportFormat,
        user_plan: SubscriptionPlan,
        user_id: str,
        custom_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate report with subscription-based access control"""
        
        # Check access permissions
        access_check = self.paywall_manager.check_access(user_plan, "report_types", report_type)
        if not access_check["allowed"]:
            return {
                "success": False,
                "error": "Access denied",
                "reason": access_check["reason"],
                "upgrade_info": self.paywall_manager.get_upgrade_recommendation(user_plan, "report_types")
            }
        
        format_check = self.paywall_manager.check_access(user_plan, "export_formats", export_format)
        if not format_check["allowed"]:
            return {
                "success": False,
                "error": "Export format not available",
                "reason": format_check["reason"],
                "upgrade_info": self.paywall_manager.get_upgrade_recommendation(user_plan, "export_formats")
            }
        
        # Filter data based on report type and subscription
        if report_type == ReportType.PREVIEW:
            filtered_data = self.data_filter.filter_for_preview(data)
        else:
            filtered_data = self.data_filter.filter_for_full(data, user_plan)
        
        # Generate report content
        try:
            if export_format == ExportFormat.JSON:
                report_content = await self._generate_json_report(filtered_data, report_type, user_plan)
            elif export_format == ExportFormat.HTML:
                report_content = await self._generate_html_report(filtered_data, report_type, user_plan)
            elif export_format == ExportFormat.PDF:
                report_content = await self._generate_pdf_report(filtered_data, report_type, user_plan)
            elif export_format == ExportFormat.CSV:
                report_content = await self._generate_csv_report(filtered_data, report_type, user_plan)
            else:
                return {
                    "success": False,
                    "error": f"Export format {export_format} not implemented"
                }
            
            # Generate report metadata
            report_metadata = self._generate_report_metadata(
                data, filtered_data, report_type, export_format, user_plan, user_id
            )
            
            return {
                "success": True,
                "report_id": report_metadata["report_id"],
                "report_type": report_type,
                "export_format": export_format,
                "content": report_content,
                "metadata": report_metadata,
                "access_info": {
                    "user_plan": user_plan,
                    "features_used": [report_type, export_format],
                    "limitations": filtered_data.get("report_metadata", {}).get("limitations", [])
                }
            }
            
        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            return {
                "success": False,
                "error": "Report generation failed",
                "details": str(e)
            }
    
    async def _generate_json_report(self, data: Dict[str, Any], report_type: ReportType, user_plan: SubscriptionPlan) -> Dict[str, Any]:
        """Generate JSON format report"""
        return {
            "report_header": {
                "title": f"Intelligence Report - {report_type.title()}",
                "generated_at": datetime.utcnow().isoformat(),
                "report_type": report_type,
                "subscription_plan": user_plan
            },
            "data": data,
            "format": "json"
        }
    
    async def _generate_html_report(self, data: Dict[str, Any], report_type: ReportType, user_plan: SubscriptionPlan) -> str:
        """Generate HTML format report"""
        template = self.templates.get("html", {}).get(report_type, self.templates["html"]["default"])
        
        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Intelligence Report - {report_type.title()}</title>
            <style>
                {self._get_html_styles(user_plan)}
            </style>
        </head>
        <body>
            <div class="report-container">
                <header class="report-header">
                    <h1>Intelligence Gathering Report</h1>
                    <div class="report-meta">
                        <span class="report-type">{report_type.title()} Report</span>
                        <span class="generated-date">{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</span>
                        <span class="subscription-badge {user_plan.lower()}">{user_plan.title()}</span>
                    </div>
                </header>
                
                <main class="report-content">
                    {self._render_html_summary(data.get('summary', {}))}
                    {self._render_html_entities(data.get('entities', []))}
                    {self._render_html_scanner_results(data.get('scanner_results', []))}
                    {self._render_html_limitations(data.get('report_metadata', {}).get('limitations', []))}
                </main>
                
                <footer class="report-footer">
                    <p>Generated by Intelligence Gathering Platform</p>
                    <p class="disclaimer">Report accuracy depends on source data quality and availability.</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    async def _generate_pdf_report(self, data: Dict[str, Any], report_type: ReportType, user_plan: SubscriptionPlan) -> bytes:
        """Generate PDF format report"""
        if not REPORTLAB_AVAILABLE:
            # Fallback to simple text-based PDF representation
            pdf_content = f"""
            Intelligence Gathering Report - {report_type.title()}
            Generated: {datetime.utcnow().isoformat()}
            Subscription: {user_plan.title()}
            
            === SUMMARY ===
            {json.dumps(data.get('summary', {}), indent=2)}
            
            === ENTITIES ===
            {json.dumps(data.get('entities', []), indent=2)}
            
            === LIMITATIONS ===
            {chr(10).join(data.get('report_metadata', {}).get('limitations', []))}
            
            Note: PDF rendering requires reportlab library for full formatting.
            """
            return pdf_content.encode('utf-8')
        
        # Use ReportLab for proper PDF generation
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Title
        story.append(Paragraph(f"Intelligence Gathering Report", title_style))
        story.append(Paragraph(f"{report_type.title()} Report - {user_plan.title()} Plan", styles['Heading2']))
        story.append(Spacer(1, 12))
        
        # Summary section
        if data.get('summary'):
            story.append(Paragraph("Executive Summary", styles['Heading2']))
            summary = data['summary']
            
            summary_data = [
                ['Metric', 'Value'],
                ['Total Entities', str(summary.get('total_entities', 0))],
                ['High Confidence Results', str(summary.get('confidence_distribution', {}).get('high', 0))],
                ['Data Sources Used', str(len(summary.get('source_distribution', {})))]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), blue),
                ('TEXTCOLOR', (0, 0), (-1, 0), black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), (0.8, 0.8, 0.8)),
                ('GRID', (0, 0), (-1, -1), 1, black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 20))
        
        # Entities section
        if data.get('entities'):
            story.append(Paragraph("Discovered Entities", styles['Heading2']))
            
            for entity in data['entities'][:10]:  # Limit to top 10 for PDF
                entity_para = Paragraph(
                    f"<b>{entity.get('type', 'Unknown').title()}:</b> {entity.get('value', 'N/A')} "
                    f"(Confidence: {entity.get('confidence', 0):.2f})",
                    styles['Normal']
                )
                story.append(entity_para)
            
            story.append(Spacer(1, 20))
        
        # Limitations
        limitations = data.get('report_metadata', {}).get('limitations', [])
        if limitations:
            story.append(Paragraph("Report Limitations", styles['Heading2']))
            for limitation in limitations:
                story.append(Paragraph(f"• {limitation}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content
    
    async def _generate_csv_report(self, data: Dict[str, Any], report_type: ReportType, user_plan: SubscriptionPlan) -> str:
        """Generate CSV format report"""
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([f"Intelligence Report - {report_type.title()}"])
        writer.writerow([f"Generated: {datetime.utcnow().isoformat()}"])
        writer.writerow([f"Subscription: {user_plan.title()}"])
        writer.writerow([])  # Empty row
        
        # Entities section
        if data.get('entities'):
            writer.writerow(["ENTITIES"])
            writer.writerow(["Type", "Value", "Confidence", "Source Count"])
            
            for entity in data['entities']:
                writer.writerow([
                    entity.get('type', ''),
                    entity.get('value', ''),
                    entity.get('confidence', ''),
                    len(entity.get('sources', []))
                ])
            
            writer.writerow([])  # Empty row
        
        # Summary section
        if data.get('summary'):
            writer.writerow(["SUMMARY"])
            summary = data['summary']
            
            writer.writerow(["Total Entities", summary.get('total_entities', 0)])
            
            # Entity types breakdown
            entity_types = summary.get('entity_types', {})
            for entity_type, count in entity_types.items():
                writer.writerow([f"{entity_type.title()} Entities", count])
        
        csv_content = output.getvalue()
        output.close()
        
        return csv_content
    
    def _load_report_templates(self) -> Dict[str, Any]:
        """Load report templates"""
        return {
            "html": {
                "preview": "preview_template.html",
                "full": "full_template.html",
                "default": "default_template.html"
            },
            "pdf": {
                "preview": "preview_template.pdf",
                "full": "full_template.pdf"
            }
        }
    
    def _get_html_styles(self, user_plan: SubscriptionPlan) -> str:
        """Get CSS styles for HTML report"""
        base_styles = """
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .report-container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .report-header { border-bottom: 2px solid #333; padding-bottom: 20px; margin-bottom: 30px; }
        .report-header h1 { margin: 0; color: #333; font-size: 2.5em; }
        .report-meta { margin-top: 10px; }
        .report-type { background: #007bff; color: white; padding: 5px 10px; border-radius: 4px; margin-right: 10px; }
        .generated-date { color: #666; margin-right: 10px; }
        .subscription-badge { padding: 5px 10px; border-radius: 4px; font-weight: bold; }
        .free { background: #6c757d; color: white; }
        .professional { background: #28a745; color: white; }
        .enterprise { background: #dc3545; color: white; }
        .section { margin: 30px 0; }
        .section h2 { color: #333; border-bottom: 1px solid #ddd; padding-bottom: 10px; }
        .entity-item { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 4px; border-left: 4px solid #007bff; }
        .confidence-high { border-left-color: #28a745; }
        .confidence-medium { border-left-color: #ffc107; }
        .confidence-low { border-left-color: #dc3545; }
        .limitation { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 10px; margin: 5px 0; border-radius: 4px; }
        .report-footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; }
        .disclaimer { font-size: 0.9em; font-style: italic; }
        """
        
        return base_styles
    
    def _render_html_summary(self, summary: Dict[str, Any]) -> str:
        """Render summary section in HTML"""
        if not summary:
            return ""
        
        html = '<div class="section"><h2>Summary</h2>'
        
        if 'total_entities' in summary:
            html += f'<p><strong>Total Entities Found:</strong> {summary["total_entities"]}</p>'
        
        if 'entity_types' in summary:
            html += '<h3>Entity Types</h3><ul>'
            for entity_type, count in summary['entity_types'].items():
                html += f'<li>{entity_type.title()}: {count}</li>'
            html += '</ul>'
        
        if 'confidence_distribution' in summary:
            conf_dist = summary['confidence_distribution']
            html += f'''
            <h3>Confidence Distribution</h3>
            <p>High Confidence: {conf_dist.get('high', 0)} | 
            Medium Confidence: {conf_dist.get('medium', 0)} | 
            Low Confidence: {conf_dist.get('low', 0)}</p>
            '''
        
        html += '</div>'
        return html
    
    def _render_html_entities(self, entities: List[Dict[str, Any]]) -> str:
        """Render entities section in HTML"""
        if not entities:
            return ""
        
        html = '<div class="section"><h2>Discovered Entities</h2>'
        
        for entity in entities:
            confidence = entity.get('confidence', 0)
            confidence_class = 'confidence-high' if confidence > 0.8 else 'confidence-medium' if confidence > 0.5 else 'confidence-low'
            
            html += f'''
            <div class="entity-item {confidence_class}">
                <strong>{entity.get('type', 'Unknown').title()}:</strong> {entity.get('value', 'N/A')}<br>
                <small>Confidence: {confidence:.2f} | Sources: {entity.get('source_count', 0)}</small>
            </div>
            '''
        
        html += '</div>'
        return html
    
    def _render_html_scanner_results(self, scanner_results: List[Dict[str, Any]]) -> str:
        """Render scanner results section in HTML"""
        if not scanner_results:
            return ""
        
        html = '<div class="section"><h2>Scanner Results</h2>'
        
        for result in scanner_results:
            html += f'''
            <div class="entity-item">
                <strong>{result.get('scanner', 'Unknown Scanner')}</strong><br>
                Status: {result.get('status', 'Unknown')}<br>
                <small>Confidence: {result.get('confidence', 0):.2f}</small>
            </div>
            '''
        
        html += '</div>'
        return html
    
    def _render_html_limitations(self, limitations: List[str]) -> str:
        """Render limitations section in HTML"""
        if not limitations:
            return ""
        
        html = '<div class="section"><h2>Report Limitations</h2>'
        
        for limitation in limitations:
            html += f'<div class="limitation">{limitation}</div>'
        
        html += '</div>'
        return html
    
    def _generate_report_metadata(
        self,
        original_data: Dict[str, Any],
        filtered_data: Dict[str, Any],
        report_type: ReportType,
        export_format: ExportFormat,
        user_plan: SubscriptionPlan,
        user_id: str
    ) -> Dict[str, Any]:
        """Generate comprehensive report metadata"""
        
        report_id = hashlib.sha256(
            f"{user_id}_{datetime.utcnow().isoformat()}_{report_type}_{export_format}".encode()
        ).hexdigest()[:16]
        
        return {
            "report_id": report_id,
            "generated_at": datetime.utcnow().isoformat(),
            "generated_by": user_id,
            "report_type": report_type,
            "export_format": export_format,
            "subscription_plan": user_plan,
            "data_summary": {
                "original_entities": len(original_data.get('entities', [])),
                "filtered_entities": len(filtered_data.get('entities', [])),
                "original_scanner_results": len(original_data.get('scanner_results', [])),
                "filtered_scanner_results": len(filtered_data.get('scanner_results', []))
            },
            "access_controls": {
                "preview_mode": report_type == ReportType.PREVIEW,
                "data_redacted": user_plan == SubscriptionPlan.FREE,
                "limitations_applied": bool(filtered_data.get('report_metadata', {}).get('limitations'))
            },
            "quality_metrics": {
                "completeness_score": self._calculate_completeness_score(filtered_data),
                "confidence_score": self._calculate_average_confidence(filtered_data),
                "source_diversity": len(set(
                    source.get('source', '') 
                    for entity in filtered_data.get('entities', [])
                    for source in entity.get('sources', [])
                ))
            }
        }
    
    def _calculate_completeness_score(self, data: Dict[str, Any]) -> float:
        """Calculate data completeness score"""
        score = 0.0
        
        if data.get('entities'):
            score += 0.4
        if data.get('scanner_results'):
            score += 0.3
        if data.get('relationships'):
            score += 0.2
        if data.get('summary'):
            score += 0.1
        
        return score
    
    def _calculate_average_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate average confidence across all entities"""
        entities = data.get('entities', [])
        if not entities:
            return 0.0
        
        confidences = [e.get('final_confidence', 0) for e in entities]
        return sum(confidences) / len(confidences) if confidences else 0.0


# Factory function for easy instantiation
def create_report_generator() -> ReportGenerator:
    """Create and return a configured ReportGenerator instance"""
    return ReportGenerator()