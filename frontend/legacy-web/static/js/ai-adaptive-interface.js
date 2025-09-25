/**
 * AI-Adaptive Interface System
 * Advanced machine learning-powered UI that adapts to user behavior
 * Inspired by modern platforms like GitHub Copilot, Linear, and Discord
 */

class AIAdaptiveInterface {
    constructor() {
        this.userBehaviorData = {
            interactions: [],
            preferences: {},
            patterns: {},
            skills: {},
            contexts: []
        };
        
        this.adaptiveElements = new Map();
        this.personalityProfile = {
            expertiseLevel: 'intermediate',
            preferredWorkflow: 'standard',
            interactionStyle: 'balanced',
            uiComplexity: 'moderate'
        };
        
        this.machineLearningModel = {
            predictions: new Map(),
            confidenceScores: new Map(),
            learningRate: 0.1,
            trainingData: []
        };
        
        this.contextualSuggestions = [];
        this.adaptiveAnimations = new Map();
        this.intelligentShortcuts = new Map();
        
        this.init();
    }

    init() {
        this.loadUserProfile();
        this.setupBehaviorTracking();
        this.initializeAdaptiveElements();
        this.startContextualAnalysis();
        this.setupIntelligentRecommendations();
        this.initializePersonalizationEngine();
    }

    loadUserProfile() {
        // Load existing user profile from localStorage or API
        const savedProfile = localStorage.getItem('ai_adaptive_profile');
        if (savedProfile) {
            try {
                const profile = JSON.parse(savedProfile);
                this.userBehaviorData = { ...this.userBehaviorData, ...profile.behaviorData };
                this.personalityProfile = { ...this.personalityProfile, ...profile.personality };
                console.log('AI Adaptive Profile loaded:', this.personalityProfile);
            } catch (e) {
                console.warn('Could not load AI profile, starting fresh');
            }
        }
        
        this.analyzeInitialContext();
    }

    setupBehaviorTracking() {
        // Track mouse movements for interaction patterns
        document.addEventListener('mousemove', this.debounce((e) => {
            this.recordInteraction('mouse_movement', {
                x: e.clientX,
                y: e.clientY,
                timestamp: Date.now(),
                element: e.target.tagName,
                context: this.getCurrentContext()
            });
        }, 100));

        // Track clicks and their context
        document.addEventListener('click', (e) => {
            this.recordInteraction('click', {
                element: e.target,
                className: e.target.className,
                id: e.target.id,
                position: { x: e.clientX, y: e.clientY },
                timestamp: Date.now(),
                context: this.getCurrentContext(),
                modifiers: {
                    ctrl: e.ctrlKey,
                    alt: e.altKey,
                    shift: e.shiftKey,
                    meta: e.metaKey
                }
            });
            
            this.updateUserPreferences(e.target);
            this.analyzeClickPattern(e);
        });

        // Track keyboard usage patterns
        document.addEventListener('keydown', (e) => {
            this.recordInteraction('keypress', {
                key: e.key,
                code: e.code,
                timestamp: Date.now(),
                context: this.getCurrentContext(),
                modifiers: {
                    ctrl: e.ctrlKey,
                    alt: e.altKey,
                    shift: e.shiftKey,
                    meta: e.metaKey
                }
            });
            
            this.analyzeKeyboardShortcuts(e);
        });

        // Track form interactions
        document.addEventListener('input', this.debounce((e) => {
            if (e.target.matches('input, textarea, select')) {
                this.recordInteraction('form_input', {
                    type: e.target.type,
                    name: e.target.name,
                    valueLength: e.target.value.length,
                    timestamp: Date.now(),
                    context: this.getCurrentContext()
                });
                
                this.analyzeFormBehavior(e.target);
            }
        }, 200));

        // Track scroll behavior
        window.addEventListener('scroll', this.debounce(() => {
            this.recordInteraction('scroll', {
                scrollY: window.scrollY,
                scrollX: window.scrollX,
                timestamp: Date.now(),
                context: this.getCurrentContext()
            });
        }, 150));

        // Track time spent on elements
        this.setupElementFocusTracking();
    }

