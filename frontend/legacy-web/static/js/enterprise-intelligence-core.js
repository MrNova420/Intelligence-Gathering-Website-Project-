/**
 * Enterprise Intelligence Core System
 * Advanced intelligence gathering platform with AI capabilities
 * Comprehensive feature set including scanning, analysis, reporting, and collaboration
 */

class EnterpriseIntelligenceCore {
    constructor() {
        this.version = '2.0.0';
        this.modules = {
            scanner: new IntelligenceScannerModule(),
            analyzer: new DataAnalysisModule(),
            reporter: new ReportingModule(),
            collaboration: new CollaborationModule(),
            security: new SecurityModule(),
            ai: new AIIntelligenceModule(),
            visualization: new DataVisualizationModule(),
            workflow: new WorkflowAutomationModule()
        };
        
        this.state = {
            currentScan: null,
            activeUsers: new Set(),
            scanHistory: [],
            systemHealth: {
                status: 'operational',
                uptime: 0,
                performance: 100,
                lastUpdate: Date.now()
            }
        };
        
        this.config = {
            maxConcurrentScans: 10,
            scanTimeout: 300000, // 5 minutes
            retryAttempts: 3,
            dataRetentionDays: 90,
            realTimeUpdates: true,
            aiAssistance: true
        };
        
        this.eventBus = new EventBus();
        this.init();
    }

    async init() {
        console.log(`🚀 Initializing Enterprise Intelligence Core v${this.version}`);
        
        try {
            await this.initializeModules();
            await this.setupEventListeners();
            await this.loadUserPreferences();
            await this.establishConnections();
            this.startHealthMonitoring();
            this.enableRealtimeFeatures();
            
            console.log('✅ Enterprise Intelligence Core initialized successfully');
            this.eventBus.emit('system:ready', { version: this.version });
        } catch (error) {
            console.error('❌ Failed to initialize Enterprise Intelligence Core:', error);
            this.eventBus.emit('system:error', { error, phase: 'initialization' });
        }
    }

    async initializeModules() {
        console.log('🔧 Initializing modules...');
        
        for (const [name, module] of Object.entries(this.modules)) {
            try {
                await module.init(this);
                console.log(`✅ Module ${name} initialized`);
            } catch (error) {
                console.error(`❌ Failed to initialize module ${name}:`, error);
                // Continue with other modules
            }
        }
    }

    async setupEventListeners() {
        // Global event handlers
        this.eventBus.on('scan:started', this.handleScanStarted.bind(this));
        this.eventBus.on('scan:completed', this.handleScanCompleted.bind(this));
        this.eventBus.on('scan:error', this.handleScanError.bind(this));
        this.eventBus.on('user:joined', this.handleUserJoined.bind(this));
        this.eventBus.on('user:left', this.handleUserLeft.bind(this));
        this.eventBus.on('data:updated', this.handleDataUpdated.bind(this));
        this.eventBus.on('threat:detected', this.handleThreatDetected.bind(this));
        this.eventBus.on('system:maintenance', this.handleSystemMaintenance.bind(this));
    }

    // ===== SCANNING OPERATIONS =====
    
    async startScan(scanConfig) {
        console.log('🔍 Starting new intelligence scan...', scanConfig);
        
        try {
            // Validate scan configuration
            const validatedConfig = await this.validateScanConfig(scanConfig);
            
            // Check concurrent scan limits
            if (this.getActiveScanCount() >= this.config.maxConcurrentScans) {
                throw new Error('Maximum concurrent scans reached');
            }
            
            // Create scan instance
            const scan = await this.modules.scanner.createScan(validatedConfig);
            this.state.currentScan = scan;
            
            // Start scan execution
            const results = await this.modules.scanner.execute(scan);
            
            // Process results through AI analysis
            if (this.config.aiAssistance) {
                results.aiAnalysis = await this.modules.ai.analyzeResults(results);
            }
            
            // Generate report
            const report = await this.modules.reporter.generateReport(results);
            
            // Store in history
            this.state.scanHistory.unshift({
                id: scan.id,
                timestamp: new Date().toISOString(),
                config: validatedConfig,
                results,
                report
            });
            
            this.eventBus.emit('scan:completed', { scan, results, report });
            return { scan, results, report };
            
        } catch (error) {
            console.error('❌ Scan failed:', error);
            this.eventBus.emit('scan:error', { error, config: scanConfig });
            throw error;
        }
    }

