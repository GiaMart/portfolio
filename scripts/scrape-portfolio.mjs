import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const OUT = path.join(ROOT, "content");
const IMG = path.join(ROOT, "public", "images");

const PAGES = [
  { slug: "seton-hall", title: "Seton Hall", category: "design", year: "2022" },
  { slug: "2021", title: "NBA", category: "design", year: "2021" },
  { slug: "art-work-1", title: "HS & College", category: "design", year: "2019" },
  { slug: "commissions", title: "Commissions", category: "design", year: "2022" },
  { slug: "sterling", title: "Sterling", category: "design", year: "2025" },
  { slug: "ariannas-angels", title: "Volunteer", category: "design", year: "2024" },
  { slug: "misc", title: "Misc.", category: "design", year: "2022" },
  { slug: "uniform-inventory-tracking", title: "Uniform Inventory Tracking", category: "systems", year: "2025" },
  { slug: "employee-portal", title: "Employee Portal", category: "systems", year: "2025" },
  { slug: "scheduling-automation", title: "Scheduling Automation", category: "systems", year: "2025" },
];

const THUMBNAILS = {
  "seton-hall": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/68e97a88-d371-4175-93ad-6c5fe1f55ecb_carw_1x1x32.jpg?h=bac7b88a70e60ee7f62f8eb839bf92f7",
  "2021": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/a285d108-34a7-4331-8226-2b758783d327_carw_1x1x32.jpg?h=5cf93386cc219c265217d0082a395473",
  "art-work-1": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/c22eaaab-4ed2-4df3-9498-011c05414c39_carw_1x1x32.jpg?h=4c27c44e42f932200a6229128d917f79",
  commissions: "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/b04653d2-0770-431d-b013-d047007136bc_carw_1x1x32.jpg?h=6ebfeedccab982d01dcec3d46c2c4361",
  sterling: "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/8ce5d24c-1151-4561-8b9e-fa18c655759c_carw_1x1x32.jpg?h=2890be8671d4f9d3094d4e8f929cc652",
  "ariannas-angels": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/a65784bb-7e58-47d6-87ef-0910d1290528_carw_1x1x32.png?h=98e603324fa20888dfb002213a499e49",
  misc: "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/d770741b-e8dc-4650-b95f-bcde00e7a08a_carw_1x1x32.jpg?h=0a211cc43bb1d35c6922b87382f88d72",
  "uniform-inventory-tracking": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/8415b2d3-55cc-4cfe-b1da-7be3b3c34651_rwc_0x0x1024x1024x32.png?h=af28c770ec4b79bc71518d1d9f1299ba",
  "employee-portal": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/308301a5-3172-4402-b3ad-7ca9b0c131cf_rwc_0x0x1024x1024x32.png?h=538c0f78cc0063f7499c3be109a93576",
  "scheduling-automation": "https://cdn.myportfolio.com/49061339-b9d9-4688-8a59-78f830b9f5a2/11daa52f-57e5-46a9-930d-ed0e173ec6f8_rwc_0x0x1024x1024x32.png?h=5527b46681ca8b9732e6c34cd5e20557",
};

const BASE = "https://giamartini.myportfolio.com";

function pickBestUrl(html, uuid) {
  const regex = new RegExp(
    `https://cdn\\.myportfolio\\.com/[^"']*${uuid}[^"']*_rw_(\\d+)\\.(jpg|png|webp)[^"']*`,
    "g"
  );
  const matches = [...html.matchAll(regex)];
  if (!matches.length) return null;
  let best = matches[0][0];
  let bestSize = parseInt(matches[0][1], 10);
  for (const m of matches) {
    const size = parseInt(m[1], 10);
    if (size > bestSize) {
      bestSize = size;
      best = m[0];
    }
  }
  return best.split('"')[0].split("'")[0];
}

function extractImages(html) {
  const items = [];
  const blockRegex =
    /<img[^>]*(?:alt="([^"]*)")?[^>]*(?:data-src="([^"]+)"|src="(https:\/\/cdn\.myportfolio\.com[^"]+)")[^>]*>/g;
  let match;
  const seen = new Set();

  while ((match = blockRegex.exec(html)) !== null) {
    const alt = match[1] || "";
    const url = match[2] || match[3];
    if (!url || url.includes("data:image") || url.includes("_108x108") || url.includes("_carw_")) continue;

    const uuidMatch = url.match(/\/([a-f0-9-]{36})_/);
    if (!uuidMatch) continue;
    const uuid = uuidMatch[1];
    if (seen.has(uuid)) continue;
    seen.add(uuid);

    const best = pickBestUrl(html, uuid) || url;
    items.push({ alt, url: best });
  }

  return items;
}

