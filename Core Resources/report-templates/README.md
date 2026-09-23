# Report Templates — Quarto reveal.js executive-summary decks

A reusable kit for clean, modern, on-brand slide reports, with **two brand
schemes you can switch between in one line**:

- **Personal** — jacaranda / gold / green. Distinctive, memorable — for your
  external-facing portfolio.
- **HomeStart** — the official HomeStart Finance blue/green brand guide — for
  internal presentations (e.g. an FP&A role-change pitch).

## Files

| File | What it is |
|---|---|
| `brand.scss` | **Layout + furniture, palette-agnostic.** All spacing, cover/closing, callouts, figure framing, the bar motif. Its colour tokens are `!default`, so a palette file overrides them. The defaults are the personal scheme, so `brand.scss` alone = personal. |
| `palette-homestart.scss` | **Only the HomeStart tokens.** Drop it ahead of `brand.scss` to reskin everything to HomeStart. (Add more `palette-*.scss` files for other brands the same way.) |
| `deck_utils.py` | Chart helpers + the matching chart palettes. `deck_style(theme=...)` recolours matplotlib and returns a palette (`PAL`). |
| `report_template.qmd` | The starter. Cover → hero → chart slide → text slide → closing. |

## Switch scheme — two lines in the `.qmd`

**Personal (external portfolio):**
```
theme: [default, brand.scss]
PAL = deck_style()
```
**HomeStart (internal presentation):**
```
theme: [default, palette-homestart.scss, brand.scss]
PAL = deck_style(theme="homestart")
```
That's the whole switch — the first line reskins the slides, the second reskins
the charts. Nothing else changes. (Both lines are flagged with `← swap …`
comments in `report_template.qmd`.)

## Make a new report

1. Copy `report_template.qmd` to your report's name; keep `brand.scss`,
   `palette-homestart.scss` and `deck_utils.py` beside it.
2. Pick the scheme (the two lines above).
3. Change `title` / `subtitle` / `footer`; edit the cover kicker + stat chips in
   the `<script>` at the bottom.
4. Write slides. Patterns:
   - New slide: `## Title {data-kick="Section · label"}`.
   - Key point: `::: {.takeaway} … :::`. Watch-out: `::: {.caveat} … :::`.
   - Answer-first hero: the `.hero` block. Full-bleed closing: `## {.closing}`.
   - Charts: `PAL.primary` / `PAL.secondary` for colours, `PAL.ramp` for graded
     bars, `add_baseline(axes, BASE)` for a reference line.
5. `quarto render your_report.qmd --to revealjs` → one self-contained `.html`.

## Adding another brand (or finishing the HomeStart one)

The HomeStart palette uses the official brand-guide hexes (HomeStart Blue
`#0093D6`, Space Blue `#002E6D`, Saphire `#0069A6`, Light Blue `#8CC6E7`, Light
Grey `#DAE0E9`, HomeStart Green `#80C7BC`, Corporate Tan/Salmon, Finance Grey,
Light Jade). The two green accent shades used for on-white text (`$gold-300/400`)
are darker tints of HomeStart Green, derived so accent text stays legible.

To add a new brand `X`:
1. Copy `palette-homestart.scss` to `palette-X.scss`, set the tokens to brand X.
2. Add an `"X": dict(...)` entry to `THEMES` in `deck_utils.py` (primary,
   primary_dk, primary_lt, secondary, tertiary, ramp) so charts match.
3. Use `theme: [default, palette-X.scss, brand.scss]` + `deck_style(theme="X")`.

**Fonts / logo:** set `$body-font` / `$head-font` / `$mono-font` at the top of
`brand.scss` (or per-palette). For a company logo, add an `<img>` in the cover
`<script>` — send me the asset and I'll position it.

## Requirements

Quarto, and a Python with pandas / numpy / matplotlib / seaborn / jupyter, plus
`python_style_util.py` and `deck_utils.py` importable (in this repo they're in
`Core Resources` and `Core Resources/Scripts`; the kit also bundles a copy of
`deck_utils.py`). Install the fonts (Inter, DM Sans, JetBrains Mono, or your
corporate typeface) before presenting so nothing falls back.
