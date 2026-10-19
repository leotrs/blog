#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "opencv-python-headless==4.10.0.84",
#     "numpy==1.26.4",
#     "pyyaml==6.0.2",
#     "pillow==10.4.0",
# ]
# ///
"""Build the /tattoos page: each entry animates from the source of the idea into
the tattoo, then back, and the cards are rendered into the site's own chrome.

    uv run tools/build_tattoos.py tools/tattoos.yaml --out tattoos/ \
        --images-dir ~/tattoo-sources

Run it, commit what lands in tattoos/, push. Netlify serves the repo as-is.

Entry fields in the YAML (a list, one mapping per tattoo):

    slug            required  file names and the anchor id
    title           required  short name
    source, tattoo  required  image paths, relative to the YAML file unless
                              --images-dir is given, in which case relative to that
    date            required  YYYY-MM or YYYY
    place, artist   required  free text
    artist_url      optional  makes the artist name a link
    notes           optional  one short paragraph under the card
    source_credit   optional  credit or licence line for the source image
    align           optional  >=3 point pairs warping the source onto the tattoo
                              frame (3 = affine, >=4 = homography)
    transition      optional  crossfade (default) | edges
    hold, fade      optional  timing overrides, in seconds

Nothing published is a copy of an original file: every output is re-encoded from
a pixel array, so EXIF and GPS cannot survive into the site.
"""
import argparse
import html
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np
import yaml
from PIL import Image

SIZE = 720
FPS = 24
POSTER_WIDTH = 480
WEBP_WIDTH = 480

REQUIRED = ("slug", "title", "source", "tattoo", "date", "place", "artist")


# --- image preparation ------------------------------------------------------

def load(path):
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise SystemExit(f"cannot read image: {path}")
    return img


def cover(img, size=SIZE):
    """Center-crop to square and resize. Returns the image and the affine used."""
    h, w = img.shape[:2]
    s = size / min(h, w)
    tx, ty = (size - w * s) / 2, (size - h * s) / 2
    M = np.array([[s, 0, tx], [0, s, ty]], dtype=np.float64)
    return cv2.warpAffine(img, M, (size, size), flags=cv2.INTER_AREA), M


def apply_affine(M, pts):
    pts = np.asarray(pts, dtype=np.float64)
    return pts @ M[:, :2].T + M[:, 2]


def prepare_pair(entry, src_path, tat_path):
    """Both images as SIZE x SIZE frames, the source warped onto the tattoo if
    the entry gives alignment points. That warp is what keeps the motif still
    while everything around it changes."""
    src, tat = load(src_path), load(tat_path)
    tat_sq, Mt = cover(tat)
    align = entry.get("align")
    if not align:
        src_sq, _ = cover(src)
        return src_sq, tat_sq

    ps = np.asarray(align["source"], dtype=np.float64)
    pt = apply_affine(Mt, align["tattoo"])
    if len(ps) >= 4:
        H, _ = cv2.findHomography(ps, pt, 0)
        warped = cv2.warpPerspective(src, H, (SIZE, SIZE), flags=cv2.INTER_AREA,
                                     borderMode=cv2.BORDER_REFLECT)
    else:
        A, _ = cv2.estimateAffine2D(ps, pt)
        warped = cv2.warpAffine(src, A, (SIZE, SIZE), flags=cv2.INTER_AREA,
                                borderMode=cv2.BORDER_REFLECT)
    return warped, tat_sq


def line_drawing(img):
    """Dark lines on light paper. Bridges photograph and ink."""
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    g = cv2.bilateralFilter(g, 9, 50, 50)
    e = cv2.Canny(g, 40, 120)
    e = cv2.dilate(e, np.ones((2, 2), np.uint8))
    paper = np.full_like(img, 236)
    paper[e > 0] = (30, 30, 30)
    return paper


def ease(t):
    return 0.5 - 0.5 * np.cos(np.pi * t)


