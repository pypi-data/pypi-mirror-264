import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon
from shapely.wkt import loads as load_wkt


def plotpoly(obj, verbose=False, invert_y=True):
    """Plot polygons from various input types."""
    try:
        # Setup plot
        fig, ax = plt.subplots()
        if invert_y:
            ax.invert_yaxis()

        # Plotting directly based on type
        if isinstance(obj, (Polygon, MultiPolygon, GeometryCollection)):
            plot_shapely_entity(ax, obj)
        elif isinstance(obj, list):
            if not obj:  # Check if the list is empty
                raise ValueError("The input list is empty.")
            if all(isinstance(item, str) for item in obj):
                try:
                    for wkt_str in obj:
                        plot_shapely_entity(ax, load_wkt(wkt_str))
                except wkt.WKTReadingError as e:
                    raise ValueError(f"Invalid WKT string detected: {e}")
            elif all(isinstance(item, tuple) for item in obj):
                try:
                    plot_shapely_entity(ax, Polygon(obj))
                except ValueError as e:
                    raise ValueError(f"Invalid tuple list for polygon creation: {e}")
            elif all(isinstance(item, Polygon) for item in obj):
                for polygon in obj:
                    plot_shapely_entity(ax, polygon)
            else:
                raise ValueError("List contains unsupported or mixed content types.")
        elif isinstance(obj, np.ndarray):
            if obj.ndim != 2 or obj.shape[1] != 2:
                raise ValueError(
                    "NumPy array must be of shape (n, 2) for polygon vertices."
                )
            plot_shapely_entity(ax, Polygon(obj))
        elif isinstance(obj, dict):
            if not obj:
                raise ValueError("The input dictionary is empty.")
            for v in obj.values():
                plot_shapely_entity(ax, Polygon(v))
        elif isinstance(obj, str):
            try:
                plot_shapely_entity(ax, load_wkt(obj))
            except wkt.WKTReadingError as e:
                raise ValueError(f"Invalid WKT string: {e}")
        elif isinstance(obj, tuple):
            if len(obj) != 2 or any(not isinstance(i, (list, np.ndarray)) for i in obj):
                raise ValueError(
                    "Tuple must be of two lists or arrays of x and y coordinates."
                )
            plot_shapely_entity(ax, Polygon(zip(*obj)))
        else:
            raise ValueError(f"Unsupported object type: {type(obj)}.")

        plt.gca().set_aspect("equal", adjustable="box")
        plt.show()

    except Exception as e:
        raise ValueError(f"Error converting input to polygon: {e}") from e


def plot_shapely_entity(ax, entity):
    if hasattr(entity, "geoms"):  # Works for both GeometryCollection and MultiPolygon
        for geom in entity.geoms:
            plot_polygon_with_holes(ax, geom)
    elif isinstance(entity, Polygon):
        plot_polygon_with_holes(ax, entity)
    else:
        raise TypeError(f"Unsupported Shapely geometry type: {type(entity)}")


def plot_polygon_with_holes(ax, polygon):
    """Plot a single polygon, including any holes, on the provided axes."""
    # Plot the exterior
    exterior_coords = polygon.exterior.coords.xy
    ax.plot(exterior_coords[0], exterior_coords[1], "b")  # Blue for exterior

    # Plot each hole
    for hole in polygon.interiors:
        hole_coords = hole.coords.xy
        ax.plot(hole_coords[0], hole_coords[1], "r")  # Red for holes
