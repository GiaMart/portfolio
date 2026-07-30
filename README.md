# Gia Martini Portfolio

Personal portfolio migrated from Adobe Portfolio. Static HTML site — no build tools required to view.

## What's included

- **10 projects** — 7 Graphic Design + 3 Digital Systems
- All images downloaded locally to `images/`
- About page with bio and tools
- Contact page (form placeholder — wire up Formspree before launch)

## View locally

**Easiest way:** double-click `start-server.bat` in this folder.

Or in a terminal:

```bash
python -m http.server 5500
```

Then open:

- **Homepage:** http://localhost:5500/
- **Employee Portal 2.0 demo:** http://localhost:5500/work/employee-portal-2.html

If port 5500 is busy, try `8080` or another port number.

## Re-scrape from Adobe Portfolio

If you update your Adobe site and want to pull fresh content:

```bash
python scripts/scrape_portfolio.py
python scripts/build_site.py
```

## Store in GitHub (edit on any device)

This project is ready to push to your **personal GitHub account**.

### One-time setup on this PC

1. Install [Git for Windows](https://git-scm.com/download/win) (use default options).
2. Create a new repo on GitHub — go to [github.com/new](https://github.com/new) while logged into your **personal** account.
   - Name it something like `portfolio` or `giamartini-portfolio`
   - Choose **Private** or **Public** (public is fine for job hunting)
   - Do **not** add a README — this folder already has one
3. In a terminal, from this folder:

```bash
git init
git add .
git commit -m "Initial portfolio migration from Adobe"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/portfolio.git
git push -u origin main
```

Replace `YOUR_USERNAME/portfolio` with your actual repo path.

### On your other devices

```bash
git clone https://github.com/YOUR_USERNAME/portfolio.git
cd portfolio
python -m http.server 8080
```

Edit files, then sync:

```bash
git add .
git commit -m "Update project descriptions"
git push
```

On another device, pull the latest:

```bash
git pull
```

### What to edit

| Goal | Edit this |
|---|---|
| Change bio or tools | `content/site.json` → run `python scripts/build_site.py` |
| Change styling | `css/style.css` |
| Change a project page directly | `work/your-project.html` |
| Add images | Put in `images/` and update `content/site.json` |

### Free live site with GitHub Pages

After pushing, enable **Settings → Pages → Deploy from branch → main → / (root)**. Your site will be at:

`https://YOUR_USERNAME.github.io/portfolio/`

## Deploy elsewhere

Upload the folder to any static host (Netlify, Vercel, Cloudflare Pages). Point your domain when ready.

## Next steps

- [ ] Buy a domain (e.g. giamartini.com)
- [ ] Wire contact form to Formspree or similar
- [ ] Design revamp (typography, colors, case study layout)
- [ ] Add resume PDF to About page
