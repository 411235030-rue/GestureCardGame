from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")

replacements = [
    ('const AUTO_SCROLL_INTERVAL_MS = 600;', 'const AUTO_SCROLL_INTERVAL_MS = 30;'),
    ('const CAROUSEL_ANIMATION_MS = 380;', 'const CAROUSEL_ANIMATION_MS = 30;'),
    ('transform .38s cubic-bezier(.2,.8,.2,1),', 'transform .03s linear,'),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f"not found: {old}")
    text = text.replace(old, new)

p.write_text(text, encoding="utf-8")
