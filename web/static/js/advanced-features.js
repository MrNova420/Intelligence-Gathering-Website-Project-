/**
 * Advanced Features Implementation
 * Inspired by SocialFish, FutureCoder, GitHub, and Discord
 * Implementing cutting-edge UI/UX with holographic effects and AI-driven interactions
 */

class AdvancedIntelligencePlatform {
    constructor() {
        this.version = '2.0.0-enterprise';
        this.initialized = false;
        this.features = {
            holographicEffects: true,
            quantumBackground: true,
            aiAdaptiveUI: true,
            smartNotifications: true,
            contextualHelp: true,
            advancedSearch: true
        };
        
        this.init();
    }

    async init() {
        console.log('🚀 Initializing Advanced Intelligence Platform v' + this.version);
        
        // Initialize core systems
        await this.initializeHolographicSystem();
        await this.initializeQuantumBackground();
        await this.initializeAIAdaptiveUI();
        await this.initializeSmartOnboarding();
        await this.initializeAdvancedSearch();
        await this.initializeContextualHelp();
        
        this.setupAdvancedEventListeners();
        this.startPerformanceMonitoring();
        
        this.initialized = true;
        console.log('✅ Advanced Intelligence Platform initialized successfully');
        
        // Show welcome animation
        this.showWelcomeAnimation();
    }

    async initializeHolographicSystem() {
        console.log('🌟 Initializing Holographic Effects System...');
        
        // Create holographic container
        const holoContainer = document.createElement('div');
        holoContainer.className = 'holographic-container';
        holoContainer.innerHTML = `
            <div class="holographic-overlay"></div>
            <div class="holographic-particles"></div>
            <div class="holographic-grid"></div>
        `;
        document.body.appendChild(holoContainer);

        // Add holographic effects to cards
        const cards = document.querySelectorAll('.card, .modern-card');
        cards.forEach(card => {
            this.addHolographicEffect(card);
        });

        // Initialize holographic animations
        this.startHolographicAnimations();
    }

    addHolographicEffect(element) {
        element.classList.add('holographic-element');
        
        // Add holographic border
        const holoBorder = document.createElement('div');
        holoBorder.className = 'holographic-border';
        element.appendChild(holoBorder);

        // Add mouse tracking for holographic tilt
        element.addEventListener('mousemove', (e) => {
            const rect = element.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            element.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            
            // Update holographic gradient
            const gradient = `radial-gradient(circle at ${x}px ${y}px, rgba(99, 102, 241, 0.3) 0%, transparent 50%)`;
            holoBorder.style.background = gradient;
        });

        element.addEventListener('mouseleave', () => {
            element.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
            holoBorder.style.background = '';
        });
    }

