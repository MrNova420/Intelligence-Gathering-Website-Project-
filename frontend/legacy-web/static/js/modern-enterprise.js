/**
 * Intelligence Gathering Platform - Modern AAA Enterprise JavaScript Framework
 * Advanced client-side functionality with modern animations and interactions
 * Inspired by GitHub, Discord, Linear, and top-tier platforms
 */

class ModernIntelligencePlatform {
    constructor() {
        this.apiBase = '/api/v1';
        this.animations = new ModernAnimationSystem();
        this.ui = new ModernUIManager();
        this.performance = new PerformanceMonitor();
        this.shortcuts = new KeyboardShortcuts();
        this.particles = new ParticleSystem();
        this.notifications = new NotificationSystem();
        this.init();
    }

    async init() {
        console.log('🚀 Initializing Modern Intelligence Platform...');
        
        // Initialize systems in order
        await this.initializeAnimations();
        this.setupEventListeners();
        this.initializeParticles();
        this.setupKeyboardShortcuts();
        this.initializeUI();
        this.startPerformanceMonitoring();
        
        console.log('✅ Modern Intelligence Platform initialized successfully');
    }

    async initializeAnimations() {
        // Initialize Intersection Observer for scroll animations
        this.setupScrollAnimations();
        
        // Add smooth page transitions
        this.setupPageTransitions();
        
        // Initialize hover effects
        this.setupHoverEffects();
        
        // Add loading animations
        this.setupLoadingAnimations();
    }

