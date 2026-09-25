import random
from core.models import bar_model as bm
from core.models.question_model import Question

NOTES = """
**Non-Calculator Percentages — Common Percentages:**

- 50% = half → ÷ 2
- 25% = quarter → ÷ 4
- 75% = three quarters → ÷ 4, then × 3
- 10% → ÷ 10
- 20% → ÷ 10, then × 2
- 33⅓% = one third → ÷ 3
- 66⅔% = two thirds → ÷ 3, then × 2

**Example:** Find 75% of £48.
- 25% of £48 = £48 ÷ 4 = £12
- 75% of £48 = £12 × 3 = **£36**
"""

_PERCENTAGES = [
    (50, 2, "half", "÷ 2"),
    (25, 4, "quarter", "÷ 4"),
    (10, 10, "one tenth", "÷ 10"),
    (20, 5, "one fifth", "÷ 10, then × 2"),
    (75, 4, "three quarters", "÷ 4, then × 3"),
]
_THIRDS = [
    (33.333333, 3, "one third", "÷ 3"),
    (66.666667, 3, "two thirds", "÷ 3, then × 2"),
]

_UNITS = ["", "", "", "g", "cm", "kg", "ml", "p"]


def _clean_amount_for(percentage_label):
    """Pick an amount that divides cleanly for the given common percentage."""
    if percentage_label == 10:
        return random.choice(range(10, 2001, 10))
    if percentage_label == 20:
        return random.choice(range(10, 2001, 10))
    if percentage_label == 25:
        return random.choice(range(4, 2001, 4))
    if percentage_label == 50:
        return random.choice(range(2, 2001, 2))
    if percentage_label == 75:
        return random.choice(range(4, 2001, 4))
    if percentage_label in (33, "33"):
        return random.choice(range(3, 2001, 3))
    if percentage_label in (66, "66"):
        return random.choice(range(3, 2001, 3))
    return random.choice(range(10, 2001, 10))


# ---------------------------------------------------------------------------
# Level 1 — direct "find X% of Y" using common percentages
# ---------------------------------------------------------------------------

def generate_percentages_non_calculator_l1():
    use_third = random.random() < 0.3
    unit = random.choice(_UNITS)
    money = unit == ""

    if use_third:
        pct_display, divisor, word, method = random.choice(_THIRDS)
        amount = _clean_amount_for(33 if divisor == 3 and pct_display < 50 else 66)
        pct_str = "33⅓" if pct_display < 50 else "66⅔"
        one_share = amount // 3
        answer = one_share if pct_display < 50 else one_share * 2
    else:
        pct, divisor, word, method = random.choice(_PERCENTAGES)
        amount = _clean_amount_for(pct)
        pct_str = str(pct)
        if pct == 10:
            answer = amount // 10
        elif pct == 20:
            answer = (amount // 10) * 2
        elif pct == 25:
            answer = amount // 4
        elif pct == 50:
            answer = amount // 2
        else:  # 75
            answer = (amount // 4) * 3

    amount_str = f"£{amount}" if money else f"{amount}{unit}"
    answer_str = f"£{answer}" if money else f"{answer}{unit}"

    question_text = f"Work out {pct_str}% of {amount_str} (no calculator)."

    worked = [
        f"{pct_str}% of {amount_str} is found using: {method}",
        f"{pct_str}% of {amount_str} = {answer_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Percentages (Non-Calculator)",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "percentage_method_picker",
            "scaffold_widget_params": {"pct_label": pct_str, "amount": amount},
            "bar_model": bm.bar_model([
                bm.common_percent(f"Find {pct_str}%", bm.given("Whole amount (100%)", amount), pct_str,
                                  bm.unknown(f"{pct_str}%", answer)),
            ], *bm.unit_affixes(unit)),
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — simple word problems
# ---------------------------------------------------------------------------

_L2_CONTEXTS = [
    {"subject": "A turtle laid {n} eggs.", "group": "were eaten by birds", "noun": "eggs"},
    {"subject": "There are {n} pupils in a school.", "group": "are left-handed", "noun": "pupils"},
    {"subject": "A car boot sale sold {n} items.", "group": "were CDs", "noun": "items"},
    {"subject": "There are {n} days in a year.", "group": "were sunny in Stornoway", "noun": "days"},
    {"subject": "A ferry carried {n} passengers.", "group": "were foot passengers", "noun": "passengers"},
    {"subject": "A shop sold {n} umbrellas last month.", "group": "were returned as faulty", "noun": "umbrellas"},
]


def generate_percentages_non_calculator_l2():
    ctx = random.choice(_L2_CONTEXTS)
    pct, divisor, word, method = random.choice(_PERCENTAGES)
    n = _clean_amount_for(pct)
    if pct == 10:
        answer = n // 10
    elif pct == 20:
        answer = (n // 10) * 2
    elif pct == 25:
        answer = n // 4
    elif pct == 50:
        answer = n // 2
    else:
        answer = (n // 4) * 3

    subject = ctx["subject"].format(n=n)
    question_text = (
        f"{subject} {pct}% of the {ctx['noun']} {ctx['group']}.\n\n"
        f"How many {ctx['noun']} {ctx['group']}?"
    )
    worked = [
        f"{pct}% of {n} is found using: {method}",
        f"{pct}% of {n} = {answer}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Percentages (Non-Calculator)",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "percentage_method_picker",
            "scaffold_widget_params": {"pct_label": str(pct), "amount": n},
            "bar_model": bm.bar_model([
                bm.common_percent(f"Find {pct}%", bm.given(f"All {ctx['noun']} (100%)", n), str(pct),
                                  bm.unknown(f"{pct}%", answer)),
            ], suffix=f" {ctx['noun']}"),
        },
    )


def generate_percentages_non_calculator_question():
    return random.choice([
        generate_percentages_non_calculator_l1,
        generate_percentages_non_calculator_l2,
    ])()
