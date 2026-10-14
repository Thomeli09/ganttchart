"""Create, manage, and visualize Gantt charts.

Examples
--------
from ganttchart import GanttChart
chart = GanttChart()
chart.add_task("Planning", "2026-10-14", "2026-10-17", completion=0.5)
len(chart.tasks)
1
"""

from .ganttchart import GanttChart, Task, add_days

__all__ = ["GanttChart", "Task", "add_days"]