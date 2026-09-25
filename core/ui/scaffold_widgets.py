"""Interactive scaffold widgets shown inside a question's "🎮 Interactive scaffold" expander
(see core/ui/scaffold_ui.py's render_simulation), dispatched via the WIDGET_REGISTRY dict at
the bottom of this file — keyed by the same string a topic module puts in
`metadata["scaffold_widget"]`, called with `**metadata["scaffold_widget_params"]`.

Two families of widget live here:

1. Tools ported from the separate maths-scaffolds project
   (https://github.com/MC-Dermott/maths-scaffolds, ~/Documents/maths-scaffolds locally),
   embedded from assets/maths_scaffolds.html — a single self-contained page with several
   independent tools, switched between via a JS `showApp('<id>-app')` call.
2. Tools built directly for N3apps (not part of that separate project — see
   assets/managing_money_scaffolds.html, assets/numeracy_scaffolds.html and
   assets/shape_space_and_measures_scaffolds.html), one file per unit, each following the exact
   same structural pattern (a `showApp()`-switched set of appContainer divs) and copying the
   shared CSS design system from maths_scaffolds.html, purely so the embedding mechanism below
   can stay identical across both families.

Either way: each tool has a "Random question" / "My own numbers" mode; where a tool exposes
plain numeric inputs for "My own numbers" mode, we inject a small script (mirroring the pattern
test_ui.py already uses for the Geometry Dash embed) that jumps straight to that tool, switches
it to custom mode, fills in this exact question's own numbers, and clicks Start — so the
scaffold walks through the same shape/value the question shows, not an unrelated demo. Where a
tool has no such input, only the matching mode/direction is pre-selected and the tool generates
its own practice example — note this explicitly in that render function's docstring.
"""

import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

_ASSETS_DIR = Path(__file__).parent / "assets"
_html_cache = {}


def _json(value):
    """json.dumps with a belt-and-braces escape of '</' so a label/category string can never
    accidentally close the surrounding <script> tag once embedded."""
    return json.dumps(value).replace("</", "<\\/")


def _load_html(filename):
    if filename not in _html_cache:
        _html_cache[filename] = (_ASSETS_DIR / filename).read_text(encoding="utf-8")
    return _html_cache[filename]


def _embed(app_id, setup_js, height=760, html_file="maths_scaffolds.html"):
    script = f"""
        <script>
        (function() {{
            showApp('{app_id}');
            {setup_js}
        }})();
        </script>
    </body>"""
    page = _load_html(html_file).replace("</body>", script)
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


def render_bus_stop_division_scaffold(dividend, divisor):
    """dividend, divisor: whole numbers only (the bus-stop tool works digit-by-digit on a
    whole-number dividend, letting any decimal places in the quotient emerge naturally as the
    division continues — it doesn't accept a dividend that already has its own decimal point).
    Where a question's actual dividend has decimal places, pass it with the point removed (the
    same "ignore the point, divide, then put the point back" whole-number division used by
    topics/numeracy/decimal_multiplication_division.py's single-digit case), rather than the
    question's own formatted value. Unlike the other maths-scaffolds ports, this tool's own
    "My own numbers" mode has no plain numeric fields to fill in (pupils type digits straight
    into an empty bus stop instead), so this calls the window.bsStart() entry point added to
    N3apps's copy of assets/maths_scaffolds.html for this purpose."""
    setup_js = f"window.bsStart({_json({'dividend': dividend, 'divisor': divisor})});"
    _embed("bs-app", setup_js, height=640)


# ---------------------------------------------------------------------------
# Numeracy unit widgets — assets/numeracy_scaffolds.html. Each mirrors the exact numbers of
# the question that triggered it by switching the tool to "My own numbers" mode and filling
# in its custom fields before clicking Start (see module docstring for the general pattern).
# ---------------------------------------------------------------------------

def _set_value(elem_id, value):
    return f"document.getElementById('{elem_id}').value = {_json(str(value))};\n"


