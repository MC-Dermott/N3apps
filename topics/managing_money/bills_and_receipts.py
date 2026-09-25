import random
from core.models import bar_model as bm
from core.models.question_model import Question

NOTES = """
**Bills and Receipts:**

- A **till receipt total** is the sum of every item's price.
- A **bill** often has a fixed **standing charge** plus a **usage cost** — add them together.
- A **VAT-inclusive total** = price before VAT + VAT amount.
- A **discount** is subtracted from the original price.
- **Cost plus postage** = item cost + postage cost.

**Example:** A gas bill has a standing charge of £15.60 and a cost of units used of £39.58.
- Total = £15.60 + £39.58 = **£55.18**
"""

_SHOPS = ["Safeco", "Asdabury", "Sainsco", "Morrigan's", "Cooper's Corner", "Village Stores"]

_ITEMS = [
    "Bread", "Milk", "Yoghurt", "Digestives", "Potatoes", "Bleach", "Paper Hankies",
    "Crisps", "Corn Flakes", "Jam", "Tomato Soup", "Bacon", "Smoked Ham", "Soap Powder",
    "Newspaper", "Fun Size Chocolate", "Coffee", "Toilet Rolls", "Fruit Juice",
    "Apples", "Bananas", "Ribena", "Cheese", "Butter", "Eggs", "Tea Bags", "Pasta",
    "Rice", "Baked Beans", "Orange Squash",
]

_BILL_COMPANIES = [
    ("gas", "Northern Gas Company"), ("electricity", "Bright Electric Company"),
    ("water", "Isles Water Board"), ("mobile phone", "Mobile Phone Company"),
    ("broadband", "Clearline Broadband"),
]

_SHOP_ITEMS = [
    "jacket", "pair of trainers", "television", "laptop", "bicycle", "sofa",
    "dining table", "smartphone", "microwave", "vacuum cleaner", "CD player",
    "games console", "watch", "printer",
]


def _money(lo, hi):
    return round(random.uniform(lo, hi), 2)


# ---------------------------------------------------------------------------
# Level 1 — till receipt totals
# ---------------------------------------------------------------------------

def generate_bills_and_receipts_l1():
    shop = random.choice(_SHOPS)
    n_items = random.randint(4, 7)
    items = random.sample(_ITEMS, n_items)
    prices = [_money(0.29, 6.50) for _ in items]
    total = round(sum(prices), 2)

    lines = "\n".join(f"- {item}: £{price:,.2f}" for item, price in zip(items, prices))

    question_text = (
        f"Here is a copy of {shop}'s till receipt.\n\n"
        f"{lines}\n\n"
        f"Find the **TOTAL** of the receipt."
    )

    worked = [
        "Total = " + " + ".join(f"£{p:,.2f}" for p in prices) + f" = £{total:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=total,
        topic="Managing Money",
        question_type="Bills and Receipts",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "receipt_adder",
            "scaffold_widget_params": {"items": list(zip(items, prices))},
        },
    )


# ---------------------------------------------------------------------------
# Level 2 — mixed simple bills: standing charge + usage / discount / postage
# ---------------------------------------------------------------------------

def _standing_charge_question():
    kind, company = random.choice(_BILL_COMPANIES)
    standing = _money(8, 30)
    usage = _money(15, 70)
    total = round(standing + usage, 2)

    question_text = (
        f"Here is {company}'s {kind} bill.\n\n"
        f"- Standing Charge: £{standing:,.2f}\n"
        f"- Cost of Units Used: £{usage:,.2f}\n\n"
        f"Find the total cost of the bill."
    )
    worked = [f"Total = £{standing:,.2f} + £{usage:,.2f} = £{total:,.2f}"]

    return Question(
        question_text=question_text,
        correct_answer=total,
        topic="Managing Money",
        question_type="Bills and Receipts",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "receipt_adder",
            "scaffold_widget_params": {"items": [("Standing Charge", standing), ("Cost of Units Used", usage)]},
            "bar_model": bm.bar_model([
                bm.part_whole("Total bill", bm.unknown("Total bill", total),
                              [bm.given("Standing Charge", standing), bm.given("Units Used", usage)]),
            ], prefix="£", dp=2),
        },
    )


