# N3apps

A Streamlit app that generates randomised practice questions for Scottish **National 3**
Applications of Mathematics, with step-by-step scaffolds and worked solutions.

Companion app to [N5apps](https://github.com/MC-Dermott/N5apps), which covers National 4/5/Higher
but has no National 3 support — this is N3's own app, mirroring N5apps' architecture (see
`core/engine/question_factory.py` for the registry pattern).

## Status

First version — one unit built so far:

- **Managing Money**: Wages and Deductions, Bills and Receipts, Money Word Problems,
  Percentages (Non-Calculator), Percentages (Calculator), Percentage Increase/Decrease,
  Tally and Frequency, Pictographs, Bar Graphs, Line Graphs, Pie Charts.

Two further National 3 units — Shape, Space & Measures, and Numeracy — are not built yet. The
registry in `core/engine/question_factory.py` is structured so a second unit package
(`topics/<new_unit>/`) slots in alongside `topics/managing_money/` without changing `n3_app.py`.

Login, signup, student progress tracking and a teacher dashboard are wired up — same
Supabase-backed structure as N5apps/N5physics (`core/auth/`, `core/db/`, `core/ui/auth_ui.py`,
`core/ui/dashboard_ui.py`, `core/ui/student_dashboard_ui.py`). N3apps shares its Supabase
project with N5apps (both maths — see `core/db/tracker.py`'s `SUBJECT` constant), so a
student uses the same login on both apps and a teacher can manage both from either app's
dashboard. N5physics has its own separate project (different subject).

## Running it

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/streamlit run n3_app.py
```

### Auth setup

1. Create a Supabase project for N3apps and run `supabase_schema.sql` against it in the
   Supabase SQL Editor.
2. Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in
   `SUPABASE_URL`, `SUPABASE_KEY`, and a `TEACHER_CODE` (the signup code that grants the
   teacher role — give it to teachers only). `ADMIN_KEY`/`ADMIN_USERNAME` are optional.
3. `.streamlit/secrets.toml` is gitignored — never commit real credentials.

## Adding a new topic / question type

Same contract as N5apps:

1. Write `topics/<unit_package>/<type_snake_case>.py`: a module-level `NOTES` markdown
   constant, module-level scenario/context lists for randomisation (plain
   `random.choice`/`randint`, never seeded), one `generate_<type>_l1()`/`_l2()`/`_l3()` per
   difficulty tier — each builds `question_text`, `scaffold_steps`, `worked_solution` and
   returns a `core.models.question_model.Question` — plus a `generate_<type>_question()`
   dispatcher (`random.choice([...])()` across the levels).
2. In `core/engine/question_factory.py`: import the new generator(s), add
   `_N3_TOPICS["<Unit>"]["<Question Type>"] = generate_<type>_question`, and (if more than
   one level) `_N3_LEVELS["<Unit>"]["<Question Type>"] = {"Level label": generate_<type>_lN, ...}`.
3. Every generated question should include `scaffold_steps` except genuinely single-step
   calculations.
4. For word problems (sharing, change, differences, parts of a total, percentages of an
   amount), add a bar model with `metadata["bar_model"] = bar_model.bar_model([...])`
   using the builders in `core/models/bar_model.py`. It shows in its own "📊 Bar
   model" expander alongside any `scaffold_widget`.
5. For chart-based question types, reuse `core/ui/question_ui.py`'s `_render_bar_chart` /
   `_render_pie_chart` / `_render_line_chart` / `_render_pictograph` where the mechanism
   matches, rather than building a new renderer — wire `metadata["diagram"]` /
   `metadata["diagram_params"]` the same way the existing chart topics do.
6. **Stress-test with 100+ random iterations** before committing — check for exceptions,
   absurd/negative values, and formatting artifacts (e.g. `f"{x:g}"` producing
   `1e+07`-style output on large numbers).
