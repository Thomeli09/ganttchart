# -*- coding: utf-8 -*-


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
Base de donnée

Improvements:
    Should add a list of axes to the ParamPLT object to avoid having to call plt.gca() each time as an option.
"""


# Display parameters
class ParamPLT:
    def __init__(self, color, lineType, marker, linesize, fontsize):
        """
        Ajouter le système de liste si différents éléments, pas que pour les légendes,...
        """
        # Plot
        self._color = color
        self._colorMap = 'viridis'
        self._LineType = LineType
        self._LineSize = Linesize
        self._MarkerType = Marker
        self._MarkerSize = Linesize
        self._Alpha = 1  # Blending value, from 0 (transparent) to 1 (opaque)
        self._HatchType = ''

        # Text
        self._TitleSize = Fontsize
        self._FontSize = Fontsize
        self._TicksSize = Fontsize
        self._LegendsSize = Fontsize
        self._XLabel = None
        self._YLabel = None
        self._ZLabel = None
        self._Title = None
        self._LegendTitle = None
        self._Legends = []
        self._BLegends = True
        self._BLegendsInsideBox = True  # To put the legend inside the plot or not
        self._LegendsLoc = 0  # Location of the legend (0 = best, ...)
        self._ColorBarTitle = None

        # Scale
        self._Scale = 1
        self._XScaleType = 'linear'
        self._YScaleType = 'linear'
        self._ZScaleType = 'linear'
        self._BXAxisDate = False
        self._XAxisDateFormat = mdates.DateFormatter('%Y-%m-%d')
        self._BXAxisDateRotate = False
        self._GenericScaleType = 'linear'
        self._Scale3D = 1

        # Plot Format
        self._PltAspect = None

        # Grid
        self._GridAxis = 'both'
        self._GridColor = None
        self._GridLineType = None
        self._GridLineSize = 0.4
        self._GridAlpha = 1
        self._BBox = True # To add a box around the plot or not

        # Limits
        self._XLimit = []
        self._YLimit = []
        self._Zlimit = []

        # Link to Figure and Axes
        self._Figure = None  # Figure
        self._BAxes = False  
        self._LAxes = []  # List of axes if BAxes = True
        self._PlottedObject = []  # List of plotted objects to be able to modify them later if needed
        self._BMappable = False
        self._LMappable = []  # List of mappable if BMappable = True

    # Plot
    @property
    def BoolColor(self):
        if not self._Color:
            return False
        else:
            return True

    @property
    def Color(self):
        if not self._Color:
            return None
        else:
            if isinstance(self._Color, list):
                return self._Color.pop(0)
            else:
                return self._Color

    @Color.setter
    def Color(self, Color):
        if isinstance(Color, list):
            if isinstance(self._Color, list):
                self._Color = self._Color + Color
            else:
                self._Color = None
                self._Color = Color
        else:
            self._Color = Color

    def ColorFillList(self, ShadesNumber, FloatMin=0.0, FloatMax=1.0, B2ParamPLTColor=True):
        """
        Create a list of Colors based on a Color map and a range of values.

        Args:
            ShadesNumber (int): Number of shades to generate.
            FloatMin (float): Minimum value of the range.
            FloatMax (float): Maximum value of the range.
            B2ParamPLTColor (bool): If True, transfer the Color to the ParamPLT object. Else, return the list of Colors.
        """
        CMap = cm._cmap(self._ColorMap)
        ColorRange = np.linspace(FloatMin, FloatMax, ShadesNumber)
        ListColors = [CMap(Value) for Value in ColorRange]

        if B2ParamPLTColor:
            self._Color = ListColors
        else:
            return ListColors

    def ColorFullList(self, BEmptying=False):
        if isinstance(self._Color, list):
            Temp = self._Color
            if BEmptying:
                self._Color = None
            return Temp
        else:
            print("Warning: No list of Colors found.")
            return self._Color

    @property
    def ColorMap(self):
        return self._ColorMap

    @ColorMap.setter
    def ColorMap(self, ValColorMap):
        ColorMapDict = {"Perceptually Uniform Sequential": (0, 4),  # Indices: 0-4
                         0: "viridis", 1: "plasma", 2: "inferno", 3: "magma", 4: "cividis",

                         "Sequential": (5, 22),  # Indices: 5-22
                         5: "Greys", 6: "Purples", 7: "Blues", 8: "Greens", 9: "Oranges", 10: "Reds",
                         11: "YlOrBr", 12: "YlOrRd", 13: "OrRd", 14: "PuRd", 15: "RdPu", 16: "BuPu",
                         17: "GnBu", 18: "PuBu", 19: "YlGnBu", 20: "PuBuGn", 21: "BuGn", 22: "YlGn",

                         "Diverging": (23, 34),  # Indices: 23-34
                         23: "PiYG", 24: "PRGn", 25: "BrBG", 26: "PuOr", 27: "RdGy", 28: "RdBu",
                         29: "RdYlBu", 30: "RdYlGn", 31: "Spectral", 32: "coolwarm", 33: "bwr", 34: "seismic",

                         "Cyclic": (35, 37),  # Indices: 35-37
                         35: "twilight", 36: "twilight_shifted", 37: "hsv",

                         "Qualitative": (38, 49),  # Indices: 38-49
                         38: "Pastel1", 39: "Pastel2", 40: "Paired", 41: "Accent", 42: "Dark2",
                         43: "Set1", 44: "Set2", 45: "Set3", 46: "tab10", 47: "tab20", 48: "tab20b", 49: "tab20c",

                         "Miscellaneous": (50, 66),  # Indices: 50-66
                         50: "flag", 51: "prism", 52: "ocean", 53: "gist_earth", 54: "terrain", 55: "gist_stern",
                         56: "gnuplot", 57: "gnuplot2", 58: "CMRmap", 59: "cubehelix", 60: "brg",
                         61: "gist_rainbow", 62: "rainbow", 63: "jet", 64: "turbo", 65: "nipy_spectral", 66: "gist_ncar",

                         "Sequential (Miscellaneous)": (67, 82),  # Indices: 67-82
                         67: "binary", 68: "gist_yarg", 69: "gist_gray", 70: "gray", 71: "bone", 72: "pink",
                         73: "spring", 74: "summer", 75: "autumn", 76: "winter", 77: "cool", 78: "Wistia",
                         79: "hot", 80: "afmhot", 81: "gist_heat", 82: "copper",

                         "Perceptually Uniform Sequential (Reversed)": (83, 87),  # Indices: 83-87
                         83: "viridis_r", 84: "plasma_r", 85: "inferno_r", 86: "magma_r", 87: "cividis_r",

                         "Sequential (Reversed)": (88, 105),  # Indices: 88-105
                         88: "Greys_r", 89: "Purples_r", 90: "Blues_r", 91: "Greens_r", 92: "Oranges_r", 93: "Reds_r",
                         94: "YlOrBr_r", 95: "YlOrRd_r", 96: "OrRd_r", 97: "PuRd_r", 98: "RdPu_r", 99: "BuPu_r",
                         100: "GnBu_r", 101: "PuBu_r", 102: "YlGnBu_r", 103: "PuBuGn_r", 104: "BuGn_r", 105: "YlGn_r",
                         
                         "Diverging (Reversed)": (106, 117),  # Indices: 106-117
                         106: "PiYG_r", 107: "PRGn_r", 108: "BrBG_r", 109: "PuOr_r", 110: "RdGy_r", 111: "RdBu_r",
                         112: "RdYlBu_r", 113: "RdYlGn_r", 114: "Spectral_r", 115: "coolwarm_r", 116: "bwr_r", 117: "seismic_r",

                         "Cyclic (Reversed)": (118, 120),  # Indices: 118-120
                         118: "twilight_r", 119: "twilight_shifted_r", 120: "hsv_r",

                         "Miscellaneous (Reversed)": (121, 137),  # Indices: 121-137
                         121: "flag_r", 122: "prism_r", 123: "ocean_r", 124: "gist_earth_r", 125: "terrain_r", 126: "gist_stern_r",
                         127: "gnuplot_r", 128: "gnuplot2_r", 129: "CMRmap_r", 130: "cubehelix_r", 131: "brg_r",
                         132: "gist_rainbow_r", 133: "rainbow_r", 134: "jet_r", 135: "turbo_r", 136: "nipy_spectral_r", 137: "gist_ncar_r",

                         "Sequential (Miscellaneous) (Reversed)": (138, 153),  # Indices: 138-153
                         138: "binary_r", 139: "gist_yarg_r", 140: "gist_gray_r", 141: "gray_r", 142: "bone_r", 143: "pink_r",
                         144: "spring_r", 145: "summer_r", 146: "autumn_r", 147: "winter_r", 148: "cool_r", 149: "Wistia_r",
                         150: "hot_r", 151: "afmhot_r", 152: "gist_heat_r", 153: "copper_r"}

        self._ColorMap = ColorMapDict.(ValColorMap, 'viridis')

    @property
    def LineType(self):
        # Determine line type based on LineType input
        LineTypeDict = {0: '-', 1: '--', 2: '-.', 3: ':', 4: 'None'}
        LineType = LineTypeDict.(self._LineType, '-')
        return LineType

    @LineType.setter
    def LineType(self, LineType):
        self._LineType = LineType

    @property
    def LineSize(self):
        return self._LineSize

    @LineSize.setter
    def LineSize(self, Linesize):
        self._LineSize = Linesize

    @property
    def Marker(self):
        MarkerTypeDict = {0: '', 1: '.', 2: ',', 3: 'o', 4: 'v', 5: '^',
                          6: '<', 7: '>', 8: '1', 9: '2', 10: '3', 11: '4',
                          12: '8', 13: 's', 14: 'p', 15: 'P', 16: '*', 17: 'h',
                          18: 'H', 19: '+', 20: 'x', 21: 'X', 22: 'D', 23: 'd',
                          24: '|', 25: '_'}
        MarkerType = MarkerTypeDict.(self._MarkerType, '')
        return MarkerType

    @Marker.setter
    def Marker(self, Marker):
        self._MarkerType = Marker

    @property
    def MarkerSize(self):
        return self._MarkerSize

    @MarkerSize.setter
    def MarkerSize(self, MarkerSize):
        self._MarkerSize = MarkerSize

    @property
    def Alpha(self):
        return self._Alpha

    @Alpha.setter
    def Alpha(self, Alpha):
        self._Alpha = Alpha

    @property
    def Hatch(self):
        """
        Property that retrieves and modifies the `HatchType` attribute.
        - If `HatchType` is empty (`None` or equivalent), it returns `None`.
        - If `HatchType` is a list, it removes and returns the first element of the list (FIFO behavior).
        - If `HatchType` is not a list, it simply returns the value of `HatchType`.
        """

        # Check if `HatchType` is empty or `None`
        if not self._HatchType:
            return None  # Return None if no value is present
        else:
            # If `HatchType` is a list, pop and return the first element
            if isinstance(self._HatchType, list):
                return self._HatchType.pop(0)  # Remove the first element and return it
            else:
                # If `HatchType` is not a list, return the value directly
                return self._HatchType

    @Hatch.setter
    def Hatch(self, HatchType):
        """
        Sets the `HatchType` property of the object based on the specified hatch type (`HatchType`).
        The hatch type is mapped to predefined patterns using a dictionary.
        This method can handle simple integers or complex structures such as nested lists.

        Args:
            HatchType (int, list, or other): The hatch type to configure.
                - If `HatchType` is an integer, it is directly mapped to a pattern using the dictionary (Result = 1 Hatch).
                - If `HatchType` is a flat list, each element is individually mapped to create a combined pattern (Result = 1 Hatch).
                - If `HatchType` is a nested list, each sub-list is individually mapped to create multiple patterns (Result = # of sub-lists Hatch).
        """

        # Dictionary mapping numeric values to hatch patterns
        HatchTypeDict = {
            0: '', 1: '/', 2: '\\', 3: '|', 4: '-', 5: '+',
            6: 'x', 7: 'o', 8: 'O', 9: '.', 10: '*'
        }

        # Variables to store the result
        Hatch = ''   # Combined pattern if HatchType is a flat list
        LHatch = []  # List of patterns if HatchType contains nested lists

        # Check if `HatchType` is a list
        if isinstance(HatchType, list):
            for Item in HatchType:
                if isinstance(Item, list):  # If an element is a nested list
                    LItem = Item
                    Hatch = ''  # Reset `Hatch` for each sub-list
                    for Val in LItem:
                        # Add the pattern corresponding to the value to `Hatch`
                        Hatch += HatchTypeDict.(Val, '')  
                    LHatch.append(Hatch)  # Append the complete pattern of the sub-list to `LHatch`
                else:  # If the element is an integer or a simple value
                    Val = Item
                    Hatch += HatchTypeDict.(Val, '')  # Add the pattern directly
        else:  # If `HatchType` is not a list
            Hatch = HatchTypeDict.(HatchType, '')  # Retrieve the corresponding pattern

        # Assign the final value to `self._HatchType`
        if LHatch:  # If `LHatch` contains complex patterns
            self._HatchType = LHatch
        else:  # Otherwise, use the simple pattern
            self._HatchType = Hatch

    def HatchFullList(self, BEmptying=True):
        """
        Property that retrieves the full list of hatch patterns if `HatchType` is a list.
        If `HatchType` is not a list, it displays a warning message and returns the current value of `HatchType`.

        Returns:
            list or other: If `HatchType` is a list, it returns the list of hatch patterns and resets `HatchType` to `None`.
                           If `HatchType` is not a list, it prints a warning message and returns the current value of `HatchType`.
        """
        # Check if `HatchType` is a list
        if isinstance(self._HatchType, list):
            Temp = self._HatchType  # Store the current list of hatch patterns in a temporary variable
            if BEmptying:
                self._HatchType = None  # Reset `HatchType` to `None`
            return Temp  # Return the stored list
        else:
            # Print a warning message if `HatchType` is not a list
            print("Warning: No list of hatch found.")
            return self._HatchType  # Return the current value of `HatchType`

    # Text
    @property
    def TitleSize(self):
        return self._TitleSize

    @TitleSize.setter
    def TitleSize(self, TitleSize):
        self._TitleSize = TitleSize

    @property
    def FontSize(self):
        return self._FontSize

    @FontSize.setter
    def FontSize(self, Fontsize):
        self._FontSize = Fontsize

    @property
    def TicksSize(self):
        return self._TicksSize

    @TicksSize.setter
    def TicksSize(self, TicksSize):
        self._TicksSize = TicksSize

    @property
    def LegendsSize(self):
        return self._LegendsSize

    @LegendsSize.setter
    def LegendsSize(self, LegendsSize):
        self._LegendsSize = LegendsSize

    @property
    def Title(self):
        return self._Title

    @Title.setter
    def Title(self, Title):
        self._Title = Title

    @property
    def LegendTitle(self):
        return self._LegendTitle

    @LegendTitle.setter
    def LegendTitle(self, LegendTitle):
        self._LegendTitle = LegendTitle

    @property
    def XLabel(self):
        return self._XLabel

    @XLabel.setter
    def XLabel(self, XLabel):
        self._XLabel = XLabel

    @property
    def YLabel(self):
        return self._YLabel

    @YLabel.setter
    def YLabel(self, YLabel):
        self._YLabel = YLabel

    @property
    def ZLabel(self):
        return self._ZLabel

    @ZLabel.setter
    def ZLabel(self, ZLabel):
        self._ZLabel = ZLabel

    def LabelTitle(self, Title, XLabel, YLabel, ZLabel=None):
        self._Title = Title
        self._XLabel = XLabel
        self._YLabel = YLabel
        self._ZLabel = ZLabel

    @property
    def Legends(self):
        if not self._Legends:
            return None
        else:
            return self._Legends.pop(0)

    @Legends.setter
    def Legends(self, Legends):
        self._Legends = Legends

    def LegendsFullList(self, BEmptying=True):
        # Check if `Legends` is a list
        if isinstance(self._Legends, list):
            Temp = self._Legends  # Store the current list of legend in a temporary variable
            if BEmptying:
                self._Legends = None  # Reset `Legends` to `None`
            return Temp  # Return the stored list
        else:
            # Print a warning message if `Legends` is not a list
            print("Warning: No list of legend found.")
            return self._Legends  # Return the current value of `Legends`
  
    @property
    def BLegends(self):
        return self._BLegends

    @BLegends.setter
    def BLegends(self, Bool):
        self._BLegends = Bool

    @property
    def BLegendsInsideBox(self):
        return self._BLegendsInsideBox

    @BLegendsInsideBox.setter
    def BLegendsInsideBox(self, Bool):
        self._BLegendsInsideBox = Bool

    @property
    def LegendsLoc(self):
        return self._LegendsLoc

    @LegendsLoc.setter
    def LegendsLoc(self, Loc):
        # Dictionary mapping integer values to legend locations
        LegendLocDict = {0: 'best', 1: 'upper right', 2: 'upper left', 3: 'lower left', 4: 'lower right',
                         5: 'right', 6: 'center left', 7: 'center right', 8: 'lower center', 9: 'upper center',
                         10: 'center', 'best': 'best', 'upper right': 'upper right', 'upper left': 'upper left', 
                         'lower left': 'lower left', 'lower right': 'lower right', 'right': 'right', 
                         'center left': 'center left', 'center right': 'center right', 
                         'lower center': 'lower center', 'upper center': 'upper center', 'center': 'center'}
        self._LegendsLoc = LegendLocDict.(Loc, 'best')

    @property
    def ColorBarTitle(self):
        return self._ColorBarTitle

    @ColorBarTitle.setter
    def ColorBarTitle(self, Title):
        self._ColorBarTitle = Title

    # Scale
    @property
    def Scale(self):
        return self._Scale

    @Scale.setter
    def Scale(self, scale):
        self._Scale = scale

    def ScaleVal2Name(self, Val):
        ScaleTypeDict = {0: 'linear', 1: 'log', 2: 'logit',
                         3: 'symlog', 4: 'function',
                         5: 'functionlog', 6: 'asinh',
                         7: 'mercator', 8: None}
        ScaleType = ScaleTypeDict.(Val, 'linear')
        return ScaleType

    @property
    def XScaleType(self):
        return self._XScaleType

    @XScaleType.setter
    def XScaleType(self, Val):
        self._XScaleType = self._ScaleVal2Name(Val)

    @property
    def YScaleType(self):
        return self._YScaleType

    @YScaleType.setter
    def YScaleType(self, Val):
        self._YScaleType = self._ScaleVal2Name(Val)

    @property
    def ZScaleType(self):
        return self._ZScaleType

    @ZScaleType.setter
    def ZScaleType(self, Val):
        self._ZScaleType = self._ScaleVal2Name(Val)

    @property
    def BXAxisDate(self):
        return self._BXAxisDate

    @BXAxisDate.setter
    def BXAxisDate(self, Bool):
        self._BXAxisDate = Bool

    @property
    def XAxisDateFormat(self):
        return self._XAxisDateFormat

    @XAxisDateFormat.setter
    def XAxisDateFormat(self, DateFormat):
        self._XAxisDateFormat = mdates.DateFormatter(DateFormat)

    @property
    def BXAxisDateRotate(self):
        return self._BXAxisDateRotate

    @BXAxisDateRotate.setter
    def BXAxisDateRotate(self, Bool):
        self._BXAxisDateRotate = Bool

    @property
    def GenericScaleType(self):
        return self._GenericScaleType

    @GenericScaleType.setter
    def GenericScaleType(self, Val):
        self._GenericScaleType = self._ScaleVal2Name(Val)

    @property
    def Scale3D(self):
        return self._Scale3D

    @Scale3D.setter
    def Scale3D(self, scale3D):
        self._Scale3D = scale3D

    @property
    def FMT(self):
        # Construct plot format
        fmt = f"{self._Marker}{self._LineSize}{self._Color}"
        return fmt

    # Plot Format
    @property
    def Aspect(self):
        return self._PltAspect

    @Aspect.setter
    def Aspect(self, Aspect):
        self._PltAspect = Aspect

    # Grid
    @property
    def GridAxis(self):
        return self._GridAxis

    @GridAxis.setter
    def GridAxis(self, GridAxis):
        self._GridAxis = GridAxis

    @property
    def GridColor(self):
        return self._GridColor

    @GridColor.setter
    def GridColor(self, Color):
        self._GridColor = Color

    def Grid(self, Axis, Color=None):
        if Axis == 1:
            self._GridAxis = 'x'
        elif Axis == 2:
            self._GridAxis = 'y'
        elif Axis >= 0:
            self._GridAxis = 'both'
        else:
            self._GridAxis = None

        self._GridColor = Color

        self._GridLineType = None
        self._GridLineSize = 0.4

    @property
    def GridLineType(self):
        # Determine line type based on LineType input
        LineTypeDict = {0: '-', 1: '-', 2: '--', 3: '-.', 4: ':'}
        LineType = LineTypeDict.(self._GridLineType, '-')
        return LineType

    @GridLineType.setter
    def GridLineType(self, LineType):
        self._GridLineType = LineType

    @property
    def GridLineSize(self):
        return self._GridLineSize

    @GridLineSize.setter
    def GridLineSize(self, LineSize):
        self._GridLineSize = LineSize

    @property
    def GridAlpha(self):
        return self._GridAlpha

    @GridAlpha.setter
    def GridAlpha(self, Val):
        self._GridAlpha = Val

    @property
    def BBox(self):
        return self._BBox

    @BBox.setter
    def BBox(self, Bool):
        self._BBox = Bool

    # Limits
    @property
    def XLimit(self):
        if not self._XLimit:
            return None
        else:
            return self._XLimit.pop(0)

    @XLimit.setter
    def XLimit(self, Limit):
        self._XLimit.append(Limit)
    
    @property
    def YLimit(self):
        if not self._YLimit:
            return None
        else:
            return self._YLimit.pop(0)

    @YLimit.setter
    def YLimit(self, Limit):
        self._YLimit.append(Limit)
    
    @property
    def ZLimit(self):
        if not self._ZLimit:
            return None
        else:
            return self._ZLimit.pop(0)

    @ZLimit.setter
    def ZLimit(self, Limit):
        self._ZLimit.append(Limit)

    @property
    def BoolXLimit(self):
        return bool(self._XLimit)
    
    @property
    def BoolYLimit(self):
        return bool(self._YLimit)
    
    @property
    def BoolZLimit(self):
        return bool(self._ZLimit)

    # Link to Figure and Axes
    @property
    def Figure(self):
        return self._Figure

    @Figure.setter
    def Figure(self, Figure):
        self._Figure = Figure

    @property
    def BAxes(self):
        return self._BAxes

    @BAxes.setter
    def BAxes(self, Bool):
        self._BAxes = Bool

    @property
    def Axes(self):
        if not self._BAxes:
            return None
        else:
            return self._LAxes

    @Axes.setter
    def Axes(self, Ax):
        Axes2Add = []

        # Case 1: Single Axes
        if isinstance(Ax, Axes):
            Axes2Add = [Ax]

        # Case 2: List / tuple / np.ndarray of Axes
        elif isinstance(Ax, (list, tuple, np.ndarray)):
            # If it's a numpy array, flatten it
            if isinstance(Ax, np.ndarray):
                Ax = Ax.flatten()
            # Collect valid Axes
            Axes2Add = [a for a in Ax if isinstance(a, Axes)]
            if not Axes2Add:
                print("Error: No valid Axes found in the provided collection.")
                return

        # Case 3: Not valid
        else:
            print("Error: The provided Ax is not a valid Axes or collection of Axes.")
            return

        # Store
        if self._BAxes:
            self._LAxes.extend(Axes2Add)
        else:
            self._LAxes = Axes2Add
            self._BAxes = True

    @property
    def LastAx(self):
        if not self._BAxes:
            print("Warning: No axes found.")
            return None
        else:
            return self._Axes[-1]

    @property
    def PlottedObject(self):
        if not self._PlottedObject:
            return None
        else:
            return self._PlottedObject

    @PlottedObject.setter
    def PlottedObject(self, PlottedObject):
        if isinstance(PlottedObject, list):
            self._PlottedObject.extend(PlottedObject)
        else:
            self._PlottedObject.append(PlottedObject)

    @property
    def PlottedObjectNum(self):
        return len(self._PlottedObject)

    def PlottedObjectFromIndex(self, Index):
        return self._PlottedObject[Index]

    @property
    def BMappable(self):
        return self._BMappable

    @BMappable.setter
    def BMappable(self, Bool):
        self._BMappable = Bool

    @property
    def Mappable(self):
        if not self._BMappable:
            return None
        else:
            return self._LMappable

    @Mappable.setter
    def Mappable(self, Mappable):
        # Verify if Mappable is an instance of Axes
        if not isinstance(Mappable, ScalarMappable):
            print("Error: The provided Mappable is not a valid mappable object.")
            return
        if not self._BMappable:
            self._LMappable = [Mappable]
            self._BMappable = True
        else:
            self._LMappable.append(Mappable)

    @property
    def LastMappable(self):
        if not self._BMappable:
            print("Warning: No mappable found.")
            return None
        else:
            return self._LMappable[-1]

"""
Fcts générales
"""
def ClosePlot(PlotOBJ=None):
    if PlotOBJ is None:
        plt.close()
    else:
        plt.close(PlotOBJ)

def CloseAllPlots():
    plt.close('all')

def ClosePlotsOnDemand():
    # To close all plots on demand
    input("Press Enter to close all plots...") 
    plt.close('all')

def StartPlots(paramPLT=None, Rows=1, Cols=1):
    """
    Start a new plot and link it to the ParamPLT object if provided.
    """
    Fig, Ax = plt.subplots(nrows=Rows, ncols=Cols)
    if paramPLT is not None:
        paramPLT.Figure = Fig
        paramPLT.Axes = Ax

def PLTSetWindowSize(Width, Height):
    """
    Set the size of the plot window.
    Args:
    - Width: Width of the window in inches.
    - Height: Height of the window in inches.
    """
    plt.gcf().set_size_inches(Width, Height)

def PLTLatexStyle():
    """
    Set the style of the plot to use LaTeX for text rendering. But is slower.
    """
    plt.rcParams['text.usetex'] = True

def PLTTitleAxis(paramPLT):
    """
    Add a title to the plot and label the axes based on the specified parameters.
    """
    plt.xlabel(paramPLT.XLabel, fontsize=paramPLT.FontSize)
    plt.ylabel(paramPLT.YLabel, fontsize=paramPLT.FontSize)
    plt.title(paramPLT.Title, fontsize=paramPLT.TitleSize)

def PLTTitleModified(paramPLT, X=0.5, Y=0.95):
    """
    Allows to have a different title style than the default one.

    Args:
    - TitleText: Text of the title with the desired style. 
        Example: 'Text with <highlighted Color::{"Color": "red", "fontstyle": "italic", "fontweight": "bold"}>'
    - paramPLT: Object containing plot parameters.
    - X: X position of the title.
    - Y: Y position of the title.

    Improvements:
    - Add highlight_textprops to modify the style of the title without adding that in the TitleText.
    """
    fig_text(s=paramPLT.Title, x=X, y=Y, 
             fontsize=paramPLT.TitleSize, color='black', 
             ha='center', va='center')

def PLTSizeAxis(paramPLT):
    """
    Set the size of the ticks on the plot.
    """
    plt.xticks(fontsize=paramPLT.TicksSize)
    plt.yticks(fontsize=paramPLT.TicksSize)

def PLTLegend(paramPLT):
    """
    Add a legend to the plot based on the specified parameters.

    Args:
    - paramPLT: Object containing plot parameters.
    """
    if paramPLT.BLegends:
        if paramPLT.BLegendsInsideBox:
            plt.legend(title=paramPLT.LegendTitle, title_fontproperties={'size':paramPLT.LegendsSize*1.2,'weight': 'bold'},
                       fontsize=paramPLT.LegendsSize, loc=paramPLT.LegendsLoc)
        else:
            plt.legend(title=paramPLT.LegendTitle, title_fontproperties={'size':paramPLT.LegendsSize*1.2,'weight': 'bold'},
                       fontsize=paramPLT.LegendsSize, bbox_to_anchor=(1, 1), loc='upper left')

def UpdatePlotColorsAndLegend(LColors):
    """
    Update the Colors of the lines in the plot based on a list of Colors.

    Args:
    - LColors: List of Colors to apply to the lines in the plot.
    """
    #  the current axis
    ax = plt.gca()
    
    # Verify that the number of Colors matches the number of lines
    if len(LColors) != len(ax.lines):
        print("Error: The number of Colors does not match the number of lines.")
        return
    
    # Update the Colors of the lines
    for Line, Color in zip(ax.lines, LColors):
        Line.set_color(Color)

    # Update the legend
    plt.legend()
    # plt.draw()  # Redraws the figure (updates existing)
    plt.show()

def PLTLegendWithTitlesSubtitles(LegendTitle, LLegendSubtitles, LSubtitlesPositions, paramPLT, TitleSizeRatio=1.1, SubtitlesSizeRatio=1.0, ax=None):
    """
    Add a legend with a main title and multiple subtitles at specified positions.

    Args:
        LegendTitle: Main title of the legend.
        LLegendSubtitles: List of subtitles to be added to the legend.
        LSubtitlesPositions: List of positions for the subtitles in the legend.
        paramPLT: Object containing plot parameters.
        TitleSizeRatio: Ratio to adjust the size of the main title.
        SubtitlesSizeRatio: Ratio to adjust the size of the subtitles.
        ax: Axis object to which the legend will be added. If None, the current axis will be used.

    Returns:

    Note: 
    -The subtitles are added as empty lines with the specified text, that can lead to some issues.
    -This function should be used after PLTShow() or PLTMultiPlot() to work properly.

    Improvements:
    - Refine the position of the subtitles based on the number of labels in the legend.
    - Add an argument to specify the Color of the subtitles.
    """
    #  the current axis if not provided
    if ax is None:
        print("Info: No axis provided, the current axis is used.")
        ax = plt.gca()

    #  the current legend handles and labels
    handles, labels = ax._legend_handles_labels()

    # Adding the subtitles to the legend
    for Subtitle, Position in zip(LLegendSubtitles, LSubtitlesPositions):
        if 0 <= Position <= len(handles):  # Prevent IndexError
            handles.insert(Position, plt.Line2D([], [], color='none', label=Subtitle))

    # Adding the main title to the legend
    if paramPLT.BLegendsInsideBox:
        Legend = ax.legend(handles=handles,title=LegendTitle, fontsize=paramPLT.TitleSize, 
                           loc=paramPLT.LegendsLoc)
    else:
        Legend = ax.legend(handles=handles,title=LegendTitle, fontsize=paramPLT.TitleSize,
                           bbox_to_anchor=(1, 1), loc='upper left')

    # Setting the title properties
    FormatText(Text=Legend._title(), Fontsize=paramPLT.LegendsSize * TitleSizeRatio, Weight=None,
               Style=None, Family=None, Color=None, BackgroundColor=None, Alpha=None)

    # Setting the subtitles properties
    for text in Legend._texts():
        if text._text() in LLegendSubtitles: # In case of the subtitles
            FormatText(Text=text, Fontsize=paramPLT.LegendsSize * SubtitlesSizeRatio, Weight='bold',
                       Style=None, Family=None, Color=None, BackgroundColor=None, Alpha=None)
        else:  # In case of the different labels
            pass

def PLTColorBar(paramPLT, Location=0, Fraction=0.10, Padding=-1, Spacing=0, BDrawEdges=False):
    """
    Add a Color bar to the plot based on the specified parameters.

    Args:
    - paramPLT: Object containing plot parameters.
    - Location: Location of the Color bar (0: right, 1: left, 2: top, 3: bottom).
    - Fraction: Fraction of the original axes to use for the Color bar.
    - Padding: Padding between the Color bar and the plot. If negative, a default value is used based on the location.
    - Spacing: Uniformity of the Color bar (0: uniform, 1: proportional).
    - BDrawEdges: Boolean indicating whether to draw edges around the Color bar.
    """
    Fig = paramPLT.Figure
    if Fig is None:
        print("Warning: No figure found for the Color bar.")
        return
    Mappable = paramPLT.LastMappable
    if Mappable is None:
        print("Warning: No mappable found for the Color bar.")
        return
    Ax = paramPLT.LastAx
    if Ax is None:
        print("Warning: No axis found for the Color bar.")
        return
    # Location of the Color bar
    LocationDict = {0: 'right', 1: 'left', 2: 'top', 3: 'bottom'}
    Location = LocationDict.(Location, 'right')

    # Padding between the Color bar and the plot
    if Padding<0:
        PaddingDict = {'right': 0.05, 'left': 0.05, 'top': 0.15, 'bottom': 0.15}
        Padding = PaddingDict.(Location, 0.05)
    else:
        Padding = Padding

    # Uniformity of the Color bar
    SpacingDict = {0: 'uniform', 1: 'proportional'}
    Spacing = SpacingDict.(Spacing, 'uniform')

    Cb = Fig.Colorbar(mappable=Mappable, ax=Ax, location=Location, fraction=Fraction, pad=Padding, 
                      format=None, spacing=Spacing, drawedges=BDrawEdges)
    Cb.set_label(label=paramPLT.ColorBarTitle, size=paramPLT.FontSize)
    Cb.ax.tick_params(labelsize=paramPLT.TicksSize)

def PLTGrid(paramPLT):
    if paramPLT.GridAxis:
        plt.grid(axis=paramPLT.GridAxis,
                 color=paramPLT.Color,
                 linestyle=paramPLT.GridLineType,
                 linewidth=paramPLT.GridLineSize,
                 alpha=paramPLT.GridAlpha)

def PLTLimit(paramPLT):
    if paramPLT.BoolXLimit:
        plt.xlim(paramPLT.XLimit)
    if paramPLT.BoolYLimit:
        plt.ylim(paramPLT.YLimit)

def PLTCmptLimit(Variable, Ratio=0.1):
    """
    Compute the limits of the plot based on the variable and a ratio.

    Improvements:
    - Based the computation on the current registered limits (self._XLimit, self._YLimit, self._ZLimit).
    """
    # Verify if the variable is empty
    if LenData(Variable) <= 0:
        print("Warning: The variable is empty, no plotting range will be set.")
        # Return None for both limits
        return [None, None] 
    
    else:
        MaxVal = max(Variable)
        MinVal = min(Variable)
        Delta = MaxVal-MinVal
        LowerLimit = MinVal-Delta*Ratio
        UpperLimit = MaxVal+Delta*Ratio
        return [LowerLimit, UpperLimit]

def PLTScaleType(paramPLT):
    """

    """
    if paramPLT.XScaleType:
        plt.xscale(paramPLT.XScaleType)
    if paramPLT.YScaleType:
        plt.yscale(paramPLT.YScaleType)

def PLTDate(paramPLT):
    """
    Format the x-axis to display dates properly.
    """
    if paramPLT.BXAxisDate:
        plt.gca().xaxis.set_major_formatter(paramPLT.XAxisDateFormat)

        if paramPLT.BXAxisDateRotate:
            plt.gcf().autofmt_xdate() # Rotate labels

def PLTBox(paramPLT):
    """
    Remove or add the box around the plot based on the specified parameter.
    """
    plt.box(on=paramPLT.BBox)

def PLTShow(paramPLT, BMultiplot=False):
    PLTTitleAxis(paramPLT)

    PLTSizeAxis(paramPLT)

    if paramPLT.Aspect:
        plt.gca().set_aspect('equal', adjustable='box')

    PLTLegend(paramPLT)

    PLTGrid(paramPLT)

    PLTLimit(paramPLT)

    PLTScaleType(paramPLT)

    PLTDate(paramPLT)

    PLTBox(paramPLT)

    if not BMultiplot:
        plt.show(block=False)  # Show plot without blocking

def PLTMultiPlot(paramPLT, Rows, Cols=1, Index=1, BStartPLT=True, BAvoidOverlapping=True, BCurrPLTax=False):
    """
    Allows to create a grid of subplots in a single figure.

    Args:
        paramPLT (ParamPLT): ParamPLT object containing plot parameters.
        Rows (int): Number of rows for the subplot grid.
        Cols (int): Number of columns for the subplot grid.
        Index (int): Current index for the subplot.
        BStartPLT (bool): Flag to indicate whether to start a new plot.
        BAvoidOverlapping (bool): Flag to avoid overlapping of labels, plots, etc.
        BCurrPLTax (bool): Flag to indicate whether the function returns the current axis object or not.

    Warning:
        The title of the plot should be set before calling this function, otherwise it will set the subtitle.
        BAvoidOverlapping may need to be set to False in some cases when filling the plot does not work as intended.

    Returns :
        Index: Updated index for the next subplot.
        AxesSubplot or None: Current axis object if BCurrPLTax is True; otherwise not returned.

    Improvements:
        Ability to resize the figure to fit all subplots and take into account the legend size.
    """
    if Index == 1:
        if BStartPLT:  # To start a new plot or not
            StartPlots(paramPLT=paramPLT, Rows=Rows, Cols=Cols)
        ax = plt.subplot(Rows, Cols, Index)
        plt.suptitle(paramPLT.Title, fontsize=paramPLT.TitleSize, fontweight='bold') # Set the main title of the plot
    elif Index == Rows * Cols + 1:
        if BAvoidOverlapping:
            plt.tight_layout() # Avoid overlapping of labels, plots, etc.
        PLTShow(paramPLT)
        ax = None
    elif 1 < Index <= Rows * Cols:
        PLTShow(paramPLT, BMultiplot=True)
        ax = plt.subplot(Rows, Cols, Index)
    else:
        print("Warning: Invalid index for subplot.")
        ax = None

    Index += 1  # Increment the index for the next subplot

    # Return the current index and None if the index is invalid and the current axis object
    if BCurrPLTax:
        return Index, ax
    else:
        return Index

def PLTUpdateLayout():
    plt.tight_layout()

def PLTScreenMaximize(BTaskbar=True, BUpdateLayout=True, PLTTimePause=0.1):
    if BTaskbar:
        plt._current_fig_manager().window.state('zoomed')
    else:
        plt._current_fig_manager().full_screen_toggle()

    if BUpdateLayout:
        plt.pause(PLTTimePause) # Pause to allow the window to maximize and UpdateLayout to work
        # in case of unreliable behavior, increase the pause duration
        PLTUpdateLayout()

def PLTScreenSize(Width_cm, Height_cm, Scale=1, BUpdateLayout=True, PLTTimePause=0.1):
    """
    Set the size of the plot window in centimeters.

    Args:
        Width_cm (float): Width of the plot window in centimeters.
        Height_cm (float): Height of the plot window in centimeters.
        Scale (float): Optional scaling of width/height.
        BUpdateLayout (bool): Flag to update the layout after resizing.
        PLTTimePause (float): Time to pause for layout update.

    """
    # Convert centimeters to inches (1 inch = 2.54 cm)
    Width_in = (Width_cm / 2.54) * Scale
    Height_in = (Height_cm / 2.54) * Scale

    # Set the figure size in inches
    fig = plt.gcf()  #  current figure
    fig.set_size_inches(Width_in, Height_in)

    if BUpdateLayout:
        plt.pause(PLTTimePause) # Pause to allow the window to maximize and UpdateLayout to work
        # in case of unreliable behavior, increase the pause duration
        PLTUpdateLayout()

def PLTSave(FileName, Width_cm, Height_cm, Scale=1, DPI=300, Format=1, BUpdateLayout=True, PLTTimePause=0.1, BCreateDir=False ,BClose=False):
    """
    Save the current plot to a file with customizable options.
    Args:
        FileName (str): Output filename (extension optional).
        Width_cm (float): Width of the figure in centimeters.
        Height_cm (float): Height of the figure in centimeters.
        Scale (float): Scale factor to apply to width and height.
        DPI (int): Dots per inch (resolution).
        Format (str or int): Format type (e.g., "png", 1, "pdf", etc.).
        BUpdateLayout (bool): Flag to update the layout after resizing.
        PLTTimePause (float): Time to pause for layout update.
        BCreateDir (bool): Flag to create the directory if it doesn't exist.
        BClose (bool): Whether to close the figure after saving.
    Returns:
        None: This function does not return anything.
    """

    # Ensure the directory exists
    directory = os.path.dirname(FileName) #  the directory from the filename
    if directory and not os.path.exists(directory): # Check if there needs a directory and if it exists
        if BCreateDir: # Create the directory if it doesn't exist
            print(f"Info : Creating directory: {directory}")
            os.makedirs(directory)
        else:
            print(f"Warning : Directory <<{directory}>> does not exist. File will not be saved.")
            return
    
    # Dictionary to map format values to file extensions
    FormatDict = {'png': '.png', 1: '.png', 'pdf': '.pdf', 2: '.pdf', 
                  'svg': '.svg', 3: '.svg', 'eps': '.eps', 4: '.eps', 
                  'jpg': '.jpg', 5: '.jpg', 'jpeg': '.jpeg', 6: '.jpeg'}
    FormatName = FormatDict.(Format, 'png')  # Default to PNG if format is not recognized

    FullName = FileName + FormatName

    # Set the figure size in inches
    PLTScreenSize(Width_cm=Width_cm, Height_cm=Height_cm, Scale=Scale, BUpdateLayout=BUpdateLayout, PLTTimePause=PLTTimePause)

    #  the current figure
    fig = plt.gcf()

    # Save the plot to a file
    try:
        fig.savefig(fname=FullName, dpi=DPI, bbox_inches='tight')
        print(f"Info : Plot saved as {FullName}")
    except :
        print(f"Warning : Failed to save the plot as {FullName}. Check the file path and permissions.")

    if BClose:
        plt.close()

def PLTShowRefSavePlace():
    """
    Show the path where the plots are saved.
    """
    print("Info : The reference path for saving plots is:")
    print("Info : ", os.cwd())

def DefaultParamPLT():
    return ParamPLT(Color='black', LineType=0, Marker=0, Linesize=2, Fontsize=16)

# Version in 3D case with PLT3DShow




# Text management functions for matplotlib
def FormatText(Text, Fontsize=None, Weight=None, Style=None, Family=None,
                Color=None, BackgroundColor=None, Alpha=None):
    """
    Applies text formatting options dynamically.
    If an option is None, it resets to the default Matplotlib setting.
    
    Args:
        Text: Matplotlib text object
        Fontsize: float or {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
        Weight: {'light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black'}
        Style: {'normal', 'italic', 'oblique'} or None
        Family: {'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'} or None
        Color: Named Color, hex ('#FF5733'), or RGB tuple ((1,0,0))
        BackgroundColor: Same as Color
        Alpha: float (0.0 to 1.0, where 0 is fully transparent and 1 is opaque)
    """
    if Fontsize is not None:
        Text.set_fontsize(Fontsize)

    if Weight is not None:
        Text.set_weight(Weight)

    if Style is not None:
        Text.set_style(Style)

    if Family is not None:
        Text.set_family(Family)

    if Color is not None:
        Text.set_color(Color)

    if BackgroundColor is not None:
        Text.set_backgroundcolor(BackgroundColor)

    if Alpha is not None:
        Text.set_alpha(Alpha)