from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np
import typing as tp

from .api import Stats
from .grid import Map


def draw_static(grid_map, start, goal, path=None):
    k = 50
    r = 0.25 * k
    rr = 0.05 * k
    height, width = grid_map.get_size()
    h_im = height * k
    w_im = width * k
    im = Image.new('RGB', (w_im, h_im), color='white')
    draw = ImageDraw.Draw(im)

    # grid points
    for i in range(height + 1):
        for j in range(width + 1):
            pass
            draw.ellipse((j * k - rr, i * k - rr, j * k + rr, i * k + rr), fill=(50, 50, 50))

    # obstacles
    for i in range(height):
        for j in range(width):
            if not grid_map.traversable(i, j):
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))

    # path
    if path is not None:
        step = path[0]
        draw.ellipse((step[1] * k - r, step[0] * k - r, step[1] * k + r, step[0] * k + r), fill=(52, 152, 219))
        for i in range(1, len(path)):
            prev = path[i-1]
            step = path[i]
            draw.line(((step[1] * k, step[0] * k), (prev[1] * k, prev[0] * k)), fill=(189, 42, 132))
            draw.ellipse((step[1] * k - r, step[0] * k - r, step[1] * k + r, step[0] * k + r), fill=(52, 152, 219))

    # start
    draw.ellipse((start[1] * k - r, start[0] * k - r, start[1] * k + r, start[0] * k + r), fill=(40, 180, 99))

    # goal
    draw.ellipse((goal[1] * k - r, goal[0] * k - r, goal[1] * k + r, goal[0] * k + r), fill=(231, 76, 60))

    _, ax = plt.subplots(dpi=150)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.imshow(np.asarray(im))
    plt.show()


def draw_static_if_path_found(map_: Map, start: tp.Tuple[int, int], end: tp.Tuple[int, int], result: Stats):
    if result.path_found:
        draw_static(map_, start, end, result.path)
        return result
    else:
        print("Path not found :(")