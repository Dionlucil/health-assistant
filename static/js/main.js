// Community Health Assistant - Main JavaScript

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize accessibility features
    initializeAccessibility();
    
    // Initialize theme handler
    initializeThemeHandler();
}

// Tooltip initialization
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0 && typeof bootstrap !== 'undefined') {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => 
            new bootstrap.Tooltip(tooltipTriggerEl)
        );
    }
}

// Form enhancements
function initializeFormEnhancements() {
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !form.dataset.noLoading) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                }, 10000);
            }
        });
    });
    
    // Enhanced validation for email fields
    const emailFields = document.querySelectorAll('input[type="email"]');
    emailFields.forEach(field => {
        field.addEventListener('blur', validateEmail);
        field.addEventListener('input', clearValidationError);
    });
    
    // Enhanced validation for password fields
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        field.addEventListener('input', validatePassword);
    });
    
    // Checkbox and radio enhancements
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.nextElementSibling;
            if (label) {
                if (this.checked) {
                    label.classList.add('fw-bold', 'text-primary');
                } else {
                    label.classList.remove('fw-bold', 'text-primary');
                }
            }
        });
    });
}

// Email validation
function validateEmail(event) {
    const email = event.target.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        showFieldError(event.target, 'Please enter a valid email address');
    } else {
        clearFieldError(event.target);
    }
}

// Password validation
function validatePassword(event) {
    const password = event.target.value;
    const minLength = 6;
    
    if (password.length > 0 && password.length < minLength) {
        showFieldError(event.target, `Password must be at least ${minLength} characters long`);
    } else {
        clearFieldError(event.target);
    }
}

// Show field validation error
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

// Clear field validation error
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Clear validation error on input
function clearValidationError(event) {
    clearFieldError(event.target);
}

// Animation initialization
function initializeAnimations() {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe cards and other animated elements
    const animatedElements = document.querySelectorAll('.card, .feature-card, .action-card');
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Accessibility enhancements
function initializeAccessibility() {
    // Enhanced keyboard navigation
    document.addEventListener('keydown', function(e) {
        // Skip to main content with Alt+S
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            const mainContent = document.getElementById('main-content');
            if (mainContent) {
                mainContent.focus();
                mainContent.scrollIntoView();
            }
        }
        
        // Close modals with Escape key
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
    
    // Announce page changes for screen readers
    announcePageChange();
    
    // Focus management for dynamic content
    manageFocus();
}

// Announce page changes
function announcePageChange() {
    const pageTitle = document.title;
    const announcement = document.createElement('div');
    announcement.setAttribute('aria-live', 'polite');
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only';
    announcement.textContent = `Page loaded: ${pageTitle}`;
    
    document.body.appendChild(announcement);
    
    // Remove after announcement
    setTimeout(() => {
        document.body.removeChild(announcement);
    }, 1000);
}

// Focus management
function manageFocus() {
    // Focus first form field on form pages
    const firstInput = document.querySelector('form input:not([type="hidden"]), form select, form textarea');
    if (firstInput && !document.querySelector('.alert-danger')) {
        setTimeout(() => {
            firstInput.focus();
        }, 100);
    }
    
    // Focus error messages
    const errorAlert = document.querySelector('.alert-danger');
    if (errorAlert) {
        errorAlert.setAttribute('tabindex', '-1');
        errorAlert.focus();
    }
}

// Theme handler
function initializeThemeHandler() {
    // System theme detection
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Listen for system theme changes
    prefersDark.addEventListener('change', function(e) {
        handleThemeChange(e.matches ? 'dark' : 'light');
    });
    
    // Reduced motion handling
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (prefersReducedMotion.matches) {
        document.body.classList.add('reduce-motion');
    }
}

// Handle theme changes
function handleThemeChange(theme) {
    document.body.setAttribute('data-theme', theme);
    
    // Update any theme-dependent elements
    const themeElements = document.querySelectorAll('[data-theme-element]');
    themeElements.forEach(element => {
        element.classList.toggle('dark-theme', theme === 'dark');
    });
}

// Utility functions
const Utils = {
    // Debounce function
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    // Throttle function
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Format date for display
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    // Format time for display
    formatTime: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    },
    
    // Show notification
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
};

// Health-specific utilities
const HealthUtils = {
    // Calculate age from date of birth
    calculateAge: function(dateOfBirth) {
        const today = new Date();
        const birthDate = new Date(dateOfBirth);
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--;
        }
        
        return age;
    },
    
    // Format symptom names for display
    formatSymptomName: function(symptom) {
        return symptom.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    },
    
    // Get urgency color class
    getUrgencyColorClass: function(urgency) {
        switch (urgency.toLowerCase()) {
            case 'high': return 'text-danger';
            case 'medium': return 'text-warning';
            case 'low': return 'text-success';
            default: return 'text-muted';
        }
    },
    
    // Get severity badge class
    getSeverityBadgeClass: function(severity) {
        switch (severity.toLowerCase()) {
            case 'severe': return 'bg-danger';
            case 'moderate': return 'bg-warning';
            case 'mild': return 'bg-success';
            default: return 'bg-secondary';
        }
    }
};

// Export utilities for use in other scripts
window.HealthAssistant = {
    Utils,
    HealthUtils,
    initializeApp,
    showNotification: Utils.showNotification
};

// Performance monitoring
window.addEventListener('load', function() {
    // Log performance metrics
    if (window.performance && window.performance.timing) {
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        console.log(`Page loaded in ${loadTime}ms`);
    }
});

// Error handling
window.addEventListener('error', function(e) {
    console.error('Application error:', e.error);
    
    // Show user-friendly error message for critical errors
    if (e.error && e.error.message && !e.error.message.includes('Script error')) {
        Utils.showNotification(
            'An unexpected error occurred. Please refresh the page and try again.',
            'danger'
        );
    }
});

// Service worker registration (for future PWA support)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // Service worker would be registered here in production
        console.log('Service worker support detected');
    });
}