    async initializeQuantumBackground() {
        console.log('🌌 Initializing Quantum Background System...');
        
        // Enhanced particle system with quantum effects
        const canvas = document.createElement('canvas');
        canvas.id = 'quantum-canvas';
        canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            pointer-events: none;
            opacity: 0.7;
        `;
        document.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Quantum particles with entanglement effects
        this.quantumParticles = [];
        this.createQuantumParticles(ctx, canvas);
        this.animateQuantumBackground(ctx, canvas);
    }

    createQuantumParticles(ctx, canvas) {
        const particleCount = Math.min(150, window.innerWidth / 10);
        
        for (let i = 0; i < particleCount; i++) {
            this.quantumParticles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 3 + 1,
                color: this.getQuantumColor(),
                opacity: Math.random() * 0.8 + 0.2,
                entangled: Math.random() > 0.7,
                phase: Math.random() * Math.PI * 2,
                energy: Math.random() * 100
            });
        }
    }

    getQuantumColor() {
        const colors = [
            '#60A5FA', '#A78BFA', '#34D399', '#F472B6', 
            '#FBBF24', '#FB7185', '#38BDF8', '#A855F7'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    animateQuantumBackground(ctx, canvas) {
        const animate = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            // Update quantum particles
            this.quantumParticles.forEach((particle, index) => {
                // Quantum tunneling effect
                if (Math.random() > 0.998) {
                    particle.x = Math.random() * canvas.width;
                    particle.y = Math.random() * canvas.height;
                }
                
                // Wave-particle duality
                particle.phase += 0.02;
                const waveOffset = Math.sin(particle.phase) * 2;
                
                // Update position
                particle.x += particle.vx + waveOffset;
                particle.y += particle.vy;
                
                // Boundary conditions with quantum reflection
                if (particle.x < 0 || particle.x > canvas.width) {
                    particle.vx *= -1;
                    particle.color = this.getQuantumColor();
                }
                if (particle.y < 0 || particle.y > canvas.height) {
                    particle.vy *= -1;
                    particle.color = this.getQuantumColor();
                }
                
                // Quantum entanglement effects
                if (particle.entangled) {
                    const nearbyParticles = this.quantumParticles.filter((p, i) => {
                        if (i === index) return false;
                        const distance = Math.sqrt(
                            Math.pow(p.x - particle.x, 2) + Math.pow(p.y - particle.y, 2)
                        );
                        return distance < 100;
                    });
                    
                    // Draw entanglement connections
                    nearbyParticles.forEach(p => {
                        ctx.save();
                        ctx.strokeStyle = particle.color;
                        ctx.globalAlpha = 0.1;
                        ctx.lineWidth = 0.5;
                        ctx.beginPath();
                        ctx.moveTo(particle.x, particle.y);
                        ctx.lineTo(p.x, p.y);
                        ctx.stroke();
                        ctx.restore();
                    });
                }
                
                // Draw particle with quantum glow
                ctx.save();
                ctx.globalAlpha = particle.opacity;
                
                // Quantum glow effect
                const gradient = ctx.createRadialGradient(
                    particle.x, particle.y, 0,
                    particle.x, particle.y, particle.size * 3
                );
                gradient.addColorStop(0, particle.color);
                gradient.addColorStop(1, 'transparent');
                
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size * 3, 0, Math.PI * 2);
                ctx.fill();
                
                // Core particle
                ctx.fillStyle = particle.color;
                ctx.beginPath();
                ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.restore();
            });
            
            requestAnimationFrame(animate);
        };
        
        animate();
    }

    async initializeAIAdaptiveUI() {
        console.log('🤖 Initializing AI Adaptive UI System...');
        
        // AI-driven user behavior analysis
        this.userBehavior = {
            clickPatterns: [],
            timeSpent: {},
            preferredFeatures: [],
            skillLevel: 'intermediate'
        };
        
        // Track user interactions
        this.startBehaviorTracking();
        
        // Adaptive recommendations
        this.showAdaptiveRecommendations();
    }

    startBehaviorTracking() {
        // Track clicks
        document.addEventListener('click', (e) => {
            if (e.target.closest('.card, .btn, .nav-link')) {
                this.userBehavior.clickPatterns.push({
                    element: e.target.className,
                    timestamp: Date.now(),
                    x: e.clientX,
                    y: e.clientY
                });
                
                // Keep only last 100 clicks
                if (this.userBehavior.clickPatterns.length > 100) {
                    this.userBehavior.clickPatterns.shift();
                }
            }
        });
        
        // Track time spent on sections
        const sections = document.querySelectorAll('.card, .dashboard-section');
        sections.forEach(section => {
            let enterTime = null;
            
            section.addEventListener('mouseenter', () => {
                enterTime = Date.now();
            });
            
            section.addEventListener('mouseleave', () => {
                if (enterTime) {
                    const timeSpent = Date.now() - enterTime;
                    const sectionId = section.id || section.className;
                    
                    if (!this.userBehavior.timeSpent[sectionId]) {
                        this.userBehavior.timeSpent[sectionId] = 0;
                    }
                    this.userBehavior.timeSpent[sectionId] += timeSpent;
                }
            });
        });
    }

    showAdaptiveRecommendations() {
        // Analyze user behavior and show contextual tips
        setTimeout(() => {
            const mostUsedSection = Object.keys(this.userBehavior.timeSpent)
                .reduce((a, b) => this.userBehavior.timeSpent[a] > this.userBehavior.timeSpent[b] ? a : b, '');
            
            if (mostUsedSection) {
                this.showSmartNotification(
                    `💡 Pro tip: Based on your usage, you might find the Advanced ${mostUsedSection} features helpful!`,
                    'info',
                    5000
                );
            }
        }, 30000); // Show after 30 seconds
    }

    async initializeSmartOnboarding() {
        console.log('🎓 Initializing Smart Onboarding System...');
        
        // Check if user is new
        const isNewUser = !localStorage.getItem('intelligence_platform_user');
        
        if (isNewUser) {
            setTimeout(() => {
                this.startInteractiveOnboarding();
            }, 2000);
        }
    }

    startInteractiveOnboarding() {
        const onboardingSteps = [
            {
                target: '.navbar-brand',
                title: 'Welcome to Intelligence Platform',
                content: 'This is your command center for advanced intelligence gathering and analysis.',
                position: 'bottom'
            },
            {
                target: '.quick-actions',
                title: 'Quick Actions',
                content: 'Start here for common intelligence tasks. Each action is optimized for different investigation types.',
                position: 'top'
            },
            {
                target: '.dashboard-metrics',
                title: 'Real-time Metrics',
                content: 'Monitor system performance and scan results in real-time with our advanced analytics.',
                position: 'bottom'
            },
            {
                target: '.intelligence-feed',
                title: 'Live Intelligence Feed',
                content: 'Stay updated with the latest intelligence data and automated threat detection.',
                position: 'top'
            }
        ];
        
        this.createOnboardingTour(onboardingSteps);
    }

    createOnboardingTour(steps) {
        let currentStep = 0;
        
        const showStep = (step) => {
            const target = document.querySelector(step.target);
            if (!target) return;
            
            // Create tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'onboarding-tooltip';
            tooltip.innerHTML = `
                <div class="onboarding-content">
                    <h4>${step.title}</h4>
                    <p>${step.content}</p>
                    <div class="onboarding-actions">
                        <button class="btn-skip">Skip Tour</button>
                        <button class="btn-next">${currentStep === steps.length - 1 ? 'Finish' : 'Next'}</button>
                    </div>
                    <div class="onboarding-progress">
                        ${currentStep + 1} of ${steps.length}
                    </div>
                </div>
                <div class="onboarding-arrow"></div>
            `;
            
            // Position tooltip
            const rect = target.getBoundingClientRect();
            tooltip.style.position = 'fixed';
            tooltip.style.zIndex = '10000';
            
            if (step.position === 'top') {
                tooltip.style.bottom = (window.innerHeight - rect.top + 10) + 'px';
                tooltip.style.left = (rect.left + rect.width / 2) + 'px';
                tooltip.style.transform = 'translateX(-50%)';
            } else {
                tooltip.style.top = (rect.bottom + 10) + 'px';
                tooltip.style.left = (rect.left + rect.width / 2) + 'px';
                tooltip.style.transform = 'translateX(-50%)';
            }
            
            document.body.appendChild(tooltip);
            
            // Highlight target
            target.classList.add('onboarding-highlight');
            
            // Event listeners
            tooltip.querySelector('.btn-next').addEventListener('click', () => {
                target.classList.remove('onboarding-highlight');
                document.body.removeChild(tooltip);
                
                currentStep++;
                if (currentStep < steps.length) {
                    setTimeout(() => showStep(steps[currentStep]), 500);
                } else {
                    localStorage.setItem('intelligence_platform_user', 'true');
                    this.showSmartNotification('🎉 Welcome aboard! You\'re ready to start gathering intelligence.', 'success');
                }
            });
            
            tooltip.querySelector('.btn-skip').addEventListener('click', () => {
                target.classList.remove('onboarding-highlight');
                document.body.removeChild(tooltip);
                localStorage.setItem('intelligence_platform_user', 'true');
            });
        };
        
        showStep(steps[currentStep]);
    }

    async initializeAdvancedSearch() {
        console.log('🔍 Initializing Advanced Search System...');
        
        // Create global search overlay
        this.searchOverlay = document.createElement('div');
        this.searchOverlay.className = 'advanced-search-overlay';
        this.searchOverlay.innerHTML = `
            <div class="advanced-search-container">
                <div class="search-header">
                    <h3>🔍 Advanced Intelligence Search</h3>
                    <button class="search-close">&times;</button>
                </div>
                <div class="search-input-container">
                    <input type="text" id="advanced-search-input" placeholder="Search intelligence data, commands, or documentation...">
                    <div class="search-suggestions"></div>
                </div>
                <div class="search-filters">
                    <button class="filter-btn active" data-filter="all">All</button>
                    <button class="filter-btn" data-filter="scans">Scans</button>
                    <button class="filter-btn" data-filter="reports">Reports</button>
                    <button class="filter-btn" data-filter="commands">Commands</button>
                    <button class="filter-btn" data-filter="docs">Documentation</button>
                </div>
                <div class="search-results"></div>
                <div class="search-footer">
                    <div class="search-shortcuts">
                        <span><kbd>↑</kbd><kbd>↓</kbd> Navigate</span>
                        <span><kbd>Enter</kbd> Select</span>
                        <span><kbd>Esc</kbd> Close</span>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(this.searchOverlay);
        
        this.setupAdvancedSearchEvents();
    }

