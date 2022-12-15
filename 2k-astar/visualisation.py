from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np


def draw(grid_map, start=None, goal=None, path=None, nodes_opened=None, nodes_expanded=None):
    '''
    Auxiliary function that visualizes the environment, the path and
    the open/expanded/re-expanded nodes.

    The function assumes that nodes_opened/nodes_expanded/nodes_reexpanded
    are iterable collestions of SearchNodes
    '''
    k = 5
    height, width = grid_map.get_size()

    h_im = height * k
    w_im = width * k
    im = Image.new('RGB', (w_im, h_im), color='white')
    draw = ImageDraw.Draw(im)

    for i in range(height):
        for j in range(width):
            if (not grid_map.traversable(i, j)):
                draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))

    if nodes_opened is not None:
        nodes_coords = []
        for node in nodes_opened:
            nodes_coords.append((node.j * k, node.i * k))
        draw.point(nodes_coords, fill=(213, 219, 219))

    if nodes_expanded is not None:
        nodes_coords = []
        for node in nodes_expanded:
            nodes_coords.append((node.j * k, node.i * k))
        draw.point(nodes_coords, fill=(131, 145, 146))

    if path is not None:
        nodes_coords = []
        for step in path:
            nodes_coords.append((step.j * k, step.i * k))
        draw.line(nodes_coords, fill=(52, 152, 219))
        draw.point(nodes_coords, fill=(0, 0, 128))

    if (start is not None):
        draw.point((start.j * k, start.i * k), fill=(40, 180, 99))
    if (goal is not None):
        draw.point((goal.j * k, goal.i * k), fill=(231, 76, 60))

    _, ax = plt.subplots(dpi=150)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.imshow(np.asarray(im))
    plt.show()
