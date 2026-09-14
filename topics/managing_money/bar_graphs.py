import random
from core.models.question_model import Question

NOTES = """
**Reading Bar Graphs:**

- Read the height of each bar against the scale on the axis.
- To find a **total**: add up all the bar heights.
- To find the **range**: subtract the smallest bar value from the largest.
- To **compare**: look at which bars are taller/shorter for each category.

**Example:** Bars show 4, 7, 2, 9, 5.
- Total = 4 + 7 + 2 + 9 + 5 = 27
- Range = 9 − 2 = **7**
"""

_SINGLE_SCENARIOS = [
    {"title": "Hours of Sunshine This Week", "x_label": "Day", "y_label": "Hours of sunshine",
     "categories": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]},
    {"title": "Pocket Money Given", "x_label": "Name", "y_label": "Pocket money (£)",
     "categories": ["Alice", "Allan", "Brian", "Mary", "Ian", "Carol"]},
    {"title": "Sandwiches Sold at Lunchtime", "x_label": "Flavour", "y_label": "No. sold",
     "categories": ["Cheese", "Ham", "Tuna", "Chicken", "Steak"]},
    {"title": "Cans Collected", "x_label": "Name", "y_label": "No. of cans",
     "categories": ["Alice", "Kevin", "Tim", "Priya"]},
    {"title": "Distance Walked to School", "x_label": "Name", "y_label": "Distance (m)",
     "categories": ["Tom", "Zara", "Ewan", "Lucy", "Cameron"]},
]

_DOUBLE_SCENARIOS = [
    {"title": "Favourite School Subjects", "x_label": "Subject", "y_label": "No. of pupils",
     "group1": "S1", "group2": "S2", "categories": ["Maths", "English", "Art", "PE", "Music"]},
    {"title": "Weekly Sports Participation", "x_label": "Sport", "y_label": "No. of pupils",
     "group1": "Girls", "group2": "Boys", "categories": ["Football", "Swimming", "Athletics", "Cycling"]},
    {"title": "Library Book Borrowing", "x_label": "Genre", "y_label": "No. of books",
     "group1": "Adults", "group2": "Teenagers", "categories": ["Fiction", "Crime", "Sci-Fi", "Biography"]},
]


def _bar_vals(n, lo=2, hi=32, step=1):
    return [random.randint(lo, hi) for _ in range(n)]


# ---------------------------------------------------------------------------
# Level 1 — single-series: read, total, range
# ---------------------------------------------------------------------------

def generate_bar_graphs_l1():
    sc = random.choice(_SINGLE_SCENARIOS)
    n = len(sc["categories"])
    values = _bar_vals(n)

    focus = random.choice(["read", "total", "range"])

    if focus == "read":
        idx = random.randrange(n)
        answer = values[idx]
        question_text = (
            f"The bar graph shows **{sc['title'].lower()}**.\n\n"
            f"How many does **{sc['categories'][idx]}** show?"
        )
        worked = [f"{sc['categories'][idx]} = {answer}"]
        scaffold_steps = []
    elif focus == "total":
        answer = sum(values)
        question_text = (
            f"The bar graph shows **{sc['title'].lower()}**.\n\n"
            f"Find the total shown across all categories."
        )
        worked = ["Total = " + " + ".join(str(v) for v in values) + f" = {answer}"]
        scaffold_steps = [
            {"prompt": f"Read the value for {cat}", "answer": val}
            for cat, val in zip(sc["categories"], values)
        ]
    else:
        answer = max(values) - min(values)
        question_text = (
            f"The bar graph shows **{sc['title'].lower()}**.\n\n"
            f"Find the **range** (the difference between the largest and smallest values)."
        )
        worked = [
            f"Largest = {max(values)}, Smallest = {min(values)}",
            f"Range = {max(values)} − {min(values)} = {answer}",
        ]
        scaffold_steps = [
            {"prompt": "Read the largest bar value", "answer": max(values)},
            {"prompt": "Read the smallest bar value", "answer": min(values)},
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Bar Graphs",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "bar_chart",
            "diagram_params": {
                "categories": sc["categories"],
                "group1_data": values,
                "group2_data": None,
                "group1_name": sc["title"],
                "group2_name": None,
                "x_label": sc["x_label"],
                "y_label": sc["y_label"],
                "title": sc["title"],
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — two-series: compare categories
# ---------------------------------------------------------------------------

def generate_bar_graphs_l2():
    sc = random.choice(_DOUBLE_SCENARIOS)
    n = len(sc["categories"])
    g1 = _bar_vals(n)
    g2 = _bar_vals(n)

    focus = random.choice(["compare", "total_one", "combined_total"])

    if focus == "compare":
        idx = random.randrange(n)
        cat = sc["categories"][idx]
        bigger_group = sc["group1"] if g1[idx] >= g2[idx] else sc["group2"]
        answer = abs(g1[idx] - g2[idx])
        question_text = (
            f"The bar graph shows **{sc['title'].lower()}**, comparing {sc['group1']} and {sc['group2']}.\n\n"
            f"How many more **{cat}** pupils are there in the group with more — **{bigger_group}**?"
        )
        worked = [
            f"{sc['group1']} ({cat}) = {g1[idx]}, {sc['group2']} ({cat}) = {g2[idx]}",
            f"Difference = {answer}",
        ]
        scaffold_steps = [
            {"prompt": f"Read the {sc['group1']} value for {cat}", "answer": g1[idx]},
            {"prompt": f"Read the {sc['group2']} value for {cat}", "answer": g2[idx]},
        ]
    elif focus == "total_one":
        group_name, data = random.choice([(sc["group1"], g1), (sc["group2"], g2)])
        answer = sum(data)
        question_text = (
            f"The bar graph shows **{sc['title'].lower()}**, comparing {sc['group1']} and {sc['group2']}.\n\n"
            f"Find the total for **{group_name}** across all categories."
        )
        worked = ["Total = " + " + ".join(str(v) for v in data) + f" = {answer}"]
        scaffold_steps = [
            {"prompt": f"Read the {group_name} value for {cat}", "answer": val}
            for cat, val in zip(sc["categories"], data)
        ]
    else:
        answer = sum(g1) + sum(g2)
        question_text = (
            f"The bar graph shows **{sc['title'].lower()}**, comparing {sc['group1']} and {sc['group2']}.\n\n"
            f"Find the combined total across both groups and all categories."
        )
        worked = [
            f"{sc['group1']} total = " + " + ".join(str(v) for v in g1) + f" = {sum(g1)}",
            f"{sc['group2']} total = " + " + ".join(str(v) for v in g2) + f" = {sum(g2)}",
            f"Combined total = {sum(g1)} + {sum(g2)} = {answer}",
        ]
        scaffold_steps = [
            {"prompt": f"Find the total for {sc['group1']}", "answer": sum(g1)},
            {"prompt": f"Find the total for {sc['group2']}", "answer": sum(g2)},
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Bar Graphs",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "bar_chart",
            "diagram_params": {
                "categories": sc["categories"],
                "group1_data": g1,
                "group2_data": g2,
                "group1_name": sc["group1"],
                "group2_name": sc["group2"],
                "x_label": sc["x_label"],
                "y_label": sc["y_label"],
                "title": sc["title"],
            },
        },
    )


def generate_bar_graphs_question():
    return random.choice([
        generate_bar_graphs_l1,
        generate_bar_graphs_l2,
    ])()
