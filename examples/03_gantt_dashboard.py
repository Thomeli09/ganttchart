"""Advanced integration: embed a Gantt chart and a progress curve in subplots.

Run: python examples/03_gantt_dashboard.py
"""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

from ganttchart import GanttChart
from ganttchart.visualization import (
    PlotParameters,
    close_figure,
    configure_axes,
    create_figure,
    plot_series,
    save_figure,
)


def main() -> Path:
    chart = GanttChart()
    chart.add_task("Specification", "2026-10-01", "2026-10-08", completion=1, group="Design")
    chart.add_task("Prototype", "2026-10-09", "2026-10-20", completion=0.6, group="Build")
    chart.add_task("Validation", "2026-10-18", "2026-10-28", completion=0.1, group="Test")
    chart.add_task("Release", "2026-10-30", "2026-10-30", completion=0, group="Test")

    style = PlotParameters(
        figsize=(12, 8), title="Project tasks", xlabel="Date", tick_size=10,
        show_grid=True, grid_axis="x", grid_alpha=0.2, alpha=0.35,
        palette=("steelblue", "darkorange", "seagreen"),
    )
    fig, axes = create_figure(rows=2, columns=1, parameters=style)
    gantt_ax, progress_ax = axes
    chart.plot(parameters=style, ax=gantt_ax, show_weekends=True, show_bar_labels=False)

    weeks = [0, 1, 2, 3, 4]
    planned = [0, 20, 50, 80, 100]
    actual = [0, 15, 35, 58, 78]
    lower_style = replace(
        style, title="Overall project completion", xlabel="Week", ylabel="Completion (%)",
        palette=("steelblue", "firebrick"), alpha=1.0, marker="o",
        grid_axis="both", ylim=(0, 110),
    )
    plot_series(
        progress_ax, [weeks, weeks], [planned, actual],
        parameters=lower_style, labels=["Planned", "Actual"],
    )
    configure_axes(progress_ax, lower_style)
    output = Path(os.environ.get("GANTTCHART_EXAMPLE_OUTPUT", Path(__file__).parent / "output"))
    path = save_figure(fig, output / "03_gantt_dashboard.pdf", create_directories=True)
    close_figure(fig)
    print(f"Saved: {path}")
    return path


if __name__ == "__main__":
    main()
