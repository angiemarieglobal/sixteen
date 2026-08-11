# amg-lead-magnets

Lead magnets for Angie Marie Global. One repo, one folder per asset, source and built PDF
together so a magnet can be rebuilt from scratch two years from now without archaeology.

Landing pages are served from `docs/` by GitHub Pages.

---

## What is in here

| # | Asset | Keyword | Doorway | Status |
|---|-------|---------|---------|--------|
| 16 | Sixteen | `16` | Baseline | **BUILT** |
| — | What You Are Tolerating | tbc | Baseline | planned |
| — | The Anti-Escape Plan | `FREEDOM` | Baseline | planned |
| — | The Seven Day Baseline | `BASELINE` | Baseline | planned |
| — | The Gap Map | `SHIFT` | Shift | planned, September |
| — | The Permission Slips | `PERMISSION` | Permission | planned |
| — | The 4:30am Drive | tbc | Baseline | planned |
| — | The Leaked Moment Log | tbc | Baseline | planned |
| — | The Ceiling Test | `CAPACITY` | Capacity | planned, November |
| — | The Wheel | `ENCOMPASSED` | Encompassed | planned, October |

Full bank of 22 ideas, build order and strategy: see the project doc
`claude/amg-lead-magnet-bank-2026-07-28.md`.

**Every keyword must exist in the amg-ecosystem capture table before the asset goes live.**
A keyword recorded only in a repo is a keyword nobody else can find.

---

## Folder shape

```
amg-lead-magnets/
  README.md
  docs/                          <- GitHub Pages root
    sixteen/index.html           <- GENERATED. the opt-in page.
    sixteen/thank-you/index.html <- GENERATED. delivery, next step, two upsells.
    sixteen/scan/index.html      <- GENERATED. the live interactive scan.
    sixteen/AMG-Sixteen.pdf      <- COPIED. the guide, served from the repo.
    sixteen/*.jpg                <- image sources. inlined into the pages at build.
  lm-16-sixteen/
    build/content.py             <- every word of the PDF. the source of truth.
    build/build_sixteen.py       <- renders the PDF
    build/add_scan_script.py     <- attaches the interactive layer to the scan page
    build/funnel_content.py      <- every word and every URL on the three web pages
    build/build_funnel.py        <- renders the three web pages into docs/sixteen/
    build/prepare_assets.py      <- bakes the banner fade, writes cover and web hero
    build/build_tiles.py         <- renders the sixteen redacted grid tiles
    build/export_copy.py         <- regenerates the readable copy doc
    assets/                      <- source banner and the baked cover
    content/sixteen-copy.md      <- generated. do not hand edit.
    dist/AMG-Sixteen.pdf         <- the deliverable
    GHL-BUILD-SPEC.md            <- keyword, tags, workflow, the three emails
```

Copy lives in exactly one file per asset. The PDF and the readable copy doc both render
from it, so they cannot drift apart.

---

## Rebuild an asset

```bash
cd lm-16-sixteen/build
pip install reportlab pikepdf pillow
python3 prepare_assets.py ../assets/sixteen-banner-source.png
python3 build_sixteen.py     # -> ../dist/AMG-Sixteen.pdf, script attached
python3 export_copy.py       # -> ../content/sixteen-copy.md
python3 build_tiles.py       # -> ../../docs/tile-01..16.jpg  the redacted grid
python3 build_funnel.py      # -> ../../docs/  all three pages + the PDF
```

To change a word, edit `build/content.py` and run both. Never edit the PDF or the
generated markdown directly.

---

## THE ASSET LAW

Locked 27 July 2026 in amg-brand-boards, and it is not optional.

- **No gradients.** Any fade is baked into a raster before it reaches the document.
- **No transparency.** Every alpha value pre-mixed into a solid colour.
- **Plain DeviceRGB.** No soft masks, no transparency groups.

