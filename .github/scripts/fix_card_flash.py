from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")

css_old = '''    .card {
      width: 100%;
      height: 100%;
      position: absolute;
      inset: 0;
      transform-style: preserve-3d;
      transition: transform .52s cubic-bezier(.2,.8,.2,1), opacity .32s ease;
      border-radius: 24px;
    }

    .card-face {'''

css_new = '''    .card {
      width: 100%;
      height: 100%;
      position: absolute;
      inset: 0;
      transform-style: preserve-3d;
      transition: transform .52s cubic-bezier(.2,.8,.2,1), opacity .32s ease;
      border-radius: 24px;
    }

    .card.instant-state {
      transition: none !important;
    }

    .card-face {'''

if css_old not in text:
    raise SystemExit("card CSS anchor not found")
text = text.replace(css_old, css_new, 1)

comment_old = '''    // 中央卡切換時仍會重新蓋回卡背；旁邊則記得曾經翻開過的卡。
    let isAnimating = false;
    const revealedCards = new Set();'''

comment_new = '''    // 本輪翻過的卡會維持揭露；重新整理頁面後 Set 會自然重置。
    let isAnimating = false;
    const revealedCards = new Set();'''

if comment_old not in text:
    raise SystemExit("reveal state comment not found")
text = text.replace(comment_old, comment_new, 1)

old = '''    function updateCard() {
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

new = '''    function updateCard() {
      const data = cards[currentIndex];
      const revealed = revealedCards.has(currentIndex);

      // 先瞬間回到卡背，再換圖片，避免未翻過的新卡閃出正面。
      // 若這張卡本輪已翻過，再於同一幀直接套回 flipped，不播放重複翻牌動畫。
      card.className = "card instant-state";
      if (data.rarity === "SR") {
        card.classList.add("sr");
      }

      backNumber.textContent = currentIndex + 1;

      cardImage.src = data.image;
      cardImage.alt =
        `CARD ${String(currentIndex + 1).padStart(2, "0")}`;

      cardFront.className = "card-face card-front";
      if (revealed) {
        card.classList.add("flipped");
      }

      updateDeckPeeks();

      // 強制套用這次的無動畫狀態，下一幀恢復正常翻牌動畫。
      void card.offsetWidth;
      requestAnimationFrame(() => {
        card.classList.remove("instant-state");
      });
    }'''

if old not in text:
    raise SystemExit("updateCard block not found")
text = text.replace(old, new, 1)

p.write_text(text, encoding="utf-8")
