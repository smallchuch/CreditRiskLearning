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
# To swap a colour: change the hex string. Full 100-900 scale per hue.
# 100 = lightest tint, 900 = darkest shade, 500 = base colour.

palette = {

    # ── PURPLE — Brand Primary ─────────────────────────────────────────────
    # Use for: main chart bars/lines, primary headers, key callouts
    'purple': {
        100: '#F1EAFB',   # barely-there tint — panel backgrounds, table fills
        200: '#DCCAF5',   # light tint — hover states, subtle highlights
        300: '#C0A0ED',   # soft — secondary bars, light chart elements
        400: '#9D6CE4',   # medium — supporting data series
        500: '#732DD9',   # BASE — primary bars, main data series, headings
        600: '#5E26AF',   # dark — emphasis, selected states
        700: '#491F86',   # darker — strong emphasis
        800: '#34185C',   # very dark — near-black text on light backgrounds
        900: '#1F1133',   # deepest — backgrounds only, use sparingly
    },

    # ── CYAN — Brand Secondary ─────────────────────────────────────────────
    # Use for: secondary data series, accent lines, highlights alongside purple
    'cyan': {
        100: '#E6FCFF',   # barely-there — background washes
        200: '#C2F9FF',   # light — subtle highlights
        300: '#92F5FF',   # soft — secondary chart fills
        400: '#56F0FF',   # medium-light — supporting accents
        500: '#0EEAFF',   # BASE — secondary bars/lines, accent elements
        600: '#0DBDCE',   # dark — stronger accent, borders
        700: '#0C909D',   # darker — text on light cyan backgrounds
        800: '#0B636C',   # very dark — high contrast use
        900: '#0A363B',   # deepest — use sparingly
    },

    # ── ORANGE — Brand Tertiary ────────────────────────────────────────────
    # Use for: third data series, callout boxes, highlights, annotations
    'orange': {
        100: '#FFEEE8',   # barely-there — background tints
        200: '#FFD5C7',   # light — soft fills
        300: '#FFB39B',   # soft — tertiary chart fills
        400: '#FF8964',   # medium — supporting highlights
        500: '#FF5722',   # BASE — tertiary bars/lines, callouts
        600: '#CE471D',   # dark — stronger callouts, borders
        700: '#9D3818',   # darker — text on light orange backgrounds
        800: '#6C2813',   # very dark — high contrast
        900: '#3B190E',   # deepest — use sparingly
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

    # ── GREY — Neutral / Secondary Information ─────────────────────────────
    # Use for: axes, gridlines, secondary labels, benchmarks, disabled states
    'grey': {
        100: '#F7F7F7',   # near white — page/panel backgrounds
        200: '#EBEBEB',   # light — dividers, table borders
        300: '#D4D4D4',   # soft — gridlines, subtle borders
        400: '#ABABAB',   # medium — secondary axis ticks, placeholders
        500: '#7F7F7F',   # BASE — secondary labels, annotations
        600: '#5C5C5C',   # dark — body text, axis labels
        700: '#3D3D3D',   # darker — strong secondary text
        800: '#262626',   # very dark — primary body text, titles
        900: '#0A0A0A',   # near black — maximum contrast text
    },

    # ── WHITE ──────────────────────────────────────────────────────────────
    'white': '#FFFFFF',   # chart backgrounds, card fills, text on dark

    # ── SEMANTIC SHORTCUTS ─────────────────────────────────────────────────
    # Convenience keys mapping credit risk concepts to colours
    'default_colour':  '#E53935',   # = red 500   — default / loss
    'safe_colour':     '#91C46C',   # = green 500 — performing / approve
    'watch_colour':    '#FFD34E',   # = yellow 500 — watch / caution
    'primary':         '#732DD9',   # = purple 500 — brand primary
    'secondary':       '#0EEAFF',   # = cyan 500   — brand secondary
    'tertiary':        '#FF5722',   # = orange 500 — brand tertiary
    'text':            '#262626',   # = grey 800   — primary text
    'subtext':         '#7F7F7F',   # = grey 500   — secondary text
    'background':      '#F7F7F7',   # = grey 100   — backgrounds
    'border':          '#EBEBEB',   # = grey 200   — borders/dividers
}


# ── SHORTHAND HELPERS ─────────────────────────────────────────────────────────

def p(hue, shade):
    """
    Shorthand palette accessor.
    p('purple', 500) -> '#732DD9'
    p('red', 100)    -> '#FCEBEA'
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
    Default returns [200, 300, 400, 500, 600, 700] — good for bar charts.

    Usage:
        bars = plt.bar(x, y, color=gradient('purple'))
    """
    if shades is None:
        shades = [200, 300, 400, 500, 600, 700]
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
    return [palette['primary'], palette['secondary'], palette['tertiary']]


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
        'axes.edgecolor':           palette['grey'][300],
        'axes.labelcolor':          palette['grey'][800],
        'axes.labelsize':           sizes['body'],
        'axes.labelpad':            8,
        'axes.titlesize':           sizes['title'],
        'axes.titleweight':         'bold',
        'axes.titlecolor':          palette['grey'][900],
        'axes.titlepad':            12,
        'axes.spines.top':          False,
        'axes.spines.right':        False,
        'axes.grid':                True,
        'axes.axisbelow':           True,

        # Grid
        'grid.color':               palette['grey'][200],
        'grid.linewidth':           0.8,
        'grid.linestyle':           '--',

        # Ticks
        'xtick.color':              palette['grey'][600],
        'ytick.color':              palette['grey'][600],
        'xtick.labelsize':          sizes['small'],
        'ytick.labelsize':          sizes['small'],
        'xtick.major.pad':          6,
        'ytick.major.pad':          6,

        # Font — body font for all general text
        'font.family':              'sans-serif',
        'font.sans-serif':          [fonts['body']] + fonts['body_fallback'],
        'text.color':               palette['grey'][800],

        # Legend
        'legend.frameon':           False,
        'legend.fontsize':          sizes['small'],
        'legend.title_fontsize':    sizes['body'],

        # Bars
        'patch.facecolor':          palette['purple'][500],

        # Lines
        'lines.linewidth':          2.0,
        'lines.color':              palette['purple'][500],
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
        color=palette['grey'][900],
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
            color=palette['grey'][500],
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
        color=color or palette['grey'][600],
        ha='center',
        va='bottom'
    )