A CSS fade becomes a PDF shading with a transparency mask, and some viewers render that
mask as magenta. A magenta stripe already appeared once on a finished asset. It cost
nothing visually to draw solid fills instead, and the file then renders identically on
Mac, PC, a print RIP and inside GHL.

Verify any new build:

```bash
python3 - <<'EOF'
raw = open('dist/AMG-Sixteen.pdf','rb').read()
for t in [b'/SMask', b'/ShadingType', b'/Shading', b'/Transparency',
          b'/DeviceCMYK', b'/DeviceGray', b'/ca ']:
    assert raw.count(t) == 0, f"{t.decode().strip()} found. fix before shipping."
print("clean")
EOF
```

`/CA` is deliberately not on that list. Inside a form widget's `/MK` dictionary `/CA` is
the button caption, not the constant alpha, so a fillable page will always show sixteen of
them. Lowercase `/ca` is the non-stroking alpha and that one must stay at zero.

Cover images ship as JPEG rather than PNG. A DCTDecode RGB image cannot carry an alpha
channel at all, which makes the law structurally impossible to break, and it took this
file from 2.6MB to 340KB. `build/prepare_assets.py` bakes the fade into the pixels and
writes both the PDF cover and the web hero from one source banner.

---

## FONTS

The locked AMG type system is **Forum** (title) and **Montserrat** (subtitle uppercase
tracked, and body). Both are free on Google Fonts and GHL ready.

Landing pages load the real fonts from the Google Fonts CDN.

The PDF build environment cannot reach Google Fonts, so **Lora** and **Poppins** stand in,
matching the Recognise Loop Map build of 27 July 2026. The two Recognise assets therefore
match each other. To ship the real fonts, drop the TTFs into `build/fonts/` and flip one
flag:

```
build/fonts/Forum-Regular.ttf
build/fonts/Montserrat-Light.ttf
build/fonts/Montserrat-Regular.ttf
build/fonts/Montserrat-Medium.ttf
build/fonts/Montserrat-SemiBold.ttf

# then in build_sixteen.py
USE_REAL_FONTS = True
```

Rebuild and the whole document picks them up. Nothing else changes.

---

## DEPLOY

**One time.** Push the repo, then Settings, Pages, source `main` branch, folder `/docs`.

**Custom domain.** Point `angiemarieglobal.com/sixteen` at the Pages URL, or host the
page inside GHL and keep this repo as the source of record. Slug convention across the
site is no `the-` prefixes, and `sixteen` follows it exactly, in line with the AMG
one-word naming system.

**Every push.** Pages redeploys on its own. Hard refresh to clear the CDN.

```bash
git init
git add .
git commit -m "Sixteen: PDF, landing page, live scan, GHL spec"
git branch -M main
git remote add origin git@github.com:USERNAME/amg-lead-magnets.git
git push -u origin main
```

---

## VOICE AND ROUTING

Copy is written to **amg-voice-master**: no em dashes, no exclamation marks, no ellipses,
no emoji, AU/UK spelling, non-gendered throughout, never lead with the label.

Pattern content is written to **amg-high-performer-codes**: the moment enters, the name
arrives at the bottom of the page.

Architecture, pricing, dates and keywords come from **amg-ecosystem** and nowhere else.
No asset in this repo prints a price.

---

## INTERACTIVITY, AND HOW FAR IT REACHES

The scan page of the PDF is a real AcroForm. Sixteen checkboxes, three typeable lines, a
counter, and six cluster rows.

**Ticking and typing work in every reader.** Acrobat, Apple Preview, Chrome, Edge, Firefox,
iOS Files, most Android readers. That is plain form filling and it is universal.

**The automatic cluster highlighting is form JavaScript, and only Adobe Acrobat Reader runs
it.** Every other viewer shows the page, ticks the boxes, keeps the typing, and simply does
not light the clusters. Nothing breaks and nothing looks wrong. The reader counts for
themselves, which the page tells them to do.

That gap is why the scan also lives on the web at `docs/sixteen/scan/`, where the ticking,
the counter, the cluster states and the closing verdict all move in every browser on every
device. Page 19 of the PDF links straight to it. Treat the web scan as the primary
experience and the PDF form as the offline one.

