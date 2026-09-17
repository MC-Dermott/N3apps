import random

from core.models.question_model import Question

NOTES = """
**Adding and Subtracting Decimals:**

- Line up the **decimal points** underneath each other before you add or subtract.
- Fill in any empty spaces with a zero so both numbers have the same number of decimal places.
- Add/subtract as normal, then bring the decimal point straight down into the answer.

**Example:** 4·31 + 4·58
- 4·31
- + 4·58
- = **8·89**

**Example:** 27·58 − 13·27
- 27·58
- − 13·27
- = **14·31**
"""

_LENGTH_UNITS = ["cm", "m"]
_WEIGHT_UNITS = ["kg", "g"]


def _fmt(x, dp=2):
    return f"{x:.{dp}f}"


def _decimal(lo, hi, dp=2):
    scale = 10 ** dp
    return random.randint(int(round(lo * scale)), int(round(hi * scale))) / scale


# ---------------------------------------------------------------------------
# Level 1 — column-style addition/subtraction of two decimals
# ---------------------------------------------------------------------------

def generate_decimal_addition_subtraction_l1():
    dp = random.choice([1, 2])
    op = random.choice(["+", "-"])

    a = _decimal(1, 90, dp)
    b = _decimal(1, 90, dp)
    if op == "-" and a < b:
        a, b = b, a

    answer = round(a + b, dp) if op == "+" else round(a - b, dp)

    question_text = (
        f"Work out:\n\n"
        f"{_fmt(a, dp)} {op} {_fmt(b, dp)}"
    )
    op_word = "add" if op == "+" else "subtract"
    worked = [
        f"Line up the decimal points, then {op_word}:",
        f"{_fmt(a, dp)} {op} {_fmt(b, dp)} = {_fmt(answer, dp)}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Decimal Addition and Subtraction",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "decimal_column",
            "scaffold_widget_params": {"a": _fmt(a, dp), "b": _fmt(b, dp), "op": op},
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — word-style problems, sometimes with more than two decimals
# ---------------------------------------------------------------------------

def _addition_word_question():
    context = random.choice([
        {"item": "table", "plural": "tables", "unit": "cm",
         "verb": "placed together to form a longer bench"},
        {"item": "plank", "plural": "planks", "unit": "cm",
         "verb": "joined end to end"},
        {"item": "box", "plural": "boxes", "unit": "kg",
         "verb": "stacked on a delivery pallet"},
    ])
    n = random.choice([2, 2, 3])
    dp = random.choice([1, 2])
    values = [_decimal(2, 90, dp) for _ in range(n)]
    total = round(sum(values), dp)

    if n == 2:
        question_text = (
            f"Two {context['plural']} are {context['verb']}.\n\n"
            f"The first {context['item']} is {_fmt(values[0], dp)} {context['unit']} and the "
            f"second is {_fmt(values[1], dp)} {context['unit']}.\n\n"
            f"What is the total?"
        )
    else:
        parts = ", ".join(f"{_fmt(v, dp)} {context['unit']}" for v in values[:-1])
        question_text = (
            f"Three {context['plural']} weigh {parts} and {_fmt(values[-1], dp)} "
            f"{context['unit']}.\n\n" if context['unit'] == "kg" else
            f"Three {context['plural']} measure {parts} and {_fmt(values[-1], dp)} "
            f"{context['unit']}.\n\n"
        ) + "What is the total?"

    worked = [" + ".join(_fmt(v, dp) for v in values) + f" = {_fmt(total, dp)} {context['unit']}"]
    scaffold_steps = []
    metadata = {}
    if n == 3:
        scaffold_steps = [
            {"prompt": f"Add the first two values ({_fmt(values[0], dp)} + {_fmt(values[1], dp)})",
             "answer": round(values[0] + values[1], dp)},
        ]
    else:
        metadata = {
            "scaffold_widget": "decimal_column",
            "scaffold_widget_params": {"a": _fmt(values[0], dp), "b": _fmt(values[1], dp), "op": "+"},
        }

    return Question(
        question_text=question_text,
        correct_answer=total,
        topic="Numeracy",
        question_type="Decimal Addition and Subtraction",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=metadata,
    )


def _subtraction_word_question():
    context = random.choice([
        {"noun": "piece of ribbon", "unit": "cm", "verb": "cut off"},
        {"noun": "length of wood", "unit": "cm", "verb": "cut off"},
        {"noun": "bottle of juice", "unit": "litres", "verb": "poured out"},
        {"noun": "bag of flour", "unit": "kg", "verb": "used"},
    ])
    dp = random.choice([1, 2])
    start = _decimal(20, 150, dp)
    removed = _decimal(2, start - 5, dp)
    remaining = round(start - removed, dp)

    question_text = (
        f"A {context['noun']} is {_fmt(start, dp)} {context['unit']} long to start with.\n\n"
        if context['unit'] in ("cm",) else
        f"A {context['noun']} holds {_fmt(start, dp)} {context['unit']} to start with.\n\n"
    ) + (
        f"If {_fmt(removed, dp)} {context['unit']} is {context['verb']}, how much remains?"
    )
    worked = [f"Remaining = {_fmt(start, dp)} − {_fmt(removed, dp)} = {_fmt(remaining, dp)} {context['unit']}"]

    return Question(
        question_text=question_text,
        correct_answer=remaining,
        topic="Numeracy",
        question_type="Decimal Addition and Subtraction",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "decimal_column",
            "scaffold_widget_params": {"a": _fmt(start, dp), "b": _fmt(removed, dp), "op": "-"},
        },
    )


def generate_decimal_addition_subtraction_l2():
    return random.choice([
        _addition_word_question,
        _subtraction_word_question,
    ])()


def generate_decimal_addition_subtraction_question():
    return random.choice([
        generate_decimal_addition_subtraction_l1,
        generate_decimal_addition_subtraction_l2,
    ])()
