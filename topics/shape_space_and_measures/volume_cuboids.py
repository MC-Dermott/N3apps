import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import fmt_num

NOTES = """
**Volume of a Cuboid:**

- Volume = length × width × height
- Always give your answer in **cubic units** (cm³, m³).

**Example:** A cuboid is 6 cm long, 4 cm wide and 3 cm high.
- Volume = 6 × 4 × 3 = 24 × 3 = **72 cm³**
"""

_UNITS = ["cm", "m"]


# ---------------------------------------------------------------------------
# Level 1 — from a diagram, whole-number cm
# ---------------------------------------------------------------------------

def generate_volume_cuboids_l1():
    length = random.randint(2, 15)
    width = random.randint(2, 12)
    height = random.randint(2, 12)
    base_area = length * width
    answer = base_area * height

    question_text = "Find the **volume** of this cuboid (lengths are in cm)."
    scaffold_steps = [
        {"prompt": "Find the area of the base (length × width)", "answer": base_area},
    ]
    worked = [
        f"Base area = {length} × {width} = {base_area} cm²",
        f"Volume = {base_area} × {height} = {answer} cm³",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Volume of Cuboids",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "cuboid",
            "diagram_params": {
                "length": length, "width": width, "height": height,
                "length_label": f"{length} cm", "width_label": f"{width} cm",
                "height_label": f"{height} cm",
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — from given dimensions as text, decimals allowed, calculator
# ---------------------------------------------------------------------------

def generate_volume_cuboids_l2():
    unit = random.choice(_UNITS)
    length = round(random.uniform(1.5, 20), 1)
    width = round(random.uniform(1.5, 15), 1)
    height = round(random.uniform(1.5, 12), 1)
    base_area = round(length * width, 2)
    answer = round(base_area * height, 2)

    question_text = (
        f"Find the volume of a cuboid **{fmt_num(length, 1)} {unit} long, "
        f"{fmt_num(width, 1)} {unit} wide and {fmt_num(height, 1)} {unit} high**.\n\n"
        f"(Remember to work in {unit}³.)"
    )
    scaffold_steps = [
        {"prompt": "Find the area of the base (length × width)", "answer": base_area},
    ]
    worked = [
        f"Base area = {fmt_num(length, 1)} × {fmt_num(width, 1)} = {fmt_num(base_area)} {unit}²",
        f"Volume = {fmt_num(base_area)} × {fmt_num(height, 1)} = {fmt_num(answer)} {unit}³",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Volume of Cuboids",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_volume_cuboids_question():
    return random.choice([
        generate_volume_cuboids_l1,
        generate_volume_cuboids_l2,
    ])()
