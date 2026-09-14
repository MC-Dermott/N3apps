import random

from core.models.question_model import Question

NOTES = """
**Fraction of an Amount:**

- **Unit fraction** (top number is 1), e.g. 1/4 of 60: divide by the bottom number.
  1/4 of 60 = 60 ÷ 4 = 15
- **Non-unit fraction**, e.g. 3/4 of 60: first find one part (divide by the bottom number),
  then multiply by the top number.
  1/4 of 60 = 15, so 3/4 of 60 = 15 × 3 = **45**

**Example:** Find 3/8 of 480.
- 1/8 of 480 = 480 ÷ 8 = 60
- 3/8 of 480 = 60 × 3 = **180**
"""

_UNIT_DENOMS = [2, 3, 4, 5, 8, 10]
_NON_UNIT_FRACTIONS = [
    (2, 3), (3, 4), (3, 5), (2, 5), (4, 5), (3, 8), (5, 8), (7, 8),
    (7, 10), (9, 10), (3, 10), (2, 3),
]


def _amount_for_denom(denom, lo_mult=2, hi_mult=40):
    return denom * random.randint(lo_mult, hi_mult)


# ---------------------------------------------------------------------------
# Level 1 — unit fraction of a quantity
# ---------------------------------------------------------------------------

def generate_fraction_of_amount_l1():
    denom = random.choice(_UNIT_DENOMS)
    amount = _amount_for_denom(denom, 2, 40)
    unit = random.choice(["", "", "", "g", "cm", "kg", "ml"])
    money = unit == "" and random.random() < 0.4

    answer = amount // denom
    amount_str = f"£{amount}" if money else f"{amount}{unit}"
    answer_str = f"£{answer}" if money else f"{answer}{unit}"

    question_text = f"Find 1/{denom} of {amount_str}."
    worked = [f"1/{denom} of {amount_str} = {amount_str} ÷ {denom} = {answer_str}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Fraction of an Amount",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 2 — non-unit fraction of a larger quantity
# ---------------------------------------------------------------------------

_UNIT_SUFFIXES = {"": "", "g": "g", "cm": "cm", "kg": "kg", "m": "m", "pupils": " pupils"}


def generate_fraction_of_amount_l2():
    num, denom = random.choice(_NON_UNIT_FRACTIONS)
    amount = _amount_for_denom(denom, 10, 90)
    unit = random.choice(["", "", "", "g", "cm", "kg", "pupils", "m"])
    money = unit == "" and random.random() < 0.4
    suffix = _UNIT_SUFFIXES[unit]

    one_part = amount // denom
    answer = one_part * num
    amount_str = f"£{amount}" if money else f"{amount}{suffix}"
    answer_str = f"£{answer}" if money else f"{answer}{suffix}"

    question_text = f"Find {num}/{denom} of {amount_str}."
    scaffold_steps = [
        {"prompt": f"Find 1/{denom} of {amount_str} first", "answer": one_part},
    ]
    worked = [
        f"1/{denom} of {amount_str} = {amount_str} ÷ {denom} = {one_part}",
        f"{num}/{denom} of {amount_str} = {one_part} × {num} = {answer_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Fraction of an Amount",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_fraction_of_amount_question():
    return random.choice([
        generate_fraction_of_amount_l1,
        generate_fraction_of_amount_l2,
    ])()
