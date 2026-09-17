import random
from core.models.question_model import Question

NOTES = """
**Calculator Percentages:**

To find any percentage of an amount:

$$\\text{percentage} \\div 100 \\times \\text{amount}$$

**Example:** Find 35% of £640.
- 35 ÷ 100 × 640 = **£224**
"""

_ITEMS = [
    "laptop", "television", "sofa", "washing machine", "bicycle", "smartphone",
    "camera", "fridge freezer", "games console", "microwave", "vacuum cleaner",
]


def _money(lo, hi):
    return round(random.uniform(lo, hi), 2)


# ---------------------------------------------------------------------------
# Level 1 — direct calculation
# ---------------------------------------------------------------------------

def generate_percentages_calculator_l1():
    pct = random.randint(1, 99)
    amount = _money(5, 900)
    answer = round(pct / 100 * amount, 2)

    scaffold_steps = [
        {"prompt": "Divide the percentage by 100", "answer": round(pct / 100, 4)},
        {"prompt": "Multiply this by the amount", "answer": answer},
    ]

    question_text = f"Calculate {pct}% of £{amount:,.2f}."
    worked = [f"{pct}% of £{amount:,.2f} = {pct} ÷ 100 × {amount:,.2f} = £{answer:,.2f}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Percentages (Calculator)",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "percentage_calculator_steps",
            "scaffold_widget_params": {"pct": pct, "amount": amount},
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — simple word problem using a calculator percentage
# ---------------------------------------------------------------------------

def generate_percentages_calculator_l2():
    item = random.choice(_ITEMS)
    price = _money(80, 1500)
    pct = random.randint(1, 40)
    deposit = round(price * pct / 100, 2)

    question_text = (
        f"A {item} costs £{price:,.2f}.\n\n"
        f"A shop asks for a deposit of {pct}% of the price.\n\n"
        f"How much is the deposit?"
    )
    scaffold_steps = [
        {"prompt": "Divide the percentage by 100", "answer": round(pct / 100, 4)},
        {"prompt": "Multiply this by the price", "answer": deposit},
    ]
    worked = [f"Deposit = {pct}% of £{price:,.2f} = {pct} ÷ 100 × {price:,.2f} = £{deposit:,.2f}"]

    return Question(
        question_text=question_text,
        correct_answer=deposit,
        topic="Managing Money",
        question_type="Percentages (Calculator)",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "percentage_calculator_steps",
            "scaffold_widget_params": {"pct": pct, "amount": price},
        },
    )


def generate_percentages_calculator_question():
    return random.choice([
        generate_percentages_calculator_l1,
        generate_percentages_calculator_l2,
    ])()
