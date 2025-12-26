// Dark mode toggle functionality
const darkModeToggle = document.getElementById("darkModeToggle");
const htmlElement = document.documentElement;
const mainNavbar = document.getElementById("mainNavbar");

// Check localStorage for saved theme preference
const savedTheme = localStorage.getItem("theme") || "light";
htmlElement.setAttribute("data-bs-theme", savedTheme);
updateToggleIcon(savedTheme);
updateNavbarStyle(savedTheme);

// Toggle dark mode on button click
darkModeToggle.addEventListener("click", () => {
  const currentTheme = htmlElement.getAttribute("data-bs-theme");
  const newTheme = currentTheme === "light" ? "dark" : "light";

  htmlElement.setAttribute("data-bs-theme", newTheme);
  localStorage.setItem("theme", newTheme);
  updateToggleIcon(newTheme);
  updateNavbarStyle(newTheme);
});

// Update button icon based on theme
function updateToggleIcon(theme) {
  const icon = darkModeToggle.querySelector("i");
  if (theme === "dark") {
    icon.classList.remove("bi-moon-fill");
    icon.classList.add("bi-sun-fill");
  } else {
    icon.classList.remove("bi-sun-fill");
    icon.classList.add("bi-moon-fill");
  }
}

// Update navbar styling based on theme
function updateNavbarStyle(theme) {
  if (theme === "dark") {
    // In dark mode, make navbar slightly darker
    mainNavbar.style.backgroundColor = "#0a0e27";
  } else {
    // In light mode, use the default dark background
    mainNavbar.style.backgroundColor = "";
  }
}
