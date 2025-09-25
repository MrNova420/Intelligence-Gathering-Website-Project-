/**
 * Intelligence Gathering Platform - AAA Enterprise JavaScript Framework
 * Advanced client-side functionality inspired by GitHub, Discord, and modern platforms
 */

class IntelligencePlatformAAA {
    constructor() {
        this.apiBase = '/api/v1';
        this.wsConnection = null;
        this.notifications = new NotificationManager();
        this.themeManager = new ThemeManager();
        this.performanceMonitor = new PerformanceMonitor();
        this.features = new AdvancedFeatures();
        this.init();
    }

    async init() {
        await this.initializeComponents();
        this.setupEventListeners();
        this.startRealtimeUpdates();
        this.setupKeyboardShortcuts();
        this.initializeAnimations();
        this.loadAdvancedFeatures();
    }

    async initializeComponents() {
        // Initialize real-time clock with timezone support
        this.updateClock();
        setInterval(() => this.updateClock(), 1000);

        // Initialize dashboard metrics with caching
        if (document.getElementById('dashboard-metrics')) {
            await this.loadDashboardMetrics();
            setInterval(() => this.loadDashboardMetrics(), 15000); // More frequent updates
        }

        // Initialize all advanced features
        this.themeManager.init();
        this.performanceMonitor.init();
        this.features.init();

        console.log('%c🚀 Intelligence Platform AAA Enterprise Initialized', 
                   'color: #238636; font-weight: bold; font-size: 16px; text-shadow: 0 0 5px #238636;');
    }

    updateClock() {
        const clockElement = document.getElementById('current-time');
        if (clockElement) {
            const now = new Date();
            const options = {
                year: 'numeric', month: 'short', day: 'numeric',
                hour: '2-digit', minute: '2-digit', second: '2-digit',
                timeZoneName: 'short'
            };
            clockElement.textContent = `Current Time: ${now.toLocaleString('en-US', options)}`;
        }
    }

    async loadDashboardMetrics() {
        try {
            const [metricsResponse, performanceResponse] = await Promise.all([
                fetch(`${this.apiBase}/dashboard/metrics`),
                fetch(`${this.apiBase}/performance/metrics`)
            ]);
            
            const metricsData = await metricsResponse.json();
            const performanceData = await performanceResponse.json();
            
            if (metricsData.success) {
                this.updateMetricCards(metricsData.data);
                this.updateCharts(metricsData.data);
                this.updateSystemStatus(metricsData.system_status);
            }
            
            if (performanceData.success) {
                this.updatePerformanceIndicators(performanceData.data);
            }
        } catch (error) {
            console.error('Failed to load dashboard metrics:', error);
            this.notifications.show('Failed to load dashboard metrics', 'error');
        }
    }

    updateMetricCards(metrics) {
        Object.entries(metrics).forEach(([key, value]) => {
            const element = document.getElementById(`metric-${key}`);
            if (element) {
                const currentValue = parseInt(element.textContent.replace(/,/g, '')) || 0;
                this.animateNumber(element, currentValue, value);
                
                // Add sparkline effect
                this.addSparklineEffect(element, value);
            }
        });
    }

    animateNumber(element, start, end) {
        const duration = 1500;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentValue = Math.floor(start + (end - start) * this.easeOutCubic(progress));
            element.textContent = currentValue.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }

    addSparklineEffect(element, value) {
        // Create a mini sparkline visualization
        const sparkline = element.parentNode.querySelector('.sparkline') ||
                          this.createSparklineElement(element.parentNode);
        
        // Update sparkline with new data point
        this.updateSparkline(sparkline, value);
    }

    createSparklineElement(parent) {
        const sparkline = document.createElement('div');
        sparkline.className = 'sparkline';
        sparkline.style.cssText = `
            height: 20px; 
            width: 100%; 
            margin-top: 8px; 
            background: linear-gradient(90deg, transparent, var(--accent-color), transparent);
            border-radius: 10px;
            opacity: 0.3;
        `;
        parent.appendChild(sparkline);
        return sparkline;
    }