def frames(a, b, hold, fade, transition):
    """Hold on the source, transition, linger on the tattoo, transition back."""
    nh, nf = int(hold * FPS), int(fade * FPS)
    a32, b32 = a.astype(np.float32), b.astype(np.float32)
    stops = [a32, line_drawing(a).astype(np.float32), b32] if transition == "edges" else [a32, b32]

    def blend_path(path):
        for x, y in zip(path, path[1:]):
            for i in range(nf):
                t = ease(i / nf)
                yield ((1 - t) * x + t * y).astype(np.uint8)
            for _ in (range(max(nh // 3, 1)) if y is not path[-1] else ()):
                yield y.astype(np.uint8)

    for _ in range(nh):
        yield a
    yield from blend_path(stops)
    for _ in range(nh * 2):
        yield b
    yield from blend_path(stops[::-1])


# --- encoding ---------------------------------------------------------------

def encode(entry, a, b, out, want_gif):
    slug = entry["slug"]
    hold = entry.get("hold", 1.5)
    fade = entry.get("fade", 1.2)
    transition = entry.get("transition", "crossfade")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        small = []
        for i, f in enumerate(frames(a, b, hold, fade, transition)):
            cv2.imwrite(str(td / f"{i:05d}.png"), f)
            rgb = cv2.cvtColor(cv2.resize(f, (WEBP_WIDTH, WEBP_WIDTH), interpolation=cv2.INTER_AREA),
                               cv2.COLOR_BGR2RGB)
            small.append(Image.fromarray(rgb))

        ff = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
              "-i", str(td / "%05d.png")]
        run(ff + ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26",
                  "-preset", "slow", "-movflags", "+faststart", "-an",
                  str(out / f"{slug}.mp4")])
        if want_gif:
            pal = ("fps=12,scale=360:-1:flags=lanczos,split[s0][s1];"
                   "[s0]palettegen=stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=4")
            run(ff + ["-filter_complex", pal, "-loop", "0", str(out / f"{slug}.gif")])

    # Pillow rather than ffmpeg, because a stock homebrew ffmpeg has no libwebp.
    small[0].save(out / f"{slug}.webp", save_all=True, append_images=small[1:],
                  duration=round(1000 / FPS), loop=0, quality=70, method=4)

    poster = cv2.resize(b, (POSTER_WIDTH, POSTER_WIDTH), interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(out / f"{slug}-poster.jpg"), poster, [cv2.IMWRITE_JPEG_QUALITY, 78])


def run(cmd):
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f"ffmpeg failed ({exc.returncode}): {' '.join(cmd[:8])} ...")


# --- the page ---------------------------------------------------------------

def esc(value):
    return html.escape(str(value))


def card(entry):
    rows = [f"<dt>When</dt><dd>{esc(entry['date'])}</dd>",
            f"<dt>Where</dt><dd>{esc(entry['place'])}</dd>"]
    artist = esc(entry["artist"])
    if entry.get("artist_url"):
        artist = f'<a href="{esc(entry["artist_url"])}" rel="noopener">{artist}</a>'
    rows.append(f"<dt>Artist</dt><dd>{artist}</dd>")

    slug, title = esc(entry["slug"]), esc(entry["title"])
    label = f"{title}: from its source to the tattoo"
    notes = f'\n        <p class="notes">{esc(entry["notes"])}</p>' if entry.get("notes") else ""
    credit = (f'\n        <p class="credit">{esc(entry["source_credit"])}</p>'
              if entry.get("source_credit") else "")

    # role="img" because the clip is a silent moving picture, not a film: it
    # carries no audio track, so the captions a <video> would otherwise be
    # expected to have would be empty.
    return f"""      <article class="tattoo-card" id="{slug}">
        <div class="frame">
          <video autoplay muted loop playsinline preload="metadata"
                 poster="{slug}-poster.jpg" role="img" aria-label="{label}">
            <source src="{slug}.mp4" type="video/mp4">
            <img src="{slug}.webp" alt="{label}">
          </video>
          <img class="poster" src="{slug}-poster.jpg" alt="{label}">
        </div>
        <h2>{title}</h2>
        <dl>{''.join(rows)}</dl>{notes}{credit}
      </article>"""


