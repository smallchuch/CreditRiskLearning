# ══════════════════════════════════════════════════════════════════════════════
# credit_utils.py
# Brand design system — colours, fonts, chart utilities
# Credit Risk ML Portfolio
# ══════════════════════════════════════════════════════════════════════════════
#
# USAGE — add this to the top of every notebook:
#
#   from credit_utils import palette, fonts, p, set_style
#   set_style()
#
# To preview your full design system:
#   show_palette()
#   show_fonts()
#   show_style_guide()   # everything together
#
# To swap a font: change the string in the fonts dict below.
# To swap a colour: change the hex in the palette dict below.
# All notebooks pick up changes automatically on next import.
#
# ══════════════════════════════════════════════════════════════════════════════

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import numpy as np


# ── FONT REGISTRATION ─────────────────────────────────────────────────────────
# Rebuild font cache to ensure installed fonts are detected
# Only needs to run once per environment — comment out after first run
# fm._load_fontmanager(try_read_cache=False)


# ── FONTS ─────────────────────────────────────────────────────────────────────
# To swap a font: change the string value. Must be installed on your system.
# Fallbacks listed in order — matplotlib uses first available.

fonts = {

    # ── Heading font — large titles, chart titles, section headers
    # Inter: geometric, modern, used by Figma/Linear/Vercel — reads as premium
    'heading':      'Inter',
    'heading_fallback': ['DM Sans', 'Arial'],

    # ── Body font — axis labels, legends, annotations, subtitles
    # DM Sans: warmer than Inter, pairs perfectly, excellent at small sizes
    'body':         'DM Sans',
    'body_fallback': ['Inter', 'Arial'],

    # ── Mono font — numbers in tables, code blocks, data callouts
    # JetBrains Mono: tabular numbers align perfectly in columns
    'mono':         'JetBrains Mono',
    'mono_fallback': ['Courier New'],
}


# ── FONT SIZES ────────────────────────────────────────────────────────────────
# Consistent type scale — reference these rather than hardcoding sizes

sizes = {
    'display':    20,   # chart supertitles, hero numbers
    'title':      15,   # chart titles (axes.title)
    'subtitle':   12,   # chart subtitles, section labels
    'body':       10,   # axis labels, legend text
    'small':       9,   # tick labels, secondary annotations
    'tiny':        8,   # watermarks, footnotes, dense tables
    'mono':        9,   # numbers, code, data callouts
}


# ── PALETTE ───────────────────────────────────────────────────────────────────
# To swap a colour: change the hex string.
# Brand/neutral hues use a compact 100-500 scale — 300 = the named base colour,
# 100/200 = lighter tints, 400/500 = darker shades.
# Risk-semantic hues (red/green/yellow) keep the fuller 100-900 scale so
# heatmaps and gradients still have enough steps to work with.

