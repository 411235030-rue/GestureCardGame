from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str):
    global text
    if old not in text:
        raise SystemExit(f"{label} block not found")
    text = text.replace(old, new, 1)


replace_once(
'''    // 本輪翻過的卡會維持揭露；重新整理頁面後 Set 會自然重置。
    let isAnimating = false;
    const revealedCards = new Set();''',
'''    // 本輪翻過的卡會維持揭露；重新整理頁面後 Set 會自然重置。
    let isAnimating = false;
    const revealedCards = new Set();

    // 桌機手勢巡卡：左右滑一次後持續移動，握拳才停止。
    let autoScrollDirection = null; // "next" | "previous" | null
    let autoScrollTimer = null;
    const AUTO_SCROLL_INTERVAL_MS = 600;
    const CAROUSEL_ANIMATION_MS = 380;
    const AUTO_SCROLL_GAP_MS = Math.max(0, AUTO_SCROLL_INTERVAL_MS - CAROUSEL_ANIMATION_MS);''',
"auto scroll state"
)

replace_once(
'''    function finishCarouselMove(delta) {
      setTimeout(() => {
        currentIndex += delta;
        deckShell.classList.add("snap-reset");
        updateCard();
        deckShell.classList.remove("carousel-next", "carousel-prev");
        void deckShell.offsetWidth;

        requestAnimationFrame(() => {
          deckShell.classList.remove("snap-reset");
          isAnimating = false;
        });
      }, 380);
    }

    function nextCard() {
      if (isAnimating) return;

      if (currentIndex >= cards.length - 1) {
        gestureStatus.textContent = "已經是最後一張";
        return;
      }

      isAnimating = true;
      gestureStatus.textContent = "← 下一張";
      deckShell.classList.add("carousel-next");
      finishCarouselMove(1);
    }

    function previousCard() {
      if (isAnimating) return;

      if (currentIndex <= 0) {
        gestureStatus.textContent = "已經是第一張";
        return;
      }

      isAnimating = true;
      gestureStatus.textContent = "→ 上一張";
      deckShell.classList.add("carousel-prev");
      finishCarouselMove(-1);
    }''',
'''    function clearAutoScrollTimer() {
      if (autoScrollTimer) {
        clearTimeout(autoScrollTimer);
        autoScrollTimer = null;
      }
    }

    function stopAutoScroll(message = "巡卡已停止 · 可上滑翻牌") {
      autoScrollDirection = null;
      clearAutoScrollTimer();
      gestureStatus.textContent = message;
    }

    function scheduleAutoScrollStep() {
      if (isTouchMode || !gestureArmed || !autoScrollDirection || isAnimating) return;

      clearAutoScrollTimer();
      autoScrollTimer = setTimeout(() => {
        autoScrollTimer = null;

        if (autoScrollDirection === "next") {
          nextCard();
        } else if (autoScrollDirection === "previous") {
          previousCard();
        }
      }, AUTO_SCROLL_GAP_MS);
    }

    function startAutoScroll(direction) {
      if (isTouchMode || !gestureArmed) return;
      if (direction !== "next" && direction !== "previous") return;

      autoScrollDirection = direction;
      clearAutoScrollTimer();

      gestureStatus.textContent = direction === "next"
        ? "← 向左巡卡中 · 握拳停止"
        : "→ 向右巡卡中 · 握拳停止";

      if (!isAnimating) {
        if (direction === "next") {
          nextCard();
        } else {
          previousCard();
        }
      }
    }

    function finishCarouselMove(delta) {
      setTimeout(() => {
        currentIndex += delta;
        deckShell.classList.add("snap-reset");
        updateCard();
        deckShell.classList.remove("carousel-next", "carousel-prev");
        void deckShell.offsetWidth;

        requestAnimationFrame(() => {
          deckShell.classList.remove("snap-reset");
          isAnimating = false;

          // 巡卡狀態仍在時，補足到約 600ms / 張後自動走下一張。
          if (autoScrollDirection) {
            scheduleAutoScrollStep();
          }
        });
      }, CAROUSEL_ANIMATION_MS);
    }

    function nextCard() {
      if (isAnimating) return;

      if (currentIndex >= cards.length - 1) {
        if (autoScrollDirection) {
          stopAutoScroll("已到最後一張 · 巡卡停止");
        } else {
          gestureStatus.textContent = "已經是最後一張";
        }
        return;
      }

      isAnimating = true;
      gestureStatus.textContent = autoScrollDirection === "next"
        ? "← 向左巡卡中 · 握拳停止"
        : "← 下一張";
      deckShell.classList.add("carousel-next");
      finishCarouselMove(1);
    }

    function previousCard() {
      if (isAnimating) return;

      if (currentIndex <= 0) {
        if (autoScrollDirection) {
          stopAutoScroll("已到第一張 · 巡卡停止");
        } else {
          gestureStatus.textContent = "已經是第一張";
        }
        return;
      }

      isAnimating = true;
      gestureStatus.textContent = autoScrollDirection === "previous"
        ? "→ 向右巡卡中 · 握拳停止"
        : "→ 上一張";
      deckShell.classList.add("carousel-prev");
      finishCarouselMove(-1);
    }''',
"carousel functions"
)

