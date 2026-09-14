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

from topics.numeracy.rounding import (
    generate_rounding_question,
    generate_rounding_l1,
    generate_rounding_l2,
)
from topics.numeracy.number_problem_solving import (
    generate_number_problem_solving_question,
    generate_number_problem_solving_l1,
    generate_number_problem_solving_l2,
    generate_number_problem_solving_l3,
)
from topics.numeracy.decimal_addition_subtraction import (
    generate_decimal_addition_subtraction_question,
    generate_decimal_addition_subtraction_l1,
    generate_decimal_addition_subtraction_l2,
)
from topics.numeracy.decimal_multiplication_division import (
    generate_decimal_multiplication_division_question,
    generate_decimal_multiplication_division_l1,
    generate_decimal_multiplication_division_l2,
)
from topics.numeracy.decimal_word_problems import (
    generate_decimal_word_problems_question,
    generate_decimal_word_problems_l1,
    generate_decimal_word_problems_l2,
)
from topics.numeracy.fraction_of_amount import (
    generate_fraction_of_amount_question,
    generate_fraction_of_amount_l1,
    generate_fraction_of_amount_l2,
)
from topics.numeracy.fraction_word_problems import (
    generate_fraction_word_problems_question,
    generate_fraction_word_problems_l1,
    generate_fraction_word_problems_l2,
)
from topics.numeracy.numeracy_percentages import (
    generate_numeracy_percentages_question,
    generate_numeracy_percentages_l1,
    generate_numeracy_percentages_l2,
    generate_numeracy_percentages_l3,
)
from topics.numeracy.reading_scales import (
    generate_reading_scales_question,
    generate_reading_scales_l1,
    generate_reading_scales_l2,
)
from topics.numeracy.probability import (
    generate_probability_question,
    generate_probability_l1,
    generate_probability_l2,
    generate_probability_l3,
)

from topics.shape_space_and_measures.clock_conversion import (
    generate_clock_conversion_question,
    generate_clock_conversion_l1,
    generate_clock_conversion_l2,
)
from topics.shape_space_and_measures.time_intervals import (
    generate_time_intervals_question,
    generate_time_intervals_l1,
    generate_time_intervals_l2,
    generate_time_intervals_l3,
)
from topics.shape_space_and_measures.timetables import (
    generate_timetables_question,
    generate_timetables_l1,
    generate_timetables_l2,
)
from topics.shape_space_and_measures.perimeter import (
    generate_perimeter_question,
    generate_perimeter_l1,
    generate_perimeter_l2,
)
from topics.shape_space_and_measures.area_rectangles import (
    generate_area_rectangles_question,
    generate_area_rectangles_l1,
    generate_area_rectangles_l2,
)
from topics.shape_space_and_measures.area_triangles import (
    generate_area_triangles_question,
    generate_area_triangles_l1,
    generate_area_triangles_l2,
)
from topics.shape_space_and_measures.area_composite import (
    generate_area_composite_question,
    generate_area_composite_l1,
    generate_area_composite_l2,
)
from topics.shape_space_and_measures.volume_cuboids import (
    generate_volume_cuboids_question,
    generate_volume_cuboids_l1,
    generate_volume_cuboids_l2,
)
from topics.shape_space_and_measures.directions import (
    generate_directions_question,
    generate_directions_l1,
    generate_directions_l2,
)

