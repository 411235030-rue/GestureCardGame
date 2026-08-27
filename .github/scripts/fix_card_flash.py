from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")

old = '''    function updateCard() {
      const data = cards[currentIndex];

      backNumber.textContent = currentIndex + 1;

      cardImage.src = data.image;
      cardImage.alt =
        `CARD ${String(currentIndex + 1).padStart(2, "0")}`;

      cardFront.className = "card-face card-front";

      updateDeckPeeks();

      // 切到任何卡片時，一律先回到卡背。
      // 例如：2 翻開 → 3 → 回到 2，2 會重新是覆蓋狀態。
      card.className = "card";
      if (data.rarity === "SR") {
        card.classList.add("sr");
      }
    }'''

new = '''    function updateCard() {
      const data = cards[currentIndex];

      // 一定要先清掉上一張的 flipped 狀態，再更換圖片。
      // 否則圖片已快取時，下一張正面會在回到卡背前閃一下。
      card.className = "card";
      if (data.rarity === "SR") {
        card.classList.add("sr");
      }

      backNumber.textContent = currentIndex + 1;

      cardImage.src = data.image;
      cardImage.alt =
        `CARD ${String(currentIndex + 1).padStart(2, "0")}`;

      cardFront.className = "card-face card-front";
      updateDeckPeeks();
    }'''

if old not in text:
    raise SystemExit("updateCard block not found")

p.write_text(text.replace(old, new, 1), encoding="utf-8")
