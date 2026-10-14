"""More visualization primitives: circles, pie charts, and artist updates.

Run: python examples/07_visualization_shapes.py
"""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

from ganttchart.visualization import (
    PlotParameters,
    close_figure,
    configure_axes,
    create_figure,
    draw_circle,
    draw_infinite_line,
    plot_empty_line,
    plot_pie,
    save_figure,
    update_line,
)


def main() -> Path:
    style = PlotParameters(figsize=(11, 4), show_grid=True, grid_alpha=0.2)
    fig, axes = create_figure(columns=2, parameters=style)

    # Draw and later update a Matplotlib artist.
    line = plot_empty_line(axes[0], parameters=replace(style, color="steelblue", marker="o"), label="Trajectory")
    update_line(line, [0, 1, 2, 3], [0, 1, 1.7, 2.5])
    draw_circle(axes[0], (1.4, 1.2), 0.5,
                parameters=replace(style, color="seagreen", alpha=0.4), filled=True)
    draw_infinite_line(axes[0], (0, 0), slope=0.75,
                       parameters=replace(style, color="grey", linestyle="--"))
    configure_axes(axes[0], replace(style, title="Editable artists", xlabel="X", ylabel="Y"))

    pie_style = replace(style, palette=("steelblue", "seagreen", "darkorange"), show_grid=False, show_legend=False)
    plot_pie(axes[1], [40, 35, 25], labels=["Design", "Build", "Test"],
             parameters=pie_style, display="both", percent_precision=0)
    configure_axes(axes[1], replace(pie_style, title="Work distribution"))

    output = Path(os.environ.get("GANTTCHART_EXAMPLE_OUTPUT", Path(__file__).parent / "output"))
    path = save_figure(fig, output / "07_visualization_shapes.png", create_directories=True)
    close_figure(fig)
    print(f"Saved: {path}")
    return path


if __name__ == "__main__":
    main()
