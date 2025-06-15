/**
 * Mobile Navigation Component
 * Provides smooth, accessible mobile navigation with touch gestures
 */

class MobileNavigation {
    constructor() {
        this.isOpen = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.isScrolling = false;
        this.init();
    }
    
    init() {
        this.createMobileNav();
        this.setupEventListeners();
        this.setupTouchGestures();
        this.setupKeyboardNavigation();
        this.observeViewportChanges();
    }
    
    createMobileNav() {
        // Create mobile navigation HTML if it doesn't exist
        if (!document.getElementById('mobileNav')) {
            const mobileNavHTML = `
                <div id="mobileNav" class="mobile-nav" aria-label="Mobile navigation">
                    <!-- Mobile Header -->
                    <div class="mobile-nav-header">
                        <button id="mobileNavToggle" class="mobile-nav-toggle" aria-label="Toggle navigation menu" aria-expanded="false">
                            <span class="hamburger-line"></span>
                            <span class="hamburger-line"></span>
                            <span class="hamburger-line"></span>
                        </button>
                        <div class="mobile-nav-logo">
                            <span class="logo-icon">🚀</span>
                            <span class="logo-text">AI Platform</span>
                        </div>
                        <div class="mobile-nav-actions">
                            <button class="mobile-action-btn" aria-label="Notifications">
                                <span class="notification-icon">🔔</span>
                                <span class="notification-badge">2</span>
                            </button>
                        </div>
                    </div>
                    
                    <!-- Mobile Menu Overlay -->
                    <div id="mobileNavOverlay" class="mobile-nav-overlay" aria-hidden="true"></div>
                    
                    <!-- Mobile Menu Sidebar -->
                    <nav id="mobileNavSidebar" class="mobile-nav-sidebar" aria-hidden="true" role="navigation">
                        <div class="mobile-nav-content">
                            <!-- User Profile Section -->
                            <div class="mobile-user-profile">
                                <div class="user-avatar">
                                    <img src="https://ui-avatars.com/api/?name=John+Doe&background=667eea&color=fff" alt="User avatar">
                                </div>
                                <div class="user-info">
                                    <div class="user-name">John Doe</div>
                                    <div class="user-email">john@example.com</div>
                                    <div class="user-plan">Pro Plan</div>
                                </div>
                            </div>
                            
                            <!-- Quick Stats -->
                            <div class="mobile-quick-stats">
                                <div class="stat-item">
                                    <div class="stat-value">$28.76</div>
                                    <div class="stat-label">Today's Usage</div>
                                </div>
                                <div class="stat-item">
                                    <div class="stat-value">5</div>
                                    <div class="stat-label">Active Integrations</div>
                                </div>
                            </div>
                            
                            <!-- Navigation Menu -->
                            <div class="mobile-nav-menu">
                                <a href="/dashboard" class="mobile-nav-item active">
                                    <span class="nav-icon">📊</span>
                                    <span class="nav-text">Dashboard</span>
                                    <span class="nav-arrow">→</span>
                                </a>
                                
                                <a href="/integration-quickstart" class="mobile-nav-item">
                                    <span class="nav-icon">🔌</span>
                                    <span class="nav-text">Integrations</span>
                                    <span class="nav-badge">3</span>
                                    <span class="nav-arrow">→</span>
                                </a>
                                
                                <div class="mobile-nav-expandable">
                                    <button class="mobile-nav-item expandable-trigger" aria-expanded="false">
                                        <span class="nav-icon">🤖</span>
                                        <span class="nav-text">AI Services</span>
                                        <span class="nav-expand">⌄</span>
                                    </button>
                                    <div class="expandable-content">
                                        <a href="/services/chatbots" class="mobile-nav-subitem">
                                            <span class="subnav-icon">💬</span>
                                            <span class="subnav-text">Chatbots</span>
                                        </a>
                                        <a href="/services/image" class="mobile-nav-subitem">
                                            <span class="subnav-icon">🎨</span>
                                            <span class="subnav-text">Image Generation</span>
                                        </a>
                                        <a href="/services/video" class="mobile-nav-subitem">
                                            <span class="subnav-icon">🎬</span>
                                            <span class="subnav-text">Video Creation</span>
                                        </a>
                                    </div>
                                </div>
                                
                                <a href="/usage" class="mobile-nav-item">
                                    <span class="nav-icon">📈</span>
                                    <span class="nav-text">Usage & Billing</span>
                                    <span class="nav-arrow">→</span>
                                </a>
                                
                                <a href="/settings" class="mobile-nav-item">
                                    <span class="nav-icon">⚙️</span>
                                    <span class="nav-text">Settings</span>
                                    <span class="nav-arrow">→</span>
                                </a>
                                
                                <div class="mobile-nav-divider"></div>
                                
                                <a href="/help" class="mobile-nav-item">
                                    <span class="nav-icon">❓</span>
                                    <span class="nav-text">Help & Support</span>
                                    <span class="nav-arrow">→</span>
                                </a>
                                
                                <a href="/docs" class="mobile-nav-item">
                                    <span class="nav-icon">📚</span>
                                    <span class="nav-text">Documentation</span>
                                    <span class="nav-arrow">→</span>
                                </a>
                            </div>
                            
                            <!-- Quick Actions -->
                            <div class="mobile-quick-actions">
                                <button class="quick-action-btn primary">
                                    <span class="action-icon">➕</span>
                                    <span class="action-text">Add Integration</span>
                                </button>
                                <button class="quick-action-btn secondary">
                                    <span class="action-icon">🚀</span>
                                    <span class="action-text">Quick Generate</span>
                                </button>
                            </div>
                            
                            <!-- Footer -->
                            <div class="mobile-nav-footer">
                                <button class="logout-btn">
                                    <span class="logout-icon">🚪</span>
                                    <span class="logout-text">Sign Out</span>
                                </button>
                                <div class="app-version">v2.1.0</div>
                            </div>
                        </div>
                    </nav>
                </div>
            `;
            
            document.body.insertAdjacentHTML('afterbegin', mobileNavHTML);
        }
        
        // Add mobile navigation styles
        this.addStyles();
    }
    