palette = {

    # ── OFF WHITE — Background / Neutral Light ─────────────────────────────
    # Use for: page backgrounds, cards/surfaces, subtle fills
    'off_white': {
        100: '#FDFCFB',   # near-white tint — cards, surfaces, text on dark
        200: '#FAF9F5',   # subtle tint — table stripes, input fills
        300: '#F7F5F0',   # BASE — page background
        400: '#B9B8B4',   # medium — muted secondary text, placeholders
        500: '#7C7B78',   # dark — use sparingly, low-emphasis mid-tone
    },

    # ── OLIVE — Brand Tertiary ──────────────────────────────────────────────
    # Use for: third data series, callout boxes, highlights, annotations
    'olive': {
        100: '#D1D5CA',   # barely-there — background tints
        200: '#9CA38D',   # light — soft fills
        300: '#67724F',   # BASE — tertiary bars/lines, callouts
        400: '#4D563B',   # dark — stronger callouts, borders
        500: '#343928',   # darkest — high contrast, use sparingly
    },

    # ── JACARANDA — Brand Primary ───────────────────────────────────────────
    # Use for: main chart bars/lines, primary headers, key callouts
    'jacaranda': {
        100: '#D7CEE2',   # barely-there tint — panel backgrounds, table fills
        200: '#A995C0',   # light — secondary bars, light chart elements
        300: '#7A5C9E',   # BASE — primary bars, main data series, headings
        400: '#5C4577',   # dark — emphasis, hover/link states
        500: '#3D2E4F',   # darkest — pressed/active states, use sparingly
    },

    # ── GOLD — Brand Secondary ──────────────────────────────────────────────
    # Use for: secondary data series, accent lines, highlights alongside jacaranda
    'gold': {
        100: '#EFE1C5',   # barely-there — background washes
        200: '#DBBE80',   # light — subtle highlights
        300: '#C89B3C',   # BASE — secondary bars/lines, accent elements
        400: '#96742D',   # dark — stronger accent, borders
        500: '#644E1E',   # darkest — high contrast use, use sparingly
    },

    # ── CHARCOAL — Neutral / Secondary Information ──────────────────────────
    # Use for: axes, gridlines, secondary labels, benchmarks, body text
    'charcoal': {
        100: '#C1C1C1',   # light — dividers, table borders, gridlines
        200: '#787878',   # medium — secondary axis ticks, mid-tone labels
        300: '#2F2F2F',   # BASE — body text, axis labels, headings
        400: '#232323',   # dark — primary body text, titles
        500: '#181818',   # near-black — maximum contrast text
    },

    # ── RED — Danger / Default / High Risk / Reject ────────────────────────
    # Use for: default flag, high PD, rejected applications, losses
    'red': {
        100: '#FCEBEA',   # barely-there — row highlights for flagged records
        200: '#F8CDCC',   # light — background fills for risk alerts
        300: '#F3A5A4',   # soft — light risk indicators
        400: '#EC7471',   # medium — supporting risk elements
        500: '#E53935',   # BASE — default bars, high risk labels, loss figures
        600: '#B92F2C',   # dark — strong risk emphasis
        700: '#8D2623',   # darker — text on light red backgrounds
        800: '#611C1B',   # very dark — high contrast risk text
        900: '#351312',   # deepest — use sparingly
    },

    # ── GREEN — Safe / Approve / No Default / Low Risk ─────────────────────
    # Use for: no default, low PD, approved applications, performing loans
    'green': {
        100: '#F4F9F0',   # barely-there — row highlights for clean records
        200: '#E3F0DA',   # light — background fills for safe indicators
        300: '#CDE4BC',   # soft — light safe indicators
        400: '#B2D598',   # medium — supporting safe elements
        500: '#91C46C',   # BASE — no-default bars, low risk labels
        600: '#769E58',   # dark — strong safe emphasis
        700: '#5B7944',   # darker — text on light green backgrounds
        800: '#405431',   # very dark — high contrast safe text
        900: '#252F1D',   # deepest — use sparingly
    },

    # ── YELLOW — Watch / Medium Risk / Caution ────────────────────────────
    # Use for: medium PD, watch list loans, borderline decisions
    'yellow': {
        100: '#FFFAED',   # barely-there — subtle caution backgrounds
        200: '#FFF4D2',   # light — soft caution fills
        300: '#FFEBAF',   # soft — light caution indicators
        400: '#FFE083',   # medium — supporting caution elements
        500: '#FFD34E',   # BASE — watch bars, medium risk labels
        600: '#CEAA40',   # dark — more readable than 500 on white backgrounds
        700: '#9D8232',   # darker — text on light yellow backgrounds
        800: '#6C5A25',   # very dark — high contrast caution text
        900: '#3B3217',   # deepest — use sparingly
    },

# ── SEMANTIC — DATA VISUALISATION ─────────────────────────────────────
    # For chart elements — bars, lines, risk indicators
    'default_colour':       '#E53935',   # red 500       — default / loss
    'safe_colour':          '#91C46C',   # green 500     — performing / approve
    'watch_colour':         '#FFD34E',   # yellow 500    — watch / caution
    'chart_primary':        '#7A5C9E',   # jacaranda 300 — main data series
    'chart_secondary':      '#C89B3C',   # gold 300      — secondary series
    'chart_tertiary':       '#67724F',   # olive 300     — third series
    'chart_fourth':         '#A995C0',   # jacaranda 200 — fourth series

    # ── SEMANTIC — TYPOGRAPHY ──────────────────────────────────────────────
    # For text elements across dashboards and reports
    'text_primary':         '#2F2F2F',   # charcoal 300  — headlines, body text
    'text_secondary':       '#787878',   # charcoal 200  — subheadings, labels
    'text_tertiary':        '#7C7B78',   # off-white 500 — hints, placeholders
    'text_disabled':        '#B9B8B4',   # off-white 400 — disabled state text
    'text_inverse':         '#FDFCFB',   # off-white 100 — text on dark backgrounds
    'text_on_primary':      '#FDFCFB',   # off-white 100 — text on jacaranda backgrounds
    'text_on_danger':       '#FDFCFB',   # off-white 100 — text on red backgrounds
    'text_link':            '#5C4577',   # jacaranda 400 — hyperlinks, clickable

    # ── SEMANTIC — BACKGROUNDS ─────────────────────────────────────────────
    # For surfaces, panels, cards, page backgrounds
    'bg_page':              '#F7F5F0',   # off-white 300 — outermost page background
    'bg_surface':           '#FDFCFB',   # off-white 100 — cards, panels, modals
    'bg_subtle':            '#FAF9F5',   # off-white 200 — table stripes, input fills
    'bg_primary':           '#7A5C9E',   # jacaranda 300 — primary buttons, headers
    'bg_primary_hover':     '#5C4577',   # jacaranda 400 — primary button hover
    'bg_primary_light':     '#D7CEE2',   # jacaranda 100 — light tint backgrounds
    'bg_danger':            '#FCEBEA',   # red 100       — error/alert backgrounds
    'bg_danger_strong':     '#E53935',   # red 500       — strong danger fills
    'bg_safe':              '#F4F9F0',   # green 100     — success backgrounds
    'bg_safe_strong':       '#91C46C',   # green 500     — strong safe fills
    'bg_watch':             '#FFFAED',   # yellow 100    — warning backgrounds
    'bg_watch_strong':      '#FFD34E',   # yellow 500    — strong watch fills
    'bg_info':              '#EFE1C5',   # gold 100      — info/highlight backgrounds
    'bg_info_strong':       '#C89B3C',   # gold 300      — strong info fills

    # ── SEMANTIC — BORDERS ─────────────────────────────────────────────────
    # For dividers, outlines, input borders
    'border_subtle':        '#C1C1C1',   # charcoal 100  — subtle dividers, table lines
    'border_default':       '#787878',   # charcoal 200  — default input borders
    'border_strong':        '#2F2F2F',   # charcoal 300  — focused/active borders
    'border_primary':       '#7A5C9E',   # jacaranda 300 — primary accent borders
    'border_danger':        '#E53935',   # red 500       — error state borders
    'border_safe':          '#91C46C',   # green 500     — success state borders
    'border_watch':         '#FFD34E',   # yellow 500    — warning state borders

    # ── SEMANTIC — INTERACTIVE STATES ──────────────────────────────────────
    # For buttons, inputs, clickable elements
    'interactive_primary':          '#7A5C9E',   # jacaranda 300 — default
    'interactive_primary_hover':    '#5C4577',   # jacaranda 400 — hover
    'interactive_primary_active':   '#3D2E4F',   # jacaranda 500 — pressed
    'interactive_primary_disabled': '#D7CEE2',   # jacaranda 100 — disabled
    'interactive_secondary':        '#C89B3C',   # gold 300
    'interactive_secondary_hover':  '#96742D',   # gold 400

    # ── SEMANTIC — STATUS / BADGES ─────────────────────────────────────────
    # For pills, tags, status indicators
    'status_default_bg':    '#FCEBEA',   # red 100
    'status_default_text':  '#8D2623',   # red 700
    'status_safe_bg':       '#F4F9F0',   # green 100
    'status_safe_text':     '#5B7944',   # green 700
    'status_watch_bg':      '#FFFAED',   # yellow 100
    'status_watch_text':    '#9D8232',   # yellow 700
    'status_info_bg':       '#EFE1C5',   # gold 100
    'status_info_text':     '#96742D',   # gold 400
    'status_neutral_bg':    '#FAF9F5',   # off-white 200
    'status_neutral_text':  '#2F2F2F',   # charcoal 300

    # ── SEMANTIC — SHADOWS / OVERLAYS ──────────────────────────────────────
    'overlay':              'rgba(0, 0, 0, 0.4)',   # modal backdrops
    'shadow_sm':            '0 1px 3px rgba(0,0,0,0.08)',
    'shadow_md':            '0 4px 12px rgba(0,0,0,0.10)',
    'shadow_lg':            '0 8px 24px rgba(0,0,0,0.12)',

}

