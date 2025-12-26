// Password strength checker
const passwordInput = document.getElementById("password");
const strengthBar = document.getElementById("strengthBar");
const strengthText = document.getElementById("strengthText");
const strengthContainer = document.getElementById("strengthContainer");

if (passwordInput) {
  passwordInput.addEventListener("input", () => {
    const password = passwordInput.value;
    const strength = calculateStrength(password);
    updateStrengthBar(strength);
  });
}

function calculateStrength(password) {
  let strength = 0;

  // Length checks
  if (password.length >= 8) strength++;
  if (password.length >= 12) strength++;
  if (password.length >= 16) strength++;

  // Character type checks
  if (/[a-z]/.test(password)) strength++;
  if (/[A-Z]/.test(password)) strength++;
  if (/[0-9]/.test(password)) strength++;
  if (/[^a-zA-Z0-9]/.test(password)) strength++;

  return strength;
}

function updateStrengthBar(strength) {
  let color = "";
  let text = "";
  let percentage = (strength / 7) * 100;

  if (strength === 0) {
    strengthContainer.style.display = "none";
    return;
  } else if (strength <= 2) {
    color = "bg-danger";
    text = "Weak";
  } else if (strength <= 4) {
    color = "bg-warning";
    text = "Fair";
  } else if (strength <= 5) {
    color = "bg-info";
    text = "Good";
  } else if (strength <= 6) {
    color = "bg-success";
    text = "Strong";
  } else {
    color = "bg-success";
    text = "Very Strong";
  }

  strengthContainer.style.display = "block";
  strengthBar.className = `progress-bar ${color}`;
  strengthBar.style.width = percentage + "%";
  strengthText.textContent = text;
}
