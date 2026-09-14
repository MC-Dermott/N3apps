import random
from decimal import Decimal, ROUND_HALF_UP

from core.models.question_model import Question

NOTES = """
**Rounding:**

- Look at the digit **immediately after** the place you are rounding to.
- If it is **5 or more**, round up. If it is **4 or less**, leave the digit as it is.
- Rounding to the nearest **whole number**: look at the first decimal digit.
- Rounding to the nearest **ten / hundred / thousand**: look at the digit to the right of
  that place, then replace every digit after it with zeros.
- Rounding to **1 or 2 decimal places**: look at the digit just after the place you're keeping.

**Example:** Round 738·29 to the nearest whole number.
- The digit after the decimal point is 2 (less than 5) → round down → **738**

**Example:** Round 9·305 to 2 decimal places.
- The third decimal digit is 5 → round up → **9·31**
"""


def _fmt(x, dp=None):
    """Fixed-point formatting — never scientific notation."""
    if dp is not None:
        return f"{x:.{dp}f}"
    if float(x).is_integer():
        return str(int(x))
    return f"{x:.6f}".rstrip("0").rstrip(".")


def _round_half_up(value, dp=0):
    d = Decimal(str(value))
    if dp <= 0:
        q = Decimal(1).scaleb(-dp) if dp < 0 else Decimal(1)
        return int(d.quantize(q, rounding=ROUND_HALF_UP))
    q = Decimal(1).scaleb(-dp)
    return float(d.quantize(q, rounding=ROUND_HALF_UP))


def _round_to_place(value, place):
    d = (Decimal(str(value)) / Decimal(place)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(d) * place


def _random_decimal(int_digits, dp):
    scale = 10 ** dp
    lo = 10 ** (int_digits - 1)
    hi = 10 ** int_digits - 1
    whole = random.randint(lo, hi)
    frac = random.randint(0, scale - 1)
    return whole + frac / scale


# ---------------------------------------------------------------------------
# Level 1 — round to nearest whole number / ten / hundred / thousand
# ---------------------------------------------------------------------------

def generate_rounding_l1():
    target = random.choice(["whole number", "ten", "hundred", "thousand"])

    if target == "whole number":
        value = round(_random_decimal(random.choice([1, 2, 3]), random.choice([1, 2])), 2)
        answer = _round_half_up(value, 0)
        question_text = f"Round {_fmt(value)} to the nearest whole number."
    elif target == "ten":
        value = random.randint(11, 998)
        answer = _round_to_place(value, 10)
        question_text = f"Round {value} to the nearest ten."
    elif target == "hundred":
        value = random.randint(101, 9899)
        answer = _round_to_place(value, 100)
        question_text = f"Round {value} to the nearest hundred."
    else:
        value = random.randint(1001, 98999)
        answer = _round_to_place(value, 1000)
        question_text = f"Round {value} to the nearest thousand."

    worked = [f"{_fmt(value)} rounded to the nearest {target} = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Rounding",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 2 — round to 1 or 2 decimal places
# ---------------------------------------------------------------------------

def generate_rounding_l2():
    dp = random.choice([1, 2])
    src_dp = dp + random.choice([1, 2])
    value = round(_random_decimal(random.choice([1, 2]), src_dp), src_dp)
    answer = _round_half_up(value, dp)

    question_text = (
        f"Round {_fmt(value, src_dp)} correct to {dp} decimal place{'s' if dp > 1 else ''}."
    )
    worked = [
        f"{_fmt(value, src_dp)} rounded to {dp} d.p. = {_fmt(answer, dp)}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Rounding",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
    )


def generate_rounding_question():
    return random.choice([
        generate_rounding_l1,
        generate_rounding_l2,
    ])()
