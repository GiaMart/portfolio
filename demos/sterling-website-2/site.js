const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.getAttribute("data-open") === "true";
    nav.setAttribute("data-open", String(!open));
    toggle.setAttribute("aria-expanded", String(!open));
    toggle.textContent = open ? "Menu" : "Close";
  });
  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      nav.setAttribute("data-open", "false");
      toggle.setAttribute("aria-expanded", "false");
      toggle.textContent = "Menu";
    });
  });
}

document.querySelectorAll("[data-slider]").forEach((slider) => {
  const track = slider.querySelector(".slider-track");
  const viewport = slider.querySelector(".slider-viewport");
  const slides = [...track.querySelectorAll(".slider-slide")];
  const gap = 4;
  let index = 0;

  const offsetFor = (i) => {
    let offset = 0;
    for (let n = 0; n < i; n += 1) offset += slides[n].offsetWidth + gap;
    return offset;
  };
  const limit = () => Math.max(0, track.scrollWidth - viewport.clientWidth);
  const place = () => {
    track.style.transform = "translateX(-" + Math.min(offsetFor(index), limit()) + "px)";
  };
  const show = (next) => {
    const atEnd = offsetFor(index) >= limit() - 2;
    if (next > index && atEnd) index = 0;
    else if (next < 0) index = slides.length - 1;
    else index = Math.max(0, Math.min(next, slides.length - 1));
    place();
  };

  slider.querySelector(".prev").addEventListener("click", () => show(index - 1));
  slider.querySelector(".next").addEventListener("click", () => show(index + 1));
  slider.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") show(index - 1);
    if (event.key === "ArrowRight") show(index + 1);
  });
  slides.forEach((slide) => slide.addEventListener("load", place));
  window.addEventListener("resize", place);
  place();
});

const fieldGrid = document.querySelector(".field-grid");
if (fieldGrid) {
  const shots = [...fieldGrid.querySelectorAll(".field-open")];
  const box = document.createElement("div");
  box.className = "lightbox";
  box.hidden = true;
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-modal", "true");
  box.setAttribute("aria-label", "Enlarged photo");
  box.innerHTML = '<button type="button" class="lightbox-close">Close</button><button type="button" class="lightbox-prev" aria-label="Previous photo">‹</button><img alt=""><button type="button" class="lightbox-next" aria-label="Next photo">›</button>';
  document.body.appendChild(box);
  const full = box.querySelector("img");
  let current = 0;
  let lastFocus = null;

  const show = (index) => {
    current = (index + shots.length) % shots.length;
    const source = shots[current].querySelector("img");
    full.src = source.currentSrc || source.src;
    full.alt = (shots[current].getAttribute("aria-label") || "").replace(/^Enlarge photo:\s*/, "");
    box.hidden = false;
    document.body.classList.add("lightbox-open");
  };
  const close = () => {
    box.hidden = true;
    full.removeAttribute("src");
    document.body.classList.remove("lightbox-open");
    if (lastFocus) lastFocus.focus();
  };

  shots.forEach((shot, index) => {
    shot.addEventListener("click", () => {
      lastFocus = shot;
      show(index);
    });
  });
  box.querySelector(".lightbox-close").addEventListener("click", close);
  box.querySelector(".lightbox-prev").addEventListener("click", () => show(current - 1));
  box.querySelector(".lightbox-next").addEventListener("click", () => show(current + 1));
  box.addEventListener("click", (event) => {
    if (event.target === box) close();
  });
  document.addEventListener("keydown", (event) => {
    if (box.hidden) return;
    if (event.key === "Escape") close();
    if (event.key === "ArrowLeft") show(current - 1);
    if (event.key === "ArrowRight") show(current + 1);
  });
}