# ── SHORTHAND HELPERS ─────────────────────────────────────────────────────────

def p(hue, shade):
    """
    Shorthand palette accessor.
    p('jacaranda', 300) -> '#7A5C9E'
    p('red', 100)       -> '#FCEBEA'
    """
    return palette[hue][shade]


def f(role):
    """
    Shorthand font accessor.
    f('heading') -> 'Inter'
    f('body')    -> 'DM Sans'
    f('mono')    -> 'JetBrains Mono'
    """
    return fonts[role]


def s(role):
    """
    Shorthand size accessor.
    s('title') -> 15
    s('body')  -> 10
    """
    return sizes[role]


# ── GRADIENT HELPERS ──────────────────────────────────────────────────────────

def gradient(hue, shades=None):
    """
    Return a list of hex colours for a gradient within one hue.
    Default returns [100, 200, 300, 400, 500] — good for bar charts.

    Usage:
        bars = plt.bar(x, y, color=gradient('jacaranda'))
    """
    if shades is None:
        shades = [100, 200, 300, 400, 500]
    return [palette[hue][s] for s in shades]


def traffic_light(n_segments=3):
    """
    Return green/yellow/red colours for traffic light charts.
    """
    if n_segments == 3:
        return [palette['green'][500], palette['yellow'][500], palette['red'][500]]
    colors = [palette['green'][500], palette['yellow'][500], palette['red'][500]]
    cmap = mcolors.LinearSegmentedColormap.from_list('traffic', colors)
    return [mcolors.to_hex(cmap(i / (n_segments - 1))) for i in range(n_segments)]


def diverging(n=9):
    """
    Green-to-red diverging scale — useful for risk heatmaps.
    """
    colors = [palette['green'][400], palette['yellow'][400], palette['red'][400]]
    cmap = mcolors.LinearSegmentedColormap.from_list('diverging', colors)
    return [mcolors.to_hex(cmap(i / (n - 1))) for i in range(n)]


def multi_series():
    """
    Return the three brand colours for multi-series charts.
    Usage: colors = multi_series()
    """
    return [palette['chart_primary'], palette['chart_secondary'], palette['chart_tertiary']]


# ── CHART STYLE ───────────────────────────────────────────────────────────────

