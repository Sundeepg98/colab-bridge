/**
 * Enhanced Modern SaaS Platform JavaScript Framework
 * Provides interactive components, animations, and utilities
 */

class EnhancedUI {
    constructor() {
        this.init();
        this.setupGlobalEventListeners();
        this.initializeComponents();
    }

    init() {
        // Initialize theme
        this.theme = localStorage.getItem('theme') || 'light';
        this.setTheme(this.theme);

        // Initialize API base URL
        this.apiBase = '/api';

        // Component registry
        this.components = new Map();

        // Toast notification queue
        this.toastQueue = [];
        this.maxToasts = 5;

        // Global loading state
        this.loadingStates = new Set();

        // Mobile breakpoint
        this.mobileBreakpoint = 768;
    }

    setupGlobalEventListeners() {
        // Handle escape key for modals and dropdowns
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeAllModals();
                this.closeAllDropdowns();
            }
        });

        // Handle click outside for dropdowns
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dropdown')) {
                this.closeAllDropdowns();
            }
        });

        // Handle resize events
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 100);
        });

        // Handle form validation
        document.addEventListener('input', (e) => {
            if (e.target.hasAttribute('data-validate')) {
                this.validateField(e.target);
            }
        });

        // Auto-save drafts
        document.addEventListener('input', (e) => {
            if (e.target.hasAttribute('data-autosave')) {
                this.autoSave(e.target);
            }
        });
    }

    initializeComponents() {
        // Initialize all components on page load
        this.initTooltips();
        this.initDropdowns();
        this.initModals();
        this.initTabs();
        this.initAccordions();
        this.initProgressBars();
        this.initInfiniteScroll();
        this.initLazyLoading();
        this.initMobileNavigation();
        
        // Add skip links for accessibility
        this.addSkipLinks();
        
        // Initialize ARIA live regions
        this.initAriaLiveRegions();
    }

    // Theme Management
    setTheme(theme) {
        this.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        // Update theme toggle button if exists
        const themeToggle = document.querySelector('[data-theme-toggle]');
        if (themeToggle) {
            themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }

    toggleTheme() {
        const newTheme = this.theme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    // Toast Notifications
    showToast(message, type = 'info', duration = 5000, actions = []) {
        // Remove oldest toast if at max capacity
        if (this.toastQueue.length >= this.maxToasts) {
            const oldestToast = this.toastQueue.shift();
            oldestToast.remove();
        }

        const toast = this.createToast(message, type, duration, actions);
        this.toastQueue.push(toast);

        // Add to DOM
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        container.appendChild(toast);

        // Animate in
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => this.removeToast(toast), duration);
        }

        return toast;
    }

    createToast(message, type, duration, actions) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        const icons = {
            success: '✓',
            error: '✗',
            warning: '⚠',
            info: 'ℹ'
        };

        toast.innerHTML = `
            <div class="toast-icon">${icons[type] || icons.info}</div>
            <div class="toast-content">
                <div class="toast-message">${message}</div>
                ${actions.length > 0 ? `
                    <div class="toast-actions mt-2">
                        ${actions.map(action => `
                            <button class="btn btn-xs ${action.class || 'btn-ghost'}" 
                                    onclick="${action.handler}">
                                ${action.text}
                            </button>
                        `).join('')}
                    </div>
                ` : ''}
            </div>
            <button class="toast-close" onclick="enhancedUI.removeToast(this.closest('.toast'))">
                ×
            </button>
        `;

        return toast;
    }

    removeToast(toast) {
        toast.classList.remove('show');
        setTimeout(() => {
            toast.remove();
            const index = this.toastQueue.indexOf(toast);
            if (index > -1) {
                this.toastQueue.splice(index, 1);
            }
        }, 200);
    }

    // Modal Management
    initModals() {
        document.querySelectorAll('[data-modal-trigger]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const modalId = trigger.getAttribute('data-modal-trigger');
                this.openModal(modalId);
            });
        });

        document.querySelectorAll('[data-modal-close]').forEach(closeBtn => {
            closeBtn.addEventListener('click', () => {
                this.closeModal(closeBtn.closest('.modal-overlay'));
            });
        });
    }

    openModal(modalId) {
        const modal = document.querySelector(`#${modalId}`);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Focus first focusable element
            const focusable = modal.querySelector('input, button, select, textarea, [tabindex]');
            if (focusable) {
                setTimeout(() => focusable.focus(), 100);
            }

            // Trap focus within modal
            this.trapFocus(modal);
        }
    }

    closeModal(modal) {
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    closeAllModals() {
        document.querySelectorAll('.modal-overlay.active').forEach(modal => {
            this.closeModal(modal);
        });
    }

    trapFocus(element) {
        const focusableElements = element.querySelectorAll(
            'input, button, select, textarea, [href], [tabindex]:not([tabindex="-1"])'
        );
        const firstFocusable = focusableElements[0];
        const lastFocusable = focusableElements[focusableElements.length - 1];

        element.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstFocusable) {
                        lastFocusable.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === lastFocusable) {
                        firstFocusable.focus();
                        e.preventDefault();
                    }
                }
            }
        });
    }

    // Dropdown Management
    initDropdowns() {
        document.querySelectorAll('[data-dropdown-trigger]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                const dropdown = trigger.closest('.dropdown');
                this.toggleDropdown(dropdown);
            });
        });
    }

    toggleDropdown(dropdown) {
        const isActive = dropdown.classList.contains('active');
        this.closeAllDropdowns();
        
        if (!isActive) {
            dropdown.classList.add('active');
            this.positionDropdown(dropdown);
        }
    }

    closeAllDropdowns() {
        document.querySelectorAll('.dropdown.active').forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    }

    positionDropdown(dropdown) {
        const menu = dropdown.querySelector('.dropdown-menu');
        const rect = dropdown.getBoundingClientRect();
        const menuRect = menu.getBoundingClientRect();
        
        // Check if dropdown goes off-screen
        if (rect.bottom + menuRect.height > window.innerHeight) {
            menu.style.top = 'auto';
            menu.style.bottom = '100%';
        } else {
            menu.style.top = '100%';
            menu.style.bottom = 'auto';
        }
    }

    // Tooltip Management
    initTooltips() {
        document.querySelectorAll('[data-tooltip]').forEach(element => {
            const tooltip = this.createTooltip(element);
            element.appendChild(tooltip);

            element.addEventListener('mouseenter', () => {
                tooltip.style.opacity = '1';
                tooltip.style.visibility = 'visible';
            });

            element.addEventListener('mouseleave', () => {
                tooltip.style.opacity = '0';
                tooltip.style.visibility = 'hidden';
            });
        });
    }

    createTooltip(element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-content';
        tooltip.textContent = element.getAttribute('data-tooltip');
        return tooltip;
    }

    // Tab Management
    initTabs() {
        document.querySelectorAll('[data-tab-trigger]').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const tabId = trigger.getAttribute('data-tab-trigger');
                const tabGroup = trigger.closest('[data-tab-group]');
                this.switchTab(tabGroup, tabId);
            });
        });
    }

    switchTab(tabGroup, activeTabId) {
        // Update triggers
        tabGroup.querySelectorAll('[data-tab-trigger]').forEach(trigger => {
            trigger.classList.remove('active');
            if (trigger.getAttribute('data-tab-trigger') === activeTabId) {
                trigger.classList.add('active');
            }
        });

        // Update content
        tabGroup.querySelectorAll('[data-tab-content]').forEach(content => {
            content.classList.remove('active');
            if (content.getAttribute('data-tab-content') === activeTabId) {
                content.classList.add('active');
            }
        });
    }

    // Accordion Management
    initAccordions() {
        document.querySelectorAll('[data-accordion-trigger]').forEach(trigger => {
            trigger.addEventListener('click', () => {
                const accordion = trigger.closest('[data-accordion-item]');
                const content = accordion.querySelector('[data-accordion-content]');
                this.toggleAccordion(accordion, content);
            });
        });
    }

    toggleAccordion(accordion, content) {
        const isOpen = accordion.classList.contains('active');
        
        if (isOpen) {
            accordion.classList.remove('active');
            content.style.height = '0';
        } else {
            accordion.classList.add('active');
            content.style.height = content.scrollHeight + 'px';
        }
    }

    // Progress Bar Management
    initProgressBars() {
        document.querySelectorAll('[data-progress]').forEach(progressBar => {
            const value = progressBar.getAttribute('data-progress');
            this.updateProgress(progressBar, value);
        });
    }

    updateProgress(progressBar, value) {
        const bar = progressBar.querySelector('.progress-bar');
        if (bar) {
            bar.style.width = `${Math.min(Math.max(value, 0), 100)}%`;
        }
    }

    // Form Validation
    validateField(field) {
        const validationType = field.getAttribute('data-validate');
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        switch (validationType) {
            case 'required':
                isValid = value.length > 0;
                errorMessage = 'This field is required';
                break;
            case 'email':
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                isValid = emailRegex.test(value);
                errorMessage = 'Please enter a valid email address';
                break;
            case 'url':
                try {
                    new URL(value);
                    isValid = true;
                } catch {
                    isValid = false;
                    errorMessage = 'Please enter a valid URL';
                }
                break;
            case 'min-length':
                const minLength = parseInt(field.getAttribute('data-min-length')) || 0;
                isValid = value.length >= minLength;
                errorMessage = `Minimum length is ${minLength} characters`;
                break;
        }

        this.setFieldValidation(field, isValid, errorMessage);
        return isValid;
    }

    setFieldValidation(field, isValid, errorMessage) {
        const formGroup = field.closest('.form-group');
        let errorElement = formGroup?.querySelector('.form-error');

        if (isValid) {
            field.classList.remove('invalid');
            if (errorElement) {
                errorElement.remove();
            }
        } else {
            field.classList.add('invalid');
            if (!errorElement && formGroup) {
                errorElement = document.createElement('div');
                errorElement.className = 'form-error';
                errorElement.textContent = errorMessage;
                formGroup.appendChild(errorElement);
            }
        }
    }

    // Auto-save functionality
    autoSave(field) {
        const key = field.getAttribute('data-autosave');
        clearTimeout(field.autoSaveTimeout);
        
        field.autoSaveTimeout = setTimeout(() => {
            localStorage.setItem(`autosave_${key}`, field.value);
            this.showToast('Draft saved', 'info', 2000);
        }, 1000);
    }

    loadAutoSave(field) {
        const key = field.getAttribute('data-autosave');
        const saved = localStorage.getItem(`autosave_${key}`);
        if (saved) {
            field.value = saved;
        }
    }

    // Loading States
    setLoading(element, isLoading = true) {
        if (isLoading) {
            element.classList.add('loading');
            this.loadingStates.add(element);
            
            // Add loading overlay if it doesn't exist
            if (!element.querySelector('.loading-overlay')) {
                const overlay = document.createElement('div');
                overlay.className = 'loading-overlay';
                overlay.innerHTML = '<div class="spinner"></div>';
                element.style.position = 'relative';
                element.appendChild(overlay);
            }
        } else {
            element.classList.remove('loading');
            this.loadingStates.delete(element);
            
            const overlay = element.querySelector('.loading-overlay');
            if (overlay) {
                overlay.remove();
            }
        }
    }

    // Infinite Scroll
    initInfiniteScroll() {
        document.querySelectorAll('[data-infinite-scroll]').forEach(container => {
            const loadMore = () => {
                const scrollTop = container.scrollTop;
                const scrollHeight = container.scrollHeight;
                const clientHeight = container.clientHeight;
                
                if (scrollTop + clientHeight >= scrollHeight - 100) {
                    const callback = container.getAttribute('data-infinite-scroll');
                    if (window[callback] && typeof window[callback] === 'function') {
                        window[callback]();
                    }
                }
            };

            container.addEventListener('scroll', this.throttle(loadMore, 200));
        });
    }

    // Lazy Loading
    initLazyLoading() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.getAttribute('data-src');
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                img.classList.add('lazy');
                observer.observe(img);
            });
        }
    }

    // API Request Wrapper
    async request(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };

        const config = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            return data;
        } catch (error) {
            console.error('API Request failed:', error);
            this.showToast(error.message, 'error');
            throw error;
        }
    }

    // Utility Functions
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

    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    formatCurrency(amount, currency = 'USD') {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    formatDate(date, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        };
        return new Intl.DateTimeFormat('en-US', {
            ...defaultOptions,
            ...options
        }).format(new Date(date));
    }

    formatNumber(number, options = {}) {
        return new Intl.NumberFormat('en-US', options).format(number);
    }

    // Animation Utilities
    animate(element, animation, duration = 300) {
        return new Promise((resolve) => {
            element.style.animation = `${animation} ${duration}ms ease-in-out`;
            
            const handleAnimationEnd = () => {
                element.style.animation = '';
                element.removeEventListener('animationend', handleAnimationEnd);
                resolve();
            };
            
            element.addEventListener('animationend', handleAnimationEnd);
        });
    }

    slideDown(element, duration = 300) {
        element.style.height = '0';
        element.style.overflow = 'hidden';
        element.style.transition = `height ${duration}ms ease-in-out`;
        
        setTimeout(() => {
            element.style.height = element.scrollHeight + 'px';
        }, 10);
        
        setTimeout(() => {
            element.style.height = '';
            element.style.overflow = '';
            element.style.transition = '';
        }, duration);
    }

    slideUp(element, duration = 300) {
        element.style.height = element.offsetHeight + 'px';
        element.style.overflow = 'hidden';
        element.style.transition = `height ${duration}ms ease-in-out`;
        
        setTimeout(() => {
            element.style.height = '0';
        }, 10);
        
        setTimeout(() => {
            element.style.display = 'none';
            element.style.height = '';
            element.style.overflow = '';
            element.style.transition = '';
        }, duration);
    }

    fadeIn(element, duration = 300) {
        element.style.opacity = '0';
        element.style.transition = `opacity ${duration}ms ease-in-out`;
        
        setTimeout(() => {
            element.style.opacity = '1';
        }, 10);
        
        setTimeout(() => {
            element.style.transition = '';
        }, duration);
    }

    fadeOut(element, duration = 300) {
        element.style.transition = `opacity ${duration}ms ease-in-out`;
        element.style.opacity = '0';
        
        setTimeout(() => {
            element.style.display = 'none';
            element.style.transition = '';
            element.style.opacity = '';
        }, duration);
    }

    // Mobile Detection
    isMobile() {
        return window.innerWidth <= this.mobileBreakpoint;
    }

    // Handle Resize
    handleResize() {
        // Close dropdowns on mobile orientation change
        if (this.isMobile()) {
            this.closeAllDropdowns();
        }

        // Reposition visible dropdowns
        document.querySelectorAll('.dropdown.active').forEach(dropdown => {
            this.positionDropdown(dropdown);
        });
    }

    // Copy to Clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            this.showToast('Copied to clipboard', 'success', 2000);
            return true;
        } catch (error) {
            console.error('Failed to copy:', error);
            this.showToast('Failed to copy to clipboard', 'error');
            return false;
        }
    }

    // Local Storage Helpers
    setStorage(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Failed to save to localStorage:', error);
        }
    }

    getStorage(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Failed to read from localStorage:', error);
            return defaultValue;
        }
    }

    removeStorage(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Failed to remove from localStorage:', error);
        }
    }

    // Mobile Navigation Management
    initMobileNavigation() {
        // Create mobile navigation elements if they don't exist
        this.createMobileNavElements();
        
        // Setup event listeners
        const mobileToggle = document.querySelector('.mobile-nav-toggle');
        const mobileBackdrop = document.querySelector('.mobile-nav-backdrop');
        const sidebar = document.querySelector('.sidebar');
        
        if (mobileToggle) {
            mobileToggle.addEventListener('click', () => {
                this.toggleMobileNav();
            });
        }
        
        if (mobileBackdrop) {
            mobileBackdrop.addEventListener('click', () => {
                this.closeMobileNav();
            });
        }
        
        // Close mobile nav on escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && sidebar?.classList.contains('mobile-open')) {
                this.closeMobileNav();
            }
        });
        
        // Close mobile nav when clicking nav links
        document.querySelectorAll('.sidebar .nav-link').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= this.mobileBreakpoint) {
                    this.closeMobileNav();
                }
            });
        });
    }
    
    createMobileNavElements() {
        // Create mobile nav toggle if it doesn't exist
        if (!document.querySelector('.mobile-nav-toggle')) {
            const toggle = document.createElement('button');
            toggle.className = 'mobile-nav-toggle';
            toggle.setAttribute('aria-label', 'Toggle navigation menu');
            toggle.setAttribute('aria-expanded', 'false');
            toggle.innerHTML = `
                <div class="hamburger">
                    <div class="hamburger-line"></div>
                    <div class="hamburger-line"></div>
                    <div class="hamburger-line"></div>
                </div>
            `;
            document.body.appendChild(toggle);
        }
        
        // Create mobile backdrop if it doesn't exist
        if (!document.querySelector('.mobile-nav-backdrop')) {
            const backdrop = document.createElement('div');
            backdrop.className = 'mobile-nav-backdrop';
            backdrop.setAttribute('aria-hidden', 'true');
            document.body.appendChild(backdrop);
        }
    }
    
    toggleMobileNav() {
        const sidebar = document.querySelector('.sidebar');
        const toggle = document.querySelector('.mobile-nav-toggle');
        const backdrop = document.querySelector('.mobile-nav-backdrop');
        
        if (sidebar && toggle && backdrop) {
            const isOpen = sidebar.classList.contains('mobile-open');
            
            if (isOpen) {
                this.closeMobileNav();
            } else {
                this.openMobileNav();
            }
        }
    }
    
    openMobileNav() {
        const sidebar = document.querySelector('.sidebar');
        const toggle = document.querySelector('.mobile-nav-toggle');
        const backdrop = document.querySelector('.mobile-nav-backdrop');
        
        if (sidebar && toggle && backdrop) {
            sidebar.classList.add('mobile-open');
            toggle.classList.add('active');
            toggle.setAttribute('aria-expanded', 'true');
            backdrop.classList.add('active');
            backdrop.setAttribute('aria-hidden', 'false');
            
            // Prevent body scroll
            document.body.style.overflow = 'hidden';
            
            // Focus first nav link
            const firstNavLink = sidebar.querySelector('.nav-link');
            if (firstNavLink) {
                setTimeout(() => firstNavLink.focus(), 100);
            }
        }
    }
    
    closeMobileNav() {
        const sidebar = document.querySelector('.sidebar');
        const toggle = document.querySelector('.mobile-nav-toggle');
        const backdrop = document.querySelector('.mobile-nav-backdrop');
        
        if (sidebar && toggle && backdrop) {
            sidebar.classList.remove('mobile-open');
            toggle.classList.remove('active');
            toggle.setAttribute('aria-expanded', 'false');
            backdrop.classList.remove('active');
            backdrop.setAttribute('aria-hidden', 'true');
            
            // Restore body scroll
            document.body.style.overflow = '';
            
            // Return focus to toggle button
            toggle.focus();
        }
    }
    
    // ARIA and Accessibility Utilities
    announceToScreenReader(message, priority = 'polite') {
        let liveRegion = document.querySelector('.live-region');
        
        if (!liveRegion) {
            liveRegion = document.createElement('div');
            liveRegion.className = 'live-region';
            liveRegion.setAttribute('aria-live', priority);
            liveRegion.setAttribute('aria-atomic', 'true');
            document.body.appendChild(liveRegion);
        }
        
        // Clear and set message
        liveRegion.textContent = '';
        setTimeout(() => {
            liveRegion.textContent = message;
        }, 100);
    }
    
    // Enhanced Loading States with ARIA
    setLoadingAria(element, isLoading = true, message = 'Loading...') {
        if (isLoading) {
            element.setAttribute('aria-busy', 'true');
            element.setAttribute('aria-live', 'polite');
            
            if (message) {
                this.announceToScreenReader(message);
            }
            
            this.setLoading(element, true);
        } else {
            element.removeAttribute('aria-busy');
            element.removeAttribute('aria-live');
            this.setLoading(element, false);
            
            this.announceToScreenReader('Loading complete');
        }
    }
    
    // Enhanced Form Validation with ARIA
    setFieldValidationAria(field, isValid, errorMessage) {
        const formGroup = field.closest('.form-group');
        let errorElement = formGroup?.querySelector('.form-error');
        let errorId = field.getAttribute('aria-describedby');
        
        if (isValid) {
            field.classList.remove('invalid');
            field.removeAttribute('aria-invalid');
            
            if (errorElement) {
                field.removeAttribute('aria-describedby');
                errorElement.remove();
            }
        } else {
            field.classList.add('invalid');
            field.setAttribute('aria-invalid', 'true');
            
            if (!errorElement && formGroup) {
                errorElement = document.createElement('div');
                errorElement.className = 'form-error';
                errorElement.id = `error-${Date.now()}`;
                errorElement.textContent = errorMessage;
                formGroup.appendChild(errorElement);
                
                field.setAttribute('aria-describedby', errorElement.id);
            }
        }
    }
    
    // Enhanced Modal with Focus Management
    openModalWithFocus(modalId) {
        const modal = document.querySelector(`#${modalId}`);
        if (modal) {
            // Store currently focused element
            this.previouslyFocused = document.activeElement;
            
            this.openModal(modalId);
            
            // Set up focus trap
            this.setupFocusTrap(modal);
        }
    }
    
    closeModalWithFocus(modal) {
        this.closeModal(modal);
        
        // Restore focus to previously focused element
        if (this.previouslyFocused) {
            this.previouslyFocused.focus();
            this.previouslyFocused = null;
        }
    }
    
    setupFocusTrap(modal) {
        const focusableElements = modal.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        if (focusableElements.length > 0) {
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];
            
            // Focus first element
            firstElement.focus();
            
            // Handle tab key
            modal.addEventListener('keydown', (e) => {
                if (e.key === 'Tab') {
                    if (e.shiftKey) {
                        if (document.activeElement === firstElement) {
                            e.preventDefault();
                            lastElement.focus();
                        }
                    } else {
                        if (document.activeElement === lastElement) {
                            e.preventDefault();
                            firstElement.focus();
                        }
                    }
                }
            });
        }
    }
    
    // Keyboard Navigation Helpers
    handleArrowKeyNavigation(container, selector) {
        const items = container.querySelectorAll(selector);
        let currentIndex = Array.from(items).findIndex(item => 
            item === document.activeElement
        );
        
        container.addEventListener('keydown', (e) => {
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
                e.preventDefault();
                
                if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
                    currentIndex = (currentIndex + 1) % items.length;
                } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
                    currentIndex = (currentIndex - 1 + items.length) % items.length;
                }
                
                items[currentIndex].focus();
            }
        });
    }
    
    // Add Skip Links for Accessibility
    addSkipLinks() {
        if (!document.querySelector('.skip-link')) {
            const skipLink = document.createElement('a');
            skipLink.className = 'skip-link';
            skipLink.href = '#main-content';
            skipLink.textContent = 'Skip to main content';
            skipLink.setAttribute('aria-label', 'Skip to main content');
            document.body.insertBefore(skipLink, document.body.firstChild);
            
            // Add main content landmark if it doesn't exist
            const mainContent = document.querySelector('main, [role="main"], #main-content');
            if (mainContent && !mainContent.id) {
                mainContent.id = 'main-content';
            }
        }
    }
    
    // Initialize ARIA Live Regions
    initAriaLiveRegions() {
        if (!document.querySelector('.live-region')) {
            const liveRegion = document.createElement('div');
            liveRegion.className = 'live-region';
            liveRegion.setAttribute('aria-live', 'polite');
            liveRegion.setAttribute('aria-atomic', 'true');
            document.body.appendChild(liveRegion);
        }
    }
    
    // Enhanced Handle Resize with Mobile Nav
    handleResize() {
        // Close mobile nav if screen becomes large
        if (window.innerWidth > this.mobileBreakpoint) {
            this.closeMobileNav();
        }
        
        // Close dropdowns on mobile orientation change
        if (this.isMobile()) {
            this.closeAllDropdowns();
        }

        // Reposition visible dropdowns
        document.querySelectorAll('.dropdown.active').forEach(dropdown => {
            this.positionDropdown(dropdown);
        });
    }
    
    // Initialize UI on DOM ready
    static init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                window.enhancedUI = new EnhancedUI();
            });
        } else {
            window.enhancedUI = new EnhancedUI();
        }
    }
}

// Auto-initialize
EnhancedUI.init();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = EnhancedUI;
}