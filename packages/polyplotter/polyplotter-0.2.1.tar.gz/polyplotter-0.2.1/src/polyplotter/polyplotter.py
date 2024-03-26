import numpy as np
from matplotlib import pyplot as plt
from shapely import wkt
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon

from polyplotter.exceptions import PlotPolyShapeError


def plotpoly(obj, verbose=False, invert_y=True):
    """Plot polygons from various input types."""
    try:
        # Conversion to Shapely objects
        if isinstance(obj, np.ndarray):
            poly = Polygon(obj)
        elif isinstance(obj, dict):
            poly = MultiPolygon([Polygon(v) for v in obj.values()])
        elif isinstance(obj, list):
            poly = MultiPolygon([Polygon(item) for item in obj])
        elif isinstance(obj, str):
            poly = wkt.loads(obj)
        elif isinstance(obj, tuple):
            poly = Polygon(obj)
        else:  # Already a Shapely geometry
            poly = obj

        # Handle GeometryCollections separately
        if isinstance(poly, GeometryCollection):
            plot_shapely_geometry_collection(poly, verbose, invert_y)
        elif isinstance(poly, Polygon):
            plot_shapely_poly(poly, verbose, invert_y)
        elif isinstance(poly, MultiPolygon):
            plot_shapely_multipoly(poly, verbose, invert_y)

    except Exception as e:  # Broad exception for flexibility
        print(f"Error converting input to polygon: {e}")


def plot_ndarray_poly(arr: np.ndarray, verbose=False, invert_y=True):
    """Plot a polygon from a NumPy array.

    Args:
        arr: The NumPy array representing coordinates.
        verbose: Controls whether to print messages.
        invert_y: Inverts the y-axis if True.

    Raises:
        PlotPolyShapeError: If the array cannot be directly converted to a closed polygon.
    """

    if arr.ndim != 2 or arr.shape[1] != 2:
        raise PlotPolyShapeError("NumPy array must have shape (n, 2) for plotting as a polygon.")

    try:
        # Attempt to create a closed polygon directly
        poly = Polygon(arr)
        plot_shapely_poly(poly, invert_y)

    except ValueError:  # Array might not form a closed polygon
        if verbose:
            print("Array doesn't form a closed polygon. Trying to concatenate...")
        try:
            poly = Polygon(np.concatenate(arr, axis=0))
            plot_shapely_poly(poly, invert_y)
        except ValueError:
            raise PlotPolyShapeError("NumPy array is not compatible with polygon plotting.")


def plot_shapely_poly(poly, verbose=False, invert_y=True):
    """Plot a shapely Polygon."""
    if invert_y:
        plt.gca().invert_yaxis()
    plt.plot(*poly.exterior.xy)
    plt.show()


def plot_shapely_multipoly(multipoly, verbose=False, invert_y=True):
    """Plot a shapely MultiPolygon."""
    if invert_y:
        plt.gca().invert_yaxis()
    for geom in multipoly.geoms:
        plt.plot(*geom.exterior.xy)

    plt.gca().axis("equal")
    plt.show()


def plot_shapely_geometry_collection(gc, verbose=False, invert_y=True):
    """Plot a shapely GeometryCollection."""
    for geom in gc.geoms:
        plotpoly(geom, verbose, invert_y)


def plot_dict(obj, verbose=False, invert_y=True):
    """Plot polygons from dictionary values."""
    for _, v in obj.items():
        plotpoly(v, verbose, invert_y)


def plot_list(obj, verbose=False, invert_y=True):
    """Plot polygons from list elements."""
    for item in obj:
        plotpoly(item, verbose=verbose, invert_y=invert_y)


def plot_str(obj, verbose=False, invert_y=True):
    """Plot polygon from WKT string."""
    try:
        poly = wkt.loads(obj)
        plot_shapely_poly(poly, verbose=verbose, invert_y=invert_y)
    except wkt.WKTReadingError as e:
        raise ValueError(f"String not wkt: {obj=}") from e
    except (ValueError, TypeError) as e:
        print(f"Error converting input to polygon: {e}")


def plot_tuple(obj, verbose=False, invert_y=True):
    """Plot polygon from tuple."""
    plt.plot(*obj)
    plt.show()