def render_decimal_column_scaffold(a, b, op):
    """a, b: the two numbers exactly as formatted in the question (strings, e.g. '27.58').
    op: '+' or '-'. Powers topics/numeracy/decimal_addition_subtraction.py."""
    setup_js = (
        _click_matching("dcc-modePills", "mode", "custom")
        + _set_value("dcc-aInput", a)
        + _set_value("dcc-bInput", b)
        + _click_matching("dcc-opPills", "op", op)
        + "document.getElementById('dcc-startBtn').click();"
    )
    _embed("dcc-app", setup_js, height=760, html_file="numeracy_scaffolds.html")


def render_lattice_multiplication_scaffold(a, b):
    """a, b: the two whole numbers to multiply, as strings or ints (e.g. '236', 47) — no
    decimal points. Pupils fill in each number's digits around the blank grid, multiply cell
    by cell (with a per-cell times-table hint button, mirroring the bus stop division tool's
    "Show table" toggle), then add down the diagonals with carry boxes exactly like the
    Decimal Column Calculator's addition mode. Not yet wired to a specific topic module —
    register a metadata["scaffold_widget"] = "lattice_multiplication" entry pointing here
    when one needs it."""
    setup_js = (
        _click_matching("lat-modePills", "mode", "custom")
        + _set_value("lat-aInput", a)
        + _set_value("lat-bInput", b)
        + "document.getElementById('lat-startBtn').click();"
    )
    _embed("lat-app", setup_js, height=820, html_file="numeracy_scaffolds.html")


def render_decimal_mul_div_scaffold(value, operation, kind, n):
    """value: the decimal being multiplied/divided (string, e.g. '16.3'). operation:
    'multiply' or 'divide'. kind: 'single_digit' (ignore-point method) or 'shift' (point
    moves for x/÷ 10/100/1000). n: the single digit, or the power of ten. Powers
    topics/numeracy/decimal_multiplication_division.py."""
    setup_js = (
        _click_matching("dms-modePills", "mode", "custom")
        + _click_matching("dms-kindPills", "kind", kind)
        + _set_value("dms-valueInput", value)
        + _click_matching("dms-opPills", "op", operation)
    )
    if kind == "single_digit":
        setup_js += _set_value("dms-nDigitInput", n)
    else:
        setup_js += _click_matching("dms-nPowerPills", "n", str(n))
    setup_js += "document.getElementById('dms-startBtn').click();"
    _embed("dms-app", setup_js, height=680, html_file="numeracy_scaffolds.html")


def render_workings_pad_scaffold(kind, unit="", **values):
    """kind: 'total' (a, b), 'difference' (start, removed), 'sharing' (total, n), or
    'multiply_subtract' (n, per_unit, start) — mirrors the four sub-generators in
    topics/numeracy/decimal_word_problems.py. unit: e.g. 'cm', 'kg', 'litres', 'ml'."""
    setup_js = (
        _click_matching("wp-modePills", "mode", "custom")
        + _click_matching("wp-kindPills", "kind", kind)
        + _set_value("wp-unitInput", unit)
    )
    field_map = {
        "total": {"a": "wp-aInput", "b": "wp-bInput"},
        "difference": {"start": "wp-startInput", "removed": "wp-removedInput"},
        "sharing": {"total": "wp-totalInput", "n": "wp-nInput"},
        "multiply_subtract": {"n": "wp-msCountInput", "per_unit": "wp-msPerUnitInput", "start": "wp-msStartInput"},
    }[kind]
    for key, elem_id in field_map.items():
        if key in values:
            setup_js += _set_value(elem_id, values[key])
    setup_js += "document.getElementById('wp-startBtn').click();"
    _embed("wp-app", setup_js, height=560, html_file="numeracy_scaffolds.html")