replace_once(
'''      gestureArmed = false;
      gestureStart = null;
      lastPosition = null;
      startPoseSince = 0;''',
'''      stopAutoScroll();
      gestureArmed = false;
      gestureStart = null;
      lastPosition = null;
      startPoseSince = 0;''',
"stop recognition reset"
)

old_handle_start = '''    function handleStartPose(landmarks, position, now) {
      const pose = isStartPose(landmarks);

      if (pose) {
        startPosePoint = { x: position.x, y: position.y };

        if (!startPoseSince) {
          startPoseSince = now;
          startPoseConfirmed = false;
        }

        const held = now - startPoseSince;
        const progress = Math.min(100, Math.round(held / START_POSE_HOLD_MS * 100));

        if (held >= START_POSE_HOLD_MS) {
          startPoseConfirmed = true;
          gestureArmed = false;
          gestureStart = null;
          lastPosition = null;
          gestureStatus.textContent = "握拳辨識成功 ✓";
          setDebug([
            "Hand: YES",
            "Pose: FIST ✓",
            `x: ${position.x.toFixed(3)}  y: ${position.y.toFixed(3)}`,
            "Result: 握拳成功，放開後進入操作模式"
          ], now, true);
        } else {
          gestureStatus.textContent = `設定起點 ${progress}%`;
          setDebug([
            "Hand: YES",
            "Pose: FIST",
            `Hold: ${progress}%`,
            "Result: 維持握拳以啟動操作模式"
          ], now);
        }

        // 維持起點手勢期間完全不判斷滑動
        return true;
      }

      // 剛從起點手勢放開：以最後的起點手勢位置作為新的移動起點
      if (startPoseSince) {
        if (startPoseConfirmed && startPosePoint) {
          gestureStart = {
            x: startPosePoint.x,
            y: startPosePoint.y,
            time: now
          };
          lastPosition = { ...startPosePoint };
          gestureArmed = true;
          gestureStatus.textContent = "操作模式已啟用 ✓";
          setDebug([
            "Hand: YES",
            "Pose: RELEASED",
            `Start x: ${startPosePoint.x.toFixed(3)}  y: ${startPosePoint.y.toFixed(3)}`,
            "Result: 操作模式已啟用"
          ], now, true);
        }

        startPoseSince = 0;
        startPoseConfirmed = false;
        startPosePoint = null;
      }

      return false;
    }'''

new_handle_start = '''    function handleStartPose(landmarks, position, now) {
      const pose = isStartPose(landmarks);

      if (pose) {
        startPosePoint = { x: position.x, y: position.y };

        if (!startPoseSince) {
          startPoseSince = now;
          startPoseConfirmed = false;
        }

        const held = now - startPoseSince;
        const progress = Math.min(100, Math.round(held / START_POSE_HOLD_MS * 100));

        if (held >= START_POSE_HOLD_MS) {
          // 一次握拳只觸發一次：第一次用來啟動，巡卡中則用來停止。
          if (!startPoseConfirmed) {
            startPoseConfirmed = true;
            gestureStart = null;
            lastPosition = null;

            if (autoScrollDirection) {
              stopAutoScroll("握拳停止巡卡 ✓");
              gestureArmed = true;
              setDebug([
                "Hand: YES",
                "Pose: FIST ✓",
                `x: ${position.x.toFixed(3)}  y: ${position.y.toFixed(3)}`,
                "Result: 巡卡停止，等待目前卡片對齊"
              ], now, true);
            } else if (!gestureArmed) {
              gestureStatus.textContent = "握拳辨識成功 ✓";
              setDebug([
                "Hand: YES",
                "Pose: FIST ✓",
                `x: ${position.x.toFixed(3)}  y: ${position.y.toFixed(3)}`,
                "Result: 握拳成功，放開後進入操作模式"
              ], now, true);
            } else {
              gestureStatus.textContent = "握拳辨識成功 ✓";
              setDebug([
                "Hand: YES",
                "Pose: FIST ✓",
                `x: ${position.x.toFixed(3)}  y: ${position.y.toFixed(3)}`,
                "Result: 重新設定操作起點"
              ], now, true);
            }
          }
        } else {
          gestureStatus.textContent = autoScrollDirection
            ? `握拳停止 ${progress}%`
            : `設定起點 ${progress}%`;
          setDebug([
            "Hand: YES",
            "Pose: FIST",
            `Hold: ${progress}%`,
            autoScrollDirection
              ? "Result: 維持握拳以停止巡卡"
              : "Result: 維持握拳以啟動操作模式"
          ], now);
        }

        // 維持握拳期間完全不判斷滑動。
        return true;
      }

      // 放開握拳後，以最後的握拳位置作為新起點；操作模式維持啟用。
      if (startPoseSince) {
        if (startPoseConfirmed && startPosePoint) {
          gestureStart = {
            x: startPosePoint.x,
            y: startPosePoint.y,
            time: now
          };
          lastPosition = { ...startPosePoint };
          gestureArmed = true;
          lastGestureAt = 0;
          gestureStatus.textContent = "操作模式已啟用 ✓";
          setDebug([
            "Hand: YES",
            "Pose: RELEASED",
            `Start x: ${startPosePoint.x.toFixed(3)}  y: ${startPosePoint.y.toFixed(3)}`,
            "Result: 可左右滑開始巡卡；停住後可上滑翻牌"
          ], now, true);
        }

        startPoseSince = 0;
        startPoseConfirmed = false;
        startPosePoint = null;
      }

      return false;
    }'''
