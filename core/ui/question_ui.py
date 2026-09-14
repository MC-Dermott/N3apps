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
    elif diagram == "graduated_scale":
        _render_graduated_scale(question.metadata["diagram_params"])
    elif diagram == "timetable":
        _render_timetable(question.metadata["diagram_params"])
    elif diagram == "rect_shape":
        _render_rect_shape(question.metadata["diagram_params"])
    elif diagram == "triangle":
        _render_triangle(question.metadata["diagram_params"])
    elif diagram == "cuboid":
        _render_cuboid(question.metadata["diagram_params"])
    elif diagram == "street_map":
        _render_street_map(question.metadata["diagram_params"])

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


def _scale_label(v):
    """Fixed-point tick label — never scientific notation."""
    if float(v).is_integer():
        return str(int(v))
    return f"{v:.2f}".rstrip("0").rstrip(".")


def _render_graduated_scale(p):
    """New renderer for Numeracy's Reading Scales topic: a generic "graduated scale with a
    marker" that covers three physical widgets with one function, parameterised by `style`:
    - 'ruler'       — a horizontal number-line/ruler with labelled major ticks (+ optional
                      unlabelled minor ticks) and a red arrow pointing at `marker_value`.
    - 'container'   — a vertical rectangle outline (a measuring jug/cylinder) with a
                      graduated scale down the side and a shaded blue fill level.
    - 'thermometer' — the same vertical fill idea as 'container', narrower and red-filled,
                      and happy to run with a negative `min_value`.
    Required params: min_value, max_value, major_step, marker_value. Optional: minor_step
    (finer unlabelled ticks), unit_label, title."""
    style = p.get("style", "ruler")
    lo = p["min_value"]
    hi = p["max_value"]
    major = p["major_step"]
    minor = p.get("minor_step")
    marker = p["marker_value"]
    unit = p.get("unit_label", "")
    title = p.get("title", "")

    majors = np.arange(lo, hi + major / 2, major)

    if style == "ruler":
        fig, ax = plt.subplots(figsize=(9, 2.6))
        ax.hlines(0, lo, hi, color="#2c3e50", linewidth=2.5)
        for m in majors:
            ax.vlines(m, -0.14, 0.14, color="#2c3e50", linewidth=2)
            ax.text(m, -0.34, _scale_label(m), ha="center", va="top", fontsize=10)
        if minor:
            for mi in np.arange(lo, hi + minor / 2, minor):
                if not any(abs(mi - m) < minor / 4 for m in majors):
                    ax.vlines(mi, -0.07, 0.07, color="#2c3e50", linewidth=1)
        ax.annotate("", xy=(marker, 0.05), xytext=(marker, 0.6),
                    arrowprops=dict(arrowstyle="-|>", color="#e74c3c", linewidth=2.2))
        ax.set_xlim(lo - major * 0.4, hi + major * 0.4)
        ax.set_ylim(-0.6, 0.85)
        ax.axis("off")
        if title:
            ax.set_title(title, fontsize=12, fontweight="bold", pad=8)
        if unit:
            ax.text(hi + major * 0.4, 0, unit, ha="left", va="center", fontsize=10, style="italic")
    else:
        is_thermo = style == "thermometer"
        width = 0.55 if is_thermo else 1.5
        fill_color = "#e74c3c" if is_thermo else "#3498db"
        fig, ax = plt.subplots(figsize=(2.4 if is_thermo else 3.4, 5.6))
        ax.add_patch(plt.Rectangle((-width / 2, lo), width, hi - lo, fill=False,
                                    edgecolor="#2c3e50", linewidth=2.2, zorder=2))
        fill_top = max(lo, min(hi, marker))
        ax.add_patch(plt.Rectangle((-width / 2, lo), width, fill_top - lo,
                                    facecolor=fill_color, alpha=0.55, edgecolor=None, zorder=1))
        for m in majors:
            ax.hlines(m, -width / 2 - 0.16, -width / 2, color="#2c3e50", linewidth=1.6)
            ax.text(-width / 2 - 0.28, m, _scale_label(m), ha="right", va="center", fontsize=9)
        if minor:
            for mi in np.arange(lo, hi + minor / 2, minor):
                if not any(abs(mi - m) < minor / 4 for m in majors):
                    ax.hlines(mi, -width / 2 - 0.08, -width / 2, color="#2c3e50", linewidth=1)
        pad = (hi - lo) * 0.06
        ax.set_xlim(-width / 2 - 1.5, width / 2 + 0.5)
        ax.set_ylim(lo - pad, hi + pad)
        ax.axis("off")
        if title:
            ax.set_title(title, fontsize=12, fontweight="bold", pad=8)
        if unit:
            ax.text(0, hi + pad * 1.6, unit, ha="center", va="bottom", fontsize=10, style="italic")

    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)


