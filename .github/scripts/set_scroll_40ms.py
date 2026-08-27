from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")

replacements = [
    ('const AUTO_SCROLL_INTERVAL_MS = 30;', 'const AUTO_SCROLL_INTERVAL_MS = 40;'),
    ('const CAROUSEL_ANIMATION_MS = 30;', 'const CAROUSEL_ANIMATION_MS = 40;'),
    ('transform .03s linear,', 'transform .04s linear,'),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f"not found: {old}")
    text = text.replace(old, new)

p.write_text(text, encoding="utf-8")
