// Sign-up page client-side validation
const signUpForm = document.querySelector("form[action]");
const password = document.getElementById("password");
const confirmPassword = document.getElementById("confirm-password");
const email = document.getElementById("email");
const clientAlertContainer = document.getElementById("clientAlertContainer");
const matchFeedback = document.getElementById("matchFeedback");

function showAlert(message, type = "danger", timeout = 5000) {
  if (!clientAlertContainer) return;
  clientAlertContainer.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`;

  if (timeout) {
    setTimeout(() => {
      const alert = clientAlertContainer.querySelector(".alert");
      if (alert) {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      }
    }, timeout);
  }
}

function showEmailToast(message) {
  // Deprecated: we now use showAlert() for consistent messaging.
  showAlert(message, "warning");
}

function validateEmailFormat(emailValue) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(emailValue).toLowerCase());
}

if (confirmPassword && password && matchFeedback) {
  confirmPassword.addEventListener("input", () => {
    if (confirmPassword.value === "") {
      matchFeedback.style.display = "none";
      return;
    }

    if (password.value === confirmPassword.value) {
      matchFeedback.textContent = "Passwords match";
      matchFeedback.classList.remove("text-danger");
      matchFeedback.classList.add("text-success");
      matchFeedback.style.display = "block";
    } else {
      matchFeedback.textContent = "Passwords do not match";
      matchFeedback.classList.remove("text-success");
      matchFeedback.classList.add("text-danger");
      matchFeedback.style.display = "block";
    }
  });
}

if (signUpForm) {
  signUpForm.addEventListener("submit", (e) => {
    // Clear previous client alert
    if (clientAlertContainer) clientAlertContainer.innerHTML = "";

    let hasError = false;

    // Collect validation errors to present as a single alert
    const errors = [];

    if (email && !validateEmailFormat(email.value)) {
      errors.push("Please enter a valid email address.");
    }

    if (
      password &&
      confirmPassword &&
      password.value !== confirmPassword.value
    ) {
      errors.push("Passwords do not match.");
    }

    // Password strength check (require at least "Good")
    const requiredStrength = 5; // require >=5 (Good)
    let strength = null;
    if (typeof calculateStrength === "function") {
      strength = calculateStrength(password ? password.value : "");
    } else {
      // fallback coarse check
      const pw = password ? password.value : "";
      strength = 0;
      if (pw.length >= 8) strength++;
      if (/[A-Z]/.test(pw)) strength++;
      if (/[0-9]/.test(pw)) strength++;
      if (/[^a-zA-Z0-9]/.test(pw)) strength++;
      strength = Math.min(7, strength + (pw.length >= 12 ? 1 : 0));
    }

    if (password && strength !== null && strength < requiredStrength) {
      errors.push("Password strength must be at least 'Good'.");
    }

    if (errors.length > 0) {
      e.preventDefault();
      showAlert(errors.join("<br>"), "danger");
      hasError = true;
      // focus first invalid field
      if (email && !validateEmailFormat(email.value)) {
        email.focus();
      } else if (
        password &&
        confirmPassword &&
        password.value !== confirmPassword.value
      ) {
        confirmPassword.focus();
      } else if (password && strength !== null && strength < requiredStrength) {
        password.focus();
      }
    }

    if (hasError) {
      // Focus first invalid field
      if (
        password &&
        confirmPassword &&
        password.value !== confirmPassword.value
      ) {
        confirmPassword.focus();
      } else if (email && !validateEmailFormat(email.value)) {
        email.focus();
      }
    }
  });
}
