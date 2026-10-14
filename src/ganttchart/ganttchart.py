"""Task data and Matplotlib rendering for Gantt charts.

The data model is independent of Pandas and custom plotting libraries.
Matplotlib is used only when :meth:`GanttChart.plot` is called.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from math import isfinite
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.figure import Figure
    from pandas import DataFrame
    from .visualization.plot_parameters import PlotParameters


type DateLike = date | datetime | str
type Color = str | tuple[float, ...] | None


def _to_date(value: DateLike) -> date:
    """Convert an ISO date or a Python date/time to a calendar date."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            try:
                return datetime.fromisoformat(value).date()
            except ValueError as exc:
                raise ValueError(
                    f"Invalid date {value!r}; expected an ISO 8601 date or datetime."
                ) from exc
    raise TypeError("Dates must be a date, datetime or ISO 8601 string.")


def add_days(value: DateLike, days: int) -> str:
    """Return an ISO-formatted date after adding a number of days.

    Parameters
    ----------
    value : datetime.date, datetime.datetime, or str
        Initial date. Strings must be in ISO 8601 format.
    days : int
        Number of calendar days to add (negative values are allowed).

    Returns
    -------
    str
        Shifted date in ``YYYY-MM-DD`` format.

    Raises
    ------
    TypeError
        If the input date or number of days has an invalid type.
    ValueError
        If a date string is invalid.
    OverflowError
        If the resulting date falls outside the supported date range.

    Examples
    --------
    >>> add_days("2026-10-14", 3)
    '2026-10-17'
    """
    if isinstance(days, bool) or not isinstance(days, int):
        raise TypeError("'days' must be an integer.")
    return (_to_date(value) + timedelta(days=days)).isoformat()


@dataclass(frozen=True, slots=True, kw_only=True)
class Task:
    """A scheduled task with an inclusive date range.

    Parameters
    ----------
    name : str
        Human-readable task label.
    start : datetime.date, datetime.datetime, or str
        Task start date, inclusive. ISO 8601 strings are accepted.
    end : datetime.date, datetime.datetime, or str
        Task end date, inclusive. ISO 8601 strings are accepted.
    completion : float, default 0.0
        Fraction completed, between 0.0 and 1.0.
    color : str or tuple of float, optional
        Matplotlib-compatible task color. Ignored for tasks belonging to
        a group, since grouped tasks share a group color.
    group : str, optional
        Group identifier. Tasks in the same group are drawn in the same
        color and represented together in the plot legend.

    Raises
    ------
    TypeError
        If arguments have inappropriate types.
    ValueError
        If the name is empty, the date interval is reversed, or the
        completion fraction is outside ``[0, 1]``.

    Notes
    -----
    Start and end dates include both endpoints. A task with equal start
    and end dates therefore spans one full calendar day.
    """

    name: str
    start: DateLike
    end: DateLike
    completion: float = 0.0
    color: Color = None
    group: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("'name' must be a non-empty string.")
        start = _to_date(self.start)
        end = _to_date(self.end)
        if end < start:
            raise ValueError("'end' must be on or after 'start'.")
        if isinstance(self.completion, bool) or not isinstance(
            self.completion, (int, float)
        ):
            raise TypeError("'completion' must be a number between 0 and 1.")
        if not isfinite(self.completion) or not 0 <= self.completion <= 1:
            raise ValueError("'completion' must be between 0 and 1.")
        if self.group is not None and (
            not isinstance(self.group, str) or not self.group.strip()
        ):
            raise ValueError("'group' must be a non-empty string or None.")
        object.__setattr__(self, "start", start)
        object.__setattr__(self, "end", end)
        object.__setattr__(self, "completion", float(self.completion))

    @property
    def duration_days(self) -> int:
        """Number of calendar days covered by the task, inclusive."""
        return (self.end - self.start).days + 1

    @property
    def completed_days(self) -> float:
        """Completed portion of the duration in calendar days."""
        return self.duration_days * self.completion