def _discount_subtraction_question():
    item = random.choice(_SHOP_ITEMS)
    original = _money(15, 400)
    discount = round(random.uniform(2, min(original - 2, 90)), 2)
    sale = round(original - discount, 2)

    question_text = (
        f"A {item} usually costs £{original:,.2f}.\n\n"
        f"A discount of £{discount:,.2f} is being offered.\n\n"
        f"How much will the {item} now cost?"
    )
    worked = [f"New price = £{original:,.2f} − £{discount:,.2f} = £{sale:,.2f}"]

    return Question(
        question_text=question_text,
        correct_answer=sale,
        topic="Managing Money",
        question_type="Bills and Receipts",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "receipt_adder",
            "scaffold_widget_params": {"items": [("Original price", original), ("Discount", discount)], "op": "-"},
            "bar_model": bm.bar_model([
                bm.part_whole("New price", bm.given("Usual price", original),
                              [bm.unknown("New price", sale), bm.given("Discount", discount)]),
            ], prefix="£", dp=2),
        },
    )


def _postage_question():
    item = random.choice(["gardening book", "cookery book", "jigsaw puzzle", "board game",
                           "jumper", "pair of boots", "toy set", "picture frame"])
    cost = _money(4, 60)
    postage = _money(1.50, 6.50)
    total = round(cost + postage, 2)

    question_text = (
        f"An order for a {item} costs £{cost:,.2f} plus £{postage:,.2f} for postage.\n\n"
        f"How much will the order cost altogether?"
    )
    worked = [f"Total = £{cost:,.2f} + £{postage:,.2f} = £{total:,.2f}"]

    return Question(
        question_text=question_text,
        correct_answer=total,
        topic="Managing Money",
        question_type="Bills and Receipts",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "receipt_adder",
            "scaffold_widget_params": {"items": [("Item cost", cost), ("Postage", postage)]},
            "bar_model": bm.bar_model([
                bm.part_whole("Total cost", bm.unknown("Total", total),
                              [bm.given(item.capitalize(), cost), bm.given("Postage", postage)]),
            ], prefix="£", dp=2),
        },
    )


def generate_bills_and_receipts_l2():
    return random.choice([
        _standing_charge_question,
        _discount_subtraction_question,
        _postage_question,
    ])()


# ---------------------------------------------------------------------------
# Level 3 — VAT-inclusive totals (multi-step)
# ---------------------------------------------------------------------------

def generate_bills_and_receipts_l3():
    kind, company = random.choice(_BILL_COMPANIES)
    cost = _money(20, 500)
    vat_rate = random.choice([5, 20])
    vat = round(cost * vat_rate / 100, 2)
    total = round(cost + vat, 2)

    question_text = (
        f"{company}'s bill shows a cost of £{cost:,.2f} before VAT.\n\n"
        f"VAT is charged at {vat_rate}%.\n\n"
        f"Calculate the total amount to be paid, including VAT."
    )

    scaffold_steps = [
        {"prompt": f"Calculate {vat_rate}% of £{cost:,.2f} to find the VAT", "answer": vat},
        {"prompt": "Add the VAT to the cost before VAT to find the total", "answer": total},
    ]

    worked = [
        f"VAT = {vat_rate}% of £{cost:,.2f} = £{vat:,.2f}",
        f"Total = £{cost:,.2f} + £{vat:,.2f} = £{total:,.2f}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=total,
        topic="Managing Money",
        question_type="Bills and Receipts",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
        metadata={
            "scaffold_widget": "receipt_adder",
            "scaffold_widget_params": {"items": [("Cost before VAT", cost), ("VAT", vat)]},
            "bar_model": bm.bar_model([
                bm.percent("Find the VAT", bm.given("Cost before VAT", cost), vat_rate,
                           bm.unknown("VAT", vat)),
                bm.part_whole("Total to pay", bm.unknown("Total", total),
                              [bm.carried("Cost before VAT", cost), bm.carried("VAT", vat)]),
            ], prefix="£", dp=2),
        },
    )


def generate_bills_and_receipts_question():
    return random.choice([
        generate_bills_and_receipts_l1,
        generate_bills_and_receipts_l2,
        generate_bills_and_receipts_l3,
    ])()
