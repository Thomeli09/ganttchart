"""Optional Pandas integration: export a schedule as a CSV file.

Install: python -m pip install -e '.[data]'
Run:     python examples/04_gantt_dataframe.py
"""

from __future__ import annotations

import os
from pathlib import Path

from ganttchart import GanttChart


def main() -> Path:
    chart = GanttChart()
    chart.add_task("Planning", "2026-10-01", "2026-10-08", completion=1.0)
    chart.add_task("Execution", "2026-10-09", "2026-10-21", completion=0.4)
    frame = chart.to_dataframe()  # Pandas is imported lazily by this method.
    output = Path(os.environ.get("GANTTCHART_EXAMPLE_OUTPUT", Path(__file__).parent / "output"))
    output.mkdir(parents=True, exist_ok=True)
    path = output / "04_schedule.csv"
    frame.to_csv(path, index=False)
    print(frame[["task", "duration_days", "completion_ratio"]].to_string(index=False))
    print(f"Saved: {path}")
    return path


if __name__ == "__main__":
    main()
