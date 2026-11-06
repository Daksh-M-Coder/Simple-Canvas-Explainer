"""Brush-paint rich text renderer (PRD v1.2 §7.4, §7.8).

Supports markup: **bold**, *italic*, ~~strike~~, ==highlight==,
'- ' bullets, '1. ' numbered lines. OFL brush fonts with per-glyph
jitter (+-2 deg rotation, +-1 px position, tunable). Zone-aware
wrapping and scaling.
"""

# TODO: implement parse_markup(text) -> list[TextRun]
#       and render_rich_text(canvas, runs, zone) with jitter + highlighter bands.
