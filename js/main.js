// Mobile nav closes on link click
document.querySelectorAll(".site-nav a").forEach((link) => {
  link.addEventListener("click", () => {
    document.body.classList.remove("nav-open");
  });
});

// Contact form success message after Formspree redirect
if (new URLSearchParams(window.location.search).get("sent") === "1") {
  const success = document.getElementById("form-success");
  if (success) {
    success.hidden = false;
    success.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}
