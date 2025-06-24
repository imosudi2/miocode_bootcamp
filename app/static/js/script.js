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
  if (window.scrollY > 100) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
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
  card.addEventListener('mouseenter', function () {
    this.style.transform = 'translateY(-10px) rotateX(5deg)';
  });

  card.addEventListener('mouseleave', function () {
    this.style.transform = 'translateY(0) rotateX(0)';
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

// === Update year dynamically ===
document.getElementById("year").textContent = new Date().getFullYear();

// === Registration Form Enhancements ===
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("studentRegistration");
  const submitButton = document.getElementById("submitButton");
  const spinner = document.getElementById("loadingSpinner");
  const startDate = document.getElementById("startDate");
  const progressBar = document.getElementById("formProgressBar");

  // Set future-only constraint on date
  const today = new Date().toISOString().split("T")[0];
  startDate.setAttribute("min", today);

  // Live progress bar
  form.addEventListener("input", () => {
    const visibleFields = [...form.querySelectorAll("input, select, textarea")].filter(
      el => el.type !== "hidden" && el.offsetParent !== null
    );
    const validFields = visibleFields.filter(el => el.checkValidity());
    const percentage = Math.round((validFields.length / visibleFields.length) * 100);
    progressBar.style.width = `${percentage}%`;
    progressBar.setAttribute("aria-valuenow", percentage);

    submitButton.disabled = !form.checkValidity();
  });

  // Bootstrap validation & reCAPTCHA integration
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (!form.checkValidity()) {
      form.classList.add("was-validated");
      return;
    }

    // Disable submit, show spinner
    submitButton.disabled = true;
    spinner.classList.remove("d-none");

    // Execute reCAPTCHA v2 invisible
    grecaptcha.execute();
  });
});

// === Called by reCAPTCHA after successful challenge ===
function onSubmit(token) {
  const form = document.getElementById("studentRegistration");
  const formData = new FormData(form);
  const spinner = document.getElementById("loadingSpinner");
  const submitButton = document.getElementById("submitButton");

  // Append token for server verification
  formData.append("g-recaptcha-response", token);

  // Simulate form submission (replace with actual API call)
  setTimeout(() => {
    // Show confirmation modal
    const modal = new bootstrap.Modal(document.getElementById("confirmationModal"));
    modal.show();

    // Reset form & UI
    form.reset();
    form.classList.remove("was-validated");
    document.getElementById("formProgressBar").style.width = "0%";
    submitButton.disabled = true;
    spinner.classList.add("d-none");
    grecaptcha.reset();
  }, 1000);
}

// === Enable submit button after CAPTCHA ===
function enableSubmit(response) {
  document.getElementById('submitButton').disabled = false;
}

// === Initialize reCAPTCHA (Invisible) ===
document.addEventListener("DOMContentLoaded", function () {
  grecaptcha.ready(function () {
    grecaptcha.render('submitButton', {
      sitekey: '{{recaptcha_site_key}}',//'6LeFlWkrAAAAAGWAysVIcK9ZhvksD--q_hNW1BrO',
      callback: 'onSubmit',
      size: 'invisible'
    });
  });
});

