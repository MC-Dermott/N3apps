"""Embeds selected tools from the separate maths-scaffolds project
(https://github.com/MC-Dermott/maths-scaffolds, ~/Documents/maths-scaffolds locally) as
interactive simulations inside a question's scaffold expander.

maths_scaffolds.html is a single self-contained page with several independent tools, switched
between via a JS `showApp('<id>-app')` call. Each tool has a "Random question" / "My own
numbers" mode; where a tool exposes plain numeric inputs for "My own numbers" mode, we inject a
small script (mirroring the pattern test_ui.py already uses for the Geometry Dash embed) that
jumps straight to that tool, switches it to custom mode, fills in this exact question's own
numbers, and clicks Start — so the scaffold walks through the same shape/value the question
shows, not an unrelated demo. Where a tool has no such input (time conversion only exposes a
mode pill), only the matching mode/direction is pre-selected and the tool generates its own
practice example.
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

_HTML_PATH = Path(__file__).parent / "assets" / "maths_scaffolds.html"
_html_cache = None


def _load_html():
    global _html_cache
    if _html_cache is None:
        _html_cache = _HTML_PATH.read_text(encoding="utf-8")
    return _html_cache


def _embed(app_id, setup_js, height=760):
    script = f"""
        <script>
        (function() {{
            showApp('{app_id}');
            {setup_js}
        }})();
        </script>
    </body>"""
    page = _load_html().replace("</body>", script)
    components.html(page, height=height, scrolling=True)


def _click_matching(container_id, data_attr, value):
    return f"""
    document.querySelectorAll('#{container_id} .pill').forEach(function(b) {{
        if (b.dataset.{data_attr} === '{value}') {{ b.click(); }}
    }});
    """


def render_rounding_scaffold(value, place_e):
    """value: the exact number being rounded. place_e: 3=nearest 1000, 2=nearest 100,
    1=nearest 10, 0=nearest whole number, -1/-2/-3 = 1/2/3 decimal places (matches the
    scaffold's own LEVELS table in maths_scaffolds.html)."""
    setup_js = f"""
    document.getElementById('rn-numInput').value = '{value}';
    document.querySelectorAll('#rn-pillRow .pill').forEach(function(b) {{
        if (Number(b.dataset.e) === {place_e}) {{ b.click(); }}
    }});
    document.getElementById('rn-startBtn').click();
    """
    _embed("rn-app", setup_js, height=560)


def render_l_shape_perimeter_scaffold(width, height, notch_width, notch_height):
    """Mirrors topics/shape_space_and_measures/_helpers.make_l_shape()'s W, H, a, b exactly —
    the scaffold's 'BR' orientation produces the identical vertex layout, so the diagram it
    draws matches the question's own diagram, not just the same style of shape."""
    setup_js = (
        _click_matching("ls-modePills", "mode", "custom")
        + _click_matching("ls-orientationPills", "orient", "BR")
        + f"""
    document.getElementById('ls-widthInput').value = {width};
    document.getElementById('ls-heightInput').value = {height};
    document.getElementById('ls-notchWInput').value = {notch_width};
    document.getElementById('ls-notchHInput').value = {notch_height};
    document.getElementById('ls-startBtn').click();
    """
    )
    _embed("ls-app", setup_js, height=760)


def render_time_conversion_scaffold(direction):
    """direction: '12to24' or '24to12'. This tool has no exposed field for an exact time — it
    always generates its own random practice time — so this only pre-selects the matching
    conversion direction, it does not mirror the question's own time."""
    setup_js = (
        _click_matching("tc-directionPills", "direction", direction)
        + "document.getElementById('tc-startBtn').click();"
    )
    _embed("tc-app", setup_js, height=520)