    addStyles() {
        if (!document.getElementById('mobileNavStyles')) {
            const styles = document.createElement('style');
            styles.id = 'mobileNavStyles';
            styles.textContent = `
                /* Mobile Navigation Styles */
                .mobile-nav {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    z-index: 9999;
                    display: none;
                }
                
                @media (max-width: 768px) {
                    .mobile-nav {
                        display: block;
                    }
                    
                    /* Hide desktop navigation on mobile */
                    .sidebar, .desktop-nav {
                        display: none !important;
                    }
                    
                    /* Adjust main content for mobile header */
                    .main-content, .container {
                        margin-top: 70px;
                        padding-top: 20px;
                    }
                }
                
                /* Mobile Header */
                .mobile-nav-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    height: 70px;
                    display: flex;
                    align-items: center;
                    padding: 0 20px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    position: relative;
                    z-index: 10001;
                }
                
                .mobile-nav-toggle {
                    background: none;
                    border: none;
                    width: 44px;
                    height: 44px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    gap: 4px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    border-radius: 8px;
                }
                
                .mobile-nav-toggle:hover {
                    background: rgba(255,255,255,0.1);
                }
                
                .mobile-nav-toggle:focus {
                    outline: 2px solid rgba(255,255,255,0.5);
                    outline-offset: 2px;
                }
                
                .hamburger-line {
                    width: 20px;
                    height: 2px;
                    background: white;
                    transition: all 0.3s ease;
                    transform-origin: center;
                }
                
                .mobile-nav-toggle.active .hamburger-line:nth-child(1) {
                    transform: rotate(45deg) translate(5px, 5px);
                }
                
                .mobile-nav-toggle.active .hamburger-line:nth-child(2) {
                    opacity: 0;
                }
                
                .mobile-nav-toggle.active .hamburger-line:nth-child(3) {
                    transform: rotate(-45deg) translate(7px, -6px);
                }
                
                .mobile-nav-logo {
                    flex: 1;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    margin-left: 15px;
                }
                
                .logo-icon {
                    font-size: 24px;
                }
                
                .logo-text {
                    font-size: 18px;
                    font-weight: 700;
                }
                
                .mobile-nav-actions {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                
                .mobile-action-btn {
                    width: 44px;
                    height: 44px;
                    border: none;
                    background: rgba(255,255,255,0.1);
                    border-radius: 12px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    position: relative;
                }
                
                .mobile-action-btn:hover {
                    background: rgba(255,255,255,0.2);
                }
                
                .notification-badge {
                    position: absolute;
                    top: -2px;
                    right: -2px;
                    background: #ff4757;
                    color: white;
                    font-size: 10px;
                    width: 16px;
                    height: 16px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                }
                
                /* Mobile Overlay */
                .mobile-nav-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background: rgba(0,0,0,0.5);
                    backdrop-filter: blur(4px);
                    opacity: 0;
                    visibility: hidden;
                    transition: all 0.3s ease;
                    z-index: 10000;
                }
                
                .mobile-nav-overlay.active {
                    opacity: 1;
                    visibility: visible;
                }
                
                /* Mobile Sidebar */
                .mobile-nav-sidebar {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 320px;
                    height: 100vh;
                    background: white;
                    transform: translateX(-100%);
                    transition: transform 0.3s ease;
                    z-index: 10001;
                    overflow-y: auto;
                    box-shadow: 10px 0 30px rgba(0,0,0,0.1);
                }
                
                .mobile-nav-sidebar.active {
                    transform: translateX(0);
                }
                
                .mobile-nav-content {
                    padding: 90px 0 30px 0;
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                }
                
                /* User Profile Section */
                .mobile-user-profile {
                    padding: 0 20px 20px 20px;
                    border-bottom: 1px solid #e2e8f0;
                    margin-bottom: 20px;
                }
                
                .user-avatar {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    overflow: hidden;
                    margin: 0 auto 15px;
                    border: 3px solid #667eea;
                }
                
                .user-avatar img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }
                
                .user-info {
                    text-align: center;
                }
                
                .user-name {
                    font-size: 18px;
                    font-weight: 600;
                    color: #2d3748;
                    margin-bottom: 2px;
                }
                
                .user-email {
                    font-size: 14px;
                    color: #718096;
                    margin-bottom: 5px;
                }
                
                .user-plan {
                    font-size: 12px;
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    display: inline-block;
                }
                
                /* Quick Stats */
                .mobile-quick-stats {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    padding: 0 20px 20px 20px;
                    margin-bottom: 20px;
                    border-bottom: 1px solid #e2e8f0;
                }
                
                .stat-item {
                    text-align: center;
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 12px;
                }
                
                .stat-value {
                    font-size: 20px;
                    font-weight: 700;
                    color: #2d3748;
                    margin-bottom: 2px;
                }
                
                .stat-label {
                    font-size: 12px;
                    color: #718096;
                }
                
                /* Navigation Menu */
                .mobile-nav-menu {
                    flex: 1;
                    padding: 0 10px;
                }
                
                .mobile-nav-item {
                    display: flex;
                    align-items: center;
                    padding: 15px;
                    margin: 2px 0;
                    border-radius: 12px;
                    text-decoration: none;
                    color: #2d3748;
                    transition: all 0.3s ease;
                    border: none;
                    background: none;
                    width: 100%;
                    cursor: pointer;
                    font-size: 16px;
                }
                
                .mobile-nav-item:hover {
                    background: #f0f4f8;
                    color: #667eea;
                }
                
                .mobile-nav-item.active {
                    background: linear-gradient(135deg, #667eea10, #764ba210);
                    color: #667eea;
                    font-weight: 600;
                }
                
                .nav-icon {
                    width: 24px;
                    text-align: center;
                    margin-right: 15px;
                    font-size: 18px;
                }
                
                .nav-text {
                    flex: 1;
                    text-align: left;
                }
                
                .nav-badge {
                    background: #667eea;
                    color: white;
                    font-size: 12px;
                    padding: 2px 8px;
                    border-radius: 10px;
                    margin-right: 10px;
                }
                
                .nav-arrow {
                    color: #a0aec0;
                    font-size: 14px;
                }
                
                .nav-expand {
                    color: #a0aec0;
                    font-size: 16px;
                    transition: transform 0.3s ease;
                }
                
                .expandable-trigger[aria-expanded="true"] .nav-expand {
                    transform: rotate(180deg);
                }
                
                /* Expandable Content */
                .mobile-nav-expandable {
                    margin: 2px 0;
                }
                
                .expandable-content {
                    max-height: 0;
                    overflow: hidden;
                    transition: max-height 0.3s ease;
                    background: #f8f9fa;
                    border-radius: 12px;
                    margin-top: 2px;
                }
                
                .expandable-content.expanded {
                    max-height: 200px;
                }
                
                .mobile-nav-subitem {
                    display: flex;
                    align-items: center;
                    padding: 12px 15px 12px 40px;
                    text-decoration: none;
                    color: #4a5568;
                    transition: all 0.3s ease;
                    font-size: 14px;
                }
                
                .mobile-nav-subitem:hover {
                    background: #e2e8f0;
                    color: #667eea;
                }
                
                .subnav-icon {
                    width: 20px;
                    text-align: center;
                    margin-right: 12px;
                    font-size: 16px;
                }
                
                .mobile-nav-divider {
                    height: 1px;
                    background: #e2e8f0;
                    margin: 20px 15px;
                }
                
                /* Quick Actions */
                .mobile-quick-actions {
                    padding: 20px;
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 10px;
                    border-top: 1px solid #e2e8f0;
                }
                
                .quick-action-btn {
                    padding: 12px;
                    border-radius: 12px;
                    border: none;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 5px;
                }
                
                .quick-action-btn.primary {
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                }
                
                .quick-action-btn.secondary {
                    background: #f0f4f8;
                    color: #667eea;
                    border: 1px solid #e2e8f0;
                }
                
                .quick-action-btn:hover {
                    transform: translateY(-2px);
                }
                
                .action-icon {
                    font-size: 16px;
                }
                
                .action-text {
                    font-size: 12px;
                }
                
                /* Footer */
                .mobile-nav-footer {
                    padding: 20px;
                    border-top: 1px solid #e2e8f0;
                    margin-top: auto;
                }
                
                .logout-btn {
                    width: 100%;
                    padding: 15px;
                    background: #fff5f5;
                    border: 1px solid #fed7d7;
                    border-radius: 12px;
                    color: #e53e3e;
                    font-size: 16px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    margin-bottom: 15px;
                }
                
                .logout-btn:hover {
                    background: #fed7d7;
                }
                
                .app-version {
                    text-align: center;
                    font-size: 12px;
                    color: #a0aec0;
                }
                
                /* Animations */
                @keyframes slideInLeft {
                    from { transform: translateX(-100%); }
                    to { transform: translateX(0); }
                }
                
                @keyframes slideOutLeft {
                    from { transform: translateX(0); }
                    to { transform: translateX(-100%); }
                }
                
                /* Accessibility */
                .mobile-nav-sidebar:focus-within {
                    outline: 2px solid #667eea;
                    outline-offset: -2px;
                }
                
                /* Touch improvements */
                .mobile-nav-item, .mobile-action-btn, .quick-action-btn {
                    min-height: 44px;
                    min-width: 44px;
                }
                
                /* Reduced motion */
                @media (prefers-reduced-motion: reduce) {
                    .mobile-nav-sidebar,
                    .mobile-nav-overlay,
                    .mobile-nav-toggle,
                    .hamburger-line,
                    .expandable-content {
                        transition: none;
                    }
                }
            `;
            document.head.appendChild(styles);
        }
    }
    
