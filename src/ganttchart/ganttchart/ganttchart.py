# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:16:55 2024

@author: Thommes Eliott
"""

# GanttChart library
from datetime import datetime
from queue import Empty
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

# Custom Lib
from PlotLib import ParamPLT, PLTGrid, PLTLimit


"""
Tasks class
"""
class Tasks:
    def __init__(self):
        self.LTask = []
        self.PandasStruct = False
        self.BColorGroups = False

    @property
    def getLTask(self):
        """Getter for the list of tasks."""
        return self.LTask

    def AddTask(self, Title, StartDate, EndDate, CompletionRatio=0, Color=None, BColorGroup=False):
        """
        Add a task.

        - paramPLT: An instance of ParamPLT for plot styling.
        - start_date: Optional start date for the plot (YYYY-MM-DD format).
        - end_date: Optional end date for the plot (YYYY-MM-DD format).
        """
        self.LTask.append({
            "task": Title,
            "start": StartDate,
            "end": EndDate,
            "completion_ratio": CompletionRatio,
            "color": Color})

        self.getBColorGroups = BColorGroup

    @property
    def getPandasStruct(self):
        """Getter for the PandasStruct."""
        return self.PandasStruct

    @property
    def SetPandasStruct(self):
        if not self.getLTask:
            print("Error: No tasks.")
            return

        # Create DataFrame from the list of tasks
        self.PandasStruct = pd.DataFrame(self.getLTask)

    @property
    def getBColorGroups(self):
        """Getter for the BColorGroup."""
        return self.BColorGroups

    @getBColorGroups.setter
    def getBColorGroups(self, Value):
        """Setter for the BColorGroups."""
        self.BColorGroups = Value

    def RangePLT(self, StartDate=None, EndDate=None, BCurrentDate=False):
        """Return the range of dates for the plot."""
        if not self.getLTask:
            print("Error: No tasks.")
            return []

        if Empty(self.getPandasStruct):
            self.SetPandasStruct

        df = self.getPandasStruct
        df["start"] = pd.to_datetime(df["start"])
        df["end"] = pd.to_datetime(df["end"])

        if StartDate is None:
            StartDate = df["start"].min()
        else:
            StartDate = pd.to_datetime(StartDate)

        if EndDate is None:
            EndDate = df["end"].max()
        else:
            EndDate = pd.to_datetime(EndDate)

        if BCurrentDate:
            CurrentDate = datetime.now()
            StartDate = min(StartDate, CurrentDate)
            EndDate = max(EndDate, CurrentDate)

        return [StartDate, EndDate]

    def PLTTasks(self, paramPLT, StartDate=None, EndDate=None, BCurrentDate=False,
                 BWeekEnds=False, GroupsColors=None, BYTicks=True):
        """Plot the Gantt chart of tasks."""
        if not self.getLTask:
            print("Error: No tasks to plot.")
            return

        # Create DataFrame from the list of tasks
        self.SetPandasStruct
        df = self.getPandasStruct

        df["start"] = pd.to_datetime(df["start"])
        df["end"] = pd.to_datetime(df["end"])
        df["duration"] = (df["end"] - df["start"]).dt.days
        df["completion_days"] = df["completion_ratio"] * df["duration"]

        # Determine the plot start and end dates
        Range = self.RangePLT(StartDate=StartDate, EndDate=EndDate, BCurrentDate=BCurrentDate)
        StartDate, EndDate = Range[0], Range[1]

        # Plotting the Gantt chart     
        fig, ax = plt.subplots()
        # fig, ax = plt.subplots(figsize=(paramPLT.fig_width, paramPLT.fig_height))

        YPositions = range(len(df))

        if BWeekEnds:
            # Plot weekends
            TempDate = StartDate
            while TempDate <= EndDate:
                if TempDate.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                    ax.axvspan(TempDate, TempDate+pd.Timedelta(days=1),
                               color='lightgrey', alpha=0.5, label='Weekend' if TempDate == StartDate else None)
                TempDate += pd.Timedelta(days=1)

        for i, task in enumerate(df.itertuples()):
            task.color
            if self.getBColorGroups:
                TaskColor = GroupsColors[task.color]
            else:
                TaskColor = task.color

            if task.duration<1:
                Duration = 1
                Completion_days = task.completion_ratio * 1
            else:
                Duration = task.duration+1
                Completion_days = (task.duration+1) * task.completion_ratio

            # Adding a lower bar - for the overall task duration
            Bars = plt.barh(i, width=Duration, left=task.start, height=0.4, color=TaskColor, alpha=paramPLT.getAlpha)
            BarColors = [Bar.get_facecolor() for Bar in Bars]
            # Adding an upper bar - for the status of completion
            plt.barh(i, width=Completion_days, left=task.start, height=0.4, color=BarColors[0])

            ax.text(task.start + pd.Timedelta(days=Duration/2), i,
                    task.task, ha='center', va='center', color='k', fontsize=paramPLT.getTicksSize)

        if BCurrentDate:
            CurrentDate = pd.to_datetime(datetime.now().strftime('%Y-%m-%d'))
            ax.axvline(x=CurrentDate, color='r', linestyle='dashed', label='Current day')
            ax.text(x=CurrentDate + pd.Timedelta(days=1), y=len(df) - 1,
                    s=CurrentDate.strftime('%d/%m/%Y'), color='r', fontsize=paramPLT.getTicksSize)

        # Formatting the plot
        ax.set_xlabel("Date", fontsize=paramPLT.getFontSize)
        ax.tick_params(axis='x', labelsize=paramPLT.getTicksSize)
        if BYTicks:
            # Show y-axis tick labels
            ax.set_yticklabels(df["task"], fontsize=paramPLT.getFontSize)
        else:
            # Remove y-axis tick labels
            ax.set_yticklabels([])
        ax.set_yticks(YPositions)

        paramPLT.getXLimit = [StartDate, EndDate + pd.Timedelta(days=1)]
        PLTLimit(paramPLT)

        plt.gca().invert_yaxis()

        paramPLT.getGridAlpha = 0.4
        PLTGrid(paramPLT)

        plt.title(paramPLT.getTitle, fontsize=paramPLT.getTitleSize)

        if self.getBColorGroups:
            patches = []
            for Item in GroupsColors:
                patches.append(matplotlib.patches.Patch(color=GroupsColors[Item], alpha=paramPLT.getAlpha))
            plt.legend(handles=patches, labels=GroupsColors.keys(), fontsize=paramPLT.getFontSize, loc=paramPLT.getLegendsLoc)

        plt.show(block=False)


def DatePlusNumDays(Date, NumDays):
    """Return the date after adding a number of days."""
    Temp = pd.to_datetime(Date) + pd.Timedelta(days=NumDays)
    return f'{Temp.strftime("%Y-%m-%d")}'

"""
-------
Example
-------
# Default use of the Tasks class
from PlotLib import ParamPLT, PLTGrid, PLTLimit, ClosePlotsOnDemand