def render_fraction_bar_scaffold(amount, denom, num=1, unit="", two_step=False):
    """amount: the whole quantity the bar represents. denom/num: the fraction being found
    (num=1 for a unit fraction). two_step: True to add a final "what's left" stage (used by
    the two-step fraction_word_problems sub-types). Powers topics/numeracy/fraction_of_amount.py
    and topics/numeracy/fraction_word_problems.py."""
    setup_js = (
        _click_matching("fbs-modePills", "mode", "custom")
        + _set_value("fbs-amountInput", amount)
        + _set_value("fbs-denomInput", denom)
        + _set_value("fbs-numInput", num)
        + _set_value("fbs-unitInput", unit)
        + _click_matching("fbs-twoStepPills", "two", "yes" if two_step else "no")
        + "document.getElementById('fbs-startBtn').click();"
    )
    _embed("fbs-app", setup_js, height=620, html_file="numeracy_scaffolds.html")


def render_number_problem_solving_scaffold(kind, **kwargs):
    """kind: 'sorter' (numbers, focus), 'sequence' (terms, step, direction), or 'estimate'
    (a, b, op, place). Powers topics/numeracy/number_problem_solving.py's three levels."""
    setup_js = (
        _click_matching("nps-modePills", "mode", "custom")
        + _click_matching("nps-kindPills", "kind", kind)
    )
    if kind == "sorter":
        setup_js += (
            _set_value("nps-numbersInput", ",".join(str(v) for v in kwargs["numbers"]))
            + _click_matching("nps-focusPills", "focus", kwargs["focus"])
        )
    elif kind == "sequence":
        setup_js += (
            _set_value("nps-termsInput", ",".join(str(v) for v in kwargs["terms"]))
            + _set_value("nps-stepInput", kwargs["step"])
            + _click_matching("nps-dirPills", "dir", kwargs["direction"])
        )
    else:
        setup_js += (
            _set_value("nps-aInput", kwargs["a"])
            + _set_value("nps-bInput", kwargs["b"])
            + _click_matching("nps-opPills", "op", kwargs["op"])
            + _click_matching("nps-placePills", "place", str(kwargs["place"]))
        )
    setup_js += "document.getElementById('nps-startBtn').click();"
    _embed("nps-app", setup_js, height=680, html_file="numeracy_scaffolds.html")


def render_percentage_stepper_scaffold(kind, **kwargs):
    """kind: 'common' (pct_str, amount, unit), 'any' (pct, amount, unit), 'vat' (price, pct), or
    'compare' (pct1, base1, pct2, base2). Powers topics/numeracy/numeracy_percentages.py.
    'any' and 'vat' both walk through the ÷100 x amount method by dividing the AMOUNT by 100
    first (to find 1%) rather than dividing the percentage — 'vat' additionally opens by
    asking for the VAT percentage itself, then finishes with a chimney-sum addition of the
    price and VAT (see runChimneySum in numeracy_scaffolds.html)."""
    setup_js = (
        _click_matching("pct-modePills", "mode", "custom")
        + _click_matching("pct-kindPills", "kind", kind)
    )
    if kind == "common":
        setup_js += (
            _set_value("pct-commonPctInput", kwargs["pct_str"])
            + _set_value("pct-commonAmountInput", kwargs["amount"])
            + _set_value("pct-commonUnitInput", kwargs.get("unit", ""))
        )
    elif kind == "any":
        setup_js += (
            _set_value("pct-anyPctInput", kwargs["pct"])
            + _set_value("pct-anyAmountInput", kwargs["amount"])
            + _set_value("pct-anyUnitInput", kwargs.get("unit", ""))
        )
    elif kind == "vat":
        setup_js += (
            _set_value("pct-priceInput", kwargs["price"])
            + _set_value("pct-vatRateInput", kwargs.get("pct", 20))
        )
    else:
        setup_js += (
            _set_value("pct-pct1Input", kwargs["pct1"])
            + _set_value("pct-base1Input", kwargs["base1"])
            + _set_value("pct-pct2Input", kwargs["pct2"])
            + _set_value("pct-base2Input", kwargs["base2"])
        )
    setup_js += "document.getElementById('pct-startBtn').click();"
    _embed("pct-app", setup_js, height=680, html_file="numeracy_scaffolds.html")


