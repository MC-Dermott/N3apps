import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import fmt12, fmt24, random_time

NOTES = """
**Converting Between 12-Hour and 24-Hour Time:**

- **12-hour → 24-hour:** for times from midnight up to 12:59 p.m., the hour stays the same
  (add a leading zero if needed) — e.g. 9:40 a.m. → 09:40, 12:15 p.m. → 12:15. For 1 p.m.
  onwards, add 12 to the hour — e.g. 5:00 p.m. → 17:00.
- **24-hour → 12-hour:** for 00:00–12:59, keep the hour the same (00:00 is 12:00 a.m.,
  12:00 is 12:00 p.m.) and label it a.m./p.m. accordingly. For 13:00 and above, subtract 12
  from the hour and label it p.m. — e.g. 17:05 → 5:05 p.m.

**Example:** 2:20 p.m. → 24-hour time: **14:20**
**Example:** 20:10 → 12-hour time: **8:10 p.m.**
"""


def _make_question(t, to24):
    direction = "12to24" if to24 else "24to12"
    if to24:
        shown = fmt12(t)
        answer = fmt24(t)
        question_text = (
            f"Change **{shown}** to 24-hour time.\n\n"
            f"(Give your answer in the form HH:MM, e.g. 05:05.)"
        )
        worked = [f"{shown} = {answer}"]
    else:
        shown = fmt24(t)
        answer = fmt12(t)
        question_text = (
            f"Change **{shown}** to 12-hour time.\n\n"
            f"(Give your answer in the form h:mm am/pm, e.g. 5:05 pm.)"
        )
        worked = [f"{shown} = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Clock Conversion",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "time_conversion",
            "scaffold_widget_params": {"direction": direction},
        },
    )


# ---------------------------------------------------------------------------
# Level 1 — on the hour / half hour
# ---------------------------------------------------------------------------

def generate_clock_conversion_l1():
    t = random_time(on_half=True)
    return _make_question(t, to24=random.random() < 0.5)


# ---------------------------------------------------------------------------
# Level 2 — arbitrary minutes
# ---------------------------------------------------------------------------

def generate_clock_conversion_l2():
    t = random_time()
    return _make_question(t, to24=random.random() < 0.5)


def generate_clock_conversion_question():
    return random.choice([
        generate_clock_conversion_l1,
        generate_clock_conversion_l2,
    ])()
