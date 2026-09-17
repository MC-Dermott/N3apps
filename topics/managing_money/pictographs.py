import random
from core.models.question_model import Question

NOTES = """
**Reading Pictographs:**

- Each symbol stands for a fixed number of items — check the key (e.g. "1 symbol = 5 items").
- To read a value: count the symbols for that category and multiply by the key value.
- A half symbol represents half the key value.

**Example:** If 1 symbol = 5 lollies and Monday shows 3 symbols:
- Monday's total = 3 × 5 = **15 lollies**
"""

_SCENARIOS = [
    {"title": "Lollies Sold This Week", "unit": "lollies", "categories":
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
    {"title": "Greeting Cards Sold", "unit": "cards", "categories":
        ["Birthday", "Thank You", "Get Well", "Christmas", "Anniversary"]},
    {"title": "Favourite Fruit Drinks", "unit": "children", "categories":
        ["Pineapple", "Orange", "Blackcurrant", "Grapefruit", "Apple"]},
    {"title": "Cans Collected for Recycling", "unit": "cans", "categories":
        ["Alice", "Kevin", "Tim", "Priya"]},
    {"title": "Books Borrowed This Month", "unit": "books", "categories":
        ["Fiction", "Non-fiction", "Crime", "Biography"]},
]

_UNIT_VALUES = [2, 4, 5, 10]


def _round_to_unit(n, unit_value):
    return round(n / unit_value) * unit_value


def _build_values(categories, unit_value):
    n_symbols = [random.randint(1, 8) for _ in categories]
    # occasionally allow a half-symbol on one category
    values = [n * unit_value for n in n_symbols]
    if unit_value % 2 == 0 and random.random() < 0.4:
        idx = random.randrange(len(values))
        values[idx] += unit_value // 2
    return values


def _make_question(n_categories):
    sc = random.choice(_SCENARIOS)
    categories = sc["categories"][:n_categories] if len(sc["categories"]) >= n_categories else sc["categories"]
    unit_value = random.choice(_UNIT_VALUES)
    values = _build_values(categories, unit_value)

    focus = random.choice(["read", "compare", "total"])

    if focus == "read":
        idx = random.randrange(len(categories))
        answer = values[idx]
        question_text = (
            f"The pictogram shows **{sc['title'].lower()}**. Each symbol = {unit_value} {sc['unit']}.\n\n"
            f"How many {sc['unit']} does **{categories[idx]}** show?"
        )
        n_symbols_str = f"{values[idx] // unit_value}" + (
            "½" if values[idx] % unit_value else ""
        )
        worked = [f"{categories[idx]}: {n_symbols_str} symbols × {unit_value} = {answer} {sc['unit']}"]
        scaffold_steps = []
        widget_relevant, widget_op = [categories[idx]], "read"
    elif focus == "compare":
        i, j = random.sample(range(len(categories)), 2)
        bigger, smaller = (i, j) if values[i] >= values[j] else (j, i)
        answer = values[bigger] - values[smaller]
        question_text = (
            f"The pictogram shows **{sc['title'].lower()}**. Each symbol = {unit_value} {sc['unit']}.\n\n"
            f"Estimate how many more {sc['unit']} **{categories[bigger]}** shows than **{categories[smaller]}**."
        )
        worked = [
            f"{categories[bigger]} = {values[bigger]} {sc['unit']}, {categories[smaller]} = {values[smaller]} {sc['unit']}",
            f"Difference = {values[bigger]} − {values[smaller]} = {answer}",
        ]
        scaffold_steps = [
            {"prompt": f"Read the value for {categories[bigger]}", "answer": values[bigger]},
            {"prompt": f"Read the value for {categories[smaller]}", "answer": values[smaller]},
        ]
        widget_relevant, widget_op = [categories[bigger], categories[smaller]], "diff"
    else:
        answer = sum(values)
        question_text = (
            f"The pictogram shows **{sc['title'].lower()}**. Each symbol = {unit_value} {sc['unit']}.\n\n"
            f"Estimate the total number of {sc['unit']} shown altogether."
        )
        worked = [
            "Total = " + " + ".join(str(v) for v in values) + f" = {answer}",
        ]
        scaffold_steps = [
            {"prompt": f"Read the value for {cat}", "answer": val}
            for cat, val in zip(categories, values)
        ]
        widget_relevant, widget_op = list(categories), "sum"

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Pictographs",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "pictograph",
            "diagram_params": {
                "categories": categories,
                "values": values,
                "unit_value": unit_value,
                "icon_label": sc["unit"],
                "title": sc["title"],
            },
            "scaffold_widget": "symbol_counter",
            "scaffold_widget_params": {
                "categories": list(categories), "values": list(values), "unit_value": unit_value,
                "relevant": widget_relevant, "op": widget_op,
            },
        },
    )


def generate_pictographs_l1():
    return _make_question(4)


def generate_pictographs_l2():
    return _make_question(random.choice([5, 6]))


def generate_pictographs_question():
    return random.choice([
        generate_pictographs_l1,
        generate_pictographs_l2,
    ])()