def render_probability_fraction_scaffold(kind, **kwargs):
    """kind: 'dice'/'spinner'/'cards' (outcome, favourable, total), 'counters' (colours,
    counts, fav_colour), 'letters' (word, letter_mode, letter=''), 'without_replacement'
    (colour_a, count_a, colour_b, count_b), or 'table' (label, values, freqs, qmode, qvalue).
    Powers topics/numeracy/probability.py's Level 2/3 (Level 1 likelihood-in-words has no
    numeric mechanic, so it is left without a scaffold widget)."""
    setup_js = (
        _click_matching("pfb-modePills", "mode", "custom")
        + _click_matching("pfb-kindPills", "kind", kind)
    )
    if kind in ("dice", "spinner", "cards"):
        setup_js += (
            _set_value("pfb-outcomeInput", kwargs["outcome"])
            + _set_value("pfb-favInput", kwargs["favourable"])
            + _set_value("pfb-totalInput", kwargs["total"])
        )
        if kwargs.get("favourable_values"):
            setup_js += _set_value(
                "pfb-favValuesInput", ",".join(str(v) for v in kwargs["favourable_values"])
            )
    elif kind == "counters":
        setup_js += (
            _set_value("pfb-coloursInput", ",".join(kwargs["colours"]))
            + _set_value("pfb-countsInput", ",".join(str(c) for c in kwargs["counts"]))
            + _set_value("pfb-favColourInput", kwargs["fav_colour"])
        )
    elif kind == "letters":
        setup_js += (
            _set_value("pfb-wordInput", kwargs["word"])
            + _click_matching("pfb-letterModePills", "lettermode", kwargs["letter_mode"])
            + _set_value("pfb-letterInput", kwargs.get("letter", ""))
        )
    elif kind == "without_replacement":
        setup_js += (
            _set_value("pfb-colourAInput", kwargs["colour_a"])
            + _set_value("pfb-countAInput", kwargs["count_a"])
            + _set_value("pfb-colourBInput", kwargs["colour_b"])
            + _set_value("pfb-countBInput", kwargs["count_b"])
        )
    else:
        setup_js += (
            _set_value("pfb-labelInput", kwargs["label"])
            + _set_value("pfb-valuesInput", ",".join(str(v) for v in kwargs["values"]))
            + _set_value("pfb-freqsInput", ",".join(str(v) for v in kwargs["freqs"]))
            + _click_matching("pfb-qModePills", "qmode", kwargs["qmode"])
            + _set_value("pfb-qValueInput", kwargs["qvalue"])
        )
    setup_js += "document.getElementById('pfb-startBtn').click();"
    _embed("pfb-app", setup_js, height=680, html_file="numeracy_scaffolds.html")


def render_scale_stepper_scaffold(min_value, max_value, major_step, minor_step, marker_value, unit_label=""):
    """Mirrors topics/numeracy/reading_scales.py's Level 1 diagram_params exactly (same
    keys), so this widget always matches the static graduated_scale diagram shown above it."""
    setup_js = (
        _click_matching("ss-modePills", "mode", "custom")
        + _set_value("ss-minInput", min_value)
        + _set_value("ss-maxInput", max_value)
        + _set_value("ss-majorInput", major_step)
        + _set_value("ss-minorInput", minor_step)
        + _set_value("ss-markerInput", marker_value)
        + _set_value("ss-unitInput", unit_label)
        + "document.getElementById('ss-startBtn').click();"
    )
    _embed("ss-app", setup_js, height=520, html_file="numeracy_scaffolds.html")


def render_unit_conversion_scaffold(kind="metric", value=None, from_unit=None, to_unit=None, factor=None, mph=None):
    """kind: 'metric' (value, from_unit, to_unit, factor) or 'mph' (mph). Powers
    topics/numeracy/reading_scales.py's Level 2."""
    setup_js = _click_matching("uc-modePills", "mode", "custom") + _click_matching("uc-kindPills", "kind", kind)
    if kind == "mph":
        setup_js += _set_value("uc-mphInput", mph)
    else:
        setup_js += (
            _set_value("uc-valueInput", value)
            + _set_value("uc-fromInput", from_unit)
            + _set_value("uc-toInput", to_unit)
            + _set_value("uc-factorInput", factor)
        )
    setup_js += "document.getElementById('uc-startBtn').click();"
    _embed("uc-app", setup_js, height=480, html_file="numeracy_scaffolds.html")


