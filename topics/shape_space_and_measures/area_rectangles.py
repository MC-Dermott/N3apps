import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import fmt_num

NOTES = """
**Area of a Rectangle:**

- Area = length × width
- Always give your answer in **square units** (cm², m², km²).

**Example:** A rectangle is 7 cm by 4 cm.
- Area = 7 × 4 = **28 cm²**
"""

_UNITS = ["cm", "m", "km", "mm"]


# ---------------------------------------------------------------------------
# Level 1 — from a diagram, whole-number cm, no calculator
# ---------------------------------------------------------------------------

def generate_area_rectangles_l1():
    w = random.randint(3, 15)
    h = random.randint(3, 15)
    answer = w * h

    vertices = [(0, 0), (w, 0), (w, h), (0, h)]
    edge_labels = [f"{w} cm", f"{h} cm", None, None]

    question_text = (
        "Find the **area** of this rectangle (lengths are in cm)."
    )
    worked = [f"Area = {w} × {h} = {answer} cm²"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Area of Rectangles",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "rect_shape",
            "diagram_params": {"vertices": vertices, "edge_labels": edge_labels,
                                "title": "Area"},
            "scaffold_widget": "area_rectangles",
            "scaffold_widget_params": {"width": w, "height": h},
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — from given dimensions as text, decimals allowed, calculator
# ---------------------------------------------------------------------------

def generate_area_rectangles_l2():
    unit = random.choice(_UNITS)
    w = round(random.uniform(1.5, 60), 1)
    h = round(random.uniform(1.5, 60), 1)
    answer = round(w * h, 2)

    question_text = (
        f"Find the area of a rectangle **{fmt_num(w, 1)} {unit} by {fmt_num(h, 1)} {unit}**.\n\n"
        f"(Remember to work in {unit}².)"
    )
    worked = [f"Area = {fmt_num(w, 1)} × {fmt_num(h, 1)} = {fmt_num(answer)} {unit}²"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Area of Rectangles",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "area_rectangles",
            "scaffold_widget_params": {"width": w, "height": h},
        },
    )


def generate_area_rectangles_question():
    return random.choice([
        generate_area_rectangles_l1,
        generate_area_rectangles_l2,
    ])()
