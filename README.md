This is my blog.

It lives at [leotrs.com](http://www.leotrs.com).

If you want to clone and run it locally, you would want to do
`python3 -m http.server 8000` from the root directory and then just browse
`localhost:8000`.  But I have no idea why you would want to do that.
Seriously.

## Tattoos

The gallery at [/tattoos](https://leotrs.com/tattoos/) is generated. Each entry
animates from the source of the idea into the photo of the tattoo and back.

### Building it

```
uv run tools/build_tattoos.py tools/tattoos.yaml --out tattoos/ \
    --images-dir ~/tattoo-sources
```

Then commit whatever landed in `tattoos/` and push, the same as the CV PDFs.
There is no build step on Netlify; it serves the repo as it is.

That needs `ffmpeg` on PATH. The Python dependencies are pinned at the top of
the script, so `uv` fetches them and there is nothing to install or manage.

It re-encodes every entry every time, about five seconds each. `--only <slug>`
does one entry. Pointing the same command at `tools/demo/tattoos.yaml` renders
two placeholder entries somewhere scratch, which checks the script still works
without touching the real page.

### Where the photos live

The YAML lives in the repo at `tools/tattoos.yaml`, but the photos do not. This
repo is public on GitHub and the site is public on Netlify, so the originals sit
outside both, under `~/tattoo-sources/`. `--images-dir` is what points the
build at them; without it, paths in the YAML are read relative to the YAML
file itself.

Only the generated MP4, WebP and poster are committed. Nothing published is a
copy of an original file: every output is re-encoded from a pixel array, so EXIF
and GPS cannot survive into the site.

### The YAML

One mapping per tattoo. Order does not matter; the build lists them newest
first.

| field | required | notes |
|---|---|---|
| `slug` | yes | file names and the anchor id, so `/tattoos/#nazca-hummingbird` works |
| `title` | yes | short name |
| `source` | yes | image the idea came from, relative to `--images-dir` |
| `tattoo` | yes | photo of the tattoo, relative to `--images-dir` |
| `date` | yes | `YYYY-MM` or `YYYY` |
| `place` | yes | free text |
| `artist` | yes | free text |
| `artist_url` | no | makes the artist name a link |
| `notes` | no | one short paragraph under the card |
| `source_credit` | no | credit or licence for the source image, set small under the card |
| `align` | no | point pairs, see below |
| `transition` | no | `crossfade` (default) or `edges`, which passes through a line drawing |
| `hold`, `fade` | no | timing overrides in seconds, default 1.5 and 1.2 |

### Picking alignment points

Without `align`, both images are centre-cropped and the transition is a plain
crossfade between two differently framed pictures. With it, the source is warped
so the motif lands exactly where the tattoo is, and the motif then appears to
hold still while everything around it changes. This is the single thing that
makes the animation work, so it is worth the five minutes.

Open both images in any viewer that shows pixel coordinates, then pick the same
features in each, in the same order:

```yaml
align:
  source: [[500, 450], [387, 447], [740, 450], [920, 330]]
  tattoo: [[330, 520], [244, 549], [510, 454], [613, 315]]
```

Coordinates are pixels in the original files, not in the square output. Three
pairs give an affine warp, which handles scale, rotation and shear. Four or more
give a homography, which also handles perspective, and that is usually what you
want for a photograph taken at an angle. Pick points that are far apart and
unambiguous: the tips of a motif rather than the middle of a curve.

### Output

Per entry, into `tattoos/`:

- `<slug>.mp4`, 720x720, H.264, the format the page actually uses
- `<slug>.webp`, 480px animated, the fallback
- `<slug>-poster.jpg`, 480px, shown before the video loads and instead of it
  under `prefers-reduced-motion`
- `<slug>.gif` only with `--gif`. It is not used by the page: measured on the
  demo, the GIF is 2.8 MB at 360px against 245 kB for the MP4 at 720px.

All of it is committed. These are build outputs living in the repo, like
`leo_torres_engineer.pdf`.

The page itself is `tattoos/index.html`, built from the same template as the
rest of the site: `styles.css`, Manrope and JetBrains Mono, the dark mode
toggle, the nav and the footer.

### Linking it

The page is unlisted. `index.html` carries a commented-out nav link; uncomment
it to put Tattoos in the main navigation.
