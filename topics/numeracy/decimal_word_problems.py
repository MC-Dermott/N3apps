import random

from core.models.question_model import Question

NOTES = """
**Decimal Word Problems:**

- **Total:** add the decimal amounts together.
- **Difference / how much is left:** subtract the smaller from the larger.
- **Sharing equally:** total ÷ number of shares.
- **Repeated amounts (e.g. "6 spoonfuls of..."):** amount per share × number of shares.
- Always check your answer has the right **units** (cm, kg, litres, ml, ...) attached.

**Example:** Six spoonfuls of medicine, each 5·1 ml, are removed from a bottle of 50 ml.
- Removed = 6 × 5·1 = 30·6 ml
- Left = 50 − 30·6 = **19·4 ml**
"""


def _fmt(x, dp=2):
    return f"{x:.{dp}f}"


def _decimal(lo, hi, dp=2):
    scale = 10 ** dp
    return random.randint(int(round(lo * scale)), int(round(hi * scale))) / scale


_LENGTH_ITEMS = [
    {"noun": "plank of wood", "unit": "cm"},
    {"noun": "piece of ribbon", "unit": "cm"},
    {"noun": "garden hose", "unit": "m"},
    {"noun": "shelf", "unit": "cm"},
]
_WEIGHT_ITEMS = [
    {"noun": "sack of potatoes", "unit": "kg"},
    {"noun": "bag of flour", "unit": "kg"},
    {"noun": "delivery box", "unit": "kg"},
]
_VOLUME_ITEMS = [
    {"noun": "bottle of milk", "unit": "litres"},
    {"noun": "can of paint", "unit": "litres"},
    {"noun": "container of juice", "unit": "ml"},
]


def _random_item():
    return random.choice(_LENGTH_ITEMS + _WEIGHT_ITEMS + _VOLUME_ITEMS)


# ---------------------------------------------------------------------------
# Level 1 — total or difference
# ---------------------------------------------------------------------------

def generate_decimal_word_problems_l1():
    item = _random_item()
    dp = random.choice([1, 2])
    focus = random.choice(["total", "difference"])

    if focus == "total":
        a = _decimal(2, 40, dp)
        b = _decimal(2, 40, dp)
        answer = round(a + b, dp)
        question_text = (
            f"A {item['noun']} is made up of two pieces, {_fmt(a, dp)} {item['unit']} and "
            f"{_fmt(b, dp)} {item['unit']}.\n\n"
            f"What is the total?"
        )
        worked = [f"Total = {_fmt(a, dp)} + {_fmt(b, dp)} = {_fmt(answer, dp)} {item['unit']}"]
        widget_kind, widget_params = "total", {"a": _fmt(a, dp), "b": _fmt(b, dp)}
    else:
        start = _decimal(20, 90, dp)
        removed = _decimal(2, start - 5, dp)
        answer = round(start - removed, dp)
        question_text = (
            f"A {item['noun']} starts at {_fmt(start, dp)} {item['unit']}.\n\n"
            f"{_fmt(removed, dp)} {item['unit']} is taken away.\n\n"
            f"How much is left?"
        )
        worked = [f"Left = {_fmt(start, dp)} − {_fmt(removed, dp)} = {_fmt(answer, dp)} {item['unit']}"]
        widget_kind, widget_params = "difference", {"start": _fmt(start, dp), "removed": _fmt(removed, dp)}

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Decimal Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "workings_pad",
            "scaffold_widget_params": {"kind": widget_kind, "unit": item["unit"], **widget_params},
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — sharing equally, or a repeated (multiplied) amount
# ---------------------------------------------------------------------------

def _sharing_question():
    item = _random_item()
    dp = random.choice([1, 2])
    n_shares = random.randint(2, 8)
    share = _decimal(1, 20, dp)
    total = round(share * n_shares, dp)

    question_text = (
        f"A {item['noun']} measuring {_fmt(total, dp)} {item['unit']} is shared equally "
        f"among {n_shares} people.\n\n"
        f"How much does each person get?"
    )
    worked = [f"Each share = {_fmt(total, dp)} ÷ {n_shares} = {_fmt(share, dp)} {item['unit']}"]

    return Question(
        question_text=question_text,
        correct_answer=share,
        topic="Numeracy",
        question_type="Decimal Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "workings_pad",
            "scaffold_widget_params": {
                "kind": "sharing", "unit": item["unit"], "total": _fmt(total, dp), "n": n_shares,
            },
        },
    )


def _multiply_then_subtract_question():
    n = random.randint(3, 8)
    dp = 1
    per_unit = _decimal(1, 8, dp)
    removed = round(per_unit * n, dp)
    start = round(removed + _decimal(5, 30, dp), dp)
    answer = round(start - removed, dp)
    item = random.choice(_VOLUME_ITEMS)

    question_text = (
        f"{n} spoonfuls of medicine, each holding {_fmt(per_unit, dp)} {item['unit']}, "
        f"are removed from a {item['noun']} containing {_fmt(start, dp)} {item['unit']}.\n\n"
        f"How much is left in the {item['noun'].split()[-1]}?"
    )
    scaffold_steps = [
        {"prompt": f"Find the total amount removed ({n} × {_fmt(per_unit, dp)})", "answer": removed},
    ]
    worked = [
        f"Removed = {n} × {_fmt(per_unit, dp)} = {_fmt(removed, dp)} {item['unit']}",
        f"Left = {_fmt(start, dp)} − {_fmt(removed, dp)} = {_fmt(answer, dp)} {item['unit']}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Decimal Word Problems",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "workings_pad",
            "scaffold_widget_params": {
                "kind": "multiply_subtract", "unit": item["unit"],
                "n": n, "per_unit": _fmt(per_unit, dp), "start": _fmt(start, dp),
            },
        },
    )


def generate_decimal_word_problems_l2():
    return random.choice([
        _sharing_question,
        _multiply_then_subtract_question,
    ])()


def generate_decimal_word_problems_question():
    return random.choice([
        generate_decimal_word_problems_l1,
        generate_decimal_word_problems_l2,
    ])()
