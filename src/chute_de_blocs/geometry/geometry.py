# geometry/geometry.py


# Other Lib
from abc import ABC, abstractmethod
from typing import Any, Literal

import shapely as shp



# Custom Lib
from chute_de_bloc.materials import Material

"""
Generic class for geometry in 2D space. This class can be used as a base class for specific geometric shapes such as lines and polygons.
"""
class Geometry(ABC):
    """
    Class representing a generic geometry in 2D space.
    Attributes:
        geometry (shp.base.BaseGeometry): The geometric representation of the entity.
    """
    def __init__(self):
        """
        Initializes a Geometry instance.
        Args:
            geometry (shp.base.BaseGeometry): The geometric representation of the entity.
        """
        # Geometry attributes
        self._geometry = None
    
    # Geometry attributes
    @property
    def geometry(self) -> shp.base.BaseGeometry:
        """
        Returns the geometric representation of the entity.
        Returns:
            shp.base.BaseGeometry: The geometric representation of the entity.
        """
        return self._geometry

    @geometry.setter
    def geometry(self, geometry: shp.base.BaseGeometry):
        """
        Sets the geometric representation of the entity.
        Args:
            geometry (shp.base.BaseGeometry): The geometric representation of the entity.
        """
        self._geometry = geometry

    # Geometry creation methods
    @abstractmethod
    def create_geometry(self, coordinates: list[tuple[float, float]] | list[list[float,float]]):
        """
        Creates the geometric representation of the entity.
        Args:
            coordinates (list[tuple[float, float]]): A list of coordinate tuples representing the geometry.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support create_geometry.")

    # Geometry manipulation methods
    @abstractmethod
    def translate(self, x_offset: float, y_offset: float):
        """
        Translates the geometry by the specified offsets.
        Args:
            x_offset (float): The offset in the x-direction.
            y_offset (float): The offset in the y-direction.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support translate.")

    @abstractmethod
    def rotate(self, angle: float, origin: tuple[float, float] | list[float, float] = (0, 0)):
        """
        Rotates the geometry by the specified angle around the given origin.
        Args:
            angle (float): The angle of rotation in degrees.
            origin (tuple[float, float]): The origin point for rotation. Default is (0, 0).
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support rotate.")

    # Geometry properties
    @abstractmethod
    def length(self) -> float:
        """
        Returns the length of the geometry.
        Returns:
            float: The length of the geometry.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support length.")

    @abstractmethod
    def area(self) -> float:
        """
        Returns the area of the geometry.
        Returns:
            float: The area of the geometry.
        """
        raise NotImplementedError(f"{self.__class__.__name__} does not support area.")

class LineGeom(Geometry):
    """
    Class representing a line geometry in 2D space.
    Attributes:
        geometry (shp.LineString): The geometric representation of the line.
    """
    def __init__(self):
        """
        Initializes a LineGeom instance.
        Args:
            geometry (shp.LineString): The geometric representation of the line.
        """
        super().__init__()
    
    # Geometry creation methods
    def create_geometry(self, coordinates: list[tuple[float, float]] | list[list[float,float]]):
        """
        Creates the geometric representation of the line.
        Args:
            coordinates (list[tuple[float, float]]): A list of coordinate tuples representing the line.
        """
        self._geometry = shp.LineString(coordinates)

    # Geometry manipulation methods
    def translate(self, x_offset: float, y_offset: float):
        """
        Translates the line geometry by the specified offsets.
        Args:
            x_offset (float): The offset in the x-direction.
            y_offset (float): The offset in the y-direction.
        """
        if self._geometry is not None:
            self._geometry = shp.affinity.translate(self._geometry, xoff=x_offset, yoff=y_offset)

    def rotate(self, angle: float, origin: tuple[float, float] | list[float, float] = (0, 0)):
        """
        Rotates the line geometry by the specified angle around the given origin.
        Args:
            angle (float): The angle of rotation in degrees.
            origin (tuple[float, float]): The origin point for rotation. Default is (0, 0).
        """
        if self._geometry is not None:
            self._geometry = shp.affinity.rotate(self._geometry, angle, origin=origin)


    # Geometry properties
    def length(self) -> float:
        """
        Returns the length of the line geometry.
        Returns:
            float: The length of the line geometry.
        """
        if self._geometry is not None:
            return self._geometry.length
        else:
            return 0.0

    def area(self) -> float:
        """
        Returns the area of the line geometry. For a line, this is always 0.
        Returns:
            float: The area of the line geometry (always 0).
        """
        return 0.0

