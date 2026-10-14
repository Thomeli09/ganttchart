"""Tests for the public Gantt chart API."""

from datetime import date, datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

from ganttchart import GanttChart, Task, add_days


def test_task_dates_and_duration():
    task = Task(name="One day", start="2026-10-14", end="2026-10-14", completion=0.25)
    assert task.start == date(2026, 10, 14)
    assert task.end == task.start
    assert task.duration_days == 1
    assert task.completed_days == 0.25


def test_task_validation():
    with pytest.raises(ValueError, match="after"):
        Task(name="Reversed", start="2026-10-15", end="2026-10-14")
    with pytest.raises(ValueError, match="between"):
        Task(name="Too much", start="2026-10-14", end="2026-10-14", completion=1.5)
    with pytest.raises(ValueError, match="non-empty"):
        Task(name="", start="2026-10-14", end="2026-10-14")
    with pytest.raises(TypeError):
        Task(name="Wrong", start=123, end="2026-10-14")


def test_add_task_both_styles_and_order():
    first = Task(name="One", start="2026-10-12", end="2026-10-14")
    chart = GanttChart([first])
    second = chart.add_task("Two", datetime(2026, 10, 16), "2026-10-18", completion=1.0)
    assert chart.tasks == (first, second)
    assert list(chart) == [first, second]
    assert len(chart) == 2
    with pytest.raises(TypeError):
        chart.add_task("Missing dates")
    with pytest.raises(TypeError):
        chart.add_task(first, "2026-10-10", "2026-10-11")
    chart.clear()
    assert chart.tasks == ()


def test_date_range():
    chart = GanttChart()
    with pytest.raises(ValueError, match="without tasks"):
        chart.date_range()
    chart.add_task("A", "2026-10-10", "2026-10-12")
    chart.add_task("B", "2026-10-14", "2026-10-20")
    assert chart.date_range() == (date(2026, 10, 10), date(2026, 10, 20))
    assert chart.date_range(include_today=True, today="2026-10-22") == (
        date(2026, 10, 10), date(2026, 10, 22),
    )
    assert chart.date_range("2026-10-01", "2026-10-31") == (
        date(2026, 10, 1), date(2026, 10, 31),
    )
    with pytest.raises(ValueError, match="later"):
        chart.date_range("2026-10-31", "2026-10-01")


def test_add_days_and_dataframe():
    assert add_days("2026-10-14", 3) == "2026-10-17"
    assert add_days("2026-10-14T12:00:00", -1) == "2026-10-13"
    chart = GanttChart()
    chart.add_task("A", "2026-10-14", "2026-10-16", completion=1/3)
    df = chart.to_dataframe()
    assert df["task"].tolist() == ["A"]
    assert df["duration_days"].tolist() == [3]
    df.loc[0, "task"] = "B"
    assert chart.tasks[0].name == "A"


def test_plot_bars_and_legend_and_weekends():
    chart = GanttChart()
    chart.add_task("A", "2026-10-10", "2026-10-13", completion=0.5, group="Engineering")
    chart.add_task("B", "2026-10-10", "2026-10-10", completion=1, group="Engineering")
    chart.add_task("C", "2026-10-15", "2026-10-15", completion=0, color="purple")
    fig, ax = chart.plot(
        show_weekends=True,
        group_colors={"Engineering": "blue"},
        show_y_labels=False,
        show_bar_labels=False,
    )
    assert len(ax.patches) >= 5
    assert len(ax.get_yticklabels()) == 0
    assert ax.get_legend() is not None
    assert ax.get_title() == "Gantt chart"
    assert fig is ax.figure
    plt.close(fig)


def test_plot_today_and_external_axes():
    chart = GanttChart()
    chart.add_task("A", "2026-10-10", "2026-10-10")
    fig, ax = plt.subplots()
    result_fig, result_ax = chart.plot(show_today=True, ax=ax)
    assert result_fig is fig
    assert result_ax is ax
    assert ax.get_legend() is not None
    plt.close(fig)


def test_plot_empty_or_bad_parameters():
    with pytest.raises(ValueError):
        GanttChart().plot()
    chart = GanttChart()
    chart.add_task("A", "2026-10-10", "2026-10-10")
    with pytest.raises(ValueError):
        chart.plot(bar_height=0)


def test_matplotlib_default_task_bar_color_matches_progress():
    chart = GanttChart()
    chart.add_task("Task", "2026-10-10", "2026-10-12", completion=0.5)
    fig, ax = chart.plot()
    assert len(ax.patches) == 2
    background, completed = ax.patches
    assert background.get_facecolor()[:3] == completed.get_facecolor()[:3]
    plt.close(fig)




