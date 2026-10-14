"""Smoke, behavior, and error tests for general plotting utilities."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pytest
from matplotlib.axes import Axes
from matplotlib.collections import QuadMesh
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon

from ganttchart.visualization import (
    PlotParameters, add_colorbar, add_figure_text, add_legend,
    add_legend_with_subtitles, close_figure, compute_limits, configure_axes,
    create_figure, draw_circle, draw_infinite_line, draw_reference_line,
    draw_span, fill_area, format_text, plot_bars, plot_empty_line,
    plot_histogram, plot_histogram2d, plot_image, plot_line, plot_pie,
    plot_series, plot_text, save_figure, set_figure_size, update_line,
    update_line_colors,
)

@pytest.fixture
def plot():
    fig, ax = create_figure()
    yield fig, ax
    plt.close(fig)


def test_parameters():
    params = PlotParameters(palette=("red", "blue"), colormap="plasma")
    assert params.color_at(2) == "red"
    assert len(params.sample_colormap(4)) == 4
    assert params.color_at(0) == "red"
    with pytest.raises(ValueError):
        PlotParameters(alpha=1.1)
    with pytest.raises(ValueError):
        PlotParameters(colormap="not_a_colormap")


def test_create_and_configure(plot):
    fig, ax = plot
    params = PlotParameters(title="Demo", xlabel="Date", show_grid=True, show_box=False)
    plot_line(ax, [1, 2], [3, 4], label="data")
    configure_axes(ax, params)
    assert ax.get_title() == "Demo"
    assert ax.get_legend() is not None
    assert all(not spine.get_visible() for spine in ax.spines.values())


def test_subplots():
    fig, axs = create_figure(2, 3, squeeze=False)
    assert axs.shape == (2, 3)
    plt.close(fig)


def test_lines_and_updates(plot):
    _, ax = plot
    first = plot_line(ax, [0, 1], [1, 2], label="a")
    assert isinstance(first, Line2D)
    update_line(first, [0, 1], [3, 4])
    assert list(first.get_ydata()) == [3, 4]
    second = plot_empty_line(ax)
    assert len(second.get_xdata()) == 0
    updated = update_line_colors(ax, ["red", "blue"])
    assert len(updated) == 2
    with pytest.raises(ValueError):
        update_line_colors(ax, ["green"])


def test_series(plot):
    _, ax = plot
    params = PlotParameters(palette=("red", "blue"))
    lines = plot_series(ax, [[0, 1], [0, 1]], [[2, 3], [4, 5]],
                        parameters=params, labels=["first", "second"])
    assert len(lines) == 2
    assert lines[0].get_color() == "red"
    assert lines[1].get_color() == "blue"
    with pytest.raises(ValueError):
        plot_series(ax, [[0]], [[1], [2]])


def test_text_and_formatting(plot):
    _, ax = plot
    text = plot_text(ax, (0.5, 0.5), "note", coordinates="axes")
    assert text.get_transform() == ax.transAxes
    format_text(text, weight="bold", color="red")
    assert text.get_weight() == "bold"


def test_figure_text(plot):
    fig, _ = plot
    text = add_figure_text(fig, "heading")
    assert text.get_text() == "heading"


def test_reference_lines(plot):
    _, ax = plot
    assert isinstance(draw_reference_line(ax, 3), Line2D)
    assert len(draw_reference_line(ax, [1, 2])) == 2
    assert draw_reference_line(ax, [1, 2], relative=False) is not None
    assert draw_reference_line(ax, 3, orientation="horizontal") is not None
    with pytest.raises(ValueError):
        draw_reference_line(ax, 3, orientation="diagonal")


def test_infinite_line(plot):
    _, ax = plot
    assert isinstance(draw_infinite_line(ax, (0, 0), slope=1), Line2D)
    assert isinstance(draw_infinite_line(ax, (0, 0), second_point=(1, 1)), Line2D)
    with pytest.raises(ValueError):
        draw_infinite_line(ax, (0, 0))


def test_span_and_fill(plot):
    _, ax = plot
    assert draw_span(ax, 1, 2) is not None
    assert draw_span(ax, 1, 2, orientation="horizontal") is not None
    assert len(fill_area(ax, [0, 1, 2], [0, 2, 0])) == 1
    assert fill_area(ax, [0, 1, 2], [0, 2, 0], secondary_y=[0, 1, 0]) is not None


def test_bars(plot):
    _, ax = plot
    assert len(plot_bars(ax, ["A", "B"], [1, 3]).patches) == 2
    assert len(plot_bars(ax, ["C", "D"], [2, 4], horizontal=True, errors=[.1, .3]).patches) == 2


def test_histogram(plot):
    _, ax = plot
    counts, edges, artists = plot_histogram(ax, [1, 1, 2, 2], bins=2)
    assert len(counts) == 2
    assert len(edges) == 3
    assert artists is not None


def test_histogram2d_and_colorbar(plot):
    _, ax = plot
    _, _, _, mesh = plot_histogram2d(ax, [1, 2, 3], [2, 4, 3], colorbar=True)
    assert isinstance(mesh, QuadMesh)
    assert len(ax.figure.axes) == 2


def test_pie(plot):
    _, ax = plot
    wedges, texts, numbers = plot_pie(ax, [1, 2], labels=["A", "B"], display="both")
    assert len(wedges) == 2
    assert len(texts) == 2
    assert len(numbers) == 2
    wedges, _, numbers = plot_pie(ax, [1, 1], display="none", annotate=True,
                                  labels=["C", "D"])
    assert len(numbers) == 0
    with pytest.raises(ValueError):
        plot_pie(ax, [0, 0])


def test_image(plot):
    _, ax = plot
    image = plot_image(ax, [[1, 2], [3, 4]], annotate=True, colorbar=True)
    assert image.get_array().shape == (2, 2)
    assert len(ax.figure.axes) == 2
    with pytest.raises(ValueError):
        plot_image(ax, [[1, 2], [3]])


def test_circle(plot):
    _, ax = plot
    circle = draw_circle(ax, (0, 0), 2, points=24, filled=True)
    assert isinstance(circle, Polygon)
    with pytest.raises(ValueError):
        draw_circle(ax, (0, 0), -1)


def test_limits():
    assert compute_limits([10, 20]) == (9.0, 21.0)
    assert compute_limits(np.array([[5, 5], [5, np.nan]])) == (4.5, 5.5)
    with pytest.raises(ValueError):
        compute_limits([])


def test_figure_size_and_export(plot, tmp_path):
    fig, ax = plot
    set_figure_size(fig, 20, 10)
    assert fig.get_size_inches()[0] == pytest.approx(20 / 2.54)
    plot_line(ax, [1, 2], [3, 4])
    output = save_figure(fig, tmp_path / "nested" / "chart", file_format="png",
                         create_directories=True)
    assert output.is_file()
    assert output.suffix == ".png"
    with pytest.raises(FileNotFoundError):
        save_figure(fig, tmp_path / "missing" / "no.png")


def test_styled_legend(plot):
    _, ax = plot
    plot_line(ax, [0, 1], [1, 2], label="A")
    plot_line(ax, [0, 1], [3, 4], label="B")
    legend = add_legend_with_subtitles(ax, "Heading", ["Sub"], [1])
    assert len(legend.get_texts()) == 3

@pytest.mark.parametrize("display", ["none", "percent", "absolute", "both"])
def test_pie_indexable_container_compatibility(plot, monkeypatch, display):
    """Simulate Matplotlib 3.11's indexable PieContainer without __len__."""
    _, ax = plot
    original = Axes.pie

    class IndexOnlyPieResult:
        def __init__(self, result):
            self.result = result

        def __getitem__(self, item):
            return self.result[item]

    def pie_returning_container(self, *args, **kwargs):
        return IndexOnlyPieResult(original(self, *args, **kwargs))

    monkeypatch.setattr(Axes, "pie", pie_returning_container)
    wedges, labels, numbers = plot_pie(
        ax, [1, 2], labels=["A", "B"], display=display,
    )
    assert len(wedges) == 2
    assert len(labels) == 2
    assert len(numbers) == (0 if display == "none" else 2)
