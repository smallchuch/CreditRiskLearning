# Notebook → HTML Slides with Quarto

## 1. Install Quarto (one-time)

Download the installer from https://quarto.org/docs/get-started/ and run it. Confirm it worked:

```
quarto --version
```

You'll also need Jupyter available in whatever Python environment your notebook uses (`pip install jupyter` if it's not already there — sounds like your existing venv already has it via VS Code's Jupyter extension).

## 2. The file: `home-credit-eda-slides.ipynb`

Open it like any normal notebook. It's built from three pieces:

**A raw cell at the top** — starts and ends with `---`. This is YAML front matter, Quarto's control panel for the whole deck: title, author, `format: revealjs` (tells it to build reveal.js slides instead of a report), theme, transitions, etc.

**Markdown cells with `##` headings** — every `##` starts a new slide. Text under a heading (before the next `##`) is that slide's body.

**Code cells with `#|` comments at the top** — these are "chunk options," Quarto's way of controlling how that specific cell renders:
- `#| echo: false` → run the code, hide it, show only the output (good for portfolio slides — nobody wants to read code mid-deck)
- `#| fig-cap: "..."` → caption under a plot

## 3. Render it

From a terminal, in the same folder as the notebook:

```
quarto render home-credit-eda-slides.ipynb --to revealjs
```

This produces `home-credit-eda-slides.html` — a single self-contained file (that's what `embed-resources: true` in the YAML does) you can double-click to open, email, or upload straight to a portfolio site / GitHub Pages.

## 4. Live preview while editing

```
quarto preview home-credit-eda-slides.ipynb
```

Opens a browser tab that auto-refreshes as you edit and save the notebook. This is the fastest feedback loop while you're building a deck.

## 5. Presenting

Once the HTML is open: arrow keys or space to advance, `f` for fullscreen, `s` for speaker notes view (add notes with a `::: {.notes}` block under any slide), `o` for slide overview grid.

## 6. What to change for your real project

- Swap the synthetic `df` in the "Simulating the Dataset" cell for your actual Home Credit dataframe
- Import `python_style_util.py` at the top and use its palette in the plots for visual consistency with your other notebooks
- Adjust `theme:` in the YAML — options include `simple`, `moon`, `night`, `dark`, `sky`, `beige`, etc. (swap the value and re-render to preview)

## Note on this session

My sandbox had a startup fault this session, so I wasn't able to install Quarto and test-render the deck end-to-end myself. The notebook structure (YAML front matter, heading-per-slide, `#|` chunk options) follows Quarto's documented spec exactly, so it should render cleanly — but do a `quarto render` as your first step to confirm before building further on top of it, and let me know if anything errors.