function formatPhoneField(input) {
  const raw = input.value;
  const caret = input.selectionStart == null ? raw.length : input.selectionStart;
  let digitsBefore = raw.slice(0, caret).replace(/\D/g, "").length;
  let digits = raw.replace(/\D/g, "");
  if (digits.startsWith("1")) {
    digits = digits.slice(1);
    if (digitsBefore > 0) digitsBefore -= 1;
  }
  digits = digits.slice(0, 10);
  let formatted = "";
  if (digits.length && digits.length < 4) formatted = "(" + digits;
  else if (digits.length < 7) formatted = digits ? "(" + digits.slice(0, 3) + ") " + digits.slice(3) : "";
  else formatted = "(" + digits.slice(0, 3) + ") " + digits.slice(3, 6) + "-" + digits.slice(6);
  if (formatted === raw) return;
  input.value = formatted;
  let seen = 0;
  let pos = formatted.length;
  for (let i = 0; i < formatted.length; i += 1) {
    if (/\d/.test(formatted.charAt(i))) {
      seen += 1;
      if (seen === digitsBefore) {
        pos = i + 1;
        break;
      }
    }
  }
  if (digitsBefore === 0) pos = 0;
  input.setSelectionRange(pos, pos);
}

document.querySelectorAll('input[name="phone"]').forEach((input) => {
  input.setAttribute("inputmode", "tel");
  input.addEventListener("input", () => formatPhoneField(input));
  input.addEventListener("blur", () => formatPhoneField(input));
});

function isPortfolioDemoHost() {
  const host = location.hostname;
  if (location.protocol === "file:") return true;
  if (!host) return true;
  if (host.endsWith("github.io")) return true;
  return false;
}

function inquiryEndpoint() {
  if (isPortfolioDemoHost()) return null;
  const host = location.hostname;
  if (host === "127.0.0.1" || host === "localhost") {
    return "http://127.0.0.1:5000/api/website-inquiries";
  }
  return "https://login.sterlingsecurityguards.com/api/website-inquiries";
}

function showInquiryWait() {
  let overlay = document.getElementById("inquiry-wait");
  if (!overlay) {
    overlay = document.createElement("div");
    overlay.id = "inquiry-wait";
    overlay.className = "inquiry-wait";
    overlay.setAttribute("role", "status");
    overlay.setAttribute("aria-live", "assertive");
    overlay.innerHTML = '<div class="inquiry-wait-card"><p class="inquiry-wait-title">Please wait</p><p>Sending your request. Do not tap submit again.</p></div>';
    document.body.appendChild(overlay);
  }
  overlay.hidden = false;
}

function hideInquiryWait() {
  const overlay = document.getElementById("inquiry-wait");
  if (overlay) overlay.hidden = true;
}

document.querySelectorAll("form[data-inquiry]").forEach((form) => {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (form.getAttribute("data-submitting") === "1") return;
    form.setAttribute("data-submitting", "1");
    const button = form.querySelector("[type=submit]");
    const originalLabel = button ? button.textContent : "";
    if (button) {
      button.disabled = true;
      button.textContent = "Please wait…";
    }
    showInquiryWait();
    form.querySelectorAll('input[name="phone"]').forEach((input) => formatPhoneField(input));
    const data = Object.fromEntries(new FormData(form).entries());
    data.kind = form.dataset.inquiry;
    let note = form.querySelector(".form-error");
    try {
      const endpoint = inquiryEndpoint();
      if (!endpoint) {
        await new Promise((resolve) => window.setTimeout(resolve, 700));
      } else {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
        const body = await response.json().catch(() => ({}));
        if (!response.ok || !body.ok) {
          throw new Error(body.error || "Could not send");
        }
      }
      const sent = form.nextElementSibling;
      hideInquiryWait();
      if (!sent) return;
      form.hidden = true;
      sent.hidden = false;
      sent.focus();
    } catch (err) {
      form.removeAttribute("data-submitting");
      hideInquiryWait();
      if (button) {
        button.disabled = false;
        button.textContent = originalLabel;
      }
      if (!note) {
        note = document.createElement("p");
        note.className = "form-error";
        form.append(note);
      }
      note.textContent = err.message && err.message !== "Could not send"
        ? err.message
        : "We couldn't send that. Please call the office at (973) 484-4111.";
    }
  });
});
