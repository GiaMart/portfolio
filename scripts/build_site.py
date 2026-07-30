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
        "Skills: Cursor · ChatGPT · Prompt Engineering · Google Workspace · Render",
        "The challenge: The original Google Sites portal worked at first, but couldn't support a dynamic pay calendar, structured form routing, or an admin review queue tied to company data.",
        "My approach: I'm not a traditional developer — I use AI as a build partner. I scoped the requirements, designed the UX, and worked iteratively in Cursor with AI to build, test, and deploy Employee Portal 2.0 on a live domain.",
        "What's included: Biweekly pay schedule calendar, 7 employee request forms, email notifications on submission, and an admin submissions queue — all connected to the same company database as scheduling, uniforms, and SORA tracking.",
        "Why this matters: This project shows how someone with operations and IT knowledge can ship production software by combining clear problem-solving with AI-assisted development — not by writing every line of code from scratch.",
    ],
    "operations-portal": [
        "Skills: Cursor · ChatGPT · Prompt Engineering · Flask · SQLite · Render",
        "The problem: Sterling ran on spreadsheets and disconnected tools — guards, client sites, billing, SORA certifications, uniforms, and employee requests had no single source of truth.",
        "My approach: I mapped the ops workflow with leadership, then built the admin app iteratively in Cursor with AI — database schema, Flask routes, Bootstrap UI, and production deployment on Render.",
        "What's included: Operations dashboard with live KPIs, client and site management, guard roster, SORA compliance tracking, uniform inventory, billing, shift assignments, exportable reports, and an employee portal submission queue — all in one database.",
        "Access control: I set up multiple operations sign-in accounts with role-based access — IT full admin, HR for portal submissions, and Finance for invoices and billing.",
        "Deployment: Live on Render with Gunicorn and persistent storage. Email notifications fire when employees submit portal requests.",
        "How I used AI: Cursor helped me scaffold routes, debug SQL, refine templates, and iterate quickly. I owned the requirements, UX, and testing — AI accelerated the build.",
    ],
    "sterling-website": [
        "Skills: Squarespace · Web Design · Branding · Content Strategy",
        "The challenge: Sterling's previous website was dated and static. It listed an Employment page in the nav, but there was no way to collect applications online or review submissions — hiring relied on phone calls and scattered email attachments.",
        "What I did: Redesigned and rebuilt sterlingsecurityguards.com on Squarespace — modern homepage, service sections, and a dedicated Employment Opportunities page with an application form (resume upload, contact info, armed/unarmed status, and more).",
        "Employment applications: Submissions now go directly into Squarespace, where leadership can review applicants in one place. That workflow never existed on the old site — the Employment link was there, but it didn't capture or organize applications.",
        "Outcome: A mobile-friendly public site that presents Sterling's services clearly, routes consultation requests, and gives hiring a structured pipeline for new guard applications.",
    ],
}

PROJECT_DEMOS = {
    "employee-portal-2": [
        {
            "path": "demos/employee-portal-2/index.html",
            "heading": "Try the employee portal",
            "note": "Interactive preview — navigate the portal, open a form, and submit a simulated request.",
        },
    ],
    "operations-portal": [
        {
            "path": "demos/operations-portal/index.html",
            "heading": "Try the operations portal",
            "note": "Interactive preview — use the nav to explore the dashboard, clients, guards, SORA, invoices, reports, portal submissions, and login accounts. Sample data only; changes are simulated.",
        },
    ],
}

RELATED_LINKS = {
    "employee-portal-2": ("operations-portal.html", "Operations Portal — admin dashboard & submission queue"),
    "operations-portal": ("employee-portal-2.html", "Employee Portal 2.0 — guard-facing portal"),
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
    "employee-portal",
    "scheduling-automation",
    "sterling-website",
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
    "ariannas-angels": ["2024 Gift", "", "2023 Gift"],
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
    i = 0
    mobile_section_open = False
    while i < len(p["images"]):
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

    related_html = ""
    if slug in RELATED_LINKS:
        href, label = RELATED_LINKS[slug]
        related_html = f'<p class="project-related">Related: <a href="{href}">{esc(label)}</a></p>'

    live_html = ""
    if p.get("liveUrl"):
        live_label = p.get("liveLabel", "View live site")
        live_html = f'<p class="project-live"><a href="{esc(p["liveUrl"])}" target="_blank" rel="noopener">{esc(live_label)} ↗</a></p>'

    gallery_cls = "project-gallery"
    if slug in GALLERY_POLISH:
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
  <section class="{gallery_cls}">{images_html}
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
        <input type="text" name="_gotcha" class="contact-form-honeypot" tabindex="-1" autocomplete="off" aria-hidden="true">
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
