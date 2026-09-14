import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import fmt_num

NOTES = """
**Area of a Triangle:**

- Area = ½ × base × height
- The **height** is always measured at right angles (90°) to the base — shown as a dashed
  line in the diagram, not necessarily one of the sloped sides.
- Always give your answer in **square units** (cm², m²).

**Example:** A triangle has base 12 cm and height 5 cm.
- Area = ½ × 12 × 5 = ½ × 60 = **30 cm²**
"""


def _triangle_question(base, height, right_angled, dp):
    apex_frac = 0.0 if (right_angled and random.random() < 0.5) else \
        (1.0 if right_angled else round(random.uniform(0.3, 0.7), 2))
    base_x_area = base * height
    answer = round(base_x_area / 2, 2)

    question_text = (
        f"Find the **area** of this triangle."
    )
    scaffold_steps = [
        {"prompt": "Multiply the base by the height", "answer": round(base_x_area, dp)},
    ]
    worked = [
        f"Base × height = {fmt_num(base, dp)} × {fmt_num(height, dp)} = {fmt_num(base_x_area, dp)}",
        f"Area = {fmt_num(base_x_area, dp)} ÷ 2 = {fmt_num(answer)} cm²",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Area of Triangles",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "triangle",
            "diagram_params": {
                "base": base, "height": height, "apex_frac": apex_frac,
                "base_label": f"{fmt_num(base, dp)} cm", "height_label": f"{fmt_num(height, dp)} cm",
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 1 — whole-number cm
# ---------------------------------------------------------------------------

def generate_area_triangles_l1():
    base = random.randint(4, 24)
    height = random.randint(4, 20)
    return _triangle_question(base, height, right_angled=random.random() < 0.5, dp=0)


# ---------------------------------------------------------------------------
# Level 2 — decimal dimensions, calculator
# ---------------------------------------------------------------------------

def generate_area_triangles_l2():
    base = round(random.uniform(3, 30), 1)
    height = round(random.uniform(3, 25), 1)
    return _triangle_question(base, height, right_angled=random.random() < 0.5, dp=1)


def generate_area_triangles_question():
    return random.choice([
        generate_area_triangles_l1,
        generate_area_triangles_l2,
    ])()
