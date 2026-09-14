import math
import random

from core.models.question_model import Question

NOTES = """
**Probability:**

- **In words:** IMPOSSIBLE (can never happen), UNLIKELY (probably won't happen),
  LIKELY (probably will happen), CERTAIN (will definitely happen).
- **As a fraction:** probability = number of favourable outcomes ÷ total number of
  equally-likely outcomes, written as a fraction in its simplest form.
- **Without replacement:** once an item is removed and *not* put back, there is one fewer
  item overall (and one fewer of that colour/type if it matched), so the fraction for the
  next draw uses the new, smaller totals.
- **From a frequency table:** probability = frequency of the outcome you want ÷ total frequency.

**Example:** A bag has 6 red and 10 green counters (16 total).
- P(red) = 6/16 = **3/8**
- If a red counter is removed and not replaced: P(red again) = 5/15 = **1/3**
"""


def _reduce(num, den):
    g = math.gcd(num, den)
    return num // g, den // g


def _frac_str(num, den):
    n, d = _reduce(num, den)
    if d == 1:
        return str(n)
    return f"{n}/{d}"


# ---------------------------------------------------------------------------
# Level 1 — likelihood in words
# ---------------------------------------------------------------------------

_EVENTS = [
    ("Rolling an ordinary die and getting a 7", "impossible"),
    ("Tossing a fair coin and it landing on heads or tails", "certain"),
    ("It snowing heavily in the Sahara Desert tomorrow", "impossible"),
    ("The sun rising tomorrow morning", "certain"),
    ("Meeting a talking dog on the way to school", "impossible"),
    ("It raining at some point in Scotland this month", "likely"),
    ("Picking a red counter from a bag that only has blue counters", "impossible"),
    ("A fair coin landing on heads 10 times in a row", "unlikely"),
    ("Every pupil in a class being over 200 years old", "impossible"),
    ("The next baby born in the Western Isles being a boy or a girl", "certain"),
    ("Winning the jackpot on a single lottery ticket", "unlikely"),
    ("A dropped slice of toast landing butter-side down", "likely"),
    ("Rolling a die and getting a number from 1 to 6", "certain"),
    ("Getting a head when tossing a coin once", "likely"),
    ("Drawing an ace from a full pack of 52 playing cards", "unlikely"),
    ("The school being open on a normal Tuesday in term time", "likely"),
    ("Picking a black counter from a bag of only white counters", "impossible"),
    ("Choosing a number greater than 0 from the numbers 1 to 6", "certain"),
]

_WORD_BANK = ["IMPOSSIBLE", "UNLIKELY", "LIKELY", "CERTAIN"]


def generate_probability_l1():
    event, answer = random.choice(_EVENTS)

    question_text = (
        f"Choose the word that best describes how likely this event is — "
        f"{', '.join(_WORD_BANK)}.\n\n"
        f"**Event:** {event}\n\n"
        f"**Enter one word.**"
    )
    worked = [f"This event is **{answer.upper()}**."]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=[],
        worked_solution=worked,
        notes=NOTES,
    )


# ---------------------------------------------------------------------------
# Level 2 — probability as a fraction from equally-likely outcomes
# ---------------------------------------------------------------------------

def _dice_question():
    outcome = random.choice(["a 6", "an even number", "an odd number", "a number less than 3",
                              "a number more than 4", "a 1"])
    favourable = {
        "a 6": 1, "an even number": 3, "an odd number": 3,
        "a number less than 3": 2, "a number more than 4": 2, "a 1": 1,
    }[outcome]
    question_text = f"An ordinary six-sided die is rolled. What is the probability of getting {outcome}?"
    answer = _frac_str(favourable, 6)
    worked = [f"P({outcome}) = {favourable}/6 = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=[
            {"prompt": "How many favourable outcomes are there?", "answer": favourable},
            {"prompt": "How many outcomes are there in total?", "answer": 6},
        ],
        worked_solution=worked,
        notes=NOTES,
    )


