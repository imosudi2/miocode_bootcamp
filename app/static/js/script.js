//script.js
// === Smooth scrolling for anchor links ===
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// === Navbar scroll effect ===
window.addEventListener('scroll', () => {
  const navbar = document.getElementById('navbar');
  if (navbar) {
    if (window.scrollY > 100) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }
});

// === Scroll reveal ===
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('revealed');
    }
  });
}, observerOptions);

document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));

// === Card hover animation ===
document.querySelectorAll('.card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    card.style.transform = 'translateY(-10px) rotateX(5deg)';
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'translateY(0) rotateX(0)';
  });
});

// === Parallax effect on hero background ===
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  const parallax = document.querySelector('.hero-bg');
  if (parallax) {
    parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
  }
});

// === Dynamic year for footer ===
document.getElementById("year").textContent = new Date().getFullYear();


    // reCAPTCHA v3 Site Key - Replace with your actual key
        const RECAPTCHA_SITE_KEY = recaptchaSiteKey;

        // Set minimum date to today
        document.addEventListener('DOMContentLoaded', function() {
            const today = new Date().toISOString().split('T')[0];
            document.getElementById('startDate').setAttribute('min', today);
            
            // Initialize progress bar
            updateProgressBar();
        });

        // Form validation and submission
        document.getElementById('registrationForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Reset previous messages
            hideMessages();
            
            // Validate form
            if (!validateForm()) {
                return;
            }
            
            // Execute reCAPTCHA v3
            let recaptchaToken = '';
            try {
                recaptchaToken = await grecaptcha.execute(RECAPTCHA_SITE_KEY, {action: 'register'});
            } catch (error) {
                console.error('reCAPTCHA error:', error);
                showError('Security verification failed. Please refresh the page and try again.');
                return;
            }
            
            // Show loading state
            setLoadingState(true);
            
            // Prepare form data
            const formData = new FormData(this);
            formData.append('g-recaptcha-response', recaptchaToken);
            
            try {
                const response = await fetch('/', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showSuccess('Application submitted successfully! We will contact you soon.');
                    this.reset();
                    updateProgressBar(); // Reset progress bar after form reset
                } else {
                    showError(result.message || 'An error occurred. Please try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('Network error. Please check your connection and try again.');
            } finally {
                setLoadingState(false);
            }
        });

        function validateForm() {
            const form = document.getElementById('registrationForm');
            let isValid = true;
            
            // Clear previous validation
            form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
            
            // Required fields validation
            const requiredFields = [
                'firstName', 'lastName', 'email', 'phone', 'contactMethod', 
                'address', 'program', 'schedule', 'startDate', 'education', 
                'experience', 'goals', 'payment'
            ];
            
            requiredFields.forEach(fieldName => {
                const field = document.getElementById(fieldName);
                if (!field.value.trim()) {
                    setFieldError(field, 'This field is required');
                    isValid = false;
                }
            });
            
            // Email validation
            const email = document.getElementById('email');
            if (email.value && !isValidEmail(email.value)) {
                setFieldError(email, 'Please enter a valid email address');
                isValid = false;
            }
            
            // Phone validation
            const phone = document.getElementById('phone');
            if (phone.value && !isValidPhone(phone.value)) {
                setFieldError(phone, 'Please enter a valid phone number');
                isValid = false;
            }
            
            // Terms checkbox validation
            const agreeTerms = document.getElementById('agreeTerms');
            if (!agreeTerms.checked) {
                setFieldError(agreeTerms, 'You must agree to the terms and conditions');
                isValid = false;
            }
            
            // Date validation
            const startDate = document.getElementById('startDate');
            if (startDate.value) {
                const selectedDate = new Date(startDate.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                if (selectedDate < today) {
                    setFieldError(startDate, 'Start date cannot be in the past');
                    isValid = false;
                }
            }
            
            return isValid;
        }

        function setFieldError(field, message) {
            field.classList.add('is-invalid');
            const feedback = field.parentElement.querySelector('.invalid-feedback') || 
                        field.parentElement.parentElement.querySelector('.invalid-feedback');
            if (feedback) {
                feedback.textContent = message;
            }
        }

        function isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        function isValidPhone(phone) {
            // Remove spaces, hyphens, and parentheses
            const cleanedPhone = phone.replace(/[\s\-\(\)]/g, '');

            // Regex to match:
            // 1. + followed by digits (e.g., +2348098674598)
            // 2. Starts with 0 and more digits (e.g., 08098673498)
            // 3. Starts with non-zero digit (e.g., 8098673498)
            const phoneRegex = /^(\+\d{10,15}|0\d{9,14}|[1-9]\d{8,14})$/;
            
            return phoneRegex.test(cleanedPhone);
        }

        function setLoadingState(loading) {
            const submitBtn = document.getElementById('submitBtn');
            const submitText = document.getElementById('submitText');
            const submitSpinner = document.getElementById('submitSpinner');
            
            if (loading) {
                submitBtn.disabled = true;
                submitText.classList.add('d-none');
                submitSpinner.classList.remove('d-none');
            } else {
                submitBtn.disabled = false;
                submitText.classList.remove('d-none');
                submitSpinner.classList.add('d-none');
            }
        }

        function showSuccess(message) {
            const successDiv = document.getElementById('successMessage');
            const successText = document.getElementById('successText');
            successText.textContent = message;
            successDiv.classList.remove('d-none');
            successDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            const errorText = document.getElementById('errorText');
            errorText.textContent = message;
            errorDiv.classList.remove('d-none');
            errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        function hideMessages() {
            document.getElementById('successMessage').classList.add('d-none');
            document.getElementById('errorMessage').classList.add('d-none');
        }

        // Progress bar update function
        function updateProgressBar() {
            const form = document.getElementById('registrationForm');
            const progressBar = document.getElementById('formProgressBar');
            const submitBtn = document.getElementById('submitBtn');
            
            if (!form || !progressBar) return;
            
            // Define all required fields that count towards progress
            const requiredFields = [
                'firstName', 'lastName', 'email', 'phone', 'contactMethod', 
                'address', 'program', 'schedule', 'startDate', 'education', 
                'experience', 'goals', 'payment', 'agreeTerms'
            ];
            
            let completedFields = 0;
            let totalFields = requiredFields.length;
            
            requiredFields.forEach(fieldName => {
                const field = document.getElementById(fieldName);
                if (field) {
                    let isCompleted = false;
                    
                    if (field.type === 'checkbox') {
                        isCompleted = field.checked;
                    } else if (field.tagName === 'SELECT') {
                        isCompleted = field.value !== '';
                    } else {
                        isCompleted = field.value.trim() !== '';
                        
                        // Additional validation for email and phone
                        if (fieldName === 'email' && isCompleted) {
                            isCompleted = isValidEmail(field.value);
                        } else if (fieldName === 'phone' && isCompleted) {
                            isCompleted = isValidPhone(field.value);
                        } else if (fieldName === 'startDate' && isCompleted) {
                            const selectedDate = new Date(field.value);
                            const today = new Date();
                            today.setHours(0, 0, 0, 0);
                            isCompleted = selectedDate >= today;
                        }
                    }
                    
                    if (isCompleted) {
                        completedFields++;
                    }
                }
            });
            
            const percentage = Math.round((completedFields / totalFields) * 100);
            progressBar.style.width = `${percentage}%`;
            progressBar.setAttribute('aria-valuenow', percentage);
            
            // Enable/disable submit button based on completion
            if (submitBtn) {
                submitBtn.disabled = percentage < 100;
            }
            
            // Add visual feedback based on progress
            progressBar.className = 'progress-bar';
            if (percentage >= 100) {
                progressBar.classList.add('bg-success');
            } else if (percentage >= 75) {
                progressBar.classList.add('bg-info');
            } else if (percentage >= 50) {
                progressBar.classList.add('bg-warning');
            } else {
                progressBar.classList.add('bg-primary');
            }
        }

        // Real-time validation feedback and progress update
        document.querySelectorAll('input, select, textarea').forEach(input => {
            // Update progress on any input change
            input.addEventListener('input', updateProgressBar);
            input.addEventListener('change', updateProgressBar);
            
            input.addEventListener('blur', function() {
                if (this.hasAttribute('required') && !this.value.trim()) {
                    setFieldError(this, 'This field is required');
                } else {
                    this.classList.remove('is-invalid');
                }
                updateProgressBar();
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid') && this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
                updateProgressBar();
            });
        });

        // Special validation for email and phone on input
        document.getElementById('email').addEventListener('input', function() {
            if (this.value && !isValidEmail(this.value)) {
                setFieldError(this, 'Please enter a valid email address');
            } else if (this.value) {
                this.classList.remove('is-invalid');
            }
            updateProgressBar();
        });

        document.getElementById('phone').addEventListener('input', function() {
            if (this.value && !isValidPhone(this.value)) {
                setFieldError(this, 'Please enter a valid phone number');
            } else if (this.value) {
                this.classList.remove('is-invalid');
            }
            updateProgressBar();
        });

        
    // reCAPTCHA v3 Site Key - Replace with your actual key
    //const RECAPTCHA_SITE_KEY = '{{recaptcha_site_key}}';

    // Set minimum date to today
    document.addEventListener('DOMContentLoaded', function() {
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('startDate').setAttribute('min', today);
        
        // Initialize progress bar
        updateProgressBar();
    });

    // Form validation and submission
    document.getElementById('registrationForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset previous messages
        hideMessages();
        
        // Validate form
        if (!validateForm()) {
            return;
        }
        
        // Execute reCAPTCHA v3
        let recaptchaToken = '';
        try {
            recaptchaToken = await grecaptcha.execute(RECAPTCHA_SITE_KEY, {action: 'register'});
        } catch (error) {
            console.error('reCAPTCHA error:', error);
            showError('Security verification failed. Please refresh the page and try again.');
            return;
        }
        
        // Show loading state
        setLoadingState(true);
        
        // Prepare form data
        const formData = new FormData(this);
        formData.append('g-recaptcha-response', recaptchaToken);
        
        try {
            const response = await fetch('/', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                showSuccess('Application submitted successfully! We will contact you soon.');
                this.reset();
                updateProgressBar(); // Reset progress bar after form reset
            } else {
                showError(result.message || 'An error occurred. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            setLoadingState(false);
        }
    });

    function validateForm() {
        const form = document.getElementById('registrationForm');
        let isValid = true;
        
        // Clear previous validation
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        
        // Required fields validation
        const requiredFields = [
            'firstName', 'lastName', 'email', 'phone', 'contactMethod', 
            'address', 'program', 'schedule', 'startDate', 'education', 
            'experience', 'goals', 'payment'
        ];
        
        requiredFields.forEach(fieldName => {
            const field = document.getElementById(fieldName);
            if (!field.value.trim()) {
                setFieldError(field, 'This field is required');
                isValid = false;
            }
        });
        
        // Email validation
        const email = document.getElementById('email');
        if (email.value && !isValidEmail(email.value)) {
            setFieldError(email, 'Please enter a valid email address');
            isValid = false;
        }
        
        // Phone validation
        const phone = document.getElementById('phone');
        if (phone.value && !isValidPhone(phone.value)) {
            setFieldError(phone, 'Please enter a valid phone number');
            isValid = false;
        }
        
        // Terms checkbox validation
        const agreeTerms = document.getElementById('agreeTerms');
        if (!agreeTerms.checked) {
            setFieldError(agreeTerms, 'You must agree to the terms and conditions');
            isValid = false;
        }
        
        // Date validation
        const startDate = document.getElementById('startDate');
        if (startDate.value) {
            const selectedDate = new Date(startDate.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                setFieldError(startDate, 'Start date cannot be in the past');
                isValid = false;
            }
        }
        
        return isValid;
    }

    function setFieldError(field, message) {
        field.classList.add('is-invalid');
        const feedback = field.parentElement.querySelector('.invalid-feedback') || 
                    field.parentElement.parentElement.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.textContent = message;
        }
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPhone(phone) {
        // Remove spaces, hyphens, and parentheses
        const cleanedPhone = phone.replace(/[\s\-\(\)]/g, '');

        // Regex to match:
        // 1. + followed by digits (e.g., +2348098674598)
        // 2. Starts with 0 and more digits (e.g., 08098673498)
        // 3. Starts with non-zero digit (e.g., 8098673498)
        const phoneRegex = /^(\+\d{10,15}|0\d{9,14}|[1-9]\d{8,14})$/;
        
        return phoneRegex.test(cleanedPhone);
    }

    function setLoadingState(loading) {
        const submitBtn = document.getElementById('submitBtn');
        const submitText = document.getElementById('submitText');
        const submitSpinner = document.getElementById('submitSpinner');
        
        if (loading) {
            submitBtn.disabled = true;
            submitText.classList.add('d-none');
            submitSpinner.classList.remove('d-none');
        } else {
            submitBtn.disabled = false;
            submitText.classList.remove('d-none');
            submitSpinner.classList.add('d-none');
        }
    }

    function showSuccess(message) {
        const successDiv = document.getElementById('successMessage');
        const successText = document.getElementById('successText');
        successText.textContent = message;
        successDiv.classList.remove('d-none');
        successDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        const errorText = document.getElementById('errorText');
        errorText.textContent = message;
        errorDiv.classList.remove('d-none');
        errorDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideMessages() {
        document.getElementById('successMessage').classList.add('d-none');
        document.getElementById('errorMessage').classList.add('d-none');
    }

    // Progress bar update function
    function updateProgressBar() {
        const form = document.getElementById('registrationForm');
        const progressBar = document.getElementById('formProgressBar');
        const submitBtn = document.getElementById('submitBtn');
        
        if (!form || !progressBar) return;
        
        // Define all required fields that count towards progress
        const requiredFields = [
            'firstName', 'lastName', 'email', 'phone', 'contactMethod', 
            'address', 'program', 'schedule', 'startDate', 'education', 
            'experience', 'goals', 'payment', 'agreeTerms'
        ];
        
        let completedFields = 0;
        let totalFields = requiredFields.length;
        
        requiredFields.forEach(fieldName => {
            const field = document.getElementById(fieldName);
            if (field) {
                let isCompleted = false;
                
                if (field.type === 'checkbox') {
                    isCompleted = field.checked;
                } else if (field.tagName === 'SELECT') {
                    isCompleted = field.value !== '';
                } else {
                    isCompleted = field.value.trim() !== '';
                    
                    // Additional validation for email and phone
                    if (fieldName === 'email' && isCompleted) {
                        isCompleted = isValidEmail(field.value);
                    } else if (fieldName === 'phone' && isCompleted) {
                        isCompleted = isValidPhone(field.value);
                    } else if (fieldName === 'startDate' && isCompleted) {
                        const selectedDate = new Date(field.value);
                        const today = new Date();
                        today.setHours(0, 0, 0, 0);
                        isCompleted = selectedDate >= today;
                    }
                }
                
                if (isCompleted) {
                    completedFields++;
                }
            }
        });
        
        const percentage = Math.round((completedFields / totalFields) * 100);
        progressBar.style.width = `${percentage}%`;
        progressBar.setAttribute('aria-valuenow', percentage);
        
        // Enable/disable submit button based on completion
        if (submitBtn) {
            submitBtn.disabled = percentage < 100;
        }
        
        // Add visual feedback based on progress
        progressBar.className = 'progress-bar';
        if (percentage >= 100) {
            progressBar.classList.add('bg-success');
        } else if (percentage >= 75) {
            progressBar.classList.add('bg-info');
        } else if (percentage >= 50) {
            progressBar.classList.add('bg-warning');
        } else {
            progressBar.classList.add('bg-primary');
        }
    }

    // Real-time validation feedback and progress update
    document.querySelectorAll('input, select, textarea').forEach(input => {
        // Update progress on any input change
        input.addEventListener('input', updateProgressBar);
        input.addEventListener('change', updateProgressBar);
        
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                setFieldError(this, 'This field is required');
            } else {
                this.classList.remove('is-invalid');
            }
            updateProgressBar();
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') && this.value.trim()) {
                this.classList.remove('is-invalid');
            }
            updateProgressBar();
        });
    });

    // Special validation for email and phone on input
    document.getElementById('email').addEventListener('input', function() {
        if (this.value && !isValidEmail(this.value)) {
            setFieldError(this, 'Please enter a valid email address');
        } else if (this.value) {
            this.classList.remove('is-invalid');
        }
        updateProgressBar();
    });

    document.getElementById('phone').addEventListener('input', function() {
        if (this.value && !isValidPhone(this.value)) {
            setFieldError(this, 'Please enter a valid phone number');
        } else if (this.value) {
            this.classList.remove('is-invalid');
        }
        updateProgressBar();
    });

    // Update progress when checkbox is clicked
    document.getElementById('agreeTerms').addEventListener('change', updateProgressBar);

  

