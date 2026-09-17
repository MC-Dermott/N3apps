import random
from core.models.question_model import Question

NOTES = """
**Reading Pie Charts:**

- A full pie chart represents **100%** (360°).
- If a sector's **angle** is given, its percentage = angle ÷ 360 × 100.
- If every sector's percentage is given except one, the missing percentage is found by
  subtracting the sum of the others from 100%.

**Example:** A sector has an angle of 90°.
- Percentage = 90 ÷ 360 × 100 = **25%**

**Example:** Three sectors are 40%, 25% and 15%. The fourth sector is missing.
- Missing % = 100 − (40 + 25 + 15) = **20%**
"""

_SCENARIOS = [
    {"title": "How Pupils Travel to School", "categories": ["Bus", "Car", "Walking", "Bike"]},
    {"title": "Favourite Sport", "categories": ["Football", "Swimming", "Athletics", "Tennis"]},
    {"title": "Breakfast Cereal Ingredients", "categories": ["Wheat", "Barley", "Oats", "Sugar"]},
    {"title": "Holiday Arrangements", "categories": ["Seaside", "Touring", "Camping", "At Home"]},
    {"title": "Favourite Drink", "categories": ["Water", "Irn Bru", "Coke", "Orange", "Lemon"]},
    {"title": "Household Income Use", "categories": ["Rent", "Food", "Entertainment", "Travel", "Savings"]},
]

_ANGLE_CHOICES = [30, 36, 45, 60, 72, 90, 108, 120, 135, 144, 150, 180]


# ---------------------------------------------------------------------------
# Level 1 — read a percentage from a labelled angle
# ---------------------------------------------------------------------------

def generate_pie_charts_l1():
    sc = random.choice(_SCENARIOS)
    n = min(len(sc["categories"]), random.choice([3, 4]))
    categories = sc["categories"][:n]

    # Build angles that sum to 360, each a "nice" value
    while True:
        angles = [random.choice(_ANGLE_CHOICES) for _ in range(n - 1)]
        remaining = 360 - sum(angles)
        if 10 <= remaining <= 200:
            angles.append(remaining)
            break

    idx = random.randrange(n)
    answer = round(angles[idx] / 360 * 100, 1)
    if answer == int(answer):
        answer = int(answer)

    question_text = (
        f"This pie chart shows **{sc['title'].lower()}**.\n\n"
        f"What percentage of the total does **{categories[idx]}** represent?"
    )

    scaffold_steps = [
        {"prompt": f"Divide the angle for {categories[idx]} by 360", "answer": round(angles[idx] / 360, 4)},
    ]
    worked = [
        f"{categories[idx]} angle = {angles[idx]}°",
        f"Percentage = {angles[idx]} ÷ 360 × 100 = {answer}%",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": categories,
                "angles": angles,
                "wedge_labels": [f"{a}°" for a in angles],
                "show_legend": False,
            },
            "scaffold_widget": "pie_angle_calculator",
            "scaffold_widget_params": {
                "categories": list(categories), "kind": "angle_to_pct", "target_idx": idx, "angles": list(angles),
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — infer a missing sector's percentage
# ---------------------------------------------------------------------------

def generate_pie_charts_l2():
    sc = random.choice(_SCENARIOS)
    n = min(len(sc["categories"]), random.choice([3, 4, 5]))
    categories = sc["categories"][:n]

    # Build percentages (multiples of 5) summing to 100, none zero
    while True:
        pcts = [random.choice(range(5, 51, 5)) for _ in range(n - 1)]
        remaining = 100 - sum(pcts)
        if 5 <= remaining <= 60:
            pcts.append(remaining)
            break

    missing_idx = random.randrange(n)
    answer = pcts[missing_idx]

    wedge_labels = [f"{p}%" if i != missing_idx else "?" for i, p in enumerate(pcts)]
    angles = [round(p / 100 * 360) for p in pcts]
    # correct rounding drift so angles sum to exactly 360
    angles[-1] += 360 - sum(angles)

    known = [(categories[i], pcts[i]) for i in range(n) if i != missing_idx]
    known_str = ", ".join(f"{cat}: {pct}%" for cat, pct in known)

    question_text = (
        f"This pie chart shows **{sc['title'].lower()}**.\n\n"
        f"The percentages are: {known_str}, and **{categories[missing_idx]}** (shown as '?').\n\n"
        f"All percentages add up to 100%. What percentage does **{categories[missing_idx]}** represent?"
    )

    scaffold_steps = [
        {"prompt": "Add up the known percentages", "answer": sum(p for i, p in enumerate(pcts) if i != missing_idx)},
    ]
    worked = [
        f"Known percentages sum to: {sum(p for i, p in enumerate(pcts) if i != missing_idx)}%",
        f"Missing percentage = 100 − {sum(p for i, p in enumerate(pcts) if i != missing_idx)} = {answer}%",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Pie Charts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "pie_chart",
            "diagram_params": {
                "categories": categories,
                "angles": angles,
                "wedge_labels": wedge_labels,
                "show_legend": False,
            },
            "scaffold_widget": "pie_angle_calculator",
            "scaffold_widget_params": {
                "categories": list(categories), "kind": "missing_sector", "target_idx": missing_idx, "pcts": list(pcts),
            },
        },
    )


def generate_pie_charts_question():
    return random.choice([
        generate_pie_charts_l1,
        generate_pie_charts_l2,
    ])()