def _spinner_question():
    n = random.choice([4, 5, 6, 8])
    outcome = random.choice(["an even number", "an odd number", "the number " + str(random.randint(1, n))])
    if outcome.startswith("an even"):
        favourable = n // 2
    elif outcome.startswith("an odd"):
        favourable = n - n // 2
    else:
        favourable = 1
    question_text = (
        f"A spinner has {n} equal sections, numbered 1 to {n}. "
        f"What is the probability the spinner lands on {outcome}?"
    )
    answer = _frac_str(favourable, n)
    worked = [f"P({outcome}) = {favourable}/{n} = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=[
            {"prompt": "How many favourable outcomes are there?", "answer": favourable},
            {"prompt": "How many outcomes are there in total?", "answer": n},
        ],
        worked_solution=worked,
        notes=NOTES,
    )


def _card_question():
    outcome = random.choice(["an ace", "a heart", "a king", "a red card", "a picture card (jack, queen or king)"])
    favourable = {
        "an ace": 4, "a heart": 13, "a king": 4, "a red card": 26,
        "a picture card (jack, queen or king)": 12,
    }[outcome]
    question_text = (
        f"A card is drawn at random from a full, well-shuffled pack of 52 playing cards. "
        f"What is the probability it is {outcome}?"
    )
    answer = _frac_str(favourable, 52)
    worked = [f"P({outcome}) = {favourable}/52 = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=[
            {"prompt": "How many favourable outcomes are there?", "answer": favourable},
            {"prompt": "How many outcomes are there in total?", "answer": 52},
        ],
        worked_solution=worked,
        notes=NOTES,
    )


_COLOURS = ["red", "blue", "green", "yellow", "white", "black"]


def _coloured_items_question():
    n_colours = random.choice([2, 3])
    colours = random.sample(_COLOURS, n_colours)
    counts = [random.randint(2, 12) for _ in colours]
    total = sum(counts)
    idx = random.randrange(len(colours))
    colour, favourable = colours[idx], counts[idx]

    breakdown = ", ".join(f"{c} {col}" for c, col in zip(counts, colours))
    question_text = (
        f"A bag contains {breakdown} counters (all the same shape and size).\n\n"
        f"A counter is picked at random. What is the probability it is {colour}?"
    )
    answer = _frac_str(favourable, total)
    worked = [f"Total counters = {total}", f"P({colour}) = {favourable}/{total} = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=[
            {"prompt": "How many counters are there altogether?", "answer": total},
        ],
        worked_solution=worked,
        notes=NOTES,
    )


_WORDS = ["SUCCESS", "PEPPER", "GEORGE", "PENELOPE", "WOODWORK", "NEEDLEWORK", "BANANA", "STATISTICS"]
_VOWELS = set("AEIOU")


def _letters_question():
    word = random.choice(_WORDS)
    letters = list(word)
    total = len(letters)
    mode = random.choice(["letter", "vowel", "consonant"])

    if mode == "letter":
        letter = random.choice(sorted(set(letters)))
        favourable = letters.count(letter)
        outcome = f"the letter {letter}"
    elif mode == "vowel":
        favourable = sum(1 for c in letters if c in _VOWELS)
        outcome = "a vowel (A, E, I, O, U)"
    else:
        favourable = sum(1 for c in letters if c not in _VOWELS)
        outcome = "a consonant"

    question_text = (
        f"A letter is chosen at random from the word {word}. "
        f"What is the probability it is {outcome}?"
    )
    answer = _frac_str(favourable, total)
    worked = [f"'{word}' has {total} letters; {favourable} match {outcome}",
              f"P({outcome}) = {favourable}/{total} = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=[
            {"prompt": f"How many letters are there in total in '{word}'?", "answer": total},
        ],
        worked_solution=worked,
        notes=NOTES,
    )


def generate_probability_l2():
    return random.choice([
        _dice_question,
        _spinner_question,
        _card_question,
        _coloured_items_question,
        _letters_question,
    ])()


# ---------------------------------------------------------------------------
# Level 3 — without-replacement (two-step), and probability from a
# frequency table
# ---------------------------------------------------------------------------

