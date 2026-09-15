import streamlit as st

from core.ui.scaffold_widgets import (
    render_rounding_scaffold,
    render_l_shape_perimeter_scaffold,
    render_time_conversion_scaffold,
)


def _parse_numeric(s):
    s = str(s).strip().replace(",", "").replace("£", "")
    try:
        return float(s)
    except ValueError:
        return None


def _is_correct(user_input, expected):
    student = _parse_numeric(user_input)
    exp = _parse_numeric(expected)
    if student is not None and exp is not None:
        if abs(exp) < 1e-9:
            return abs(student) < 0.01
        if abs(exp) <= 1.0:
            return abs(student - exp) <= 0.005
        return abs(student - exp) / abs(exp) <= 0.02
    return str(user_input).strip().lower() == str(expected).strip().lower()


def render_notes(question):
    if question.notes:
        with st.expander("📚 Notes"):
            st.markdown(question.notes)


def render_scaffold(question, suffix=""):
    if not question.scaffold_steps:
        return
    with st.expander("🔍 Step-by-step scaffold"):
        for i, step in enumerate(question.scaffold_steps):
            st.markdown(f"**Step {i + 1}:** {step['prompt']}")

            inp_key = f"scaf_{question.qid}_{suffix}_{i}_inp"
            chk_key = f"scaf_{question.qid}_{suffix}_{i}_chk"
            ok_key = f"scaf_{question.qid}_{suffix}_{i}_ok"

            col1, col2 = st.columns([3, 1])
            with col1:
                user_val = st.text_input("Answer:", key=inp_key, label_visibility="visible")
            with col2:
                st.write("")
                st.write("")
                if st.button("Check", key=f"scaf_{question.qid}_{suffix}_{i}_btn"):
                    st.session_state[chk_key] = True
                    st.session_state[ok_key] = _is_correct(user_val, step["answer"])

            if st.session_state.get(chk_key):
                if st.session_state.get(ok_key):
                    st.success("✓ Correct!")
                else:
                    st.error("✗ Not quite — check your working and try again.")

            if i < len(question.scaffold_steps) - 1:
                st.divider()


def render_simulation(question):
    """Renders an interactive scaffold tool (from the separate maths-scaffolds project) for
    this question in its own expander, dispatched on metadata["scaffold_widget"] — kept
    separate from metadata["diagram"] (the static picture in the main question view, e.g.
    perimeter's own "rect_shape" drawing), since a question can have both at once."""
    widget = question.metadata.get("scaffold_widget")
    if not widget:
        return
    params = question.metadata.get("scaffold_widget_params", {})
    with st.expander("🎮 Interactive scaffold"):
        if widget == "rounding":
            render_rounding_scaffold(**params)
        elif widget == "l_shape_perimeter":
            render_l_shape_perimeter_scaffold(**params)
        elif widget == "time_conversion":
            render_time_conversion_scaffold(**params)


def render_solution(question):
    st.markdown("**Worked Solution:**")
    for line in question.worked_solution:
        if line == "":
            st.markdown("&nbsp;")
        else:
            st.markdown(f"- {line}")