function extractText(html) {
  const main = html.match(/<main[\s\S]*?<\/main>/)?.[0] || html;
  const parts = [];
  const pRegex = /<p[^>]*>([\s\S]*?)<\/p>/g;
  let m;
  while ((m = pRegex.exec(main)) !== null) {
    const text = m[1]
      .replace(/<br\s*\/?>/gi, "\n")
      .replace(/<[^>]+>/g, "")
      .replace(/&nbsp;/g, " ")
      .replace(/&amp;/g, "&")
      .trim();
    if (text && !text.includes("Adobe Portfolio")) parts.push(text);
  }
  return parts;
}

async function download(url, dest) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed ${url}: ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, buf);
  return dest;
}

function extFromUrl(url) {
  const m = url.match(/\.(jpg|jpeg|png|webp|gif)/i);
  return m ? `.${m[1].toLowerCase().replace("jpeg", "jpg")}` : ".jpg";
}

async function scrapePage(page) {
  console.log(`Scraping ${page.slug}...`);
  const res = await fetch(`${BASE}/${page.slug}`);
  const html = await res.text();
  const images = extractImages(html);
  const text = extractText(html);

  const localImages = [];
  for (let i = 0; i < images.length; i++) {
    const img = images[i];
    const ext = extFromUrl(img.url);
    const filename = `${page.slug}-${i}${ext}`;
    const rel = `/images/${page.slug}/${filename}`;
    const dest = path.join(IMG, page.slug, filename);
    try {
      await download(img.url, dest);
      localImages.push({ alt: img.alt, src: rel });
      console.log(`  ✓ ${filename}`);
    } catch (e) {
      console.warn(`  ✗ ${filename}: ${e.message}`);
      localImages.push({ alt: img.alt, src: img.url });
    }
  }

  let thumb = `/images/${page.slug}/thumb${extFromUrl(THUMBNAILS[page.slug])}`;
  try {
    await download(
      THUMBNAILS[page.slug].replace("_carw_1x1x32", "_car_1x1").replace("_rwc_0x0x1024x1024x32", "_rwc_0x0x1024x1024"),
      path.join(IMG, page.slug, `thumb${extFromUrl(THUMBNAILS[page.slug])}`)
    );
  } catch {
    thumb = localImages[0]?.src || THUMBNAILS[page.slug];
  }

  return {
    slug: page.slug,
    title: page.title,
    category: page.category,
    year: page.year,
    thumbnail: thumb,
    text,
    images: localImages,
  };
}

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  fs.mkdirSync(IMG, { recursive: true });

  const projects = [];
  for (const page of PAGES) {
    projects.push(await scrapePage(page));
  }

  const site = {
    name: "Gia Martini",
    tagline:
      "I design clean, engaging visuals and build practical digital systems that solve real business problems.",
    skills: {
      design: "Flyers, logos, digital ads, video, branding",
      systems: "Google Workspace automation, dashboards, no-code apps",
    },
    about: {
      bio: `Hi, I'm Gia Martini — a creative problem-solver with a passion for digital systems, workflow automation, and clean design.

I hold an MBA in Information Technology Management and a B.S.B. in Sports Management & Marketing from Seton Hall University. My work bridges the gap between technology and operations: I build no-code solutions that streamline business processes and support internal teams, while also designing user-friendly visuals and branded assets.

Whether it's launching a company website on Squarespace, creating a centralized employee portal with Google Sites, or developing a custom AppSheet app with QR checkouts, I approach every project with the same mindset: how can I make this easier, cleaner, and more effective?`,
      tools: {
        "Workflow & Automation": ["Google Sheets", "Google Forms", "Zapier", "AppSheet", "Google Apps Script"],
        "Data & Docs": ["Excel", "Word", "ADP Workforce Now"],
        "Design & Media": ["Adobe Photoshop", "Premiere Pro", "Canva"],
        "Web & CMS": ["Squarespace", "Google Sites"],
        Other: ["PowerBI", "Tableau", "SQL", "Python (basic)", "PC Building & Troubleshooting"],
      },
    },
    projects,
  };

  fs.writeFileSync(path.join(OUT, "site.json"), JSON.stringify(site, null, 2));
  console.log(`\nDone! ${projects.length} projects scraped.`);
}

main().catch(console.error);
