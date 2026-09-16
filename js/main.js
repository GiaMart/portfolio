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

function initGalleryLightbox() {
  const triggers = document.querySelectorAll("[data-lightbox-src]");
  if (!triggers.length) return;

  let overlay = document.getElementById("gallery-lightbox");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "gallery-lightbox";
    overlay.className = "gallery-lightbox";
    overlay.hidden = true;
    overlay.innerHTML = `
      <button type="button" class="gallery-lightbox-close" aria-label="Close">×</button>
      <figure class="gallery-lightbox-figure">
        <img class="gallery-lightbox-image" alt="">
        <figcaption class="gallery-lightbox-caption"></figcaption>
      </figure>`;
    document.body.appendChild(overlay);
  }

  const image = overlay.querySelector(".gallery-lightbox-image");
  const caption = overlay.querySelector(".gallery-lightbox-caption");
  const closeBtn = overlay.querySelector(".gallery-lightbox-close");

  const closeLightbox = () => {
    overlay.hidden = true;
    document.body.classList.remove("lightbox-open");
  };

  const openLightbox = (src, label) => {
    image.src = src;
    image.alt = label;
    if (label) {
      caption.textContent = label;
      caption.hidden = false;
    } else {
      caption.textContent = "";
      caption.hidden = true;
    }
    overlay.hidden = false;
    document.body.classList.add("lightbox-open");
    closeBtn.focus();
  };

  triggers.forEach((trigger) => {
    trigger.addEventListener("click", () => {
      openLightbox(trigger.dataset.lightboxSrc, trigger.dataset.lightboxCaption || "");
    });
  });

  closeBtn.addEventListener("click", closeLightbox);
  overlay.addEventListener("click", (event) => {
    if (event.target === overlay) closeLightbox();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !overlay.hidden) closeLightbox();
  });
}

initGalleryLightbox();
