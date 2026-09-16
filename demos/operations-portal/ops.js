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

const BIWEEKLY = 14;
const PERIOD_SPAN = 13;
const PAYDAY_AFTER_END = 7;

let opsCalendarMonth = new Date();
opsCalendarMonth = new Date(opsCalendarMonth.getFullYear(), opsCalendarMonth.getMonth(), 1);

function startOfDay(d = new Date()) {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate());
}

function dateOnly(y, m, d) {
  return new Date(y, m - 1, d);
}

const PAY_ANCHOR_PERIOD_START = dateOnly(2025, 5, 24);
const PAY_ANCHOR_PERIOD_END = dateOnly(2025, 6, 6);
const PAY_ANCHOR_PAYDAY = dateOnly(2025, 6, 13);

function dateKey(d) {
  const x = startOfDay(d);
  const m = String(x.getMonth() + 1).padStart(2, "0");
  const day = String(x.getDate()).padStart(2, "0");
  return `${x.getFullYear()}-${m}-${day}`;
}

function addDays(d, n) {
  const r = new Date(d);
  r.setDate(r.getDate() + n);
  return r;
}

function sameDay(a, b) {
  return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
}

function fmtPeriod(start, end) {
  const sameYear = start.getFullYear() === end.getFullYear();
  const startStr = start.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  const endStr = end.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: sameYear ? undefined : "numeric",
  });
  return `${startStr} – ${endStr}${sameYear ? `, ${end.getFullYear()}` : ""}`;
}

function fmtPayday(d) {
  return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
}

function alignAnchor(anchor, target) {
  let current = new Date(anchor);
  if (current > target) {
    while (current > target) current = addDays(current, -BIWEEKLY);
  } else {
    while (addDays(current, BIWEEKLY) <= target) current = addDays(current, BIWEEKLY);
  }
  return current;
}

function biweeklyRange(anchor, start, end) {
  let current = new Date(anchor);
  while (current > start) current = addDays(current, -BIWEEKLY);
  while (current < start) current = addDays(current, BIWEEKLY);
  const dates = [];
  while (current <= end) {
    dates.push(new Date(current));
    current = addDays(current, BIWEEKLY);
  }
  return dates;
}

function payScheduleMarkers(rangeStart, rangeEnd) {
  const rs = startOfDay(rangeStart);
  const re = startOfDay(rangeEnd);
  const periodStarts = new Set(biweeklyRange(PAY_ANCHOR_PERIOD_START, rs, re).map((d) => dateKey(d)));
  const periodEnds = new Set(biweeklyRange(PAY_ANCHOR_PERIOD_END, rs, re).map((d) => dateKey(d)));
  const paydays = new Set(biweeklyRange(PAY_ANCHOR_PAYDAY, rs, re).map((d) => dateKey(d)));
  const inPeriod = new Set();

  biweeklyRange(PAY_ANCHOR_PERIOD_START, rs, re).forEach((ps) => {
    const pe = addDays(startOfDay(ps), PERIOD_SPAN);
    let day = startOfDay(ps);
    while (day <= pe) {
      if (day >= rs && day <= re) inPeriod.add(dateKey(day));
      day = addDays(day, 1);
    }
  });

  return { periodStarts, periodEnds, paydays, inPeriod };
}

function payCalendar(today = startOfDay(), past = 2, future = 6) {
  const anchor = alignAnchor(PAY_ANCHOR_PERIOD_START, today);
  const periods = [];
  const startAnchor = addDays(anchor, -BIWEEKLY * past);
  for (let i = 0; i < past + 1 + future; i += 1) {
    const ps = startOfDay(addDays(startAnchor, BIWEEKLY * i));
    const pe = startOfDay(addDays(ps, PERIOD_SPAN));
    const pd = startOfDay(addDays(pe, PAYDAY_AFTER_END));
    let label = "past";
    if (ps <= today && today <= pe) label = "current";
    else if (pd >= today) label = "upcoming";
    periods.push({ period_start: ps, period_end: pe, payday: pd, label });
  }
  return periods;
}