    async validateScanConfig(config) {
        const required = ['target', 'scanType', 'modules'];
        const missing = required.filter(field => !config[field]);
        
        if (missing.length > 0) {
            throw new Error(`Missing required fields: ${missing.join(', ')}`);
        }
        
        // Sanitize inputs
        const sanitized = {
            ...config,
            target: this.sanitizeTarget(config.target),
            scanType: this.validateScanType(config.scanType),
            modules: this.validateModules(config.modules),
            options: config.options || {},
            timeout: config.timeout || this.config.scanTimeout,
            retries: config.retries || this.config.retryAttempts
        };
        
        return sanitized;
    }

    sanitizeTarget(target) {
        // Remove potentially dangerous characters
        return target.replace(/[<>"/\\&]/g, '').trim();
    }

    validateScanType(scanType) {
        const validTypes = [
            'email_lookup',
            'phone_lookup', 
            'username_search',
            'domain_analysis',
            'social_media_scan',
            'comprehensive_search',
            'threat_assessment',
            'digital_footprint'
        ];
        
        if (!validTypes.includes(scanType)) {
            throw new Error(`Invalid scan type: ${scanType}`);
        }
        
        return scanType;
    }

    validateModules(modules) {
        const availableModules = [
            'email_verification',
            'phone_validation', 
            'social_media_search',
            'domain_intelligence',
            'breach_detection',
            'reputation_analysis',
            'geolocation_tracking',
            'network_analysis'
        ];
        
        const invalidModules = modules.filter(m => !availableModules.includes(m));
        if (invalidModules.length > 0) {
            throw new Error(`Invalid modules: ${invalidModules.join(', ')}`);
        }
        
        return modules;
    }

    getActiveScanCount() {
        return this.modules.scanner.getActiveScanCount();
    }

    async pauseScan(scanId) {
        return this.modules.scanner.pauseScan(scanId);
    }

    async resumeScan(scanId) {
        return this.modules.scanner.resumeScan(scanId);
    }

    async cancelScan(scanId) {
        return this.modules.scanner.cancelScan(scanId);
    }

    // ===== DATA ANALYSIS =====
    
    async analyzeData(data, options = {}) {
        console.log('📊 Starting data analysis...');
        
        try {
            // Preprocess data
            const preprocessed = await this.modules.analyzer.preprocess(data);
            
            // Run analysis algorithms
            const analysis = await this.modules.analyzer.analyze(preprocessed, options);
            
            // Generate insights
            const insights = await this.modules.ai.generateInsights(analysis);
            
            // Create visualizations
            const visualizations = await this.modules.visualization.createCharts(analysis);
            
            const result = {
                analysis,
                insights,
                visualizations,
                metadata: {
                    timestamp: new Date().toISOString(),
                    dataSize: data.length,
                    processingTime: analysis.processingTime
                }
            };
            
            this.eventBus.emit('analysis:completed', result);
            return result;
            
        } catch (error) {
            console.error('❌ Analysis failed:', error);
            this.eventBus.emit('analysis:error', { error, data });
            throw error;
        }
    }

    async correlateData(datasets) {
        return this.modules.analyzer.correlate(datasets);
    }

    async detectAnomalies(data) {
        return this.modules.ai.detectAnomalies(data);
    }

    async predictTrends(historicalData) {
        return this.modules.ai.predictTrends(historicalData);
    }

    // ===== REPORTING =====
    
    async generateReport(data, template = 'comprehensive') {
        console.log('📋 Generating intelligence report...');
        
        try {
            const report = await this.modules.reporter.generate(data, {
                template,
                includeVisualizations: true,
                includeAIInsights: this.config.aiAssistance,
                format: 'html'
            });
            
            this.eventBus.emit('report:generated', { report, template });
            return report;
            
        } catch (error) {
            console.error('❌ Report generation failed:', error);
            throw error;
        }
    }

    async exportReport(reportId, format = 'pdf') {
        return this.modules.reporter.export(reportId, format);
    }

    async scheduleReport(config) {
        return this.modules.workflow.scheduleTask('generate_report', config);
    }

    // ===== COLLABORATION =====
    
    async shareResults(resultsId, users, permissions = 'read') {
        console.log('👥 Sharing results with team...');
        
        try {
            const shareConfig = {
                resultsId,
                users: Array.isArray(users) ? users : [users],
                permissions,
                timestamp: new Date().toISOString(),
                sharedBy: this.getCurrentUser()
            };
            
            const shareResult = await this.modules.collaboration.share(shareConfig);
            
            // Send notifications
            await this.notifyUsers(users, 'results_shared', {
                resultsId,
                sharedBy: shareConfig.sharedBy
            });
            
            this.eventBus.emit('results:shared', shareResult);
            return shareResult;
            
        } catch (error) {
            console.error('❌ Sharing failed:', error);
            throw error;
        }
    }

    async createTeam(teamConfig) {
        return this.modules.collaboration.createTeam(teamConfig);
    }

    async inviteUser(email, role = 'analyst') {
        return this.modules.collaboration.inviteUser(email, role);
    }

    async startVideoCall(participants) {
        return this.modules.collaboration.startVideoCall(participants);
    }

    // ===== SECURITY =====
    
    async authenticateUser(credentials) {
        return this.modules.security.authenticate(credentials);
    }

    async authorizeAction(userId, action, resource) {
        return this.modules.security.authorize(userId, action, resource);
    }

    async auditAction(userId, action, details) {
        return this.modules.security.auditLog(userId, action, details);
    }

    async encryptSensitiveData(data) {
        return this.modules.security.encrypt(data);
    }

    async decryptSensitiveData(encryptedData) {
        return this.modules.security.decrypt(encryptedData);
    }

    // ===== AI CAPABILITIES =====
    
    async getAIRecommendations(context) {
        return this.modules.ai.getRecommendations(context);
    }

    async askAIAssistant(question, context = {}) {
        console.log('🤖 Asking AI Assistant:', question);
        
        try {
            const response = await this.modules.ai.processQuery(question, {
                context,
                userId: this.getCurrentUser(),
                timestamp: new Date().toISOString()
            });
            
            this.eventBus.emit('ai:response', { question, response });
            return response;
            
        } catch (error) {
            console.error('❌ AI Assistant error:', error);
            throw error;
        }
    }

    async trainAIModel(trainingData) {
        return this.modules.ai.train(trainingData);
    }

    // ===== WORKFLOW AUTOMATION =====
    
    async createWorkflow(workflowConfig) {
        return this.modules.workflow.create(workflowConfig);
    }

    async executeWorkflow(workflowId, inputs = {}) {
        return this.modules.workflow.execute(workflowId, inputs);
    }

    async scheduleWorkflow(workflowId, schedule) {
        return this.modules.workflow.schedule(workflowId, schedule);
    }

    // ===== SYSTEM MONITORING =====
    
    startHealthMonitoring() {
        setInterval(() => {
            this.updateSystemHealth();
        }, 30000); // Update every 30 seconds
    }

    updateSystemHealth() {
        const health = {
            status: this.calculateSystemStatus(),
            uptime: Date.now() - this.state.systemHealth.lastUpdate,
            performance: this.calculatePerformanceScore(),
            lastUpdate: Date.now(),
            modules: this.getModuleHealthStatus()
        };
        
        this.state.systemHealth = health;
        this.eventBus.emit('system:health_updated', health);
    }

    calculateSystemStatus() {
        const moduleStatuses = Object.values(this.modules).map(module => 
            module.getStatus ? module.getStatus() : 'unknown'
        );
        
        if (moduleStatuses.includes('error')) return 'degraded';
        if (moduleStatuses.includes('warning')) return 'warning';
        return 'operational';
    }

    calculatePerformanceScore() {
        // Simple performance calculation based on response times
        const recentTasks = this.getRecentTaskPerformance();
        if (recentTasks.length === 0) return 100;
        
        const avgResponseTime = recentTasks.reduce((sum, task) => sum + task.duration, 0) / recentTasks.length;
        
        // Score based on response time (lower is better)
        if (avgResponseTime < 1000) return 100;
        if (avgResponseTime < 3000) return 80;
        if (avgResponseTime < 5000) return 60;
        return 40;
    }

    getModuleHealthStatus() {
        const status = {};
        for (const [name, module] of Object.entries(this.modules)) {
            status[name] = module.getHealth ? module.getHealth() : 'unknown';
        }
        return status;
    }

    // ===== REAL-TIME FEATURES =====
    
    enableRealtimeFeatures() {
        if (!this.config.realTimeUpdates) return;
        
        // WebSocket connection for real-time updates
        this.setupWebSocketConnection();
        
        // Real-time collaboration
        this.modules.collaboration.enableRealtime();
        
        // Live data streaming
        this.setupLiveDataStreaming();
    }

    setupWebSocketConnection() {
        // WebSocket implementation would go here
        console.log('🔗 Setting up WebSocket connection for real-time updates');
    }

    setupLiveDataStreaming() {
        // Live data streaming implementation
        console.log('📡 Setting up live data streaming');
    }

    // ===== EVENT HANDLERS =====
    
    handleScanStarted(event) {
        console.log('🔍 Scan started:', event.scan.id);
        this.updateUI('scan_started', event);
    }

    handleScanCompleted(event) {
        console.log('✅ Scan completed:', event.scan.id);
        this.updateUI('scan_completed', event);
        
        // Auto-generate insights if AI is enabled
        if (this.config.aiAssistance) {
            this.modules.ai.generateInsights(event.results);
        }
    }

    handleScanError(event) {
        console.error('❌ Scan error:', event.error);
        this.updateUI('scan_error', event);
        
        // Auto-retry if configured
        if (event.config.retries > 0) {
            setTimeout(() => {
                this.startScan({
                    ...event.config,
                    retries: event.config.retries - 1
                });
            }, 5000);
        }
    }

    handleUserJoined(event) {
        this.state.activeUsers.add(event.userId);
        this.updateUI('user_joined', event);
    }

    handleUserLeft(event) {
        this.state.activeUsers.delete(event.userId);
        this.updateUI('user_left', event);
    }

    handleDataUpdated(event) {
        this.updateUI('data_updated', event);
        
        // Trigger real-time analysis if enabled
        if (this.config.realTimeUpdates) {
            this.analyzeData(event.data, { realtime: true });
        }
    }

    handleThreatDetected(event) {
        console.warn('⚠️ Threat detected:', event.threat);
        this.updateUI('threat_detected', event);
        
        // Auto-escalate critical threats
        if (event.threat.severity === 'critical') {
            this.escalateThreat(event.threat);
        }
    }

    handleSystemMaintenance(event) {
        console.log('🔧 System maintenance:', event.type);
        this.updateUI('system_maintenance', event);
    }

    // ===== UTILITY METHODS =====
    
    updateUI(eventType, data) {
        // Update UI components based on events
        const uiEvent = new CustomEvent('intelligence:update', {
            detail: { type: eventType, data }
        });
        document.dispatchEvent(uiEvent);
    }

    async notifyUsers(users, type, data) {
        for (const user of users) {
            await this.modules.collaboration.sendNotification(user, type, data);
        }
    }

    getCurrentUser() {
        // Get current user context
        return window.currentUser || 'anonymous';
    }

    getRecentTaskPerformance() {
        // Return recent task performance metrics
        return this.state.recentTasks || [];
    }

    async escalateThreat(threat) {
        // Escalate critical threats to administrators
        const admins = await this.modules.security.getAdministrators();
        await this.notifyUsers(admins, 'threat_escalation', threat);
    }

    // ===== PUBLIC API =====
    
    getSystemInfo() {
        return {
            version: this.version,
            status: this.state.systemHealth.status,
            uptime: this.state.systemHealth.uptime,
            activeUsers: this.state.activeUsers.size,
            activeScanCount: this.getActiveScanCount(),
            lastUpdate: this.state.systemHealth.lastUpdate
        };
    }

    getCapabilities() {
        return {
            scanning: Object.keys(this.modules.scanner.getAvailableModules()),
            analysis: Object.keys(this.modules.analyzer.getCapabilities()),
            ai: this.modules.ai.getCapabilities(),
            collaboration: this.modules.collaboration.getFeatures(),
            security: this.modules.security.getFeatures()
        };
    }

    async shutdown() {
        console.log('🛑 Shutting down Enterprise Intelligence Core...');
        
        // Cancel active scans
        await this.modules.scanner.cancelAllScans();
        
        // Close connections
        await this.closeConnections();
        
        // Cleanup modules
        for (const module of Object.values(this.modules)) {
            if (module.cleanup) {
                await module.cleanup();
            }
        }
        
        this.eventBus.emit('system:shutdown');
        console.log('✅ Shutdown complete');
    }

    async closeConnections() {
        // Close WebSocket and other connections
        console.log('🔌 Closing connections...');
    }
}

// ===== MODULE CLASSES =====

class IntelligenceScannerModule {
    constructor() {
        this.activeScans = new Map();
        this.scanQueue = [];
        this.availableModules = new Map();
    }

    async init(core) {
        this.core = core;
        console.log('🔍 Scanner module initialized');
    }

    async createScan(config) {
        const scan = {
            id: this.generateScanId(),
            config,
            status: 'created',
            createdAt: new Date().toISOString(),
            progress: 0
        };
        
        this.activeScans.set(scan.id, scan);
        return scan;
    }

    async execute(scan) {
        scan.status = 'running';
        scan.startedAt = new Date().toISOString();
        
        try {
            const results = await this.performScan(scan);
            scan.status = 'completed';
            scan.completedAt = new Date().toISOString();
            scan.results = results;
            return results;
        } catch (error) {
            scan.status = 'failed';
            scan.error = error.message;
            throw error;
        } finally {
            this.activeScans.delete(scan.id);
        }
    }

    async performScan(scan) {
        // Simulate scan execution
        console.log(`🔍 Executing scan ${scan.id}...`);
        
        // Progress simulation
        for (let progress = 0; progress <= 100; progress += 10) {
            scan.progress = progress;
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        return {
            target: scan.config.target,
            scanType: scan.config.scanType,
            findings: this.generateMockFindings(),
            metadata: {
                duration: 1000,
                modulesUsed: scan.config.modules,
                confidence: 0.85
            }
        };
    }

    generateMockFindings() {
        return [
            {
                type: 'email_found',
                value: 'example@domain.com',
                source: 'social_media',
                confidence: 0.9
            },
            {
                type: 'phone_found',
                value: '+1234567890',
                source: 'public_records',
                confidence: 0.8
            }
        ];
    }

    generateScanId() {
        return 'scan_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    getActiveScanCount() {
        return this.activeScans.size;
    }

    async cancelAllScans() {
        for (const scan of this.activeScans.values()) {
            scan.status = 'cancelled';
        }
        this.activeScans.clear();
    }

    getAvailableModules() {
        return {
            email_verification: 'Email address validation and enrichment',
            phone_validation: 'Phone number validation and carrier lookup',
            social_media_search: 'Social media profile discovery',
            domain_intelligence: 'Domain and website analysis'
        };
    }
}

class DataAnalysisModule {
    async init(core) {
        this.core = core;
        console.log('📊 Analysis module initialized');
    }

    async preprocess(data) {
        // Data preprocessing logic
        return data;
    }

    async analyze(data, options) {
        // Analysis logic
        return {
            summary: 'Analysis complete',
            processingTime: 500,
            insights: []
        };
    }

    async correlate(datasets) {
        // Data correlation logic
        return { correlations: [] };
    }

    getCapabilities() {
        return {
            preprocessing: 'Data cleaning and normalization',
            statistical_analysis: 'Statistical analysis and modeling',
            pattern_recognition: 'Pattern and anomaly detection'
        };
    }
}

class ReportingModule {
    async init(core) {
        this.core = core;
        console.log('📋 Reporting module initialized');
    }

    async generate(data, options) {
        // Report generation logic
        return {
            id: this.generateReportId(),
            title: 'Intelligence Report',
            content: 'Report content here',
            format: options.format,
            createdAt: new Date().toISOString()
        };
    }

    async export(reportId, format) {
        // Export logic
        return { exportUrl: `/reports/${reportId}.${format}` };
    }

    generateReportId() {
        return 'report_' + Date.now();
    }
}

class CollaborationModule {
    async init(core) {
        this.core = core;
        console.log('👥 Collaboration module initialized');
    }

    async share(config) {
        // Sharing logic
        return { shareId: 'share_' + Date.now() };
    }

    async createTeam(config) {
        return { teamId: 'team_' + Date.now() };
    }

    async inviteUser(email, role) {
        return { inviteId: 'invite_' + Date.now() };
    }

    async startVideoCall(participants) {
        return { callId: 'call_' + Date.now() };
    }

    async sendNotification(user, type, data) {
        console.log(`📨 Sending notification to ${user}:`, type);
    }

    enableRealtime() {
        console.log('🔄 Real-time collaboration enabled');
    }

    getFeatures() {
        return {
            team_management: 'Team creation and management',
            real_time_collaboration: 'Real-time collaborative editing',
            video_conferencing: 'Integrated video calls'
        };
    }
}

class SecurityModule {
    async init(core) {
        this.core = core;
        console.log('🔒 Security module initialized');
    }

    async authenticate(credentials) {
        // Authentication logic
        return { success: true, token: 'jwt_token' };
    }

    async authorize(userId, action, resource) {
        // Authorization logic
        return true;
    }

    async auditLog(userId, action, details) {
        console.log(`📝 Audit: ${userId} performed ${action}`);
    }

    async encrypt(data) {
        // Encryption logic
        return 'encrypted_' + btoa(JSON.stringify(data));
    }

    async decrypt(encryptedData) {
        // Decryption logic
        return JSON.parse(atob(encryptedData.replace('encrypted_', '')));
    }

    async getAdministrators() {
        return ['admin@example.com'];
    }

    getFeatures() {
        return {
            multi_factor_auth: 'Multi-factor authentication',
            role_based_access: 'Role-based access control',
            audit_logging: 'Comprehensive audit logging'
        };
    }
}

class AIIntelligenceModule {
    async init(core) {
        this.core = core;
        console.log('🤖 AI module initialized');
    }

    async analyzeResults(results) {
        // AI analysis logic
        return {
            confidence: 0.85,
            insights: ['High confidence match found'],
            recommendations: ['Investigate further']
        };
    }

    async generateInsights(data) {
        return {
            insights: ['Pattern detected in data'],
            confidence: 0.8
        };
    }

    async detectAnomalies(data) {
        return { anomalies: [] };
    }

    async predictTrends(data) {
        return { trends: [] };
    }

    async getRecommendations(context) {
        return {
            recommendations: ['Try advanced search options'],
            confidence: 0.7
        };
    }

    async processQuery(question, context) {
        return {
            answer: 'Based on the available data...',
            confidence: 0.8,
            sources: []
        };
    }

    async train(data) {
        return { success: true, modelVersion: '1.1' };
    }

    getCapabilities() {
        return {
            natural_language_processing: 'NLP for query understanding',
            machine_learning: 'ML-powered insights and predictions',
            anomaly_detection: 'AI-powered anomaly detection'
        };
    }
}

class DataVisualizationModule {
    async init(core) {
        this.core = core;
        console.log('📈 Visualization module initialized');
    }

    async createCharts(data) {
        return {
            charts: [
                { type: 'bar', title: 'Data Distribution' },
                { type: 'line', title: 'Trends Over Time' }
            ]
        };
    }
}

class WorkflowAutomationModule {
    constructor() {
        this.workflows = new Map();
        this.scheduledTasks = new Map();
    }

    async init(core) {
        this.core = core;
        console.log('⚡ Workflow module initialized');
    }

    async create(config) {
        const workflow = {
            id: 'workflow_' + Date.now(),
            config,
            createdAt: new Date().toISOString()
        };
        
        this.workflows.set(workflow.id, workflow);
        return workflow;
    }

    async execute(workflowId, inputs) {
        const workflow = this.workflows.get(workflowId);
        if (!workflow) {
            throw new Error('Workflow not found');
        }
        
        return { success: true, result: 'Workflow executed' };
    }

    async schedule(workflowId, schedule) {
        return { scheduleId: 'schedule_' + Date.now() };
    }

    async scheduleTask(taskType, config) {
        return { taskId: 'task_' + Date.now() };
    }
}

// Simple Event Bus Implementation
class EventBus {
    constructor() {
        this.events = {};
    }

    on(event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(callback);
    }

    emit(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in event handler for ${event}:`, error);
                }
            });
        }
    }

    off(event, callback) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(cb => cb !== callback);
        }
    }
}

// Initialize the Enterprise Intelligence Core
let enterpriseCore = null;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        enterpriseCore = new EnterpriseIntelligenceCore();
        window.enterpriseCore = enterpriseCore;
        console.log('🚀 Enterprise Intelligence Platform is ready!');
    } catch (error) {
        console.error('❌ Failed to initialize platform:', error);
    }
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { 
        EnterpriseIntelligenceCore,
        IntelligenceScannerModule,
        DataAnalysisModule,
        ReportingModule,
        CollaborationModule,
        SecurityModule,
        AIIntelligenceModule,
        DataVisualizationModule,
        WorkflowAutomationModule
    };
}

// Global export for browser
if (typeof window !== 'undefined') {
    window.EnterpriseIntelligenceCore = EnterpriseIntelligenceCore;
}