def _render_timetable(p):
    """New renderer for Shape, Space & Measures' Timetables topic: a plain matplotlib table
    (rows = stops, columns = services) rather than a chart. `stops` (list), `services` (list
    of column labels), `times` (2D list, `times[service_idx][stop_idx]` as "HH:MM" strings),
    `title` optional."""
    stops = p["stops"]
    services = p["services"]
    times = p["times"]

    header = ["Stop"] + list(services)
    cell_text = [[stops[i]] + [times[j][i] for j in range(len(services))] for i in range(len(stops))]

    n_rows = len(stops) + 1
    n_cols = len(services) + 1
    fig, ax = plt.subplots(figsize=(1.7 * n_cols + 1, 0.55 * n_rows + 1))
    ax.axis("off")
    table = ax.table(cellText=cell_text, colLabels=header, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.9)
    for j in range(n_cols):
        cell = table[0, j]
        cell.set_facecolor("#2c3e50")
        cell.set_text_props(color="white", fontweight="bold")
    for i in range(1, n_rows):
        cell = table[i, 0]
        cell.set_text_props(fontweight="bold")
    ax.set_title(p.get("title", "Timetable"), fontsize=13, fontweight="bold", pad=14)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)


def _render_rect_shape(p):
    """New renderer, shared by Perimeter, Area of Rectangles (diagram level) and Area of
    Composite Shapes: a plain outlined rectilinear polygon with a label (or "?" for an
    unknown/to-be-inferred side) on each edge. `vertices` is a list of (x, y) points in
    order; `edge_labels` has one entry per edge (the edge from vertices[i] to
    vertices[i+1]), each a label string or None to leave that edge unlabelled."""
    vertices = p["vertices"]
    edge_labels = p["edge_labels"]
    title = p.get("title", "")

    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    n = len(vertices)
    cx, cy = sum(xs) / n, sum(ys) / n

    fig, ax = plt.subplots(figsize=(7, 6))
    poly = plt.Polygon(vertices, closed=True, facecolor="#eaf1f8", edgecolor="#2c3e50",
                        linewidth=2.5)
    ax.add_patch(poly)

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        label = edge_labels[i] if i < len(edge_labels) else None
        if not label:
            continue
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = mx - cx, my - cy
        norm = (dx ** 2 + dy ** 2) ** 0.5 or 1
        span = max(max(xs) - min(xs), max(ys) - min(ys)) or 1
        offset = span * 0.09
        ox, oy = mx + dx / norm * offset, my + dy / norm * offset
        color = "#c0392b" if label == "?" else "#2c3e50"
        ax.text(ox, oy, label, ha="center", va="center", fontsize=12, fontweight="bold",
                color=color)

    pad = max(max(xs) - min(xs), max(ys) - min(ys), 1) * 0.22
    ax.set_xlim(min(xs) - pad, max(xs) + pad)
    ax.set_ylim(min(ys) - pad, max(ys) + pad)
    ax.set_aspect("equal")
    ax.axis("off")
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)


def _render_triangle(p):
    """New renderer for Area of Triangles: a filled triangle with the base labelled along
    the bottom and the (possibly oblique) height shown as a dashed perpendicular from the
    apex, with a small right-angle marker at its foot. `base`, `height` (for proportions),
    `base_label`/`height_label` (display strings), `apex_frac` (0-1, how far along the base
    the apex sits — 0 or 1 gives a right-angled triangle)."""
    base = p["base"]
    height = p["height"]
    apex_frac = p.get("apex_frac", 0.5)
    base_label = p.get("base_label", str(base))
    height_label = p.get("height_label", str(height))

    apex_x = base * apex_frac
    A, B, C = (0, 0), (base, 0), (apex_x, height)

    fig, ax = plt.subplots(figsize=(7, 5.5))
    tri = plt.Polygon([A, B, C], closed=True, facecolor="#eaf1f8", edgecolor="#2c3e50",
                       linewidth=2.5)
    ax.add_patch(tri)
    ax.plot([apex_x, apex_x], [0, height], linestyle="--", color="#c0392b", linewidth=1.6)

    if 1e-6 < apex_x < base - 1e-6:
        s = min(base, height) * 0.07
        ax.plot([apex_x - s, apex_x - s, apex_x], [0, s, s], color="#c0392b", linewidth=1.3)

    ax.text(base / 2, -height * 0.14, f"base = {base_label}", ha="center", fontsize=12,
            fontweight="bold")
    ax.text(apex_x + base * 0.03, height / 2, f"height = {height_label}", ha="left",
            fontsize=12, fontweight="bold", color="#c0392b")

    ax.set_xlim(-base * 0.15, base * 1.2)
    ax.set_ylim(-height * 0.28, height * 1.15)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)