    setupEventListeners() {
        const toggle = document.getElementById('mobileNavToggle');
        const overlay = document.getElementById('mobileNavOverlay');
        const sidebar = document.getElementById('mobileNavSidebar');
        
        // Toggle button
        toggle?.addEventListener('click', () => this.toggleNav());
        
        // Overlay click to close
        overlay?.addEventListener('click', () => this.closeNav());
        
        // Expandable menu items
        document.querySelectorAll('.expandable-trigger').forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleExpandable(trigger);
            });
        });
        
        // Close on navigation
        document.querySelectorAll('.mobile-nav-item:not(.expandable-trigger)').forEach(item => {
            item.addEventListener('click', () => {
                if (item.getAttribute('href')) {
                    this.closeNav();
                }
            });
        });
        
        // Quick actions
        document.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                // Handle quick actions
                const text = btn.querySelector('.action-text')?.textContent;
                if (text === 'Add Integration') {
                    window.location.href = '/integration-quickstart';
                } else if (text === 'Quick Generate') {
                    // Open quick generate modal
                    this.closeNav();
                }
            });
        });
    }
    
    setupTouchGestures() {
        const sidebar = document.getElementById('mobileNavSidebar');
        const overlay = document.getElementById('mobileNavOverlay');
        
        // Touch events for swipe gestures
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
            this.isScrolling = false;
        }, { passive: true });
        
        document.addEventListener('touchmove', (e) => {
            if (!this.touchStartX || !this.touchStartY) return;
            
            const touchX = e.touches[0].clientX;
            const touchY = e.touches[0].clientY;
            const diffX = this.touchStartX - touchX;
            const diffY = this.touchStartY - touchY;
            
            // Detect if this is a vertical scroll
            if (Math.abs(diffY) > Math.abs(diffX)) {
                this.isScrolling = true;
                return;
            }
            
            // Swipe right to open (from left edge)
            if (this.touchStartX < 20 && diffX < -50 && !this.isScrolling && !this.isOpen) {
                this.openNav();
            }
            
            // Swipe left to close (when nav is open)
            if (diffX > 50 && !this.isScrolling && this.isOpen) {
                this.closeNav();
            }
        }, { passive: true });
        
        document.addEventListener('touchend', () => {
            this.touchStartX = 0;
            this.touchStartY = 0;
            this.isScrolling = false;
        }, { passive: true });
    }
    
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            // ESC to close navigation
            if (e.key === 'Escape' && this.isOpen) {
                this.closeNav();
                document.getElementById('mobileNavToggle')?.focus();
            }
            
            // Tab trapping when nav is open
            if (this.isOpen && e.key === 'Tab') {
                this.trapFocus(e);
            }
        });
    }
    
    trapFocus(e) {
        const sidebar = document.getElementById('mobileNavSidebar');
        const focusableElements = sidebar.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (e.shiftKey) {
            // Shift + Tab
            if (document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            }
        } else {
            // Tab
            if (document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
            }
        }
    }
    
    observeViewportChanges() {
        // Handle orientation changes
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.updateViewportHeight();
            }, 100);
        });
        
        // Handle resize
        window.addEventListener('resize', () => {
            this.updateViewportHeight();
            
            // Close nav on desktop
            if (window.innerWidth > 768 && this.isOpen) {
                this.closeNav();
            }
        });
    }
    
    updateViewportHeight() {
        // Fix for mobile viewport height issues
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    toggleNav() {
        if (this.isOpen) {
            this.closeNav();
        } else {
            this.openNav();
        }
    }
    
    openNav() {
        const toggle = document.getElementById('mobileNavToggle');
        const overlay = document.getElementById('mobileNavOverlay');
        const sidebar = document.getElementById('mobileNavSidebar');
        
        this.isOpen = true;
        
        // Update elements
        toggle?.classList.add('active');
        toggle?.setAttribute('aria-expanded', 'true');
        overlay?.classList.add('active');
        overlay?.setAttribute('aria-hidden', 'false');
        sidebar?.classList.add('active');
        sidebar?.setAttribute('aria-hidden', 'false');
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
        
        // Focus first focusable element
        setTimeout(() => {
            const firstFocusable = sidebar?.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            firstFocusable?.focus();
        }, 300);
        
        // Announce to screen readers
        this.announceToScreenReader('Navigation menu opened');
    }
    
    closeNav() {
        const toggle = document.getElementById('mobileNavToggle');
        const overlay = document.getElementById('mobileNavOverlay');
        const sidebar = document.getElementById('mobileNavSidebar');
        
        this.isOpen = false;
        
        // Update elements
        toggle?.classList.remove('active');
        toggle?.setAttribute('aria-expanded', 'false');
        overlay?.classList.remove('active');
        overlay?.setAttribute('aria-hidden', 'true');
        sidebar?.classList.remove('active');
        sidebar?.setAttribute('aria-hidden', 'true');
        
        // Restore body scroll
        document.body.style.overflow = '';
        
        // Announce to screen readers
        this.announceToScreenReader('Navigation menu closed');
    }
    
    toggleExpandable(trigger) {
        const content = trigger.parentElement.querySelector('.expandable-content');
        const isExpanded = trigger.getAttribute('aria-expanded') === 'true';
        
        trigger.setAttribute('aria-expanded', !isExpanded);
        
        if (!isExpanded) {
            content.classList.add('expanded');
            content.style.maxHeight = content.scrollHeight + 'px';
        } else {
            content.classList.remove('expanded');
            content.style.maxHeight = '0';
        }
    }
    
    announceToScreenReader(message) {
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.style.position = 'absolute';
        announcement.style.left = '-10000px';
        announcement.style.width = '1px';
        announcement.style.height = '1px';
        announcement.style.overflow = 'hidden';
        
        document.body.appendChild(announcement);
        announcement.textContent = message;
        
        setTimeout(() => {
            document.body.removeChild(announcement);
        }, 1000);
    }
    
    // Public methods for external use
    setActiveNavItem(href) {
        document.querySelectorAll('.mobile-nav-item').forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === href) {
                item.classList.add('active');
            }
        });
    }
    
    updateUserInfo(userData) {
        const nameElement = document.querySelector('.user-name');
        const emailElement = document.querySelector('.user-email');
        const planElement = document.querySelector('.user-plan');
        const avatarElement = document.querySelector('.user-avatar img');
        
        if (nameElement) nameElement.textContent = userData.name;
        if (emailElement) emailElement.textContent = userData.email;
        if (planElement) planElement.textContent = userData.plan;
        if (avatarElement) avatarElement.src = userData.avatar;
    }
    
    updateStats(stats) {
        const statValues = document.querySelectorAll('.stat-value');
        if (statValues[0]) statValues[0].textContent = stats.usage || '$0.00';
        if (statValues[1]) statValues[1].textContent = stats.integrations || '0';
    }
    
    updateNotificationBadge(count) {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'flex' : 'none';
        }
    }
}

// Initialize mobile navigation when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.mobileNav = new MobileNavigation();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MobileNavigation;
}