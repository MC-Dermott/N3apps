import random

from core.models.question_model import Question

NOTES = """
**Fraction Word Problems:**

- Work out the fraction of the amount first (see "Fraction of an Amount"), then answer what
  the question actually asks — the fraction itself is often only the first step.
- **"How much is left / how many remain"**: whole amount − the fraction you just found.
- **Time:** there are 60 minutes in an hour, so a fraction of an hour = fraction × 60.
- **Angles:** there are 90° in a right angle, so a fraction of a right angle = fraction × 90.

**Example:** A class has 30 pupils. 3/10 are absent.
- Absent = 3/10 of 30 = 9
- Present = 30 − 9 = **21**
"""

_NAMES = [
    "Alex", "Shona", "Miriam", "Mark", "Angela", "Mary", "Emma", "Kevin",
    "Sally", "Jane", "Deborah", "Fiona", "Callum", "Iona", "Murdo", "Effie",
    "Donald", "Morag", "Neil", "Katie",
]

_MONEY_FRACTIONS = [(1, 2), (1, 4), (1, 5), (1, 10), (3, 4), (2, 5)]
_QUANTITY_FRACTIONS = [(1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 10), (1, 3), (2, 3)]


def _amount_for_denom(denom, lo_mult, hi_mult):
    return denom * random.randint(lo_mult, hi_mult)


# ---------------------------------------------------------------------------
# Level 1 — single fraction-of-quantity word problems
# ---------------------------------------------------------------------------

def _time_question():
    num, denom = random.choice([(1, 2), (1, 4), (3, 4), (1, 3), (2, 3), (1, 6), (5, 6)])
    minutes = num * 60 // denom
    question_text = f"There are 60 minutes in an hour. How many minutes are there in {num}/{denom} of an hour?"
    worked = [f"{num}/{denom} of 60 = 60 ÷ {denom} × {num} = {minutes} minutes"]

    return Question(
        question_text=question_text,
        correct_answer=minutes,
        topic="Numeracy",
        question_type="Fraction Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "fraction_bar",
            "scaffold_widget_params": {"amount": 60, "denom": denom, "num": num, "unit": "min", "two_step": False},
        },
    )


def _angle_question():
    # denominators must divide 90 evenly (90 = 2 x 3^2 x 5)
    num, denom = random.choice([(1, 2), (1, 3), (2, 3), (1, 5), (2, 5), (3, 5), (4, 5),
                                 (1, 6), (5, 6), (1, 9), (2, 9), (1, 10), (3, 10)])
    angle = num * 90 // denom
    question_text = f"There are 90° in a right angle. How many degrees are in {num}/{denom} of a right angle?"
    worked = [f"{num}/{denom} of 90° = 90° ÷ {denom} × {num} = {angle}°"]

    return Question(
        question_text=question_text,
        correct_answer=angle,
        topic="Numeracy",
        question_type="Fraction Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "fraction_bar",
            "scaffold_widget_params": {"amount": 90, "denom": denom, "num": num, "unit": "°", "two_step": False},
        },
    )


def _prize_money_question():
    name = random.choice(_NAMES)
    num, denom = random.choice(_MONEY_FRACTIONS)
    amount = _amount_for_denom(denom, 5, 60)
    answer = amount // denom * num

    question_text = f"{name} gets {num}/{denom} of £{amount} as a prize. How much money do they get?"
    worked = [f"{num}/{denom} of £{amount} = £{amount} ÷ {denom} × {num} = £{answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Fraction Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "fraction_bar",
            "scaffold_widget_params": {"amount": amount, "denom": denom, "num": num, "unit": "", "two_step": False},
        },
    )


def generate_fraction_word_problems_l1():
    return random.choice([
        _time_question,
        _angle_question,
        _prize_money_question,
    ])()


# ---------------------------------------------------------------------------
# Level 2 — two-step problems: find the fraction, then what's left/present
# ---------------------------------------------------------------------------

def _owes_money_question():
    name1, name2 = random.sample(_NAMES, 2)
    num, denom = random.choice(_MONEY_FRACTIONS)
    total = _amount_for_denom(denom, 4, 40)
    owed = total // denom * num
    left = total - owed

    question_text = (
        f"{name1} has {total}p, but owes {num}/{denom} of it to {name2}.\n\n"
        f"**(a)** How much does {name1} owe {name2}?\n\n"
        f"**(b)** How much does {name1} have left?\n\n"
        f"**Enter your answer for part (b).**"
    )
    scaffold_steps = [
        {"prompt": f"Find {num}/{denom} of {total}p (how much is owed)", "answer": owed},
    ]
    worked = [
        f"(a) {num}/{denom} of {total}p = {total}p ÷ {denom} × {num} = {owed}p",
        f"(b) Left = {total}p − {owed}p = {left}p",
    ]

    return Question(
        question_text=question_text,
        correct_answer=left,
        topic="Numeracy",
        question_type="Fraction Word Problems",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "fraction_bar",
            "scaffold_widget_params": {"amount": total, "denom": denom, "num": num, "unit": "p", "two_step": True},
        },
    )


def _class_absent_question():
    num, denom = random.choice(_QUANTITY_FRACTIONS)
    class_size = _amount_for_denom(denom, 3, 12)
    absent = class_size // denom * num
    present = class_size - absent

    question_text = (
        f"{num}/{denom} of a class of {class_size} pupils are absent.\n\n"
        f"**(a)** How many are absent?\n\n"
        f"**(b)** How many are present?\n\n"
        f"**Enter your answer for part (b).**"
    )
    scaffold_steps = [
        {"prompt": f"Find {num}/{denom} of {class_size} (how many are absent)", "answer": absent},
    ]
    worked = [
        f"(a) {num}/{denom} of {class_size} = {class_size} ÷ {denom} × {num} = {absent}",
        f"(b) Present = {class_size} − {absent} = {present}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=present,
        topic="Numeracy",
        question_type="Fraction Word Problems",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "fraction_bar",
            "scaffold_widget_params": {
                "amount": class_size, "denom": denom, "num": num, "unit": "pupils", "two_step": True,
            },
        },
    )


def _tank_used_question():
    num, denom = random.choice(_QUANTITY_FRACTIONS)
    capacity = _amount_for_denom(denom, 20, 120)
    remaining_fraction_num = denom - num
    used = capacity // denom * num
    remaining = capacity - used

    question_text = (
        f"A tank holds {capacity} litres of oil when it is full.\n\n"
        f"If it is now {remaining_fraction_num}/{denom} full, how many litres have been used?"
    )
    scaffold_steps = [
        {"prompt": f"Find how many litres are currently in the tank "
                    f"({remaining_fraction_num}/{denom} of {capacity})", "answer": remaining},
    ]
    worked = [
        f"Litres remaining = {remaining_fraction_num}/{denom} of {capacity} = {remaining} litres",
        f"Litres used = {capacity} − {remaining} = {used} litres",
    ]

    return Question(
        question_text=question_text,
        correct_answer=used,
        topic="Numeracy",
        question_type="Fraction Word Problems",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "fraction_bar",
            "scaffold_widget_params": {
                "amount": capacity, "denom": denom, "num": remaining_fraction_num,
                "unit": "litres", "two_step": True,
            },
        },
    )


def generate_fraction_word_problems_l2():
    return random.choice([
        _owes_money_question,
        _class_absent_question,
        _tank_used_question,
    ])()


def generate_fraction_word_problems_question():
    return random.choice([
        generate_fraction_word_problems_l1,
        generate_fraction_word_problems_l2,
    ])()
