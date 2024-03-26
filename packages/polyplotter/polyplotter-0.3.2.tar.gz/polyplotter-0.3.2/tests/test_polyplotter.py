import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest
from shapely import wkt  # required to access shapely.wkt
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon

from polyplotter import plotpoly as p

matplotlib.use("Agg")  # non-iteractive usage so the graphs don't pop up


def test_empty_geom_collection():
    empty_shape = wkt.loads("GEOMETRYCOLLECTION EMPTY")
    p(empty_shape)


def test_simple_wkt():
    simple_poly_wkt = (
        "POLYGON ((45 58, 46 59, 57 55, 54 46, 44 49, 46 53, 44 54, 45 58))"
    )
    p(simple_poly_wkt)


def test_square_wkt():
    square_wkt = "POLYGON ((4 5, 5 5, 5 4, 4 4, 4 5))"
    p(square_wkt)


def test_simple_poly():
    simple_poly_wkt = (
        "POLYGON ((45 58, 46 59, 57 55, 54 46, 44 49, 46 53, 44 54, 45 58))"
    )
    simple_poly = wkt.loads(simple_poly_wkt)
    empty_shape = wkt.loads("GEOMETRYCOLLECTION EMPTY")
    empty_geometry_collection = empty_shape.intersection(simple_poly)
    p(empty_geometry_collection)


def test_list_coords():
    polygon_coords = [(0, 0), (5, 0), (5, 5), (0, 5)]
    p(polygon_coords)


def test_ndarray_coords():
    coords = np.array(
        [
            [1389, 2300],
            [1390, 2301],
            [1394, 2305],
            [1368, 2306],
            [1374, 2300],
            [1379, 2299],
            [1383, 2299],
            [1389, 2300],
        ],
        dtype=np.int32,
    )
    p(coords)


def test_plot_ndarray_poly():
    arr = np.array([[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]])
    p(arr)


def test_plot_shapely_poly():
    poly = Polygon([[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]])
    p(poly)


def test_plot_shapely_multipoly():
    multipoly = MultiPolygon(
        [
            Polygon([[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]),
            Polygon([[3, 3], [4, 3], [4, 4], [3, 4], [3, 3]]),
        ]
    )
    p(multipoly)


def test_plot_shapely_geometry_collection():
    gc = GeometryCollection(
        [
            Polygon([[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]),
            Polygon([[3, 3], [4, 3], [4, 4], [3, 4], [3, 3]]),
        ]
    )
    p(gc)


def test_plot_dict():
    dict_obj = {
        "poly1": Polygon([[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]),
        "poly2": Polygon([[3, 3], [4, 3], [4, 4], [3, 4], [3, 3]]),
    }
    p(dict_obj)


def test_plot_list_of_polys():
    list_obj = [
        Polygon([[1, 1], [2, 1], [2, 2], [1, 2], [1, 1]]),
        Polygon([[3, 3], [4, 3], [4, 4], [3, 4], [3, 3]]),
    ]
    p(list_obj)


def test_plot_list_of_wkts():
    list_obj = [
        "POLYGON ((4 5, 5 5, 5 4, 4 4, 4 5))",
        "POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))",
    ]
    p(list_obj)


def test_plot_str():
    wkt_str = "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))"
    p(wkt_str)


def test_plot_tuple():
    tuple_obj = ([1, 2, 3, 4], [1, 2, 3, 4])
    p(tuple_obj)


# @pytest.mark.skip(reason="This test requires manual verification and is not automated.")
def test_polygon_with_hole_MANUAL_TEST():
    """
    This test must be verified manually. I skip it by default.
    """
    matplotlib.use("TkAgg")
    # Define the exterior of the polygon
    exterior = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
    # Define a hole in the polygon
    hole = [(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)]
    # Create the polygon with the hole
    poly_with_hole = Polygon(shell=exterior, holes=[hole])

    # Plot the polygon
    p(poly_with_hole, verbose=True, invert_y=False)

    # Instructions for manual verification;
    print("Verify the plotted polygon does NOT fill in the specified hole.")
    plt.show()


# @pytest.mark.skip(reason="This test requires manual verification and is not automated.")
def test_list_with_holes_MANUAL_TEST():
    """
    This test must be verified manually. I skip it by default.
    """
    matplotlib.use("TkAgg")
    # Define the exterior of the polygon
    exterior1 = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
    # Define a hole in the polygon
    hole1 = [(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)]
    # Create the polygon with the hole
    poly_with_hole1 = Polygon(shell=exterior1, holes=[hole1])

    exterior2 = [(10, 10), (15, 10), (15, 15), (10, 15), (10, 10)]
    # Define a hole in the polygon
    hole2 = [(11, 11), (14, 11), (14, 14), (11, 14), (11, 11)]
    # Create the polygon with the hole
    poly_with_hole2 = Polygon(shell=exterior2, holes=[hole2])

    list_with_holes = [poly_with_hole1, poly_with_hole2]

    # Plot the polygon
    p(list_with_holes, verbose=True, invert_y=False)

    # Instructions for manual verification;
    print("Verify the plotted polygon does NOT fill in the specified hole.")
    plt.show()


if __name__ == "__main__":
    pytest.main([__file__])
