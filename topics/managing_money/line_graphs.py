import random
from core.models.question_model import Question

NOTES = """
**Reading Line Graphs:**

- Find the point on the x-axis, then trace up to the line and across to the y-axis to read the
  value.
- To find a **difference**: read both values and subtract.
- The **maximum** is the highest point on the line; the **minimum** is the lowest point.

**Example:** A temperature graph shows 14°C at 10:00 and 19°C at 14:00.
- Difference = 19 − 14 = **5°C**
"""

_SCENARIOS = [
    {"title": "Temperature Over a Day", "x_label": "Time", "y_label": "Temperature (°C)",
     "x_values": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"], "lo": -2, "hi": 24},
    {"title": "Average Monthly Rainfall", "x_label": "Month", "y_label": "Rainfall (mm)",
     "x_values": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "lo": 20, "hi": 220},
    {"title": "Hours of Sunshine", "x_label": "Month", "y_label": "Hours of sunshine",
     "x_values": ["Mar", "Apr", "May", "Jun", "Jul", "Aug"], "lo": 1, "hi": 12},
    {"title": "Ferry Passenger Numbers", "x_label": "Month", "y_label": "Passengers (hundreds)",
     "x_values": ["Jan", "Mar", "May", "Jul", "Sep", "Nov"], "lo": 4, "hi": 40},
    {"title": "Water Tank Level Over a Week", "x_label": "Day", "y_label": "Level (litres)",
     "x_values": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "lo": 100, "hi": 900},
]


def _values(sc):
    n = len(sc["x_values"])
    return [random.randint(sc["lo"], sc["hi"]) for _ in range(n)]


def _make_question(focus_choices):
    sc = random.choice(_SCENARIOS)
    y_values = _values(sc)
    focus = random.choice(focus_choices)

    if focus == "read":
        idx = random.randrange(len(sc["x_values"]))
        answer = y_values[idx]
        question_text = (
            f"The line graph shows **{sc['title'].lower()}**.\n\n"
            f"What value is shown at **{sc['x_values'][idx]}**?"
        )
        worked = [f"At {sc['x_values'][idx]}, the graph reads {answer}"]
        scaffold_steps = []
    elif focus == "difference":
        i, j = random.sample(range(len(sc["x_values"])), 2)
        bigger, smaller = (i, j) if y_values[i] >= y_values[j] else (j, i)
        answer = y_values[bigger] - y_values[smaller]
        question_text = (
            f"The line graph shows **{sc['title'].lower()}**.\n\n"
            f"What is the difference between the values at **{sc['x_values'][bigger]}** "
            f"and **{sc['x_values'][smaller]}**?"
        )
        worked = [
            f"{sc['x_values'][bigger]} = {y_values[bigger]}, {sc['x_values'][smaller]} = {y_values[smaller]}",
            f"Difference = {y_values[bigger]} − {y_values[smaller]} = {answer}",
        ]
        scaffold_steps = [
            {"prompt": f"Read the value at {sc['x_values'][bigger]}", "answer": y_values[bigger]},
            {"prompt": f"Read the value at {sc['x_values'][smaller]}", "answer": y_values[smaller]},
        ]
    else:  # max or min
        want_max = random.choice([True, False])
        answer = max(y_values) if want_max else min(y_values)
        which = "highest" if want_max else "lowest"
        question_text = (
            f"The line graph shows **{sc['title'].lower()}**.\n\n"
            f"What is the **{which}** value shown on the graph?"
        )
        worked = [f"The {which} value on the graph is {answer}"]
        scaffold_steps = []

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Line Graphs",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "line_chart",
            "diagram_params": {
                "x_values": sc["x_values"],
                "y_values": y_values,
                "x_label": sc["x_label"],
                "y_label": sc["y_label"],
                "title": sc["title"],
            },
        },
    )


def generate_line_graphs_l1():
    return _make_question(["read", "max_min"])


def generate_line_graphs_l2():
    return _make_question(["difference", "max_min"])


def generate_line_graphs_question():
    return random.choice([
        generate_line_graphs_l1,
        generate_line_graphs_l2,
    ])()
