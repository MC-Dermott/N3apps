import math
import random
from core.models.question_model import Question

NOTES = """
**Money Word Problems:**

- **Equal sharing:** total ÷ number of people/items
- **Change:** amount paid − cost of items
- **Weight/quantity subtraction:** starting amount − amount used/lost
- **Monthly pay from annual salary:** annual salary ÷ 12
- **How many boxes needed:** total needed ÷ amount per box, **rounded up** to the next whole box
- **Savings needed:** total cost ÷ amount saved each week

**Example:** Kevin needs 252 tiles. Tiles are sold in boxes of 12.
- Boxes needed = 252 ÷ 12 = **21 boxes** (exact, no rounding needed here)
"""

_NAMES = [
    "Alex", "Shona", "Miriam", "Mark", "Angela", "Mary", "Emma", "Kevin",
    "Sally", "Jane", "Deborah", "Fiona", "Callum", "Iona", "Murdo", "Effie",
    "Donald", "Morag", "Neil", "Katie",
]


def _money(lo, hi, step=1):
    cents = random.randrange(int(lo * 100), int(hi * 100) + 1, step)
    return round(cents / 100, 2)


# ---------------------------------------------------------------------------
# Level 1 — single-step problems
# ---------------------------------------------------------------------------

def _equal_sharing_question():
    name1, name2 = random.sample(_NAMES, 2)
    n_people = random.choice([2, 3, 4, 5])
    per_person = random.randint(4, 60)
    total = per_person * n_people

    question_text = (
        f"£{total} is shared equally between {name1} and {n_people - 1} "
        f"other{'s' if n_people - 1 != 1 else ''} ({n_people} people altogether).\n\n"
        f"How much does each person receive?"
    )
    worked = [f"Each share = £{total} ÷ {n_people} = £{per_person}"]

    return Question(
        question_text=question_text,
        correct_answer=per_person,
        topic="Managing Money",
        question_type="Money Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "bar_model_splitter",
            "scaffold_widget_params": {"total": total, "mode": "share", "n": n_people},
        },
    )


def _change_question():
    name = random.choice(_NAMES)
    item = random.choice(["pair of trousers", "jumper", "book", "board game",
                           "pair of shoes", "handbag", "umbrella", "scarf"])
    paid = random.choice([10, 20, 30, 50, 100])
    cost = _money(2, paid - 1)
    change = round(paid - cost, 2)

    question_text = (
        f"{name} has £{paid}.\n\n"
        f"{name} buys a {item} costing £{cost:,.2f}.\n\n"
        f"How much money does {name} have left?"
    )
    worked = [f"Change = £{paid:,.2f} − £{cost:,.2f} = £{change:,.2f}"]

    return Question(
        question_text=question_text,
        correct_answer=change,
        topic="Managing Money",
        question_type="Money Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
    )


def _weight_subtraction_question():
    name = random.choice(_NAMES)
    start = round(random.uniform(55, 100), 1)
    target = round(start - random.uniform(6, 20), 1)
    lost_so_far = round(random.uniform(1.5, 5.5), 1)
    now = round(start - lost_so_far, 1)
    still_to_lose = round(now - target, 1)

    question_text = (
        f"{name} weighs {start} kg when they join a fitness club.\n\n"
        f"Their target weight is {target} kg.\n\n"
        f"After a few weeks, {name} has lost {lost_so_far} kg.\n\n"
        f"**(a)** What is {name}'s weight now?\n\n"
        f"**(b)** How much more does {name} still have to lose to reach their target weight?\n\n"
        f"**Enter your answer for part (b).**"
    )
    scaffold_steps = [
        {"prompt": f"Find {name}'s weight now (starting weight − weight lost)", "answer": now},
    ]
    worked = [
        f"(a) Weight now = {start} − {lost_so_far} = {now} kg",
        f"(b) Still to lose = {now} − {target} = {still_to_lose} kg",
    ]

    return Question(
        question_text=question_text,
        correct_answer=still_to_lose,
        topic="Managing Money",
        question_type="Money Word Problems",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_money_word_problems_l1():
    return random.choice([
        _equal_sharing_question,
        _change_question,
        _weight_subtraction_question,
    ])()


# ---------------------------------------------------------------------------
# Level 2 — division with larger numbers
# ---------------------------------------------------------------------------

def _monthly_pay_question():
    name = random.choice(_NAMES)
    monthly = random.choice(range(900, 4001, 50))
    annual = monthly * 12

    question_text = (
        f"{name} earns £{annual:,} each year.\n\n"
        f"They earn the same amount each month.\n\n"
        f"How much does {name} earn each month?"
    )
    worked = [f"Monthly pay = £{annual:,} ÷ 12 = £{monthly:,}"]

    return Question(
        question_text=question_text,
        correct_answer=monthly,
        topic="Managing Money",
        question_type="Money Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "bar_model_splitter",
            "scaffold_widget_params": {"total": annual, "mode": "share", "n": 12},
        },
    )


