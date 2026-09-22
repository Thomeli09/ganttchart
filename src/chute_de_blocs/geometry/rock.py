# geometry/rock.py


# Other Lib
import shapely as shp


# Custom Lib
from geometry import GeometryMaterial, Geometry, PolygonGeom
from chute_de_bloc.materials import RockMaterial


class Rock(GeometryMaterial):
    """
    Class representing a rock in the chute de blocs simulation.
    Attributes:
        material (RockMaterial): The material of the rock.
        geometry (PolygonGeom): The geometric representation of the rock.
    """
    def __init__(self, name: str, color: str, material: RockMaterial, geometry: PolygonGeom):
        """
        Initializes a Rock instance.
        Args:
            name (str): The name of the rock.
            color (str): The color of the rock.
            material (RockMaterial): The material of the rock.
            geometry (PolygonGeom): The geometric representation of the rock.
        """
        super().__init__(name=name, color=color, material=material, geometry=geometry)

        # Metadata attributes
        
        # Rock-mass attributes

        # Rock-specific attributes
        

    # Metadata attributes

    # Rock-mass attributes

    # Rock-specific attributes