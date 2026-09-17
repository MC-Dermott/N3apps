import random

from core.models.question_model import Question

NOTES = """
**Reading Scales:**

- Work out what each **small gap** between the labelled numbers is worth: count how many
  small gaps there are between two labelled marks, then divide the difference between them
  by that number of gaps.
- Count small gaps from the nearest labelled mark up to the arrow/marker/fill level to find
  the reading.
- For a container, the reading is the level the liquid has filled **up to**, read against
  the scale marked on the side.
- For a thermometer, remember the scale can include values **below zero**.

**Example:** A scale is marked every 50 ml, with 5 small gaps between each label
(so each small gap = 10 ml). If the level is 2 gaps past the 100 ml mark, the reading is
100 + 2 × 10 = **120 ml**.
"""


def _fmt(v):
    if float(v).is_integer():
        return str(int(v))
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ---------------------------------------------------------------------------
# Level 1 — read a value from a ruler / container / thermometer diagram
# ---------------------------------------------------------------------------

def _ruler_scale():
    major = random.choice([10, 20])
    minor = 1 if major == 10 else 2
    n_majors = random.randint(4, 8)
    hi = major * n_majors
    lo = 0
    marker = random.randrange(lo + minor, hi, minor)
    unit = random.choice(["", "", "cm"])
    title = "Number Line" if unit == "" else "Ruler"

    return {
        "style": "ruler",
        "min_value": lo,
        "max_value": hi,
        "major_step": major,
        "minor_step": minor,
        "marker_value": marker,
        "unit_label": unit,
        "title": title,
    }, marker, unit


def _container_scale():
    if random.random() < 0.5:
        lo, hi, major, minor, unit = 0, 200, 50, 10, "ml"
    else:
        lo, hi, major, minor, unit = 0, 2, 0.5, 0.1, "litres"
    n_steps = int(round((hi - lo) / minor))
    marker = round(lo + random.randint(1, n_steps - 1) * minor, 2)

    return {
        "style": "container",
        "min_value": lo,
        "max_value": hi,
        "major_step": major,
        "minor_step": minor,
        "marker_value": marker,
        "unit_label": unit,
        "title": "How much water is in the container?",
    }, marker, unit


def _thermometer_scale():
    lo, hi, major, minor, unit = -10, 40, 10, 2, "°C"
    n_steps = int(round((hi - lo) / minor))
    marker = lo + random.randint(1, n_steps - 1) * minor

    return {
        "style": "thermometer",
        "min_value": lo,
        "max_value": hi,
        "major_step": major,
        "minor_step": minor,
        "marker_value": marker,
        "unit_label": unit,
        "title": "Thermometer",
    }, marker, unit


def generate_reading_scales_l1():
    builder = random.choice([_ruler_scale, _container_scale, _thermometer_scale])
    params, marker, unit = builder()

    unit_suffix = f" {unit}" if unit else ""
    if params["style"] == "ruler":
        prompt = "What number is the arrow pointing to?"
    elif params["style"] == "container":
        prompt = "How much water is in the container?"
    else:
        prompt = "What temperature is the thermometer showing?"

    question_text = prompt
    worked = [f"The arrow/level is at {_fmt(marker)}{unit_suffix}"]

    return Question(
        question_text=question_text,
        correct_answer=marker,
        topic="Numeracy",
        question_type="Reading Scales",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "diagram": "graduated_scale",
            "diagram_params": params,
            "scaffold_widget": "scale_stepper",
            "scaffold_widget_params": {
                "min_value": params["min_value"], "max_value": params["max_value"],
                "major_step": params["major_step"], "minor_step": params["minor_step"],
                "marker_value": params["marker_value"], "unit_label": params["unit_label"],
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — unit-conversion word problems (a plain substitute for the
# speedometer mph <-> km/h reading, which doesn't fit the scale-diagram
# pattern cleanly — see module notes / pipeline report)
# ---------------------------------------------------------------------------

def _metric_conversion_question():
    conversions = [
        {"from_unit": "m", "to_unit": "cm", "factor": 100},
        {"from_unit": "cm", "to_unit": "m", "factor": 0.01},
        {"from_unit": "kg", "to_unit": "g", "factor": 1000},
        {"from_unit": "g", "to_unit": "kg", "factor": 0.001},
        {"from_unit": "litres", "to_unit": "ml", "factor": 1000},
        {"from_unit": "ml", "to_unit": "litres", "factor": 0.001},
    ]
    conv = random.choice(conversions)
    if conv["factor"] >= 1:
        value = random.randint(1, 50)
    else:
        value = random.choice(range(100, 10001, 100))

    answer = round(value * conv["factor"], 3)
    if float(answer).is_integer():
        answer = int(answer)

    question_text = (
        f"Convert {_fmt(value)} {conv['from_unit']} to {conv['to_unit']}."
    )
    worked = [f"{_fmt(value)} {conv['from_unit']} = {_fmt(answer)} {conv['to_unit']}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Reading Scales",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "unit_conversion",
            "scaffold_widget_params": {
                "kind": "metric", "value": value, "from_unit": conv["from_unit"],
                "to_unit": conv["to_unit"], "factor": conv["factor"],
            },
        },
    )


def _mph_kmh_question():
    # Uses the approximation 5 miles is about 8 km (i.e. 1 mph is about 1.6 km/h),
    # stated in the question — a plain word-problem substitute for reading the
    # conversion off a speedometer's dual mph/km-h scale.
    mph = random.choice([20, 30, 40, 50, 60, 70, 10, 80])
    kmh = round(mph * 1.6)

    question_text = (
        f"5 miles is about the same distance as 8 km (so 1 mph is about 1·6 km/h).\n\n"
        f"A car is travelling at {mph} mph.\n\n"
        f"Roughly what speed is this in km/h?"
    )
    scaffold_steps = [
        {"prompt": f"Multiply {mph} by 1·6", "answer": kmh},
    ]
    worked = [f"{mph} mph × 1·6 ≈ {kmh} km/h"]

    return Question(
        question_text=question_text,
        correct_answer=kmh,
        topic="Numeracy",
        question_type="Reading Scales",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "unit_conversion",
            "scaffold_widget_params": {"kind": "mph", "mph": mph},
        },
    )


def generate_reading_scales_l2():
    return random.choice([
        _metric_conversion_question,
        _metric_conversion_question,
        _mph_kmh_question,
    ])()


def generate_reading_scales_question():
    return random.choice([
        generate_reading_scales_l1,
        generate_reading_scales_l2,
    ])()
