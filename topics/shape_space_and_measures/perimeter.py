import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import make_l_shape

NOTES = """
**Perimeter:**

- The perimeter of a shape is the total distance all the way round its outside edge.
- **Rectangle:** Perimeter = 2 × (length + width).
- **Other shapes:** add up the length of every side.
- **Missing sides:** opposite/parallel sides of a rectilinear shape must add up to the full
  length of the shape — use the sides you know to work out the ones you don't.

**Example:** A shape is 12 cm wide overall. One side is labelled 5 cm and the matching
missing side is directly below it. Missing side = 12 − 5 = **7 cm**.
"""


def _rect_shape(w, h):
    vertices = [(0, 0), (w, 0), (w, h), (0, h)]
    edges = [w, h, w, h]
    return vertices, edges


def _diagram(vertices, edge_labels, title="Perimeter", l_shape=None):
    metadata = {
        "diagram": "rect_shape",
        "diagram_params": {
            "vertices": vertices,
            "edge_labels": edge_labels,
            "title": title,
        },
    }
    if l_shape is not None:
        W, H, a, b = l_shape
        metadata["scaffold_widget"] = "l_shape_perimeter"
        metadata["scaffold_widget_params"] = {
            "width": W, "height": H, "notch_width": a, "notch_height": b,
        }
    return metadata


# ---------------------------------------------------------------------------
# Level 1 — every side length is labelled
# ---------------------------------------------------------------------------

def generate_perimeter_l1():
    shape_kind = random.choice(["rectangle", "l_shape"])

    if shape_kind == "rectangle":
        w = random.randint(4, 20)
        h = random.randint(3, 16)
        vertices, edges = _rect_shape(w, h)
        answer = 2 * (w + h)
        edge_labels = [f"{e} cm" for e in edges]
        worked = [
            f"Perimeter = {' + '.join(str(e) for e in edges)} = {answer} cm",
            f"(Or: 2 × ({w} + {h}) = {answer} cm)",
        ]
        l_shape_dims = None
    else:
        shape = make_l_shape()
        edges = shape["edges"]
        vertices = shape["vertices"]
        answer = sum(edges)
        edge_labels = [f"{e} cm" for e in edges]
        worked = [f"Perimeter = {' + '.join(str(e) for e in edges)} = {answer} cm"]
        l_shape_dims = (shape["W"], shape["H"], shape["a"], shape["b"])

    question_text = (
        "Every side of this shape is labelled.\n\n"
        "Find the **perimeter** of the shape (all lengths are in cm)."
    )

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Perimeter",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(vertices, edge_labels, l_shape=l_shape_dims),
    )


# ---------------------------------------------------------------------------
# Level 2 — one or two sides must be inferred
# ---------------------------------------------------------------------------

def generate_perimeter_l2():
    shape = make_l_shape()
    W, H, a, b = shape["W"], shape["H"], shape["a"], shape["b"]
    edges = shape["edges"]
    vertices = shape["vertices"]
    answer = sum(edges)

    # Edge indices: 0=W (bottom), 1=H-b (right), 2=a (notch bottom), 3=b (notch side),
    # 4=W-a (top-left), 5=H (left). 0 and 5 (the bounding-box sides) always stay visible;
    # hide one of {1,4} (the H/W-derived pair) and/or one of {2,3} (the a/b-derived... wait
    # 1 pairs with 3 via H, 2 pairs with 4 via W) so the hidden value can always be found by
    # subtracting the visible partner from the bounding-box side.
    hide_horizontal = random.random() < 0.85  # hides one of edge 2 (a) / edge 4 (W-a)
    hide_vertical = random.random() < 0.85    # hides one of edge 1 (H-b) / edge 3 (b)
    if not hide_horizontal and not hide_vertical:
        hide_horizontal = True  # always hide at least one side

    hidden = set()
    if hide_horizontal:
        hidden.add(random.choice([2, 4]))
    if hide_vertical:
        hidden.add(random.choice([1, 3]))

    edge_labels = [f"{e} cm" if i not in hidden else "?" for i, e in enumerate(edges)]

    infer_lines = []
    if 2 in hidden:
        infer_lines.append(f"Notch width = {W} − {W - a} = {a} cm")
    if 4 in hidden:
        infer_lines.append(f"Top-left width = {W} − {a} = {W - a} cm")
    if 1 in hidden:
        infer_lines.append(f"Right-hand height = {H} − {b} = {H - b} cm")
    if 3 in hidden:
        infer_lines.append(f"Notch height = {H} − {H - b} = {b} cm")

    question_text = (
        "Some of this shape's side lengths are missing — work them out from the sides you "
        "can see before finding the total.\n\n"
        "Find the **perimeter** of the shape (all lengths are in cm)."
    )
    _EDGE_DESC = {1: "right-hand edge", 2: "notch (horizontal)", 3: "notch (vertical)",
                  4: "top-left edge"}
    scaffold_steps = [
        {"prompt": f"Work out the missing side length marked '?' near the {_EDGE_DESC[i]}",
         "answer": edges[i]}
        for i in sorted(hidden)
    ]
    worked = infer_lines + [f"Perimeter = {' + '.join(str(e) for e in edges)} = {answer} cm"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Perimeter",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(vertices, edge_labels, l_shape=(W, H, a, b)),
    )


def generate_perimeter_question():
    return random.choice([
        generate_perimeter_l1,
        generate_perimeter_l2,
    ])()