def set_style():
    """
    Apply global matplotlib defaults. Call once at the top of each notebook.
    Swap fonts or sizes here by editing the fonts/sizes dicts above.
    """
    plt.rcParams.update({
        # Figure
        'figure.figsize':           (11, 5),
        'figure.facecolor':         'white',
        'figure.dpi':               120,

        # Axes
        'axes.facecolor':           'white',
        'axes.edgecolor':           palette['charcoal'][100],
        'axes.labelcolor':          palette['charcoal'][400],
        'axes.labelsize':           sizes['body'],
        'axes.labelpad':            8,
        'axes.titlesize':           sizes['title'],
        'axes.titleweight':         'bold',
        'axes.titlecolor':          palette['charcoal'][500],
        'axes.titlepad':            12,
        'axes.spines.top':          False,
        'axes.spines.right':        False,
        'axes.grid':                True,
        'axes.axisbelow':           True,

        # Grid
        'grid.color':               palette['charcoal'][100],
        'grid.linewidth':           0.8,
        'grid.linestyle':           '--',

        # Ticks
        'xtick.color':              palette['charcoal'][200],
        'ytick.color':              palette['charcoal'][200],
        'xtick.labelsize':          sizes['small'],
        'ytick.labelsize':          sizes['small'],
        'xtick.major.pad':          6,
        'ytick.major.pad':          6,

        # Font — body font for all general text
        'font.family':              'sans-serif',
        'font.sans-serif':          [fonts['body']] + fonts['body_fallback'],
        'text.color':               palette['charcoal'][400],

        # Legend
        'legend.frameon':           False,
        'legend.fontsize':          sizes['small'],
        'legend.title_fontsize':    sizes['body'],

        # Bars
        'patch.facecolor':          palette['jacaranda'][300],

        # Lines
        'lines.linewidth':          2.0,
        'lines.color':              palette['jacaranda'][300],
    })


# ── TEXT HELPERS ──────────────────────────────────────────────────────────────

def chart_title(ax, title, subtitle=None):
    """
    Add a styled title and optional subtitle to an axes object.

    Usage:
        fig, ax = plt.subplots()
        chart_title(ax, 'Default Rate by Purpose', 'German Credit Dataset — 1,000 loans')
    """
    ax.set_title(
        title,
        fontfamily=fonts['heading'],
        fontsize=sizes['title'],
        fontweight='bold',
        color=palette['charcoal'][500],
        pad=16 if subtitle else 12,
        loc='left'
    )
    if subtitle:
        ax.annotate(
            subtitle,
            xy=(0, 1),
            xycoords='axes fraction',
            xytext=(0, 1.02),
            textcoords='axes fraction',
            fontfamily=fonts['body'],
            fontsize=sizes['small'],
            color=palette['charcoal'][200],
            va='bottom'
        )


def annotate(ax, x, y, text, color=None, offset=(0, 8)):
    """
    Add a styled data label annotation above a bar or point.

    Usage:
        annotate(ax, bar.get_x(), bar.get_height(), '32%')
    """
    ax.annotate(
        text,
        xy=(x, y),
        xytext=(offset[0], offset[1]),
        textcoords='offset points',
        fontfamily=fonts['mono'],
        fontsize=sizes['mono'],
        color=color or palette['charcoal'][200],
        ha='center',
        va='bottom'
    )


# ── SPECIMEN SHEETS ───────────────────────────────────────────────────────────

def show_palette():
    """
    Render a visual swatch of the full colour palette.
    """
    brand_hues = ['off_white', 'olive', 'jacaranda', 'gold', 'charcoal']
    brand_shades = [100, 200, 300, 400, 500]
    risk_hues = ['red', 'green', 'yellow']
    risk_shades = [100, 200, 300, 400, 500, 600, 700, 800, 900]

    rows = [(hue, brand_shades) for hue in brand_hues] + [(hue, risk_shades) for hue in risk_hues]

    fig, axes = plt.subplots(len(rows), 1, figsize=(13, len(rows) * 1.0))
    fig.patch.set_facecolor('white')

    for ax, (hue, shades) in zip(axes, rows):
        colors = [palette[hue][s] for s in shades]
        for i, (shade, color) in enumerate(zip(shades, colors)):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
            rgb = mcolors.to_rgb(color)
            brightness = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
            text_color = '#0A0A0A' if brightness > 0.5 else '#FFFFFF'
            ax.text(i + 0.5, 0.5, str(shade),
                    ha='center', va='center',
                    fontsize=8, color=text_color,
                    fontweight='bold',
                    fontfamily=fonts['mono'])
        ax.set_xlim(0, len(shades))
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([])
        label_shade = 400 if hue in brand_hues else 600
        ax.set_ylabel(hue.replace('_', ' ').title(),
                      rotation=0, labelpad=55, va='center',
                      fontsize=10, fontweight='bold',
                      color=palette[hue][label_shade],
                      fontfamily=fonts['heading'])
        for spine in ax.spines.values():
            spine.set_visible(False)

    plt.suptitle('Colour Palette', fontsize=sizes['title'],
                 fontweight='bold', color=palette['charcoal'][500],
                 fontfamily=fonts['heading'], y=1.01)
    plt.tight_layout()
    plt.show()


