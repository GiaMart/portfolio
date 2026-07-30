const DIAMOND = "img/sterling-diamond.svg";
const BIWEEKLY = 14;
const PERIOD_SPAN = 13;
const PAYDAY_AFTER_END = 7;
const PAY_ANCHOR_PERIOD_START = dateOnly(2025, 5, 24);
const PAY_ANCHOR_PERIOD_END = dateOnly(2025, 6, 6);
const PAY_ANCHOR_PAYDAY = dateOnly(2025, 6, 13);

const FORM_TYPES = [
  { key: "uniform", icon: "👔", title: "Uniform Request", description: "Request shirts, pants, and hats. Please read the instructions before submitting.", demo: true },
  { key: "id_card", icon: "🪪", title: "ID Card Request", description: "Request a new Sterling company ID card.", demo: false },
  { key: "contact_update", icon: "📬", title: "Updated Contact / Address", description: "Submit your updated home address, email, or phone number.", demo: false },
  { key: "emergency_contact", icon: "🆘", title: "Emergency Contact Update", description: "Submit or update up to three emergency contacts on file.", demo: false },
  { key: "more_hours", icon: "⏰", title: "Request More Hours", description: "Request extra hours outside of your scheduled shift.", demo: false },
  { key: "sora_update", icon: "📋", title: "SORA License Update", description: "Submit your renewed or updated SORA certification.", demo: false },
  { key: "license_update", icon: "🚗", title: "Driver's License / Carry Permit", description: "Submit your updated driver's license or carrying permit.", demo: false },
];

const UNIFORM_SIZES = ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"];
const UNIFORM_REASONS = ["Weather Change", "New Hire", "Damaged items", "Wrong Size", "Extra Set"];
const DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

let calendarMonth = new Date();
calendarMonth = new Date(calendarMonth.getFullYear(), calendarMonth.getMonth(), 1);

function startOfDay(d = new Date()) {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate());
}

function dateOnly(y, m, d) {
  return new Date(y, m - 1, d);
}

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

function currentPayPeriod(today = startOfDay()) {
  return payCalendar(today).find((p) => p.label === "current") || null;
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

function quickLink(title, subtitle, opts = {}) {
  const classes = ["portal-quick-link", opts.clickable ? "is-clickable" : "is-disabled"].join(" ");
  const attrs = opts.go ? ` data-go="${opts.go}" role="button" tabindex="0"` : "";
  return `
    <div class="${classes}"${attrs}>
      <span class="portal-quick-link-icon" aria-hidden="true">
        <img src="${DIAMOND}" alt="" class="portal-quick-link-diamond">
      </span>
      <span class="portal-quick-link-text">
        <strong>${title}</strong>
        <span class="portal-quick-link-subtitle">${subtitle}</span>
      </span>
    </div>`;
}

function renderQuickLinks() {
  const el = document.getElementById("quick-links");
  if (!el) return;
  el.innerHTML = [
    quickLink("Supervisor Hotline", "(555) 010-0200 · demo only"),
    quickLink("Verona Office", "Mon–Fri 9 AM – 4 PM"),
    quickLink("ADP Pay Stubs", "workforcenow.adp.com"),
    quickLink("Request Forms", "Submit a Request", { clickable: true, go: "forms" }),
    quickLink("Portal Help", "Email Tech Desk (demo)"),
    quickLink("FAQs", "Payroll &amp; Office Info", { clickable: true, go: "faq" }),
  ].join("");
}

function renderPayCalendar() {
  const grid = document.getElementById("pay-month-grid");
  const title = document.getElementById("pay-month-title");
  if (!grid || !title) return;

  const today = startOfDay();
  const { title: monthTitle, weeks } = monthGrid(calendarMonth.getFullYear(), calendarMonth.getMonth(), today);
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

function renderPayTable() {
  const tbody = document.getElementById("pay-tbody");
  if (!tbody) return;
  const today = startOfDay();
  const periods = payCalendar(today);
  let nextPaydayShown = false;

  tbody.innerHTML = periods
    .map((p) => {
      let badge = "";
      if (p.label === "current") badge = '<span class="badge text-bg-info">Current period</span>';
      else if (p.label === "upcoming" && p.payday >= today && !nextPaydayShown) {
        nextPaydayShown = true;
        badge = '<span class="badge text-bg-primary">Next payday</span>';
      }
      const rowClass = p.label === "current" ? "current-period" : "";
      return `<tr class="${rowClass}">
        <td>${fmtPeriod(p.period_start, p.period_end)}</td>
        <td>${fmtPayday(p.payday)}</td>
        <td class="text-end">${badge}</td>
      </tr>`;
    })
    .join("");
}

function officeHoursForWeekday(weekday) {
  return weekday >= 5 ? "Closed" : "9 AM–4 PM";
}

function renderOfficeHours() {
  const container = document.getElementById("office-hours-rows");
  if (!container) return;

  const today = startOfDay();
  const start = (today.getDay() + 6) % 7;
  container.innerHTML = Array.from({ length: 7 }, (_, offset) => {
    const weekday = (start + offset) % 7;
    const isToday = offset === 0;
    return `
      <div class="office-hours-row${isToday ? " is-today" : ""}">
        <span class="office-hours-day">${DAY_NAMES[weekday]}</span>
        <span class="office-hours-time">${officeHoursForWeekday(weekday)}</span>
      </div>`;
  }).join("");
}

function renderFormList() {
  const list = document.getElementById("form-type-list");
  if (!list) return;
  list.innerHTML = FORM_TYPES.map((f) => `<li>${f.title}</li>`).join("");
}

function sizeOptions() {
  return [`<option value="">— Not requested —</option>`, ...UNIFORM_SIZES.map((s) => `<option value="${s}">${s}</option>`)].join("");
}

function renderUniformForm() {
  const reasons = document.getElementById("uniform-reasons");
  if (reasons) {
    reasons.innerHTML = UNIFORM_REASONS.map(
      (reason) => `
      <label class="uniform-reason-option">
        <input type="radio" name="reason" value="${reason}" required>
        <span>${reason}</span>
      </label>`
    ).join("");
  }
  ["short-sleeve", "long-sleeve", "pants"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) el.innerHTML = sizeOptions();
  });
}

