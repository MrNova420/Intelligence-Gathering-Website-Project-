
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