    setupScrollAnimations() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-slide-up');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observe all cards and main content sections
        document.querySelectorAll('.card, .alert, .btn-group').forEach(el => {
            observer.observe(el);
        });
    }

    setupPageTransitions() {
        // Add smooth transitions between pages
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href]');
            if (link && link.href && !link.href.startsWith('mailto:') && !link.href.startsWith('tel:')) {
                const isInternal = link.href.startsWith(window.location.origin);
                const isNotExternal = !link.target || link.target === '_self';
                
                if (isInternal && isNotExternal) {
                    e.preventDefault();
                    this.navigateWithTransition(link.href);
                }
            }
        });
    }

    navigateWithTransition(url) {
        // Create transition overlay
        const overlay = document.createElement('div');
        overlay.className = 'transition-overlay';
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--slate-900) 0%, var(--slate-800) 100%);
            z-index: 9999;
            opacity: 0;
            transition: opacity 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--slate-100);
            font-size: 1.2rem;
            font-weight: 600;
        `;
        overlay.innerHTML = `
            <div style="text-align: center;">
                <div class="spinner-border text-primary mb-3" role="status"></div>
                <div>Loading...</div>
            </div>
        `;

        document.body.appendChild(overlay);
        
        // Fade in overlay
        requestAnimationFrame(() => {
            overlay.style.opacity = '1';
        });

        // Navigate after animation
        setTimeout(() => {
            window.location.href = url;
        }, 300);
    }

    setupHoverEffects() {
        // Enhanced hover effects for cards
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', (e) => {
                this.animations.addGlowEffect(e.target);
            });
            
            card.addEventListener('mouseleave', (e) => {
                this.animations.removeGlowEffect(e.target);
            });
        });

        // Magnetic buttons
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('mousemove', (e) => {
                this.animations.magneticEffect(e);
            });
            
            button.addEventListener('mouseleave', (e) => {
                this.animations.resetMagnetic(e.target);
            });
        });
    }

    setupLoadingAnimations() {
        // Add shimmer effect to loading elements
        document.querySelectorAll('[data-loading="true"]').forEach(element => {
            element.classList.add('shimmer');
        });
    }

    initializeParticles() {
        const canvas = document.createElement('canvas');
        canvas.className = 'particle-bg';
        document.body.appendChild(canvas);
        
        this.particles.init(canvas);
    }

    setupKeyboardShortcuts() {
        // Global shortcuts
        this.shortcuts.add('cmd+k', () => this.ui.openCommandPalette());
        this.shortcuts.add('/', () => this.ui.focusSearch());
        this.shortcuts.add('?', () => this.ui.showKeyboardShortcuts());
        this.shortcuts.add('esc', () => this.ui.closeModals());
        
        // Navigation shortcuts
        this.shortcuts.add('g d', () => window.location.href = '/');
        this.shortcuts.add('g s', () => window.location.href = '/scan');
        this.shortcuts.add('g r', () => window.location.href = '/reports');
        this.shortcuts.add('g p', () => window.location.href = '/privacy');
    }

    initializeUI() {
        // Initialize modern UI components
        this.ui.initializeTooltips();
        this.ui.initializeModals();
        this.ui.initializeCharts();
        this.ui.initializeRealTimeUpdates();
        
        // Add modern loading states
        this.ui.setupLoadingStates();
        
        // Initialize notification system
        this.notifications.init();
    }

    startPerformanceMonitoring() {
        this.performance.startMonitoring();
        
        // Show performance metrics in development
        if (window.location.hostname === 'localhost') {
            this.performance.showMetrics();
        }
    }
}

class ModernAnimationSystem {
    addGlowEffect(element) {
        element.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        element.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 0 30px rgba(59, 130, 246, 0.3)';
    }

    removeGlowEffect(element) {
        element.style.boxShadow = '';
    }

    magneticEffect(e) {
        const button = e.currentTarget;
        const rect = button.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        const strength = 0.3;
        button.style.transform = `translate(${x * strength}px, ${y * strength}px) scale(1.05)`;
    }

    resetMagnetic(element) {
        element.style.transform = '';
    }

    typeWriter(element, text, speed = 50) {
        element.innerHTML = '';
        let i = 0;
        
        const timer = setInterval(() => {
            if (i < text.length) {
                element.innerHTML += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    }

    countUp(element, start, end, duration = 2000) {
        const startTime = performance.now();
        const startValue = parseInt(start);
        const endValue = parseInt(end);
        const difference = endValue - startValue;

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutCubic = 1 - Math.pow(1 - progress, 3);
            const currentValue = Math.floor(startValue + (difference * easeOutCubic));
            
            element.textContent = currentValue.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    }
}

class ModernUIManager {
    constructor() {
        this.modals = [];
        this.tooltips = [];
    }

    initializeTooltips() {
        // Initialize modern tooltips
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            const tooltip = this.createTooltip(element.dataset.tooltip);
            this.tooltips.push({ element, tooltip });
            
            element.addEventListener('mouseenter', () => this.showTooltip(tooltip, element));
            element.addEventListener('mouseleave', () => this.hideTooltip(tooltip));
        });
    }

    createTooltip(text) {
        const tooltip = document.createElement('div');
        tooltip.className = 'modern-tooltip';
        tooltip.textContent = text;
        tooltip.style.cssText = `
            position: absolute;
            background: rgba(15, 23, 42, 0.95);
            color: var(--slate-100);
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.875rem;
            font-weight: 500;
            z-index: 1000;
            opacity: 0;
            transform: translateY(8px);
            transition: all 0.2s ease;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.1);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
            pointer-events: none;
        `;
        document.body.appendChild(tooltip);
        return tooltip;
    }

    showTooltip(tooltip, element) {
        const rect = element.getBoundingClientRect();
        tooltip.style.left = `${rect.left + rect.width / 2}px`;
        tooltip.style.top = `${rect.top - 40}px`;
        
        requestAnimationFrame(() => {
            tooltip.style.opacity = '1';
            tooltip.style.transform = 'translateY(0)';
        });
    }

    hideTooltip(tooltip) {
        tooltip.style.opacity = '0';
        tooltip.style.transform = 'translateY(8px)';
    }

    initializeModals() {
        // Enhanced modal system
        document.querySelectorAll('[data-modal]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                this.openModal(trigger.dataset.modal);
            });
        });
    }

    openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;

        modal.style.display = 'flex';
        modal.style.opacity = '0';
        modal.style.transform = 'scale(0.9)';
        
        requestAnimationFrame(() => {
            modal.style.opacity = '1';
            modal.style.transform = 'scale(1)';
        });
    }

    closeModals() {
        document.querySelectorAll('.modal.show').forEach(modal => {
            modal.style.opacity = '0';
            modal.style.transform = 'scale(0.9)';
            
            setTimeout(() => {
                modal.style.display = 'none';
            }, 200);
        });
    }

    openCommandPalette() {
        // Create command palette if it doesn't exist
        let palette = document.getElementById('command-palette');
        if (!palette) {
            palette = this.createCommandPalette();
        }
        
        palette.style.display = 'flex';
        palette.style.opacity = '0';
        palette.style.transform = 'translateY(-20px)';
        
        requestAnimationFrame(() => {
            palette.style.opacity = '1';
            palette.style.transform = 'translateY(0)';
            palette.querySelector('input').focus();
        });
    }

    createCommandPalette() {
        const palette = document.createElement('div');
        palette.id = 'command-palette';
        palette.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            z-index: 9999;
            display: none;
            align-items: flex-start;
            justify-content: center;
            padding-top: 100px;
            transition: all 0.2s ease;
        `;
        
        palette.innerHTML = `
            <div style="
                background: rgba(30, 41, 59, 0.95);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
                width: 90%;
                max-width: 600px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(20px);
            ">
                <input type="text" placeholder="Search or type a command..." style="
                    width: 100%;
                    background: transparent;
                    border: none;
                    padding: 20px;
                    color: var(--slate-100);
                    font-size: 1.1rem;
                    outline: none;
                " />
                <div class="command-results" style="
                    max-height: 300px;
                    overflow-y: auto;
                    border-top: 1px solid rgba(148, 163, 184, 0.1);
                ">
                    <div style="padding: 16px; color: var(--slate-400); text-align: center;">
                        Type to search for pages, commands, or actions...
                    </div>
                </div>
            </div>
        `;
        
        // Close on escape or outside click
        palette.addEventListener('click', (e) => {
            if (e.target === palette) {
                this.closeCommandPalette(palette);
            }
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && palette.style.display === 'flex') {
                this.closeCommandPalette(palette);
            }
        });
        
        document.body.appendChild(palette);
        return palette;
    }

    closeCommandPalette(palette) {
        palette.style.opacity = '0';
        palette.style.transform = 'translateY(-20px)';
        
        setTimeout(() => {
            palette.style.display = 'none';
        }, 200);
    }

    focusSearch() {
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="search"], input[placeholder*="Search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }

    showKeyboardShortcuts() {
        const shortcuts = [
            { key: 'Cmd+K', description: 'Open command palette' },
            { key: '/', description: 'Focus search' },
            { key: '?', description: 'Show keyboard shortcuts' },
            { key: 'Esc', description: 'Close modals' },
            { key: 'G → D', description: 'Go to Dashboard' },
            { key: 'G → S', description: 'Go to Scan' },
            { key: 'G → R', description: 'Go to Reports' },
        ];

        const modal = this.createShortcutsModal(shortcuts);
        document.body.appendChild(modal);
        this.openModal(modal.id);
    }

    createShortcutsModal(shortcuts) {
        const modal = document.createElement('div');
        modal.id = 'shortcuts-modal';
        modal.className = 'modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            z-index: 9999;
            display: none;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
        `;

        const shortcutsList = shortcuts.map(shortcut => `
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 0;
                border-bottom: 1px solid rgba(148, 163, 184, 0.1);
            ">
                <span style="color: var(--slate-300);">${shortcut.description}</span>
                <kbd style="
                    background: rgba(148, 163, 184, 0.1);
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 0.75rem;
                    color: var(--slate-400);
                    font-family: var(--font-mono);
                ">${shortcut.key}</kbd>
            </div>
        `).join('');

        modal.innerHTML = `
            <div style="
                background: rgba(30, 41, 59, 0.95);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 12px;
                width: 90%;
                max-width: 500px;
                padding: 24px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(20px);
            ">
                <h3 style="color: var(--slate-100); margin-bottom: 20px; text-align: center;">
                    Keyboard Shortcuts
                </h3>
                <div>
                    ${shortcutsList}
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <button onclick="this.closest('.modal').style.display='none'" style="
                        background: var(--gradient-primary);
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 6px;
                        cursor: pointer;
                        font-weight: 600;
                    ">Close</button>
                </div>
            </div>
        `;

        return modal;
    }

    initializeCharts() {
        // Initialize modern chart visualizations
        const chartElements = document.querySelectorAll('[data-chart]');
        chartElements.forEach(element => {
            this.createModernChart(element);
        });
    }

    createModernChart(element) {
        // Create animated chart placeholder
        element.innerHTML = `
            <div style="
                height: 200px;
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: var(--slate-400);
                position: relative;
                overflow: hidden;
            ">
                <div>Chart visualization will be loaded here</div>
                <div style="
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                    animation: shimmer 2s infinite;
                "></div>
            </div>
        `;
    }

    initializeRealTimeUpdates() {
        // Simulate real-time updates
        setInterval(() => {
            this.updateTimestamp();
            this.updateMetrics();
        }, 1000);
    }

    updateTimestamp() {
        const timeElements = document.querySelectorAll('[data-current-time]');
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        
        timeElements.forEach(element => {
            element.textContent = `Current time: ${timeString}`;
        });
    }

    updateMetrics() {
        // Simulate metric updates
        const metricElements = document.querySelectorAll('[data-metric]');
        metricElements.forEach(element => {
            const baseValue = parseInt(element.textContent) || 0;
            const variation = Math.floor(Math.random() * 10) - 5;
            const newValue = Math.max(0, baseValue + variation);
            
            if (newValue !== baseValue) {
                element.style.color = variation > 0 ? 'var(--green-400)' : 'var(--red-400)';
                setTimeout(() => {
                    element.style.color = '';
                }, 1000);
            }
        });
    }

    setupLoadingStates() {
        // Add loading states to buttons
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', () => {
                if (button.type === 'submit' || button.dataset.loading === 'true') {
                    this.showButtonLoading(button);
                }
            });
        });
    }

    showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status"></span>
            Loading...
        `;
        button.disabled = true;

        // Reset after 2 seconds (adjust based on actual loading time)
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 2000);
    }
}

