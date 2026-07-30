"""Generate square cover thumbnails for Digital Systems portfolio projects."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "images"
SIZE = 800

CHROME_CANDIDATES = (
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
)

PORTAL_DEMO = ROOT / "demos" / "employee-portal-2" / "index.html"
OPS_DEMO = ROOT / "demos" / "operations-portal" / "index.html"
STERLING_SITE = "https://www.sterlingsecurityguards.com/"


def find_browser() -> Path | None:
    for path in CHROME_CANDIDATES:
        if path.exists():
            return path
    return None


def save_cover(img: Image.Image, slug: str) -> Path:
    out = IMAGES / slug / "cover.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    rgb = img.convert("RGB") if img.mode != "RGB" else img
    rgb.resize((SIZE, SIZE), Image.Resampling.LANCZOS).save(out, "PNG", optimize=True)
    print(f"  {out.relative_to(ROOT)}")
    return out


def crop_square(img: Image.Image, *, left: int = 0, top: int = 0, side: int | None = None) -> Image.Image:
    side = side or min(img.width - left, img.height - top)
    return img.crop((left, top, left + side, top + side))


def screenshot_url(url: str, *, window: str = "1400,920") -> Image.Image:
    browser = find_browser()
    if browser is None:
        raise RuntimeError("Chrome/Edge not found — cannot capture screenshot")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={window}",
        f"--screenshot={tmp_path}",
        url,
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    with Image.open(tmp_path) as img:
        captured = img.copy()
    tmp_path.unlink(missing_ok=True)
    return captured


def screenshot_demo(path: Path, *, top: int = 38) -> Image.Image:
    img = screenshot_url(path.resolve().as_uri())
    side = min(img.width, img.height - top)
    left = (img.width - side) // 2
    return crop_square(img, left=left, top=top, side=side)


def cover_employee_portal_2() -> Image.Image:
    return screenshot_demo(PORTAL_DEMO, top=72)


def cover_operations_portal() -> Image.Image:
    return screenshot_demo(OPS_DEMO, top=38)


def cover_uniform() -> Image.Image:
    src = IMAGES / "uniform-inventory-tracking" / "uniform-inventory-tracking-0.png"
    img = Image.open(src)
    return crop_square(img, left=0, top=0, side=min(img.width, img.height))


def cover_scheduling() -> Image.Image:
    src = IMAGES / "scheduling-automation" / "scheduling-automation-0.png"
    img = Image.open(src)
    side = min(img.width, img.height)
    left = max(0, min(620, img.width - side))
    return crop_square(img, left=left, top=0, side=side)


def cover_employee_portal() -> Image.Image:
    gif_path = IMAGES / "employee-portal" / "employee-portal-0.gif"
    with Image.open(gif_path) as gif:
        gif.seek(0)
        frame = gif.convert("RGBA")
    background = Image.new("RGB", frame.size, "#ffffff")
    background.paste(frame, mask=frame.split()[3])
    return crop_square(background, left=0, top=0, side=min(background.width, background.height))


def cover_sterling_website() -> Image.Image:
    img = screenshot_url(STERLING_SITE, window="1440,1200")
    return crop_square(img, left=0, top=0, side=min(img.width, img.height))


def save_sterling_gallery() -> None:
    out_dir = IMAGES / "sterling-website"
    out_dir.mkdir(parents=True, exist_ok=True)

    home = screenshot_url(STERLING_SITE, window="1440,1400")
    home.crop((0, 0, home.width, min(900, home.height))).save(
        out_dir / "sterling-website-0.png", "PNG", optimize=True
    )
    print(f"  {out_dir.relative_to(ROOT) / 'sterling-website-0.png'}")

    services = screenshot_url(STERLING_SITE, window="1440,2800")
    services.crop((0, 700, services.width, min(1700, services.height))).save(
        out_dir / "sterling-website-1.png", "PNG", optimize=True
    )
    print(f"  {out_dir.relative_to(ROOT) / 'sterling-website-1.png'}")


def main() -> None:
    covers = {
        "operations-portal": cover_operations_portal,
        "employee-portal-2": cover_employee_portal_2,
        "sterling-website": cover_sterling_website,
        "uniform-inventory-tracking": cover_uniform,
        "scheduling-automation": cover_scheduling,
        "employee-portal": cover_employee_portal,
    }

    print("Generating system project covers...")
    for slug, builder in covers.items():
        save_cover(builder(), slug)

    print("Capturing Sterling website gallery...")
    save_sterling_gallery()

    for stale in (
        IMAGES / "employee-portal-2" / "cover-test.png",
        IMAGES / "employee-portal" / "frame-0.png",
    ):
        stale.unlink(missing_ok=True)

    print("Done.")


if __name__ == "__main__":
    main()
