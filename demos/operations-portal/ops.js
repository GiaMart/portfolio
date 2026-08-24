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

const REPORT_TABLES = {
  roster: {
    head: ["Employee ID", "Last", "First", "Status", "Site", "Armed", "SORA expiry"],
    rows: [
      ["1042", "Santos", "Maria", "Active", "ShopRite Verona", "No", "04/02/2027"],
      ["1038", "Rivera", "James", "Active", "Citizens Bank Newark", "Yes", "08/15/2026"],
      ["1031", "Brooks", "Tyler", "Active", "Essex Green", "No", "09/28/2026"],
      ["1024", "Patel", "Aisha", "Active", "Newark Academy", "No", "02/14/2027"],
    ],
  },
  sora: {
    head: ["Empl #", "Last", "First", "SORA #", "Expiry", "Type", "Status"],
    rows: [
      ["1019", "Mendez", "Carlos", "SR-812004", "05/01/2025", "Armed", "Expired"],
      ["1038", "Rivera", "James", "SR-882104", "08/15/2026", "Armed", "Active"],
      ["1031", "Brooks", "Tyler", "SR-877331", "09/28/2026", "Unarmed", "Active"],
    ],
  },
  incidents: {
    head: ["Date", "Site", "Guard", "Summary", "Status"],
    rows: [
      ["Jul 28, 2026", "ShopRite Verona", "Maria Santos", "Customer altercation — supervisor notified", "Open"],
      ["Jul 25, 2026", "Citizens Bank Newark", "James Rivera", "Broken lock on rear entrance", "Closed"],
      ["Jul 22, 2026", "Essex Green", "Tyler Brooks", "Medical assist — EMS called", "Closed"],
    ],
  },
  writeups: {
    head: ["Date", "Site", "Guard", "Violation", "Status"],
    rows: [
      ["Jul 20, 2026", "Home Depot East Hanover", "Carlos Mendez", "Late arrival — documented", "Closed"],
      ["Jul 15, 2026", "Kean University", "Aisha Patel", "Uniform policy reminder", "Open"],
    ],
  },
  logsheets: {
    head: ["Date", "Site", "Supervisor", "Shift", "Status"],
    rows: [
      ["Jul 29, 2026", "Citizens Bank Newark", "Vinny R.", "Overnight", "Filed"],
      ["Jul 28, 2026", "ShopRite Verona", "Ronnie M.", "Day", "Filed"],
    ],
  },
  shiftchanges: {
    head: ["Date", "Site", "Guard", "Change", "Status"],
    rows: [
      ["Jul 30, 2026", "Essex Green", "Tyler Brooks", "Coverage swap approved", "Completed"],
      ["Jul 27, 2026", "Newark Academy", "Maria Santos", "Extra shift added", "Pending"],
    ],
  },
};

function statusBadge(label) {
  const map = {
    Open: "warning",
    Closed: "success",
    Active: "success",
    Expired: "danger",
    Filed: "success",
    Completed: "success",
    Pending: "warning",
  };
  const tone = map[label] || "secondary";
  return `<span class="badge text-bg-${tone}">${esc(label)}</span>`;
}

function renderReportTable(key) {
  const table = REPORT_TABLES[key];
  const head = document.getElementById("report-table-head");
  const body = document.getElementById("report-table-body");
  if (!table || !head || !body) return;

  head.innerHTML = `<tr>${table.head.map((col, i) => `<th${i === 0 ? ' class="ps-3"' : ""}>${esc(col)}</th>`).join("")}</tr>`;
  body.innerHTML = table.rows
    .map(
      (row) =>
        `<tr>${row
          .map((cell, i) => {
            const isStatus = table.head[i] === "Status";
            const content = isStatus ? statusBadge(cell) : esc(cell);
            return `<td${i === 0 ? ' class="ps-3"' : ""}>${content}</td>`;
          })
          .join("")}</tr>`
    )
    .join("");
}

function bindReportPills() {
  document.querySelectorAll("#report-pills [data-report]").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#report-pills .nav-link").forEach((pill) => pill.classList.remove("active"));
      btn.classList.add("active");
      renderReportTable(btn.dataset.report);
    });
  });
  renderReportTable("incidents");
}

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
  document.querySelectorAll(".ops-nav .nav-link[data-view], .ops-nav .dropdown-item[data-view]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.view === navView);
  });
  document.querySelectorAll(".ops-nav .dropdown-toggle").forEach((toggle) => {
    const group = toggle.closest(".dropdown");
    const childActive = group?.querySelector(`[data-view="${navView}"]`);
    toggle.classList.toggle("active", !!childActive);
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
    showToast("Submission updated for this demo session.");
    showDetail(activeId);
    renderDashboardPortal();
  });
}

function bindUniformTabs() {
  document.querySelectorAll("[data-uniform-tab]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.dataset.uniformTab;
      document.querySelectorAll("[data-uniform-tab]").forEach((b) => {
        b.classList.toggle("btn-primary", b.dataset.uniformTab === tab);
        b.classList.toggle("btn-outline-primary", b.dataset.uniformTab !== tab);
      });
      document.querySelectorAll(".uniform-panel").forEach((panel) => {
        panel.classList.toggle("active", panel.id === `uniform-panel-${tab}`);
      });
    });
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
      document.querySelector("#opsNav.show")?.classList.remove("show");
    });
  });
}

bindNav();
bindFilters();
bindDetail();
bindReportPills();
bindUniformTabs();
renderDashboardPortal();
renderList();
showView("dashboard");
window.showDetail = showDetail;
window.showView = showView;