def _envelope_sharing_question():
    n_items = random.choice([12, 14, 16, 18, 20, 24])
    per_pupil = random.randint(20, 60)
    total = n_items * per_pupil

    question_text = (
        f"There are {n_items} pupils in a class.\n\n"
        f"They have to address {total} envelopes for a charity appeal.\n\n"
        f"All pupils address the same number of envelopes.\n\n"
        f"How many envelopes will each pupil address?"
    )
    worked = [f"Each pupil addresses {total} ÷ {n_items} = {per_pupil} envelopes"]

    return Question(
        question_text=question_text,
        correct_answer=per_pupil,
        topic="Managing Money",
        question_type="Money Word Problems",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "bar_model_splitter",
            "scaffold_widget_params": {"total": total, "mode": "share", "n": n_items},
        },
    )


def generate_money_word_problems_l2():
    return random.choice([
        _monthly_pay_question,
        _envelope_sharing_question,
    ])()


# ---------------------------------------------------------------------------
# Level 3 — two-step problems (division + multiplication, or round-up division)
# ---------------------------------------------------------------------------

def _boxes_needed_question():
    name = random.choice(_NAMES)
    item = random.choice(["tiles", "bricks", "roof slates", "paving stones", "bottles of juice"])
    per_box = random.choice([6, 8, 10, 12, 15, 20, 24])
    n_boxes_exact = random.randint(8, 30)
    extra = random.choice([0, 0, 0, random.randint(1, per_box - 1)])
    needed = per_box * n_boxes_exact + extra
    boxes = math.ceil(needed / per_box)
    price_per_box = _money(2, 15)
    total_cost = round(boxes * price_per_box, 2)

    question_text = (
        f"{name} needs {needed} {item} altogether. The {item} are sold in boxes of {per_box}.\n\n"
        f"**(a)** How many boxes of {item} will {name} need to buy?\n\n"
        f"Each box costs £{price_per_box:,.2f}.\n\n"
        f"**(b)** How much will the {item} cost?\n\n"
        f"**Enter your answer for part (b).**"
    )
    scaffold_steps = [
        {"prompt": f"Divide {needed} by {per_box} and round up to the next whole box", "answer": boxes},
    ]
    worked = [
        f"(a) {needed} ÷ {per_box} = {needed / per_box:.2f} → round up to {boxes} boxes",
        f"(b) Cost = {boxes} × £{price_per_box:,.2f} = £{total_cost:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=total_cost,
        topic="Managing Money",
        question_type="Money Word Problems",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "bar_model_splitter",
            "scaffold_widget_params": {
                "total": needed, "mode": "group", "n": per_box,
                "multiplier": price_per_box, "multiplier_label": "Cost per box (£)",
            },
        },
    )


def _savings_weeks_question():
    name1, name2 = random.sample(_NAMES, 2)
    item = random.choice(["jacket", "bike", "games console", "phone", "guitar", "watch"])
    weekly1 = random.choice([3.50, 4.00, 5.00, 5.50, 6.50, 7.50, 8.00, 9.75, 10.50])
    n_weeks1 = random.randint(6, 14)
    cost = round(weekly1 * n_weeks1, 2)
    weekly2 = random.choice([4.00, 6.00, 7.50, 9.00, 9.75, 12.00, 15.00])
    weeks2 = math.ceil(cost / weekly2)

    question_text = (
        f"{name1} is saving £{weekly1:,.2f} each week to buy a {item} costing £{cost:,.2f}.\n\n"
        f"**(a)** How many weeks will {name1} need to save to buy the {item}?\n\n"
        f"{name2} can save £{weekly2:,.2f} each week.\n\n"
        f"**(b)** How many weeks will {name2} need to save to buy the {item}?\n\n"
        f"**Enter your answer for part (b).**"
    )
    scaffold_steps = [
        {"prompt": f"How many weeks does {name1} need? (£{cost:,.2f} ÷ £{weekly1:,.2f})", "answer": n_weeks1},
    ]
    worked = [
        f"(a) £{cost:,.2f} ÷ £{weekly1:,.2f} = {n_weeks1} weeks",
        f"(b) £{cost:,.2f} ÷ £{weekly2:,.2f} = {cost / weekly2:.2f} → round up to {weeks2} weeks",
    ]

    return Question(
        question_text=question_text,
        correct_answer=weeks2,
        topic="Managing Money",
        question_type="Money Word Problems",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "bar_model_splitter",
            "scaffold_widget_params": {"total": cost, "mode": "group", "n": weekly2},
        },
    )


def generate_money_word_problems_l3():
    return random.choice([
        _boxes_needed_question,
        _savings_weeks_question,
    ])()


def generate_money_word_problems_question():
    return random.choice([
        generate_money_word_problems_l1,
        generate_money_word_problems_l2,
        generate_money_word_problems_l3,
    ])()