# Define the Tasks instance
my_tasks = Tasks()

# Add tasks to the agenda
my_tasks.AddTask(Title="Project Planning",
                 StartDate="2024-01-01", EndDate="2024-06-30",
                 CompletionRatio=1, Color=None)
my_tasks.AddTask(Title="Development Phase 1",
                 StartDate="2024-07-01", EndDate="2025-06-30",
                 CompletionRatio=0.9, Color=None)
my_tasks.AddTask(Title="Testing Phase",
                 StartDate="2025-07-01", EndDate="2026-03-31",
                 CompletionRatio=0.5, Color=None)
my_tasks.AddTask(Title="Development Phase 2",
                 StartDate="2026-04-01", EndDate="2027-06-30",
                 CompletionRatio=0.25, Color=None)
my_tasks.AddTask(Title="Final Review",
                 StartDate="2027-07-01", EndDate="2027-12-31",
                 CompletionRatio=0, Color=None)

# Plot the tasks with default date range
paramPLT = ParamPLT(colour=['k'], linetype=0, marker=0, linesize=16, fontsize=10, scale=1, scale3D=None)

my_tasks.PLTTasks(paramPLT, StartDate=None, EndDate=None, BCurrentDate=True)

# Plot the tasks with a user-defined date range
paramPLT = ParamPLT(colour=['k'], linetype=0, marker=0, linesize=16, fontsize=10, scale=1, scale3D=None)
paramPLT.getGridAxis = 'x'

my_tasks.PLTTasks(paramPLT, StartDate="2024-10-01", EndDate="2028-01-01", BCurrentDate=True)

# Grouping Tasks by Colors with Legends

# Define the Tasks instance
my_tasks = Tasks()

# Add grouped tasks
my_tasks.AddTask(Title="Project Planning",
                 StartDate="2024-01-01", EndDate="2024-06-30",
                 CompletionRatio=1, Color='Accounting')
my_tasks.AddTask(Title="Development Phase 1",
                 StartDate="2024-07-01", EndDate="2025-06-30",
                 CompletionRatio=0.9, Color='IT')
my_tasks.AddTask(Title="Testing Phase",
                 StartDate="2025-07-01", EndDate="2026-03-31",
                 CompletionRatio=0.5, Color='Accounting')
my_tasks.AddTask(Title="Development Phase 2",
                 StartDate="2026-04-01", EndDate="2027-06-30",
                 CompletionRatio=0.25, Color='IT')
my_tasks.AddTask(Title="Final Review",
                 StartDate="2027-07-01", EndDate="2027-12-31",
                 CompletionRatio=0, Color='Sales')

# Enable color grouping
my_tasks.getBColorGroups = True

# Define color mapping for groups
GroupsColors = {'IT': 'b', 'Sales': 'y', 'Accounting': 'r'}

# Plot with group colors and legend
paramPLT = ParamPLT(colour=['k'], linetype=0, marker=0, linesize=16, fontsize=10, scale=1, scale3D=None)
paramplt.getTitle = 'Project Timeline'
paramPLT.getGridAxis = 'x'

my_tasks.PLTTasks(paramPLT, BCurrentDate=True, BWeekEnds=False, GroupsColors=GroupsColors)

# Close all plots on demand
ClosePlotsOnDemand()
"""
