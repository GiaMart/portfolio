"""Generate LinkedIn featured and GitHub profile banner images."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images"

WHITE = "#ffffff"
TEXT = "#111111"
MUTED = "#666666"
ACCENT = "#2563eb"
DIVIDER = "#d1d5db"
TOP_BAR = "#2563eb"

FONT_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_ITALIC_BOLD = "C:/Windows/Fonts/arialbi.ttf"
LOGO_SOURCE = OUT / "gm-logo.png"


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def draw_banner(
    *,
    width: int,
    height: int,
    label: str,
    monogram_size: int,
    name_size: int,
    title_size: int,
    label_size: int,
    divider_height: int,
    content_x: int,
    divider_x: int,
    top_bar: int = 6,
) -> Image.Image:
    img = Image.new("RGB", (width, height), WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle((0, 0, width, top_bar), fill=TOP_BAR)

    monogram_font = load_font(FONT_ITALIC_BOLD, monogram_size)
    name_font = load_font(FONT_BOLD, name_size)
    title_font = load_font(FONT_REG, title_size)
    label_font = load_font(FONT_REG, label_size)

    monogram = "GM"
    monogram_bbox = draw.textbbox((0, 0), monogram, font=monogram_font)
    monogram_w = monogram_bbox[2] - monogram_bbox[0]
    monogram_h = monogram_bbox[3] - monogram_bbox[1]
    monogram_x = divider_x - monogram_w - (divider_x - content_x) // 2
    monogram_y = (height - monogram_h) // 2 - 4
    draw.text((monogram_x, monogram_y), monogram, fill=TEXT, font=monogram_font)

    divider_top = (height - divider_height) // 2
    draw.line((divider_x, divider_top, divider_x, divider_top + divider_height), fill=DIVIDER, width=2)

    text_x = divider_x + 48
    name = "Gia Martini"
    title = "Digital Systems & Design"

    name_bbox = draw.textbbox((0, 0), name, font=name_font)
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    label_bbox = draw.textbbox((0, 0), label, font=label_font)

    name_h = name_bbox[3] - name_bbox[1]
    title_h = title_bbox[3] - title_bbox[1]
    label_h = label_bbox[3] - label_bbox[1]
    gap = max(8, height // 40)
    underline_gap = max(10, height // 36)
    underline_w = max(72, width // 18)
    block_h = name_h + gap + title_h + underline_gap + 4 + gap + label_h
    start_y = (height - block_h) // 2

    draw.text((text_x, start_y), name, fill=TEXT, font=name_font)
    draw.text((text_x, start_y + name_h + gap), title, fill=MUTED, font=title_font)

    underline_y = start_y + name_h + gap + title_h + underline_gap
    draw.line((text_x, underline_y, text_x + underline_w, underline_y), fill=ACCENT, width=3)
    draw.text((text_x, underline_y + gap), label, fill=ACCENT, font=label_font)

    return img


def linkedin_featured() -> Image.Image:
    return linkedin_layout(label="Portfolio")


def linkedin_layout(*, label: str) -> Image.Image:
    """Shared wide banner layout — matches LinkedIn featured proportions."""
    return draw_banner(
        width=1584,
        height=396,
        label=label,
        monogram_size=112,
        name_size=54,
        title_size=28,
        label_size=24,
        divider_height=150,
        content_x=120,
        divider_x=430,
    )


def github_cover() -> Image.Image:
    return draw_banner(
        width=1280,
        height=640,
        label="GitHub",
        monogram_size=150,
        name_size=62,
        title_size=32,
        label_size=28,
        divider_height=220,
        content_x=110,
        divider_x=390,
        top_bar=8,
    )


def github_social_preview() -> Image.Image:
    """Same wide banner style as Portfolio — label reads GitHub."""
    return linkedin_layout(label="GitHub")


def load_gm_logo() -> Image.Image:
    logo = Image.open(LOGO_SOURCE).convert("RGBA")
    return logo


def draw_gm_icon(size: int) -> Image.Image:
    logo = load_gm_logo()
    canvas = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    pad = max(2, size // 10)
    max_w = size - pad * 2
    max_h = size - pad * 2
    scale = min(max_w / logo.width, max_h / logo.height)
    resized = logo.resize(
        (max(1, int(logo.width * scale)), max(1, int(logo.height * scale))),
        Image.Resampling.LANCZOS,
    )
    x = (size - resized.width) // 2
    y = (size - resized.height) // 2
    canvas.paste(resized, (x, y), resized)
    return canvas.convert("RGB")


def save_favicons() -> None:
    icon16 = draw_gm_icon(16)
    icon32 = draw_gm_icon(32)
    icon180 = draw_gm_icon(180)

    icon32.save(ROOT / "favicon-32x32.png", "PNG", optimize=True)
    icon180.save(ROOT / "apple-touch-icon.png", "PNG", optimize=True)
    icon32.save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32)],
        append_images=[icon16],
    )
    print(f"  favicon.ico")
    print(f"  favicon-32x32.png")
    print(f"  apple-touch-icon.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    targets = {
        "linkedin-featured.png": linkedin_featured(),
        "github-cover.png": github_cover(),
        "github-social-preview.png": github_social_preview(),
    }
    for filename, image in targets.items():
        path = OUT / filename
        image.save(path, "PNG", optimize=True)
        print(f"  {path.relative_to(ROOT)} ({image.width}x{image.height})")
    save_favicons()
    print("Profile banners and favicons generated.")


if __name__ == "__main__":
    main()
