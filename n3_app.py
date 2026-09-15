import streamlit as st

from core.engine.question_factory import generate_question, get_levels, _N3_TOPICS
from core.engine.session_manager import initialise_session, reset_test
from core.ui.question_ui import render_question
from core.ui.scaffold_ui import render_notes, render_scaffold, render_simulation, render_solution
from core.ui.test_ui import render_test


def _parse_numeric(s):
    s = str(s).strip().replace(",", "").replace("£", "")
    try:
        return float(s)
    except ValueError:
        return None


def _answers_match(user, expected):
    u = _parse_numeric(user)
    e = _parse_numeric(expected)
    if u is not None and e is not None:
        return abs(u - e) < 0.01
    return str(user).strip().lower() == str(expected).strip().lower()


st.set_page_config(page_title="National 3 Maths Practice")

initialise_session()

st.title("National 3 Maths Practice")
st.caption("Applications of Mathematics — National 3")
st.divider()

# --- Unit and topic selection ---
unit = st.selectbox("Choose Unit", list(_N3_TOPICS.keys()))

if st.session_state.get("last_unit") != unit:
    st.session_state.last_unit = unit
    st.session_state.submitted = False
    st.session_state.quiz["current_question"] = None

question_types = list(_N3_TOPICS[unit].keys())
question_type = st.selectbox("Choose Question Type", question_types)

if st.session_state.get("last_question_type") != question_type:
    st.session_state.last_question_type = question_type
    st.session_state.submitted = False
    st.session_state.quiz["current_question"] = None

# --- Level selection ---
levels = get_levels(unit, question_type)
selected_level = None
if levels:
    level_options = ["All Question Types"] + list(levels.keys())
    level_choice = st.selectbox("Choose Level", level_options)
    selected_level = None if level_choice == "All Question Types" else level_choice

if st.session_state.get("last_level") != selected_level:
    st.session_state.last_level = selected_level
    st.session_state.submitted = False
    st.session_state.quiz["current_question"] = None

mode = st.radio("Mode", ["Practice", "Test"], horizontal=True, index=0)

if st.session_state.mode != mode:
    st.session_state.mode = mode
    reset_test()

st.divider()

if mode == "Test":
    render_test(unit, question_type, level=selected_level)
else:
    quiz = st.session_state.quiz

    if st.button("Generate Question"):
        quiz["current_question"] = generate_question(unit, question_type, level=selected_level)
        st.session_state.submitted = False
        st.rerun()

    question = quiz.get("current_question")

    if question:
        render_notes(question)
        user_answer = render_question(question, suffix="main")

        if not st.session_state.submitted:
            render_scaffold(question, suffix="main")
            render_simulation(question)

        if st.button("Submit Answer"):
            st.session_state.submitted = True
            st.rerun()

        if st.session_state.submitted:
            correct = _answers_match(user_answer.strip(), question.correct_answer)
            if correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")
            render_solution(question)
    else:
        st.info("Click **Generate Question** to get started.")
