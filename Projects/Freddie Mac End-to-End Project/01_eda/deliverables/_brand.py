"""Pre-render hook: regenerate _brand.scss / _deck.scss / _report.scss from ER_BRAND."""
from er_toolkit.brand.quarto import build

build(".")