function currentPayPeriod(today = startOfDay()) {
  return payCalendar(today).find((p) => p.label === "current") || null;
}

function monthGrid(year, month, today = startOfDay()) {
  const first = dateOnly(year, month + 1, 1);
  const last = dateOnly(year, month + 1, new Date(year, month + 1, 0).getDate());
  const gridStart = startOfDay(addDays(first, -((first.getDay() + 7) % 7)));
  const gridEnd = startOfDay(addDays(last, (6 - ((last.getDay() + 7) % 7)) % 7));
  const { periodStarts, periodEnds, paydays, inPeriod } = payScheduleMarkers(gridStart, gridEnd);
  const activePeriod = currentPayPeriod(today);

  const weeks = [];
  let day = new Date(gridStart);
  while (day <= gridEnd) {
    const week = [];
    for (let i = 0; i < 7; i += 1) {
      const dayDate = startOfDay(day);
      const key = dateKey(dayDate);
      const markers = [];
      if (periodStarts.has(key)) markers.push("period_start");
      if (periodEnds.has(key)) markers.push("period_end");
      if (paydays.has(key)) markers.push("payday");
      if (inPeriod.has(key) && !markers.includes("in_period")) markers.push("in_period");
      if (
        activePeriod &&
        dayDate >= activePeriod.period_start &&
        dayDate <= activePeriod.period_end &&
        !markers.includes("current_period")
      ) {
        markers.push("current_period");
      }
      week.push({
        date: dayDate,
        in_month: dayDate.getMonth() === month,
        is_today: sameDay(dayDate, today),
        markers,
      });
      day = addDays(day, 1);
    }
    weeks.push(week);
  }

  return {
    title: first.toLocaleDateString("en-US", { month: "long", year: "numeric" }),
    weeks,
  };
}

function renderOpsPayCalendar() {
  const grid = document.getElementById("ops-pay-month-grid");
  const title = document.getElementById("ops-pay-month-title");
  if (!grid || !title) return;

  const today = startOfDay();
  const { title: monthTitle, weeks } = monthGrid(
    opsCalendarMonth.getFullYear(),
    opsCalendarMonth.getMonth(),
    today
  );
  title.textContent = monthTitle;

  const head = `<div class="pay-month-row pay-month-head">
    <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
  </div>`;

  const body = weeks
    .map(
      (week) => `
      <div class="pay-month-row">
        ${week
          .map((day) => {
            const classes = [
              "pay-month-day",
              !day.in_month ? "other-month" : "",
              day.is_today ? "is-today" : "",
              ...day.markers.map((m) => `mark-${m}`),
            ]
              .filter(Boolean)
              .join(" ");
            let tag = "";
            if (day.markers.includes("payday")) tag = '<span class="day-tag payday">Pay</span>';
            else if (day.markers.includes("period_start")) tag = '<span class="day-tag period-start">Start</span>';
            else if (day.markers.includes("period_end")) tag = '<span class="day-tag period-end">End</span>';
            return `<div class="${classes}"><span class="day-num">${day.date.getDate()}</span>${tag}</div>`;
          })
          .join("")}
      </div>`
    )
    .join("");

  grid.innerHTML = head + body;
}

