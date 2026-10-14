# ganttchart

A Python library for defining schedules, plotting Gantt charts, and creating
reusable Matplotlib visualizations. The Gantt data model uses the Python
standard library; plotting relies on Matplotlib.

**Status:** early development (`0.0.1`). The API may change before a stable release.

## Features

- Add tasks with **inclusive** start/end dates and a completion percentage.
- Group related activities and color them consistently.
- Highlight weekends and mark a selected date (or today).
- Adjust figure size, typography, grids, legends and date formatting with `PlotParameters`.
- Reuse Matplotlib axes to assemble Gantt charts and plots in one figure.
- Export graphics to PNG, PDF or SVG; optionally export task data using Pandas.
- Use general 2D drawing helpers for lines, bars, histograms, heatmaps and more.

## Requirements

- **Python 3.15 or later** (package metadata restricts installation accordingly).
- NumPy >= 2.5.4 and Matplotlib >= 3.11.2.
- Optional: Pandas for `to_dataframe()`; `highlight_text` for enriched figure text.

This package was exercised with Python 3.13 during refactoring; a complete
runtime test on Python 3.15 is still needed before release.

## Installation

Clone the repository:

```bash
git clone https://github.com/Thomeli09/ganttchart.git
cd ganttchart
```

Create a virtual environment (example commands for Windows PowerShell):

```powershell
py -3.15 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

On Linux/macOS, use `python3.15 -m venv .venv` and `source .venv/bin/activate`.
Alternatively, `python -m pip install -r requirements.txt` installs the editable
package. To install development dependencies:

```bash
python -m pip install -e ".[dev]"
# Or: python -m pip install -r requirements-dev.txt
```

Install optional Pandas support separately if needed:

```bash
python -m pip install -e ".[data]"
```

## Quick start: Gantt chart

```python
from ganttchart import GanttChart
from ganttchart.visualization import PlotParameters, save_figure

chart = GanttChart()
chart.add_task("Design", "2026-10-01", "2026-10-10", completion=1.0, group="Planning")
chart.add_task("Build", "2026-10-11", "2026-10-25", completion=0.4, group="Construction")

style = PlotParameters(
    title="Project schedule", xlabel="Date", figsize=(12, 5),
    show_grid=True, grid_axis="x", date_format="%d %b",
)
fig, ax = chart.plot(parameters=style, show_weekends=True)
save_figure(fig, "schedule.png")
```

`completion` is a **fraction**, not a percentage: use `0.4` for 40%.
Task endpoints are **inclusive**, so a task starting and ending on the same
date has a one-day duration. A named group's color takes priority over the
individual task color. `chart.plot()` returns `(fig, ax)`; it does not show the
plot window unless you set `show=True`.

## Quick start: general 2D visualization

```python
from ganttchart.visualization import (
    PlotParameters, create_figure, plot_line, configure_axes, save_figure,
)

style = PlotParameters(title="Progress", xlabel="Week", ylabel="Completion (%)",
                       color="steelblue", marker="o", show_grid=True)
fig, ax = create_figure(parameters=style)
line = plot_line(ax, [0, 1, 2, 3], [0, 20, 45, 75], parameters=style, label="Actual")
configure_axes(ax, style)
save_figure(fig, "progress.png")
```

Plotting functions return the Matplotlib artists so you can update them later.
For example: `line.set_color("red")`.

## Runnable examples

Complete scripts are stored in [`examples/`](examples/README.md):

| File | What it demonstrates |
| --- | --- |
| [`01_gantt_basic.py`](examples/01_gantt_basic.py) | Simple task schedule and PNG export |
| [`02_gantt_advanced.py`](examples/02_gantt_advanced.py) | Task groups, colors, weekends, fixed today, PNG/PDF |
| [`03_gantt_dashboard.py`](examples/03_gantt_dashboard.py) | Gantt and progress curve in one figure |
| [`04_gantt_dataframe.py`](examples/04_gantt_dataframe.py) | Optional Pandas DataFrame and CSV export |
| [`05_visualization_basic.py`](examples/05_visualization_basic.py) | Line and bar plots |
| [`06_visualization_advanced.py`](examples/06_visualization_advanced.py) | Multi-panel plots, uncertainty, histograms, heatmaps |
| [`07_visualization_shapes.py`](examples/07_visualization_shapes.py) | Editable artists, geometric shapes and pie charts |

After installation, run any example from the repository root:

```bash
python examples/01_gantt_basic.py
python examples/02_gantt_advanced.py
python examples/03_gantt_dashboard.py
python examples/04_gantt_dataframe.py
python examples/05_visualization_basic.py
python examples/06_visualization_advanced.py
python examples/07_visualization_shapes.py
```

Outputs are written to `examples/output/` (ignored by Git). To override the
output folder, set the `GANTTCHART_EXAMPLE_OUTPUT` environment variable.
The examples have fixed input data and do not depend on external files.

## Package structure

```text
src/ganttchart/
  __init__.py                # GanttChart, Task, add_days
  ganttchart.py              # Task management; plot() delegates to the renderer
  utils/                     # List, vector and matrix operations
  visualization/
    __init__.py
    plot_parameters.py       # PlotParameters dataclass
    plot_basic.py            # Figure and axes management, legend, export
    plot_2d.py               # General 2D plotting artists
    plot_gantt.py            # Gantt-specific rendering
examples/                    # Runnable examples
tests/                      # Unit and smoke tests
```

## Testing

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

Run the smoke tests in headless mode on a CI server by setting `MPLBACKEND=Agg`.
You can also run all seven examples with `python -m pytest -q tests/test_examples.py`.

## Contributing

Contributions, bug fixes, documentation improvements and tests are welcome.
Open an issue at the [project repository](https://github.com/Thomeli09/ganttchart/issues)
before making significant API changes.

## Citation

If you use this software in technical or published work, cite the project.
Citation details are in [`CITATION.cff`](CITATION.cff).

```bibtex
@software{Thommes_GanttChart_2026,
  author  = {Thommes, Eliott},
  title   = {ganttchart},
  year    = {2026},
  version = {0.0.1},
  url     = {https://github.com/Thomeli09/ganttchart}
}
```

Author: **Eliott Thommes** · [ORCID 0009-0005-0697-2438](https://orcid.org/0009-0005-0697-2438)

## License

Copyright © 2026 Eliott Thommes.

Licensed under the **GNU General Public License, version 3 or later**
(`GPL-3.0-or-later`). See [`LICENSE`](LICENSE) for the complete GPL-3.0 text.