---

## THE FUNNEL

Three pages, generated. **Do not hand edit the HTML in `docs/`.** Edit
`build/funnel_content.py` for words and URLs, or `build/build_funnel.py` for the design
system, then rerun `python3 build_funnel.py`. One shared stylesheet across all three pages,
so they cannot drift apart.

```
/sixteen/              opt-in
/sixteen/thank-you/    delivery, next step, two upsells
/sixteen/scan/         the live interactive scan
/sixteen/AMG-Sixteen.pdf
```

### The route

```
content, keyword 16
  -> DM with the link
  -> /sixteen                opt-in, email captured
  -> GHL form submit         tags applied, workflow fires
  -> /sixteen/thank-you/     download button, next steps, two upsells
  -> delivery email          the PDF, attached and linked
  -> /baseline-audit         from the PDF page 20 and the thank-you page
  -> /recognise              upsell, step one
  -> baseline membership     upsell, step two
```

GHL does exactly one job in this funnel: capture the lead and send the email. Every page is
static and served by GitHub Pages, so nothing can break mid-launch except the form.

### THE GHL EMBED

Live since 31 July 2026. The fallback form is gone.

```
form      LM 16 - Sixteen        id pbJlsgtoTV05wrLI67gj
embed     links.angiemarieglobal.com/widget/form/pbJlsgtoTV05wrLI67gj
resizer   links.angiemarieglobal.com/js/form_embed.js
```

**Three settings live inside GHL and nothing in this repo can change them.** If any one is
wrong the funnel breaks and editing HTML will not fix it.

1. Redirect on submit, to `https://angiemarieglobal.github.io/sixteen/thank-you/`
2. Tags on submit, `lm-sixteen,doorway-baseline`
3. Workflow `LM16 - Sixteen - Deliver`, sending the guide

### TWO RULES THAT COST AN AFTERNOON

**One. The form card carries no `.rv` reveal, and it never should.**

`.rv` starts an element at opacity 0 with a transform, which puts it on its own compositing
layer. A cross origin iframe inside that layer loads its document and then never paints. The
element measures correctly, reports opacity 1 and visibility visible, and shows a blank
rectangle. Anything that forces a re-composite makes it appear, which is why it looked
intermittent and impossible to pin down. The form is the conversion element. It arrives with
the page, not on a scroll cue.

**Two. Never set the iframe `src` from JavaScript.**

`form_embed.js` re-parents the iframe into `.ep-wrapper` inside `.ep-iFrameContainer`, and
re-parenting an iframe forces a reload. Setting `src` at runtime races that and the form
renders blank. The iframe ships with a plain `src` and no script touches it.

The cost of rule two is the automatic traffic-source stamping. `?src=` no longer reaches GHL
from this page. GHL's own embed script is documented to forward the parent page's query
string into the form, but that is unconfirmed here. **Confirm it on the first real
submission:** load the page as `?src=ig-reel`, submit, and check whether the source landed on
the contact. If it did not, add a hidden field in the GHL form and populate it there.

**Height.** `form_embed.js` measures the form and sets an inline height, 525px on this four
field form. That inline style beats the stylesheet, so `min-height` is only the placeholder
for the moment before it lands, and must stay just BELOW the reported height. Set it above and
it wins the cascade and leaves dead space under the button. That happened once at 560px.

**Styling.** The form is a cross origin iframe. Nothing on this page can reach inside it, so
field styling, button colour and the button label are all edited in GHL, not here. `.formcard`
is transparent with no padding so the GHL card carries the look on its own.

`C.FIELDS` in `funnel_content.py` is no longer rendered. It stays as the spec of what the GHL
form must ask for, in order: first name, surname, email, phone optional.

### The opt-in page, in order

1. **Hero.** The banner full bleed, wordmark standing alone, a FREE 20 PAGES badge, then the
   strap and **one** button. No second option, because a second option is a decision and a
   decision is friction.