# ---------------------------------------------------------------------------
# Managing Money widgets — assets/managing_money_scaffolds.html. Each tool there exposes a
# `window.<prefix>Start(params)` JS function (rather than filling individual DOM inputs like the
# ported tools above) since several of these take variable-length lists (receipt items, chart
# categories, raw tally data) that are awkward to drive by simulating field-by-field DOM edits —
# calling the tool's own JS entry point directly is simpler and just as faithful: it still jumps
# straight to the tool, switches it to "My own numbers" mode, and starts it on this exact
# question's values.
# ---------------------------------------------------------------------------


def render_wages_scaffold(kind, basic=0, overtime=0, bonus=0, tax=0, ni=0, pension=0):
    """kind: 'gross' (Level 1), 'deductions' (Level 2) or 'full' (Level 3, chains Gross Pay ->
    Total Deductions -> Net Pay). Unused fields for a given kind can be left at 0. Each stage
    has the pupil re-enter its named values one at a time, choose add or subtract, then work
    through the column sum with carrying/borrowing — mirrors topics/numeracy/
    decimal_addition_subtraction.py's own scaffold, fixed to money's 2 decimal places."""
    params = {
        "kind": kind, "basic": basic, "overtime": overtime, "bonus": bonus,
        "tax": tax, "ni": ni, "pension": pension,
    }
    setup_js = f"window.wgStart({_json(params)});"
    _embed("wg-app", setup_js, height=700, html_file="managing_money_scaffolds.html")


def render_receipt_scaffold(items, op="+"):
    """items: list of (label, amount) pairs (amounts always positive), in the order they
    should be entered. op: '+' to add every item, or '-' to subtract the later items from the
    first (used for a discount/deduction pair). The pupil must re-enter each amount, choose
    the operation themselves, then work through the column sum with carrying/borrowing —
    mirrors topics/numeracy/decimal_addition_subtraction.py's own scaffold, fixed to money's
    2 decimal places."""
    params = {"items": [list(i) for i in items], "op": op}
    setup_js = f"window.rcStart({_json(params)});"
    _embed("rc-app", setup_js, height=640, html_file="managing_money_scaffolds.html")


def render_bar_model_scaffold(total, mode, n, multiplier=None, multiplier_label=None):
    """mode: 'share' (split `total` into `n` equal parts, answer = one part) or 'group' (group
    `total` into boxes/groups of size `n`, rounding up, answer = number of groups). If
    `multiplier` is given, a second stage multiplies the stage-1 result by it (e.g. boxes needed
    x cost per box) — `multiplier_label` names that second value."""
    params = {"total": total, "mode": mode, "n": n, "multiplier": multiplier, "multiplierLabel": multiplier_label}
    setup_js = f"window.bmStart({_json(params)});"
    _embed("bm-app", setup_js, height=680, html_file="managing_money_scaffolds.html")


def render_percentage_method_scaffold(pct_label, amount):
    """pct_label: one of '50', '25', '10', '20', '75', '33⅓', '66⅔' — must match one of the
    scaffold's own method cards exactly (mirrors percentages_non_calculator.py's _PERCENTAGES /
    _THIRDS tables)."""
    setup_js = f"window.pmStart({_json({'pctLabel': pct_label, 'amount': amount})});"
    _embed("pm-app", setup_js, height=680, html_file="managing_money_scaffolds.html")


def render_percentage_calculator_scaffold(pct, amount):
    setup_js = f"window.pcStart({_json({'pct': pct, 'amount': amount})});"
    _embed("pc-app", setup_js, height=560, html_file="managing_money_scaffolds.html")


def render_percentage_increase_decrease_scaffold(is_increase, original, pct, new_amount):
    params = {"isIncrease": bool(is_increase), "original": original, "pct": pct, "newAmount": new_amount}
    setup_js = f"window.idStart({_json(params)});"
    _embed("id-app", setup_js, height=620, html_file="managing_money_scaffolds.html")