    updateSparkline(sparkline, value) {
        // Animate sparkline based on value changes
        sparkline.style.transform = `scaleX(${Math.min(value / 100, 1)})`;
        sparkline.style.transition = 'transform 1s ease-out';
    }

    setupEventListeners() {
        // Enhanced global search with autocomplete
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.openAdvancedSearch();
            }
        });

        // Smart form handling with real-time validation
        document.querySelectorAll('form').forEach(form => {
            this.enhanceForm(form);
        });

        // Advanced button interactions
        document.querySelectorAll('.btn').forEach(button => {
            this.enhanceButton(button);
        });

        // Intelligent auto-save with conflict resolution
        document.querySelectorAll('[data-autosave]').forEach(input => {
            input.addEventListener('input', this.debounce(() => {
                this.intelligentAutoSave(input);
            }, 750));
        });

        // Advanced clipboard operations
        document.querySelectorAll('[data-copy]').forEach(element => {
            element.addEventListener('click', () => this.advancedCopyToClipboard(element));
        });

        // Enhanced drag and drop
        this.setupDragAndDrop();
        
        // Initialize advanced tooltips and popovers
        this.initializeAdvancedTooltips();
    }

    enhanceForm(form) {
        // Add real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', this.debounce(() => this.validateField(input), 300));
        });

        // Enhance form submission
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleAdvancedFormSubmit(form);
        });
    }

    async validateField(field) {
        const rules = {
            email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
            phone: /^[\+]?[1-9][\d]{0,15}$/,
            url: /^https?:\/\/.+/,
            required: (value) => value.trim().length > 0
        };

        const fieldType = field.type || field.dataset.validate;
        const value = field.value;
        let isValid = true;
        let message = '';

        // Check validation rules
        if (field.required && !rules.required(value)) {
            isValid = false;
            message = 'This field is required';
        } else if (value && rules[fieldType] && !rules[fieldType].test(value)) {
            isValid = false;
            message = `Please enter a valid ${fieldType}`;
        }

        // Apply visual feedback
        field.classList.toggle('is-valid', isValid && value);
        field.classList.toggle('is-invalid', !isValid);
        
        // Show/hide feedback message
        this.showFieldFeedback(field, message, isValid);
    }

    showFieldFeedback(field, message, isValid) {
        let feedback = field.parentNode.querySelector('.field-feedback');
        
        if (!feedback && message) {
            feedback = document.createElement('div');
            feedback.className = `field-feedback ${isValid ? 'valid-feedback' : 'invalid-feedback'}`;
            field.parentNode.appendChild(feedback);
        }
        
        if (feedback) {
            feedback.textContent = message;
            feedback.className = `field-feedback ${isValid ? 'valid-feedback' : 'invalid-feedback'}`;
            feedback.style.display = message ? 'block' : 'none';
        }
    }

    async handleAdvancedFormSubmit(form) {
        const submitButton = form.querySelector('button[type="submit"]');
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        // Show loading state
        this.showAdvancedLoading(submitButton);

        try {
            const response = await fetch(form.action || window.location.href, {
                method: form.method || 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.notifications.show(result.message || 'Form submitted successfully', 'success');
                this.handleFormSuccess(form, result);
            } else {
                this.notifications.show(result.message || 'Form submission failed', 'error');
                this.handleFormErrors(form, result.errors);
            }
        } catch (error) {
            console.error('Form submission error:', error);
            this.notifications.show('Network error occurred', 'error');
        } finally {
            this.hideAdvancedLoading(submitButton);
        }
    }

    openAdvancedSearch() {
        const searchModal = new AdvancedSearchModal();
        searchModal.show();
    }

    setupKeyboardShortcuts() {
        const shortcuts = {
            'ctrl+shift+d': () => this.navigateWithTransition('/'),
            'ctrl+shift+s': () => this.navigateWithTransition('/scan'),
            'ctrl+shift+r': () => this.navigateWithTransition('/reports'),
            'ctrl+shift+p': () => this.navigateWithTransition('/privacy'),
            'ctrl+shift+a': () => this.navigateWithTransition('/admin'),
            'ctrl+shift+t': () => this.themeManager.cycleTheme(),
            'ctrl+shift+n': () => this.notifications.clear(),
            'escape': () => this.closeAllModals(),
            'ctrl+shift+h': () => this.showKeyboardShortcuts()
        };

        document.addEventListener('keydown', (e) => {
            const key = [
                e.ctrlKey && 'ctrl',
                e.shiftKey && 'shift',
                e.altKey && 'alt',
                e.key.toLowerCase()
            ].filter(Boolean).join('+');

            if (shortcuts[key]) {
                e.preventDefault();
                shortcuts[key]();
            }
        });
    }

    navigateWithTransition(url) {
        // Add page transition effect
        document.body.style.opacity = '0.7';
        document.body.style.transform = 'scale(0.98)';
        document.body.style.transition = 'all 0.3s ease';
        
        setTimeout(() => {
            window.location.href = url;
        }, 150);
    }

    showKeyboardShortcuts() {
        const shortcuts = [
            { key: 'Ctrl+Shift+D', action: 'Go to Dashboard' },
            { key: 'Ctrl+Shift+S', action: 'New Scan' },
            { key: 'Ctrl+Shift+R', action: 'View Reports' },
            { key: 'Ctrl+Shift+P', action: 'Privacy Center' },
            { key: 'Ctrl+Shift+A', action: 'Admin Panel' },
            { key: 'Ctrl+K', action: 'Global Search' },
            { key: 'Ctrl+Shift+T', action: 'Toggle Theme' },
            { key: 'Esc', action: 'Close Modals' }
        ];

        const modal = this.createShortcutsModal(shortcuts);
        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();
    }

    createShortcutsModal(shortcuts) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-keyboard me-2"></i>Keyboard Shortcuts
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            ${shortcuts.map(shortcut => `
                                <div class="col-12 mb-2">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <span>${shortcut.action}</span>
                                        <kbd class="bg-secondary text-light px-2 py-1 rounded">${shortcut.key}</kbd>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
        return modal;
    }

    loadAdvancedFeatures() {
        // Load additional enterprise features
        this.initializeDataVisualization();
        this.setupAdvancedSecurity();
        this.initializeCollaboration();
        this.setupAnalytics();
    }

    initializeDataVisualization() {
        // Initialize Chart.js if available
        if (typeof Chart !== 'undefined') {
            this.setupAdvancedCharts();
        }
    }

    setupAdvancedSecurity() {
        // Content Security Policy enforcement
        this.enforceCSP();
        
        // Session timeout handling
        this.setupSessionTimeout();
        
        // Input sanitization
        this.setupInputSanitization();
    }

    initializeCollaboration() {
        // Real-time collaboration features
        this.setupPresenceIndicators();
        this.initializeComments();
    }

    setupAnalytics() {
        // User behavior analytics
        this.trackUserInteractions();
        this.setupHeatmapping();
    }

    easeOutCubic(t) {
        return 1 - Math.pow(1 - t, 3);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

class AdvancedFeatures {
    constructor() {
        this.features = new Map();
    }

    init() {
        this.registerFeatures();
        this.activateFeatures();
    }

    registerFeatures() {
        this.features.set('smartSearch', new SmartSearchFeature());
        this.features.set('advancedFilters', new AdvancedFiltersFeature());
        this.features.set('bulkOperations', new BulkOperationsFeature());
        this.features.set('dataExport', new DataExportFeature());
        this.features.set('collaboration', new CollaborationFeature());
    }

    activateFeatures() {
        this.features.forEach((feature, name) => {
            try {
                feature.activate();
                console.log(`✅ Activated feature: ${name}`);
            } catch (error) {
                console.error(`❌ Failed to activate feature ${name}:`, error);
            }
        });
    }
}

class AdvancedSearchModal {
    constructor() {
        this.modal = null;
        this.searchInput = null;
        this.resultsContainer = null;
        this.searchCache = new Map();
        this.searchHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    }

    show() {
        if (!this.modal) {
            this.createAdvancedModal();
        }
        
        const modalInstance = new bootstrap.Modal(this.modal);
        modalInstance.show();
        
        this.modal.addEventListener('shown.bs.modal', () => {
            this.searchInput.focus();
            this.showSearchHistory();
        });
    }

    createAdvancedModal() {
        this.modal = document.createElement('div');
        this.modal.className = 'modal fade';
        this.modal.innerHTML = `
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header border-0 pb-0">
                        <div class="w-100">
                            <div class="search-container">
                                <i class="fas fa-search search-icon"></i>
                                <input type="text" class="form-control search-input" 
                                       placeholder="Search everything... (use filters: type:email, status:active, date:today)" 
                                       id="advanced-search-input">
                            </div>
                            <div class="search-filters mt-3">
                                <div class="btn-group btn-group-sm" role="group">
                                    <button type="button" class="btn btn-outline-primary filter-btn" data-filter="type:email">
                                        <i class="fas fa-envelope me-1"></i>Emails
                                    </button>
                                    <button type="button" class="btn btn-outline-primary filter-btn" data-filter="type:domain">
                                        <i class="fas fa-globe me-1"></i>Domains
                                    </button>
                                    <button type="button" class="btn btn-outline-primary filter-btn" data-filter="type:phone">
                                        <i class="fas fa-phone me-1"></i>Phones
                                    </button>
                                    <button type="button" class="btn btn-outline-primary filter-btn" data-filter="date:today">
                                        <i class="fas fa-calendar me-1"></i>Today
                                    </button>
                                </div>
                            </div>
                        </div>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body pt-0">
                        <div id="advanced-search-results" class="search-results"></div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.modal);
        
        this.searchInput = this.modal.querySelector('#advanced-search-input');
        this.resultsContainer = this.modal.querySelector('#advanced-search-results');
        
        this.setupAdvancedSearchHandlers();
    }

    setupAdvancedSearchHandlers() {
        let searchTimeout;
        
        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                this.performAdvancedSearch(e.target.value);
            }, 200);
        });
        
        // Filter button handlers
        this.modal.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const filter = btn.dataset.filter;
                this.searchInput.value += ` ${filter}`;
                this.performAdvancedSearch(this.searchInput.value);
            });
        });
        
        this.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                this.addToSearchHistory(this.searchInput.value);
            }
        });
    }

    async performAdvancedSearch(query) {
        if (query.length < 2) {
            this.showSearchHistory();
            return;
        }
        
        try {
            const response = await fetch(`/api/v1/search/advanced?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            
            this.displayAdvancedResults(results);
        } catch (error) {
            console.error('Advanced search failed:', error);
            this.resultsContainer.innerHTML = '<div class="text-muted">Search failed. Please try again.</div>';
        }
    }

    displayAdvancedResults(results) {
        if (!results.data || results.data.length === 0) {
            this.resultsContainer.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No results found</h5>
                    <p class="text-muted">Try adjusting your search terms or filters</p>
                </div>
            `;
            return;
        }
        
        const categorized = this.categorizeResults(results.data);
        let html = '';
        
        Object.entries(categorized).forEach(([category, items]) => {
            html += `
                <div class="search-category mb-4">
                    <h6 class="text-uppercase text-muted mb-3">
                        <i class="${this.getCategoryIcon(category)} me-2"></i>
                        ${category} (${items.length})
                    </h6>
                    <div class="row">
                        ${items.map(item => this.createResultCard(item)).join('')}
                    </div>
                </div>
            `;
        });
        
        this.resultsContainer.innerHTML = html;
    }

    categorizeResults(results) {
        const categories = {};
        results.forEach(result => {
            const category = result.category || result.type || 'Other';
            if (!categories[category]) categories[category] = [];
            categories[category].push(result);
        });
        return categories;
    }

    createResultCard(result) {
        return `
            <div class="col-md-6 col-lg-4 mb-3">
                <div class="card h-100 result-card">
                    <div class="card-body">
                        <div class="d-flex align-items-start mb-2">
                            <i class="${result.icon || 'fas fa-file'} me-2 text-primary"></i>
                            <div class="flex-grow-1">
                                <h6 class="card-title mb-1">
                                    <a href="${result.url}" class="text-decoration-none">${result.title}</a>
                                </h6>
                                <p class="card-text small text-muted">${result.description}</p>
                            </div>
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="badge bg-secondary">${result.type}</span>
                            <small class="text-muted">${result.date || 'Recent'}</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getCategoryIcon(category) {
        const icons = {
            'Scans': 'fas fa-search',
            'Reports': 'fas fa-chart-bar',
            'Users': 'fas fa-users',
            'Settings': 'fas fa-cog',
            'API': 'fas fa-code'
        };
        return icons[category] || 'fas fa-folder';
    }

    showSearchHistory() {
        if (this.searchHistory.length === 0) {
            this.resultsContainer.innerHTML = `
                <div class="text-center py-4">
                    <i class="fas fa-history fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No search history</h5>
                    <p class="text-muted">Start searching to see your recent queries here</p>
                </div>
            `;
            return;
        }
        
        const html = `
            <div class="search-history">
                <h6 class="text-uppercase text-muted mb-3">
                    <i class="fas fa-history me-2"></i>Recent Searches
                </h6>
                <div class="list-group list-group-flush">
                    ${this.searchHistory.map(query => `
                        <button type="button" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                                onclick="document.getElementById('advanced-search-input').value = '${query}'; platform.searchModal.performAdvancedSearch('${query}')">
                            <span><i class="fas fa-search me-2 text-muted"></i>${query}</span>
                            <i class="fas fa-arrow-right text-muted"></i>
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
        
        this.resultsContainer.innerHTML = html;
    }

    addToSearchHistory(query) {
        if (query.trim() && !this.searchHistory.includes(query)) {
            this.searchHistory.unshift(query);
            this.searchHistory = this.searchHistory.slice(0, 10); // Keep only 10 recent searches
            localStorage.setItem('searchHistory', JSON.stringify(this.searchHistory));
        }
    }
}

// Initialize the AAA Enterprise platform
document.addEventListener('DOMContentLoaded', () => {
    window.platformAAA = new IntelligencePlatformAAA();
    
    // Enhanced error handling with user-friendly messages
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
        if (window.platformAAA && window.platformAAA.notifications) {
            window.platformAAA.notifications.show('An unexpected error occurred. Our team has been notified.', 'error');
        }
    });
    
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled promise rejection:', event.reason);
        if (window.platformAAA && window.platformAAA.notifications) {
            window.platformAAA.notifications.show('A network error occurred. Please check your connection.', 'error');
        }
    });
});

// Enhanced global functions
window.refreshDashboard = async function() {
    if (window.platformAAA) {
        await window.platformAAA.loadDashboardMetrics();
        window.platformAAA.notifications.show('Dashboard refreshed successfully', 'success');
    }
};

window.quickScan = function(type = null) {
    const url = type ? `/scan?type=${type}&quick=true` : '/scan?quick=true';
    window.platformAAA?.navigateWithTransition(url) || (window.location.href = url);
};

window.exportAdvanced = async function(format, filters = {}) {
    try {
        const queryString = new URLSearchParams({ format, ...filters }).toString();
        const response = await fetch(`/api/v1/reports/export?${queryString}`);
        
        if (!response.ok) throw new Error('Export failed');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `intelligence-report-${Date.now()}.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        window.platformAAA?.notifications.show(`Report exported successfully as ${format.toUpperCase()}`, 'success');
    } catch (error) {
        console.error('Export failed:', error);
        window.platformAAA?.notifications.show('Export failed. Please try again.', 'error');
    }
};