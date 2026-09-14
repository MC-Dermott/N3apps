import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import ordinal

NOTES = """
**Giving and Following Directions:**

- Side-streets are counted in the order you reach them as you walk along the main road.
- "**Left**" and "**right**" turnings are counted separately — the "second turning on the
  left" is the second side-street *on the left* that you pass, ignoring any streets on the
  right in between.
- To work out where a set of turns leads, follow them one at a time, in the order given.

**Example:** Walking along Main Street from **X**, you pass a street on the left, then one on
the right, then a second street on the left.
- The "second turning on the left" is the **third** street you reach overall, but the
  **second** one specifically on the left.
"""

_STREET_NAMES = [
    "Oak Street", "Birch Avenue", "Cedar Way", "Ash Lane", "Elm Road", "Pine Close",
    "Willow Drive", "Maple Terrace", "Rowan Place", "Heather Road",
]
_UP_LANDMARKS = ["the Park", "the School", "the Library", "the Health Centre", "the Church",
                 "the Community Centre", "the Museum"]
_DOWN_LANDMARKS = ["the Shop", "the Swimming Pool", "the Bank", "the Car Park", "the Cinema",
                    "the Bus Station", "the Harbour"]


def _build_map(n_streets, with_extension):
    # decide up/down for each street position, guaranteeing at least 2 of each
    while True:
        dirs = [random.choice(["up", "down"]) for _ in range(n_streets)]
        if dirs.count("up") >= 2 and dirs.count("down") >= 2:
            break

    up_count = dirs.count("up")
    down_count = dirs.count("down")
    up_landmarks = random.sample(_UP_LANDMARKS, up_count)
    down_landmarks = random.sample(_DOWN_LANDMARKS, down_count)
    names = random.sample(_STREET_NAMES, n_streets)

    streets = []
    ui = di = 0
    for idx in range(n_streets):
        d = dirs[idx]
        if d == "up":
            landmark = up_landmarks[ui]
            ui += 1
        else:
            landmark = down_landmarks[di]
            di += 1
        streets.append({
            "x": idx + 1,
            "dir": d,
            "name": names[idx],
            "landmark": landmark,
            "length": round(random.uniform(1.1, 1.9), 2),
            "has_ext": False,
        })

    if with_extension:
        used = {s["landmark"] for s in streets}
        remaining = [l for l in (_UP_LANDMARKS + _DOWN_LANDMARKS) if l not in used]
        s = random.choice(streets)
        s["has_ext"] = True
        s["ext_left"], s["ext_right"] = random.sample(remaining, 2)

    return streets


def _lr_lists(streets):
    left = [s for s in streets if s["dir"] == "up"]
    right = [s for s in streets if s["dir"] == "down"]
    return left, right


def _diagram(streets):
    return {"diagram": "street_map", "diagram_params": {"streets": streets}}


def _preamble():
    return "Look at the map. Imagine you are standing at **X**, facing along Main Street.\n\n"


# ---------------------------------------------------------------------------
# Level 1 — single turn: name a road, or say where a numbered turning leads
# ---------------------------------------------------------------------------

def generate_directions_l1():
    streets = _build_map(n_streets=random.randint(4, 6), with_extension=False)
    left, right = _lr_lists(streets)
    focus = random.choice(["to_landmark", "nth_name", "nth_destination"])

    if focus == "to_landmark":
        s = random.choice(streets)
        question_text = _preamble() + f"Which road leads to **{s['landmark']}**?"
        answer = s["name"]
        scaffold_steps = []
        worked = [f"{s['landmark']} is at the end of {s['name']}."]
    elif focus == "nth_name":
        side = random.choice(["left", "right"])
        lst = left if side == "left" else right
        n = random.randint(1, len(lst))
        s = lst[n - 1]
        question_text = _preamble() + f"Which road is the **{ordinal(n)} turning on the {side}**?"
        answer = s["name"]
        scaffold_steps = []
        worked = [f"The {ordinal(n)} turning on the {side} is {s['name']}."]
    else:
        side = random.choice(["left", "right"])
        lst = left if side == "left" else right
        n = random.randint(1, len(lst))
        s = lst[n - 1]
        question_text = (
            _preamble()
            + f"If you take the **{ordinal(n)} turning on the {side}**, where will you end up?"
        )
        answer = s["landmark"]
        scaffold_steps = [
            {"prompt": f"Which road is the {ordinal(n)} turning on the {side}?", "answer": s["name"]},
        ]
        worked = [
            f"The {ordinal(n)} turning on the {side} is {s['name']}.",
            f"{s['name']} leads to {s['landmark']}.",
        ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Directions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(streets),
    )


# ---------------------------------------------------------------------------
# Level 2 — two turns: take a numbered turning, then turn again at its end
# ---------------------------------------------------------------------------

def generate_directions_l2():
    streets = _build_map(n_streets=random.randint(5, 7), with_extension=True)
    left, right = _lr_lists(streets)
    s = next(st for st in streets if st["has_ext"])
    lst = left if s["dir"] == "up" else right
    n = lst.index(s) + 1
    side = "left" if s["dir"] == "up" else "right"
    sub_side = random.choice(["left", "right"])
    answer = s["ext_left"] if sub_side == "left" else s["ext_right"]

    question_text = (
        _preamble()
        + f"Take the **{ordinal(n)} turning on the {side}**. Walk to the end of that road, "
        + f"then turn **{sub_side}**.\n\nWhere will you end up?"
    )
    scaffold_steps = [
        {"prompt": f"Which road is the {ordinal(n)} turning on the {side}?", "answer": s["name"]},
    ]
    worked = [
        f"The {ordinal(n)} turning on the {side} is {s['name']}.",
        f"Turning {sub_side} at the end of {s['name']} leads to {answer}.",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Directions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram(streets),
    )


def generate_directions_question():
    return random.choice([
        generate_directions_l1,
        generate_directions_l2,
    ])()
