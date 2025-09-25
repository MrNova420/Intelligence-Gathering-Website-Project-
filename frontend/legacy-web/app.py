#!/usr/bin/env python3
"""
Simple Flask application to showcase the modernized Intelligence Platform interface
"""

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.secret_key = 'dev-key-for-demo'

# Demo data for the dashboard
demo_data = {
    'system_status': {'status': 'healthy'},
    'active_scanners': 12,
    'total_scans': 1247,
    'success_rate': 96.1
}

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html', **demo_data)

@app.route('/scan')
def scan():
    """Scan page"""
    scan_type = request.args.get('type', 'email')
    return render_template('scan.html', scan_type=scan_type)

@app.route('/reports')
def reports():
    """Reports page"""
    return render_template('dashboard.html', **demo_data)  # Use dashboard for demo

@app.route('/privacy')
def privacy():
    """Privacy page"""
    return render_template('dashboard.html', **demo_data)  # Use dashboard for demo

@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('dashboard.html', **demo_data)  # Use dashboard for demo

@app.route('/help')
def help_page():
    """Help page"""
    return render_template('dashboard.html', **demo_data)  # Use dashboard for demo

@app.route('/docs')
def docs():
    """API Documentation page"""
    return render_template('dashboard.html', **demo_data)  # Use dashboard for demo

@app.route('/api/v1/scan', methods=['POST'])
def api_scan():
    """Demo API endpoint"""
    return jsonify({
        'success': True,
        'scan_id': 'demo-scan-123',
        'status': 'started',
        'estimated_time': '2-3 minutes'
    })

@app.route('/api/v1/performance/metrics')
def api_metrics():
    """Demo metrics endpoint"""
    return jsonify({
        'uptime': '99.9%',
        'response_time': '0.3s',
        'active_scans': 5,
        'queue_size': 12
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting Intelligence Platform on http://localhost:{port}")
    print(f"📊 Dashboard: http://localhost:{port}/")
    print(f"🔍 Scan Interface: http://localhost:{port}/scan")
    print(f"✨ Modern UI Framework: Active")
    
    app.run(host='0.0.0.0', port=port, debug=debug)