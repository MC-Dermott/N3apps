import random
from core.models.question_model import Question

NOTES = """
**Gross Pay, Deductions and Net Pay:**

- **Gross Pay** = Basic Pay + Overtime + Bonus
- **Total Deductions** = Income Tax + National Insurance (NI) + Pension
- **Net Pay** = Gross Pay − Total Deductions

**Example:** Basic Pay £340.00, Overtime £62.00, Bonus £15.00, Income Tax £48.00, NI £26.00,
Pension £12.00.
- Gross Pay = £340.00 + £62.00 + £15.00 = £417.00
- Total Deductions = £48.00 + £26.00 + £12.00 = £86.00
- Net Pay = £417.00 − £86.00 = **£331.00**
"""

_PEOPLE = [
    ("Mr", "Morton"), ("Mrs", "Nimmo"), ("Miss", "Baxter"), ("Mr", "Wilson"),
    ("Mr", "McGregor"), ("Mrs", "Campbell"), ("Miss", "Stewart"), ("Mr", "Fraser"),
    ("Mrs", "MacDonald"), ("Mr", "Murray"), ("Miss", "Kennedy"), ("Mrs", "Ross"),
    ("Mr", "MacLeod"), ("Mrs", "MacKay"),
]


def _money(lo, hi):
    return round(random.uniform(lo, hi), 2)


def _person():
    return random.choice(_PEOPLE)


# ---------------------------------------------------------------------------
# Level 1 — Gross Pay
# ---------------------------------------------------------------------------

def generate_wages_and_deductions_l1():
    title, surname = _person()
    period = random.choice(["week", "month"])
    if period == "week":
        basic = _money(180, 650)
        overtime = _money(0, 160)
    else:
        basic = _money(900, 2600)
        overtime = _money(0, 400)
    bonus = _money(5, 120) if random.random() < 0.7 else 0.0
    gross = round(basic + overtime + bonus, 2)

    question_text = (
        f"{title} {surname} works a {period}. Their pay is made up of:\n\n"
        f"- Basic Pay: £{basic:,.2f}\n"
        f"- Overtime: £{overtime:,.2f}\n"
        f"- Bonus: £{bonus:,.2f}\n\n"
        f"Calculate {title} {surname}'s **Gross Pay**."
    )

    worked = [
        f"Gross Pay = £{basic:,.2f} + £{overtime:,.2f} + £{bonus:,.2f} = £{gross:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=gross,
        topic="Managing Money",
        question_type="Wages and Deductions",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "wages_and_deductions",
            "scaffold_widget_params": {"kind": "gross", "basic": basic, "overtime": overtime, "bonus": bonus},
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — Total Deductions
# ---------------------------------------------------------------------------

def generate_wages_and_deductions_l2():
    title, surname = _person()
    period = random.choice(["week", "month"])
    if period == "week":
        tax = _money(20, 160)
        ni = _money(5, 60)
    else:
        tax = _money(100, 700)
        ni = _money(30, 260)
    pension = _money(0, 90)
    deductions = round(tax + ni + pension, 2)

    question_text = (
        f"{title} {surname}'s payslip shows the following deductions for the {period}:\n\n"
        f"- Income Tax: £{tax:,.2f}\n"
        f"- National Insurance: £{ni:,.2f}\n"
        f"- Pension: £{pension:,.2f}\n\n"
        f"Calculate {title} {surname}'s **Total Deductions**."
    )

    worked = [
        f"Total Deductions = £{tax:,.2f} + £{ni:,.2f} + £{pension:,.2f} = £{deductions:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=deductions,
        topic="Managing Money",
        question_type="Wages and Deductions",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "wages_and_deductions",
            "scaffold_widget_params": {"kind": "deductions", "tax": tax, "ni": ni, "pension": pension},
        },
    )


# ---------------------------------------------------------------------------
# Level 3 — Full wage slip: Gross Pay, Total Deductions, Net Pay
# ---------------------------------------------------------------------------

def generate_wages_and_deductions_l3():
    title, surname = _person()
    period = random.choice(["week", "month"])
    if period == "week":
        basic = _money(180, 650)
        overtime = _money(0, 160)
        tax = _money(20, 160)
        ni = _money(5, 60)
    else:
        basic = _money(900, 2600)
        overtime = _money(0, 400)
        tax = _money(100, 700)
        ni = _money(30, 260)
    bonus = _money(5, 120) if random.random() < 0.6 else 0.0
    pension = _money(0, 90)

    gross = round(basic + overtime + bonus, 2)
    deductions = round(tax + ni + pension, 2)
    net = round(gross - deductions, 2)

    question_text = (
        f"Here is a copy of {title} {surname}'s {period}ly wage slip.\n\n"
        f"Basic Pay: £{basic:,.2f}   Overtime: £{overtime:,.2f}   Bonus: £{bonus:,.2f}\n\n"
        f"Income Tax: £{tax:,.2f}   NI: £{ni:,.2f}   Pension: £{pension:,.2f}\n\n"
        f"**(a)** Calculate the Gross Pay.\n\n"
        f"**(b)** Calculate the Total Deductions.\n\n"
        f"**(c)** Calculate the Net Pay.\n\n"
        f"**Enter your answer for part (c) — the Net Pay.**"
    )

    scaffold_steps = [
        {"prompt": "Calculate the Gross Pay (Basic Pay + Overtime + Bonus)", "answer": gross},
        {"prompt": "Calculate the Total Deductions (Income Tax + NI + Pension)", "answer": deductions},
    ]

    worked = [
        f"(a) Gross Pay = £{basic:,.2f} + £{overtime:,.2f} + £{bonus:,.2f} = £{gross:,.2f}",
        f"(b) Total Deductions = £{tax:,.2f} + £{ni:,.2f} + £{pension:,.2f} = £{deductions:,.2f}",
        f"(c) Net Pay = £{gross:,.2f} − £{deductions:,.2f} = £{net:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=net,
        topic="Managing Money",
        question_type="Wages and Deductions",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "wages_and_deductions",
            "scaffold_widget_params": {
                "kind": "full", "basic": basic, "overtime": overtime, "bonus": bonus,
                "tax": tax, "ni": ni, "pension": pension,
            },
        },
    )


def generate_wages_and_deductions_question():
    return random.choice([
        generate_wages_and_deductions_l1,
        generate_wages_and_deductions_l2,
        generate_wages_and_deductions_l3,
    ])()