def _without_replacement_question():
    colour_a, colour_b = random.sample(_COLOURS, 2)
    count_a = random.randint(2, 12)
    count_b = random.randint(2, 12)
    total = count_a + count_b

    first = _frac_str(count_a, total)
    second = _frac_str(count_a - 1, total - 1)

    question_text = (
        f"A bag contains {count_a} {colour_a} counters and {count_b} {colour_b} counters.\n\n"
        f"**(a)** If a counter is removed at random, what is the probability that it is "
        f"{colour_a}?\n\n"
        f"**(b)** If that counter is {colour_a} and it is **not replaced**, what is the "
        f"probability that the next counter picked is also {colour_a}?\n\n"
        f"**Enter your answer for part (b).**"
    )
    scaffold_steps = [
        {"prompt": f"How many counters are there altogether before anything is removed?",
         "answer": total},
    ]
    worked = [
        f"(a) P({colour_a}) = {count_a}/{total} = {first}",
        f"(b) After removing one {colour_a} counter: {count_a - 1} {colour_a} left out of "
        f"{total - 1} counters altogether",
        f"P({colour_a} again) = {count_a - 1}/{total - 1} = {second}",
    ]

    return Question(
        question_text=question_text,
        correct_answer=second,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


_TABLE_CONTEXTS = [
    {"context": "The pupils in a class were asked how many times they visited the library last term.",
     "label": "visits"},
    {"context": "A group of pupils were asked how many pets they own.",
     "label": "pets"},
    {"context": "Customers at a cafe were asked how many cups of tea they had last week.",
     "label": "cups"},
]


def _frequency_table_question():
    ctx = random.choice(_TABLE_CONTEXTS)
    values = list(range(1, random.choice([5, 6])))
    freqs = [random.randint(2, 15) for _ in values]
    total = sum(freqs)

    table_lines = "\n".join(f"| {v} | {f} |" for v, f in zip(values, freqs))
    table_md = f"| {ctx['label'].capitalize()} | Frequency |\n|---|---|\n{table_lines}"

    mode = random.choice(["exact", "less_than", "more_than"])
    if mode == "exact":
        v = random.choice(values)
        favourable = freqs[values.index(v)]
        question_text = (
            f"{ctx['context']} Here are the results:\n\n{table_md}\n\n"
            f"What is the probability that a pupil chosen at random said **{v}**?"
        )
        worked_line = f"P({v}) = {favourable}/{total}"
    elif mode == "less_than":
        v = random.choice(values[1:]) if len(values) > 1 else values[0]
        favourable = sum(f for val, f in zip(values, freqs) if val < v)
        question_text = (
            f"{ctx['context']} Here are the results:\n\n{table_md}\n\n"
            f"What is the probability that a pupil chosen at random said **less than {v}**?"
        )
        worked_line = f"P(less than {v}) = {favourable}/{total}"
    else:
        v = random.choice(values[:-1]) if len(values) > 1 else values[0]
        favourable = sum(f for val, f in zip(values, freqs) if val > v)
        question_text = (
            f"{ctx['context']} Here are the results:\n\n{table_md}\n\n"
            f"What is the probability that a pupil chosen at random said **more than {v}**?"
        )
        worked_line = f"P(more than {v}) = {favourable}/{total}"

    answer = _frac_str(favourable, total)
    scaffold_steps = [
        {"prompt": "How many people were asked altogether (the total frequency)?", "answer": total},
    ]
    worked = [worked_line + f" = {answer}"]

    return Question(
        question_text=question_text,
        correct_answer=answer,
        topic="Numeracy",
        question_type="Probability",
        scaffold_steps=scaffold_steps,
        worked_solution=worked,
        notes=NOTES,
    )


def generate_probability_l3():
    return random.choice([
        _without_replacement_question,
        _frequency_table_question,
    ])()


def generate_probability_question():
    return random.choice([
        generate_probability_l1,
        generate_probability_l2,
        generate_probability_l3,
    ])()