def show_fonts():
    """
    Render a font specimen sheet showing all three fonts at all sizes.
    """
    fig, ax = plt.subplots(figsize=(13, 9))
    fig.patch.set_facecolor('white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(0, 9.6, 'Font Specimen',
            fontfamily=fonts['heading'], fontsize=sizes['display'],
            fontweight='bold', color=palette['charcoal'][500], va='top')

    # Divider
    ax.axhline(9.2, color=palette['jacaranda'][200], linewidth=1.5, xmin=0, xmax=1)

    font_specs = [
        (fonts['heading'], 'Heading — Inter',     'HEADING / TITLES / SECTION LABELS',         palette['jacaranda'][300]),
        (fonts['body'],    'Body — DM Sans',       'Body text / Axis labels / Legend / Notes',  palette['gold'][400]),
        (fonts['mono'],    'Mono — JetBrains Mono','0123456789  |  Data labels / Numbers / Code', palette['olive'][300]),
    ]

    y = 8.6
    for font, label_text, specimen, color in font_specs:
        # Font role label
        ax.text(0, y, label_text,
                fontfamily=fonts['body'], fontsize=sizes['tiny'],
                color=palette['charcoal'][200], va='top', fontstyle='italic')
        y -= 0.4

        # Specimen text at display size
        ax.text(0, y, specimen,
                fontfamily=font, fontsize=sizes['display'],
                fontweight='bold', color=color, va='top')
        y -= 0.85

        # Size scale
        for size_name, size_val in sizes.items():
            ax.text(0, y, f'{size_name} ({size_val}pt) — The quick brown fox',
                    fontfamily=font, fontsize=size_val,
                    color=palette['charcoal'][400], va='top')
            y -= (size_val / 10) * 0.38

        y -= 0.3
        ax.axhline(y + 0.1, color=palette['charcoal'][100], linewidth=0.8, xmin=0, xmax=1)
        y -= 0.2

    plt.tight_layout()
    plt.show()


def style_df(df, gradient_cols=None, gradient_cmap='Purples', gradient_vmin=None,
             gradient_vmax=None, gradient_axis=0, highlight_nulls=False):
    """Apply clean consistent styling to any DataFrame output."""
    BG_HEADER = '#1F4E79'
    BG_EVEN   = '#DEEAF1'
    BG_ODD    = '#FFFFFF'
    BG_HOVER  = '#F3EDFC'   # purple 50 — your bg_primary_light
    TXT_BODY  = '#1A1A1A'

    styled = df.style.set_properties(**{
        'font-family': 'DM Sans, Arial, sans-serif',
        'font-size':   '12px',
        'color':       TXT_BODY,
        'border':      '1px solid #EBEBEB',
        'padding':     '6px 12px',
    }).set_table_styles([
        # Header row
        {'selector': 'thead tr th', 'props': [
            ('background-color', BG_HEADER),
            ('color', 'white'),
            ('font-weight', 'bold'),
            ('font-size', '12px'),
            ('padding', '8px 12px'),
            ('text-align', 'left'),
        ]},
        # Body cells — alternating (target td so it beats inline set_properties)
        {'selector': 'tbody tr:nth-child(even) td', 'props': [
            ('background-color', BG_EVEN),
        ]},
        {'selector': 'tbody tr:nth-child(odd) td', 'props': [
            ('background-color', BG_ODD),
        ]},
        # Index labels (count/mean/std...) — these are th, need their own bg + text colour
        {'selector': 'tbody tr th', 'props': [
            ('background-color', BG_ODD),
            ('color', TXT_BODY),
        ]},
        # Hover — resolved hex, not a token string
        {'selector': 'tbody tr:hover td', 'props': [
            ('background-color', BG_HOVER),
        ]},
    ])
    if gradient_cols:
        styled = styled.background_gradient(
            subset=gradient_cols,
            cmap=gradient_cmap,
            vmin=gradient_vmin,
            vmax=gradient_vmax,
            axis=gradient_axis,
        )
    if highlight_nulls:
        styled = styled.highlight_null(color='#FCEBEA')

    styled = styled.format(precision=2, na_rep='—')
    return styled