2. **The problem**, in the avatar's own words.
3. **THE GATE.** Sixteen numbered tiles, redacted. No moment text and no names. The page
   proves the shape and the count, and nothing else. A capture page that hands over the
   substance has no reason to capture anything. Locked 31 July 2026.
4. **The loop**, as a six link chain with the last link inverted.
5. **See inside.** Four real pages of the PDF, fanned on a tilt.
6. **The counts.** 16, 6, 1.
7. **The scan**, sold rather than opened. The CTA goes to `#get`, not to `/scan/`.
8. **Capture**, on deep umber so the cream form is the brightest thing on screen.
9. **Who wrote this.**
10. **The two upsells.**

### Images are inlined

Every image is embedded as a base64 data URI, so each page is one self-contained file that
renders correctly wherever it is opened, not only when the sibling `.jpg` files happen to be
next to it. That was a real failure: a single HTML file sent for review had nothing to point
at and the hero looked missing.

The cost is page weight. The opt-in page is about 437KB, of which roughly 360KB is image
data that would have loaded anyway. If that ever matters more than the guarantee, switch
`data_uri()` in the builder to return the plain filename and the pages go back to external
images with no other change.

The `.jpg` files stay in `docs/sixteen/` regardless, because `og:image` needs a real URL for
link previews.

### Regenerate the page previews

Proof goes stale. Whenever `content.py` changes, the four preview shots are selling a
document that no longer exists.

```bash
cd lm-16-sixteen/dist
for pg in 1 2 19 20; do pdftoppm -jpeg -r 130 -f $pg -l $pg AMG-Sixteen.pdf pv; done
```

Resize each to 520px wide, save into `docs/` as
`preview-cover|howto|scan|close.jpg`, then rerun `build_funnel.py`.

Pages 1, 2, 19 and 20 are chosen on purpose. They prove the craft and reveal no moment and
no name. `preview-code.jpg` and `preview-escape.jpg` came from pages 3 and 14, showed a
named pattern, and were deleted from the repo on 31 July 2026. Do not bring them back.

### THE REDACTED TILES, AND WHY THE BLUR IS IN THE PIXELS

Each grid tile carries a JPEG of the real moment, typeset on brand oat, blurred by
`build_tiles.py` before the file is written. Rerun that script whenever `content.py` changes.

**Never do this with a CSS blur.** A CSS filter is a costume. One line removed in dev tools and
all sixteen moments are readable, which walks straight through the gate. A baked blur has no
sharp layer to recover: what ships is a JPEG of soft shapes. The tile tells the truth about
being real text and still gives nothing away.

Blur radius is 8.5 at 560px wide, tested. 5.5 was still readable. 10 washed out to a smudge and
stopped reading as words at all.

### THE GATE, and how far it reaches

The opt-in page shows sixteen redacted tiles and links to nothing but the form. The moments,
the names, the PDF and the live scan all sit on the far side of `/thank-you/`.

This is a friction gate, not a lock. Every page here is static, so a determined person can
type `/sixteen/scan/` into a browser and reach it. That is true of every static lead magnet
on the internet and it does not matter: the scan is a list of sixteen numbers and six cluster
names, and without the guide it says nothing. The value being protected is the words, and the
words only ever arrive by email.

If the scan ever needs a real lock, the move is a GHL-hosted page behind the workflow, not a
token in a static URL.

### URLs, confirmed

`BASELINE_URL` is `https://www.angiemarieglobal.com/baseline` and the page is live, confirmed
31 July 2026. `RECOGNISE_URL` is `https://www.angiemarieglobal.com/recognise`, also live. Both
upsell cards were written against those pages after reading them. **Read the destination page
before an upsell card ships.** That rule exists because a card once promised a monthly live
transmission that the sales page did not sell.

No page in this funnel prints a price. Recognise and the membership carry their own pricing
on their own pages, which also means these pages stay correct if pricing moves.

---

*Abundance is your baseline.*
