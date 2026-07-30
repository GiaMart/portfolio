"""Scrape Adobe Portfolio content and download assets."""
import json
import re
import urllib.request
from pathlib import Path

BASE = "https://giamartini.myportfolio.com"
ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "images"
CONTENT_DIR = ROOT / "content"

PAGES = [
    {"slug": "seton-hall", "title": "Seton Hall", "category": "design", "year": "2022"},
    {"slug": "2021", "title": "NBA", "category": "design", "year": "2021"},
    {"slug": "art-work-1", "title": "HS & College", "category": "design", "year": "2019"},
    {"slug": "commissions", "title": "Commissions", "category": "design", "year": "2022"},
    {"slug": "sterling", "title": "Sterling", "category": "design", "year": "2025"},
    {"slug": "ariannas-angels", "title": "Volunteer", "category": "design", "year": "2024"},
    {"slug": "misc", "title": "Misc.", "category": "design", "year": "2022"},
    {"slug": "uniform-inventory-tracking", "title": "Uniform Inventory Tracking", "category": "systems", "year": "2025"},
    {"slug": "employee-portal", "title": "Employee Portal", "category": "systems", "year": "2025"},
    {"slug": "scheduling-automation", "title": "Scheduling Automation", "category": "systems", "year": "2025"},
]

THUMBNAILS = {
    "seton-hall": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/68e97a88-d371-4175-93ad-6c5fe1f55ecb_car_1x1.jpg?h=e920178d7bdd987704decc9ab3c4699e",
    "2021": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/a285d108-34a7-4331-8226-2b758783d327_car_1x1.jpg?h=5cf93386cc219c265217d0082a395473",
    "art-work-1": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/c22eaaab-4ed2-4df3-9498-011c05414c39_car_1x1.jpg?h=4c27c44e42f932200a6229128d917f79",
    "commissions": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/b04653d2-0770-431d-b013-d047007136bc_car_1x1.jpg?h=6ebfeedccab982d01dcec3d46c2c4361",
    "sterling": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/8ce5d24c-1151-4561-8b9e-fa18c655759c_car_1x1.jpg?h=2890be8671d4f9d3094d4e8f929cc652",
    "ariannas-angels": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/a65784bb-7e58-47d6-87ef-0910d1290528_car_1x1.png?h=98e603324fa20888dfb002213a499e49",
    "misc": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/d770741b-e8dc-4650-b95f-bcde00e7a08a_car_1x1.jpg?h=0a211cc43bb1d35c6922b87382f88d72",
    "uniform-inventory-tracking": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/8415b2d3-55cc-4cfe-b1da-7be3b3c34651_rwc_0x0x1024x1024.png?h=af28c770ec4b79bc71518d1d9f1299ba",
    "employee-portal": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/308301a5-3172-4402-b3ad-7ca9b0c131cf_rwc_0x0x1024x1024.png?h=538c0f78cc0063f7499c3be109a93576",
    "scheduling-automation": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/11daa52f-57e5-46a9-930d-ed0e173ec6f8_rwc_0x0x1024x1024.png?h=5527b46681ca8b9732e6c34cd5e20557",
}

PROFILE_PHOTO = "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/bf7efdd0-ba47-401d-929e-eff20f36815a_rwc_108x108x807x807x4096.png?h=863206bf0781cc2b31c9e34debfd3d12"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())


def ext_from_url(url: str) -> str:
    m = re.search(r"\.(jpg|jpeg|png|webp|gif)", url, re.I)
    if not m:
        return ".jpg"
    ext = m.group(1).lower()
    return ".jpg" if ext == "jpeg" else f".{ext}"


def pick_best_url(html: str, uuid: str) -> str | None:
    pattern = re.compile(
        rf"https://cdn\.myportfolio\.com/[^\"']*{uuid}[^\"']*_rw_(\d+)\.(jpg|png|webp)[^\"']*",
        re.I,
    )
    matches = list(pattern.finditer(html))
    if not matches:
        return None
    best = max(matches, key=lambda m: int(m.group(1)))
    return best.group(0).split('"')[0].split("'")[0]