def render_pictograph_scaffold(categories, values, unit_value, relevant, op):
    """categories/values: the pictogram's full data (parallel lists). relevant: the subset of
    category names actually needed to answer this question, in the order they should be
    revealed. op: 'read' (single category, that's the answer), 'diff' (two categories,
    bigger - smaller) or 'sum' (every relevant category added together)."""
    params = {
        "categories": categories, "values": values, "unitValue": unit_value,
        "relevant": relevant, "op": op,
    }
    setup_js = f"window.syStart({_json(params)});"
    _embed("sy-app", setup_js, height=640, html_file="managing_money_scaffolds.html")


def render_bar_graph_scaffold(categories, group1, group1_name, relevant, op,
                                group2=None, group2_name=None):
    """categories/group1(/group2): the bar chart's full data. relevant: list of
    {"series": 1|2, "idx": i} dicts naming exactly which bars need to be clicked/revealed to
    answer this question, in order. op: 'sum' (add every relevant bar) or 'diff'
    (largest - smallest of the relevant bars)."""
    params = {
        "categories": categories, "group1": group1, "group1Name": group1_name,
        "group2": group2, "group2Name": group2_name, "relevant": relevant, "op": op,
    }
    setup_js = f"window.baStart({_json(params)});"
    _embed("ba-app", setup_js, height=680, html_file="managing_money_scaffolds.html")


def render_line_graph_scaffold(x_values, y_values, relevant, op):
    """x_values/y_values: the line graph's full data (parallel lists). relevant: the point
    index/indices needed. op: 'single' (one point — that's the answer) or 'diff' (two points,
    larger - smaller)."""
    params = {"xValues": x_values, "yValues": y_values, "relevant": relevant, "op": op}
    setup_js = f"window.lgStart({_json(params)});"
    _embed("lg-app", setup_js, height=600, html_file="managing_money_scaffolds.html")


def render_pie_chart_scaffold(categories, kind, target_idx, angles=None, pcts=None):
    """kind: 'angle_to_pct' (Level 1 — pass `angles`, a list summing to 360; target_idx's angle
    is converted to a percentage via ÷360×100) or 'missing_sector' (Level 2 — pass `pcts`, a
    list of percentages summing to 100 where target_idx is the missing one; found via
    100 - sum of the others)."""
    params = {"categories": categories, "kind": kind, "targetIdx": target_idx, "angles": angles, "pcts": pcts}
    setup_js = f"window.paStart({_json(params)});"
    _embed("pa-app", setup_js, height=640, html_file="managing_money_scaffolds.html")


def render_tally_scaffold(categories, data):
    """categories: the frequency table's row labels. data: the raw, unsorted list of every
    item surveyed, exactly as the question presents it — the tool works through it one item at
    a time, adding a tally mark to the matching row as it goes."""
    setup_js = f"window.tyStart({_json({'categories': categories, 'data': data})});"
    _embed("ty-app", setup_js, height=680, html_file="managing_money_scaffolds.html")


# ---------------------------------------------------------------------------
# Shape, Space & Measures widgets — assets/shape_space_and_measures_scaffolds.html. The four
# simple-numeric ones (time_intervals, volume_cuboids, area_triangles, area_rectangles,
# area_composite) fill individual DOM inputs like the ported tools; timetables and directions
# have variable-length list/dict data (a whole timetable, a whole street list) so, like the
# Managing Money widgets above, they're started via a `window.<prefix>Start(params)` JS entry
# point instead of simulating field-by-field DOM edits.
# ---------------------------------------------------------------------------


