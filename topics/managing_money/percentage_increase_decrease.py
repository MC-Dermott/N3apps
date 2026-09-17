import random
from core.models.question_model import Question

NOTES = """
**Percentage Increase and Decrease:**

1. Find the percentage **of** the original amount.
2. **Add** it (increase) or **subtract** it (decrease) from the original amount.

**Example:** A lawnmower costing £130 is reduced by 50% in a sale.
- 50% of £130 = £65
- Sale price = £130 − £65 = **£65**

**Example:** A cake weighing 1600g has its weight increased by 20%.
- 20% of 1600g = 320g
- New weight = 1600g + 320g = **1920g**
"""

_DISCOUNT_ITEMS = [
    "lawnmower", "games console", "pair of shoes", "bike", "helicopter ride",
    "painting", "tablet", "pair of headphones", "coffee machine", "electric heater",
]

_INCREASE_ITEMS = [
    ("cake", "weight", "g", False),
    ("shampoo bottle", "amount of shampoo", "ml", False),
    ("recipe", "amount of sugar", "g", False),
    ("monthly salary", "salary", "", True),
    ("monthly rent", "rent", "", True),
    ("car's value", "value", "", True),
]


def _round_amount():
    return random.choice(range(20, 2001, 5))


# ---------------------------------------------------------------------------
# Level 1 — single direct calculation (discount or increase)
# ---------------------------------------------------------------------------

def generate_percentage_increase_decrease_l1():
    is_increase = random.choice([True, False])
    pct = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 75])
    amount = _round_amount()
    change = round(amount * pct / 100, 2)
    new_amount = round(amount + change, 2) if is_increase else round(amount - change, 2)

    if is_increase:
        name, noun, unit, is_money = random.choice(_INCREASE_ITEMS)
        amount_str = f"£{amount}" if is_money else f"{amount}{unit}"
        question_text = (
            f"A {name} of {amount_str} is increased by {pct}%.\n\n"
            f"Calculate the new {noun}."
        )
    else:
        item = random.choice(_DISCOUNT_ITEMS)
        question_text = (
            f"A {item} costing £{amount} is reduced by {pct}% in a sale.\n\n"
            f"Calculate the sale price of the {item}."
        )

    scaffold_steps = [
        {"prompt": f"Calculate {pct}% of {amount}", "answer": change},
    ]
    verb_word = "increase" if is_increase else "decrease"
    op = "+" if is_increase else "−"
    worked = [
        f"{pct}% of {amount} = {change}",
        f"New amount ({verb_word}) = {amount} {op} {change} = {new_amount}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=new_amount,
        topic="Managing Money",
        question_type="Percentage Increase/Decrease",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "increase_decrease_number_line",
            "scaffold_widget_params": {
                "is_increase": is_increase, "original": amount, "pct": pct, "new_amount": new_amount,
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — item table (several items/rates in one question)
# ---------------------------------------------------------------------------

def generate_percentage_increase_decrease_l2():
    is_increase = random.choice([True, False])
    n_items = random.choice([3, 4])
    items = random.sample(_DISCOUNT_ITEMS if not is_increase else
                           ["laptop", "camera", "calculator", "tablet", "printer", "speaker"], n_items)
    rows = []
    total_new = 0.0
    for item in items:
        price = round(random.uniform(8, 800), 2)
        pct = random.choice([5, 10, 12, 15, 18, 20, 24, 25, 30, 35])
        change = round(price * pct / 100, 2)
        new_price = round(price + change, 2) if is_increase else round(price - change, 2)
        rows.append((item, price, pct, new_price))
        total_new += new_price
    total_new = round(total_new, 2)

    verb = "increases" if is_increase else "reductions"
    table_lines = "\n".join(
        f"| {item.capitalize()} | £{price:,.2f} | {pct}% |" for item, price, pct, _ in rows
    )
    question_text = (
        f"A shop applies the following {verb}:\n\n"
        f"| Item | Normal Price | {'Increase' if is_increase else 'Discount'} |\n"
        f"|---|---|---|\n"
        f"{table_lines}\n\n"
        f"Calculate the **total** of the new prices for all {n_items} items."
    )

    scaffold_steps = []
    running = 0.0
    for item, price, pct, new_price in rows:
        running = round(running + new_price, 2)
        scaffold_steps.append(
            {"prompt": f"New price of the {item} (after {pct}% {'increase' if is_increase else 'discount'})",
             "answer": new_price}
        )

    worked = []
    for item, price, pct, new_price in rows:
        change = round(price * pct / 100, 2)
        op = "+" if is_increase else "−"
        worked.append(
            f"{item.capitalize()}: {pct}% of £{price:,.2f} = £{change:,.2f} → "
            f"£{price:,.2f} {op} £{change:,.2f} = £{new_price:,.2f}"
        )
    worked.append(
        "Total = " + " + ".join(f"£{r[3]:,.2f}" for r in rows) + f" = £{total_new:,.2f}"
    )

    return Question(
        question_text=question_text,
        correct_answer=total_new,
        topic="Managing Money",
        question_type="Percentage Increase/Decrease",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 3 — two-step "further problems"
# ---------------------------------------------------------------------------

def generate_percentage_increase_decrease_l3():
    kind = random.choice(["bonus", "rent_share"])
    if kind == "bonus":
        salary = random.choice(range(12000, 35001, 500))
        pct = random.choice([2, 3, 4, 5, 6, 8, 10])
        bonus = round(salary * pct / 100, 2)
        total = round(salary + bonus, 2)

        question_text = (
            f"A worker has a salary of £{salary:,}.\n\n"
            f"They receive a bonus of {pct}% of their salary.\n\n"
            f"How much do they get altogether (salary plus bonus)?"
        )
        scaffold_steps = [
            {"prompt": f"Calculate the bonus ({pct}% of £{salary:,})", "answer": bonus},
        ]
        worked = [
            f"Bonus = {pct}% of £{salary:,} = £{bonus:,.2f}",
            f"Total = £{salary:,} + £{bonus:,.2f} = £{total:,.2f}",
        ]
        answer = total
    else:
        full_rent = random.choice(range(200, 901, 10))
        pct = random.choice([70, 75, 80, 85, 90])
        paid = round(full_rent * pct / 100, 2)

        question_text = (
            f"The rental on a flat is £{full_rent} per month.\n\n"
            f"Two friends get a special deal and only have to pay {pct}% of this.\n\n"
            f"How much do they pay per month?"
        )
        scaffold_steps = [
            {"prompt": f"Calculate {pct}% of £{full_rent}", "answer": paid},
        ]
        worked = [f"{pct}% of £{full_rent} = £{paid:,.2f}"]
        answer = paid

    if kind == "bonus":
        widget_params = {"is_increase": True, "original": salary, "pct": pct, "new_amount": total}
    else:
        widget_params = {"is_increase": False, "original": full_rent, "pct": 100 - pct, "new_amount": paid}

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Percentage Increase/Decrease",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "increase_decrease_number_line",
            "scaffold_widget_params": widget_params,
        },
    )


def generate_percentage_increase_decrease_question():
    return random.choice([
        generate_percentage_increase_decrease_l1,
        generate_percentage_increase_decrease_l2,
        generate_percentage_increase_decrease_l3,
    ])()
