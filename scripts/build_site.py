"""Generate static HTML site from content/site.json"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))

LINKEDIN_SVG = """<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path fill="currentColor" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
</svg>"""

# Text content the HTML scraper missed (from Adobe Portfolio)
PROJECT_TEXT = {
    "uniform-inventory-tracking": [
        "Skills: ChatGPT · Google Apps Script · AppSheet · Google Sheets · QR",
        "The problem: Uniform checkout was manual and error-prone — no real-time visibility into stock levels or who took what.",
        "What I built: A Google Sheets tracker with automated low-stock email alerts, a mobile AppSheet app for QR-based checkouts, and a Python script (written with ChatGPT) to generate printable QR labels.",
        "How I used AI: ChatGPT helped write and debug Apps Script and Python. I defined the workflow and requirements; AI accelerated the code and documentation.",
        "Outcome: Employees scan and submit takeouts from the uniform room. Admin staff get live inventory oversight and alerts before items run out.",
    ],
    "uniform-inventory-tracking-2": [
        "Skills: Cursor · Flask · SQLite · Render · SMTP",
        "Evolution: Version 1 proved QR checkout and alerts in Google Sheets. Uniform Inventory Tracking 2.0 lives inside the operations portal — same database as employee uniform requests, guard history, and stock-room takeouts.",
        "Uniforms dashboard: SKUs tracked, total on hand, low/out counts, pending requests with pack chips, recent takeouts, and size charts — the ops home screen for uniform inventory.",
        "Inventory module: Full SKU table with starting/restock/takeout/adjust columns, reorder thresholds, restock log, takeout log, and a secret stock-room QR link for no-login checkout from the Verona uniform room.",
        "Employee form: Guards submit uniform requests from the employee portal — site picker, armed/unarmed, reason, item sizes with out-of-stock labels, and sweater field for eligible sites only. Submissions land in the admin portal queue.",
        "Portal integration: When guards submit uniform requests, HR sees them in the portal queue. Rows highlight in purple for special-uniform sites (custom to specific site). Rows highlight in red when a guard already received a one-time item — like a sweater — so staff do not double-issue.",
        "Sweater rules: Only certain sites can request a sweater in the employee portal. The demo form includes Essex Green (regular) and Newark Academy (sweater-eligible) so visitors can see the sweater field appear when an eligible site is selected. Guards get one sweater; the form explains the policy and HR can review exceptions in the notes.",
        "Stock alert emails: When inventory newly hits low or out of stock, the system emails Office Administrator automatically with a branded alert listing affected sizes. Seasonal items respect in-season rules so winter skully alerts do not fire in July.",
        "How I used AI: Cursor helped wire inventory mutations to alert checks, portal row highlighting, and sweater site logic. I owned thresholds, eligible sites, and the HR workflow.",
    ],
    "employee-portal": [
        "Skills: Google Sites · Google Forms · Google Sheets",
        "A modern, mobile-friendly Google Site that consolidates essential company resources for employees in one place — from pay schedules to HR forms.",
        "Form Submissions: Integrated Google Forms for ID card requests, personal info updates, and onboarding data.",
        "Reduced back-and-forth with HR and management by streamlining common employee requests.",
    ],
    "scheduling-automation": [
        "Skills: Google Forms · Zapier · Google Calendar · Google Sheets · Workflow Automation",
        "Automated Callouts & Hour Requests",
        "I created two Google Forms to simplify time-sensitive scheduling communications:",
        "One for supervisors to report sick days",
        "One for employees to request additional hours",
    ],
    "employee-portal-2": [
        "Skills: Cursor · ChatGPT · Prompt Engineering · Flask · SQLite · Render",
        "The challenge: The original Google Sites portal couldn't support a dynamic pay calendar, guard-facing incident reporting, structured form routing with file uploads, or an admin review queue tied to company data.",
        "My approach: I'm not a traditional developer — I use AI as a build partner. I scoped requirements with HR and ops, designed the UX, and iteratively built Employee Portal 2.0 in Cursor — then deployed it on its own live domain alongside the operations admin.",
        "What's included: Biweekly pay calendar, office map and FAQs, 7 employee request forms (each with production-style fields and file uploads where applicable), guard-facing incident reports, QR stock-room takeout, site-specific QR logs (Wayne Mall and Castle Ridge), and email notifications on every submission — all connected to the same database as SORA, uniforms, and billing.",
        "Why this matters: This project shows how someone with operations and IT knowledge can ship production software by combining clear problem-solving with AI-assisted development — not by writing every line of code from scratch.",
    ],
    "operations-portal": [
        "Skills: Cursor · ChatGPT · Prompt Engineering · Flask · SQLite · Render",
        "The problem: Sterling ran on spreadsheets and disconnected tools — and supervisors still filed incident reports, disciplinary write-ups, and log sheets on pen and paper. Guards, client sites, billing, SORA certifications, uniforms, and employee requests had no single source of truth.",
        "My approach: I mapped the ops workflow with leadership, then built the admin app iteratively in Cursor with AI — database schema, Flask routes, Bootstrap UI, role-based permissions, and production deployment on Render with separate employee and admin domains.",
        "Field reporting: Supervisors now file incident reports, write-ups, and log sheets from their phones in the field instead of paper forms. For sites that require daily logs, we set up site-specific log types and scheduled email times so completed logs go automatically to the property manager — no manual forwarding.",
        "What's included: Operations dashboard with pay calendar, SORA watch, billing snapshot, and portal queue (armed status, special-uniform sites, sweater/jacket flags), client and site management, guard roster, SORA compliance tracking, uniform inventory with QR stock-room checkout, billing (invoices, oldest open, deposits, all payments), supervisor mobile reporting, site-specific log queues with auto-email to property managers (e.g. Wayne Mall, Castle Ridge), documents and printables, equipment registry, and an employee portal submission queue with workflow automation.",
        "Access control: Role-based sign-in accounts — IT full admin, HR for portal submissions, Finance for invoices and billing, supervisors for field reports, and view-only access where needed.",
        "Deployment: Live on Render with Gunicorn and persistent storage. Email notifications fire when employees submit portal requests or incident reports.",
        "How I used AI: Cursor helped me scaffold routes, debug SQL, refine templates, and iterate quickly. I owned the requirements, UX, and testing — AI accelerated the build.",
    ],
    "sterling-website": [
        "Skills: Squarespace · Web Design · Branding · Content Strategy",
        "The challenge: Sterling's previous website was dated and static. It listed an Employment page in the nav, but there was no way to collect applications online or review submissions — hiring relied on phone calls and scattered email attachments.",
        "What I did: Redesigned and rebuilt sterlingsecurityguards.com on Squarespace — modern homepage, service sections, and a dedicated Employment Opportunities page with an application form (resume upload, contact info, armed/unarmed status, and more).",
        "Employment applications: Submissions sync from the Squarespace form into a Google Sheet, where leadership can review applicants in one place and mass-email candidates to schedule interviews. That workflow never existed on the old site — the Employment link was there, but it didn't capture or organize applications.",
        "Outcome: A mobile-friendly public site that presents Sterling's services clearly, routes consultation requests, and gives hiring a structured pipeline for new guard applications.",
    ],
}

PROJECT_DEMOS = {
    "employee-portal-2": [
        {
            "path": "demos/employee-portal-2/index.html",
            "heading": "Try the employee portal",
            "note": "Interactive preview — pay calendar, incident report, all 7 production-style request forms, stock-room QR takeout, and FAQs. Submissions are simulated.",
        },
        {
            "path": "demos/employee-portal-2/index.html#uniform-form",
            "heading": "Uniform request form",
            "note": "Site picker includes Essex Green (regular) and Newark Academy (sweater-eligible). Select Newark Academy to reveal the sweater size field.",
        },
    ],
    "operations-portal": [
        {
            "path": "demos/operations-portal/index.html",
            "heading": "Try the operations portal",
            "note": "Interactive preview — updated dashboard (pay calendar, SORA watch, billing snapshot), portal queue with armed/special-uniform cues, billing (oldest open, all payments), Wayne Mall & Castle Ridge logs, uniforms, printables, and all major modules. Sample data only.",
        },
    ],
    "uniform-inventory-tracking-2": [
        {
            "path": "demos/operations-portal/index.html#uniforms/dashboard",
            "heading": "Uniforms dashboard",
            "note": "Staff → Uniforms → Dashboard. Overview stats, low/out-of-stock watch, pending requests with pack chips, recent takeouts, and size charts. Sample data only.",
        },
        {
            "path": "demos/operations-portal/index.html#uniforms/inventory",
            "heading": "Inventory table",
            "note": "Full SKU grid with filters, on-hand vs requests vs current, and adjust buttons — same layout as production.",
        },
        {
            "path": "demos/operations-portal/index.html#uniforms/portal-requests",
            "heading": "Portal uniform requests",
            "note": "Admin queue for employee submissions. Purple = special-uniform sites. Red = sweater or jacket already issued. Pending vs on-hand chips at the top.",
        },
        {
            "path": "demos/employee-portal-2/index.html#uniform-form",
            "heading": "Employee uniform request form",
            "note": "Guard-facing form with Before You Submit copy and a demo site picker: Essex Green (regular) or Newark Academy (sweater-eligible — select it to reveal the sweater field). Submissions are simulated.",
        },
    ],
}

RELATED_LINKS = {
    "employee-portal-2": ("operations-portal.html", "Operations Portal — admin dashboard & submission queue"),
    "operations-portal": ("employee-portal-2.html", "Employee Portal 2.0 — guard-facing portal"),
    "uniform-inventory-tracking-2": (
        "uniform-inventory-tracking.html",
        "Uniform Inventory Tracking (v1) — Google Sheets & AppSheet",
    ),
    "uniform-inventory-tracking": (
        "uniform-inventory-tracking-2.html",
        "Uniform Inventory Tracking 2.0 — operations portal module",
    ),
}

IMAGE_LAYOUT = {
    "uniform-inventory-tracking": ["dashboard", "mobile", "mobile", "mobile"],
    "employee-portal": ["browser", "browser"],
    "scheduling-automation": ["dashboard"],
    "sterling-website": ["compare", "browser"],
}

COMPARE_FRAMES = {
    "sterling-website": ("Previous website", "sterlingsecurityguards.com"),
}

FRAME_TITLES = {
    "uniform-inventory-tracking": ["Uniform Inventory · Google Sheets"],
    "employee-portal": [
        "Sterling Employee Portal",
        "Request Forms",
    ],
    "scheduling-automation": ["Form Responses · Google Sheets"],
    "sterling-website": [
        "Sterling Securities · Employment",
    ],
}

GALLERY_POLISH = {
    "uniform-inventory-tracking",
    "uniform-inventory-tracking-2",
    "employee-portal",
    "scheduling-automation",
    "sterling-website",
}

GALLERY_GRID = {
    "ariannas-angels",
}


def uniform_inventory_2_gallery() -> str:
    return """
    <div class="gallery-section">
      <h2 class="gallery-section-title">Low &amp; out-of-stock email alerts</h2>
      <figure class="project-image project-image--email">
        <div class="uniform-email-preview" role="img" aria-label="Sample uniform stock alert email">
          <div style="max-width:640px;margin:0 auto 1rem;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden;background:#fff;font-family:Segoe UI,Helvetica,Arial,sans-serif;">
            <div style="padding:0.75rem 1rem;background:#f8fafc;border-bottom:1px solid #e2e8f0;font-size:0.82rem;color:#64748b;">
              <div><strong style="color:#0f172a;">From:</strong> Sterling Operations Portal</div>
              <div><strong style="color:#0f172a;">Subject:</strong> Uniform Stock alert — 1 out, 3 low</div>
            </div>
          </div>
          <div style="margin:0;padding:0;background:#eef2f7;font-family:Segoe UI,Helvetica,Arial,sans-serif;color:#0f172a;border-radius:12px;overflow:hidden;">
            <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;border-collapse:collapse;">
              <tr>
                <td align="center" style="padding:32px 16px;">
                  <table width="560" cellpadding="0" cellspacing="0" role="presentation"
                         style="width:100%;max-width:560px;background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(10,22,40,0.08);border-collapse:collapse;">
                    <tr>
                      <td style="background:linear-gradient(135deg,#0a1628 0%,#1e3a5f 100%);padding:32px 28px;text-align:center;">
                        <p style="margin:0 0 10px;font-size:24px;font-weight:700;line-height:1.3;color:#ffffff;">Uniform Inventory Alert</p>
                        <p style="margin:0;font-size:15px;font-weight:700;line-height:1.5;color:#ffffff;">The following in-season items need attention.</p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:28px 32px 24px;">
                        <h2 style="margin:0 0 8px;font-size:13px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#dc2626;">Out of stock</h2>
                        <table width="100%" cellpadding="0" cellspacing="0" style="width:100%;font-size:15px;border-collapse:collapse;">
                          <tr>
                            <td style="padding:8px 0;border-bottom:1px solid #e2e8f0;">
                              <span style="font-weight:600;color:#0f172a;">Long sleeve shirt</span>
                              <span style="color:#64748b;"> — 2XL</span>
                            </td>
                            <td align="right" style="padding:8px 0;border-bottom:1px solid #e2e8f0;font-weight:600;color:#0f172a;white-space:nowrap;">0 on hand</td>
                          </tr>
                        </table>
                        <h2 style="margin:24px 0 8px;font-size:13px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:#d97706;">Low stock</h2>
                        <table width="100%" cellpadding="0" cellspacing="0" style="width:100%;font-size:15px;border-collapse:collapse;">
                          <tr>
                            <td style="padding:8px 0;border-bottom:1px solid #e2e8f0;">
                              <span style="font-weight:600;color:#0f172a;">Short sleeve shirt</span>
                              <span style="color:#64748b;"> — L</span>
                            </td>
                            <td align="right" style="padding:8px 0;border-bottom:1px solid #e2e8f0;font-weight:600;color:#0f172a;white-space:nowrap;">4 on hand</td>
                          </tr>
                          <tr>
                            <td style="padding:8px 0;border-bottom:1px solid #e2e8f0;">
                              <span style="font-weight:600;color:#0f172a;">Pants</span>
                              <span style="color:#64748b;"> — 34</span>
                            </td>
                            <td align="right" style="padding:8px 0;border-bottom:1px solid #e2e8f0;font-weight:600;color:#0f172a;white-space:nowrap;">6 on hand</td>
                          </tr>
                          <tr>
                            <td style="padding:8px 0;border-bottom:1px solid #e2e8f0;">
                              <span style="font-weight:600;color:#0f172a;">Winter skully</span>
                              <span style="color:#64748b;"> — One size</span>
                            </td>
                            <td align="right" style="padding:8px 0;border-bottom:1px solid #e2e8f0;font-weight:600;color:#0f172a;white-space:nowrap;">3 on hand</td>
                          </tr>
                        </table>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 32px 32px;">
                        <p style="margin:0;font-size:14px;line-height:1.5;color:#64748b;">
                          View full inventory in the admin site under
                          <strong style="color:#1e3a5f;">Uniforms → Inventory</strong>.
                        </p>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </div>
          <p style="margin:1rem 0 0;font-size:0.82rem;color:#666;text-align:center;">Sent to Office Administrator when a SKU newly crosses its reorder threshold</p>
        </div>
        <figcaption>Automated SMTP alert when inventory newly hits low or out of stock — same template as production</figcaption>
      </figure>
    </div>
    <div class="gallery-section">
      <h2 class="gallery-section-title">Portal queue highlighting</h2>
      <figure class="project-image project-image--dashboard">
        <div style="border:1px solid #e8e8e8;border-radius:12px;overflow:hidden;background:#fff;font-family:Segoe UI,Helvetica,Arial,sans-serif;">
          <div style="display:flex;flex-wrap:wrap;gap:0.75rem 1.25rem;padding:0.85rem 1rem;background:#f8fafc;border-bottom:1px solid #e8e8e8;font-size:0.82rem;color:#666;">
            <span><span style="display:inline-block;width:0.85rem;height:0.85rem;border-radius:0.2rem;margin-right:0.35rem;background:rgba(124,58,237,0.45);vertical-align:-0.1rem;border:1px solid rgba(0,0,0,0.08);"></span> Special uniform site (purple)</span>
            <span><span style="display:inline-block;width:0.85rem;height:0.85rem;border-radius:0.2rem;margin-right:0.35rem;background:rgba(220,38,38,0.45);vertical-align:-0.1rem;border:1px solid rgba(0,0,0,0.08);"></span> Sweater / one-time item already issued (red)</span>
          </div>
          <table width="100%" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;font-size:0.9rem;">
            <thead>
              <tr style="background:#f1f5f9;">
                <th style="text-align:left;padding:0.65rem 1rem;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.04em;color:#666;">Employee</th>
                <th style="text-align:left;padding:0.65rem 1rem;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.04em;color:#666;">Site</th>
                <th style="text-align:left;padding:0.65rem 1rem;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.04em;color:#666;">Flags</th>
              </tr>
            </thead>
            <tbody>
              <tr style="background:rgba(220,38,38,0.12);">
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;">Maria Santos</td>
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;">ShopRite Verona <span style="display:inline-block;padding:0.15rem 0.45rem;border-radius:999px;font-size:0.68rem;font-weight:700;background:#7c3aed;color:#fff;margin-left:0.25rem;">Special</span></td>
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;"><span style="display:inline-block;padding:0.15rem 0.45rem;border-radius:999px;font-size:0.68rem;font-weight:700;background:#dc2626;color:#fff;">Sweater issued</span></td>
              </tr>
              <tr style="background:rgba(220,38,38,0.12);">
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;">James Rivera</td>
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;">Citizens Bank Newark</td>
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;"><span style="display:inline-block;padding:0.15rem 0.45rem;border-radius:999px;font-size:0.68rem;font-weight:700;background:#dc2626;color:#fff;">Sweater issued</span></td>
              </tr>
              <tr>
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;">Tyler Brooks</td>
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;">Newark Academy</td>
                <td style="padding:0.75rem 1rem;border-top:1px solid #e8e8e8;color:#666;font-size:0.82rem;">Sweater-eligible site</td>
              </tr>
            </tbody>
          </table>
        </div>
        <figcaption>Purple = special-uniform site. Red = guard already received a one-time item — prevents double-issuing sweaters.</figcaption>
      </figure>
    </div>"""


PROJECT_GALLERY_EXTRA = {
    "uniform-inventory-tracking-2": uniform_inventory_2_gallery,
}

IMAGE_CAPTIONS = {
    "seton-hall": [
        "", "Men's Next Game", "", "Women's Next Game", "", "Wounded Warrior Project",
    ],
    "2021": [
        "Lakers Poster", "Luka", "Lamelo", "LA Bron", "Mamba Out", "KD To NYC",
        "CP3 To Houston", "Lebron NBA Logoman", "Lebron Lakers Logoman", "Kyrie NBA Logoman",
        "Kyrie Celtics Logoman", "Kyrie Celtics Logoman Alt", "Porzingus NBA Logoman",
        "Porzingus Knicks Logoman", "Kemba Record", "Derozan Trade", "Butler Potential Trades",
    ],
    "art-work-1": [
        "Brotherhood", "Matthew Hurt Commitment", "Kyree Walker Top Schools", "March Madness",
        "Les Quinones Commitment", "Cassius Stanley Commitment", "Cole Anthony Commitment",
        "Villanova Commitments", "Drew Timme Commitment", "DJ Jeffries Commitment",
        "Boogie Ellis Commitment", "Josh Green Commitment", "Myles Powell Statline",
        "Johnny Juzang Commitment", "Jeremy Roach Commitment",
    ],
    "commissions": ["Top Schools", "Transfer", "", "", "", "", "", "Jesse Jones G League"],
    "ariannas-angels": [
        "2026 Logo",
        "2024 Gift — Phone Wallet",
        "2024 Sticker",
        "2023 Gift — Keychain",
        "10th Anniversary Mint Label",
        "Bucco's Rising Stars Christmas Lunch — Banner",
        "Bucco's Rising Stars Christmas Lunch — Poster",
    ],
    "uniform-inventory-tracking": [
        "Live inventory dashboard with color-coded sizes and low-stock alerts",
        "AppSheet · Inventory view",
        "AppSheet · Checkout form",
        "AppSheet · QR checkout",
    ],
    "employee-portal": [
        "Google Sites home page — pay calendar, FAQs, and quick links",
        "Embedded Google Forms for employee requests",
    ],
    "scheduling-automation": [
        "Automated form responses synced to Google Sheets for scheduling review",
    ],
    "sterling-website": [
        "The old site had an Employment nav link but no application form or submission inbox. The new Squarespace site is mobile-friendly with clear service pages and a consultation path.",
        "Employment Opportunities — online application with resume upload; submissions reviewable in Squarespace",
    ],
}


def esc(s: str) -> str:
    return html.escape(s)


def projects_by_category(category: str) -> list:
    items = [p for p in CONTENT["projects"] if p["category"] == category]

    def sort_key(project: dict) -> tuple:
        year = int(project.get("year", 0))
        order = project.get("order", 0)
        return (-year, -order)

    return sorted(items, key=sort_key)


def nav(active: str = "") -> str:
    links = [
        ("index.html", "Welcome", "home"),
        ("about.html", "About", "about"),
        ("systems.html", "Digital Systems", "systems"),
        ("design.html", "Graphic Design", "design"),
        ("contact.html", "Contact", "contact"),
    ]
    items = []
    for href, label, key in links:
        cls = ' class="active"' if active == key else ""
        items.append(f'<a href="{href}"{cls}>{esc(label)}</a>')
    return "\n".join(items)


def favicon_tags(asset_prefix: str = "") -> str:
    return f"""  <link rel="icon" href="{asset_prefix}favicon.ico" sizes="any">
  <link rel="icon" href="{asset_prefix}favicon-32x32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="{asset_prefix}apple-touch-icon.png">"""