class ParticleSystem {
    init(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: 0, y: 0 };
        
        this.resize();
        this.createParticles();
        this.setupEventListeners();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const particleCount = Math.min(100, Math.floor((this.canvas.width * this.canvas.height) / 10000));
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                size: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.2,
                color: this.getRandomColor(),
            });
        }
    }

    getRandomColor() {
        const colors = ['59, 130, 246', '139, 92, 246', '6, 182, 212', '16, 185, 129'];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    setupEventListeners() {
        window.addEventListener('resize', () => this.resize());
        
        document.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
        });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        this.particles.forEach(particle => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;

            // Bounce off edges
            if (particle.x <= 0 || particle.x >= this.canvas.width) particle.vx *= -1;
            if (particle.y <= 0 || particle.y >= this.canvas.height) particle.vy *= -1;

            // Mouse interaction
            const dx = this.mouse.x - particle.x;
            const dy = this.mouse.y - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 100) {
                const force = (100 - distance) / 100;
                particle.x -= dx * force * 0.01;
                particle.y -= dy * force * 0.01;
            }

            // Draw particle
            this.ctx.save();
            this.ctx.globalAlpha = particle.opacity;
            this.ctx.fillStyle = `rgba(${particle.color}, ${particle.opacity})`;
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.restore();

            // Draw connections
            this.particles.forEach(otherParticle => {
                const dx = particle.x - otherParticle.x;
                const dy = particle.y - otherParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < 100) {
                    this.ctx.save();
                    this.ctx.globalAlpha = (100 - distance) / 100 * 0.1;
                    this.ctx.strokeStyle = `rgba(${particle.color}, 0.3)`;
                    this.ctx.lineWidth = 1;
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(otherParticle.x, otherParticle.y);
                    this.ctx.stroke();
                    this.ctx.restore();
                }
            });
        });

        requestAnimationFrame(() => this.animate());
    }
}

