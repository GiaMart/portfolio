const FORM_LABELS = {
  uniform: "Uniform Request",
  id_card: "ID Card Request",
  contact_update: "Updated Contact / Address",
  emergency_contact: "Emergency Contact Update",
  more_hours: "Request More Hours",
  sora_update: "SORA License Update",
  license_update: "Driver's License / Carry Permit",
};

const STATUS_BADGE = {
  new: "primary",
  in_progress: "warning",
  completed: "success",
  cancelled: "secondary",
};

const SUBMISSIONS = [
  {
    id: 1042,
    created_at: "Jul 28, 2026 2:14 PM",
    form_type: "uniform",
    first_name: "Maria",
    last_name: "Santos",
    site_name: "ShopRite Verona",
    phone: "(973) 555-0142",
    email: "maria.santos@example.com",
    status: "new",
    admin_notes: "",
    details: [
      ["Reason", "Damaged items"],
      ["Armed status", "Unarmed"],
      ["Short sleeve", "L"],
      ["Pants", "34"],
    ],
  },
  {
    id: 1038,
    created_at: "Jul 27, 2026 9:02 AM",
    form_type: "sora_update",
    first_name: "James",
    last_name: "Rivera",
    site_name: "Citizens Bank Newark",
    phone: "(973) 555-0198",
    email: "j.rivera@example.com",
    status: "in_progress",
    admin_notes: "Waiting on HR to verify renewal date.",
    details: [
      ["SORA expiration", "Aug 15, 2026"],
      ["Upload", "sora_card.pdf"],
    ],
    attachments: ["SORA card scan"],
  },
  {
    id: 1031,
    created_at: "Jul 25, 2026 4:48 PM",
    form_type: "more_hours",
    first_name: "Tyler",
    last_name: "Brooks",
    site_name: "Essex Green",
    phone: "(973) 555-0116",
    email: "",
    status: "new",
    admin_notes: "",
    details: [
      ["Requested date", "Jul 30, 2026"],
      ["Shift window", "6:00 PM – 2:00 AM"],
      ["Notes", "Available for coverage shift"],
    ],
  },
  {
    id: 1024,
    created_at: "Jul 22, 2026 11:20 AM",
    form_type: "id_card",
    first_name: "Aisha",
    last_name: "Patel",
    site_name: "Newark Academy",
    phone: "(973) 555-0177",
    email: "a.patel@example.com",
    status: "completed",
    admin_notes: "ID printed and mailed.",
    details: [["Reason", "New hire"]],
  },
  {
    id: 1019,
    created_at: "Jul 20, 2026 3:05 PM",
    form_type: "contact_update",
    first_name: "Carlos",
    last_name: "Mendez",
    site_name: "Payne Tech Interior",
    phone: "(973) 555-0133",
    email: "carlos.m@example.com",
    status: "cancelled",
    admin_notes: "Duplicate submission — kept earlier request.",
    details: [
      ["New address", "12 Oak Street, Bloomfield, NJ"],
      ["New phone", "(973) 555-0133"],
    ],
  },
];

let filters = { form_type: "", status: "", site_name: "" };
let activeId = null;

function esc(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function statusLabel(status) {
  return status.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function filteredSubmissions() {
  return SUBMISSIONS.filter((row) => {
    if (filters.form_type && row.form_type !== filters.form_type) return false;
    if (filters.status && row.status !== filters.status) return false;
    if (filters.site_name && row.site_name !== filters.site_name) return false;
    return true;
  });
}

function siteOptions() {
  return [...new Set(SUBMISSIONS.map((r) => r.site_name))].sort();
}

function setNavActive(view) {
  const navView = view === "detail" ? "list" : view;
  document.querySelectorAll(".ops-nav [data-view]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.view === navView);
  });
}

function showView(name) {
  document.querySelectorAll(".view").forEach((el) => el.classList.remove("active"));
  document.getElementById(`view-${name}`)?.classList.add("active");
  setNavActive(name);
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showToast(message) {
  const toast = document.getElementById("demo-toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("show");
  window.clearTimeout(showToast._timer);
  showToast._timer = window.setTimeout(() => toast.classList.remove("show"), 2400);
}

function renderDashboardPortal() {
  const tbody = document.querySelector("#dashboard-portal-table tbody");
  if (!tbody) return;
  const pending = SUBMISSIONS.filter((r) => r.status === "new" || r.status === "in_progress").slice(0, 4);
  tbody.innerHTML = pending
    .map(
      (row) => `
    <tr data-id="${row.id}">
      <td class="text-nowrap ps-3">${esc(row.created_at.split(" ").slice(0, 3).join(" "))}</td>
      <td>${esc(FORM_LABELS[row.form_type] || row.form_type)}</td>
      <td>${esc(row.first_name)} ${esc(row.last_name)}</td>
      <td><span class="badge text-bg-${STATUS_BADGE[row.status]}">${esc(statusLabel(row.status))}</span></td>
    </tr>`
    )
    .join("");
  tbody.querySelectorAll("tr[data-id]").forEach((tr) => {
    tr.addEventListener("click", () => showDetail(Number(tr.dataset.id)));
  });
}

function renderList() {
  const tbody = document.getElementById("submissions-tbody");
  const newCount = document.getElementById("new-count");
  const totalCount = document.getElementById("total-count");
  if (!tbody) return;

  const rows = filteredSubmissions();
  if (newCount) newCount.textContent = String(SUBMISSIONS.filter((r) => r.status === "new").length);
  if (totalCount) totalCount.textContent = String(SUBMISSIONS.length);

  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted py-4">No submissions match these filters.</td></tr>';
    return;
  }

  tbody.innerHTML = rows
    .map(
      (row) => `
    <tr data-id="${row.id}">
      <td onclick="event.stopPropagation()"><input class="form-check-input row-check" type="checkbox" aria-label="Select submission"></td>
      <td class="text-nowrap">${esc(row.created_at)}</td>
      <td>${esc(FORM_LABELS[row.form_type] || row.form_type)}</td>
      <td>${esc(row.first_name)} ${esc(row.last_name)}</td>
      <td><span class="site-hint"><strong>${esc(row.site_name)}</strong></span></td>
      <td><span class="badge text-bg-${STATUS_BADGE[row.status]}">${esc(statusLabel(row.status))}</span></td>
      <td class="text-end"><button type="button" class="btn btn-sm btn-outline-primary" data-view-id="${row.id}">View</button></td>
    </tr>`
    )
    .join("");

  tbody.querySelectorAll("tr[data-id]").forEach((tr) => {
    tr.addEventListener("click", () => showDetail(Number(tr.dataset.id)));
  });
  tbody.querySelectorAll("[data-view-id]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      showDetail(Number(btn.dataset.viewId));
    });
  });
}