PAGE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tattoos - Leo Torres</title>
    <meta name="description" content="{description}">
    <meta property="og:title" content="Tattoos - Leo Torres">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{og_image}">
    <link rel="icon" type="image/svg+xml" href="../favicon-navy.svg">
    <link rel="icon" type="image/x-icon" href="../favicon.ico">
    <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
    <style>
      /* This page is not one of the three personas, so no accent is claimed and
         all three diamonds stay outlined. */
      .diamond-accent .diamond:nth-child(1) {{ border: 2px solid var(--plum); }}
      .diamond-accent .diamond:nth-child(2) {{ border: 2px solid var(--gold); }}
      .diamond-accent .diamond:nth-child(3) {{ border: 2px solid var(--verdigris); }}
      .section-divider {{ background-color: var(--navy); }}
      .nav-links a.active::after {{ background-color: var(--navy); }}

      /* The diamond tooltip is laid out even while hidden, which makes the page
         9px wider than the viewport on a phone. Keeping it out of layout until
         hover fixes that. The same two lines in styles.css would fix it for
         every other page on the site, which is why they are not there. */
      .diamond::after {{ display: none; }}
      .diamond:hover::after {{ display: block; }}

      .intro {{ font-size: 0.9rem; color: var(--dark-gray); max-width: 600px; margin-bottom: var(--space-lg); }}

      /* Inside the site's 800px column this lands on two cards per row and
         collapses to one well before phone width. */
      .tattoo-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: var(--space-lg) var(--space-md);
        margin-bottom: var(--space-xl);
      }}

      .tattoo-card {{ min-width: 0; }}
      .tattoo-card .frame {{
        position: relative;
        aspect-ratio: 1;
        border-radius: 4px;
        overflow: hidden;
        background-color: var(--light-bg);
      }}
      .tattoo-card video,
      .tattoo-card .poster {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
      .tattoo-card .poster {{ display: none; }}

      .tattoo-card h2 {{
        font-size: 1rem; font-weight: 600; color: var(--navy);
        margin-top: var(--space-sm); margin-bottom: 4px;
      }}
      .tattoo-card dl {{
        display: grid; grid-template-columns: max-content 1fr;
        gap: 2px var(--space-sm);
        font-size: 0.8rem; font-family: var(--font-mono);
      }}
      .tattoo-card dt {{ color: var(--medium-gray); }}
      .tattoo-card dd {{ color: var(--dark-gray); font-weight: 500; }}
      .tattoo-card dd a {{ color: var(--dark-gray); text-decoration: underline; text-underline-offset: 2px; }}
      .tattoo-card dd a:hover {{ color: var(--navy); }}
      .tattoo-card .notes {{ font-size: 0.85rem; color: var(--dark-gray); margin-top: var(--space-xs); }}
      .tattoo-card .credit {{ font-size: 0.7rem; color: var(--medium-gray); margin-top: 6px; }}

      a:focus-visible, button:focus-visible {{ outline: 2px solid var(--navy); outline-offset: 2px; }}

      /* Reduced motion: the poster stands in and nothing ever plays. */
      @media (prefers-reduced-motion: reduce) {{
        .tattoo-card video {{ display: none; }}
        .tattoo-card .poster {{ display: block; }}
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <header>
        <nav>
          <div class="nav-left">
            <div class="burger-menu" onclick="toggleBurgerMenu()" id="burger-menu">
              <div class="burger-line"></div>
              <div class="burger-line"></div>
              <div class="burger-line"></div>
            </div>
            <div class="page-title" id="page-title">Tattoos</div>
          </div>

          <div class="nav-links" id="nav-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/tattoos/" class="nav-link active">Tattoos</a>
          </div>

          <div style="display: flex; align-items: center; gap: var(--space-md);">
            <button class="theme-toggle" onclick="toggleTheme()" id="theme-toggle">
              <span class="theme-text">Dark</span>
            </button>
            <div class="diamond-accent">
              <div class="diamond" onclick="window.location.href='/scholar.html'" data-tooltip="Scholar"></div>
              <div class="diamond" onclick="window.location.href='/manager.html'" data-tooltip="Manager"></div>
              <div class="diamond" onclick="window.location.href='/engineer.html'" data-tooltip="Engineer"></div>
            </div>
          </div>
        </nav>
      </header>

      <main>
        <h1 class="section-title">Tattoos</h1>
        <div class="section-divider"></div>
        <p class="intro">{intro}</p>

        <div class="tattoo-grid">
{cards}
        </div>
      </main>

      <footer class="contact">
        <div class="contact-links">
          <a href="mailto:leo@leotrs.com">Email</a>
          <a href="https://github.com/leotrs">GitHub</a>
          <a href="https://www.linkedin.com/in/leo-torres-550ba068/">LinkedIn</a>
        </div>

        <div class="footer-diamonds">
          <div class="diamond"></div>
          <div class="diamond"></div>
          <div class="diamond"></div>
        </div>
      </footer>
    </div>

    <script>
      // Dark mode, same contract as the rest of the site.
      function toggleTheme() {{
        const html = document.documentElement;
        const text = document.getElementById('theme-toggle').querySelector('.theme-text');
        const newTheme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        text.textContent = newTheme === 'dark' ? 'Light' : 'Dark';
      }}

      function initTheme() {{
        const html = document.documentElement;
        const text = document.getElementById('theme-toggle').querySelector('.theme-text');
        const saved = localStorage.getItem('theme');
        const theme = saved || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        html.setAttribute('data-theme', theme);
        text.textContent = theme === 'dark' ? 'Light' : 'Dark';
      }}
      initTheme();

      function toggleBurgerMenu() {{
        document.getElementById('burger-menu').classList.toggle('active');
        document.getElementById('nav-links').classList.toggle('active');
      }}

      const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const clips = document.querySelectorAll('.tattoo-card video');
      if (reduced) {{
        clips.forEach(v => {{ v.removeAttribute('autoplay'); v.pause(); }});
      }} else {{
        // Only play what is on screen.
        const io = new IntersectionObserver(entries => entries.forEach(e => {{
          if (e.isIntersecting) e.target.play().catch(() => {{}});
          else e.target.pause();
        }}), {{ threshold: 0.25 }});
        clips.forEach(v => io.observe(v));
      }}
    </script>
  </body>
</html>
"""

INTRO = ("Each one started somewhere else: a photograph, a line on a plate, a textile. "
         "The animation runs from that source into the tattoo and back.")


def render_page(entries, out):
    og = f"{entries[0]['slug']}-poster.jpg" if entries else ""
    page = PAGE.format(
        description="Tattoos, each shown next to the image it came from.",
        og_image=esc(og),
        intro=esc(INTRO),
        cards="\n".join(card(e) for e in entries),
    )
    (out / "index.html").write_text(page)


# --- cli --------------------------------------------------------------------

def sort_key(entry):
    """Newest first. A year-only date sorts after the dated entries of that year."""
    date = str(entry["date"])
    return date if "-" in date else f"{date}-00"


def resolve(entry, key, cfg_dir, images_dir):
    base = images_dir if images_dir else cfg_dir
    path = base / entry[key]
    if not path.exists():
        raise SystemExit(f"{entry['slug']}: {key} image not found: {path}")
    return path


def main():
    ap = argparse.ArgumentParser(description="Build the tattoo gallery page.")
    ap.add_argument("config", help="path to tattoos.yaml")
    ap.add_argument("--out", default="tattoos", help="output directory (default: tattoos)")
    ap.add_argument("--images-dir", help="where the photos live, if not beside the YAML")
    ap.add_argument("--only", help="rebuild just this slug")
    ap.add_argument("--gif", action="store_true", help="also write a GIF (large; not used by the page)")
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is not on PATH. Install it (brew install ffmpeg) and try again.")

    cfg = Path(args.config)
    entries = yaml.safe_load(cfg.read_text()) or []
    images_dir = Path(args.images_dir).expanduser() if args.images_dir else None

    for entry in entries:
        missing = [f for f in REQUIRED if not entry.get(f)]
        if missing:
            raise SystemExit(f"{entry.get('slug', '<no slug>')}: missing {', '.join(missing)}")

    entries.sort(key=sort_key, reverse=True)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for entry in entries:
        slug = entry["slug"]
        if args.only and slug != args.only:
            continue
        src = resolve(entry, "source", cfg.parent, images_dir)
        tat = resolve(entry, "tattoo", cfg.parent, images_dir)
        a, b = prepare_pair(entry, src, tat)
        encode(entry, a, b, out, args.gif)
        print(f"built {slug}")

    render_page(entries, out)
    print(f"wrote {out / 'index.html'}")


if __name__ == "__main__":
    sys.exit(main())
