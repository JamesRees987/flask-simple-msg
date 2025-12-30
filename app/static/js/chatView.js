// Auto-resize textarea as user types
const textarea = document.getElementById("messageInput");
textarea.addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";
});

// Allow Enter to send, Shift+Enter for new line
textarea.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    document.getElementById("messageForm").dispatchEvent(new Event("submit"));
  }
});

// Auto-scroll to bottom on page load
function scrollToBottom() {
  const messagesContainer = document.getElementById("messagesContainer");
  if (messagesContainer) {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
}

// Call on page load
scrollToBottom();
