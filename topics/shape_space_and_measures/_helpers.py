"""Shared, non-public helpers for the Shape, Space & Measures unit's topic modules.

Not part of the module contract described in README.md (no `generate_*` functions here) —
just time/number formatting and simple rectilinear-shape geometry reused by several of the
nine topic modules (clock_conversion, time_intervals and timetables all need the same time
formatting; perimeter and area_composite both build and label the same kind of L-shaped
polygon). Kept private (leading underscore, not imported by question_factory.py).
"""

import random

# ---------------------------------------------------------------------------
# Number formatting — always explicit, never f"{x:g}" (which silently produces
# 1e+07-style output on some values).
# ---------------------------------------------------------------------------

def fmt_num(x, dp=2):
    """Whole numbers print with no decimal point; anything else prints with up to `dp`
    decimal places and no trailing zeros (3.50 -> "3.5", 3.0 -> "3")."""
    x = round(x, dp)
    if float(x).is_integer():
        return str(int(round(x)))
    s = f"{x:.{dp}f}".rstrip("0").rstrip(".")
    return s


def ordinal(n):
    if 11 <= n % 100 <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


# ---------------------------------------------------------------------------
# Time helpers — internal representation is minutes since midnight (0-1439).
# ---------------------------------------------------------------------------

def fmt24(t):
    t = t % 1440
    h, m = divmod(t, 60)
    return f"{h:02d}:{m:02d}"


def fmt12(t):
    t = t % 1440
    h, m = divmod(t, 60)
    period = "am" if h < 12 else "pm"
    h12 = h % 12
    if h12 == 0:
        h12 = 12
    return f"{h12}:{m:02d} {period}"


def random_time(on_hour=False, on_half=False, lo=0, hi=1439):
    t = random.randint(lo, hi)
    h = t // 60
    if on_hour:
        m = 0
    elif on_half:
        m = random.choice([0, 30])
    else:
        m = random.randint(0, 59)
    return h * 60 + m


# ---------------------------------------------------------------------------
# Rectilinear "L-shape" (a rectangle with one rectangular notch cut from a
# corner) — used by both perimeter.py and area_composite.py.
#
# Vertices go clockwise from the origin: (0,0) -> (W,0) -> (W,H-b) ->
# (W-a,H-b) -> (W-a,H) -> (0,H) -> back to (0,0).
#
# Its 6 successive edge lengths are [W, H-b, a, b, W-a, H]. The two
# "bounding-box" edges (index 0 = W, index 5 = H) always stay labelled;
# indices 1-4 are the ones perimeter.py/area_composite.py may hide to build
# an "infer the missing side" question, since W = a + (W-a) and
# H = b + (H-b).
# ---------------------------------------------------------------------------

def make_l_shape(w_range=(8, 20), h_range=(6, 16), notch_frac=(0.2, 0.6)):
    W = random.randint(*w_range)
    H = random.randint(*h_range)
    a = max(2, round(W * random.uniform(*notch_frac)))
    b = max(2, round(H * random.uniform(*notch_frac)))
    a = min(a, W - 2)
    b = min(b, H - 2)
    vertices = [(0, 0), (W, 0), (W, H - b), (W - a, H - b), (W - a, H), (0, H)]
    edges = [W, H - b, a, b, W - a, H]
    return {"W": W, "H": H, "a": a, "b": b, "vertices": vertices, "edges": edges}