class GanttChart:
    """Manage and draw an ordered collection of scheduled tasks.

    Parameters
    ----------
    tasks : iterable of Task, optional
        Tasks to include initially. Their order is preserved.

    Examples
    --------
    >>> chart = GanttChart()
    >>> chart.add_task("Design", "2026-10-14", "2026-10-19", completion=0.5)
    Task(name='Design', start=datetime.date(2026, 10, 14), end=datetime.date(2026, 10, 19), completion=0.5, color=None, group=None)
    >>> len(chart.tasks)
    1
    """

    def __init__(self, tasks: Iterable[Task] | None = None) -> None:
        self._tasks: list[Task] = []
        if tasks is not None:
            for task in tasks:
                self.add_task(task)

    @property
    def tasks(self) -> tuple[Task, ...]:
        """Read-only snapshot of tasks in insertion order."""
        return tuple(self._tasks)

    def __len__(self) -> int:
        """Return the number of tasks."""
        return len(self._tasks)

    def __iter__(self) -> Iterator[Task]:
        """Iterate over tasks in insertion order."""
        return iter(self._tasks)

    @overload
    def add_task(self, task: Task, /) -> Task: ...

    @overload
    def add_task(
        self,
        task: str,
        start: DateLike,
        end: DateLike,
        *,
        completion: float = 0.0,
        color: Color = None,
        group: str | None = None,
    ) -> Task: ...

    def add_task(
        self,
        task: Task | str,
        start: DateLike | None = None,
        end: DateLike | None = None,
        *,
        completion: float = 0.0,
        color: Color = None,
        group: str | None = None,
    ) -> Task:
        """Add an existing task or create one from its attributes.

        Parameters
        ----------
        task : Task or str
            Task object or name of a new task.
        start, end : datetime.date, datetime.datetime, or str, optional
            Required when ``task`` is a string; inclusive date range.
        completion : float, default 0.0
            Completion fraction in ``[0, 1]`` for a newly created task.
        color : str or tuple of float, optional
            Matplotlib-compatible color for an ungrouped task.
        group : str, optional
            Optional color-group name.

        Returns
        -------
        Task
            Newly added task instance.

        Raises
        ------
        TypeError
            If arguments are provided in the wrong combination.
        ValueError
            If the task attributes fail validation.
        """
        if isinstance(task, Task):
            if (
                start is not None
                or end is not None
                or completion != 0.0
                or color is not None
                or group is not None
            ):
                raise TypeError("Additional attributes cannot accompany a Task.")
            created = task
        elif isinstance(task, str):
            if start is None or end is None:
                raise TypeError("'start' and 'end' are required for a new task.")
            created = Task(
                name=task,
                start=start,
                end=end,
                completion=completion,
                color=color,
                group=group,
            )
        else:
            raise TypeError("'task' must be a Task object or task name.")

        self._tasks.append(created)
        return created

    def clear(self) -> None:
        """Remove all tasks from the chart."""
        self._tasks.clear()

    def date_range(
        self,
        start: DateLike | None = None,
        end: DateLike | None = None,
        *,
        include_today: bool = False,
        today: DateLike | None = None,
    ) -> tuple[date, date]:
        """Return the date interval containing tasks and optional limits.

        Parameters
        ----------
        start, end : datetime.date, datetime.datetime, or str, optional
            Explicit boundaries; omitted boundaries are inferred from tasks.
        include_today : bool, default False
            Expand the interval to include today's date.
        today : datetime.date, datetime.datetime, or str, optional
            Override the date used for ``include_today`` (useful for tests).

        Returns
        -------
        tuple of datetime.date
            Start and end of the visible interval, inclusive.

        Raises
        ------
        ValueError
            If the collection is empty or the interval is reversed.
        """
        if not self._tasks:
            raise ValueError("Cannot determine a date range without tasks.")
        first = _to_date(start) if start is not None else min(t.start for t in self._tasks)
        last = _to_date(end) if end is not None else max(t.end for t in self._tasks)
        if first > last:
            raise ValueError("'start' must not be later than 'end'.")
        if include_today:
            current = _to_date(today) if today is not None else date.today()
            first = min(first, current)
            last = max(last, current)
        return first, last

    def to_dataframe(self) -> DataFrame:
        """Return a fresh Pandas DataFrame containing all tasks.

        Returns
        -------
        pandas.DataFrame
            Columns ``task``, ``start``, ``end``, ``completion_ratio``,
            ``color``, ``group``, ``duration_days``, ``completed_days``.

        Raises
        ------
        ImportError
            If Pandas is not installed.

        Notes
        -----
        Pandas is an optional dependency; it is needed only for this method.
        Modifying the returned frame does not change chart tasks.
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "Install pandas to use GanttChart.to_dataframe()."
            ) from exc
        return pd.DataFrame.from_records(
            (
                {
                    "task": t.name,
                    "start": t.start,
                    "end": t.end,
                    "completion_ratio": t.completion,
                    "color": t.color,
                    "group": t.group,
                    "duration_days": t.duration_days,
                    "completed_days": t.completed_days,
                }
                for t in self._tasks
            ),
            columns=[
                "task", "start", "end", "completion_ratio", "color", "group",
                "duration_days", "completed_days",
            ],
        )

    def plot(
        self,
        *,
        parameters: PlotParameters | None = None,
        start: DateLike | None = None,
        end: DateLike | None = None,
        show_today: bool = False,
        today: DateLike | None = None,
        show_weekends: bool = False,
        group_colors: Mapping[str, Color] | None = None,
        show_y_labels: bool = True,
        show_bar_labels: bool = True,
        bar_height: float = 0.5,
        bar_alpha: float | None = None,
        # Transitional style overrides for the pre-visualization API.
        title: str | None = None,
        figsize: tuple[float, float] | None = None,
        grid_alpha: float | None = None,
        font_size: float | None = None,
        ax: Axes | None = None,
        show: bool = False,
    ) -> tuple[Figure, Axes]:
        """Render tasks using the package's shared visualization utilities.

        Task management remains independent of Matplotlib. The renderer is
        imported only when this method is called.

        Parameters
        ----------
        parameters : PlotParameters, optional
            Common plotting configuration for typography, colors, figure
            dimensions, grids, axes and legends. The default configuration
            provides a title, date label, vertical grid and 12x6 inch figure.
        start, end : date, datetime or str, optional
            Inclusive visible date limits; inferred from the tasks otherwise.
            These limits take precedence over ``parameters.xlim``.
        show_today : bool, default False
            Draw a marker for today's date and include it in the visible range.
        today : date, datetime or str, optional
            Date used for the marker, useful for reproducible figures/tests.
        show_weekends : bool, default False
            Shade Saturday and Sunday date intervals.
        group_colors : mapping, optional
            Explicit colors for named task groups; overrides the palette.
        show_y_labels : bool, default True
            Show task names on the vertical axis.
        show_bar_labels : bool, default True
            Display task names centered inside their bars.
        bar_height : float, default 0.5
            Bar height as a fraction of one task row, in ``(0, 1]``.
        bar_alpha : float, optional
            Opacity of total-duration bars. Defaults to 0.4 without a
            configuration, or ``parameters.alpha`` otherwise. Completed
            portions remain fully opaque.
        title : str, optional
            Compatibility override for ``parameters.title``.
        figsize : tuple of float, optional
            Compatibility override for ``parameters.figsize`` when creating
            a new figure.
        grid_alpha : float, optional
            Compatibility override for ``parameters.grid_alpha``.
        font_size : float, optional
            Compatibility override for general, tick and legend font sizes.
        ax : matplotlib.axes.Axes, optional
            Existing axes. If omitted, create a new figure.
        show : bool, default False
            Display the figure using the current Matplotlib backend.

        Returns
        -------
        tuple of matplotlib.figure.Figure and matplotlib.axes.Axes
            Figure and modified axes. Artists can be inspected and edited
            using Matplotlib directly.

        Raises
        ------
        ValueError
            If no tasks exist or any plotting parameter is invalid.
        TypeError
            If ``parameters`` is not a PlotParameters instance.
        ImportError
            If Matplotlib is not available.

        Notes
        -----
        Both task start and end dates are inclusive. Unlike the original
        implementation, drawing is delegated to ``visualization.plot_gantt``.
        """
        from .visualization.plot_gantt import render_gantt

        return render_gantt(
            self,
            parameters=parameters,
            start=start,
            end=end,
            show_today=show_today,
            today=today,
            show_weekends=show_weekends,
            group_colors=group_colors,
            show_y_labels=show_y_labels,
            show_bar_labels=show_bar_labels,
            bar_height=bar_height,
            bar_alpha=bar_alpha,
            title=title,
            figsize=figsize,
            grid_alpha=grid_alpha,
            font_size=font_size,
            ax=ax,
            show=show,
        )


__all__ = ["Task", "GanttChart", "add_days"]