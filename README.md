# HCI & Data Visualization Case Study: Redesigning a Chart with User-Centered Design

Case study for the *Informatics Practitioner Lecture Series* session
"Human-Computer Interaction & Data Visualization" (Universitas Bengkulu x BRIN).

## Idea from the lecture
Good visualization is designed for a **specific user and task** ("you are not the user"), uses the **right chart for the data**, exploits **preattentive attributes** and **Gestalt principles**, respects **accessibility (WCAG)**, and is **evaluated with real users** (task time, success rate, SUS).

## What this project does
1. **Redesigns one visualization** (before/after) and documents each design decision against a lecture principle.
2. **Checks colour contrast** against WCAG thresholds in code.
3. **Provides a usability-test toolkit** (SUS scoring + task success/time) to evaluate the redesign with real participants.

> The sample data (`data/sample_tickets.csv`) and the files `usability/*_EXAMPLE.csv` are **synthetic**, only to show the pipeline works. The usability test and persona below must be done with real people to count as evidence.

## Before vs after (`src/chart_redesign.py`)
| Problem in "before" (`results/before_pie.png`) | Fix in "after" (`results/after_bar.png`) | Lecture principle |
|---|---|---|
| 8-slice pie: hard to compare similar slices | Horizontal bar chart, sorted | Chart taxonomy (bar for category comparison; pie only for few parts of a whole) |
| 8 rainbow colours, legend far from data | One neutral colour, top-2 highlighted, direct value labels, no legend | Preattentive attribute (colour), proximity, less working-memory load |
| Title "Tickets" says nothing | Title states the finding | Communication purpose of visualization |
| Colour alone encodes emphasis | Values printed on every bar | Accessibility (do not rely on colour only) |
| - | Contrast ratios computed (text >= 4.5:1, graphics >= 3:1) | WCAG 1.4.3 / 1.4.11 |

## UCD artifacts (fill in with real data)
**Persona** (from interviews/observation of real target users, not guesses):
- Demographics: TODO | Goals: TODO | Pain points: TODO | Behaviours: TODO

**Scenario:** Context -> Trigger -> Action -> Outcome: TODO

**Usability test plan** (suggestion: 5+ participants from the persona group):
- Tasks, e.g. T1 "Find the category with the most tickets", T2 "State the share of the top two categories". Compare the *before* and *after* chart (ideally different participants per version or counterbalanced order).
- Record per task: time (sec) and success (1/0). After the session: the 10 SUS items (1-5) in `usability/responses.csv`.

## Run
```bash
pip install -r requirements.txt
python -m src.chart_redesign --csv data/sample_tickets.csv     # or your own CSV: category,value
python -m src.sus --responses usability/responses.csv --tasks usability/tasks.csv
```
Formats: see `usability/*_EXAMPLE.csv`. SUS: odd items score = answer - 1, even items = 5 - answer, sum x 2.5 (range 0-100).

## Results
> TODO: add your real SUS / success rate / time numbers, screenshots, and what you changed after testing.

## Limitations
- Small-n usability tests give directional evidence, not statistical proof.
- Only one chart type is redesigned; interaction design (dashboards, filters) is not covered.
- Automated contrast checks do not replace testing with assistive technologies or colour-blind users.
