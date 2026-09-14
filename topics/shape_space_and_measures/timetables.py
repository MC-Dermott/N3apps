import random
from core.models.question_model import Question
from topics.shape_space_and_measures._helpers import fmt24

NOTES = """
**Reading Timetables:**

- Find the **row** for the stop you want and the **column** for the service you want — the
  cell where they meet is the time.
- To find a **journey time**, subtract the departure time from the arrival time (careful when
  it crosses the hour, e.g. 09:40 to 10:15 is 35 minutes, not 25).
- To find **which service to catch**, compare the times for your starting stop and pick the
  one that gets you there in time.

**Example:** A bus leaves Stop A at 09:00 and arrives at Stop B at 09:35.
- Journey time = 09:35 − 09:00 = **35 minutes**
"""

_STOP_POOLS = [
    ["Stornoway", "Tarbert", "Leverburgh", "Balallan", "Ness"],
    ["Stonehouse", "Larkhall", "Hamilton", "Rutherglen", "Glasgow"],
    ["Motherwell", "Hamilton", "Blantyre", "Glasgow", "Partick"],
    ["Aberdeen", "Dundee", "Perth", "Stirling", "Glasgow"],
    ["Portree", "Broadford", "Kyle", "Invergarry", "Fort William"],
]
_MODE_LABELS = {"bus": "Bus Timetable", "train": "Train Timetable", "ferry": "Ferry Timetable"}


def _build_timetable(n_stops, n_services):
    stops = random.choice(_STOP_POOLS)[:n_stops]
    mode = random.choice(list(_MODE_LABELS.keys()))
    service_labels = [chr(ord("A") + i) for i in range(n_services)]

    # Same leg (journey-time) gaps for every service — a fixed route, just different starts.
    leg_gaps = [random.randint(8, 45) for _ in range(n_stops - 1)]

    # Increasing start times per service, spaced well apart across the day.
    starts = []
    t = random.randint(6 * 60, 8 * 60)
    for _ in range(n_services):
        starts.append(t)
        t += random.randint(70, 190)

    # times[service_idx][stop_idx]
    times = []
    for s in starts:
        row = [s]
        for gap in leg_gaps:
            row.append(row[-1] + gap)
        times.append(row)

    times_str = [[fmt24(t) for t in row] for row in times]

    return {
        "mode": mode,
        "stops": stops,
        "service_labels": service_labels,
        "leg_gaps": leg_gaps,
        "times": times,          # minutes, [service][stop]
        "times_str": times_str,  # "HH:MM", [service][stop]
    }


def _diagram_params(tt):
    return {
        "diagram": "timetable",
        "diagram_params": {
            "stops": tt["stops"],
            "services": tt["service_labels"],
            "times": tt["times_str"],
            "title": _MODE_LABELS[tt["mode"]],
        },
    }


# ---------------------------------------------------------------------------
# Level 1 — reading a timetable: departure, arrival, journey time
# ---------------------------------------------------------------------------

def generate_timetables_l1():
    tt = _build_timetable(n_stops=random.choice([3, 4]), n_services=random.choice([2, 3]))
    stops = tt["stops"]
    svc_idx = random.randrange(len(tt["service_labels"]))
    svc = tt["service_labels"][svc_idx]
    end_idx = random.randrange(1, len(stops))

    depart_time = tt["times_str"][svc_idx][0]
    arrive_time = tt["times_str"][svc_idx][end_idx]
    journey_minutes = tt["times"][svc_idx][end_idx] - tt["times"][svc_idx][0]

    question_text = (
        f"Here is part of a {tt['mode']} timetable.\n\n"
        f"**(a)** What time does service **{svc}** leave {stops[0]}?\n\n"
        f"**(b)** What time does service **{svc}** arrive at {stops[end_idx]}?\n\n"
        f"**(c)** How long is the journey from {stops[0]} to {stops[end_idx]} on service "
        f"**{svc}**?\n\n"
        f"**Enter your answer for part (c) — the journey time in minutes.**"
    )
    scaffold_steps = [
        {"prompt": f"What time does service {svc} leave {stops[0]}?", "answer": depart_time},
        {"prompt": f"What time does service {svc} arrive at {stops[end_idx]}?", "answer": arrive_time},
    ]
    worked = [
        f"(a) Service {svc} leaves {stops[0]} at {depart_time}",
        f"(b) Service {svc} arrives at {stops[end_idx]} at {arrive_time}",
        f"(c) Journey time = {arrive_time} − {depart_time} = {journey_minutes} minutes",
    ]

    return Question(
        question_text=question_text,
        correct_answer=journey_minutes,
        topic="Shape, Space & Measures",
        question_type="Timetables",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram_params(tt),
    )


# ---------------------------------------------------------------------------
# Level 2 — which service to catch
# ---------------------------------------------------------------------------

def generate_timetables_l2():
    tt = _build_timetable(n_stops=random.choice([4, 5]), n_services=random.choice([3, 4]))
    stops = tt["stops"]
    start_idx = random.randrange(0, len(stops) - 1)
    dest_idx = random.randrange(start_idx + 1, len(stops))

    # Later services always depart AND arrive later (every service follows the same route,
    # just starting at a different time), so pick a deadline strictly between two
    # consecutive services' arrival times at the destination — the later of that pair is the
    # last one that still makes it, which is the non-trivial part of the question.
    arrivals = [tt["times"][i][dest_idx] for i in range(len(tt["service_labels"]))]
    k = random.randrange(0, len(arrivals) - 1)
    deadline = random.randint(arrivals[k] + 1, arrivals[k + 1] - 1)
    candidates = [i for i in range(len(arrivals)) if arrivals[i] <= deadline]
    best = max(candidates)
    answer = tt["service_labels"][best]

    question_text = (
        f"Here is part of a {tt['mode']} timetable.\n\n"
        f"You need to arrive at **{stops[dest_idx]}** by **{fmt24(deadline)}**.\n\n"
        f"Which service from **{stops[start_idx]}** should you catch?\n\n"
        f"(Enter just the service letter, e.g. A.)"
    )
    scaffold_steps = [
        {
            "prompt": f"Which services arrive at {stops[dest_idx]} at or before {fmt24(deadline)}?",
            "answer": ", ".join(tt["service_labels"][i] for i in candidates),
        },
    ]
    worked = (
        [f"Service {tt['service_labels'][i]} arrives at {stops[dest_idx]} at "
         f"{tt['times_str'][i][dest_idx]}" for i in range(len(arrivals))]
        + [f"Services arriving at or before {fmt24(deadline)}: "
           + ", ".join(tt["service_labels"][i] for i in candidates)]
        + [f"Latest one that still makes it → catch service **{answer}**"]
    )

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Shape, Space & Measures",
        question_type="Timetables",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata=_diagram_params(tt),
    )


def generate_timetables_question():
    return random.choice([
        generate_timetables_l1,
        generate_timetables_l2,
    ])()
