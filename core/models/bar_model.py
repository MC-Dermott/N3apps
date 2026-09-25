"""Builders for bar model specs — the data a topic module puts in
`metadata["bar_model"]`, rendered by core/ui/scaffold_ui.py's render_bar_model() in its own
"📊 Bar model" expander (separate from metadata["scaffold_widget"], so a question can
keep its existing calculation tool and gain a bar model alongside it).

A spec is a list of stages, each one bar model with exactly one unknown ('?'). For every
stage the pupil (1) fills in the values they know from the question, (2) chooses the operation
the model points to, then (3) works out the unknown. A later stage can reuse an earlier
answer by marking it `carried(...)` — it's shown pre-filled rather than asked for again.

Stage kinds (see assets/bar_model_scaffolds.html for the drawing of each):
- part_whole:  one bar split into parts, with a brace for the whole (addition / subtraction)
- compare:     two bars side by side; the dashed gap is the difference
- equal_parts: one bar split into equal boxes (sharing, grouping, repeated amounts)
- fraction:    d equal boxes with k shaded (fractions, and the common non-calculator percentages)
- percent:     a 100% bar with pct% shaded, found via 1% (any percentage)
"""


def given(label, value):
    return {"label": label, "value": value, "state": "given"}


def unknown(label, value):
    """`value` is the correct answer — used to check the pupil's working and draw to scale."""
    return {"label": label, "value": value, "state": "unknown"}


def carried(label, value):
    return {"label": label, "value": value, "state": "carried"}


def _plain(item):
    """Mark an item as a plain count (no £/unit attached when displayed)."""
    return {**item, "plain": True}


def part_whole(heading, whole, parts):
    return {"kind": "part_whole", "heading": heading, "whole": whole, "parts": parts}


def compare(heading, larger, smaller, difference):
    return {"kind": "compare", "heading": heading, "larger": larger, "smaller": smaller,
            "difference": difference}


def equal_parts(heading, whole, part, count, round_up=False):
    """count: a given/unknown/carried item for the number of equal boxes, whose label reads
    after the number (e.g. given("people", 4) shows as "4 people"). Set round_up when the
    count is unknown and a part-filled box still counts (boxes needed, weeks of saving)."""
    return {"kind": "equal_parts", "heading": heading, "whole": whole, "part": part,
            "count": _plain(count), "round_up": round_up}


def fraction(heading, whole, d, k, seg_label, target):
    """whole split into d equal boxes, the first k shaded; seg_label names one box (e.g.
    '1/4' or '25%'); target is the unknown shaded amount."""
    return {"kind": "fraction", "heading": heading, "whole": whole, "d": d, "k": k,
            "seg_label": seg_label, "target": target}


def percent(heading, whole, pct, target):
    return {"kind": "percent", "heading": heading, "whole": whole, "pct": pct, "target": target}


# Common non-calculator percentages as (boxes, shaded) — 20% is 1 of 5 boxes, 75% is 3 of 4...
COMMON_PERCENT_FRACTIONS = {
    "10": (10, 1), "20": (5, 1), "25": (4, 1), "50": (2, 1), "75": (4, 3),
    "33⅓": (3, 1), "66⅔": (3, 2),
}


def common_percent(heading, whole, pct_str, target):
    d, k = COMMON_PERCENT_FRACTIONS[pct_str]
    seg_pct = {"33⅓": "33⅓", "66⅔": "33⅓"}.get(pct_str, str(100 // d))
    return fraction(heading, whole, d, k, f"{seg_pct}%", target)


def with_units(stage, prefix="", suffix="", dp=None):
    """Override the whole spec's units for one stage."""
    return {**stage, "prefix": prefix, "suffix": suffix, "dp": dp}


def bar_model(stages, prefix="", suffix="", dp=None, question=""):
    """prefix/suffix: the unit shown on every non-count value, e.g. prefix='£' or
    suffix=' kg'. dp: fixed decimal places for display (None = as needed). question: optional
    short restatement shown above the model."""
    return {"stages": stages, "prefix": prefix, "suffix": suffix, "dp": dp, "question": question}


def unit_affixes(unit):
    """Map a percentages topic's unit string ('' = money, 'kg', 'p', 'pupils'...) to
    (prefix, suffix), matching how those topics write amounts ('48kg' but '48 pupils')."""
    if unit == "":
        return "£", ""
    if unit in ("pupils", "marbles"):
        return "", f" {unit}"
    return "", unit