function showView(name) {
  document.querySelectorAll(".view").forEach((el) => el.classList.remove("active"));
  document.getElementById(`view-${name}`)?.classList.add("active");
  document.querySelectorAll(".portal-nav .nav-link[data-view]").forEach((btn) => {
    const match = btn.dataset.view === name || (name === "uniform-form" && btn.dataset.view === "forms") || (name === "thank-you" && btn.dataset.view === "forms");
    btn.classList.toggle("active", match);
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function shiftMonth(delta) {
  calendarMonth = new Date(calendarMonth.getFullYear(), calendarMonth.getMonth() + delta, 1);
  renderPayCalendar();
}

function resetCalendarToToday() {
  const today = new Date();
  calendarMonth = new Date(today.getFullYear(), today.getMonth(), 1);
  renderPayCalendar();
}

function bindNavigation() {
  document.querySelectorAll(".portal-nav .nav-link[data-view]").forEach((btn) => {
    btn.addEventListener("click", () => showView(btn.dataset.view));
  });

  document.body.addEventListener("click", (e) => {
    const go = e.target.closest("[data-go]");
    if (go) showView(go.dataset.go);
  });

  document.body.addEventListener("keydown", (e) => {
    const go = e.target.closest("[data-go]");
    if (go && (e.key === "Enter" || e.key === " ")) {
      e.preventDefault();
      showView(go.dataset.go);
    }
  });

  document.getElementById("cal-prev")?.addEventListener("click", () => shiftMonth(-1));
  document.getElementById("cal-next")?.addEventListener("click", () => shiftMonth(1));
  document.getElementById("cal-today")?.addEventListener("click", resetCalendarToToday);

  document.getElementById("uniform-form-el")?.addEventListener("submit", (e) => {
    e.preventDefault();
    const first = document.getElementById("first-name")?.value.trim();
    document.getElementById("thank-name").textContent = first ? `, ${first}` : "";
    showView("thank-you");
  });

  document.getElementById("thank-home")?.addEventListener("click", () => {
    document.getElementById("uniform-form-el")?.reset();
    showView("home");
  });

  document.getElementById("thank-another")?.addEventListener("click", () => showView("forms"));
}

renderQuickLinks();
renderPayCalendar();
renderPayTable();
renderOfficeHours();
renderFormList();
renderUniformForm();
bindNavigation();
showView("home");
window.showView = showView;