    recordInteraction(type, data) {
        const interaction = {
            type,
            data,
            timestamp: Date.now(),
            sessionId: this.getSessionId()
        };
        
        this.userBehaviorData.interactions.push(interaction);
        
        // Keep only last 1000 interactions to prevent memory issues
        if (this.userBehaviorData.interactions.length > 1000) {
            this.userBehaviorData.interactions = this.userBehaviorData.interactions.slice(-1000);
        }
        
        // Trigger real-time analysis
        this.analyzeRecentBehavior();
    }

    analyzeRecentBehavior() {
        const recentInteractions = this.userBehaviorData.interactions.slice(-10);
        
        // Detect patterns in recent behavior
        this.detectInteractionPatterns(recentInteractions);
        this.updateSkillAssessment(recentInteractions);
        this.generateContextualSuggestions(recentInteractions);
        this.adaptUIBasedOnBehavior(recentInteractions);
    }

    detectInteractionPatterns(interactions) {
        // Analyze clicking patterns
        const clicks = interactions.filter(i => i.type === 'click');
        if (clicks.length >= 3) {
            const clickSpeed = this.calculateInteractionSpeed(clicks);
            const clickPrecision = this.calculateClickPrecision(clicks);
            
            if (clickSpeed > 0.5 && clickPrecision > 0.8) {
                this.updatePersonalityTrait('interactionStyle', 'efficient');
                this.suggestKeyboardShortcuts();
            } else if (clickSpeed < 0.2) {
                this.updatePersonalityTrait('interactionStyle', 'deliberate');
                this.enableAdvancedTooltips();
            }
        }

        // Analyze keyboard usage
        const keypresses = interactions.filter(i => i.type === 'keypress');
        const shortcutUsage = keypresses.filter(k => k.data.modifiers.ctrl || k.data.modifiers.meta);
        
        if (shortcutUsage.length / Math.max(keypresses.length, 1) > 0.3) {
            this.updatePersonalityTrait('expertiseLevel', 'advanced');
            this.enablePowerUserFeatures();
        }
    }

    updateSkillAssessment(interactions) {
        const contexts = interactions.map(i => i.data.context).filter(c => c);
        
        contexts.forEach(context => {
            if (!this.userBehaviorData.skills[context]) {
                this.userBehaviorData.skills[context] = {
                    level: 0,
                    interactions: 0,
                    efficiency: 0,
                    lastUpdated: Date.now()
                };
            }
            
            const skill = this.userBehaviorData.skills[context];
            skill.interactions++;
            
            // Calculate efficiency based on interaction patterns
            const contextInteractions = interactions.filter(i => i.data.context === context);
            if (contextInteractions.length > 1) {
                const timeSpent = contextInteractions[contextInteractions.length - 1].timestamp - contextInteractions[0].timestamp;
                const actionsPerSecond = contextInteractions.length / (timeSpent / 1000);
                skill.efficiency = (skill.efficiency + actionsPerSecond) / 2;
            }
            
            // Update skill level
            if (skill.interactions > 10 && skill.efficiency > 0.5) {
                skill.level = Math.min(skill.level + 0.1, 1.0);
            }
            
            skill.lastUpdated = Date.now();
        });
    }

    generateContextualSuggestions(interactions) {
        const currentContext = this.getCurrentContext();
        const contextInteractions = interactions.filter(i => i.data.context === currentContext);
        
        if (contextInteractions.length < 3) return;

        // Analyze common patterns in current context
        const commonElements = this.findCommonElements(contextInteractions);
        const suggestionScore = this.calculateSuggestionRelevance(commonElements, currentContext);
        
        if (suggestionScore > 0.7) {
            const suggestion = this.createContextualSuggestion(commonElements, currentContext);
            this.showIntelligentSuggestion(suggestion);
        }
    }

    adaptUIBasedOnBehavior(interactions) {
        // Adapt animation speeds based on user preference
        const clickSpeed = this.calculateAverageClickSpeed(interactions);
        if (clickSpeed > 0.8) {
            this.setAnimationSpeed('fast');
        } else if (clickSpeed < 0.3) {
            this.setAnimationSpeed('slow');
        }

        // Adapt UI complexity based on expertise
        if (this.personalityProfile.expertiseLevel === 'advanced') {
            this.enableAdvancedUI();
        } else if (this.personalityProfile.expertiseLevel === 'beginner') {
            this.simplifyUI();
        }

        // Adapt color scheme based on time of day and usage patterns
        this.adaptColorScheme();
    }

