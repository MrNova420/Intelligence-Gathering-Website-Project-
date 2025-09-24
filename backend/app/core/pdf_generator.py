"""
Professional PDF Report Generator
As promised in PR #1 and PR #2 for comprehensive intelligence reporting
"""

import io
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import base64
import json

# Conditional imports with fallbacks
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, black, grey, blue, red, green
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.platypus.flowables import HRFlowable
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    # Mock classes for when reportlab is not available
    class MockSimpleDocTemplate:
        def __init__(self, *args, **kwargs):
            pass
        def build(self, story):
            return b"PDF generation requires reportlab library"

logger = logging.getLogger(__name__)


class IntelligencePDFGenerator:
    """Professional PDF report generator for intelligence data"""
    
    def __init__(self):
        self.styles = self._setup_styles() if REPORTLAB_AVAILABLE else {}
        
    def _setup_styles(self):
        """Setup custom styles for professional PDF reports"""
        styles = getSampleStyleSheet()
        
        # Custom styles for intelligence reports
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1a365d'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=12,
            textColor=HexColor('#2c5aa0'),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=styles['Heading3'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=HexColor('#4a5568'),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='BodyText',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=HexColor('#2d3748'),
            fontName='Helvetica'
        ))
        
        styles.add(ParagraphStyle(
            name='ConfidenceHigh',
            parent=styles['Normal'],
            fontSize=11,
            textColor=HexColor('#38a169'),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='ConfidenceMedium',
            parent=styles['Normal'],
            fontSize=11,
            textColor=HexColor('#d69e2e'),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='ConfidenceLow',
            parent=styles['Normal'],
            fontSize=11,
            textColor=HexColor('#e53e3e'),
            fontName='Helvetica-Bold'
        ))
        
        styles.add(ParagraphStyle(
            name='Metadata',
            parent=styles['Normal'],
            fontSize=9,
            textColor=HexColor('#718096'),
            fontName='Helvetica'
        ))
        
        return styles
    
    def generate_intelligence_report(self, scan_data: Dict[str, Any], 
                                   report_type: str = "full") -> bytes:
        """Generate a professional intelligence report in PDF format"""
        if not REPORTLAB_AVAILABLE:
            logger.error("ReportLab not available for PDF generation")
            return b"PDF generation requires reportlab library"
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build the story (content)
        story = []
        
        # Title and header
        story.extend(self._create_report_header(scan_data))
        
        # Executive summary
        story.extend(self._create_executive_summary(scan_data))
        
        # Scanner results
        if report_type == "full":
            story.extend(self._create_detailed_results(scan_data))
        else:
            story.extend(self._create_preview_results(scan_data))
        
        # Confidence analysis
        story.extend(self._create_confidence_analysis(scan_data))
        
        # Source attribution
        story.extend(self._create_source_attribution(scan_data))
        
        # Footer and metadata
        story.extend(self._create_report_footer(scan_data))
        
        # Build PDF
        doc.build(story)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    def _create_report_header(self, scan_data: Dict[str, Any]) -> List[Any]:
        """Create professional report header"""
        story = []
        
        # Title
        title = Paragraph("Intelligence Gathering Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Report metadata table
        query_info = scan_data.get('query', {})
        metadata = [
            ['Report ID:', scan_data.get('scan_id', 'N/A')],
            ['Query Type:', query_info.get('type', 'N/A')],
            ['Query Value:', query_info.get('value', 'N/A')],
            ['Generated:', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')],
            ['Platform:', 'Intelligence Gathering Platform v1.0']
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 3*inch])
        metadata_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#4a5568')),
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#e2e8f0')))
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_executive_summary(self, scan_data: Dict[str, Any]) -> List[Any]:
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Summary statistics
        results = scan_data.get('results', {})
        total_scanners = len(results)
        successful_scans = len([r for r in results.values() if not r.get('error')])
        overall_confidence = scan_data.get('confidence_score', 0.0)
        
        summary_text = f"""
        This intelligence report contains analysis from {total_scanners} scanner tools, 
        with {successful_scans} successful scans ({(successful_scans/total_scanners*100):.1f}% success rate). 
        The overall confidence score is {overall_confidence:.1f}%.
        
        Key findings include data aggregation from multiple intelligence sources, 
        cross-reference validation, and confidence scoring based on source reliability.
        """
        
        story.append(Paragraph(summary_text, self.styles['BodyText']))
        story.append(Spacer(1, 15))
        
        # Summary statistics table
        stats_data = [
            ['Metric', 'Value', 'Status'],
            ['Total Scanners Used', str(total_scanners), self._get_status_indicator(total_scanners > 5)],
            ['Successful Scans', str(successful_scans), self._get_status_indicator(successful_scans > 0)],
            ['Overall Confidence', f"{overall_confidence:.1f}%", self._get_confidence_indicator(overall_confidence)],
            ['Data Sources', str(len(scan_data.get('sources', []))), self._get_status_indicator(len(scan_data.get('sources', [])) > 0)],
        ]
        
        stats_table = Table(stats_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f7fafc')),
            ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#2d3748')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0'))
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_detailed_results(self, scan_data: Dict[str, Any]) -> List[Any]:
        """Create detailed scanner results section (full report only)"""
        story = []
        
        story.append(Paragraph("Detailed Scanner Results", self.styles['SectionHeader']))
        
        results = scan_data.get('results', {})
        
        for scanner_name, result in results.items():
            # Scanner subsection header
            story.append(Paragraph(f"{scanner_name.replace('_', ' ').title()}", 
                                 self.styles['SubsectionHeader']))
            
            if result.get('error'):
                # Error case
                error_text = f"<font color='red'>Error: {result['error']}</font>"
                story.append(Paragraph(error_text, self.styles['BodyText']))
            else:
                # Success case - display key findings
                self._add_scanner_findings(story, scanner_name, result)
            
            story.append(Spacer(1, 12))
        
        return story
    
    def _create_preview_results(self, scan_data: Dict[str, Any]) -> List[Any]:
        """Create preview results section (limited data)"""
        story = []
        
        story.append(Paragraph("Preview Results", self.styles['SectionHeader']))
        
        preview_text = """
        <font color='orange'><b>Preview Mode:</b></font> This is a limited preview of the intelligence report. 
        The full report includes detailed scanner results, advanced analytics, 
        data correlation analysis, and comprehensive source attribution.
        
        <b>To access the full report:</b>
        • Upgrade to Professional ($29/month) for complete intelligence data
        • Get detailed scanner outputs with confidence scoring
        • Access advanced analytics and data visualization
        • Export in multiple formats (PDF, CSV, JSON)
        """
        
        story.append(Paragraph(preview_text, self.styles['BodyText']))
        story.append(Spacer(1, 15))
        
        # Show limited summary only
        results = scan_data.get('results', {})
        successful_scans = [name for name, result in results.items() if not result.get('error')]
        
        if successful_scans:
            preview_data = f"<b>Available Data Sources:</b> {', '.join(successful_scans[:3])}"
            if len(successful_scans) > 3:
                preview_data += f" and {len(successful_scans) - 3} more sources..."
            
            story.append(Paragraph(preview_data, self.styles['BodyText']))
        
        story.append(Spacer(1, 20))
        
        return story
    
    def _add_scanner_findings(self, story: List[Any], scanner_name: str, result: Dict[str, Any]):
        """Add scanner-specific findings to the story"""
        # Extract key information based on scanner type
        if 'email' in scanner_name:
            self._add_email_findings(story, result)
        elif 'phone' in scanner_name:
            self._add_phone_findings(story, result)
        elif 'social' in scanner_name:
            self._add_social_findings(story, result)
        else:
            self._add_generic_findings(story, result)
    
    def _add_email_findings(self, story: List[Any], result: Dict[str, Any]):
        """Add email-specific findings"""
        findings = []
        
        if result.get('valid'):
            findings.append("✓ Email address syntax validated")
        
        if result.get('domain_check', {}).get('domain_exists'):
            findings.append("✓ Domain exists and is reachable")
        
        if result.get('mx_check', {}).get('has_mx'):
            findings.append("✓ Mail exchange records found")
        
        reputation = result.get('reputation_score', 0)
        if reputation > 0.8:
            findings.append(f"✓ High reputation score ({reputation:.1%})")
        elif reputation > 0.5:
            findings.append(f"⚠ Medium reputation score ({reputation:.1%})")
        else:
            findings.append(f"⚠ Low reputation score ({reputation:.1%})")
        
        for finding in findings:
            story.append(Paragraph(finding, self.styles['BodyText']))
    
    def _add_phone_findings(self, story: List[Any], result: Dict[str, Any]):
        """Add phone-specific findings"""
        findings = []
        
        if result.get('valid'):
            findings.append("✓ Phone number format validated")
        
        location = result.get('location', {})
        if location.get('country'):
            findings.append(f"📍 Country: {location['country']}")
        
        if location.get('region'):
            findings.append(f"📍 Region: {location['region']}")
        
        carrier = result.get('carrier', {})
        if carrier.get('name'):
            findings.append(f"📱 Carrier: {carrier['name']}")
        
        for finding in findings:
            story.append(Paragraph(finding, self.styles['BodyText']))
    
    def _add_social_findings(self, story: List[Any], result: Dict[str, Any]):
        """Add social media findings"""
        findings = []
        
        if result.get('profile_found'):
            findings.append("✓ Social media profile located")
        
        if result.get('profile_data', {}).get('followers_count'):
            count = result['profile_data']['followers_count']
            findings.append(f"👥 Followers: {count:,}")
        
        if result.get('profile_data', {}).get('verified'):
            findings.append("✓ Verified account")
        
        for finding in findings:
            story.append(Paragraph(finding, self.styles['BodyText']))
    
    def _add_generic_findings(self, story: List[Any], result: Dict[str, Any]):
        """Add generic findings for other scanner types"""
        confidence = result.get('confidence', 0)
        timestamp = result.get('timestamp', 'Unknown')
        
        findings = [
            f"Confidence Level: {confidence:.1%}",
            f"Data Collected: {timestamp}"
        ]
        
        # Add any key-value pairs from result
        for key, value in result.items():
            if key not in ['confidence', 'timestamp', 'error'] and isinstance(value, (str, int, float)):
                findings.append(f"{key.replace('_', ' ').title()}: {value}")
        
        for finding in findings[:5]:  # Limit to 5 findings
            story.append(Paragraph(finding, self.styles['BodyText']))
    
    def _create_confidence_analysis(self, scan_data: Dict[str, Any]) -> List[Any]:
        """Create confidence analysis section"""
        story = []
        
        story.append(Paragraph("Confidence Analysis", self.styles['SectionHeader']))
        
        overall_confidence = scan_data.get('confidence_score', 0.0)
        confidence_level = self._get_confidence_level(overall_confidence)
        
        confidence_text = f"""
        The overall confidence level for this intelligence report is <b>{confidence_level}</b> 
        ({overall_confidence:.1f}%). This score is calculated based on:
        
        • Source reliability and historical accuracy
        • Cross-validation between multiple sources
        • Data freshness and recency
        • Technical validation (syntax, format, etc.)
        • Response consistency across scanners
        """
        
        story.append(Paragraph(confidence_text, self.styles['BodyText']))
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_source_attribution(self, scan_data: Dict[str, Any]) -> List[Any]:
        """Create source attribution section"""
        story = []
        
        story.append(Paragraph("Source Attribution", self.styles['SectionHeader']))
        
        results = scan_data.get('results', {})
        sources = []
        
        for scanner_name, result in results.items():
            if not result.get('error'):
                confidence = result.get('confidence', 0.0)
                timestamp = result.get('timestamp', 'Unknown')
                sources.append([
                    scanner_name.replace('_', ' ').title(),
                    f"{confidence:.1%}",
                    timestamp.split('T')[0] if 'T' in str(timestamp) else str(timestamp)
                ])
        
        if sources:
            source_data = [['Source', 'Confidence', 'Last Updated']] + sources
            
            source_table = Table(source_data, colWidths=[2.5*inch, 1*inch, 1.5*inch])
            source_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f7fafc')),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#2d3748')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#e2e8f0'))
            ]))
            
            story.append(source_table)
        
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_report_footer(self, scan_data: Dict[str, Any]) -> List[Any]:
        """Create report footer with disclaimers"""
        story = []
        
        story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#e2e8f0')))
        story.append(Spacer(1, 12))
        
        footer_text = """
        <b>Disclaimer:</b> This intelligence report is generated using publicly available information 
        and automated analysis tools. The data should be verified independently before making any 
        decisions based on this information. Intelligence Platform is not responsible for the 
        accuracy or completeness of third-party data sources.
        
        <b>Privacy Notice:</b> All data collection complies with applicable privacy laws and 
        uses only publicly accessible sources. No unauthorized access or data breaches are involved 
        in the intelligence gathering process.
        """
        
        story.append(Paragraph(footer_text, self.styles['Metadata']))
        
        return story
    
    def _get_status_indicator(self, is_good: bool) -> str:
        """Get status indicator for table cells"""
        return "✓" if is_good else "⚠"
    
    def _get_confidence_indicator(self, confidence: float) -> str:
        """Get confidence indicator based on score"""
        if confidence >= 80:
            return "High"
        elif confidence >= 60:
            return "Medium"
        else:
            return "Low"
    
    def _get_confidence_level(self, confidence: float) -> str:
        """Get human-readable confidence level"""
        if confidence >= 90:
            return "Very High"
        elif confidence >= 80:
            return "High"
        elif confidence >= 70:
            return "Good"
        elif confidence >= 60:
            return "Medium"
        elif confidence >= 40:
            return "Low"
        else:
            return "Very Low"


# Global PDF generator instance
pdf_generator = IntelligencePDFGenerator()