# ---------------------------------------------------------------------------
# Registry
#
# _N3_TOPICS["<Unit>"]["<Question Type>"] = generate_<type>_question   (dispatcher)
# _N3_LEVELS["<Unit>"]["<Question Type>"] = {"Level label": generate_<type>_lN, ...}
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
    "Numeracy": {
        "Rounding": generate_rounding_question,
        "Number Problem Solving": generate_number_problem_solving_question,
        "Decimal Addition and Subtraction": generate_decimal_addition_subtraction_question,
        "Decimal Multiplication and Division": generate_decimal_multiplication_division_question,
        "Decimal Word Problems": generate_decimal_word_problems_question,
        "Fraction of an Amount": generate_fraction_of_amount_question,
        "Fraction Word Problems": generate_fraction_word_problems_question,
        "Percentages": generate_numeracy_percentages_question,
        "Reading Scales": generate_reading_scales_question,
        "Probability": generate_probability_question,
    },
    "Shape, Space & Measures": {
        "Clock Conversion": generate_clock_conversion_question,
        "Time Intervals": generate_time_intervals_question,
        "Timetables": generate_timetables_question,
        "Perimeter": generate_perimeter_question,
        "Area of Rectangles": generate_area_rectangles_question,
        "Area of Triangles": generate_area_triangles_question,
        "Area of Composite Shapes": generate_area_composite_question,
        "Volume of Cuboids": generate_volume_cuboids_question,
        "Directions": generate_directions_question,
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
    "Numeracy": {
        "Rounding": {
            "Whole Number / Ten / Hundred / Thousand": generate_rounding_l1,
            "Decimal Places": generate_rounding_l2,
        },
        "Number Problem Solving": {
            "Sums, Differences & Evens/Odds": generate_number_problem_solving_l1,
            "Number Sequences": generate_number_problem_solving_l2,
            "Estimating": generate_number_problem_solving_l3,
        },
        "Decimal Addition and Subtraction": {
            "Column Addition/Subtraction": generate_decimal_addition_subtraction_l1,
            "Word Problems": generate_decimal_addition_subtraction_l2,
        },
        "Decimal Multiplication and Division": {
            "By a Single Digit": generate_decimal_multiplication_division_l1,
            "By 10, 100 or 1000": generate_decimal_multiplication_division_l2,
        },
        "Decimal Word Problems": {
            "Total or Difference": generate_decimal_word_problems_l1,
            "Sharing & Multiplying": generate_decimal_word_problems_l2,
        },
        "Fraction of an Amount": {
            "Unit Fraction": generate_fraction_of_amount_l1,
            "Non-Unit Fraction": generate_fraction_of_amount_l2,
        },
        "Fraction Word Problems": {
            "Single-Step Problems": generate_fraction_word_problems_l1,
            "Two-Step Problems": generate_fraction_word_problems_l2,
        },
        "Percentages": {
            "Common Percentages (Non-Calculator)": generate_numeracy_percentages_l1,
            "Any Percentage (Calculator)": generate_numeracy_percentages_l2,
            "VAT & Comparing Offers": generate_numeracy_percentages_l3,
        },
        "Reading Scales": {
            "Ruler, Container & Thermometer": generate_reading_scales_l1,
            "Unit Conversion": generate_reading_scales_l2,
        },
        "Probability": {
            "Likelihood in Words": generate_probability_l1,
            "Probability as a Fraction": generate_probability_l2,
            "Without Replacement & Frequency Tables": generate_probability_l3,
        },
    },
    "Shape, Space & Measures": {
        "Clock Conversion": {
            "On the Hour / Half Hour": generate_clock_conversion_l1,
            "Any Minutes": generate_clock_conversion_l2,
        },
        "Time Intervals": {
            "Whole Hours or Minutes": generate_time_intervals_l1,
            "Hours and Minutes": generate_time_intervals_l2,
            "Word Problems": generate_time_intervals_l3,
        },
        "Timetables": {
            "Reading a Timetable": generate_timetables_l1,
            "Which Service": generate_timetables_l2,
        },
        "Perimeter": {
            "All Sides Given": generate_perimeter_l1,
            "Missing Sides": generate_perimeter_l2,
        },
        "Area of Rectangles": {
            "From a Diagram": generate_area_rectangles_l1,
            "From Given Dimensions": generate_area_rectangles_l2,
        },
        "Area of Triangles": {
            "Whole Numbers": generate_area_triangles_l1,
            "Decimals (Calculator)": generate_area_triangles_l2,
        },
        "Area of Composite Shapes": {
            "Sides Given": generate_area_composite_l1,
            "Missing Sides": generate_area_composite_l2,
        },
        "Volume of Cuboids": {
            "From a Diagram": generate_volume_cuboids_l1,
            "From Given Dimensions": generate_volume_cuboids_l2,
        },
        "Directions": {
            "Single Turn": generate_directions_l1,
            "Two Turns": generate_directions_l2,
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
