from pathlib import Path

p = Path("index.html")
text = p.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str):
    global text
    if old not in text:
        raise SystemExit(f"{label} block not found")
    text = text.replace(old, new, 1)


replace_once(
'''      body.touch-mode .debug-toggle { display: none; }
      body.touch-mode #cameraDot { display: none; }
      body.touch-mode .control-chip.start-pose-chip { display: none; }''',
'''      body.touch-mode .debug-toggle { display: none; }''',
"mobile hidden controls"
)

replace_once(
'''    // 手機 / 平板以觸控為主；桌機維持相機手勢。
    const isTouchMode =
      window.matchMedia("(pointer: coarse) and (hover: none)").matches ||
      (window.innerWidth <= 860 && navigator.maxTouchPoints > 0);

    if (isTouchMode) {
      document.body.classList.add("touch-mode");
      cameraStatusBar.style.display = "none";
      startBtn.textContent = "開始抽卡";
      welcomeLead.textContent = "左右滑動切換卡片，點一下或往上滑即可翻開你的收藏照片。";
      welcomeGestures.innerHTML = `
        <span><i class="gesture-mark">←</i> 左滑 · 下一張</span>
        <span><i class="gesture-mark">○</i> 點一下 · 翻牌</span>
        <span><i class="gesture-mark">→</i> 右滑 · 上一張</span>
      `;
    }''',
'''    // 手機 / 平板保留觸控，同時也啟用前鏡頭手勢辨識。
    const isTouchMode =
      window.matchMedia("(pointer: coarse) and (hover: none)").matches ||
      (window.innerWidth <= 860 && navigator.maxTouchPoints > 0);

    if (isTouchMode) {
      document.body.classList.add("touch-mode");
      startBtn.textContent = "開始抽卡";
      welcomeLead.textContent = "可用前鏡頭手勢巡卡，也可以直接觸控操作；握拳啟動／停止巡卡，停住後上滑翻牌。";
      welcomeGestures.innerHTML = `
        <span><i class="gesture-mark">◫</i> 握拳 · 啟動 / 停止</span>
        <span><i class="gesture-mark">←</i> 手勢向左巡卡</span>
        <span><i class="gesture-mark">○</i> 觸控點一下翻牌</span>
        <span><i class="gesture-mark">→</i> 手勢向右巡卡</span>
      `;
    }''',
"touch mode intro"
)

replace_once(
'''    function scheduleAutoScrollStep() {
      if (isTouchMode || !gestureArmed || !autoScrollDirection || isAnimating) return;''',
'''    function scheduleAutoScrollStep() {
      if (!gestureArmed || !autoScrollDirection || isAnimating) return;''',
"schedule mobile auto scroll"
)

replace_once(
'''    function startAutoScroll(direction) {
      if (isTouchMode || !gestureArmed) return;''',
'''    function startAutoScroll(direction) {
      if (!gestureArmed) return;''',
"start mobile auto scroll"
)

old_start_game = '''    async function startGame() {
      startBtn.disabled = true;
      errorBox.style.display = "none";

      // 觸控裝置不要求相機權限，直接進入卡片畫面。
      if (isTouchMode) {
        welcomeScreen.classList.remove("active");
        gameScreen.classList.add("active");
        updateCard();
        cameraText.textContent = "觸控模式";
        gestureStatus.textContent = "左右滑動切換 · 點一下或上滑翻牌";
        controlRow.innerHTML = `
          <span class="control-chip"><b>←</b>左滑 · 下一張</span>
          <span class="control-chip"><b>○</b>點一下 · 翻牌</span>
          <span class="control-chip"><b>→</b>右滑 · 上一張</span>
        `;
        keyboardNote.style.display = "none";
        return;
      }

      startBtn.textContent = "準備中…";

      try {
        if (!handLandmarker) {
          await createHandLandmarker();
        }

        await startCamera();

        welcomeScreen.classList.remove("active");
        gameScreen.classList.add("active");

        updateCard();

        detectionStarted = true;
        requestAnimationFrame(detectLoop);
      } catch (error) {
        console.error(error);

        startBtn.disabled = false;
        startBtn.textContent = "重新嘗試";

        errorBox.style.display = "block";
        errorBox.innerHTML = `
          <strong>無法啟動鏡頭或手勢辨識。</strong><br>
          ${error.message}<br><br>
          請確認：<br>
          1. 已允許瀏覽器使用相機<br>
          2. 使用 localhost 或 HTTPS 開啟網站
        `;
      }
    }'''

new_start_game = '''    async function startGame() {
      startBtn.disabled = true;
      errorBox.style.display = "none";
      startBtn.textContent = "準備中…";

      try {
        if (!handLandmarker) {
          await createHandLandmarker();
        }

        await startCamera();

        welcomeScreen.classList.remove("active");
        gameScreen.classList.add("active");
        updateCard();

        detectionStarted = true;
        gestureToggle.textContent = "關閉";
        gestureToggle.classList.remove("off");

        if (isTouchMode) {
          keyboardNote.style.display = "none";
          gestureStatus.textContent = "請先握拳啟動手勢 · 也可直接觸控";
          controlRow.innerHTML = `
            <span class="control-chip start-pose-chip"><b>◫</b>握拳 · 啟動 / 停止</span>
            <span class="control-chip"><b>←</b>手勢巡卡</span>
            <span class="control-chip"><b>○</b>點一下翻牌</span>
            <span class="control-chip"><b>↔</b>觸控切換</span>
          `;
        }

        requestAnimationFrame(detectLoop);
      } catch (error) {
        console.error(error);

        // 手機 / 平板若無法使用相機，仍可直接進遊戲用觸控操作。
        if (isTouchMode) {
          welcomeScreen.classList.remove("active");
          gameScreen.classList.add("active");
          updateCard();

          cameraDot.classList.remove("on");
          cameraText.textContent = "觸控模式 · 手勢未啟用";
          gestureToggle.textContent = "開啟手勢";
          gestureToggle.classList.add("off");
          gestureToggle.disabled = false;
          gestureStatus.textContent = "可直接觸控操作 · 點「開啟手勢」可重試相機";
          keyboardNote.style.display = "none";
          controlRow.innerHTML = `
            <span class="control-chip"><b>←</b>左滑 · 下一張</span>
            <span class="control-chip"><b>○</b>點一下 · 翻牌</span>
            <span class="control-chip"><b>→</b>右滑 · 上一張</span>
          `;
          return;
        }

        startBtn.disabled = false;
        startBtn.textContent = "重新嘗試";

        errorBox.style.display = "block";
        errorBox.innerHTML = `
          <strong>無法啟動鏡頭或手勢辨識。</strong><br>
          ${error.message}<br><br>
          請確認：<br>
          1. 已允許瀏覽器使用相機<br>
          2. 使用 localhost 或 HTTPS 開啟網站
        `;
      }
    }'''
replace_once(old_start_game, new_start_game, "startGame")

replace_once(
'''    deckShell.addEventListener("touchstart", (event) => {
      if (!isTouchMode || event.touches.length !== 1) return;
      const touch = event.touches[0];''',
'''    deckShell.addEventListener("touchstart", (event) => {
      if (!isTouchMode || event.touches.length !== 1) return;

      // 觸控優先：若正在手勢巡卡，碰到螢幕就立刻停止巡卡。
      if (autoScrollDirection) {
        stopAutoScroll("觸控接管 · 巡卡已停止");
      }

      const touch = event.touches[0];''',
"touch takeover"
)

p.write_text(text, encoding="utf-8")
