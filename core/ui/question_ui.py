import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def render_question(question, suffix="default"):
    """Renders the question text, any diagram, and returns the raw text the pupil typed
    into the answer box (not yet checked against the correct answer)."""
    st.subheader(question.question_text)

    diagram = question.metadata.get("diagram")
    if diagram == "bar_chart":
        _render_bar_chart(question.metadata["diagram_params"])
    elif diagram == "pie_chart":
        _render_pie_chart(question.metadata["diagram_params"])
    elif diagram == "line_chart":
        _render_line_chart(question.metadata["diagram_params"])
    elif diagram == "pictograph":
        _render_pictograph(question.metadata["diagram_params"])

    return st.text_input("Your answer", key=f"ans_{question.qid}_{suffix}")


def _render_bar_chart(p):
    """Reused near-verbatim from N5apps' core/ui/question_ui.py, extended to also support
    a single-series chart when group2_data is None/empty (N3's Bar Graphs topic)."""
    categories = p["categories"]
    g1 = p["group1_data"]
    g2 = p.get("group2_data")
    g1_name = p.get("group1_name") or "Series 1"
    g2_name = p.get("group2_name")

    x = np.arange(len(categories))
    fig, ax = plt.subplots(figsize=(9, 5))

    if g2:
        width = 0.38
        ax.bar(x - width / 2, g1, width, label=g1_name, color="#2c3e50")
        ax.bar(x + width / 2, g2, width, label=g2_name, color="#95a5a6")
        max_val = max(max(g1), max(g2))
        ax.legend(loc="upper right")
    else:
        width = 0.6
        ax.bar(x, g1, width, color="#2c3e50")
        max_val = max(g1)

    ax.set_ylim(0, max_val + 5)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_xlabel(p.get("x_label", "Category"), fontsize=11)
    ax.set_ylabel(p.get("y_label", "Frequency"), fontsize=11)
    ax.set_title(p.get("title", "Bar Chart"), fontsize=13, fontweight="bold")
    ax.yaxis.set_major_locator(plt.MultipleLocator(max(1, (max_val + 5) // 10)))
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)


def _text_color_for(hex_color):
    """White text on a dark wedge, black text on a light one (perceived-luminance threshold)."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "black" if luminance > 140 else "white"


def _render_pie_chart(p):
    """Reused near-verbatim from N5apps' core/ui/question_ui.py. `categories`/`angles`
    define the wedges (need not sum exactly to 360 — matplotlib normalises them);
    `wedge_labels` (one per category, defaults to "<angle>°", pass "?" for a missing/
    target sector); `colors` optional; `show_legend` draws a colour-swatch key instead of
    on-wedge category names."""
    categories = p["categories"]
    angles = p["angles"]
    wedge_labels = p.get("wedge_labels", [f"{a}°" for a in angles])
    colors = p.get("colors") or (
        ["#3498db", "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c"] * (len(categories) // 6 + 1)
    )[:len(categories)]
    caption = p.get("caption", "")
    show_legend = p.get("show_legend", False)

    fig, ax = plt.subplots(figsize=(8.5, 5) if show_legend else (7, 5))
    wedges, _ = ax.pie(
        angles,
        labels=categories if p.get("show_labels", not show_legend) else None,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )

    if show_legend:
        ax.legend(wedges, categories, loc="center left", bbox_to_anchor=(1.02, 0.5),
                   frameon=False, fontsize=11)

    for wedge, label, color in zip(wedges, wedge_labels, colors):
        if not label:
            continue
        theta = np.radians((wedge.theta1 + wedge.theta2) / 2)
        r = 0.6
        ax.text(r * np.cos(theta), r * np.sin(theta), label,
                ha="center", va="center", fontsize=10, fontweight="bold",
                color=_text_color_for(color))

    if caption:
        ax.set_title(caption, fontsize=10, pad=12)
    fig.patch.set_facecolor("white")
    if show_legend:
        plt.tight_layout(rect=[0, 0, 0.72, 1])
    else:
        plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)


def _render_line_chart(p):
    """New renderer, same code style/parameter shape as `_render_bar_chart`: a matplotlib
    line plot with markers. `x_values`/`y_values` are the plotted points (x_values may be
    numeric or category labels); `x_label`, `y_label`, `title` as usual."""
    x_values = p["x_values"]
    y_values = p["y_values"]

    x = np.arange(len(x_values))
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(x, y_values, color="#2c3e50", linewidth=2.2, marker="o", markersize=7,
            markerfacecolor="#e74c3c", markeredgecolor="#2c3e50")

    ax.set_xticks(x)
    ax.set_xticklabels(x_values)
    ax.set_xlabel(p.get("x_label", "x"), fontsize=11)
    ax.set_ylabel(p.get("y_label", "y"), fontsize=11)
    ax.set_title(p.get("title", "Line Graph"), fontsize=13, fontweight="bold")
    y_min = min(y_values)
    y_max = max(y_values)
    pad = max(1, (y_max - y_min) * 0.15)
    ax.set_ylim(y_min - pad, y_max + pad)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)


def _render_pictograph(p):
    """New renderer: an honest pictogram — one row per category, filled with repeated icon
    markers (a whole marker per full unit, a faded half-marker for a half unit), not a bar
    reskinned as icons. `categories`/`values` as usual; `unit_value` = how many items one
    icon represents (labelled in the title as "1 symbol = N <icon_label>"); `icon_label` is
    the plural noun shown in that caption."""
    categories = p["categories"]
    values = p["values"]
    unit_value = p["unit_value"]
    icon_label = p.get("icon_label", "items")
    title = p.get("title", "Pictograph")

    max_symbols = max(v / unit_value for v in values)
    fig_w = max(6, min(12, 1.5 + max_symbols * 0.7))
    fig, ax = plt.subplots(figsize=(fig_w, 0.7 * len(categories) + 1.5))

    for row, (cat, val) in enumerate(zip(categories, values)):
        y = len(categories) - row
        whole = int(val // unit_value)
        half = 1 if (val % unit_value) else 0
        for i in range(whole):
            ax.scatter(i + 0.5, y, s=260, marker="o", color="#2c3e50", zorder=3)
        if half:
            ax.scatter(whole + 0.5, y, s=260, marker="o", color="#2c3e50", alpha=0.35, zorder=3)
        ax.text(-0.3, y, cat, ha="right", va="center", fontsize=11, fontweight="bold")

    ax.set_xlim(-max(2.5, max_symbols * 0.35), max_symbols + 1)
    ax.set_ylim(0.3, len(categories) + 0.7)
    ax.axis("off")
    ax.set_title(f"{title}\n(1 symbol = {unit_value} {icon_label})", fontsize=12, fontweight="bold")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)