function renderOpsPayTable() {
  const tbody = document.getElementById("ops-pay-tbody");
  if (!tbody) return;
  const today = startOfDay();
  const periods = payCalendar(today);
  let nextPaydayShown = false;

  tbody.innerHTML = periods
    .map((p) => {
      const isNext = !nextPaydayShown && p.payday >= today && p.label !== "past";
      if (isNext) nextPaydayShown = true;

      let badge = "";
      if (p.label === "current") badge = '<span class="badge text-bg-info">Current period</span>';
      if (isNext) {
        badge += `<span class="badge text-bg-primary${p.label === "current" ? " ms-1" : ""}">Next payday</span>`;
      }

      const rowClass = [
        p.label === "current" ? "current-period" : "",
        isNext ? "next-payday-period" : "",
      ]
        .filter(Boolean)
        .join(" ");
      return `<tr class="${rowClass}">
        <td>${fmtPeriod(p.period_start, p.period_end)}</td>
        <td>${fmtPayday(p.payday)}</td>
        <td class="text-end text-nowrap">${badge}</td>
      </tr>`;
    })
    .join("");
}

function shiftOpsCalendarMonth(delta) {
  opsCalendarMonth = new Date(opsCalendarMonth.getFullYear(), opsCalendarMonth.getMonth() + delta, 1);
  renderOpsPayCalendar();
}

function resetOpsCalendarToToday() {
  const today = new Date();
  opsCalendarMonth = new Date(today.getFullYear(), today.getMonth(), 1);
  renderOpsPayCalendar();
}