class PolygonGeom(Geometry):
    """
    Class representing a polygon geometry in 2D space.
    Attributes:
        geometry (shp.Polygon): The geometric representation of the polygon.
    """
    def __init__(self):
        """
        Initializes a PolygonGeom instance.
        Args:
            geometry (shp.Polygon): The geometric representation of the polygon.
        """
        super().__init__()
    
    # Geometry creation methods
    def create_geometry(self, coordinates: list[tuple[float, float]] | list[list[float,float]]):
        """
        Creates the geometric representation of the polygon.
        Args:
            coordinates (list[tuple[float, float]]): A list of coordinate tuples representing the polygon.
        """
        self._geometry = shp.Polygon(coordinates)

    # Geometry manipulation methods
    def translate(self, x_offset: float, y_offset: float):
        """
        Translates the polygon geometry by the specified offsets.
        Args:
            x_offset (float): The offset in the x-direction.
            y_offset (float): The offset in the y-direction.
        """
        if self._geometry is not None:
            self._geometry = shp.affinity.translate(self._geometry, xoff=x_offset, yoff=y_offset)

    def rotate(self, angle: float, origin: tuple[float, float] | list[float, float] = (0, 0)):
        """
        Rotates the polygon geometry by the specified angle around the given origin.
        Args:
            angle (float): The angle of rotation in degrees.
            origin (tuple[float, float]): The origin point for rotation. Default is (0, 0).
        """
        if self._geometry is not None:
            self._geometry = shp.affinity.rotate(self._geometry, angle, origin=origin)

    # Geometry properties
    def length(self) -> float:
        """
        Returns the length of the polygon geometry.
        Returns:
            float: The length of the polygon geometry.
        """
        if self._geometry is not None:
            return self._geometry.length
        else:
            return 0.0

    def area(self) -> float:
        """
        Returns the area of the polygon geometry.
        Returns:
            float: The area of the polygon geometry.
        """
        if self._geometry is not None:
            return self._geometry.area
        else:
            return 0.0

class GeometryMaterial:
    """
    Class representing a geometric entity in the chute de blocs simulation.
    Attributes:
        material (Material): The material associated with the geometry.
        geometry (shp.Polygon): The geometric representation of the entity.
    """
    def __init__(self, name:str, color:str, material: Material, geometry: Geometry):
        """
        Initializes a Geometry instance.
        Args:
            material (Material): The material associated with the geometry.
            geometry (shp.Polygon): The geometric representation of the entity.
        """
        # Metadata attributes
        self._name = name
        self._color = color
        
        # Geometry and type attributes
        self._material = material
        self._geometry = geometry

        # Geometry-specific attributes
        
    # Metadata attributes
    @property
    def name(self) -> str:
        """
        Returns the name of the geometry.
        Returns:
            str: The name of the geometry.
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Sets the name of the geometry.
        Args:
            name (str): The name of the geometry.
        """
        self._name = name

    @property
    def color(self) -> str:
        """
        Returns the color of the geometry.
        Returns:
            str: The color of the geometry.
        """
        return self._color

    @color.setter
    def color(self, color: str):
        """
        Sets the color of the geometry.
        Args:
            color (str): The color of the geometry.
        """
        self._color = color

    # Geometry attributes
    @property
    def material(self) -> Material:
        """
        Returns the material associated with the geometry.
        Returns:
            Material: The material associated with the geometry.
        """
        return self._material
    @material.setter
    def material(self, material: Material):
        """
        Sets the material associated with the geometry.
        Args:
            material (Material): The material associated with the geometry.
        """
        self._material = material

    @property
    def geometry(self) -> shp.Polygon:
        """
        Returns the geometric representation of the entity.
        Returns:
            shp.Polygon: The geometric representation of the entity.
        """
        return self._geometry

    @geometry.setter
    def geometry(self, geometry: shp.Polygon):
        """
        Sets the geometric representation of the entity.
        Args:
            geometry (shp.Polygon): The geometric representation of the entity.
        """
        self._geometry = geometry

    # Geometry-specific attributes
