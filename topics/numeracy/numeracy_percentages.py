import random

from core.models.question_model import Question

NOTES = """
**Percentages:**

- **Common percentages (no calculator):**
  - 50% = half → ÷ 2
  - 25% = quarter → ÷ 4
  - 75% = three quarters → ÷ 4, then × 3
  - 10% → ÷ 10
  - 20% → ÷ 10, then × 2
  - 33⅓% = one third → ÷ 3
  - 66⅔% = two thirds → ÷ 3, then × 2
- **Any percentage (calculator):** percentage ÷ 100 × amount.
- **VAT** (Value Added Tax) is a tax added to the price of goods. The current rate is **20%**.
  VAT amount = 20% of the price. Total to pay = price + VAT.

**Example:** VAT on a £689 item.
- VAT = 20% of £689 = 689 ÷ 100 × 20 = **£137.80**
"""

_COMMON_PCTS = [
    (50, "÷ 2"), (25, "÷ 4"), (10, "÷ 10"), (20, "÷ 10, then × 2"), (75, "÷ 4, then × 3"),
]
_THIRDS = [(33, "÷ 3", "1"), (66, "÷ 3, then × 2", "2")]

_QUANTITY_UNITS = ["", "", "kg", "cm", "g", "ml", "pupils", "marbles"]


def _clean_amount_for(pct):
    if pct == 10 or pct == 20:
        return random.choice(range(10, 1001, 10))
    if pct in (25, 75):
        return random.choice(range(4, 1001, 4))
    if pct == 50:
        return random.choice(range(2, 1001, 2))
    if pct in (33, 66):
        return random.choice(range(3, 1002, 3))
    return random.choice(range(10, 1001, 10))


def _common_pct_answer(pct, amount):
    if pct == 10:
        return amount // 10
    if pct == 20:
        return (amount // 10) * 2
    if pct == 25:
        return amount // 4
    if pct == 50:
        return amount // 2
    if pct == 75:
        return (amount // 4) * 3
    if pct == 33:
        return amount // 3
    return (amount // 3) * 2  # 66


def _fmt_unit(amount, unit):
    return f"{amount} {unit}" if unit in ("pupils", "marbles") else f"{amount}{unit}"


# ---------------------------------------------------------------------------
# Level 1 — common percentages, non-calculator
# ---------------------------------------------------------------------------

def generate_numeracy_percentages_l1():
    unit = random.choice(_QUANTITY_UNITS)
    use_third = random.random() < 0.25

    if use_third:
        pct, method, _ = random.choice(_THIRDS)
        amount = _clean_amount_for(pct)
        pct_str = "33⅓" if pct == 33 else "66⅔"
    else:
        pct, method = random.choice(_COMMON_PCTS)
        amount = _clean_amount_for(pct)
        pct_str = str(pct)

    answer = _common_pct_answer(pct, amount)
    amount_str = _fmt_unit(amount, unit)
    answer_str = _fmt_unit(answer, unit)

    question_text = f"Work out {pct_str}% of {amount_str} (no calculator)."
    worked = [
        f"{pct_str}% of {amount_str} is found using: {method}",
        f"{pct_str}% of {amount_str} = {answer_str}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "percentage_stepper",
            "scaffold_widget_params": {"kind": "common", "pct_str": pct_str, "amount": amount, "unit": unit},
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — any percentage, calculator allowed
# ---------------------------------------------------------------------------

def generate_numeracy_percentages_l2():
    pct = random.randint(1, 99)
    unit = random.choice(_QUANTITY_UNITS)
    amount = random.choice(range(10, 901, 5))
    answer = round(pct / 100 * amount, 2)
    if float(answer).is_integer():
        answer = int(answer)

    amount_str = _fmt_unit(amount, unit)
    answer_str = _fmt_unit(answer, unit)

    scaffold_steps = [
        {"prompt": "Divide the percentage by 100", "answer": round(pct / 100, 4)},
        {"prompt": f"Multiply this by {amount}", "answer": answer},
    ]
    question_text = f"Calculate {pct}% of {amount_str}."
    worked = [f"{pct}% of {amount_str} = {pct} ÷ 100 × {amount} = {answer_str}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "percentage_stepper",
            "scaffold_widget_params": {"kind": "any", "pct": pct, "amount": amount, "unit": unit},
        },
    )


# ---------------------------------------------------------------------------
# Level 3 — VAT at 20%, and percentage problem-solving comparisons
# ---------------------------------------------------------------------------

def _vat_question():
    price = round(random.uniform(20, 2500), 2)
    vat = round(price * 0.2, 2)
    total = round(price + vat, 2)

    question_text = (
        f"VAT (Value Added Tax) is charged at 20%.\n\n"
        f"An item costs £{price:,.2f} before VAT.\n\n"
        f"**(a)** How much VAT must be added?\n\n"
        f"**(b)** What is the total price including VAT?\n\n"
        f"**Enter your answer for part (b).**"
    )
    scaffold_steps = [
        {"prompt": f"Find the VAT (20% of £{price:,.2f})", "answer": vat},
    ]
    worked = [
        f"(a) VAT = 20% of £{price:,.2f} = £{price:,.2f} ÷ 100 × 20 = £{vat:,.2f}",
        f"(b) Total = £{price:,.2f} + £{vat:,.2f} = £{total:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=total,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "percentage_stepper",
            "scaffold_widget_params": {"kind": "vat", "price": price},
        },
    )


_NAMES = [
    "Alex", "Shona", "Miriam", "Mark", "Angela", "Mary", "Emma", "Kevin",
    "Sally", "Jane", "Deborah", "Fiona", "Callum", "Iona", "Murdo", "Effie",
]


def _compare_offers_question():
    name = random.choice(_NAMES)
    pct1 = random.choice([5, 8, 10, 11, 15, 22, 30])
    base1 = random.choice(range(50, 800, 10))
    pct2 = random.choice([25, 30, 40, 45, 50, 60, 75])
    base2 = random.choice(range(20, 200, 5))

    val1 = round(pct1 / 100 * base1, 2)
    val2 = round(pct2 / 100 * base2, 2)
    while val1 == val2:
        base2 += 5
        val2 = round(pct2 / 100 * base2, 2)
    better = "first" if val1 > val2 else "second"
    better_value = max(val1, val2)

    question_text = (
        f"{name} is offered {pct1}% of £{base1} or {pct2}% of £{base2}.\n\n"
        f"Which offer is worth more — the **first** ({pct1}% of £{base1}) or the "
        f"**second** ({pct2}% of £{base2})?\n\n"
        f"**Enter the value of the better offer, in pounds.**"
    )
    scaffold_steps = [
        {"prompt": f"Work out {pct1}% of £{base1}", "answer": val1},
        {"prompt": f"Work out {pct2}% of £{base2}", "answer": val2},
    ]
    worked = [
        f"{pct1}% of £{base1} = £{val1:,.2f}",
        f"{pct2}% of £{base2} = £{val2:,.2f}",
        f"The {better} offer is worth more: £{better_value:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=better_value,
        topic="Numeracy",
        question_type="Percentages",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "percentage_stepper",
            "scaffold_widget_params": {
                "kind": "compare", "pct1": pct1, "base1": base1, "pct2": pct2, "base2": base2,
            },
        },
    )


def generate_numeracy_percentages_l3():
    return random.choice([
        _vat_question,
        _compare_offers_question,
    ])()


def generate_numeracy_percentages_question():
    return random.choice([
        generate_numeracy_percentages_l1,
        generate_numeracy_percentages_l2,
        generate_numeracy_percentages_l3,
    ])()