function showDetail(id) {
  const row = SUBMISSIONS.find((r) => r.id === id);
  if (!row) return;
  activeId = id;

  document.getElementById("detail-title").textContent = FORM_LABELS[row.form_type] || row.form_type;
  document.getElementById("detail-submitted").textContent = `Submitted ${row.created_at}`;
  document.getElementById("detail-status-badge").className = `badge text-bg-${STATUS_BADGE[row.status]} fs-6`;
  document.getElementById("detail-status-badge").textContent = statusLabel(row.status);

  document.getElementById("detail-name").textContent = `${row.first_name} ${row.last_name}`;
  document.getElementById("detail-phone").innerHTML = row.phone
    ? `<span class="demo-masked">${esc(row.phone)}</span>`
    : "—";
  document.getElementById("detail-email").innerHTML = row.email
    ? `<span class="demo-masked">${esc(row.email)}</span>`
    : "—";
  document.getElementById("detail-site").innerHTML = `<strong>${esc(row.site_name)}</strong>`;

  document.getElementById("detail-fields").innerHTML = row.details
    .map(([label, value]) => `<dt class="col-sm-4">${esc(label)}</dt><dd class="col-sm-8">${esc(value)}</dd>`)
    .join("");

  const uploadsSection = document.getElementById("detail-uploads-section");
  const uploads = document.getElementById("detail-uploads-wrap");
  if (uploadsSection && uploads) {
    if (row.attachments?.length) {
      uploadsSection.hidden = false;
      uploads.innerHTML = row.attachments
        .map((name) => `<li><span class="text-muted">${esc(name)} · demo only</span></li>`)
        .join("");
    } else {
      uploadsSection.hidden = true;
      uploads.innerHTML = "";
    }
  }

  const statusSelect = document.getElementById("status-select");
  const notesField = document.getElementById("admin-notes");
  if (statusSelect) statusSelect.value = row.status;
  if (notesField) notesField.value = row.admin_notes || "";

  showView("detail");
}

function bindFilters() {
  const form = document.getElementById("filter-form");
  if (!form) return;

  const siteSelect = form.querySelector('[name="site_name"]');
  if (siteSelect) {
    siteSelect.innerHTML =
      '<option value="">All sites</option>' +
      siteOptions()
        .map((site) => `<option value="${esc(site)}">${esc(site)}</option>`)
        .join("");
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    filters = {
      form_type: form.form_type.value,
      status: form.status.value,
      site_name: form.site_name.value,
    };
    renderList();
  });
}

function bindDetail() {
  document.getElementById("back-to-list")?.addEventListener("click", () => {
    activeId = null;
    showView("list");
    renderList();
  });

  document.getElementById("save-status")?.addEventListener("click", (e) => {
    e.preventDefault();
    const row = SUBMISSIONS.find((r) => r.id === activeId);
    if (!row) return;
    row.status = document.getElementById("status-select").value;
    row.admin_notes = document.getElementById("admin-notes").value.trim();
    showToast("Submission updated (demo only — not saved).");
    showDetail(activeId);
    renderDashboardPortal();
  });
}

function bindNav() {
  document.querySelectorAll("[data-view]").forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      const view = el.dataset.view;
      if (view === "list") {
        activeId = null;
        renderList();
      }
      showView(view);
    });
  });
}

bindNav();
bindFilters();
bindDetail();
renderDashboardPortal();
renderList();
showView("dashboard");
window.showDetail = showDetail;
window.showView = showView;