def head(title: str, asset_prefix: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <title>{esc(title)} — Gia Martini</title>
{favicon_tags(asset_prefix)}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{asset_prefix}css/style.css">
</head>"""


def layout(
    title: str,
    active: str,
    body: str,
    main_class: str = "",
    asset_prefix: str = "",
    nav_prefix: str = "",
) -> str:
    main_attr = f' class="{esc(main_class)}"' if main_class else ""
    profile_src = f"{asset_prefix}{CONTENT['profilePhoto']}"
    nav_html = nav(active)
    if nav_prefix:
        for page in ("index.html", "about.html", "design.html", "systems.html", "contact.html"):
            nav_html = nav_html.replace(f'href="{page}"', f'href="{nav_prefix}{page}"')
    return f"""{head(title, asset_prefix)}
<body>
  <header class="site-header">
    <a href="{nav_prefix}index.html" class="logo">
      <img src="{profile_src}" alt="Gia Martini" class="logo-img">
      <span>Gia Martini</span>
    </a>
    <nav class="site-nav">{nav_html}</nav>
    <button class="nav-toggle" aria-label="Menu" onclick="document.body.classList.toggle('nav-open')">☰</button>
  </header>
  <main{main_attr}>{body}</main>
  <footer class="site-footer">
    <p>&copy; {CONTENT['name']}</p>
  </footer>
  <script src="{asset_prefix}js/main.js"></script>
</body>
</html>"""


def project_card(p: dict) -> str:
    return f"""
    <a href="work/{p['slug']}.html" class="project-card">
      <img src="{p['thumbnail']}" alt="{esc(p['title'])}" loading="lazy">
      <div class="project-card-info">
        <span class="year">{esc(p['year'])}</span>
        <h3>{esc(p['title'])}</h3>
      </div>
    </a>"""


def build_home() -> str:
    design = projects_by_category("design")
    systems = projects_by_category("systems")
    body = f"""
  <section class="hero">
    <h1>{esc(CONTENT['name'])}</h1>
    <div class="skill-tags">
      <span>{esc(CONTENT['skills']['systems'])}</span>
      <span>{esc(CONTENT['skills']['design'])}</span>
    </div>
  </section>
  <section class="section">
    <div class="section-header">
      <h2>Digital Systems</h2>
      <a href="systems.html" class="view-all">View all →</a>
    </div>
    <div class="project-grid">{''.join(project_card(p) for p in systems)}</div>
  </section>
  <section class="section">
    <div class="section-header">
      <h2>Graphic Design</h2>
      <a href="design.html" class="view-all">View all →</a>
    </div>
    <div class="project-grid">{''.join(project_card(p) for p in design[:4])}</div>
  </section>"""
    return layout("Welcome", "home", body)


def build_gallery_page(title: str, active: str, category: str) -> str:
    projects = projects_by_category(category)
    body = f"""
  <section class="page-header">
    <h1>{esc(title)}</h1>
  </section>
  <section class="section">
    <div class="project-grid">{''.join(project_card(p) for p in projects)}</div>
  </section>"""
    return layout(title, active, body)


def grid_figure_html(src: str, alt: str, title: str) -> str:
    return f"""
    <figure class="project-image project-image--grid-card">
      <div class="project-image-card">
        <img src="../{src}" alt="{esc(alt)}" loading="lazy">
        <span class="project-image-label">{esc(title)}</span>
      </div>
    </figure>"""


def figure_html(p: dict, i: int, img: dict, img_layout: str, captions: list) -> str:
    cap = captions[i] if i < len(captions) else img.get("alt", "")
    alt = cap or p["title"]
    cap_html = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
    cls = "project-image project-image--mobile" if img_layout == "mobile" else "project-image"
    return f"""
      <figure class="{cls}">
        <div class="phone-frame">
          <img src="../{img['src']}" alt="{esc(alt)}" loading="lazy">
        </div>
        {cap_html}
      </figure>"""


def browser_frame_inner(src: str, alt: str, title: str) -> str:
    return f"""
      <div class="browser-frame">
        <div class="browser-frame-bar">
          <span class="browser-dots" aria-hidden="true"><i></i><i></i><i></i></span>
          <span class="browser-frame-title">{esc(title)}</span>
        </div>
        <div class="browser-frame-body">
          <img src="../{src}" alt="{esc(alt)}" loading="lazy">
        </div>
      </div>"""


def comparison_html(
    slug: str,
    before_src: str,
    after_src: str,
    caption: str,
) -> str:
    before_title, after_title = COMPARE_FRAMES.get(slug, ("Before", "After"))
    cap_html = f'<figcaption class="site-compare-caption">{esc(caption)}</figcaption>' if caption else ""
    return f"""
    <figure class="gallery-section site-compare-section">
      <h2 class="gallery-section-title">Before &amp; After</h2>
      <div class="site-compare">
        <figure class="site-compare-item">
          <span class="site-compare-label">Before</span>
          {browser_frame_inner(before_src, before_title, before_title).strip()}
        </figure>
        <figure class="site-compare-item">
          <span class="site-compare-label">After</span>
          {browser_frame_inner(after_src, after_title, after_title).strip()}
        </figure>
      </div>
      {cap_html}
    </figure>"""


def browser_frame_html(src: str, alt: str, title: str, cap_html: str) -> str:
    return f"""
    <figure class="project-image project-image--dashboard">
      {browser_frame_inner(src, alt, title).strip()}
      {cap_html}
    </figure>"""


def build_project(p: dict) -> str:
    slug = p["slug"]
    text = p.get("text") or PROJECT_TEXT.get(slug, [])
    captions = IMAGE_CAPTIONS.get(slug, [])
    layouts = IMAGE_LAYOUT.get(slug, ["full"] * len(p["images"]))

    text_html = ""
    if text:
        text_html = '<div class="project-text">' + "".join(f"<p>{esc(t)}</p>" for t in text) + "</div>"

    images_html = ""
    if slug in GALLERY_GRID:
        grid_items = []
        for i, img in enumerate(p["images"]):
            cap = captions[i] if i < len(captions) else img.get("alt", "") or p["title"]
            alt = cap or p["title"]
            grid_items.append(grid_figure_html(img["src"], alt, cap))
        images_html = f'<div class="project-gallery-grid">{"".join(grid_items)}</div>'
    i = 0
    mobile_section_open = False
    while i < len(p["images"]) and slug not in GALLERY_GRID:
        layout_idx = i
        if slug == "sterling-website" and i >= 2:
            layout_idx = 1
        img_layout = layouts[layout_idx] if layout_idx < len(layouts) else "full"
        if img_layout == "mobile":
            if not mobile_section_open:
                section_title = "AppSheet mobile app"
                if slug == "uniform-inventory-tracking":
                    section_title = "AppSheet mobile app"
                images_html += f"""
    <div class="gallery-section">
      <h2 class="gallery-section-title">{esc(section_title)}</h2>
      <div class="mobile-screenshots">"""
                mobile_section_open = True
            group = []
            while i < len(p["images"]) and (layouts[i] if i < len(layouts) else "full") == "mobile":
                group.append(figure_html(p, i, p["images"][i], "mobile", captions))
                i += 1
            images_html += "".join(group) + """
      </div>
    </div>"""
        elif img_layout == "compare" and i + 1 < len(p["images"]):
            cap = captions[i] if i < len(captions) else ""
            images_html += comparison_html(
                slug,
                p["images"][i]["src"],
                p["images"][i + 1]["src"],
                cap,
            )
            i += 2
        elif img_layout in ("dashboard", "browser"):
            cap_idx = 1 if slug == "sterling-website" and i >= 2 else i
            cap = captions[cap_idx] if cap_idx < len(captions) else p["images"][i].get("alt", "")
            alt = cap or p["title"]
            cap_html = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
            titles = FRAME_TITLES.get(slug, [p["title"]])
            title_idx = 0 if slug == "sterling-website" else i
            frame_title = titles[title_idx] if title_idx < len(titles) else p["title"]
            frame = browser_frame_html(p["images"][i]["src"], alt, frame_title, cap_html)
            if slug == "sterling-website" and img_layout == "browser":
                images_html += f"""
    <div class="gallery-section">
      <h2 class="gallery-section-title">Employment applications</h2>
      {frame.strip()}
    </div>"""
            else:
                images_html += frame
            i += 1
        else:
            cap = captions[i] if i < len(captions) else p["images"][i].get("alt", "")
            alt = cap or p["title"]
            cap_html = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
            images_html += f"""
    <figure class="project-image">
      <img src="../{p['images'][i]['src']}" alt="{esc(alt)}" loading="lazy">
      {cap_html}
    </figure>"""
            i += 1

    back = "design.html" if p["category"] == "design" else "systems.html"

    demo_html = ""
    demos = PROJECT_DEMOS.get(slug, [])
    if demos:
        if isinstance(demos, str):
            demos = [{
                "path": demos,
                "heading": "Try the demo",
                "note": "Interactive preview.",
            }]
        demo_html = "".join(
            f"""
  <section class="project-demo">
    <h2 class="demo-heading">{esc(d["heading"])}</h2>
    <p class="demo-note">{esc(d["note"])}</p>
    <div class="demo-frame-wrap">
      <iframe src="../{d["path"]}" title="{esc(d["heading"])}" loading="lazy"></iframe>
    </div>
  </section>"""
            for d in demos
        )

    gallery_extra_html = ""
    gallery_extra = PROJECT_GALLERY_EXTRA.get(slug)
    if gallery_extra:
        gallery_extra_html = gallery_extra()

    related_html = ""
    if slug in RELATED_LINKS:
        href, label = RELATED_LINKS[slug]
        related_html = f'<p class="project-related">Related: <a href="{href}">{esc(label)}</a></p>'

    live_html = ""
    if p.get("liveUrl"):
        live_label = p.get("liveLabel", "View live site")
        live_html = f'<p class="project-live"><a href="{esc(p["liveUrl"])}" target="_blank" rel="noopener">{esc(live_label)} ↗</a></p>'

    gallery_cls = "project-gallery"
    if slug in GALLERY_GRID:
        gallery_cls = "project-gallery project-gallery--grid"
    elif slug in GALLERY_POLISH:
        gallery_cls = "project-gallery project-gallery--systems"

    body = f"""
  <section class="project-header">
    <a href="../{back}" class="back-link">← Back</a>
    <h1>{esc(p['title'])}</h1>
    <span class="year">{esc(p['year'])}</span>
  </section>
  {text_html}
  {related_html}
  {live_html}
  {demo_html}
  <section class="{gallery_cls}">{images_html}{gallery_extra_html}
  </section>"""
    main_class = "main--with-demo" if slug in PROJECT_DEMOS else ""
    return layout(
        p["title"],
        p["category"],
        body,
        main_class=main_class,
        asset_prefix="../",
        nav_prefix="../",
    )


def build_about() -> str:
    tools_html = ""
    for category, items in CONTENT["about"]["tools"].items():
        tags = "".join(f"<span>{esc(i)}</span>" for i in items)
        tools_html += f"""
      <div class="tool-group">
        <h3>{esc(category)}</h3>
        <div class="tool-tags">{tags}</div>
      </div>"""

    bio_paragraphs = "".join(f"<p>{esc(p)}</p>" for p in CONTENT["about"]["bio"].split("\n\n"))

    resume_path = CONTENT.get("resume", "")
    resume_btn = ""
    if resume_path:
        resume_btn = f'<a class="resume-btn" href="{esc(resume_path)}" download>Download Resume (PDF)</a>'

    education_html = ""
    edu = CONTENT["about"].get("education")
    if isinstance(edu, dict):
        school = esc(edu.get("school", ""))
        location = esc(edu.get("location", ""))
        degrees_html = ""
        for deg in edu.get("degrees", []):
            title = esc(deg.get("title", ""))
            date = esc(deg.get("date", ""))
            if deg.get("majors") or deg.get("minor"):
                majors = esc(deg.get("majors", ""))
                minor = esc(deg.get("minor", ""))
                degrees_html += f"""
        <li class="education-degree">
          <div class="education-degree-title">{title}</div>
          <div class="education-degree-details">
            <span><strong>Majors:</strong> {majors}</span>
            <span class="education-sep">·</span>
            <span><strong>Minor:</strong> {minor}</span>
            <span class="education-sep">·</span>
            <span>{date}</span>
          </div>
        </li>"""
            else:
                degrees_html += f"""
        <li class="education-degree">
          <div class="education-degree-title">{title} <span class="education-date">· {date}</span></div>
        </li>"""
        education_html = f"""
    <div class="education-block">
      <div class="education-school">{school} · {location}</div>
      <ul class="about-list education-list">{degrees_html}
      </ul>
    </div>"""
    elif isinstance(edu, list):
        for item in edu:
            education_html += f"<li>{esc(item)}</li>"
        education_html = f'<ul class="about-list">{education_html}</ul>'

    education_section = ""
    if education_html:
        education_section = f"""
    <h2>Education</h2>
    {education_html}"""

    experience_html = ""
    for job in CONTENT["about"].get("experience", []):
        bullets = "".join(f"<li>{esc(h)}</li>" for h in job.get("highlights", []))
        experience_html += f"""
      <article class="experience-item">
        <h3>{esc(job['title'])}</h3>
        <p class="experience-meta">{esc(job['company'])} · {esc(job['location'])} · {esc(job['dates'])}</p>
        <ul class="about-list">{bullets}</ul>
      </article>"""
    experience_section = ""
    if experience_html:
        experience_section = f"""
    <h2>Experience</h2>
    <div class="experience-grid">{experience_html}</div>"""

    linkedin = CONTENT.get("linkedin", "")
    linkedin_html = ""
    if linkedin:
        job = CONTENT["about"].get("experience", [{}])[0]
        headline = job.get("title", "Digital Transformation & Systems Coordinator")
        company = job.get("company", "Sterling Securities")
        linkedin_html = f"""
    <h2>Connect on LinkedIn</h2>
    <a class="linkedin-card" href="{esc(linkedin)}" target="_blank" rel="noopener">
      <div class="linkedin-card-icon" aria-hidden="true">
        {LINKEDIN_SVG.replace('fill="currentColor"', 'fill="#0A66C2"')}
      </div>
      <div class="linkedin-card-body">
        <div class="linkedin-card-name">{esc(CONTENT['name'])}</div>
        <div class="linkedin-card-headline">{esc(headline)} · {esc(company)}</div>
        <span class="linkedin-card-btn">View profile on LinkedIn →</span>
      </div>
    </a>"""

    job = CONTENT["about"].get("experience", [{}])[0]
    role = job.get("title", "Digital Transformation & Systems Coordinator")

    body = f"""
  <section class="page-header">
    <h1>About</h1>
    {resume_btn}
  </section>
  <section class="about-hero">
    <div class="about-hero-inner">
      <img src="{CONTENT.get('headshot', CONTENT['profilePhoto'])}" alt="{esc(CONTENT['name'])}" class="about-headshot">
      <div class="about-hero-text">
        <h2>{esc(CONTENT['name'])}</h2>
        <p class="about-role">{esc(role)}</p>
      </div>
    </div>
  </section>
  <section class="about-content">
    <div class="about-bio">{bio_paragraphs}</div>
    {experience_section}
    {education_section}
    <h2>Skills & Tools</h2>
    <div class="tools-grid">{tools_html}</div>
    {linkedin_html}
    <p class="connect-cta"><a href="contact.html">Get in touch →</a></p>
  </section>"""
    return layout("About", "about", body)


def build_contact() -> str:
    email = CONTENT.get("email", "")
    phone = CONTENT.get("phone", "")
    linkedin = CONTENT.get("linkedin", "")
    resume = CONTENT.get("resume", "")
    formspree_id = (CONTENT.get("formspreeId") or "").strip()
    site_url = (CONTENT.get("siteUrl") or "").rstrip("/")

    contact_items = []
    if email:
        contact_items.append(f'<li><a href="mailto:{esc(email)}">{esc(email)}</a></li>')
    if phone:
        phone_digits = phone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
        contact_items.append(f'<li><a href="tel:{esc(phone_digits)}">{esc(phone)}</a></li>')
    if linkedin:
        contact_items.append(
            f'<li class="contact-info-linkedin">'
            f'<a class="contact-linkedin" href="{esc(linkedin)}" target="_blank" rel="noopener" aria-label="LinkedIn profile">'
            f'{LINKEDIN_SVG}'
            f"</a></li>"
        )
    if resume:
        contact_items.append(f'<li><a href="{esc(resume)}" download>Download Resume (PDF)</a></li>')

    if formspree_id:
        next_url = f"{site_url}/contact.html?sent=1" if site_url else "contact.html?sent=1"
        form_html = f"""
      <p class="form-success" id="form-success" hidden>Thanks — your message was sent. I&#x27;ll get back to you soon.</p>
      <form class="contact-form" action="https://formspree.io/f/{esc(formspree_id)}" method="POST">
        <input type="hidden" name="_subject" value="Portfolio contact form">
        <input type="hidden" name="_next" value="{esc(next_url)}">
        <label>Name *<input type="text" name="name" required autocomplete="name"></label>
        <label>Email Address *<input type="email" name="email" required autocomplete="email"></label>
        <label>Message *<textarea name="message" rows="6" required></textarea></label>
        <button type="submit">Submit</button>
      </form>"""
    else:
        form_html = f"""
      <form class="contact-form contact-form--disabled">
        <label>Name *<input type="text" name="name" disabled></label>
        <label>Email Address *<input type="email" name="email" disabled></label>
        <label>Message *<textarea name="message" rows="6" disabled></textarea></label>
        <button type="submit" disabled>Submit</button>
      </form>
      <p class="form-note">Email me directly at <a href="mailto:{esc(email)}">{esc(email)}</a>.</p>"""

    body = f"""
  <section class="page-header page-header-stacked">
    <h1>Contact</h1>
    <p class="page-subtitle">Interested in working together? Send me a message.</p>
  </section>
  <div class="contact-layout">
    <aside class="contact-info-card">
      <h2 class="contact-info-title">Contact info</h2>
      <ul class="contact-info-list">
        {"".join(contact_items)}
      </ul>
    </aside>
    <section class="contact-form-section">{form_html}
    </section>
  </div>"""
    return layout("Contact", "contact", body)


def main():
    work_dir = ROOT / "work"
    work_dir.mkdir(exist_ok=True)

    (ROOT / "index.html").write_text(build_home(), encoding="utf-8")
    (ROOT / "about.html").write_text(build_about(), encoding="utf-8")
    (ROOT / "contact.html").write_text(build_contact(), encoding="utf-8")
    (ROOT / "design.html").write_text(build_gallery_page("Graphic Design", "design", "design"), encoding="utf-8")
    (ROOT / "systems.html").write_text(build_gallery_page("Digital Systems", "systems", "systems"), encoding="utf-8")

    for p in CONTENT["projects"]:
        (work_dir / f"{p['slug']}.html").write_text(build_project(p), encoding="utf-8")
        print(f"  {p['slug']}.html")

    print("Site built!")


if __name__ == "__main__":
    main()
