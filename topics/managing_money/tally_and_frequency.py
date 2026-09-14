import random
from core.models.question_model import Question

NOTES = """
**Tally and Frequency Tables:**

1. Go through the raw data one item at a time and add a tally mark (|) to the matching category
   — group tally marks in fives (|||| ) to make them easy to count.
2. Count the tally marks in each row to find the **frequency**.
3. Add all the frequencies to find the **total**.

**Example:** Apple, Pear, Apple, Banana, Apple → Apple: ||| (3), Pear: | (1), Banana: | (1)
"""

_SCENARIOS = [
    {"context": "Shoppers in a supermarket were asked their favourite fruit.",
     "categories": ["Apple", "Banana", "Grape", "Orange", "Strawberry"]},
    {"context": "A children's shoe shop surveyed customers' shoe size over one day.",
     "categories": ["Size 1", "Size 2", "Size 3", "Size 4", "Size 5"]},
    {"context": "The Leisure Centre surveyed pupils' favourite activities.",
     "categories": ["Football", "Swimming", "Gymnastics", "Basketball"]},
    {"context": "A shop selling baguettes recorded what customers bought.",
     "categories": ["Chicken", "Salad", "Tuna", "Beef"]},
    {"context": "A local shop surveyed how many lottery tickets people bought.",
     "categories": ["1", "2", "3", "4", "5"]},
    {"context": "Kiz asked classmates what television programme they prefer.",
     "categories": ["Cartoons", "Films", "Sport", "Soaps"]},
    {"context": "A woodland survey recorded which minibeasts were found.",
     "categories": ["Wood ant", "Woodlice", "Small fly", "Caterpillar", "Slug", "Snail"]},
]


def _build_data(categories, n_items):
    weights = [random.randint(1, 6) for _ in categories]
    data = []
    for _ in range(n_items):
        data.append(random.choices(categories, weights=weights)[0])
    return data


def _format_data_list(data, per_row=5):
    rows = [data[i:i + per_row] for i in range(0, len(data), per_row)]
    return "\n".join("  ".join(rows[r]) for r in range(len(rows)))


def _generate(n_categories_range, n_items_range):
    sc = random.choice(_SCENARIOS)
    categories = sc["categories"][:random.randint(*n_categories_range)] \
        if len(sc["categories"]) > n_categories_range[1] else sc["categories"]
    n_items = random.randint(*n_items_range)
    data = _build_data(categories, n_items)
    # guarantee every category appears at least once
    for cat in categories:
        if cat not in data:
            data[random.randrange(len(data))] = cat

    freq = {cat: data.count(cat) for cat in categories}
    total = sum(freq.values())
    max_cat = max(freq, key=freq.get)
    min_cat = min(freq, key=freq.get)

    focus = random.choice(["most", "least", "difference", "total"])

    if focus == "most":
        question_text = (
            f"{sc['context']} Here are the results:\n\n"
            f"{_format_data_list(data)}\n\n"
            f"Copy and complete a frequency table for this data, then state which category "
            f"was the **most common**.\n\n"
            f"**Enter the frequency of the most common category.**"
        )
        answer = freq[max_cat]
        worked_line = f"Most common: **{max_cat}** with a frequency of {freq[max_cat]}"
    elif focus == "least":
        question_text = (
            f"{sc['context']} Here are the results:\n\n"
            f"{_format_data_list(data)}\n\n"
            f"Copy and complete a frequency table for this data, then state which category "
            f"was the **least common**.\n\n"
            f"**Enter the frequency of the least common category.**"
        )
        answer = freq[min_cat]
        worked_line = f"Least common: **{min_cat}** with a frequency of {freq[min_cat]}"
    elif focus == "difference":
        cat_a, cat_b = random.sample(categories, 2)
        bigger, smaller = (cat_a, cat_b) if freq[cat_a] >= freq[cat_b] else (cat_b, cat_a)
        answer = freq[bigger] - freq[smaller]
        question_text = (
            f"{sc['context']} Here are the results:\n\n"
            f"{_format_data_list(data)}\n\n"
            f"Copy and complete a frequency table for this data.\n\n"
            f"How many more people chose **{bigger}** than **{smaller}**?"
        )
        worked_line = f"{bigger} ({freq[bigger]}) − {smaller} ({freq[smaller]}) = {answer}"
    else:
        answer = total
        question_text = (
            f"{sc['context']} Here are the results:\n\n"
            f"{_format_data_list(data)}\n\n"
            f"Copy and complete a frequency table for this data, then find the **total** "
            f"number surveyed."
        )
        worked_line = "Total = " + " + ".join(str(freq[c]) for c in categories) + f" = {total}"

    worked = (
        ["Frequency table:"]
        + [f"{cat}: {freq[cat]}" for cat in categories]
        + ["", worked_line]
    )

    scaffold_steps = [
        {"prompt": f"Tally the data and find the frequency of '{categories[0]}'", "answer": freq[categories[0]]},
    ]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Managing Money",
        question_type="Tally and Frequency",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_tally_and_frequency_l1():
    return _generate((4, 4), (18, 24))


def generate_tally_and_frequency_l2():
    return _generate((5, 6), (25, 36))


def generate_tally_and_frequency_question():
    return random.choice([
        generate_tally_and_frequency_l1,
        generate_tally_and_frequency_l2,
    ])()