def render_time_intervals_scaffold(direction, start=None, end=None, target=None, duration=None, use24=True):
    """direction: 'elapsed' (start & end both known, find the gap — Level 1/2), 'forward'
    (start + duration known, find the end time — Level 3 forwards) or 'backward' (target +
    duration known, find the leave-by time — Level 3 backwards). start/end/target are minutes
    since midnight; duration is minutes. use24 controls whether times are shown as 24-hour or
    12-hour am/pm on the number line (matches whichever fmt24/fmt12 the question itself used)."""
    setup_js = (
        _click_matching("ti-modePills", "mode", "custom")
        + _click_matching("ti-directionPills", "direction", direction)
        + _click_matching("ti-formatPills", "fmt", "24" if use24 else "12")
        + _set_value("ti-startInput", start if start is not None else 0)
        + _set_value("ti-endInput", end if end is not None else 0)
        + _set_value("ti-targetInput", target if target is not None else 0)
        + _set_value("ti-durationInput", duration if duration is not None else 0)
        + "document.getElementById('ti-startBtn').click();"
    )
    _embed("ti-app", setup_js, height=620, html_file="shape_space_and_measures_scaffolds.html")


def render_timetables_scaffold(title, stops, services, times_str, times_min, focus,
                                 svc_idx=None, end_idx=None, dest_idx=None, start_idx=None,
                                 deadline_str=None, deadline_min=None):
    """focus: 'journey' (Level 1 — svc_idx/end_idx name the service/stop for the
    departure->arrival->journey-time reveal) or 'deadline' (Level 2 — dest_idx/deadline_str/
    deadline_min drive the service-by-service check against the deadline). times_str/times_min
    are [service_idx][stop_idx] 2D lists, mirroring topics/shape_space_and_measures/
    timetables.py's own `tt["times_str"]`/`tt["times"]` exactly."""
    params = {
        "title": title, "stops": stops, "services": services,
        "times_str": times_str, "times_min": times_min, "focus": focus,
        "svc_idx": svc_idx, "end_idx": end_idx, "dest_idx": dest_idx, "start_idx": start_idx,
        "deadline_str": deadline_str, "deadline_min": deadline_min,
    }
    setup_js = f"window.ttStart({_json(params)});"
    _embed("tt-app", setup_js, height=760, html_file="shape_space_and_measures_scaffolds.html")


def render_volume_cuboids_scaffold(length, width, height):
    setup_js = (
        _click_matching("vc-modePills", "mode", "custom")
        + _set_value("vc-lengthInput", length)
        + _set_value("vc-widthInput", width)
        + _set_value("vc-heightInput", height)
        + "document.getElementById('vc-startBtn').click();"
    )
    _embed("vc-app", setup_js, height=640, html_file="shape_space_and_measures_scaffolds.html")


def render_area_triangles_scaffold(base, height):
    """Only base/height are mirrored — the widget picks its own apex position for the
    diagram, it doesn't need to match the question's own (random) apex_frac exactly."""
    setup_js = (
        _click_matching("at-modePills", "mode", "custom")
        + _set_value("at-baseInput", base)
        + _set_value("at-heightInput", height)
        + "document.getElementById('at-startBtn').click();"
    )
    _embed("at-app", setup_js, height=600, html_file="shape_space_and_measures_scaffolds.html")


def render_area_rectangles_scaffold(width, height):
    setup_js = (
        _click_matching("ar-modePills", "mode", "custom")
        + _set_value("ar-widthInput", width)
        + _set_value("ar-heightInput", height)
        + "document.getElementById('ar-startBtn').click();"
    )
    _embed("ar-app", setup_js, height=560, html_file="shape_space_and_measures_scaffolds.html")


def render_area_composite_scaffold(width, height, notch_width, notch_height):
    """Same W, H, a, b parameter shape as render_l_shape_perimeter_scaffold (mirrors
    topics/shape_space_and_measures/_helpers.make_l_shape() exactly) — but this tool splits
    the L-shape into two rectangles and adds their areas, rather than finding the perimeter."""
    setup_js = (
        _click_matching("ac-modePills", "mode", "custom")
        + _set_value("ac-widthInput", width)
        + _set_value("ac-heightInput", height)
        + _set_value("ac-notchWInput", notch_width)
        + _set_value("ac-notchHInput", notch_height)
        + "document.getElementById('ac-startBtn').click();"
    )
    _embed("ac-app", setup_js, height=700, html_file="shape_space_and_measures_scaffolds.html")