    initializeAdaptiveElements() {
        // Find all elements that can be adapted
        const adaptableElements = document.querySelectorAll('[data-adaptive]');
        
        adaptableElements.forEach(element => {
            const adaptiveType = element.dataset.adaptive;
            this.adaptiveElements.set(element, {
                type: adaptiveType,
                originalState: this.captureElementState(element),
                adaptations: [],
                learningData: {
                    interactions: 0,
                    effectiveAdaptations: 0,
                    userSatisfaction: 0.5
                }
            });
            
            this.setupElementAdaptation(element, adaptiveType);
        });
    }

    setupElementAdaptation(element, type) {
        switch (type) {
            case 'button':
                this.adaptButton(element);
                break;
            case 'form':
                this.adaptForm(element);
                break;
            case 'navigation':
                this.adaptNavigation(element);
                break;
            case 'content':
                this.adaptContent(element);
                break;
            default:
                this.adaptGenericElement(element);
        }
    }

    adaptButton(button) {
        const adaptiveData = this.adaptiveElements.get(button);
        
        // Track button usage patterns
        button.addEventListener('click', () => {
            adaptiveData.learningData.interactions++;
            
            // Adapt button appearance based on usage frequency
            if (adaptiveData.learningData.interactions > 5) {
                this.enhanceButtonVisibility(button);
            }
            
            // Adapt button position based on click patterns
            this.optimizeButtonPosition(button);
        });

        // Add hover analytics
        button.addEventListener('mouseenter', () => {
            this.recordButtonHover(button);
        });
    }