# ── SPECIMEN SHEETS ───────────────────────────────────────────────────────────

def show_palette():
    """
    Render a visual swatch of the full colour palette.
    """
    hues = ['purple', 'cyan', 'orange', 'red', 'green', 'yellow', 'grey']
    shades = [100, 200, 300, 400, 500, 600, 700, 800, 900]

    fig, axes = plt.subplots(len(hues), 1, figsize=(13, len(hues) * 1.0))
    fig.patch.set_facecolor('white')

    for ax, hue in zip(axes, hues):
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
        ax.set_xlim(0, 9)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_ylabel(hue.capitalize(),
                      rotation=0, labelpad=55, va='center',
                      fontsize=10, fontweight='bold',
                      color=palette[hue][600],
                      fontfamily=fonts['heading'])
        for spine in ax.spines.values():
            spine.set_visible(False)

    plt.suptitle('Colour Palette', fontsize=sizes['title'],
                 fontweight='bold', color=palette['grey'][900],
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
            fontweight='bold', color=palette['grey'][900], va='top')

    # Divider
    ax.axhline(9.2, color=palette['purple'][300], linewidth=1.5, xmin=0, xmax=1)

    font_specs = [
        (fonts['heading'], 'Heading — Inter',     'HEADING / TITLES / SECTION LABELS',         palette['purple'][500]),
        (fonts['body'],    'Body — DM Sans',       'Body text / Axis labels / Legend / Notes',  palette['cyan'][600]),
        (fonts['mono'],    'Mono — JetBrains Mono','0123456789  |  Data labels / Numbers / Code', palette['orange'][500]),
    ]

    y = 8.6
    for font, label_text, specimen, color in font_specs:
        # Font role label
        ax.text(0, y, label_text,
                fontfamily=fonts['body'], fontsize=sizes['tiny'],
                color=palette['grey'][500], va='top', fontstyle='italic')
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
                    color=palette['grey'][700], va='top')
            y -= (size_val / 10) * 0.38

        y -= 0.3
        ax.axhline(y + 0.1, color=palette['grey'][200], linewidth=0.8, xmin=0, xmax=1)
        y -= 0.2

    plt.tight_layout()
    plt.show()


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
             fontweight='bold', color=palette['purple'][500], va='top')
    fig.text(0.05, 0.955, 'Colour palette · Typography · Chart elements',
             fontfamily=fonts['body'], fontsize=sizes['body'],
             color=palette['grey'][500], va='top')

    # ── Palette swatches ──
    hues = ['purple', 'cyan', 'orange', 'red', 'green', 'yellow', 'grey']
    shades = [100, 300, 500, 700, 900]
    for row, hue in enumerate(hues):
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
                 hue.capitalize(), fontfamily=fonts['heading'],
                 fontsize=8, color=palette[hue][600], fontweight='bold', va='center')

    # ── Example bar chart ──
    ax_bar = fig.add_axes([0.05, 0.49, 0.55, 0.22])
    categories = ['Car', 'Furniture', 'Education', 'Business', 'Repairs']
    default_rates = [0.24, 0.31, 0.38, 0.42, 0.18]
    bars = ax_bar.bar(categories, default_rates,
                      color=gradient('purple', [300, 400, 500, 600, 700]),
                      width=0.6, edgecolor='white', linewidth=0.8)
    ax_bar.set_ylim(0, 0.55)
    ax_bar.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)
    ax_bar.grid(axis='y', color=palette['grey'][200], linestyle='--', linewidth=0.8)
    ax_bar.set_axisbelow(True)
    for bar in bars:
        ax_bar.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.01,
                    f'{bar.get_height():.0%}',
                    ha='center', va='bottom',
                    fontfamily=fonts['mono'], fontsize=sizes['mono'],
                    color=palette['grey'][700])
    ax_bar.set_title('Default Rate by Loan Purpose',
                     fontfamily=fonts['heading'], fontsize=sizes['subtitle'],
                     fontweight='bold', color=palette['grey'][900],
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
    ax_tl.grid(axis='y', color=palette['grey'][200], linestyle='--', linewidth=0.8)
    ax_tl.set_axisbelow(True)
    ax_tl.set_title('Portfolio Risk Segmentation',
                    fontfamily=fonts['heading'], fontsize=sizes['subtitle'],
                    fontweight='bold', color=palette['grey'][900],
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

    ax_type.axhline(9.7, color=palette['grey'][200], linewidth=1)
    ax_type.text(0, 9.4, 'Typography',
                 fontfamily=fonts['heading'], fontsize=sizes['subtitle'],
                 fontweight='bold', color=palette['grey'][800], va='top')

    type_specs = [
        (fonts['heading'], sizes['title'],    'bold',  palette['purple'][500], f"Inter — {sizes['title']}pt Bold — Chart Titles & Headers"),
        (fonts['heading'], sizes['subtitle'], 'bold',  palette['purple'][400], f"Inter — {sizes['subtitle']}pt Bold — Subtitles & Section Labels"),
        (fonts['body'],    sizes['body'],     'normal',palette['grey'][700],   f"DM Sans — {sizes['body']}pt — Axis Labels, Legend, Body Text"),
        (fonts['body'],    sizes['small'],    'normal',palette['grey'][600],   f"DM Sans — {sizes['small']}pt — Tick Labels, Secondary Annotations"),
        (fonts['mono'],    sizes['mono'],     'normal',palette['grey'][700],   f"JetBrains Mono — {sizes['mono']}pt — 0123456789  |  Data Labels & Numbers"),
        (fonts['mono'],    sizes['tiny'],     'normal',palette['grey'][500],   f"JetBrains Mono — {sizes['tiny']}pt — Dense Tables, Footnotes"),
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


# ══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE
# ══════════════════════════════════════════════════════════════════════════════
#
#  IMPORT
#  from credit_utils import palette, fonts, sizes, p, f, s, set_style
#  set_style()
#
#  SINGLE COLOUR
#  plt.bar(x, y, color=p('purple', 500))
#
#  GRADIENT BARS
#  plt.bar(x, y, color=gradient('purple'))
#
#  MULTI-SERIES
#  colors = multi_series()   # [purple, cyan, orange]
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