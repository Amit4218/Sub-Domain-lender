const showButton = document.getElementById("show-form");
const form = document.getElementById("add-record-form");
const overlay = document.getElementById("modal-overlay");
const closeButton = document.getElementById("close-form");
const dashboardErrorElement = document.getElementById("error");
const copyright = document.getElementById("copyright");

function openForm() {
  form.classList.remove("hidden");
  overlay.classList.remove("hidden");
}

function closeForm() {
  form.classList.add("hidden");
  overlay.classList.add("hidden");
}

if (showButton) {
  showButton.addEventListener("click", openForm);
}

if (closeButton) {
  closeButton.addEventListener("click", closeForm);
}

if (overlay) {
  overlay.addEventListener("click", closeForm);
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeForm();
  }
});

if (dashboardErrorElement) {
  dashboardErrorElement.addEventListener("click", () => {
    dashboardErrorElement.classList.add("hidden");
  });
}

if (copyright) {
  copyright.textContent = `© ${new Date().getFullYear()} Amit Bhagat. All rights reserved.`;
}
