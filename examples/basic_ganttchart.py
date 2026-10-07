"""
-------
Example
-------
"""

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