function bindOpsPayCalendar() {
  document.getElementById("ops-cal-prev")?.addEventListener("click", () => shiftOpsCalendarMonth(-1));
  document.getElementById("ops-cal-next")?.addEventListener("click", () => shiftOpsCalendarMonth(1));
  document.getElementById("ops-cal-today")?.addEventListener("click", resetOpsCalendarToToday);
}

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
    armed: "Unarmed",
    special_uniform: true,
    sweater_issued: true,
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
    armed: "Armed",
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
    armed: "Unarmed",
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
    armed: "Unarmed",
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
    armed: "Armed",
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
  idcards: {
    head: ["Employee ID", "Last", "First", "Card role", "SORA #", "Status"],
    rows: [
      ["1038", "Rivera", "James", "Armed", "SR-882104", "Active"],
      ["1042", "Santos", "Maria", "Unarmed", "SR-901442", "Active"],
      ["1024", "Patel", "Aisha", "Unarmed", "SR-877119", "Pending print"],
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

function submissionRowClass(row) {
  const classes = [];
  if (row.special_uniform) classes.push("table-row-special-uniform");
  if (row.sweater_issued) classes.push("table-row-sweater-issued");
  return classes.join(" ");
}

function armedBadge(label) {
  if (!label) return "—";
  const tone = label === "Armed" ? "danger" : "secondary";
  return `<span class="badge text-bg-${tone}">${esc(label)}</span>`;
}

function guardCell(row) {
  const flags = [];
  if (row.sweater_issued) flags.push('<span class="badge badge-sweater-issued">Sweater issued</span>');
  return `${esc(row.first_name)} ${esc(row.last_name)}${flags.length ? `<div class="mt-1">${flags.join(" ")}</div>` : ""}`;
}

function siteCell(row) {
  const special = row.special_uniform ? '<span class="badge badge-special-uniform ms-1">Special</span>' : "";
  return `<span class="site-hint"><strong>${esc(row.site_name)}</strong>${special}</span>`;
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

function syncFilterForm() {
  const form = document.getElementById("filter-form");
  if (!form) return;
  if (form.form_type) form.form_type.value = filters.form_type;
  if (form.status) form.status.value = filters.status;
  if (form.site_name) form.site_name.value = filters.site_name;
}

function applyRouteParams() {
  const params = new URLSearchParams(window.location.search);
  if (params.has("form_type")) filters.form_type = params.get("form_type") || "";
  if (params.has("status")) filters.status = params.get("status") || "";
  if (params.has("site_name")) filters.site_name = params.get("site_name") || "";
  syncFilterForm();
}

function applyRoute() {
  applyRouteParams();
  const params = new URLSearchParams(window.location.search);
  let view = params.get("view");
  let uniformTab = params.get("tab") || params.get("uniformTab");

  if (!view) {
    const hash = (window.location.hash || "").replace(/^#/, "").trim();
    if (hash) {
      const [hashView, sub] = hash.split("/");
      view = hashView;
      if (hashView === "uniforms") uniformTab = sub || "dashboard";
    }
  }

  if (view === "uniforms") {
    showView("uniforms");
    activateUniformTab(uniformTab || "dashboard");
    window.requestAnimationFrame(() => activateUniformTab(uniformTab || "dashboard"));
    return;
  }

  if (view && document.getElementById(`view-${view}`)) {
    if (view === "list") {
      activeId = null;
      renderList();
    }
    showView(view);
    return;
  }

  if (!view) showView("dashboard");
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
    <tr data-id="${row.id}" class="${submissionRowClass(row)}">
      <td class="text-nowrap ps-3">${esc(row.created_at.split(" ").slice(0, 3).join(" "))}</td>
      <td>${esc(FORM_LABELS[row.form_type] || row.form_type)}</td>
      <td>${guardCell(row)}</td>
      <td>${armedBadge(row.armed)}</td>
      <td>${siteCell(row)}</td>
      <td><span class="badge text-bg-${STATUS_BADGE[row.status]}">${esc(statusLabel(row.status))}</span></td>
      <td class="text-end pe-3"><button type="button" class="btn btn-sm btn-outline-primary" data-view-id="${row.id}">View</button></td>
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

function renderList() {
  const tbody = document.getElementById("submissions-tbody");
  const newCount = document.getElementById("new-count");
  const totalCount = document.getElementById("total-count");
  if (!tbody) return;

  const rows = filteredSubmissions();
  if (newCount) newCount.textContent = String(SUBMISSIONS.filter((r) => r.status === "new").length);
  if (totalCount) totalCount.textContent = String(SUBMISSIONS.length);

  if (!rows.length) {
    tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted py-4">No submissions match these filters.</td></tr>';
    return;
  }

  tbody.innerHTML = rows
    .map(
      (row) => `
    <tr data-id="${row.id}" class="${submissionRowClass(row)}">
      <td onclick="event.stopPropagation()"><input class="form-check-input row-check" type="checkbox" aria-label="Select submission"></td>
      <td class="text-nowrap">${esc(row.created_at)}</td>
      <td>${esc(FORM_LABELS[row.form_type] || row.form_type)}</td>
      <td>${guardCell(row)}</td>
      <td>${armedBadge(row.armed)}</td>
      <td>${siteCell(row)}</td>
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
  document.getElementById("detail-site").innerHTML = siteCell(row);

  const specialAlert = document.getElementById("detail-special-alert");
  if (specialAlert) specialAlert.hidden = !row.special_uniform;

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

function activateUniformTab(tab) {
  document.querySelectorAll("[data-uniform-tab]").forEach((b) => {
    b.classList.toggle("btn-primary", b.dataset.uniformTab === tab);
    b.classList.toggle("btn-outline-primary", b.dataset.uniformTab !== tab);
  });
  document.querySelectorAll(".uniform-panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === `uniform-panel-${tab}`);
  });
}

function bindUniformTabs() {
  document.querySelectorAll("[data-uniform-tab]").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      activateUniformTab(btn.dataset.uniformTab);
    });
  });
  document.querySelectorAll(".uniform-jump-tab").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      activateUniformTab(link.dataset.uniformTab);
    });
  });
  document.querySelectorAll("[data-uniform-tab].text-link-btn").forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      activateUniformTab(link.dataset.uniformTab);
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
bindOpsPayCalendar();
renderOpsPayCalendar();
renderOpsPayTable();
renderDashboardPortal();
renderList();
function bootRoute() {
  applyRoute();
}

bootRoute();
document.addEventListener("DOMContentLoaded", bootRoute);
window.addEventListener("load", bootRoute);
window.addEventListener("hashchange", applyRoute);
window.showDetail = showDetail;
window.showView = showView;
