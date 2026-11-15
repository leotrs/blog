#!/usr/bin/env bash
# Builds leotrs.com/hop-run in this folder: compiles hop-run.mtp, copies the mathterpiece runtime
# next to it, and writes index.html, the page that holds the figure and its buttons.
#
#   ./build.sh
#
# levels.mtp is written by levels.py, which is run by hand when the levels change. The
# mathterpiece checkout is ~/aris/mathterpiece, or $MATHTERPIECE.
set -euo pipefail
cd "$(dirname "$0")"
mtp="${MATHTERPIECE:-$HOME/aris/mathterpiece}"

uv run --project "$mtp" mtp compile hop-run.mtp -o hop-run.mtpc
(cd "$mtp/web" && pnpm build >/dev/null)
cp "$mtp/web/dist/mathterpiece.js" mathterpiece.js

cat > index.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Hop run</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600&display=swap">
<script type="module" src="mathterpiece.js"></script>
<style>
  :root { color-scheme: light dark; --page: light-dark(#f6f1e7, #1d1b19); --ink: light-dark(#2b2a33, #ece6da);
    --chip: light-dark(#fffaf0, #2a2724); --edge: light-dark(#e3d9c6, #463f36);
    --accent: #f5862b; --on: light-dark(#fff1e4, #3a2a1c); --go: #2f9e44; --go-deep: #237a34; }
  html, body { margin: 0; height: 100%; background: var(--page); color: var(--ink); font-family: Fredoka, sans-serif;
    -webkit-user-select: none; user-select: none; -webkit-touch-callout: none; overflow: hidden; touch-action: manipulation; }
  main { height: 100dvh; display: flex; flex-direction: column; box-sizing: border-box; gap: 10px;
    padding: max(10px, env(safe-area-inset-top)) max(12px, env(safe-area-inset-right)) max(10px, env(safe-area-inset-bottom)) max(12px, env(safe-area-inset-left)); }
  .top { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
  .levels, .looks { display: flex; gap: 6px; }
  .stage { flex: 1; min-height: 0; position: relative; }
  .stage mtp-canvas { position: absolute; top: 0; left: 0; display: block; border-radius: 18px; overflow: hidden; }
  main mtp-readout[name="purse-count"] { font: 600 30px/1 Fredoka, sans-serif; display: inline-flex; align-items: center; gap: 8px; }
  main mtp-readout[name="purse-count"]::before { content: ""; width: 28px; height: 28px; border-radius: 50%;
    background: #ffd31b; box-shadow: inset 0 0 0 3px #e0a800; }

  /* The figure's buttons, large enough for a small finger, labelled in one word or a number.
     Under main, so these win over mathterpiece's own button styles, which come later. */
  main mtp-button button { font: 600 22px/1 Fredoka, sans-serif; color: var(--ink); background: var(--chip);
    border: 3px solid var(--edge); border-radius: 14px; min-width: 50px; height: 50px; padding: 0 12px; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center; gap: 8px; box-shadow: none; }
  main mtp-button button:hover { background: var(--chip); border-color: var(--edge); color: var(--ink); }
  main mtp-button button[aria-pressed="true"], main mtp-button button[aria-pressed="true"]:hover { border-color: var(--accent); background: var(--on); color: var(--ink); }
  main mtp-button button:disabled { opacity: .35; cursor: default; }
  /* The looks: a round swatch each, in the critter's colors, ringed when picked. */
  main .looks mtp-button button { width: 46px; min-width: 0; height: 46px; border-radius: 50%; padding: 0; border: 4px solid var(--page);
    box-shadow: 0 0 0 2px var(--edge); }
  main .looks mtp-button button[aria-pressed="true"] { box-shadow: 0 0 0 4px var(--ink); border-color: var(--page); }
  main mtp-button[name="look-0"] button, main mtp-button[name="look-0"] button:hover { background: #f5862b; }
  main mtp-button[name="look-1"] button, main mtp-button[name="look-1"] button:hover { background: #0e9ae9; }
  main mtp-button[name="look-2"] button, main mtp-button[name="look-2"] button:hover { background: #bb89f7; }
  main mtp-button[name="look-3"] button, main mtp-button[name="look-3"] button:hover { background: #f472b6; }
  main mtp-button[name="next"] button { background: var(--go); border-color: var(--go); color: #fff; box-shadow: 0 4px 0 var(--go-deep); }
  main .card mtp-button button { height: 76px; font-size: 30px; padding: 0 24px; }
  /* Tabler icons (MIT): player-play and rotate-clockwise. */
  main mtp-button[name="next"] button::before, main mtp-button[name="again"] button::before {
    content: ""; width: 30px; height: 30px; background: currentColor; -webkit-mask: var(--icon) center / contain no-repeat; mask: var(--icon) center / contain no-repeat; }
  main mtp-button[name="next"] { --icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='black'%3E%3Cpath d='M6 4v16a1 1 0 0 0 1.524 .852l13 -8a1 1 0 0 0 0 -1.704l-13 -8a1 1 0 0 0 -1.524 .852z'/%3E%3C/svg%3E"); }
  main mtp-button[name="again"] { --icon: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='black' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4.05 11a8 8 0 1 1 .5 4m-.5 5v-5h5'/%3E%3C/svg%3E"); }

  /* The celebration: shown while Next can be pressed, that is once the critter reaches the flag. */
  .cheer { position: fixed; inset: 0; display: none; place-items: center; background: color-mix(in srgb, var(--page) 40%, transparent); }
  .cheer:has(mtp-button[name="next"]:not([data-mtp-inactive])) { display: grid; }
  .card { background: var(--chip); border-radius: 28px; padding: 30px 40px; display: grid; gap: 16px; justify-items: center;
    box-shadow: 0 12px 40px rgba(0, 0, 0, .2); }
  .card .row { display: flex; gap: 12px; align-items: center; }
  main .card mtp-readout { font: 600 48px/1.1 Fredoka, sans-serif; }

  @media (max-width: 600px) {
    main mtp-button button { font-size: 16px; min-width: 34px; height: 38px; border-radius: 10px; padding: 0 4px; border-width: 2px; }
    main .looks mtp-button button { width: 34px; height: 34px; border-width: 3px; }
    .levels, .looks { gap: 4px; }
    main mtp-readout[name="purse-count"] { font-size: 22px; }
  }
</style>
</head>
<body>
<mtp-model id="m" src="hop-run.mtpc"></mtp-model>
<main>
  <div class="top">
    <div class="levels">
      <mtp-button model="m" name="level-0"></mtp-button><mtp-button model="m" name="level-1"></mtp-button>
      <mtp-button model="m" name="level-2"></mtp-button><mtp-button model="m" name="level-3"></mtp-button>
      <mtp-button model="m" name="level-4"></mtp-button><mtp-button model="m" name="level-5"></mtp-button>
    </div>
    <mtp-readout model="m" name="purse-count"></mtp-readout>
    <div class="looks">
      <mtp-button model="m" name="look-0"></mtp-button><mtp-button model="m" name="look-1"></mtp-button>
      <mtp-button model="m" name="look-2"></mtp-button><mtp-button model="m" name="look-3"></mtp-button>
    </div>
  </div>
  <div class="stage"><mtp-canvas model="m" name="view"></mtp-canvas></div>
  <div class="cheer"><div class="card"><mtp-readout model="m" name="cheer"></mtp-readout><mtp-readout model="m" name="purse-count"></mtp-readout>
    <div class="row"><mtp-button model="m" name="again"></mtp-button><mtp-button model="m" name="next"></mtp-button></div></div></div>
</main>
<script>
  // The figure fills the room it has, keeping its shape.
  const stage = document.querySelector(".stage");
  const canvas = stage.querySelector("mtp-canvas");
  const fit = () => {
    const box = canvas.querySelector("svg")?.viewBox?.baseVal;
    if (!box || !box.width) return;
    const ratio = box.height / box.width;
    const W = stage.clientWidth, H = stage.clientHeight;
    const w = Math.min(W, H / ratio);
    canvas.style.width = `${w}px`;
    canvas.style.transform = `translate(${(W - w) / 2}px, ${(H - w * ratio) / 2}px)`;
  };
  new ResizeObserver(fit).observe(stage);
  new MutationObserver(fit).observe(canvas, { childList: true, subtree: true, attributes: true, attributeFilter: ["viewBox"] });
</script>
</body>
</html>
HTML
echo "built $(pwd)"
