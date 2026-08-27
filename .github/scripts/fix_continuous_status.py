from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")

old = '''      gestureToggle.classList.add("off");
      gestureStatus.textContent = "手勢辨識已關閉";

      stopAutoScroll();
      gestureArmed = false;'''

new = '''      gestureToggle.classList.add("off");

      stopAutoScroll();
      gestureArmed = false;
      gestureStatus.textContent = "手勢辨識已關閉";'''

if old not in text:
    raise SystemExit("gesture off status block not found")

p.write_text(text.replace(old, new, 1), encoding="utf-8")
