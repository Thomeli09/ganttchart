"""Render Gantt charts using the shared Matplotlib visualization helpers.

This module knows how to draw tasks; ``ganttchart.ganttchart`` remains
responsible for validating and storing task and date information.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from datetime import date, timedelta
from math import isfinite
from typing import TYPE_CHECKING

import matplotlib.dates as mdates
from matplotlib import rcParams
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.colors import is_color_like, to_rgb
from matplotlib.figure import Figure
from matplotlib.patches import Patch

from .plot_2d import draw_reference_line, draw_span, plot_bars, plot_text
from .plot_basic import add_legend, configure_axes, create_figure, show_figure
from .plot_parameters import PlotParameters

if TYPE_CHECKING:
    from ..ganttchart import Color, DateLike, GanttChart


def _default_parameters() -> PlotParameters:
    """Provide the standard Gantt-specific appearance."""
    return PlotParameters(
        title="Gantt chart",
        xlabel="Date",
        figsize=(12.0, 6.0),
        fontsize=10.0,
        title_size=12.0,
        tick_size=10.0,
        legend_size=10.0,
        show_grid=True,
        grid_axis="x",
        grid_alpha=0.4,
        alpha=0.4,
    )


def _parameters_with_overrides(
    parameters: PlotParameters | None,
    *,
    title: str | None,
    figsize: tuple[float, float] | None,
    grid_alpha: float | None,
    font_size: float | None,
) -> PlotParameters:
    """Build an independent configuration without mutating caller settings."""
    if parameters is not None and not isinstance(parameters, PlotParameters):
        raise TypeError("'parameters' must be a PlotParameters instance or None.")

    options = parameters if parameters is not None else _default_parameters()
    changes: dict[str, object] = {}
    if title is not None:
        changes["title"] = title
    if figsize is not None:
        changes["figsize"] = figsize
    if grid_alpha is not None:
        changes["grid_alpha"] = grid_alpha
    if font_size is not None:
        changes.update(fontsize=font_size, tick_size=font_size, legend_size=font_size)
    return replace(options, **changes) if changes else options


def render_gantt(
    chart: GanttChart,
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
    title: str | None = None,
    figsize: tuple[float, float] | None = None,
    grid_alpha: float | None = None,
    font_size: float | None = None,
    ax: Axes | None = None,
    show: bool = False,
) -> tuple[Figure, Axes]:
    """Draw a Gantt chart with the shared 2D visualization functions.

    Parameters
    ----------
    chart : GanttChart
        Collection of validated, ordered tasks to display.
    parameters : PlotParameters, optional
        General appearance settings. When supplied, the original instance
        is not modified. ``start`` and ``end`` override its x limits.
    start, end : date, datetime or str, optional
        Explicit inclusive date interval. Unspecified bounds are inferred.
    show_today : bool, default False
        Add a marker for the current date and expand the visible interval.
    today : date, datetime or str, optional
        Override the current date for a deterministic marker.
    show_weekends : bool, default False
        Shade visible Saturdays and Sundays.
    group_colors : mapping, optional
        Matplotlib colors assigned to named groups. Groups not included in
        the mapping use the configured palette or Matplotlib color cycle.
    show_y_labels, show_bar_labels : bool, default True
        Control labels beside and inside task bars, respectively.
    bar_height : float, default 0.5
        Row-relative bar thickness in the interval (0, 1].
    bar_alpha : float, optional
        Background-bar opacity. Defaults to the configured alpha.
    title, figsize, grid_alpha, font_size : optional
        Backward-compatible style overrides. Prefer setting these on
        ``parameters`` in new code.
    ax : matplotlib.axes.Axes, optional
        Existing axes, or create a new figure if omitted.
    show : bool, default False
        Display the figure after drawing.

    Returns
    -------
    tuple of matplotlib.figure.Figure and matplotlib.axes.Axes
        The plotted figure and axes.

    Raises
    ------
    ValueError
        If there are no tasks or drawing parameters are invalid.
    TypeError
        If plotting parameters have unsupported types.

    Notes
    -----
    The task end date is inclusive; widths are measured in calendar days.
    Group colors always take precedence over individual task colors.
    """
    if not isinstance(bar_height, (int, float)) or not isfinite(bar_height) or not 0 < bar_height <= 1:
        raise ValueError("'bar_height' must be finite and in (0, 1].")

    options = _parameters_with_overrides(
        parameters,
        title=title,
        figsize=figsize,
        grid_alpha=grid_alpha,
        font_size=font_size,
    )
    background_alpha = options.alpha if bar_alpha is None else bar_alpha
    if not isinstance(background_alpha, (int, float)) or not isfinite(background_alpha) or not 0 <= background_alpha <= 1:
        raise ValueError("'bar_alpha' must be finite and between 0 and 1.")

    # Validate before creating a figure, so errors do not leave empty windows.
    if group_colors is not None:
        for group, color in group_colors.items():
            if color is not None and not is_color_like(color):
                raise ValueError(f"Invalid color for group {group!r}: {color!r}.")
    current: date | None = None
    if show_today:
        # Resolve the date only once so the range and reference line agree.
        from ..ganttchart import _to_date
        current = _to_date(today) if today is not None else date.today()
    first, last = chart.date_range(
        start, end, include_today=show_today, today=current,
    )

    fig: Figure
    if ax is None:
        fig, created_axes = create_figure(parameters=options)
        if not isinstance(created_axes, Axes):
            raise RuntimeError("Expected a single axes from create_figure().")
        ax = created_axes
    else:
        fig = ax.figure

    # Color resolution is deterministic for named task groups. Individual
    # ungrouped tasks can use the configured palette or their own color.
    cycle = list(rcParams["axes.prop_cycle"].by_key().get("color", ["C0"]))
    if not cycle:
        cycle = ["C0"]
    groups = list(dict.fromkeys(task.group for task in chart if task.group is not None))
    assigned: dict[str, Color] = {}
    for group_index, group in enumerate(groups):
        specified = group_colors.get(group) if group_colors is not None else None
        assigned[group] = (
            specified if specified is not None else
            options.color_at(group_index) or cycle[group_index % len(cycle)]
        )

    if show_weekends:
        weekend_options = replace(options, color="lightgrey", palette=(), alpha=0.5, linewidth=0.0, hatch=None)
        day = first
        while day <= last:
            if day.weekday() >= 5:
                span = draw_span(
                    ax, mdates.date2num(day), mdates.date2num(day) + 1,
                    parameters=weekend_options,
                )
                span.set_zorder(0)
            day += timedelta(days=1)

    for index, task in enumerate(chart):
        if task.group is not None:
            color = assigned[task.group]
        else:
            color = task.color if task.color is not None else options.color_at(index)

        left = mdates.date2num(task.start)
        background_style = replace(
            options, color=color, palette=(), alpha=background_alpha,
            linewidth=0.0,
        )
        background = plot_bars(
            ax, [index], [task.duration_days],
            parameters=background_style,
            width=bar_height, horizontal=True, baseline=left,
        )
        background_patch = background.patches[0]
        background_patch.set_zorder(2)

        # Read the actual rendered color (even if the user specified none).
        # Dropping its alpha prevents completion bars inheriting opacity.
        resolved_color = to_rgb(background_patch.get_facecolor())
        if task.completed_days > 0:
            completed_style = replace(
                options, color=resolved_color, palette=(), alpha=1.0,
                linewidth=0.0, hatch=None,
            )
            completed = plot_bars(
                ax, [index], [task.completed_days],
                parameters=completed_style,
                width=bar_height, horizontal=True, baseline=left,
            )
            completed.patches[0].set_zorder(3)

        if show_bar_labels:
            text_style = replace(options, color="black", palette=(), alpha=1.0)
            label = plot_text(
                ax, (left + task.duration_days / 2, index), task.name,
                parameters=text_style,
            )
            label.set_zorder(4)

    legend_handles: list[Artist] = [
        Patch(facecolor=color, label=group)
        for group, color in assigned.items()
    ]
    if show_today:
        assert current is not None
        today_style = replace(
            options, color="red", palette=(), alpha=1.0,
            linewidth=1.5, linestyle="--",
        )
        marker = draw_reference_line(
            ax, mdates.date2num(current), parameters=today_style,
            label="Today",
        )
        marker.set_zorder(5)
        legend_handles.append(marker)

    # Configure generic typography, axis scales, grid and box in one place.
    # Avoid automatic legend creation until all Gantt group proxies exist.
    right_exclusive = mdates.date2num(last) + 1
    axes_style = replace(
        options,
        xlim=(mdates.date2num(first), right_exclusive),
        show_legend=False,
    )
    ax.set_axisbelow(True)
    configure_axes(ax, axes_style)
    ax.set_yticks(range(len(chart)))
    ax.set_yticklabels([task.name for task in chart])
    ax.tick_params(axis="y", labelleft=show_y_labels)
    if not ax.yaxis_inverted():
        ax.invert_yaxis()

    # Respect custom date formats. Otherwise use Matplotlib's concise dates.
    locator = mdates.AutoDateLocator()
    ax.xaxis.set_major_locator(locator)
    if options.date_format is None:
        ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

    if options.show_legend and legend_handles:
        add_legend(ax, options, handles=legend_handles)
    if show:
        show_figure(fig)
    return fig, ax


__all__ = ["render_gantt"]

