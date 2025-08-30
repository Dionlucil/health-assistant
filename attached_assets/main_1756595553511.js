// Community Health Assistant - Main JavaScript File

(function() {
    'use strict';

    // Initialize the application
    document.addEventListener('DOMContentLoaded', function() {
        initializeApp();
    });

    function initializeApp() {
        // Initialize all components
        initializeFormValidation();
        initializeTooltips();
        initializeAlerts();
        initializeAccessibility();
        initializeMobileMenu();
        initializeLoadingStates();
        initializeAnimations();
        
        // Page-specific initializations
        const currentPage = getCurrentPage();
        switch(currentPage) {
            case 'symptoms':
                initializeSymptomForm();
                break;
            case 'results':
                initializeResults();
                break;
            case 'dashboard':
                initializeDashboard();
                break;
            case 'profile':
                initializeProfile();
                break;
            case 'history':
                initializeHistory();
                break;
        }
    }

    // Utility Functions
    function getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('symptoms')) return 'symptoms';
        if (path.includes('results')) return 'results';
        if (path.includes('dashboard')) return 'dashboard';
        if (path.includes('profile')) return 'profile';
        if (path.includes('history')) return 'history';
        return 'home';
    }

    function debounce(func, wait) {
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

    // Form Validation Enhancement
    function initializeFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            // Add real-time validation
            const inputs = form.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('blur', validateField);
                input.addEventListener('input', debounce(validateField, 300));
            });

            // Enhanced form submission
            form.addEventListener('submit', function(e) {
                if (!validateForm(form)) {
                    e.preventDefault();
                    showFormErrors(form);
                } else {
                    showLoadingState(form);
                }
            });
        });
    }

    function validateField(event) {
        const field = event.target;
        const fieldContainer = field.closest('.mb-3') || field.closest('.form-group');
        const errorContainer = fieldContainer?.querySelector('.field-error') || createErrorContainer(fieldContainer);

        // Remove existing validation states
        field.classList.remove('is-valid', 'is-invalid');
        errorContainer.textContent = '';

        let isValid = true;
        let errorMessage = '';

        // Required field validation
        if (field.hasAttribute('required') && !field.value.trim()) {
            isValid = false;
            errorMessage = 'This field is required.';
        }
        
        // Email validation
        else if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address.';
            }
        }
        
        // Password validation
        else if (field.type === 'password' && field.value) {
            if (field.value.length < 6) {
                isValid = false;
                errorMessage = 'Password must be at least 6 characters long.';
            }
        }
        
        // Confirm password validation
        else if (field.name === 'confirm_password' && field.value) {
            const passwordField = document.querySelector('input[name="password"]');
            if (passwordField && field.value !== passwordField.value) {
                isValid = false;
                errorMessage = 'Passwords do not match.';
            }
        }
        
        // Age validation
        else if (field.name === 'age' && field.value) {
            const age = parseInt(field.value);
            if (age < 1 || age > 120) {
                isValid = false;
                errorMessage = 'Please enter a valid age between 1 and 120.';
            }
        }

        // Apply validation state
        if (field.value.trim()) {
            field.classList.add(isValid ? 'is-valid' : 'is-invalid');
            if (!isValid) {
                errorContainer.textContent = errorMessage;
                errorContainer.style.display = 'block';
            } else {
                errorContainer.style.display = 'none';
            }
        }

        return isValid;
    }

    function createErrorContainer(fieldContainer) {
        const errorContainer = document.createElement('div');
        errorContainer.className = 'field-error text-danger small mt-1';
        errorContainer.style.display = 'none';
        fieldContainer.appendChild(errorContainer);
        return errorContainer;
    }

    function validateForm(form) {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!validateField({ target: input })) {
                isValid = false;
            }
        });

        return isValid;
    }

    function showFormErrors(form) {
        const firstInvalidField = form.querySelector('.is-invalid');
        if (firstInvalidField) {
            firstInvalidField.focus();
            firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    // Loading States
    function initializeLoadingStates() {
        const submitButtons = document.querySelectorAll('button[type="submit"]');
        submitButtons.forEach(button => {
            const form = button.closest('form');
            if (form) {
                form.addEventListener('submit', function() {
                    showButtonLoading(button);
                });
            }
        });
    }

    function showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.disabled = true;
        button.classList.add('loading');
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        
        // Reset after 10 seconds to prevent permanent loading state
        setTimeout(() => {
            button.disabled = false;
            button.classList.remove('loading');
            button.innerHTML = originalText;
        }, 10000);
    }

    function showLoadingState(form) {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            showButtonLoading(submitButton);
        }
    }

    // Tooltips and Accessibility
    function initializeTooltips() {
        // Initialize Bootstrap tooltips if available
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }

    function initializeAccessibility() {
        // Skip link functionality
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.focus();
                    target.scrollIntoView();
                }
            });
        }

        // Enhanced keyboard navigation
        document.addEventListener('keydown', function(e) {
            // ESC key to close modals
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal.show');
                if (openModal && typeof bootstrap !== 'undefined' && bootstrap.Modal) {
                    const modal = bootstrap.Modal.getInstance(openModal);
                    if (modal) modal.hide();
                }
            }
        });

        // Focus management for modals
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('shown.bs.modal', function() {
                const firstInput = this.querySelector('input, button, select, textarea');
                if (firstInput) firstInput.focus();
            });
        });
    }

    // Alert Management
    function initializeAlerts() {
        // Auto-dismiss alerts after 5 seconds
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(alert => {
            if (!alert.querySelector('.btn-close')) return;
            
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.classList.add('fade');
                    setTimeout(() => {
                        alert.remove();
                    }, 150);
                }
            }, 5000);
        });
    }

    // Mobile Menu
    function initializeMobileMenu() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (navbarToggler && navbarCollapse) {
            // Close mobile menu when clicking outside
            document.addEventListener('click', function(e) {
                if (!navbarToggler.contains(e.target) && !navbarCollapse.contains(e.target)) {
                    if (navbarCollapse.classList.contains('show')) {
                        navbarToggler.click();
                    }
                }
            });

            // Close mobile menu when clicking a nav link
            const navLinks = navbarCollapse.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', function() {
                    if (navbarCollapse.classList.contains('show')) {
                        navbarToggler.click();
                    }
                });
            });
        }
    }

    // Animations
    function initializeAnimations() {
        // Fade in elements on scroll
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

        const animatedElements = document.querySelectorAll('.card, .feature-card, .stat-card');
        animatedElements.forEach(el => {
            observer.observe(el);
        });
    }

    // Symptom Form Specific
    function initializeSymptomForm() {
        const symptomCheckboxes = document.querySelectorAll('input[name="symptoms"]');
        const severityRadios = document.querySelectorAll('input[name="severity"]');
        const submitButton = document.querySelector('button[type="submit"]');

        // Dynamic symptom counter
        const updateSymptomCount = () => {
            const checkedSymptoms = document.querySelectorAll('input[name="symptoms"]:checked');
            const countDisplay = document.querySelector('.symptom-count');
            
            if (countDisplay) {
                countDisplay.textContent = `${checkedSymptoms.length} symptoms selected`;
            }

            // Enable/disable submit button based on selection
            if (submitButton) {
                submitButton.disabled = checkedSymptoms.length === 0;
            }
        };

        symptomCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                updateSymptomCount();
                
                // Visual feedback for selected symptoms
                const label = this.nextElementSibling;
                if (this.checked) {
                    label.classList.add('fw-bold', 'text-primary');
                    this.closest('.form-check').classList.add('selected');
                } else {
                    label.classList.remove('fw-bold', 'text-primary');
                    this.closest('.form-check').classList.remove('selected');
                }
            });
        });

        // Severity selection feedback
        severityRadios.forEach(radio => {
            radio.addEventListener('change', function() {
                // Remove previous selections
                severityRadios.forEach(r => {
                    r.closest('.form-check').classList.remove('severity-selected');
                });
                
                // Highlight current selection
                this.closest('.form-check').classList.add('severity-selected');
            });
        });

        // Initialize counters
        updateSymptomCount();
    }

    // Results Page Specific
    function initializeResults() {
        // Print functionality
        const printButton = document.querySelector('.print-results');
        if (printButton) {
            printButton.addEventListener('click', function() {
                window.print();
            });
        }

        // Smooth scroll to sections
        const sectionLinks = document.querySelectorAll('a[href^="#"]');
        sectionLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    // Dashboard Specific
    function initializeDashboard() {
        // Animate statistics on load
        const statNumbers = document.querySelectorAll('.stat-card h3, .stat-card h4');
        statNumbers.forEach(stat => {
            animateNumber(stat);
        });

        // Quick action shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case 's':
                        e.preventDefault();
                        const symptomLink = document.querySelector('a[href*="symptoms"]');
                        if (symptomLink) symptomLink.click();
                        break;
                    case 'h':
                        e.preventDefault();
                        const historyLink = document.querySelector('a[href*="history"]');
                        if (historyLink) historyLink.click();
                        break;
                }
            }
        });
    }

    function animateNumber(element) {
        const finalNumber = parseInt(element.textContent);
        if (isNaN(finalNumber)) return;

        const duration = 1000;
        const steps = 60;
        const increment = finalNumber / steps;
        let current = 0;
        let step = 0;

        const timer = setInterval(() => {
            current += increment;
            step++;
            
            if (step >= steps) {
                current = finalNumber;
                clearInterval(timer);
            }
            
            element.textContent = Math.floor(current);
        }, duration / steps);
    }

    // Profile Specific
    function initializeProfile() {
        // Password strength indicator
        const passwordInput = document.querySelector('input[type="password"]');
        if (passwordInput) {
            const strengthIndicator = createPasswordStrengthIndicator();
            passwordInput.parentNode.insertBefore(strengthIndicator, passwordInput.nextSibling);

            passwordInput.addEventListener('input', function() {
                updatePasswordStrength(this.value, strengthIndicator);
            });
        }

        // Profile picture preview (if implemented in future)
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', function(e) {
                if (e.target.files && e.target.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const preview = document.querySelector('.profile-preview');
                        if (preview) {
                            preview.src = e.target.result;
                        }
                    };
                    reader.readAsDataURL(e.target.files[0]);
                }
            });
        });
    }

    function createPasswordStrengthIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'password-strength mt-2';
        indicator.innerHTML = `
            <div class="strength-bar">
                <div class="strength-fill"></div>
            </div>
            <div class="strength-text small text-muted">Password strength</div>
        `;
        return indicator;
    }

    function updatePasswordStrength(password, indicator) {
        const strengthFill = indicator.querySelector('.strength-fill');
        const strengthText = indicator.querySelector('.strength-text');
        
        let strength = 0;
        let message = 'Too weak';
        let color = '#dc3545';

        if (password.length >= 6) strength += 20;
        if (password.length >= 8) strength += 20;
        if (/[a-z]/.test(password)) strength += 20;
        if (/[A-Z]/.test(password)) strength += 20;
        if (/[0-9]/.test(password)) strength += 10;
        if (/[^A-Za-z0-9]/.test(password)) strength += 10;

        if (strength >= 80) {
            message = 'Very strong';
            color = '#198754';
        } else if (strength >= 60) {
            message = 'Strong';
            color = '#20c997';
        } else if (strength >= 40) {
            message = 'Moderate';
            color = '#ffc107';
        } else if (strength >= 20) {
            message = 'Weak';
            color = '#fd7e14';
        }

        strengthFill.style.width = strength + '%';
        strengthFill.style.backgroundColor = color;
        strengthText.textContent = message;
        strengthText.style.color = color;
    }

    // History Page Specific
    function initializeHistory() {
        // Search functionality
        const searchInput = document.querySelector('.history-search');
        if (searchInput) {
            searchInput.addEventListener('input', debounce(filterHistory, 300));
        }

        // Sort functionality
        const sortSelect = document.querySelector('.history-sort');
        if (sortSelect) {
            sortSelect.addEventListener('change', sortHistory);
        }
    }

    function filterHistory(e) {
        const searchTerm = e.target.value.toLowerCase();
        const consultationCards = document.querySelectorAll('.consultation-card');
        
        consultationCards.forEach(card => {
            const text = card.textContent.toLowerCase();
            const shouldShow = text.includes(searchTerm);
            
            card.style.display = shouldShow ? 'block' : 'none';
            
            if (shouldShow) {
                card.classList.add('fade-in');
            }
        });
    }

    function sortHistory(e) {
        const sortBy = e.target.value;
        const container = document.querySelector('.consultations-container');
        const cards = Array.from(container.children);
        
        cards.sort((a, b) => {
            switch(sortBy) {
                case 'date-desc':
                    return new Date(b.dataset.date) - new Date(a.dataset.date);
                case 'date-asc':
                    return new Date(a.dataset.date) - new Date(b.dataset.date);
                case 'severity':
                    const severityOrder = { severe: 3, moderate: 2, mild: 1 };
                    return severityOrder[b.dataset.severity] - severityOrder[a.dataset.severity];
                default:
                    return 0;
            }
        });
        
        cards.forEach(card => container.appendChild(card));
    }

    // Utility functions for external use
    window.HealthAssistant = {
        showAlert: function(message, type = 'info') {
            const alertContainer = document.querySelector('.alert-container') || document.body;
            const alert = document.createElement('div');
            alert.className = `alert alert-${type} alert-dismissible fade show`;
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            alertContainer.insertBefore(alert, alertContainer.firstChild);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.classList.remove('show');
                    setTimeout(() => alert.remove(), 150);
                }
            }, 5000);
        },
        
        validateForm: validateForm,
        showLoading: showButtonLoading
    };

    // Error handling
    window.addEventListener('error', function(e) {
        console.error('Application error:', e.error);
        
        // Show user-friendly error message for critical errors
        if (e.error && e.error.name !== 'ChunkLoadError') {
            window.HealthAssistant.showAlert(
                'An unexpected error occurred. Please refresh the page and try again.',
                'danger'
            );
        }
    });

    // Performance monitoring
    window.addEventListener('load', function() {
        // Log page load performance
        if ('performance' in window) {
            const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
            console.log(`Page loaded in ${loadTime}ms`);
        }
    });

})();
