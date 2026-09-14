import random

from topics.managing_money.wages_and_deductions import (
    generate_wages_and_deductions_question,
    generate_wages_and_deductions_l1,
    generate_wages_and_deductions_l2,
    generate_wages_and_deductions_l3,
)
from topics.managing_money.bills_and_receipts import (
    generate_bills_and_receipts_question,
    generate_bills_and_receipts_l1,
    generate_bills_and_receipts_l2,
    generate_bills_and_receipts_l3,
)
from topics.managing_money.money_word_problems import (
    generate_money_word_problems_question,
    generate_money_word_problems_l1,
    generate_money_word_problems_l2,
    generate_money_word_problems_l3,
)
from topics.managing_money.percentages_non_calculator import (
    generate_percentages_non_calculator_question,
    generate_percentages_non_calculator_l1,
    generate_percentages_non_calculator_l2,
)
from topics.managing_money.percentages_calculator import (
    generate_percentages_calculator_question,
    generate_percentages_calculator_l1,
    generate_percentages_calculator_l2,
)
from topics.managing_money.percentage_increase_decrease import (
    generate_percentage_increase_decrease_question,
    generate_percentage_increase_decrease_l1,
    generate_percentage_increase_decrease_l2,
    generate_percentage_increase_decrease_l3,
)
from topics.managing_money.tally_and_frequency import (
    generate_tally_and_frequency_question,
    generate_tally_and_frequency_l1,
    generate_tally_and_frequency_l2,
)
from topics.managing_money.pictographs import (
    generate_pictographs_question,
    generate_pictographs_l1,
    generate_pictographs_l2,
)
from topics.managing_money.bar_graphs import (
    generate_bar_graphs_question,
    generate_bar_graphs_l1,
    generate_bar_graphs_l2,
)
from topics.managing_money.line_graphs import (
    generate_line_graphs_question,
    generate_line_graphs_l1,
    generate_line_graphs_l2,
)
from topics.managing_money.pie_charts import (
    generate_pie_charts_question,
    generate_pie_charts_l1,
    generate_pie_charts_l2,
)

# ---------------------------------------------------------------------------
# Registry
#
# _N3_TOPICS["<Unit>"]["<Question Type>"] = generate_<type>_question   (dispatcher)
# _N3_LEVELS["<Unit>"]["<Question Type>"] = {"Level label": generate_<type>_lN, ...}
#
# Only "Managing Money" exists so far. A second unit (e.g. "Shape, Space and
# Measures" or "Numeracy") slots in as another top-level key in both dicts.
# ---------------------------------------------------------------------------

_N3_TOPICS = {
    "Managing Money": {
        "Wages and Deductions": generate_wages_and_deductions_question,
        "Bills and Receipts": generate_bills_and_receipts_question,
        "Money Word Problems": generate_money_word_problems_question,
        "Percentages (Non-Calculator)": generate_percentages_non_calculator_question,
        "Percentages (Calculator)": generate_percentages_calculator_question,
        "Percentage Increase/Decrease": generate_percentage_increase_decrease_question,
        "Tally and Frequency": generate_tally_and_frequency_question,
        "Pictographs": generate_pictographs_question,
        "Bar Graphs": generate_bar_graphs_question,
        "Line Graphs": generate_line_graphs_question,
        "Pie Charts": generate_pie_charts_question,
    },
}

_N3_LEVELS = {
    "Managing Money": {
        "Wages and Deductions": {
            "Gross Pay": generate_wages_and_deductions_l1,
            "Total Deductions": generate_wages_and_deductions_l2,
            "Full Wage Slip": generate_wages_and_deductions_l3,
        },
        "Bills and Receipts": {
            "Till Receipt Totals": generate_bills_and_receipts_l1,
            "Bills, Discounts and Postage": generate_bills_and_receipts_l2,
            "VAT-Inclusive Totals": generate_bills_and_receipts_l3,
        },
        "Money Word Problems": {
            "Sharing, Change and Subtraction": generate_money_word_problems_l1,
            "Division Problems": generate_money_word_problems_l2,
            "Two-Step Problems": generate_money_word_problems_l3,
        },
        "Percentages (Non-Calculator)": {
            "Common Percentages": generate_percentages_non_calculator_l1,
            "Word Problems": generate_percentages_non_calculator_l2,
        },
        "Percentages (Calculator)": {
            "Direct Calculation": generate_percentages_calculator_l1,
            "Word Problems": generate_percentages_calculator_l2,
        },
        "Percentage Increase/Decrease": {
            "Single Item": generate_percentage_increase_decrease_l1,
            "Item Table": generate_percentage_increase_decrease_l2,
            "Further Problems": generate_percentage_increase_decrease_l3,
        },
        "Tally and Frequency": {
            "Basic": generate_tally_and_frequency_l1,
            "Extended": generate_tally_and_frequency_l2,
        },
        "Pictographs": {
            "Basic": generate_pictographs_l1,
            "Extended": generate_pictographs_l2,
        },
        "Bar Graphs": {
            "Single Series": generate_bar_graphs_l1,
            "Two Series (Comparison)": generate_bar_graphs_l2,
        },
        "Line Graphs": {
            "Reading Values": generate_line_graphs_l1,
            "Differences": generate_line_graphs_l2,
        },
        "Pie Charts": {
            "Angle to Percentage": generate_pie_charts_l1,
            "Missing Sector": generate_pie_charts_l2,
        },
    },
}


def get_levels(topic, question_type):
    return _N3_LEVELS.get(topic, {}).get(question_type, {})


def generate_question(topic, question_type, level=None):
    if level:
        levels = get_levels(topic, question_type)
        if level in levels:
            return levels[level]()
    return _N3_TOPICS[topic][question_type]()