def _render_cuboid(p):
    """New renderer for Volume of Cuboids: a simple oblique-projection box (front face +
    parallelogram top/side faces) with length/width/height labelled. `length`, `width`,
    `height` control the drawn proportions; `length_label`/`width_label`/`height_label` are
    the display strings."""
    L = p["length"]
    W = p["width"]
    H = p["height"]
    l_label = p.get("length_label", str(L))
    w_label = p.get("width_label", str(W))
    h_label = p.get("height_label", str(H))

    ox, oy = W * 0.5, W * 0.28

    fig, ax = plt.subplots(figsize=(7, 6))
    front = [(0, 0), (L, 0), (L, H), (0, H)]
    top = [(0, H), (L, H), (L + ox, H + oy), (ox, H + oy)]
    side = [(L, 0), (L + ox, oy), (L + ox, H + oy), (L, H)]

    ax.add_patch(plt.Polygon(side, closed=True, facecolor="#b0cbe8", edgecolor="#2c3e50", linewidth=2))
    ax.add_patch(plt.Polygon(top, closed=True, facecolor="#c3d8ee", edgecolor="#2c3e50", linewidth=2))
    ax.add_patch(plt.Polygon(front, closed=True, facecolor="#dce8f5", edgecolor="#2c3e50", linewidth=2.4))

    ax.text(L / 2, -H * 0.13, f"length = {l_label}", ha="center", fontsize=11.5, fontweight="bold")
    ax.text(L + ox * 1.1, oy + H * 0.12, f"width = {w_label}", ha="left", fontsize=11.5,
            fontweight="bold", rotation=18)
    ax.text(-L * 0.1, H / 2, f"height = {h_label}", ha="right", va="center", fontsize=11.5,
            fontweight="bold")

    ax.set_xlim(-L * 0.35, L + ox + L * 0.4)
    ax.set_ylim(-H * 0.3, H + oy + H * 0.25)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)


def _render_street_map(p):
    """New renderer for Directions: a small grid-style street map. `streets` is a list of
    dicts, one per side-street off a horizontal "Main Street" that the pupil stands on at
    the start (marked X, facing right/east): {"x", "dir" ("up"/"down"), "name", "landmark",
    "length", "has_ext", and if has_ext, "ext_left"/"ext_right"} — a street with `has_ext`
    also gets a short perpendicular T-junction segment drawn at its far end, labelled with
    its own left/right landmarks (used by the two-turn question level)."""
    streets = p["streets"]
    xmax = max(s["x"] for s in streets) + 1

    fig, ax = plt.subplots(figsize=(9, 6.5))
    ax.plot([-0.6, xmax], [0, 0], color="#2c3e50", linewidth=3, zorder=2)
    ax.text(xmax + 0.15, 0, "Main Street", va="center", fontsize=11, fontweight="bold")

    ax.scatter([0], [0], s=160, color="#c0392b", zorder=5)
    ax.text(0, -0.32, "X", ha="center", fontsize=13, fontweight="bold", color="#c0392b")
    ax.annotate("", xy=(0.5, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color="#c0392b", linewidth=2.2))

    for s in streets:
        x = s["x"]
        length = s["length"]
        y_end = length if s["dir"] == "up" else -length
        va = "bottom" if s["dir"] == "up" else "top"
        ax.plot([x, x], [0, y_end], color="#7f8c8d", linewidth=2.2, zorder=1)
        ax.text(x, y_end + (0.13 if s["dir"] == "up" else -0.13), s["landmark"], ha="center",
                va=va, fontsize=9.5, fontweight="bold")
        ax.text(x + 0.07, y_end / 2, s["name"], rotation=90, ha="left", va="center",
                fontsize=9, color="#2c3e50")

        if s.get("has_ext"):
            ext_w = 0.55
            ax.plot([x - ext_w, x + ext_w], [y_end, y_end], color="#7f8c8d", linewidth=2,
                     linestyle="--", zorder=1)
            ax.text(x - ext_w, y_end + (0.13 if s["dir"] == "up" else -0.13), s["ext_left"],
                    ha="center", va=va, fontsize=8.5)
            ax.text(x + ext_w, y_end + (0.13 if s["dir"] == "up" else -0.13), s["ext_right"],
                    ha="center", va=va, fontsize=8.5)

    ups = [s["length"] for s in streets if s["dir"] == "up"]
    downs = [s["length"] for s in streets if s["dir"] == "down"]
    ymax = (max(ups) if ups else 1) + 0.6
    ymin = -((max(downs) if downs else 1) + 0.6)

    ax.set_xlim(-1, xmax + 1.8)
    ax.set_ylim(ymin, ymax)
    ax.axis("off")
    ax.set_title("Street Map", fontsize=13, fontweight="bold")
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    st.pyplot(fig, width="content")
    plt.close(fig)
