from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

import numpy as np

from matplotlib.path import Path
from matplotlib.patches import Polygon
from nose.tools import assert_raises, assert_equal
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt


def test_readonly_path():
    path = Path.unit_circle()

    def modify_vertices():
        path.vertices = path.vertices * 2.0

    assert_raises(AttributeError, modify_vertices)


def test_point_in_path():
    # Test #1787
    verts2 = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]

    path = Path(verts2, closed=True)
    points = [(0.5, 0.5), (1.5, 0.5)]

    assert np.all(path.contains_points(points) == [True, False])


def test_contains_points_negative_radius():
    path = Path.unit_circle()

    points = [(0.0, 0.0), (1.25, 0.0), (0.9, 0.9)]
    expected = [True, False, False]
    result = path.contains_points(points, radius=-0.5)

    assert result.dtype == np.bool
    assert np.all(result == expected)


@image_comparison(baseline_images=['path_clipping'],
                  extensions=['svg'], remove_text=True)
def test_path_clipping():
    fig = plt.figure(figsize=(6.0, 6.2))

    for i, xy in enumerate([
            [(200, 200), (200, 350), (400, 350), (400, 200)],
            [(200, 200), (200, 350), (400, 350), (400, 100)],
            [(200, 100), (200, 350), (400, 350), (400, 100)],
            [(200, 100), (200, 415), (400, 350), (400, 100)],
            [(200, 100), (200, 415), (400, 415), (400, 100)],
            [(200, 415), (400, 415), (400, 100), (200, 100)],
            [(400, 415), (400, 100), (200, 100), (200, 415)]]):
        ax = fig.add_subplot(4, 2, i+1)
        bbox = [0, 140, 640, 260]
        ax.set_xlim(bbox[0], bbox[0] + bbox[2])
        ax.set_ylim(bbox[1], bbox[1] + bbox[3])
        ax.add_patch(Polygon(
            xy, facecolor='none', edgecolor='red', closed=True))


def test_point_in_path_nan():
    box = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    p = Path(box)
    test = np.array([[np.nan, 0.5]])
    contains = p.contains_points(test)
    assert len(contains) == 1
    assert not contains[0]


@image_comparison(baseline_images=['semi_log_with_zero'], extensions=['png'])
def test_log_transform_with_zero():
    x = np.arange(-10, 10)
    y = (1.0 - 1.0/(x**2+1))**20

    fig, ax = plt.subplots()
    ax.semilogy(x, y, "-o", lw=15)
    ax.grid(True)


def test_make_compound_path_empty():
    # We should be able to make a compound path with no arguments.
    # This makes it easier to write generic path based code.
    r = Path.make_compound_path()
    assert_equal(r.vertices.shape, (0, 2))


@image_comparison(baseline_images=['xkcd'], remove_text=True)
def test_xkcd():
    x = np.linspace(0, 2.0 * np.pi, 100.0)
    y = np.sin(x)

    with plt.xkcd():
        fig, ax = plt.subplots()
        ax.plot(x, y)


@image_comparison(baseline_images=['marker_paths'], extensions=['pdf'],
                  remove_text=True)
def test_marker_paths_pdf():
    N = 7

    plt.errorbar(np.arange(N),
                 np.ones(N) + 4,
                 np.ones(N))
    plt.xlim(-1, N)
    plt.ylim(-1, 7)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)