    setupAdvancedSearchEvents() {
        const searchInput = this.searchOverlay.querySelector('#advanced-search-input');
        const searchResults = this.searchOverlay.querySelector('.search-results');
        const closeBtn = this.searchOverlay.querySelector('.search-close');
        
        // Search data
        this.searchData = [
            { type: 'scan', title: 'Email Investigation', url: '/scan?type=email', keywords: 'email analysis investigation osint' },
            { type: 'scan', title: 'Phone Number Lookup', url: '/scan?type=phone', keywords: 'phone number lookup investigation' },
            { type: 'scan', title: 'Domain Analysis', url: '/scan?type=domain', keywords: 'domain whois analysis website' },
            { type: 'scan', title: 'Social Media Investigation', url: '/scan?type=social', keywords: 'social media profile investigation' },
            { type: 'report', title: 'Recent Scans', url: '/reports', keywords: 'reports history results' },
            { type: 'command', title: 'Quick Scan', action: () => window.location.href = '/scan', keywords: 'quick fast scan start' },
            { type: 'command', title: 'Refresh Dashboard', action: () => window.location.reload(), keywords: 'refresh reload dashboard' },
            { type: 'docs', title: 'API Documentation', url: '/docs', keywords: 'api documentation endpoints' }
        ];
        
        let selectedIndex = -1;
        
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            selectedIndex = -1;
            
            if (query.length === 0) {
                searchResults.innerHTML = '';
                return;
            }
            
            const filteredResults = this.searchData.filter(item => 
                item.title.toLowerCase().includes(query) || 
                item.keywords.toLowerCase().includes(query)
            );
            
            this.displaySearchResults(filteredResults, query);
        });
        
        searchInput.addEventListener('keydown', (e) => {
            const results = searchResults.querySelectorAll('.search-result-item');
            
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedIndex = Math.min(selectedIndex + 1, results.length - 1);
                this.updateSelectedResult(results, selectedIndex);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedIndex = Math.max(selectedIndex - 1, -1);
                this.updateSelectedResult(results, selectedIndex);
            } else if (e.key === 'Enter' && selectedIndex >= 0) {
                e.preventDefault();
                results[selectedIndex].click();
            } else if (e.key === 'Escape') {
                this.hideAdvancedSearch();
            }
        });
        
        closeBtn.addEventListener('click', () => this.hideAdvancedSearch());
        
        this.searchOverlay.addEventListener('click', (e) => {
            if (e.target === this.searchOverlay) {
                this.hideAdvancedSearch();
            }
        });
    }

    displaySearchResults(results, query) {
        const searchResults = this.searchOverlay.querySelector('.search-results');
        
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="no-results">No results found</div>';
            return;
        }
        
        searchResults.innerHTML = results.map((result, index) => `
            <div class="search-result-item" data-index="${index}">
                <div class="result-icon">${this.getResultIcon(result.type)}</div>
                <div class="result-content">
                    <div class="result-title">${this.highlightQuery(result.title, query)}</div>
                    <div class="result-type">${result.type}</div>
                </div>
            </div>
        `).join('');
        
        // Add click events
        searchResults.querySelectorAll('.search-result-item').forEach((item, index) => {
            item.addEventListener('click', () => {
                const result = results[index];
                if (result.url) {
                    window.location.href = result.url;
                } else if (result.action) {
                    result.action();
                }
                this.hideAdvancedSearch();
            });
        });
    }

    getResultIcon(type) {
        const icons = {
            scan: '🔍',
            report: '📊',
            command: '⚡',
            docs: '📚'
        };
        return icons[type] || '📄';
    }

    highlightQuery(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    updateSelectedResult(results, selectedIndex) {
        results.forEach((result, index) => {
            result.classList.toggle('selected', index === selectedIndex);
        });
    }

    showAdvancedSearch() {
        this.searchOverlay.classList.add('active');
        this.searchOverlay.querySelector('#advanced-search-input').focus();
    }

    hideAdvancedSearch() {
        this.searchOverlay.classList.remove('active');
        this.searchOverlay.querySelector('#advanced-search-input').value = '';
        this.searchOverlay.querySelector('.search-results').innerHTML = '';
    }

    async initializeContextualHelp() {
        console.log('💡 Initializing Contextual Help System...');
        
        // Create help system
        this.helpSystem = new ContextualHelpSystem();
        this.helpSystem.init();
    }

    setupAdvancedEventListeners() {
        // Enhanced keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Cmd/Ctrl + K for search
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                this.showAdvancedSearch();
            }
            
            // '/' for quick search
            if (e.key === '/' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                this.showAdvancedSearch();
            }
            
            // '?' for help
            if (e.key === '?' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                this.helpSystem.showContextualHelp();
            }
        });
    }

    startPerformanceMonitoring() {
        // Monitor FPS and performance
        let lastTime = performance.now();
        let frames = 0;
        
        const measureFPS = (currentTime) => {
            frames++;
            
            if (currentTime - lastTime >= 1000) {
                const fps = Math.round((frames * 1000) / (currentTime - lastTime));
                
                // Update performance indicator
                const perfIndicator = document.querySelector('.performance-indicator');
                if (perfIndicator) {
                    perfIndicator.textContent = `${fps} FPS`;
                    perfIndicator.className = `performance-indicator ${fps > 50 ? 'good' : fps > 30 ? 'medium' : 'poor'}`;
                }
                
                frames = 0;
                lastTime = currentTime;
            }
            
            requestAnimationFrame(measureFPS);
        };
        
        requestAnimationFrame(measureFPS);
    }

    showWelcomeAnimation() {
        // Create welcome animation overlay
        const welcomeOverlay = document.createElement('div');
        welcomeOverlay.className = 'welcome-animation-overlay';
        welcomeOverlay.innerHTML = `
            <div class="welcome-content">
                <div class="welcome-logo">🚀</div>
                <h2>Intelligence Platform</h2>
                <p>Advanced • Secure • Intelligent</p>
                <div class="welcome-progress"></div>
            </div>
        `;
        document.body.appendChild(welcomeOverlay);
        
        // Animate welcome
        setTimeout(() => {
            welcomeOverlay.classList.add('fade-out');
            setTimeout(() => {
                document.body.removeChild(welcomeOverlay);
            }, 1000);
        }, 2000);
    }

    showSmartNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `smart-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">${this.getNotificationIcon(type)}</div>
                <div class="notification-message">${message}</div>
                <button class="notification-close">&times;</button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto-hide
        const hideNotification = () => {
            notification.classList.add('hide');
            setTimeout(() => {
                if (document.body.contains(notification)) {
                    document.body.removeChild(notification);
                }
            }, 300);
        };
        
        setTimeout(hideNotification, duration);
        
        // Close button
        notification.querySelector('.notification-close').addEventListener('click', hideNotification);
    }

    getNotificationIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || 'ℹ️';
    }

    startHolographicAnimations() {
        // Animate holographic elements
        const holoElements = document.querySelectorAll('.holographic-element');
        
        setInterval(() => {
            holoElements.forEach(element => {
                const intensity = Math.random() * 0.3 + 0.7;
                element.style.setProperty('--holo-intensity', intensity);
            });
        }, 2000);
    }
}

class ContextualHelpSystem {
    constructor() {
        this.helpData = {
            dashboard: 'The dashboard provides real-time monitoring of your intelligence gathering operations.',
            scan: 'Intelligence scanning allows you to gather information from various sources using OSINT techniques.',
            reports: 'View and analyze results from your intelligence gathering activities.',
            api: 'Access our RESTful API for programmatic intelligence gathering.'
        };
    }

    init() {
        this.createHelpOverlay();
    }

    createHelpOverlay() {
        this.helpOverlay = document.createElement('div');
        this.helpOverlay.className = 'contextual-help-overlay';
        this.helpOverlay.innerHTML = `
            <div class="help-container">
                <div class="help-header">
                    <h3>💡 Contextual Help</h3>
                    <button class="help-close">&times;</button>
                </div>
                <div class="help-content">
                    <div class="help-section">
                        <h4>Keyboard Shortcuts</h4>
                        <div class="shortcut-list">
                            <div><kbd>Cmd</kbd> + <kbd>K</kbd> - Advanced Search</div>
                            <div><kbd>/</kbd> - Quick Search</div>
                            <div><kbd>?</kbd> - Show Help</div>
                            <div><kbd>Esc</kbd> - Close Overlays</div>
                        </div>
                    </div>
                    <div class="help-section">
                        <h4>Quick Actions</h4>
                        <ul>
                            <li>Click any metric card for detailed analysis</li>
                            <li>Use hover effects to reveal additional information</li>
                            <li>Access context menus with right-click</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(this.helpOverlay);
        
        this.helpOverlay.querySelector('.help-close').addEventListener('click', () => {
            this.hideContextualHelp();
        });
        
        this.helpOverlay.addEventListener('click', (e) => {
            if (e.target === this.helpOverlay) {
                this.hideContextualHelp();
            }
        });
    }

    showContextualHelp() {
        this.helpOverlay.classList.add('active');
    }

    hideContextualHelp() {
        this.helpOverlay.classList.remove('active');
    }
}

// Initialize the advanced platform
document.addEventListener('DOMContentLoaded', () => {
    window.advancedPlatform = new AdvancedIntelligencePlatform();
});