"""Example of general-purpose visualization; saves without opening a GUI window."""

from pathlib import Path

import numpy as np

from ganttchart.visualization import (
    PlotParameters,
    add_colorbar,
    configure_axes,
    create_figure,
    draw_span,
    plot_image,
    plot_line,
    save_figure,
)


def main() -> Path:
    """Create a two-panel example and return the exported file path."""
    settings = PlotParameters(
        color="steelblue", title="Time evolution", xlabel="Time",
        ylabel="Response", show_grid=True,
        figsize=(12, 4.5), colorbar_label="Intensity",
    )
    fig, axes = create_figure(1, 2, parameters=settings)

    times = np.linspace(0, 5, 100)
    plot_line(axes[0], times, np.sin(times), parameters=settings, label="Signal")
    draw_span(axes[0], 2.0, 2.7,
              parameters=PlotParameters(color="lightgray", alpha=0.4))
    configure_axes(axes[0], settings)

    image_style = PlotParameters(title="Matrix data", colormap="viridis")
    image = plot_image(axes[1], [[1, 2, 3], [3, 1, 4]],
                       parameters=image_style, annotate=True)
    configure_axes(axes[1], image_style)
    add_colorbar(image, ax=axes[1], parameters=settings)

    return save_figure(fig, "visualization_example.png")


if __name__ == "__main__":
    print(main())
