import streamlit as st

from core.engine.question_factory import generate_question, get_levels, _N3_TOPICS
from core.engine.session_manager import initialise_session, reset_test
from core.ui.question_ui import render_question
from core.ui.scaffold_ui import render_notes, render_scaffold, render_simulation, render_solution
from core.ui.test_ui import render_test
from core.ui.auth_ui import render_auth, render_change_password
from core.auth.auth import login_as_admin
from core.ui.dashboard_ui import render_dashboard
from core.ui.student_dashboard_ui import render_student_dashboard
from core.db.tracker import save_practice_attempt


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


def _do_logout():
    for key in ["user", "submitted", "last_unit", "last_question_type", "last_level",
                "last_tracked_qid", "show_dashboard", "show_student_dashboard"]:
        st.session_state.pop(key, None)
    reset_test()


def _render_auth_button():
    """Top-right login/logout button, shown on every page."""
    user = st.session_state.get("user")
    if user:
        st.caption(f"**{user['username']}**")
        if st.button("Log out", key="logout_corner"):
            _do_logout()
            st.rerun()
        if st.button("Change password", key="change_pw_corner"):
            st.session_state.show_change_password = True
            st.rerun()


# --- Auth page ---
if st.session_state.get("show_auth"):
    if st.button("← Back"):
        st.session_state.pop("show_auth", None)
        st.rerun()
    render_auth()
    st.stop()

user = st.session_state.get("user")  # None if not logged in

# --- Admin bypass: visiting the app with ?admin_key=<ADMIN_KEY secret> in the URL
# logs you straight in as the configured admin account, skipping the login form. ---
if not user:
    admin_key = st.query_params.get("admin_key")
    if admin_key:
        admin_user = login_as_admin(admin_key)
        if admin_user:
            st.session_state.user = admin_user
            user = admin_user

# --- Login gate: block all access until authenticated ---
if not user:
    render_auth()
    st.stop()

# --- Change password page ---
if st.session_state.get("show_change_password") and user:
    if st.button("← Back"):
        st.session_state.pop("show_change_password", None)
        st.rerun()
    render_change_password(user)
    st.stop()

# --- Student progress dashboard ---
if st.session_state.get("show_student_dashboard"):
    st.title("National 3 Maths Practice")
    col_back, col_corner = st.columns([5, 1])
    with col_back:
        if st.button("← Back"):
            st.session_state.pop("show_student_dashboard", None)
            st.rerun()
    with col_corner:
        _render_auth_button()
    render_student_dashboard(user)
    st.stop()

# --- Teacher dashboard ---
if st.session_state.get("show_dashboard"):
    st.title("National 3 Maths Practice")
    col_back, col_corner = st.columns([5, 1])
    with col_back:
        if st.button("← Back to practice"):
            st.session_state.pop("show_dashboard", None)
            st.rerun()
    with col_corner:
        _render_auth_button()
    render_dashboard()
    st.stop()

col_title, col_corner = st.columns([5, 1])
with col_title:
    st.title("National 3 Maths Practice")
    st.caption("Applications of Mathematics — National 3")
with col_corner:
    _render_auth_button()

if user["role"] == "teacher":
    if st.button("📊 Teacher Dashboard", use_container_width=True):
        st.session_state.show_dashboard = True
        st.rerun()
    st.write("")

if st.button("📈 My Progress", use_container_width=True):
    st.session_state.show_student_dashboard = True
    st.rerun()

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

user_id = user["id"]

if mode == "Test":
    render_test(unit, question_type, level=selected_level, user_id=user_id)
else:
    quiz = st.session_state.quiz

    if st.button("Generate Question"):
        quiz["current_question"] = generate_question(unit, question_type, level=selected_level)
        st.session_state.submitted = False
        st.session_state.pop("last_tracked_qid", None)
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

            if st.session_state.get("last_tracked_qid") != question.qid:
                save_practice_attempt(user_id, "National 3", unit, question_type, correct)
                st.session_state.last_tracked_qid = question.qid

            if correct:
                st.success("✅ Correct!")
            else:
                st.error(f"❌ Incorrect. Correct answer: {question.correct_answer}")
            render_solution(question)
    else:
        st.info("Click **Generate Question** to get started.")