class KeyboardShortcuts {
    constructor() {
        this.shortcuts = new Map();
        this.setupEventListener();
    }

    add(combination, callback) {
        this.shortcuts.set(combination.toLowerCase(), callback);
    }

    setupEventListener() {
        let sequence = '';
        let sequenceTimer = null;

        document.addEventListener('keydown', (e) => {
            // Handle single key shortcuts
            const modifiers = [];
            if (e.ctrlKey || e.metaKey) modifiers.push('cmd');
            if (e.shiftKey) modifiers.push('shift');
            if (e.altKey) modifiers.push('alt');

            const key = e.key.toLowerCase();
            const combination = [...modifiers, key].join('+');

            // Check for single key combination
            if (this.shortcuts.has(combination)) {
                e.preventDefault();
                this.shortcuts.get(combination)();
                return;
            }

            // Handle sequence shortcuts (like 'g d')
            if (!e.ctrlKey && !e.metaKey && !e.altKey && e.key.length === 1) {
                sequence += e.key.toLowerCase();
                
                if (sequenceTimer) clearTimeout(sequenceTimer);
                sequenceTimer = setTimeout(() => {
                    sequence = '';
                }, 1000);

                // Check for sequence match
                const sequenceWithSpaces = sequence.split('').join(' ');
                if (this.shortcuts.has(sequenceWithSpaces)) {
                    e.preventDefault();
                    this.shortcuts.get(sequenceWithSpaces)();
                    sequence = '';
                    clearTimeout(sequenceTimer);
                }
            } else {
                sequence = '';
                if (sequenceTimer) clearTimeout(sequenceTimer);
            }
        });
    }
}

class NotificationSystem {
    init() {
        this.container = this.createContainer();
    }

