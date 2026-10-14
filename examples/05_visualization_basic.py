"""Basic visualization: a line plot and a bar chart in one figure.

Run: python examples/05_visualization_basic.py
"""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

import numpy as np

from ganttchart.visualization import (
    PlotParameters,
    close_figure,
    configure_axes,
    create_figure,
    plot_bars,
    plot_line,
    save_figure,
)


def main() -> Path:
    style = PlotParameters(
        figsize=(11, 4), color="steelblue", linewidth=2, marker="o",
        show_grid=True, grid_alpha=0.2,
    )
    fig, axes = create_figure(rows=1, columns=2, parameters=style)
    x = np.arange(6)
    y = np.array([1.0, 2.0, 2.7, 3.2, 4.5, 5.0])
    plot_line(axes[0], x, y, parameters=style, label="Measured")
    configure_axes(axes[0], replace(style, title="Line plot", xlabel="Time", ylabel="Response"))

    plot_bars(axes[1], ["A", "B", "C"], [4, 7, 3], parameters=style)
    configure_axes(axes[1], replace(style, title="Bar chart", xlabel="Category", ylabel="Quantity", show_legend=False))

    output = Path(os.environ.get("GANTTCHART_EXAMPLE_OUTPUT", Path(__file__).parent / "output"))
    path = save_figure(fig, output / "05_visualization_basic.png", create_directories=True)
    close_figure(fig)
    print(f"Saved: {path}")
    return path


if __name__ == "__main__":
    main()
