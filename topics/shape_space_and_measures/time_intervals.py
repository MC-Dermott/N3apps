import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import fmt12, fmt24, random_time

NOTES = """
**Time Intervals:**

- To find the time between two times, count on from the start time to the end time.
- It's often easiest to count on to the next whole hour first, then add the rest.
- **Example:** From 9:40 a.m. to 11:15 a.m. — 9:40 to 10:00 is 20 minutes, 10:00 to 11:00 is
  1 hour, 11:00 to 11:15 is 15 minutes. Total = 1 hour 35 minutes (95 minutes).

**Word problems — working forwards and backwards:**
- **"What time does it end?"** → start time + duration.
- **"What time must you leave / arrive by?"** → target time − time needed.
"""

_APPOINTMENTS = [
    "a dentist appointment", "a doctor's appointment", "a hair appointment",
    "a driving lesson", "a job interview", "a music lesson", "a football training session",
]
_PLACES = [
    "the library", "the swimming pool", "the shops", "school", "the ferry terminal",
    "the community centre", "the bus station",
]
_NAMES = ["Iain", "Morag", "Callum", "Effie", "Donald", "Katie", "Murdo", "Shona", "Neil", "Fiona"]


def _fmt(t, use24):
    return fmt24(t) if use24 else fmt12(t)


# ---------------------------------------------------------------------------
# Level 1 — elapsed whole hours, or elapsed minutes (under an hour)
# ---------------------------------------------------------------------------

def generate_time_intervals_l1():
    use24 = random.random() < 0.5
    kind = random.choice(["hours", "minutes"])

    if kind == "hours":
        start = random_time(on_hour=True, lo=0, hi=1380)
        duration_h = random.randint(1, 8)
        end = start + duration_h * 60
        answer = duration_h
        unit = "hours"
    else:
        start = random_time()
        duration_m = random.randint(5, 55)
        end = start + duration_m
        answer = duration_m
        unit = "minutes"

    question_text = (
        f"Work out how many **{unit}** have passed from **{_fmt(start, use24)}** "
        f"to **{_fmt(end, use24)}**."
    )
    worked = [f"{_fmt(start, use24)} to {_fmt(end, use24)} = {answer} {unit}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Time Intervals",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "time_intervals",
            "scaffold_widget_params": {
                "direction": "elapsed", "start": start, "end": end, "use24": use24,
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — elapsed hours AND minutes (general case)
# ---------------------------------------------------------------------------

def generate_time_intervals_l2():
    use24 = random.random() < 0.5
    start = random_time(lo=0, hi=1200)
    duration = random.randint(35, 600)
    # avoid a duration that is an exact multiple of 60 (that's Level 1's case)
    if duration % 60 == 0:
        duration += random.choice([-5, 5])
    end = start + duration

    hh, mm = divmod(duration, 60)
    answer = f"{hh}h {mm}min"

    question_text = (
        f"Work out how many **hours and minutes** have passed from **{_fmt(start, use24)}** "
        f"to **{_fmt(end, use24)}**.\n\n"
        f"(Give your answer in the form Xh Ymin, e.g. 2h 15min.)"
    )
    scaffold_steps = [
        {"prompt": "Work out the total number of minutes that have passed", "answer": duration},
    ]
    worked = [
        f"Total elapsed = {duration} minutes",
        f"{duration} minutes = {hh} hours {mm} minutes = {answer}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Time Intervals",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "time_intervals",
            "scaffold_widget_params": {
                "direction": "elapsed", "start": start, "end": end, "use24": use24,
            },
        },
    )


# ---------------------------------------------------------------------------
# Level 3 — word problems (forwards: finish time; backwards: leave-by time)
# ---------------------------------------------------------------------------

def generate_time_intervals_l3():
    direction = random.choice(["forwards", "backwards"])
    name = random.choice(_NAMES)

    if direction == "forwards":
        start = random_time(lo=6 * 60, hi=21 * 60)
        duration = random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 75, 90])
        end = start + duration
        activity = random.choice(_APPOINTMENTS)
        question_text = (
            f"{name} has {activity} starting at **{fmt12(start)}**. It lasts "
            f"**{duration} minutes**.\n\n"
            f"What time does it finish?\n\n"
            f"(Give your answer in the form h:mm am/pm, e.g. 5:05 pm.)"
        )
        answer = fmt12(end)
        worked = [f"{fmt12(start)} + {duration} minutes = {answer}"]
    else:
        target = random_time(lo=8 * 60, hi=21 * 60)
        duration = random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 75, 90])
        leave = target - duration
        place = random.choice(_PLACES)
        question_text = (
            f"{name} needs to be at {place} by **{fmt12(target)}**. The journey takes "
            f"**{duration} minutes**.\n\n"
            f"What is the latest time {name} can leave?\n\n"
            f"(Give your answer in the form h:mm am/pm, e.g. 5:05 pm.)"
        )
        answer = fmt12(leave)
        worked = [f"{fmt12(target)} − {duration} minutes = {answer}"]

    if direction == "forwards":
        scaffold_params = {"direction": "forward", "start": start, "duration": duration, "use24": False}
    else:
        scaffold_params = {"direction": "backward", "target": target, "duration": duration, "use24": False}

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Time Intervals",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={"scaffold_widget": "time_intervals", "scaffold_widget_params": scaffold_params},
    )


def generate_time_intervals_question():
    return random.choice([
        generate_time_intervals_l1,
        generate_time_intervals_l2,
        generate_time_intervals_l3,
    ])()
