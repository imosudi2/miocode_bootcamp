//script.js
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
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

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
      const navbar = document.getElementById('navbar');
      if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });

    // Scroll reveal animation
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

    document.querySelectorAll('.scroll-reveal').forEach(el => {
      observer.observe(el);
    });

    // Add floating animation to cards on hover
    document.querySelectorAll('.card').forEach(card => {
      card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-10px) rotateX(5deg)';
      });
      
      card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0) rotateX(0)';
      });
    });

    // Parallax effect for hero background
    window.addEventListener('scroll', () => {
      const scrolled = window.pageYOffset;
      const parallax = document.querySelector('.hero-bg');
      if (parallax) {
        parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
      }
    });
  document.getElementById("year").textContent = new Date().getFullYear();
// reCAPTCHA functions
function enableSubmit(response) {
  document.getElementById('submitButton').disabled = false;
}

// Modified form submission handler
document.getElementById('studentRegistration').addEventListener('submit', function(e) {
  e.preventDefault();
  
  if (!this.checkValidity()) {
    this.classList.add('was-validated');
    return;
  }
  
  // Execute reCAPTCHA
  grecaptcha.execute();
});

// This function will be called when reCAPTCHA verifies the user
function onSubmit(token) {
  const form = document.getElementById('studentRegistration');
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  
  // Add the reCAPTCHA token to your form data
  data['g-recaptcha-response'] = token;
  
  console.log('Form submitted with CAPTCHA:', data);
  
  // In a real application, you would send this to your server
  // for verification and processing
  alert('Application submitted successfully! We will contact you shortly.');
  form.reset();
  form.classList.remove('was-validated');
  
  // Reset the submit button
  document.getElementById('submitButton').disabled = true;
  
  // Reset reCAPTCHA
  grecaptcha.reset();
}

// Initialize reCAPTCHA
document.addEventListener('DOMContentLoaded', function() {
  // Set your site key here (you'll get this from Google)
  // grecaptcha.ready(function() {
  //   grecaptcha.render('submitButton', {
  //     'sitekey': 'YOUR_SITE_KEY',
  //     'callback': 'onSubmit'
  //   });
  // });
});

