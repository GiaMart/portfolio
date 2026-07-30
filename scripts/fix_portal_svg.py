from pathlib import Path

p = Path(__file__).resolve().parents[1] / "images" / "employee-portal-2" / "cover.svg"
text = p.read_text(encoding="utf-8", errors="replace")
clean = "".join(ch if (ord(ch) >= 32 or ch in "\n\r\t") else "–" for ch in text)
clean = clean.replace("\ufffd", "·")
for old, new in (
    ('" Uniform', "• Uniform"),
    ('" ID', "• ID"),
    ('" Contact', "• Contact"),
):
    clean = clean.replace(old, new)
p.write_text(clean, encoding="utf-8")
print("svg cleaned")
