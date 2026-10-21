# HCI & Data Visualization Case Study: Redesigning a Chart with User-Centered Design

Case study for the _Informatics Practitioner Lecture Series_ session
"Human-Computer Interaction & Data Visualization" (Universitas Bengkulu x BRIN).

## Idea from the lecture

Good visualization is designed for a **specific user and task** ("you are not the user"), uses the **right chart for the data**, exploits **preattentive attributes** and **Gestalt principles**, respects **accessibility (WCAG)**, and is **evaluated with real users** (task time, success rate, SUS).

## What this project does

1. **Redesigns one visualization** (before/after) and documents each design decision against a lecture principle.
2. **Checks colour contrast** against WCAG thresholds in code.
3. **Provides tooling for a small task-based comparison of the two versions** (completion time and success rate per task). `src/sus.py` also provides SUS scoring, intended for interactive interfaces; it is not used here because a static chart is not an interactive system.

> The sample data (`data/sample_tickets.csv`) and the files `usability/*_EXAMPLE.csv` are **synthetic**. The sample data only demonstrates the redesign; the example files only show the file formats.

## Before vs after (`src/chart_redesign.py`)

| Problem in "before" (`results/before_pie.png`) | Fix in "after" (`results/after_bar.png`)                              | Lecture principle                                                               |
| ---------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 8-slice pie: hard to compare similar slices    | Horizontal bar chart, sorted                                          | Chart taxonomy (bar for category comparison; pie only for few parts of a whole) |
| 8 rainbow colours, legend far from data        | One neutral colour, top-2 highlighted, direct value labels, no legend | Preattentive attribute (colour), proximity, less working-memory load            |
| Title "Tickets" says nothing                   | Title states the finding                                              | Communication purpose of visualization                                          |
| Colour alone encodes emphasis                  | Values printed on every bar                                           | Accessibility (do not rely on colour only)                                      |
| -                                              | Contrast ratios computed (text >= 4.5:1, graphics >= 3:1)             | WCAG 1.4.3 / 1.4.11                                                             |

## User-centered design artifacts

**Persona and scenario:** not yet done. A persona must come from interviews or observation of real target users, so none is invented here.

## Usability test (planned)

- Participants: not yet recruited. Planned design: about 6 people, 3 shown the "before" chart and 3 the "after" chart (each person sees only one version).
- Tasks: T1 "Which category has the most tickets?"; T2 "Roughly what percentage of all tickets do the top two categories make up?" The accepted answer range for T2 is fixed before testing (planned: 45-55%).
- Data: `usability/tasks.csv` (columns: participant, version, task, time_sec, success). The file currently contains only the header.

## Run

```bash
pip install -r requirements.txt
python -m src.chart_redesign --csv data/sample_tickets.csv     # or your own CSV: category,value
python -m src.sus --tasks usability/tasks.csv                  # task success/time per version (after data is collected)
```

`usability/*_EXAMPLE.csv` only show the file formats (synthetic). SUS scoring (`python -m src.sus --responses ...`) is available for interactive interfaces: odd items score = answer - 1, even items = 5 - answer, sum x 2.5 (range 0-100).

## Results

**Redesign (done).** `results/before_pie.png` and `results/after_bar.png` show the same synthetic ticket data before and after redesign (see the table above for each change and its lecture principle).

**Colour contrast** (computed by `src/chart_redesign.py`, against a white background):

| Element          | Colour  | Contrast ratio | Target                |
| ---------------- | ------- | -------------- | --------------------- |
| Bars (neutral)   | #6B7280 | 4.83:1         | >= 3:1 (WCAG 1.4.11)  |
| Bars (highlight) | #B91C1C | 6.47:1         | >= 3:1 (WCAG 1.4.11)  |
| Text             | #111827 | 17.74:1        | >= 4.5:1 (WCAG 1.4.3) |

All colours meet the thresholds. Highlighting uses colour, but every bar also carries its value as a text label, so the message does not depend on colour alone.

**Usability test (not yet conducted).** No participants have been tested, so this repository does not claim that the redesign improves speed or accuracy.

## Limitations

- The usability test has not been run yet; the redesign is justified by established design principles, not by user data from this project.
- Once run, small-n usability tests give directional evidence, not statistical proof.
- The data is synthetic and one chart type is redesigned; interaction design (dashboards, filters) is not covered.
- Automated contrast checks do not replace testing with assistive technologies or colour-blind users.
