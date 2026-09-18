import random
from decimal import Decimal

from core.models.question_model import Question

NOTES = """
**Multiplying and Dividing Decimals:**

- To multiply or divide a decimal by a **single-digit whole number**, ignore the decimal point,
  do the calculation, then put the point back in the same relative position.
- To multiply by **10 / 100 / 1000**, move the decimal point **right** 1 / 2 / 3 places.
- To divide by **10 / 100 / 1000**, move the decimal point **left** 1 / 2 / 3 places.

**Example:** 16·3 × 6 = **97·8**

**Example:** 4·3 × 100 — move the point 2 places right → **430**

**Example:** 57·5 ÷ 100 — move the point 2 places left → **0·575**
"""


def _fmt(x):
    if float(x).is_integer():
        return str(int(x))
    s = f"{x:.6f}".rstrip("0").rstrip(".")
    return s


def _decimal(lo, hi, dp=2):
    scale = 10 ** dp
    return random.randint(int(round(lo * scale)), int(round(hi * scale))) / scale


def _mul(a, b, dp_out):
    return round(float(Decimal(str(a)) * Decimal(str(b))), dp_out)


def _div(a, b, dp_out):
    return round(float(Decimal(str(a)) / Decimal(str(b))), dp_out)


# ---------------------------------------------------------------------------
# Level 1 — multiply/divide a decimal by a single-digit whole number
# ---------------------------------------------------------------------------

def generate_decimal_multiplication_division_l1():
    op = random.choice(["multiply", "divide"])
    dp = random.choice([1, 2])
    n = random.randint(2, 9)

    if op == "multiply":
        value = _decimal(1, 40, dp)
        answer = _mul(value, n, dp)
        question_text = f"Work out {_fmt(value)} × {n}"
        worked = [f"{_fmt(value)} × {n} = {_fmt(answer)}"]
        metadata = {
            "scaffold_widget": "decimal_mul_div",
            "scaffold_widget_params": {
                "value": _fmt(value), "operation": op, "kind": "single_digit", "n": n,
            },
        }
    else:
        # build the division so it comes out exact and clean
        answer = _decimal(1, 40, dp)
        value = _mul(answer, n, dp)
        question_text = f"Work out {_fmt(value)} ÷ {n}"
        worked = [f"{_fmt(value)} ÷ {n} = {_fmt(answer)}"]
        # The "ignore the point" method reduces this to a whole-number division — hand that
        # straight to the bus stop division scaffold (maths-scaffolds.html) rather than a bare
        # answer box, so the actual division is worked through column by column.
        whole_in = int(_fmt(value).replace(".", ""))
        metadata = {
            "scaffold_widget": "bus_stop_division",
            "scaffold_widget_params": {"dividend": whole_in, "divisor": n},
        }

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Decimal Multiplication and Division",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Level 2 — multiply/divide a decimal by 10 / 100 / 1000
# ---------------------------------------------------------------------------

def generate_decimal_multiplication_division_l2():
    op = random.choice(["multiply", "divide"])
    power = random.choice([10, 100, 1000])
    dp = random.choice([1, 2])
    value = _decimal(1, 90, dp)

    if op == "multiply":
        answer = _mul(value, power, 4)
        answer = answer if not float(answer).is_integer() else int(answer)
        question_text = f"Work out {_fmt(value)} × {power}"
        places = {10: 1, 100: 2, 1000: 3}[power]
        worked = [
            f"Multiplying by {power} moves the decimal point {places} place"
            f"{'s' if places > 1 else ''} to the right.",
            f"{_fmt(value)} × {power} = {_fmt(answer)}",
        ]
    else:
        answer = _div(value, power, 6)
        question_text = f"Work out {_fmt(value)} ÷ {power}"
        places = {10: 1, 100: 2, 1000: 3}[power]
        worked = [
            f"Dividing by {power} moves the decimal point {places} place"
            f"{'s' if places > 1 else ''} to the left.",
            f"{_fmt(value)} ÷ {power} = {_fmt(answer)}",
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Decimal Multiplication and Division",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "decimal_mul_div",
            "scaffold_widget_params": {
                "value": _fmt(value), "operation": op, "kind": "shift", "n": power,
            },
        },
    )


def generate_decimal_multiplication_division_question():
    return random.choice([
        generate_decimal_multiplication_division_l1,
        generate_decimal_multiplication_division_l2,
    ])()
