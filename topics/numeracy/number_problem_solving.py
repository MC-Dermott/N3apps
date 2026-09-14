import random
from decimal import Decimal, ROUND_HALF_UP

from core.models.question_model import Question

NOTES = """
**Number Problem Solving:**

- **Odd numbers** end in 1, 3, 5, 7 or 9. **Even numbers** end in 0, 2, 4, 6 or 8.
- To find a sum, add every number in the list that matches the rule.
- **Range** (difference between largest and smallest) = largest − smallest.
- In an **arithmetic sequence**, each term changes by the same fixed amount (the *common
  difference*) — work it out from two neighbouring terms, then apply it to find the next term.
  The sequence can go up (e.g. 2, 5, 8, ...) or down (e.g. 100, 99, 98, ...).
- To **estimate**, round each number first (to the nearest 10 or 100), then add or subtract
  the rounded values — it's quick, not exact.

**Example:** Numbers: 245, 100, 39, 63, 50, 77.
- Even numbers: 100, 50 → sum = 150
- Range = 245 − 39 = **206**
"""

_UNIT_NOUNS = ["numbers", "cards", "tickets", "counters", "tiles"]


def _fmt(x):
    if float(x).is_integer():
        return str(int(x))
    return f"{x:.2f}".rstrip("0").rstrip(".")


def _round_half_up_to(value, place):
    d = (Decimal(str(value)) / Decimal(place)).quantize(Decimal(1), rounding=ROUND_HALF_UP)
    return int(d) * place


# ---------------------------------------------------------------------------
# Level 1 — sum/difference/evens & odds within a small set of numbers
# ---------------------------------------------------------------------------

def _random_number_set(n, lo=10, hi=350):
    return [random.randint(lo, hi) for _ in range(n)]


def generate_number_problem_solving_l1():
    n = random.randint(6, 9)
    numbers = _random_number_set(n)
    # guarantee at least one odd and one even so every sub-question type has a valid answer
    if not any(v % 2 == 0 for v in numbers):
        numbers[0] = numbers[0] + 1
    if not any(v % 2 == 1 for v in numbers):
        numbers[1] = numbers[1] + 1

    box_text = "  ".join(str(v) for v in numbers)
    focus = random.choice(["sum_odds", "sum_evens", "range", "count_evens"])

    if focus == "sum_odds":
        odds = [v for v in numbers if v % 2 == 1]
        answer = sum(odds)
        question_text = (
            f"Here are some numbers:\n\n{box_text}\n\n"
            f"Find the sum of all the **odd** numbers in the list."
        )
        worked = [f"Odd numbers: {', '.join(str(v) for v in odds)}",
                   f"Sum = {' + '.join(str(v) for v in odds)} = {answer}"]
    elif focus == "sum_evens":
        evens = [v for v in numbers if v % 2 == 0]
        answer = sum(evens)
        question_text = (
            f"Here are some numbers:\n\n{box_text}\n\n"
            f"Find the sum of all the **even** numbers in the list."
        )
        worked = [f"Even numbers: {', '.join(str(v) for v in evens)}",
                   f"Sum = {' + '.join(str(v) for v in evens)} = {answer}"]
    elif focus == "range":
        answer = max(numbers) - min(numbers)
        question_text = (
            f"Here are some numbers:\n\n{box_text}\n\n"
            f"Find the difference between the largest and smallest number."
        )
        worked = [f"Largest = {max(numbers)}, Smallest = {min(numbers)}",
                   f"Difference = {max(numbers)} − {min(numbers)} = {answer}"]
    else:
        evens = [v for v in numbers if v % 2 == 0]
        answer = len(evens)
        question_text = (
            f"Here are some numbers:\n\n{box_text}\n\n"
            f"How many of these numbers are **even**?"
        )
        worked = [f"Even numbers: {', '.join(str(v) for v in evens) if evens else 'none'}",
                   f"Count = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Number Problem Solving",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 2 — continue a number sequence (increasing or decreasing)
# ---------------------------------------------------------------------------

def generate_number_problem_solving_l2():
    direction = random.choice(["up", "down"])
    step = random.choice([1, 2, 3, 5, 10, 4])
    if direction == "up":
        start = random.randint(1, 50)
        terms = [start + i * step for i in range(5)]
        next1 = terms[-1] + step
        next2 = terms[-1] + 2 * step
    else:
        start = random.randint(60, 200)
        terms = [start - i * step for i in range(5)]
        next1 = terms[-1] - step
        next2 = terms[-1] - 2 * step

    seq_text = ", ".join(str(t) for t in terms) + ", ___, ___"

    question_text = (
        f"Here is a number sequence:\n\n{seq_text}\n\n"
        f"What is the **next number** in the sequence?"
    )
    scaffold_steps = [
        {"prompt": "Find the common difference between consecutive terms "
                    "(how much the sequence goes up or down by each time)", "answer": step},
    ]
    worked = [
        f"Common difference = {step} ({'increasing' if direction == 'up' else 'decreasing'})",
        f"Next number = {terms[-1]} {'+' if direction == 'up' else '−'} {step} = {next1}",
        f"(the number after that would be {next2})",
    ]

    return Question(
        question_text=question_text,
        correct_answer=next1,
        topic="Numeracy",
        question_type="Number Problem Solving",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 3 — estimate a sum/difference to the nearest 10 or 100
# ---------------------------------------------------------------------------

def generate_number_problem_solving_l3():
    place = random.choice([10, 100])
    if place == 10:
        a = random.randint(11, 98)
        b = random.randint(11, 98)
    else:
        a = random.randint(105, 9850)
        b = random.randint(105, 9850)

    op = random.choice(["+", "-"])
    if op == "-" and a < b:
        a, b = b, a

    a_round = _round_half_up_to(a, place)
    b_round = _round_half_up_to(b, place)
    answer = a_round + b_round if op == "+" else a_round - b_round

    question_text = (
        f"**Estimate** the answer to {a} {op} {b} by rounding each number to the "
        f"nearest {place} first."
    )
    scaffold_steps = [
        {"prompt": f"Round {a} to the nearest {place}", "answer": a_round},
        {"prompt": f"Round {b} to the nearest {place}", "answer": b_round},
    ]
    worked = [
        f"{a} rounds to {a_round}, {b} rounds to {b_round}",
        f"Estimate = {a_round} {op} {b_round} = {answer}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Number Problem Solving",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_number_problem_solving_question():
    return random.choice([
        generate_number_problem_solving_l1,
        generate_number_problem_solving_l2,
        generate_number_problem_solving_l3,
    ])()
