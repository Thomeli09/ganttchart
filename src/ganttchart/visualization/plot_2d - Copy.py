# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 14:15:29 2024

@author: Thommes Eliott
"""

# General Plotting library
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import axes, colors, cm
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.cm import ScalarMappable
import numpy as np
from highlight_text import fig_text
import os

from pytest import param


# Custom Lib
from DataManagementLib import LenData


"""
Type de Plots
"""
# 2D


def PLTText(XY, Text, paramPLT, FontFamily=0, FontStyle=0, FontWeight=0, HAlignement=0, Rotation=-1, RotationMode=0, BAbsoluteCoord=True):
    """
    Adds text to a plot at specified coordinates with customizable parameters.

    Args:
        XY (tuple): Coordinates (x, y) where the text will be placed.
        Text (str): The text to be displayed on the plot.
        paramPLT (object): Object containing plot parameters.
        FontFamily (int): Integer value representing the font family.
        FontStyle (int): Integer value representing the font style.
        FontWeight (int): Integer value representing the font weight.
        HAlignement (int): Integer value representing the horizontal alignment of the text.
        Rotation (int or float): Angle of rotation for the text.
        RotationMode (int): Mode of rotation (0 for default, 1 for anchor).
        BAbsoluteCoord (bool): If True, the coordinates are in absolute terms; if False, they are relative to the axes.

    Returns:
        None: This function does not return anything. It simply adds text to the plot.
    """
    # Dictionary mapping integer values to font families
    TextFontDict = {0: 'sans-serif', 1: 'serif', 2: 'cursive', 3: 'fantasy', 4: 'monospace'}
    FontFamily = TextFontDict.get(FontFamily, 'sans-serif')

    # Dictionary mapping integer values to fontstyles
    TextFontStyleDict = {0: 'normal', 1: 'italic', 2: 'oblique'}
    FontStyle = TextFontStyleDict.get(FontStyle, 'normal')

    # Dictionary mapping integer values to font weights
    TextFontWeightDict = {0: 'normal', 1: 'ultralight', 2: 'light', 3: 'regular', 4: 'book', 5: 'medium', 6: 'roman',
                      7: 'semibold', 8: 'demibold', 9: 'bold', 10: 'heavy', 11: 'extra bold', 12: 'black'}
    FontWeight = TextFontWeightDict.get(FontWeight, 'normal')

    # Dictionary mapping integer values to horizontal alignment
    TextHAlignementDict = {0: 'center', 1: 'left', 2: 'right'}
    HAlignement = TextHAlignementDict.get(HAlignement, 'center')

    # Dictionary mapping integer values to rotation
    TextRotationDict = {-1: 'horizontal', -2: 'vertical'}
    Rotation = TextRotationDict.get(Rotation, Rotation)

    # Dictionary mapping integer values to rotation mode
    TextRotationModeDict = {0: 'default', 1: 'anchor'}
    RotationMode = TextRotationModeDict.get(RotationMode, 'default')

    # Position in absolute coordinates or relative to the axes
    CoordType = None
    if not BAbsoluteCoord:
        ax = plt.gca()
        CoordType = ax.transAxes

    # Based on stored Ax or on Ax from plt.gca()
    if paramPLT.getBAxes:
        Ax = paramPLT.getLastAx
    else:
        Ax = plt.gca()
       
    if Ax is not None:
        Ax.text(x=XY[0], y=XY[1], s=Text,
                color=paramPLT.getColour, alpha=paramPLT.getAlpha,
                fontfamily=FontFamily, fontstyle=FontStyle, fontweight=FontWeight, fontsize=paramPLT.getTicksSize,
                horizontalalignment=HAlignement, rotation=Rotation, rotation_mode=RotationMode, bbox=dict(facecolor='white', alpha=0.5, edgecolor='k'))
        # transform=CoordType

def PLTPlot(XValues, YValues, paramPLT):
    """
    Creates a 2D plot using customizable parameters.

    Args:
        XValues (list ou array-like): X-axis values for the plot.
        YValues (list ou array-like): Y-axis values for the plot.
        paramPLT (objet): Object containing plot parameters.

    Returns:
        None: This function does not return anything. It simply displays the plot.
    """
    ln = plt.plot(XValues, YValues,
                  color=paramPLT.getColour,
                  alpha=paramPLT.getAlpha,
                  linestyle=paramPLT.getLineType,
                  linewidth=paramPLT.getLineSize,
                  marker=paramPLT.getMarker,
                  markersize=paramPLT.getMarkerSize,
                  label=paramPLT.getLegends)

    paramPLT.getPlottedObject = ln[0]  # Store the line object for later use

def PLTEmptyPlot(paramPLT):
    """
    Creates an empty plot with customizable parameters.
    Args:
        paramPLT (object): Object containing plot parameters.
    Returns:
        None: This function does not return anything. It simply displays the empty plot.
    """
    PLTPlot(XValues=[], YValues=[], paramPLT=paramPLT)

def PLTUpdatePlot(XValues, YValues, paramPLT, index):
    """
    Updates an existing plot with new X and Y values.
    Args:
    - XValues (list or array-like): New X-axis values for the plot.
    - YValues (list or array-like): New Y-axis values for the plot.
    - paramPLT (object): Object containing plot parameters.
    - index (int): Index of the line to update in the current axis.
    Returns:
    None: This function does not return anything. It simply updates the existing plot with new data.
    """
    Line = paramPLT.getPlottedObjectFromIndex(index)
    if isinstance(Line, Line2D):
        Line.set_data(XValues, YValues)
    else:
        print(f"Warning: The object at index {index} is not a Line2D object and cannot be updated.")

def PLTPlotSeries(LXValues, LYValues, paramPLT):
    """
    Creates a 2D plot with multiple curves from lists of X and Y values.

    Args:
        LXValues (list of lists or array-like): List of X-axis values for each curve.
        LYValues (list of lists or array-like): List of Y-axis values for each curve.
        paramPLT (object): Object containing plot parameters.

    Returns:
        None: This function does not return anything. It simply displays the plot.
    """

    for XValues, YValues in zip(LXValues, LYValues):
        PLTPlot(XValues, YValues, paramPLT)


def PLTVHLine(Val, paramPLT, BRelative=True, SecValMin=0, SecValMax=1, BOrientation=True):
    """
    Plots a vertical or horizontal line on the plot, based on the specified parameters.

    Args:
    - Val (float): Value at which to draw the line (x-coordinate for vertical line, y-coordinate for horizontal line),
        but allows Array-like input to draw multiple lines only if BRelative is False.
    - paramPLT (object): Object containing plot parameters.
    - BRelative (bool): Boolean flag to specify if the secondary axis values are in relative units (0 to 1) or absolute units.
    - SecValMin (float): Minimum value for the secondary axis (y-axis for vertical line, x-axis for horizontal line) 
        and is in relative units (0 to 1) or absolute units based on BRelative.
    - SecValMax (float): Maximum value for the secondary axis (y-axis for vertical line, x-axis for horizontal line) 
        and is in relative units (0 to 1) or absolute units based on BRelative.
    - BOrientation (bool): Boolean flag to specify the orientation of the line.
    """
    if BOrientation:  # Vertical line
        if BRelative:
            plt.axvline(x=Val, ymin=SecValMin, ymax=SecValMax,
                        color=paramPLT.getColour, linestyle=paramPLT.getLineType, linewidth=paramPLT.getLineSize,
                        marker=paramPLT.getMarker, markersize=paramPLT.getMarkerSize, 
                        alpha=paramPLT.getAlpha, label=paramPLT.getLegends)
        else:
            plt.vlines(x=Val, ymin=SecValMin, ymax=SecValMax,
                       color=paramPLT.getColour, linestyle=paramPLT.getLineType, linewidth=paramPLT.getLineSize,
                       marker=paramPLT.getMarker, markersize=paramPLT.getMarkerSize, 
                       alpha=paramPLT.getAlpha, label=paramPLT.getLegends)
    elif BOrientation == False:  # Horizontal line
        if BRelative:
            plt.axhline(y=Val, xmin=SecValMin, xmax=SecValMax,
                        color=paramPLT.getColour, linestyle=paramPLT.getLineType, linewidth=paramPLT.getLineSize,
                        marker=paramPLT.getMarker, markersize=paramPLT.getMarkerSize, 
                        alpha=paramPLT.getAlpha, label=paramPLT.getLegends)
        else:
            plt.hlines(y=Val, xmin=SecValMin, xmax=SecValMax,
                       color=paramPLT.getColour, linestyle=paramPLT.getLineType, linewidth=paramPLT.getLineSize,
                       marker=paramPLT.getMarker, markersize=paramPLT.getMarkerSize, 
                       alpha=paramPLT.getAlpha, label=paramPLT.getLegends)


def PLTAXLine(XY1, paramPLT,XY2=(0,0), Slope=None):
    """
    Plots an infinite line defined by two points or a point and a slope.

    Args:
    - XY1 (tuple): Coordinates of the first point (x1, y1).
    - paramPLT (object): Object containing plot parameters.
    - XY2 (tuple): Coordinates of the second point (x2, y2). Default is (0, 0).
    - Slope (float): Slope of the line. If provided, XY2 is ignored.

    Returns:
    - None: This function does not return anything. It simply displays the line on the plot.
    """
    if Slope is not None:
        plt.axline(xy=XY1, slope=Slope,
                   color=paramPLT.getColour, linestyle=paramPLT.getLineType, linewidth=paramPLT.getLineSize,
                   marker=paramPLT.getMarker, markersize=paramPLT.getMarkerSize,
                   alpha=paramPLT.getAlpha, label=paramPLT.getLegends)
    else:
        plt.axline(xy1=XY1, xy2=XY2,
                   color=paramPLT.getColour, linestyle=paramPLT.getLineType, linewidth=paramPLT.getLineSize,
                   marker=paramPLT.getMarker, markersize=paramPLT.getMarkerSize,
                   alpha=paramPLT.getAlpha, label=paramPLT.getLegends)


def PLTCoordsSpan(ValMin, ValMax, paramPLT, SecValMin=0, SecValMax=1, BOrientation=True):
    """
    Plots a shaded span (rectangle) on the plot, either vertically or horizontally, based on the specified parameters.

    Args:
    - ValMin (float): Minimum value for the primary axis (x-axis for vertical span, y-axis for horizontal span).
    - ValMax (float): Maximum value for the primary axis (x-axis for vertical span, y-axis for horizontal span).
    - paramPLT (object): Object containing plot parameters.
    - SecValMin (float): Minimum value for the secondary axis (y-axis for vertical span, x-axis for horizontal span) and is in relative units (0 to 1).
    - SecValMax (float): Maximum value for the secondary axis (y-axis for vertical span, x-axis for horizontal span) and is in relative units (0 to 1).
    - BOrientation (bool): Boolean flag to specify the orientation of the span.
    """
    if BOrientation:  # Vertical line
        plt.axvspan(xmin=ValMin, xmax=ValMax, ymin=SecValMin, ymax=SecValMax,
                    facecolor=paramPLT.getColour, hatch=paramPLT.getHatch,
                    edgecolor=paramPLT.getColour, linestyle=paramPLT.getLineType, linewidth=paramPLT.getLineSize, alpha=paramPLT.getAlpha,
                    label=paramPLT.getLegends)

    elif BOrientation == False:
        plt.axhspan(ymin=ValMin, ymax=ValMax, xmin=SecValMin, xmax=SecValMax,
                    facecolor=paramPLT.getColour, hatch=paramPLT.getHatch,
                    edgecolor=paramPLT.getColour, linestyle=paramPLT.getLineType, linewidth=paramPLT.getLineSize, alpha=paramPLT.getAlpha,
                    label=paramPLT.getLegends)


def PLTFill(XValues, YValues, paramPLT, ValZOrder=0, YValuesSec=False):
    """
    Creates a filled plot between two curves (primary and secondary) using customizable parameters.

    Args:
    - XValues (list or array-like): X-axis values.
    - YValues (list or array-like): Y-axis values for the primary curve.
    - paramPLT (object): Object containing plot parameters.
    - ValZOrder (int): Z-order value to determine which layer is on top.
    - YValuesSec (list or array-like): Y-axis values for the secondary curve (optional).
    """
    if YValuesSec:
        plt.fill_between(XValues, YValues, YValuesSec,
                         facecolor=paramPLT.getColour, edgecolor=paramPLT.getColour,
                         hatch=paramPLT.getHatch, alpha=paramPLT.getAlpha, zorder=ValZOrder,
                         label=paramPLT.getLegends)
    else:
        plt.fill(XValues, YValues,
                 facecolor=paramPLT.getColour, edgecolor=paramPLT.getColour,
                 hatch=paramPLT.getHatch, alpha=paramPLT.getAlpha, zorder=ValZOrder,
                 label=paramPLT.getLegends)


def PLTBar(XBars, Heights, paramPLT, Width=0.8, StdErrors=None, BOrientation=True, Bottom=0):
    """
    Creates a bar plot with optional error bars, customizable Colours, labels, and orientation.

    Args:
    - XBars: List or array of x-coordinates for the bars or labels of each bar
    - Heights: List or array of heights for each bar or values of each bar
    - paramPLT: An object containing plot parameters 
    - Width: Width of each bar (default is 0.8) and can be specified for all bars or individually
    - StdErrors (optional): List or array of standard errors for each bar.
        - Scalar: Symmetric +/- error for all bars.
        - Shape (N,): Symmetric +/- error for each bar.
        - Shape (2, N): Asymmetric error values where:
            - First row specifies lower errors.
            - Second row specifies upper errors.
    - BOrientation: Boolean flag to specify the orientation of the bars.
        - True: Vertical bar plot (default).
        - False: Horizontal bar plot.
    - Bottom: Y-coordinate of the bottom of each bar (default is 0) and can be specified for all bars or individually

    Returns:
        None: This function does not return anything. It simply displays the bar plot.

    Improovements:
    
    """
    if BOrientation:
        # Scale type for Y axis
        if paramPLT.getYScaleType:
            BLogScale = True if paramPLT.getYScaleType == 'log' else False
        elif paramPLT.getGenericScaleType:
            BLogScale = True if paramPLT.getGenericScaleType == 'log' else False
        plt.bar(x=XBars, height=Heights, width=Width, yerr=StdErrors, ecolor='k',
                facecolor=paramPLT.getcolorFullList(BEmptying=False), edgecolor=paramPLT.getColourFullList(), 
                align='center', bottom=Bottom, label=paramPLT.getLegends)
    else:
        # Scale type for X axis
        if paramPLT.getXScaleType:
            BLogScale = True if paramPLT.getXScaleType == 'log' else False
        elif paramPLT.getGenericScaleType:
            BLogScale = True if paramPLT.getGenericScaleType == 'log' else False
        plt.barh(y=XBars, height=Width, width=Heights, yerr=StdErrors, ecolor='k',
                facecolor=paramPLT.getColourFullList(BEmptying=False), edgecolor=paramPLT.getColourFullList(), 
                align='center', left=Bottom, label=paramPLT.getLegends)


def PLTHist(XValues, paramPLT, NBins=0, HistType=0, BNormalizeArea=False, BStacked=False, BCumulative=False, Weights=None, HeightShift=None):
    """
    Creates a histogram plot using customizable parameters.
    
    Args:
    - XValues (list or array-like): Data values for the histogram.
    - paramPLT (object): Object containing plot parameters.
    - NBins (int): Number of bins or binning strategy:
        0: 'auto' (default)
        -1: 'fd' (Freedman-Diaconis Estimator)
        -2: 'doane' (Doane's formula)
        -3: 'scott' (Scott's rule)
        -4: 'stone' (Stone's rule)
        -5: 'rice' (Rice rule)
        -6: 'sturges' (Sturges' formula)
        -7: 'sqrt' (Square root choice)
        Or: Exact number of bins
    - HistType (int): Type of histogram:
        0: 'bar' (default)
        1: 'barstacked'
        2: 'step'
        3: 'stepfilled'
    - BNormalizeArea (bool): Whether to normalize the histogram area to 1.
    - BStacked (bool): Whether to stack multiple histograms.
    - BCumulative (bool): Whether to compute a cumulative histogram.
    - Weights (list or array-like): Weights for each value in XValues.
    - HeightShift (float): Value to shift the height of the histogram bars.

    Returns:
    - None: This function does not return anything. It simply displays the histogram.
    """
    # Dict to map NBins values to matplotlib options
    NBinsDIct = {0: 'auto', -1: 'fd', -2: 'doane', -3: 'scott', -4: 'stone', -5: 'rice', -6: 'sturges', -7: 'sqrt'}
    NBins = NBinsDIct.get(NBins, int(abs(NBins)))  # Default to absolute value if not in dict

    # Dict to map histogram type values to matplotlib options
    HistTypeDict = {0: 'bar', 1: 'barstacked', 2: 'step', 3: 'stepfilled'}
    HistType = HistTypeDict.get(HistType, 'bar')  # Default to 'bar' if not in dict
    
    # Scale type for Y axis
    if paramPLT.getYScaleType:
        BLogScale = True if paramPLT.getYScaleType == 'log' else False
    elif paramPLT.getGenericScaleType:
        BLogScale = True if paramPLT.getGenericScaleType == 'log' else False

    im = plt.hist(XValues, bins=NBins, density=BNormalizeArea, stacked=BStacked, cumulative=BCumulative, weights=Weights,
             bottom=HeightShift, histtype=HistType, align='mid', orientation='vertical', rwidth=None, log=BLogScale, 
             color=paramPLT.getColour, label=paramPLT.getLegends)

   
def PLTHist2D(XValues, YValues, paramPLT, NBins=10, BNormalizeArea=False, BCumulative=False, 
              CountMin=None, CountMax=None, ValMin=None, ValMax=None, Weights=None):
    """
    Creates a 2D histogram plot using customizable parameters.

    Args:
    - XValues (list or array-like): X-axis data values for the histogram.
    - YValues (list or array-like): Y-axis data values for the histogram.
    - paramPLT (object): Object containing plot parameters.
    - NBins : Number of bins:
        - If int, the number of bins for the two dimensions (nx = ny = bins).
        - If [int, int], the number of bins in each dimension (nx, ny = bins).
        - If array-like, the bin edges for the two dimensions (x_edges = y_edges = bins).
        - If [array, array], the bin edges in each dimension (x_edges, y_edges = bins)
    - BNormalizeArea (bool): Whether to normalize the histogram area to 1.
    - BCumulative (bool): Whether to compute a cumulative histogram.
    - Weights (list or array-like): Weights for each value in XValues and YValues.
    - CountMin (float): Minimum count threshold to display a bin.
    - CountMax (float): Maximum count threshold to display a bin.
    - ValMin (float): Minimum value for the Colour scale.
    - ValMax (float): Maximum value for the Colour scale.

    Returns:
    - None: This function does not return anything. It simply displays the 2D histogram.
    """

    counts, xedges, yedges, im = plt.hist2d(XValues, YValues, bins=NBins, density=BNormalizeArea, weights=Weights, cmin=CountMin, cmax=CountMax,
               cmap=paramPLT.getColourMap, norm=None, vmin=ValMin, vmax=ValMax, alpha=paramPLT.getAlpha)
    paramPLT.getMappable = im  # Store the mappable object for Colourbar


def PLTPie(Val, Labels, paramPLT, TypeAutopct=0, PrecisionPct=1, AbsUnit="", PrecisionAbs=0, 
           Radius=1, StartAngle=0, LabelDist=1.25, PctDist=0.6, BShadow=False, explode=None, 
           EnableAnnotations=False):
    """
    Creates a pie plot with customizable options, including optional annotations.

    Args:
    - Val (list): Values for the pie chart.
    - Labels (list): Labels for each slice of the pie chart.
    - paramPLT (object): Object containing plot parameters (e.g., getColour, getHatch).
    - TypeAutopct (int): Type of percentage display:
        0: Display only percentages (%).
        1: Display absolute values.
        2: Display both percentages and absolute values.
    - PrecisionPct (int): Decimal precision for percentages (e.g., 1 for 1 decimal place).
    - AbsUnit (str): Unit for absolute values (e.g., 'g', 'kg').
    - PrecisionAbs (int): Decimal precision for absolute values (e.g., 2 for 2 decimal places).
    - Radius (float): Radius of the pie chart.
    - StartAngle (float): Starting angle for the pie chart, in degrees.
    - LabelDist (float): Distance of labels from the center of the pie chart, as a fraction of the radius.
    - PctDist (float): Distance of percentage values from the center of the pie chart, as a fraction of the radius.
    - BShadow (bool): Whether to add a shadow effect to the pie chart.
    - explode (list): Fraction by which to offset a slice from the pie (e.g., [0, 0.1, 0, 0]).
    - EnableAnnotations (bool): Whether to add annotations (e.g., arrows and labels) to the pie chart.

    Returns:
    - Displays a pie chart.

    Improvements:
    - Ajouter des vérifications entre les paramètres pour éviter les conflits.
    - Extraire un nombre limité de paramètres pour éviter des clash si plus de valeurs.
    """

    paramPLT.getLegends = Labels
    paramPLT.getColour = [colors.to_rgba(c) for c in paramPLT.getColourFullList(BEmptying=True)]

    def GeneAutopct(pct, allvals):
        absolute = np.round(pct / 100. * np.sum(allvals), PrecisionAbs)
        if TypeAutopct <= 0:
            return f"{pct:.{PrecisionPct}f}%"
        elif TypeAutopct == 1:
            return f"{absolute:.{PrecisionAbs}f} {AbsUnit}"
        elif TypeAutopct == 2:
            return f""
        elif TypeAutopct >= 3:
            return f"{pct:.{PrecisionPct}f}%\n({absolute:.{PrecisionAbs}f} {AbsUnit})"

    # Generate the pie chart
    LLegends = paramPLT.getLegendsFullList(BEmptying=EnableAnnotations)
    wedges, texts, autotexts = plt.pie(Val, labels=paramPLT.getLegendsFullList(), labeldistance=LabelDist,
                                       autopct=lambda pct: GeneAutopct(pct, Val), pctdistance=PctDist,
                                       colors=paramPLT.getColourFullList(), hatch=paramPLT.getHatchFullList(),
                                       radius=Radius, startangle=StartAngle,
                                       explode=explode, shadow=BShadow,
                                       textprops=dict(size=paramPLT.getFontSize, color="k"))  # Customize text properties

    # Optional Annotation logic
    if EnableAnnotations:
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="w", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            plt.annotate(LLegends[i],  # Use legend text
                         xy=(x, y), 
                         xytext=(1.35 * Radius * np.sign(x), 1.4 * Radius * y),
                         fontsize=paramPLT.getFontSize,
                         horizontalalignment=horizontalalignment, 
                         **kw)

    # Remove axes and box for pie chart
    paramPLT.getXScaleType = 8
    paramPLT.getYScaleType = 8
    paramPLT.getBBox = False
    # Remove grid and legends
    paramPLT.getGridAxis = None
    paramPLT.getBLegends = False

def PLTImShow(ValMatrix, paramPLT, FInterpolType=0, BOrigin=True, BShowVal=True, Fmt=".2f"):
    """
    Displays an image plot of the provided matrix using custom parameters.
    """
    InterpolDict = {0: 'none', 1: 'auto', 2: 'nearest', 3: 'bilinear', 4: 'bicubic',
                    5: 'spline16', 6: 'spline36', 7: 'hanning', 8: 'hamming',
                    9: 'hermite', 10: 'kaiser', 11: 'quadric', 12: 'catrom',
                    13: 'gaussian', 14: 'bessel', 15: 'mitchell', 16: 'sinc', 17: 'lanczos',
                    18: 'blackman'}
    InterpolType = InterpolDict.get(FInterpolType, 'none')
    
    TypeOrigin =  'upper' if BOrigin else 'lower'

    plt.imshow(ValMatrix, cmap=paramPLT.getColourMap, alpha=paramPLT.getAlpha,
               norm=paramPLT.GenericScaleType, interpolation=InterpolType,
               origin=TypeOrigin)

    if BShowVal:
        Rows, Cols = ValMatrix.shape
        for i in range(Rows):
            for j in range(Cols):
                plt.text(j, i, format(ValMatrix[i, j], Fmt),
                         color="black",fontsize=paramPLT.getFontSize, fontweight="bold",
                         ha='center', va='center')

    PLTColourBar(paramPLT)

    

# 2D Shapes
def PLT2DCircle(x, y, NPoints, Radius, paramPLT, BFill=False):
    # Calculate the angles for the tick marks
    Angles = np.linspace(0, 2*np.pi, NPoints+1, endpoint=True)
    PreVal = False
    xEnd = 0
    yEnd = 0
    XPoint = []
    YPoint = []
    for Angle in Angles:
        # Starting point of the tick (on the circle)
        xStart = x + Radius*np.cos(Angle)
        yStart = y + Radius*np.sin(Angle)

        if PreVal:
            plt.plot([xStart, xEnd],
                     [yStart, yEnd],
                     color=paramPLT.getColour,
                     linestyle=paramPLT.getLineType,
                     marker=paramPLT.getMarker,
                     linewidth=paramPLT.getLineSize,
                     markersize=paramPLT.getLineSize,
                     label=paramPLT.getLegends)
            XPoint.append(xEnd)
            YPoint.append(yEnd)
        else:
            PreVal = True
        xEnd = xStart
        yEnd = yStart
    if BFill:
        plt.fill(XPoint, YPoint, color=paramPLT.getColour, zorder=0,
                 label=paramPLT.getLegends)

# Plotting functions in 3D
# 3D

# 3D Shapes

