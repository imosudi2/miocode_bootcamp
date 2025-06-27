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
      navbar.classList.toggle('scrolled', window.scrollY > 100);
    }
  });
  
  // === Scroll reveal animation ===
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
    card.addEventListener('mouseenter', () => card.style.transform = 'translateY(-10px) rotateX(5deg)');
    card.addEventListener('mouseleave', () => card.style.transform = 'translateY(0) rotateX(0)');
  });
  
  // === Parallax hero background ===
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.hero-bg');
    if (parallax) {
      parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
  });
  
  // === Dynamic year ===
  document.getElementById("year").textContent = new Date().getFullYear();
  
  // === Form logic ===
  document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');
    const startDate = document.getElementById('startDate');
    const today = new Date().toISOString().split('T')[0];
    if (startDate) startDate.setAttribute('min', today);
  
    updateProgressBar();
  
    if (!form) return;
  
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      hideMessages();
  
      if (!validateForm()) return;
  
      let recaptchaToken = '';
      try {
        recaptchaToken = await grecaptcha.execute(recaptchaSiteKey, { action: 'register' });
      } catch (error) {
        console.error('reCAPTCHA error:', error);
        showError('Security verification failed. Please refresh the page and try again.');
        return;
      }
  
      setLoadingState(true);
      const formData = new FormData(this);
      formData.append('g-recaptcha-response', recaptchaToken);
  
      try {
        const response = await fetch(this.action || window.location.pathname, {
          method: 'POST',
          body: formData
        });
  
        const result = await response.json();
  
        if (result.success) {
          showSuccess('Application submitted successfully! We will contact you soon.');
          this.reset();
          updateProgressBar();
        } else {
          showError(result.message || 'An error occurred. Please try again.');
        }
      } catch (error) {
        console.error('Network error:', error);
        showError('Network error. Please check your connection and try again.');
      } finally {
        setLoadingState(false);
      }
    });
  
    // Real-time progress + validation
    document.querySelectorAll('input, select, textarea').forEach(input => {
      input.addEventListener('input', updateProgressBar);
      input.addEventListener('change', updateProgressBar);
      input.addEventListener('blur', () => {
        if (input.required && !input.value.trim()) {
          setFieldError(input, 'This field is required');
        } else {
          input.classList.remove('is-invalid');
        }
      });
    });
  });
  
  // === Validation and utilities ===
  function validateForm() {
    const requiredFields = [
      'firstName', 'lastName', 'email', 'phone', 'contactMethod',
      'address', 'program', 'schedule', 'startDate', 'education',
      'experience', 'goals', 'payment', 'agreeTerms'
    ];
  
    let isValid = true;
  
    requiredFields.forEach(id => {
      const field = document.getElementById(id);
      if (!field) return;
  
      const value = field.type === 'checkbox' ? field.checked : field.value.trim();
      if (!value) {
        setFieldError(field, 'This field is required');
        isValid = false;
      }
    });
  
    const email = document.getElementById('email');
    if (email && email.value && !isValidEmail(email.value)) {
      setFieldError(email, 'Please enter a valid email address');
      isValid = false;
    }
  
    const phone = document.getElementById('phone');
    if (phone && phone.value && !isValidPhone(phone.value)) {
      setFieldError(phone, 'Please enter a valid phone number');
      isValid = false;
    }
  
    const startDate = document.getElementById('startDate');
    if (startDate && startDate.value) {
      const selected = new Date(startDate.value);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      if (selected < today) {
        setFieldError(startDate, 'Start date cannot be in the past');
        isValid = false;
      }
    }
  
    return isValid;
  }
  
  function setFieldError(field, message) {
    field.classList.add('is-invalid');
    const feedback = field.closest('.form-floating')?.querySelector('.invalid-feedback') ||
                     field.closest('.form-check')?.querySelector('.invalid-feedback');
    if (feedback) feedback.textContent = message;
  }
  
  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
  
  function isValidPhone(phone) {
    const cleaned = phone.replace(/[\s\-\(\)]/g, '');
    return /^(\+\d{10,15}|0\d{9,14}|[1-9]\d{8,14})$/.test(cleaned);
  }
  
  function setLoadingState(loading) {
    const btn = document.getElementById('submitBtn');
    const text = document.getElementById('submitText');
    const spinner = document.getElementById('submitSpinner');
    if (!btn || !text || !spinner) return;
  
    btn.disabled = loading;
    text.classList.toggle('d-none', loading);
    spinner.classList.toggle('d-none', !loading);
  }
  
  function showSuccess(message) {
    const box = document.getElementById('successMessage');
    const text = document.getElementById('successText');
    if (text) text.textContent = message;
    if (box) {
      box.classList.remove('d-none');
      box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
  
  function showError(message) {
    const box = document.getElementById('errorMessage');
    const text = document.getElementById('errorText');
    if (text) text.textContent = message;
    if (box) {
      box.classList.remove('d-none');
      box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
  
  function hideMessages() {
    document.getElementById('successMessage')?.classList.add('d-none');
    document.getElementById('errorMessage')?.classList.add('d-none');
  }
  
  function updateProgressBar() {
    const bar = document.getElementById('formProgressBar');
    const submit = document.getElementById('submitBtn');
    if (!bar) return;
  
    const fields = [
      'firstName', 'lastName', 'email', 'phone', 'contactMethod',
      'address', 'program', 'schedule', 'startDate', 'education',
      'experience', 'goals', 'payment', 'agreeTerms'
    ];
  
    let completed = 0;
  
    fields.forEach(id => {
      const field = document.getElementById(id);
      if (!field) return;
  
      let isFilled = false;
  
      if (field.type === 'checkbox') {
        isFilled = field.checked;
      } else if (field.tagName === 'SELECT') {
        isFilled = field.value !== '';
      } else {
        isFilled = field.value.trim() !== '';
        if (id === 'email') isFilled = isValidEmail(field.value);
        if (id === 'phone') isFilled = isValidPhone(field.value);
        if (id === 'startDate') {
          const selected = new Date(field.value);
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          isFilled = selected >= today;
        }
      }
  
      if (isFilled) completed++;
    });
  
    const percentage = Math.round((completed / fields.length) * 100);
    bar.style.width = `${percentage}%`;
    bar.setAttribute('aria-valuenow', percentage);
  
    if (submit) submit.disabled = percentage < 100;
  
    bar.className = 'progress-bar';
    bar.classList.add(
      percentage >= 100 ? 'bg-success' :
      percentage >= 75 ? 'bg-info' :
      percentage >= 50 ? 'bg-warning' : 'bg-primary'
    );
  }
  