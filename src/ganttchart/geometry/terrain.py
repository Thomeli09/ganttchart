# geometry/terrain.py


# Other Lib
import shapely as shp


# Custom Lib
from geometry import GeometryMaterial, Geometry, PolygonGeom
from chute_de_bloc.materials import TerrainMaterial


class Terrain(GeometryMaterial):
    """
    Class representing a terrain in the chute de blocs simulation.
    Attributes:
        material (TerrainMaterial): The material of the terrain.
        geometry (PolygonGeom): The geometric representation of the terrain.
    """
    def __init__(self, name: str, color: str, material: TerrainMaterial, geometry: PolygonGeom):
        """
        Initializes a Terrain instance.
        Args:
            name (str): The name of the terrain.
            color (str): The color of the terrain.
            material (TerrainMaterial): The material of the terrain.
            geometry (PolygonGeom): The geometric representation of the terrain.
        """
        super().__init__(name=name, color=color, material=material, geometry=geometry)

        # Metadata attributes

        # Terrain-mass attributes

        # Terrain-specific attributes

    # Metadata attributes

    # Terrain-mass attributes

    # Terrain-specific attributes