    createContainer() {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            display: flex;
            flex-direction: column;
            gap: 12px;
            pointer-events: none;
        `;
        document.body.appendChild(container);
        return container;
    }

    show(message, type = 'info', duration = 4000) {
        const notification = this.createNotification(message, type);
        this.container.appendChild(notification);

        // Animate in
        requestAnimationFrame(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        });

        // Auto remove
        setTimeout(() => {
            this.remove(notification);
        }, duration);

        return notification;
    }

    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const colors = {
            success: '16, 185, 129',
            error: '239, 68, 68',
            warning: '245, 158, 11',
            info: '59, 130, 246'
        };

        const color = colors[type] || colors.info;

        notification.style.cssText = `
            background: rgba(30, 41, 59, 0.95);
            border: 1px solid rgba(${color}, 0.3);
            border-left: 4px solid rgb(${color});
            border-radius: 8px;
            padding: 16px 20px;
            min-width: 300px;
            max-width: 400px;
            color: var(--slate-100);
            font-weight: 500;
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            pointer-events: auto;
            cursor: pointer;
        `;

        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="
                    width: 8px;
                    height: 8px;
                    border-radius: 50%;
                    background: rgb(${color});
                    box-shadow: 0 0 8px rgba(${color}, 0.5);
                "></div>
                <div>${message}</div>
            </div>
        `;

        notification.addEventListener('click', () => {
            this.remove(notification);
        });

        return notification;
    }

    remove(notification) {
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
}

class PerformanceMonitor {
    constructor() {
        this.metrics = {
            fps: 0,
            memory: 0,
            loadTime: 0
        };
    }

    startMonitoring() {
        this.measureLoadTime();
        this.startFPSMonitoring();
        this.startMemoryMonitoring();
    }

    measureLoadTime() {
        const loadTime = performance.now();
        this.metrics.loadTime = Math.round(loadTime);
        console.log(`Page load time: ${this.metrics.loadTime}ms`);
    }

    startFPSMonitoring() {
        let lastTime = performance.now();
        let frames = 0;

        const measureFPS = () => {
            const currentTime = performance.now();
            frames++;

            if (currentTime - lastTime >= 1000) {
                this.metrics.fps = frames;
                frames = 0;
                lastTime = currentTime;
            }

            requestAnimationFrame(measureFPS);
        };

        requestAnimationFrame(measureFPS);
    }

    startMemoryMonitoring() {
        if (performance.memory) {
            setInterval(() => {
                this.metrics.memory = Math.round(performance.memory.usedJSHeapSize / 1048576);
            }, 1000);
        }
    }

    showMetrics() {
        const metricsDisplay = document.createElement('div');
        metricsDisplay.id = 'performance-metrics';
        metricsDisplay.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            background: rgba(15, 23, 42, 0.95);
            color: var(--slate-100);
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid rgba(148, 163, 184, 0.2);
            font-family: var(--font-mono);
            font-size: 0.75rem;
            z-index: 9999;
            backdrop-filter: blur(20px);
        `;

        document.body.appendChild(metricsDisplay);

        setInterval(() => {
            metricsDisplay.innerHTML = `
                FPS: ${this.metrics.fps}<br>
                Memory: ${this.metrics.memory}MB<br>
                Load: ${this.metrics.loadTime}ms
            `;
        }, 500);
    }
}

// Initialize the modern platform when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.modernPlatform = new ModernIntelligencePlatform();
    
    // Enhanced error handling
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
        if (window.modernPlatform && window.modernPlatform.notifications) {
            window.modernPlatform.notifications.show(
                'An unexpected error occurred. Please refresh the page.', 
                'error'
            );
        }
    });
    
    window.addEventListener('unhandledrejection', (event) => {
        console.error('Unhandled promise rejection:', event.reason);
        if (window.modernPlatform && window.modernPlatform.notifications) {
            window.modernPlatform.notifications.show(
                'A network error occurred. Please check your connection.', 
                'error'
            );
        }
    });
});

// Global utility functions
window.refreshDashboard = async function() {
    if (window.modernPlatform) {
        window.modernPlatform.notifications.show('Refreshing dashboard...', 'info', 2000);
        // Simulate refresh
        setTimeout(() => {
            window.location.reload();
        }, 1000);
    }
};

window.startQuickScan = function() {
    if (window.modernPlatform) {
        window.modernPlatform.notifications.show('Starting quick scan...', 'info');
        window.location.href = '/scan';
    }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ModernIntelligencePlatform;
}