replace_once(old_handle_start, new_handle_start, "handleStartPose")

replace_once(
'''      // 一次手勢完成後短暫冷卻，避免同一個揮動重複觸發
      if (now - lastGestureAt < GESTURE_COOLDOWN_MS) {''',
'''      // 巡卡中只接受握拳停止；左右與上滑都先忽略。
      // handleStartPose 會在本函式之前執行，所以握拳仍能立即生效。
      if (autoScrollDirection) {
        gestureStart = null;
        lastPosition = null;
        gestureStatus.textContent = autoScrollDirection === "next"
          ? "← 向左巡卡中 · 握拳停止"
          : "→ 向右巡卡中 · 握拳停止";
        setDebug([
          "Hand: YES",
          `x: ${position.x.toFixed(3)}  y: ${position.y.toFixed(3)}`,
          "Result: AUTO SCROLL · 握拳停止"
        ], now);
        return;
      }

      // 一次手勢完成後短暫冷卻，避免同一個揮動重複觸發
      if (now - lastGestureAt < GESTURE_COOLDOWN_MS) {''',
"auto scroll movement guard"
)

replace_once(
'''      if (gesture === "LEFT") nextCard();
      if (gesture === "RIGHT") previousCard();
      if (gesture === "UP") flipCard();''',
'''      if (gesture === "LEFT") startAutoScroll("next");
      if (gesture === "RIGHT") startAutoScroll("previous");
      if (gesture === "UP") flipCard();''',
"gesture actions"
)

replace_once(
'''          if (!waitingForRight && now - lastHandSeenAt > HAND_LOST_RESET_MS) {
            gestureArmed = false;''',
'''          if (!waitingForRight && now - lastHandSeenAt > HAND_LOST_RESET_MS) {
            if (autoScrollDirection) {
              stopAutoScroll("手離開鏡頭 · 巡卡已停止");
            }
            gestureArmed = false;''',
"hand lost stop"
)

replace_once(
'''        <p class="lead">先握拳設定操作模式，之後可連續左右滑動切換卡片，再往上滑翻牌。</p>''',
'''        <p class="lead">先握拳啟動操作模式，左右滑開始連續巡卡，握拳停住後再往上滑翻牌。</p>''',
"welcome lead"
)

replace_once(
'''          <span><i class="gesture-mark">◫</i> 握拳設定起點</span>
          <span><i class="gesture-mark">←</i> 下一張</span>
          <span><i class="gesture-mark">↑</i> 翻牌</span>
          <span><i class="gesture-mark">→</i> 上一張</span>''',
'''          <span><i class="gesture-mark">◫</i> 握拳 · 啟動 / 停止</span>
          <span><i class="gesture-mark">←</i> 向左巡卡</span>
          <span><i class="gesture-mark">↑</i> 停住後翻牌</span>
          <span><i class="gesture-mark">→</i> 向右巡卡</span>''',
"welcome gestures"
)

replace_once(
'''        <span class="control-chip start-pose-chip"><b>◫</b>握拳 · 設定起點</span>
        <span class="control-chip"><b>←</b>下一張</span>
        <span class="control-chip"><b>↑</b>翻牌</span>
        <span class="control-chip"><b>→</b>上一張</span>''',
'''        <span class="control-chip start-pose-chip"><b>◫</b>握拳 · 啟動 / 停止</span>
        <span class="control-chip"><b>←</b>向左巡卡</span>
        <span class="control-chip"><b>↑</b>停住後翻牌</span>
        <span class="control-chip"><b>→</b>向右巡卡</span>''',
"desktop control chips"
)

p.write_text(text, encoding="utf-8")
