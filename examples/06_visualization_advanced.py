"""Advanced visualization: lines with uncertainty, a histogram, and a heatmap.

Run: python examples/06_visualization_advanced.py
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
    draw_reference_line,
    draw_span,
    fill_area,
    plot_histogram,
    plot_image,
    plot_series,
    save_figure,
)


def main() -> tuple[Path, Path]:
    rng = np.random.default_rng(42)  # Reproducible synthetic data.
    style = PlotParameters(figsize=(12, 8), fontsize=10, title_size=12,
                           show_grid=True, grid_alpha=0.2)
    fig, axes = create_figure(rows=2, columns=2, parameters=style)
    ax_curve, ax_hist, ax_map, ax_summary = axes.flat

    x = np.linspace(0.0, 10.0, 200)
    signal = np.sin(x)
    model = 0.8 * np.sin(x + 0.2)
    line_style = replace(style, palette=("steelblue", "darkorange"), linewidth=2)
    plot_series(ax_curve, [x, x], [signal, model], parameters=line_style,
                labels=["Measurements", "Model"])
    fill_area(ax_curve, x, model + 0.2, secondary_y=model - 0.2,
              parameters=replace(style, color="darkorange", alpha=0.15))
    draw_reference_line(ax_curve, 0.0, orientation="horizontal",
                        parameters=replace(style, color="black", linestyle="--"))
    draw_span(ax_curve, 3.0, 4.0, parameters=replace(style, color="grey", alpha=0.15))
    configure_axes(ax_curve, replace(style, title="Signals and uncertainty",
                                     xlabel="Time", ylabel="Amplitude"))

    values = rng.normal(loc=0.0, scale=1.0, size=800)
    plot_histogram(ax_hist, values, bins=25, density=True,
                   parameters=replace(style, color="seagreen", alpha=0.8))
    configure_axes(ax_hist, replace(style, title="Sample distribution",
                                    xlabel="Value", ylabel="Probability density", show_legend=False))

    matrix = np.array([[0.2, 0.4, 0.8], [0.6, 0.3, 0.1], [0.9, 0.7, 0.5]])
    plot_image(ax_map, matrix, parameters=replace(style, colormap="viridis", colorbar_label="Index"),
               annotate=True, colorbar=True)
    configure_axes(ax_map, replace(style, title="Heatmap", xlabel="Column", ylabel="Row", show_legend=False))

    # Fourth panel: an XY histogram that returns a mappable (QuadMesh).
    from ganttchart.visualization import plot_histogram2d
    x_data = rng.normal(size=1000)
    y_data = x_data * 0.6 + rng.normal(size=1000) * 0.7
    plot_histogram2d(ax_summary, x_data, y_data, bins=25,
                     parameters=replace(style, colormap="plasma", colorbar_label="Count"),
                     colorbar=True)
    configure_axes(ax_summary, replace(style, title="2D histogram", xlabel="X", ylabel="Y", show_legend=False))

    output = Path(os.environ.get("GANTTCHART_EXAMPLE_OUTPUT", Path(__file__).parent / "output"))
    png = save_figure(fig, output / "06_visualization_advanced.png", create_directories=True)
    pdf = save_figure(fig, output / "06_visualization_advanced.pdf")
    close_figure(fig)
    print(f"Saved: {png} and {pdf}")
    return png, pdf


if __name__ == "__main__":
    main()