def extract_images(html: str) -> list[dict]:
    items = []
    seen: set[str] = set()
    img_pattern = re.compile(
        r'<img[^>]*(?:alt="([^"]*)")?[^>]*(?:data-src="([^"]+)"|src="(https://cdn\.myportfolio\.com[^"]+)")',
        re.I,
    )
    for match in img_pattern.finditer(html):
        alt = match.group(1) or ""
        url = match.group(2) or match.group(3)
        if not url or "data:image" in url or "_108x108" in url or "_carw_" in url:
            continue
        uuid_match = re.search(r"/([a-f0-9-]{36})_", url)
        if not uuid_match:
            continue
        uuid = uuid_match.group(1)
        if uuid in seen:
            continue
        seen.add(uuid)
        best = pick_best_url(html, uuid) or url
        items.append({"alt": alt, "url": best})
    return items


def extract_text(html: str) -> list[str]:
    main = re.search(r"<main[\s\S]*?</main>", html)
    scope = main.group(0) if main else html
    parts = []
    for m in re.finditer(r"<p[^>]*>([\s\S]*?)</p>", scope):
        text = m.group(1)
        text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
        text = re.sub(r"<[^>]+>", "", text)
        text = text.replace("&nbsp;", " ").replace("&amp;", "&").strip()
        if text and "Adobe Portfolio" not in text:
            parts.append(text)
    return parts


def scrape_page(page: dict) -> dict:
    slug = page["slug"]
    print(f"Scraping {slug}...")
    html = fetch(f"{BASE}/{slug}")
    images_raw = extract_images(html)
    text = extract_text(html)

    local_images = []
    for i, img in enumerate(images_raw):
        ext = ext_from_url(img["url"])
        filename = f"{slug}-{i}{ext}"
        rel = f"images/{slug}/{filename}"
        dest = ROOT / rel
        try:
            download(img["url"], dest)
            print(f"  OK {filename}")
        except Exception as e:
            print(f"  FAIL {filename}: {e}")
            rel = img["url"]
        local_images.append({"alt": img["alt"], "src": rel})

    thumb_url = THUMBNAILS[slug]
    thumb_ext = ext_from_url(thumb_url)
    thumb_rel = f"images/{slug}/thumb{thumb_ext}"
    try:
        download(thumb_url, ROOT / thumb_rel)
    except Exception:
        thumb_rel = local_images[0]["src"] if local_images else thumb_url

    return {
        **page,
        "thumbnail": thumb_rel,
        "text": text,
        "images": local_images,
    }


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)

    download(PROFILE_PHOTO, ROOT / "images" / "profile.png")

    projects = [scrape_page(p) for p in PAGES]

    site = {
        "name": "Gia Martini",
        "tagline": "I design clean, engaging visuals and build practical digital systems that solve real business problems.",
        "skills": {
            "design": "Flyers, logos, digital ads, video, branding",
            "systems": "Google Workspace automation, dashboards, no-code apps",
        },
        "profilePhoto": "images/profile.png",
        "about": {
            "bio": (
                "Hi, I'm Gia Martini — a creative problem-solver with a passion for digital systems, "
                "workflow automation, and clean design.\n\n"
                "I hold an MBA in Information Technology Management and a B.S.B. in Sports Management & Marketing "
                "from Seton Hall University. My work bridges the gap between technology and operations: I build "
                "no-code solutions that streamline business processes and support internal teams, while also designing "
                "user-friendly visuals and branded assets.\n\n"
                "Whether it's launching a company website on Squarespace, creating a centralized employee portal with "
                "Google Sites, or developing a custom AppSheet app with QR checkouts, I approach every project with "
                "the same mindset: how can I make this easier, cleaner, and more effective?"
            ),
            "tools": {
                "Workflow & Automation": [
                    "Google Sheets", "Google Forms", "Zapier", "AppSheet", "Google Apps Script"
                ],
                "Data & Docs": ["Excel", "Word", "ADP Workforce Now"],
                "Design & Media": ["Adobe Photoshop", "Premiere Pro", "Canva"],
                "Web & CMS": ["Squarespace", "Google Sites"],
                "Other": ["PowerBI", "Tableau", "SQL", "Python (basic)", "PC Building & Troubleshooting"],
            },
        },
        "projects": projects,
    }

    out = CONTENT_DIR / "site.json"
    out.write_text(json.dumps(site, indent=2), encoding="utf-8")
    print(f"\nDone — {len(projects)} projects saved to {out}")


if __name__ == "__main__":
    main()
