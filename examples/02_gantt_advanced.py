"""Advanced Gantt chart: task groups, colors, milestones and PDF/PNG export.

Run: python examples/02_gantt_advanced.py
"""

from __future__ import annotations

import os
from pathlib import Path

from ganttchart import GanttChart, Task, add_days
from ganttchart.visualization import PlotParameters, close_figure, save_figure


def main() -> tuple[Path, Path]:
    chart = GanttChart()
    chart.add_task("Site survey", "2026-10-01", "2026-10-05", completion=1, group="Preparation")
    chart.add_task("Structural design", "2026-10-03", "2026-10-12", completion=0.9, group="Preparation")
    chart.add_task("Order materials", "2026-10-10", "2026-10-14", completion=0.7, group="Procurement")
    chart.add_task("Excavation", "2026-10-15", "2026-10-22", completion=0.3, group="Construction")
    chart.add_task("Foundations", "2026-10-23", "2026-11-02", completion=0.0, group="Construction")
    chart.add_task("Wall construction", "2026-11-03", "2026-11-17", group="Construction")
    chart.add_task("Site inspection", "2026-11-18", "2026-11-18", group="Milestone")
    chart.add_task(Task(name="Final handover", start="2026-11-19", end="2026-11-19", group="Milestone"))

    # Shared styles are reusable; chart.plot() does not mutate this object.
    style = PlotParameters(
        title="Example construction schedule",
        xlabel="Calendar date",
        figsize=(14, 6),
        fontsize=11,
        title_size=15,
        tick_size=10,
        palette=("steelblue", "darkorange", "seagreen", "slategray"),
        alpha=0.35,
        show_grid=True,
        grid_axis="x",
        grid_alpha=0.25,
        date_format="%d %b",
        rotate_dates=True,
        show_legend=True,
        legend_title="Work package",
        legend_outside=True,
    )

    fig, ax = chart.plot(
        parameters=style,
        start="2026-09-29",
        end=add_days("2026-11-19", 3),
        show_weekends=True,
        show_today=True,
        today="2026-10-20",  # Fixed date for reproducible examples.
        group_colors={"Milestone": "firebrick"},
        show_y_labels=True,
        show_bar_labels=False,  # Names appear on the y-axis instead.
        bar_height=0.62,
    )
    ax.set_ylabel("Activities")
    output = Path(os.environ.get("GANTTCHART_EXAMPLE_OUTPUT", Path(__file__).parent / "output"))
    png = save_figure(fig, output / "02_gantt_advanced.png", create_directories=True)
    pdf = save_figure(fig, output / "02_gantt_advanced.pdf")
    close_figure(fig)
    print(f"Saved: {png} and {pdf}")
    return png, pdf


if __name__ == "__main__":
    main()