    adaptForm(form) {
        const adaptiveData = this.adaptiveElements.get(form);
        
        // Analyze form completion patterns
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                this.analyzeFormFieldUsage(input);
            });
            
            input.addEventListener('blur', () => {
                this.optimizeFormField(input);
            });
        });

        // Intelligent form suggestions
        form.addEventListener('submit', () => {
            this.learnFromFormSubmission(form);
        });
    }

    adaptNavigation(nav) {
        const adaptiveData = this.adaptiveElements.get(nav);
        
        // Track navigation patterns
        const navItems = nav.querySelectorAll('a, button');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                this.recordNavigationChoice(item);
                this.reorderNavigationItems(nav);
            });
        });
    }

    startContextualAnalysis() {
        // Continuously analyze the current context
        setInterval(() => {
            const context = this.analyzeCurrentContext();
            this.updateContextualRecommendations(context);
            this.triggerContextualAnimations(context);
        }, 2000);
    }

    analyzeCurrentContext() {
        const currentUrl = window.location.pathname;
        const visibleElements = this.getVisibleElements();
        const userActions = this.getRecentUserActions();
        const timeOfDay = new Date().getHours();
        
        return {
            page: currentUrl,
            elements: visibleElements,
            actions: userActions,
            timeOfDay: timeOfDay,
            sessionDuration: Date.now() - this.getSessionStartTime(),
            userIntent: this.predictUserIntent(userActions)
        };
    }

    predictUserIntent(actions) {
        if (!actions.length) return 'browsing';
        
        const recentActions = actions.slice(-5);
        const actionTypes = recentActions.map(a => a.type);
        
        // Pattern recognition for common intents
        if (actionTypes.includes('form_input') && actionTypes.includes('click')) {
            return 'form_completion';
        } else if (actionTypes.filter(t => t === 'click').length >= 3) {
            return 'navigation';
        } else if (actionTypes.includes('keypress')) {
            return 'data_entry';
        } else if (actionTypes.includes('scroll')) {
            return 'content_consumption';
        }
        
        return 'exploration';
    }

    updateContextualRecommendations(context) {
        const recommendations = this.generateRecommendations(context);
        
        recommendations.forEach(rec => {
            if (rec.confidence > 0.8) {
                this.displayRecommendation(rec);
            }
        });
    }

    generateRecommendations(context) {
        const recommendations = [];
        
        // Intent-based recommendations
        switch (context.userIntent) {
            case 'form_completion':
                recommendations.push({
                    type: 'form_assistance',
                    message: 'Would you like me to auto-fill common fields?',
                    action: () => this.enableAutoFill(),
                    confidence: 0.9
                });
                break;
                
            case 'navigation':
                const frequentPages = this.getFrequentlyVisitedPages();
                if (frequentPages.length > 0) {
                    recommendations.push({
                        type: 'quick_navigation',
                        message: 'Quick access to your frequent pages',
                        action: () => this.showQuickNavigation(frequentPages),
                        confidence: 0.85
                    });
                }
                break;
                
            case 'data_entry':
                recommendations.push({
                    type: 'keyboard_shortcuts',
                    message: 'Keyboard shortcuts available for faster input',
                    action: () => this.showKeyboardShortcuts(),
                    confidence: 0.8
                });
                break;
        }
        
        // Time-based recommendations
        if (context.timeOfDay >= 18 || context.timeOfDay <= 6) {
            recommendations.push({
                type: 'dark_mode',
                message: 'Switch to dark mode for better nighttime viewing?',
                action: () => this.enableDarkMode(),
                confidence: 0.7
            });
        }
        
        return recommendations;
    }

    setupIntelligentRecommendations() {
        // Create recommendation system
        this.recommendationEngine = {
            queue: [],
            displayedRecommendations: new Set(),
            userFeedback: new Map()
        };
        
        // Show recommendations with intelligent timing
        setInterval(() => {
            this.processRecommendationQueue();
        }, 5000);
    }

    displayRecommendation(recommendation) {
        if (this.recommendationEngine.displayedRecommendations.has(recommendation.type)) {
            return; // Don't show the same recommendation twice
        }
        
        const recommendationElement = this.createRecommendationElement(recommendation);
        document.body.appendChild(recommendationElement);
        
        this.recommendationEngine.displayedRecommendations.add(recommendation.type);
        
        // Auto-remove after 10 seconds if no interaction
        setTimeout(() => {
            if (recommendationElement.parentNode) {
                recommendationElement.remove();
            }
        }, 10000);
    }

    createRecommendationElement(recommendation) {
        const element = document.createElement('div');
        element.className = 'ai-recommendation';
        element.innerHTML = `
            <div class="ai-recommendation-content">
                <div class="ai-recommendation-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                </div>
                <div class="ai-recommendation-text">
                    <div class="ai-recommendation-title">AI Suggestion</div>
                    <div class="ai-recommendation-message">${recommendation.message}</div>
                </div>
                <div class="ai-recommendation-actions">
                    <button class="ai-rec-accept" data-action="accept">Accept</button>
                    <button class="ai-rec-dismiss" data-action="dismiss">Dismiss</button>
                </div>
            </div>
        `;
        
        // Add event listeners
        element.querySelector('.ai-rec-accept').addEventListener('click', () => {
            recommendation.action();
            this.recordRecommendationFeedback(recommendation, 'accepted');
            element.remove();
        });
        
        element.querySelector('.ai-rec-dismiss').addEventListener('click', () => {
            this.recordRecommendationFeedback(recommendation, 'dismissed');
            element.remove();
        });
        
        return element;
    }

    recordRecommendationFeedback(recommendation, feedback) {
        if (!this.recommendationEngine.userFeedback.has(recommendation.type)) {
            this.recommendationEngine.userFeedback.set(recommendation.type, {
                accepted: 0,
                dismissed: 0,
                effectiveness: 0.5
            });
        }
        
        const feedbackData = this.recommendationEngine.userFeedback.get(recommendation.type);
        feedbackData[feedback]++;
        
        // Update effectiveness score
        feedbackData.effectiveness = feedbackData.accepted / (feedbackData.accepted + feedbackData.dismissed);
        
        // Learn from feedback
        this.updateRecommendationModel(recommendation, feedback);
    }

    initializePersonalizationEngine() {
        // Load personalization settings
        this.personalizationSettings = {
            preferredAnimationSpeed: 'medium',
            preferredColorScheme: 'auto',
            uiDensity: 'comfortable',
            assistanceLevel: 'balanced',
            privacyLevel: 'standard'
        };
        
        this.applyPersonalization();
    }

    applyPersonalization() {
        // Apply animation speed preference
        document.documentElement.style.setProperty(
            '--ai-animation-speed', 
            this.getAnimationSpeedValue(this.personalizationSettings.preferredAnimationSpeed)
        );
        
        // Apply color scheme
        if (this.personalizationSettings.preferredColorScheme === 'dark') {
            document.documentElement.classList.add('ai-dark-mode');
        }
        
        // Apply UI density
        document.documentElement.classList.add(`ai-density-${this.personalizationSettings.uiDensity}`);
    }

    // Machine Learning Helper Methods
    trainModel(inputData, expectedOutput) {
        this.machineLearningModel.trainingData.push({
            input: inputData,
            output: expectedOutput,
            timestamp: Date.now()
        });
        
        // Simple neural network simulation
        const prediction = this.makePrediction(inputData);
        const error = this.calculateError(prediction, expectedOutput);
        
        // Update model weights (simplified)
        this.updateModelWeights(error);
    }

    makePrediction(inputData) {
        // Simplified prediction based on patterns
        const key = JSON.stringify(inputData);
        return this.machineLearningModel.predictions.get(key) || 0.5;
    }

    // Utility Methods
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

    getCurrentContext() {
        const activeElement = document.activeElement;
        const scrollPosition = window.scrollY;
        const viewportHeight = window.innerHeight;
        
        return {
            page: window.location.pathname,
            section: this.getCurrentSection(scrollPosition, viewportHeight),
            activeElement: activeElement ? activeElement.tagName : null,
            timestamp: Date.now()
        };
    }

    getCurrentSection(scrollY, viewportHeight) {
        // Determine which section of the page is currently visible
        const sections = document.querySelectorAll('section, .section, main, article');
        
        for (let section of sections) {
            const rect = section.getBoundingClientRect();
            if (rect.top <= viewportHeight / 2 && rect.bottom >= viewportHeight / 2) {
                return section.id || section.className || 'unnamed-section';
            }
        }
        
        return 'unknown-section';
    }

    getSessionId() {
        if (!this.sessionId) {
            this.sessionId = 'ai_session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        }
        return this.sessionId;
    }

    getSessionStartTime() {
        if (!this.sessionStartTime) {
            this.sessionStartTime = Date.now();
        }
        return this.sessionStartTime;
    }

    saveProfile() {
        const profile = {
            behaviorData: this.userBehaviorData,
            personality: this.personalityProfile,
            personalization: this.personalizationSettings,
            timestamp: Date.now()
        };
        
        try {
            localStorage.setItem('ai_adaptive_profile', JSON.stringify(profile));
        } catch (e) {
            console.warn('Could not save AI profile:', e);
        }
    }

    // Public API Methods
    getUserInsights() {
        return {
            expertiseLevel: this.personalityProfile.expertiseLevel,
            interactionStyle: this.personalityProfile.interactionStyle,
            skills: this.userBehaviorData.skills,
            preferences: this.userBehaviorData.preferences,
            totalInteractions: this.userBehaviorData.interactions.length
        };
    }

    adaptElement(element, adaptationType) {
        if (!this.adaptiveElements.has(element)) {
            this.adaptiveElements.set(element, {
                type: adaptationType,
                originalState: this.captureElementState(element),
                adaptations: [],
                learningData: {
                    interactions: 0,
                    effectiveAdaptations: 0,
                    userSatisfaction: 0.5
                }
            });
        }
        
        this.setupElementAdaptation(element, adaptationType);
    }

    setPersonalizationSetting(key, value) {
        this.personalizationSettings[key] = value;
        this.applyPersonalization();
        this.saveProfile();
    }

    getRecommendations() {
        const context = this.analyzeCurrentContext();
        return this.generateRecommendations(context);
    }

    // Clean up and save data before page unload
    destroy() {
        this.saveProfile();
        
        // Clean up event listeners and intervals
        if (this.contextAnalysisInterval) {
            clearInterval(this.contextAnalysisInterval);
        }
        
        if (this.recommendationInterval) {
            clearInterval(this.recommendationInterval);
        }
    }
}

// Auto-save profile periodically
setInterval(() => {
    if (window.aiInterface) {
        window.aiInterface.saveProfile();
    }
}, 30000); // Save every 30 seconds

// Save profile before page unload
window.addEventListener('beforeunload', () => {
    if (window.aiInterface) {
        window.aiInterface.destroy();
    }
});

// Initialize AI Interface when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.aiInterface = new AIAdaptiveInterface();
    console.log('AI Adaptive Interface initialized');
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIAdaptiveInterface;
}

// Global export for browser
if (typeof window !== 'undefined') {
    window.AIAdaptiveInterface = AIAdaptiveInterface;
}