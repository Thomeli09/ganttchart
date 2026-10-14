"""Basic Gantt chart: three tasks, one figure and a PNG export.

Run: python examples/01_gantt_basic.py
"""

from __future__ import annotations

import os
from pathlib import Path

from ganttchart import GanttChart
from ganttchart.visualization import close_figure, save_figure


def main() -> Path:
    chart = GanttChart()
    chart.add_task("Planning", "2026-10-01", "2026-10-06", completion=1.0)
    chart.add_task("Design", "2026-10-05", "2026-10-12", completion=0.7)
    chart.add_task("Construction", "2026-10-13", "2026-10-27", completion=0.2)

    # plot() creates artists, but does not display a window by default.
    fig, ax = chart.plot(title="My first Gantt chart", show_weekends=True)
    ax.set_ylabel("Tasks")

    output = Path(os.environ.get("GANTTCHART_EXAMPLE_OUTPUT", Path(__file__).parent / "output"))
    path = save_figure(fig, output / "01_gantt_basic.png", create_directories=True)
    close_figure(fig)
    print(f"Saved: {path}")
    return path


if __name__ == "__main__":
    main()