def show_style_guide():
    """
    Render a complete style guide — palette, fonts, and example chart elements
    together. Your personal brand spec sheet.
    """
    fig = plt.figure(figsize=(14, 18))
    fig.patch.set_facecolor('white')

    # ── Header ──
    fig.text(0.05, 0.97, 'Credit Risk ML — Design System',
             fontfamily=fonts['heading'], fontsize=sizes['display'],
             fontweight='bold', color=palette['jacaranda'][300], va='top')
    fig.text(0.05, 0.955, 'Colour palette · Typography · Chart elements',
             fontfamily=fonts['body'], fontsize=sizes['body'],
             color=palette['charcoal'][200], va='top')

    # ── Palette swatches ──
    hues = ['off_white', 'olive', 'jacaranda', 'gold', 'charcoal', 'red', 'green', 'yellow']
    risk_hues = ('red', 'green', 'yellow')
    for row, hue in enumerate(hues):
        shades = [100, 300, 500, 700, 900] if hue in risk_hues else [100, 200, 300, 400, 500]
        label_shade = 600 if hue in risk_hues else 400
        for col, shade in enumerate(shades):
            left = 0.05 + col * 0.085
            bottom = 0.845 - row * 0.038
            color = palette[hue][shade]
            ax_swatch = fig.add_axes([left, bottom, 0.08, 0.033])
            ax_swatch.add_patch(plt.Rectangle((0, 0), 1, 1, color=color,
                                              transform=ax_swatch.transAxes))
            rgb = mcolors.to_rgb(color)
            brightness = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
            tc = '#0A0A0A' if brightness > 0.5 else '#FFFFFF'
            ax_swatch.text(0.5, 0.5, str(shade), ha='center', va='center',
                           fontsize=6.5, color=tc, fontweight='bold',
                           fontfamily=fonts['mono'],
                           transform=ax_swatch.transAxes)
            ax_swatch.axis('off')
        # Hue label
        fig.text(0.05 + 5 * 0.085 + 0.005, 0.845 - row * 0.038 + 0.012,
                 hue.replace('_', ' ').title(), fontfamily=fonts['heading'],
                 fontsize=8, color=palette[hue][label_shade], fontweight='bold', va='center')

    # ── Example bar chart ──
    ax_bar = fig.add_axes([0.05, 0.49, 0.55, 0.22])
    categories = ['Car', 'Furniture', 'Education', 'Business', 'Repairs']
    default_rates = [0.24, 0.31, 0.38, 0.42, 0.18]
    bars = ax_bar.bar(categories, default_rates,
                      color=gradient('jacaranda'),
                      width=0.6, edgecolor='white', linewidth=0.8)
    ax_bar.set_ylim(0, 0.55)
    ax_bar.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)
    ax_bar.grid(axis='y', color=palette['charcoal'][100], linestyle='--', linewidth=0.8)
    ax_bar.set_axisbelow(True)
    for bar in bars:
        ax_bar.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.01,
                    f'{bar.get_height():.0%}',
                    ha='center', va='bottom',
                    fontfamily=fonts['mono'], fontsize=sizes['mono'],
                    color=palette['charcoal'][400])
    ax_bar.set_title('Default Rate by Loan Purpose',
                     fontfamily=fonts['heading'], fontsize=sizes['subtitle'],
                     fontweight='bold', color=palette['charcoal'][500],
                     loc='left', pad=10)
    ax_bar.tick_params(labelsize=sizes['small'])
    for label in ax_bar.get_xticklabels():
        label.set_fontfamily(fonts['body'])
    for label in ax_bar.get_yticklabels():
        label.set_fontfamily(fonts['mono'])

    # ── Traffic light chart ──
    ax_tl = fig.add_axes([0.65, 0.49, 0.32, 0.22])
    risk_bands = ['Low\n(<10% PD)', 'Medium\n(10-25% PD)', 'High\n(>25% PD)']
    counts = [580, 280, 140]
    tl_colors = traffic_light(3)
    ax_tl.bar(risk_bands, counts, color=tl_colors,
              width=0.6, edgecolor='white', linewidth=0.8)
    ax_tl.spines['top'].set_visible(False)
    ax_tl.spines['right'].set_visible(False)
    ax_tl.grid(axis='y', color=palette['charcoal'][100], linestyle='--', linewidth=0.8)
    ax_tl.set_axisbelow(True)
    ax_tl.set_title('Portfolio Risk Segmentation',
                    fontfamily=fonts['heading'], fontsize=sizes['subtitle'],
                    fontweight='bold', color=palette['charcoal'][500],
                    loc='left', pad=10)
    ax_tl.tick_params(labelsize=sizes['small'])
    for label in ax_tl.get_xticklabels():
        label.set_fontfamily(fonts['body'])
    for label in ax_tl.get_yticklabels():
        label.set_fontfamily(fonts['mono'])

    # ── Typography specimen ──
    ax_type = fig.add_axes([0.05, 0.05, 0.9, 0.38])
    ax_type.axis('off')
    ax_type.set_xlim(0, 10)
    ax_type.set_ylim(0, 10)

    ax_type.axhline(9.7, color=palette['charcoal'][100], linewidth=1)
    ax_type.text(0, 9.4, 'Typography',
                 fontfamily=fonts['heading'], fontsize=sizes['subtitle'],
                 fontweight='bold', color=palette['charcoal'][400], va='top')

    type_specs = [
        (fonts['heading'], sizes['title'],    'bold',  palette['jacaranda'][300], f"Inter — {sizes['title']}pt Bold — Chart Titles & Headers"),
        (fonts['heading'], sizes['subtitle'], 'bold',  palette['jacaranda'][200], f"Inter — {sizes['subtitle']}pt Bold — Subtitles & Section Labels"),
        (fonts['body'],    sizes['body'],     'normal',palette['charcoal'][400],  f"DM Sans — {sizes['body']}pt — Axis Labels, Legend, Body Text"),
        (fonts['body'],    sizes['small'],    'normal',palette['charcoal'][200],  f"DM Sans — {sizes['small']}pt — Tick Labels, Secondary Annotations"),
        (fonts['mono'],    sizes['mono'],     'normal',palette['charcoal'][400],  f"JetBrains Mono — {sizes['mono']}pt — 0123456789  |  Data Labels & Numbers"),
        (fonts['mono'],    sizes['tiny'],     'normal',palette['charcoal'][200],  f"JetBrains Mono — {sizes['tiny']}pt — Dense Tables, Footnotes"),
    ]

    y = 8.6
    for font, size, weight, color, specimen in type_specs:
        ax_type.text(0, y, specimen,
                     fontfamily=font, fontsize=size,
                     fontweight=weight, color=color, va='top')
        y -= (size / 10) * 0.7 + 0.2

    plt.savefig('/mnt/user-data/outputs/style_guide_preview.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.show()
    print("Style guide also saved as style_guide_preview.png")


def show_tokens():
    """
    Visual reference card for all semantic palette tokens, grouped by category.
    Run this whenever you need a reminder of what token to use.
    """

    groups = [
        {
            'label': 'Data Visualisation',
            'desc':  'Use for chart bars, lines and risk indicators',
            'tokens': [
                ('default_colour',   'Default / loss / high risk'),
                ('safe_colour',      'Performing / approve / low risk'),
                ('watch_colour',     'Watch / caution / medium risk'),
                ('chart_primary',    'Main data series'),
                ('chart_secondary',  'Secondary data series'),
                ('chart_tertiary',   'Third data series'),
                ('chart_fourth',     'Fourth data series'),
            ]
        },
        {
            'label': 'Typography',
            'desc':  'Use for text elements — labels, headings, hints',
            'tokens': [
                ('text_primary',     'Headlines, body text'),
                ('text_secondary',   'Subheadings, axis labels'),
                ('text_tertiary',    'Hints, placeholders, annotations'),
                ('text_disabled',    'Disabled state text'),
                ('text_inverse',     'Text on dark/coloured backgrounds'),
                ('text_on_primary',  'Text on jacaranda backgrounds'),
                ('text_on_danger',   'Text on red backgrounds'),
                ('text_link',        'Hyperlinks, clickable elements'),
            ]
        },
        {
            'label': 'Backgrounds',
            'desc':  'Use for surfaces, cards, panels, alert fills',
            'tokens': [
                ('bg_page',          'Outermost page background'),
                ('bg_surface',       'Cards, panels, modals'),
                ('bg_subtle',        'Table stripes, input fills'),
                ('bg_primary',       'Primary buttons, headers'),
                ('bg_primary_hover', 'Primary button hover state'),
                ('bg_primary_light', 'Light jacaranda tint backgrounds'),
                ('bg_danger',        'Error / alert backgrounds'),
                ('bg_danger_strong', 'Strong danger fills'),
                ('bg_safe',          'Success backgrounds'),
                ('bg_safe_strong',   'Strong safe fills'),
                ('bg_watch',         'Warning backgrounds'),
                ('bg_watch_strong',  'Strong watch fills'),
                ('bg_info',          'Info / highlight backgrounds'),
                ('bg_info_strong',   'Strong info fills'),
            ]
        },
        {
            'label': 'Borders',
            'desc':  'Use for dividers, outlines, input borders',
            'tokens': [
                ('border_subtle',    'Subtle dividers, table lines'),
                ('border_default',   'Default input borders'),
                ('border_strong',    'Focused / active borders'),
                ('border_primary',   'Primary accent borders'),
                ('border_danger',    'Error state borders'),
                ('border_safe',      'Success state borders'),
                ('border_watch',     'Warning state borders'),
            ]
        },
        {
            'label': 'Interactive States',
            'desc':  'Use for buttons, inputs, clickable elements',
            'tokens': [
                ('interactive_primary',          'Primary button — default'),
                ('interactive_primary_hover',    'Primary button — hover'),
                ('interactive_primary_active',   'Primary button — pressed'),
                ('interactive_primary_disabled', 'Primary button — disabled'),
                ('interactive_secondary',        'Secondary button — default'),
                ('interactive_secondary_hover',  'Secondary button — hover'),
            ]
        },
        {
            'label': 'Status Badges',
            'desc':  'Pre-paired bg/text colours for pills, tags, status chips',
            'tokens': [
                ('status_default_bg',    'Default/danger badge background'),
                ('status_default_text',  'Default/danger badge text'),
                ('status_safe_bg',       'Safe badge background'),
                ('status_safe_text',     'Safe badge text'),
                ('status_watch_bg',      'Watch badge background'),
                ('status_watch_text',    'Watch badge text'),
                ('status_info_bg',       'Info badge background'),
                ('status_info_text',     'Info badge text'),
                ('status_neutral_bg',    'Neutral badge background'),
                ('status_neutral_text',  'Neutral badge text'),
            ]
        },
    ]

    # ── Calculate total rows needed ───────────────────────────────────────────
    total_rows = sum(len(g['tokens']) + 2 for g in groups)  # +2 = header + spacer
    row_h      = 0.38
    fig_h      = max(8, total_rows * row_h + 1)

    fig, ax = plt.subplots(figsize=(13, fig_h))
    fig.patch.set_facecolor('white')
    ax.axis('off')
    ax.set_xlim(0, 10)

    total_plot_h = total_rows * row_h
    ax.set_ylim(0, total_plot_h + 0.5)

    # ── Title ─────────────────────────────────────────────────────────────────
    ax.text(0, total_plot_h + 0.3,
            'Semantic Token Reference',
            fontfamily=fonts['heading'], fontsize=sizes['title'],
            fontweight='bold', color=palette['charcoal'][500], va='top')

    # ── Column headers ────────────────────────────────────────────────────────
    header_y = total_plot_h - 0.1
    for x, label in [(1.5, 'Token'), (5.2, 'Hex'), (6.4, 'Usage')]:
        ax.text(x, header_y, label,
                fontfamily=fonts['body'], fontsize=sizes['small'],
                color=palette['charcoal'][200], va='top',
                fontstyle='italic')

    ax.axhline(header_y - 0.25,
               color=palette['charcoal'][100], linewidth=0.8,
               xmin=0, xmax=1)

    # ── Render groups ─────────────────────────────────────────────────────────
    y = header_y - 0.5

    for group in groups:

        # Group header band
        ax.add_patch(plt.Rectangle(
            (0, y - 0.05), 10, row_h * 0.85,
            color=palette['jacaranda'][100],
            clip_on=False, zorder=1
        ))
        ax.text(0.15, y + row_h * 0.35,
                group['label'],
                fontfamily=fonts['heading'], fontsize=sizes['body'],
                fontweight='bold', color=palette['jacaranda'][400],
                va='center', zorder=2)
        ax.text(5.2, y + row_h * 0.35,
                group['desc'],
                fontfamily=fonts['body'], fontsize=sizes['small'],
                color=palette['jacaranda'][300],
                va='center', fontstyle='italic', zorder=2)

        y -= row_h

        # Token rows
        for i, (token, desc) in enumerate(group['tokens']):
            hex_val = palette.get(token, None)
            if hex_val is None or not isinstance(hex_val, str):
                continue

            # Alternating row background
            if i % 2 == 0:
                ax.add_patch(plt.Rectangle(
                    (0, y - 0.04), 10, row_h * 0.88,
                    color=palette['off_white'][200],
                    clip_on=False, zorder=1
                ))

            # Colour swatch
            try:
                ax.add_patch(plt.Rectangle(
                    (0.1, y + 0.04), 1.0, row_h * 0.72,
                    color=hex_val,
                    clip_on=False, zorder=2,
                    linewidth=0.5,
                    edgecolor=palette['charcoal'][100]
                ))
            except Exception:
                pass

            # Token name
            ax.text(1.3, y + row_h * 0.4,
                    token,
                    fontfamily=fonts['mono'], fontsize=sizes['mono'],
                    color=palette['charcoal'][400],
                    va='center', zorder=2)

            # Hex value
            ax.text(5.2, y + row_h * 0.4,
                    hex_val,
                    fontfamily=fonts['mono'], fontsize=sizes['mono'] - 0.5,
                    color=palette['charcoal'][200],
                    va='center', zorder=2)

            # Usage description
            ax.text(6.4, y + row_h * 0.4,
                    desc,
                    fontfamily=fonts['body'], fontsize=sizes['small'],
                    color=palette['charcoal'][200],
                    va='center', zorder=2)

            y -= row_h

        # Spacer between groups
        y -= row_h * 0.4

    plt.tight_layout()
    plt.show()

# ══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ══════════════════════════════════════════════════════════════════════════════
#
#  IMPORT
#  from credit_utils import palette, fonts, sizes, p, f, s, set_style
#  set_style()
#
#  SINGLE COLOUR
#  plt.bar(x, y, color=p('jacaranda', 300))
#
#  GRADIENT BARS
#  plt.bar(x, y, color=gradient('jacaranda'))
#
#  MULTI-SERIES
#  colors = multi_series()   # [jacaranda, gold, olive]
#
#  TRAFFIC LIGHT
#  colors = traffic_light(3)
#
#  RISK HEATMAP
#  colors = diverging(9)
#
#  SEMANTIC
#  plt.bar(x, defaults,   color=palette['default_colour'])
#  plt.bar(x, performing, color=palette['safe_colour'])
#  plt.bar(x, watch,      color=palette['watch_colour'])
#
#  FONTS
#  ax.set_title('Chart', fontfamily=f('heading'), fontsize=s('title'))
#  ax.set_xlabel('Label', fontfamily=f('body'),   fontsize=s('body'))
#
#  STYLED TITLE + SUBTITLE
#  chart_title(ax, 'Default Rate by Purpose', 'German Credit — 1,000 loans')
#
#  DATA LABEL ANNOTATION
#  annotate(ax, x, height, '32.4%')
#
#  PREVIEW
#  show_palette()       # colour swatches
#  show_fonts()         # font specimen
#  show_style_guide()   # everything together
#
# ══════════════════════════════════════════════════════════════════════════════