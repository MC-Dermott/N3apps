import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import make_l_shape

NOTES = """
**Area of a Composite (L-shaped) Figure:**

- Split the shape into **two rectangles**, find the area of each, then add them together.
- If a side length isn't given directly, use the shape's overall width/height to work it out
  first (opposite/parallel sides must add up to the full length).

**Example:** An L-shape is 12 cm wide and 9 cm tall overall, with a 5 cm × 4 cm rectangle cut
from the top-right corner.
- Rectangle 1 (left): (12 − 5) × 9 = 7 × 9 = 63 cm²
- Rectangle 2 (bottom-right): 5 × (9 − 4) = 5 × 5 = 25 cm²
- Total area = 63 + 25 = **88 cm²**
"""


def _diagram(vertices, edge_labels):
    return {
        "diagram": "rect_shape",
        "diagram_params": {"vertices": vertices, "edge_labels": edge_labels, "title": "Area"},
    }


def _split_and_answer(W, H, a, b):
    rect1 = (W - a) * H       # left-hand rectangle, full height
    rect2 = a * (H - b)       # bottom-right rectangle, under the notch
    return rect1, rect2, rect1 + rect2


# ---------------------------------------------------------------------------
# Level 1 — the four defining side lengths (W, H, a, b) are all labelled directly
# ---------------------------------------------------------------------------

def generate_area_composite_l1():
    shape = make_l_shape()
    W, H, a, b = shape["W"], shape["H"], shape["a"], shape["b"]
    edges = shape["edges"]  # [W, H-b, a, b, W-a, H]
    vertices = shape["vertices"]
    rect1, rect2, answer = _split_and_answer(W, H, a, b)

    # Label the 4 shape-defining edges (0=W, 2=a, 3=b, 5=H); leave the two derived ones blank.
    edge_labels = [f"{W} cm", None, f"{a} cm", f"{b} cm", None, f"{H} cm"]

    question_text = (
        "This L-shaped figure is made from two rectangles.\n\n"
        "Find the **total area** of the shape (all lengths are in cm)."
    )
    scaffold_steps = [
        {"prompt": f"Find the area of the left-hand rectangle ({W} − {a}) × {H}", "answer": rect1},
        {"prompt": f"Find the area of the bottom-right rectangle {a} × ({H} − {b})", "answer": rect2},
    ]
    worked = [
        f"Left rectangle = ({W} − {a}) × {H} = {W - a} × {H} = {rect1} cm²",
        f"Bottom-right rectangle = {a} × ({H} − {b}) = {a} × {H - b} = {rect2} cm²",
        f"Total area = {rect1} + {rect2} = {answer} cm²",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Area of Composite Shapes",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(vertices, edge_labels),
    )


# ---------------------------------------------------------------------------
# Level 2 — one of the four defining lengths must be inferred first
# ---------------------------------------------------------------------------

def generate_area_composite_l2():
    shape = make_l_shape()
    W, H, a, b = shape["W"], shape["H"], shape["a"], shape["b"]
    edges = shape["edges"]
    vertices = shape["vertices"]
    rect1, rect2, answer = _split_and_answer(W, H, a, b)

    # Hide exactly one of {a, b}, revealing its complementary edge (W-a or H-b) instead, so
    # the hidden value must be found by subtracting from the bounding box first.
    hide = random.choice(["a", "b"])
    if hide == "a":
        edge_labels = [f"{W} cm", None, "?", f"{b} cm", f"{W - a} cm", f"{H} cm"]
        infer_line = f"Notch width = {W} − {W - a} = {a} cm"
    else:
        edge_labels = [f"{W} cm", f"{H - b} cm", f"{a} cm", "?", None, f"{H} cm"]
        infer_line = f"Notch height = {H} − {H - b} = {b} cm"

    question_text = (
        "This L-shaped figure is made from two rectangles. One side length isn't given "
        "directly — work it out from the sides you can see.\n\n"
        "Find the **total area** of the shape (all lengths are in cm)."
    )
    scaffold_steps = [
        {"prompt": "Work out the missing side length marked '?'", "answer": a if hide == "a" else b},
        {"prompt": f"Find the area of the left-hand rectangle ({W} − {a}) × {H}", "answer": rect1},
        {"prompt": f"Find the area of the bottom-right rectangle {a} × ({H} − {b})", "answer": rect2},
    ]
    worked = [
        infer_line,
        f"Left rectangle = ({W} − {a}) × {H} = {W - a} × {H} = {rect1} cm²",
        f"Bottom-right rectangle = {a} × ({H} − {b}) = {a} × {H - b} = {rect2} cm²",
        f"Total area = {rect1} + {rect2} = {answer} cm²",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Area of Composite Shapes",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(vertices, edge_labels),
    )


def generate_area_composite_question():
    return random.choice([
        generate_area_composite_l1,
        generate_area_composite_l2,
    ])()