def render_directions_scaffold(streets, query_type, side=None, n=None, reveal=None,
                                 target_landmark=None, sub_side=None):
    """streets: the full street list exactly as topics/shape_space_and_measures/
    directions.py's `_build_map()` builds it (list of {"x","dir","name","landmark","length",
    "has_ext",...} dicts). query_type: 'landmark' (walk until the matching landmark is
    reached, name its road — to_landmark), 'nth' (walk to the side'th/n'th turning on `side`,
    reveal its name or landmark per `reveal` — nth_name/nth_destination) or 'ext' (walk to that
    same nth turning, then walk to its end and reveal the landmark on `sub_side` — Level 2)."""
    params = {
        "streets": streets, "query_type": query_type, "side": side, "n": n,
        "reveal": reveal, "target_landmark": target_landmark, "sub_side": sub_side,
    }
    setup_js = f"window.dirStart({_json(params)});"
    _embed("dir-app", setup_js, height=760, html_file="shape_space_and_measures_scaffolds.html")


# ---------------------------------------------------------------------------
# Bar model — assets/bar_model_scaffolds.html. Not in WIDGET_REGISTRY: it's driven by
# its own metadata["bar_model"] key (built with core/models/bar_model.py) and shown in its own
# expander by core/ui/scaffold_ui.py's render_bar_model(), so it can sit alongside a question's
# existing scaffold_widget rather than replacing it.
# ---------------------------------------------------------------------------


def render_bar_model_diagram(spec):
    """spec: a core.models.bar_model.bar_model(...) dict. The tool steps through each stage:
    fill in the known values on the bars, choose the operation, then calculate the '?'."""
    setup_js = f"window.sbmStart({_json(spec)});"
    _embed("sbm-app", setup_js, height=640, html_file="bar_model_scaffolds.html")


# ---------------------------------------------------------------------------
# Registry — dispatched by core/ui/scaffold_ui.py's render_simulation(). Keys are whatever a
# topic module puts in metadata["scaffold_widget"]; values are called with
# **metadata["scaffold_widget_params"]. New widgets (own file per unit, see module docstring)
# register here too — just add a new key, no other file needs editing to wire one in.
# ---------------------------------------------------------------------------

WIDGET_REGISTRY = {
    "rounding": render_rounding_scaffold,
    "l_shape_perimeter": render_l_shape_perimeter_scaffold,
    "time_conversion": render_time_conversion_scaffold,
    "bus_stop_division": render_bus_stop_division_scaffold,
    "decimal_column": render_decimal_column_scaffold,
    "lattice_multiplication": render_lattice_multiplication_scaffold,
    "decimal_mul_div": render_decimal_mul_div_scaffold,
    "workings_pad": render_workings_pad_scaffold,
    "fraction_bar": render_fraction_bar_scaffold,
    "number_problem_solving": render_number_problem_solving_scaffold,
    "percentage_stepper": render_percentage_stepper_scaffold,
    "probability_fraction": render_probability_fraction_scaffold,
    "scale_stepper": render_scale_stepper_scaffold,
    "unit_conversion": render_unit_conversion_scaffold,
    "wages_and_deductions": render_wages_scaffold,
    "receipt_adder": render_receipt_scaffold,
    "bar_model_splitter": render_bar_model_scaffold,
    "percentage_method_picker": render_percentage_method_scaffold,
    "percentage_calculator_steps": render_percentage_calculator_scaffold,
    "increase_decrease_number_line": render_percentage_increase_decrease_scaffold,
    "symbol_counter": render_pictograph_scaffold,
    "bar_reader": render_bar_graph_scaffold,
    "line_graph_reader": render_line_graph_scaffold,
    "pie_angle_calculator": render_pie_chart_scaffold,
    "tally_marker": render_tally_scaffold,
    "time_intervals": render_time_intervals_scaffold,
    "timetables": render_timetables_scaffold,
    "volume_cuboids": render_volume_cuboids_scaffold,
    "area_triangles": render_area_triangles_scaffold,
    "area_rectangles": render_area_rectangles_scaffold,
    "area_composite": render_area_composite_scaffold,
    "directions": render_directions_scaffold,
}
