from PIL import Image, ImageDraw
import copy
import matplotlib.pyplot as plt
import numpy as np

from ..common.draw import draw_static
from .search_tree import SearchTreePQS
from .utils import *
from .theta_ap import *


class Drawer:
    def __init__(self, grid_map, start, goal):
        self.start = start
        self.goal = goal
        k = 50
        r = 0.25 * k
        rr = 0.05 * k
        self.grid_map = grid_map
        self.ims = []

        height, width = self.grid_map.get_size()
        h_im = height * k
        w_im = width * k
        self.static_im = Image.new('RGBA', (w_im, h_im), color=(255, 255, 255, 255))

        self.draw_static_im()

    def draw_static_im(self):
        k = 50
        r = 0.25 * k
        rr = 0.05 * k

        height, width = self.grid_map.get_size()
        draw = ImageDraw.Draw(self.static_im)

        # grid points
        for i in range(height + 1):
            for j in range(width + 1):
                draw.ellipse((j * k - rr, i * k - rr, j * k + rr, i * k + rr), fill=(50, 50, 50))

        # obstacles
        for i in range(height):
            for j in range(width):
                if not self.grid_map.traversable(i, j):
                    draw.rectangle((j * k, i * k, (j + 1) * k - 1, (i + 1) * k - 1), fill=(70, 80, 80))

        # start
        draw.ellipse((self.start.j * k - r, self.start.i * k - r, self.start.j * k + r, self.start.i * k + r),
                     fill=(40, 180, 99))

        # goal
        draw.ellipse((self.goal.j * k - r, self.goal.i * k - r, self.goal.j * k + r, self.goal.i * k + r),
                     fill=(231, 76, 60))

    def cute_draw(self, curr, parents, show=False, onAPRays=True):
        k = 50
        r = 0.25 * k
        rr = 0.05 * k

        height, width = self.grid_map.get_size()
        h_im = height * k
        w_im = width * k
        im = copy.deepcopy(self.static_im)
        draw = ImageDraw.Draw(im)
        static_draw = ImageDraw.Draw(self.static_im)

        if onAPRays:
            # lv, uv
            R = curr.straight.length()
            lvc = (R + 1) / curr.lv.length()
            draw.line(((curr.parent.j * k, curr.parent.i * k),
                       (curr.parent.j * k + curr.lv.j * k * lvc, curr.parent.i * k + curr.lv.i * k * lvc)),
                      fill=(0, 0, 255), width=3)
            uvc = (R + 1) / curr.uv.length()
            draw.line(((curr.parent.j * k, curr.parent.i * k),
                       (curr.parent.j * k + curr.uv.j * k * uvc, curr.parent.i * k + curr.uv.i * k * uvc)),
                      fill=(0, 0, 255), width=3)

            # curr
        draw.ellipse((curr.j * k - r, curr.i * k - r, curr.j * k + r, curr.i * k + r), fill=(52, 152, 219))
        draw.line(((curr.j * k, curr.i * k), (curr.parent.j * k, curr.parent.i * k)), fill=(189, 42, 132), width=5)

        # static curr
        if curr in parents:
            static_draw.ellipse((curr.j * k - r, curr.i * k - r, curr.j * k + r, curr.i * k + r),
                                fill=(52, 152, 219, 100))
            static_draw.line(((curr.j * k, curr.i * k), (curr.parent.j * k, curr.parent.i * k)),
                             fill=(189, 42, 132, 100), width=5)

        self.ims.append(im)
        if show:
            _, ax = plt.subplots(dpi=150)
            ax.axes.xaxis.set_visible(False)
            ax.axes.yaxis.set_visible(False)
            plt.imshow(np.asarray(im))
            plt.show()

    def save(self, path, duration=30):
        self.ims[0].save(path, save_all=True, append_images=self.ims[1:], optimize=False,
                         duration=duration * len(self.ims), loop=0)


def draw_path(grid_map, start_i, start_j, goal_i, goal_j, goal, store_path, duration, onAPRays=True):
    current = goal
    path = []
    drawer = Drawer(grid_map, Point(start_i, start_j), Point(goal_i, goal_j))
    parents = set()
    while current.prev != current:
        parents.add(current.parent)
        path.append(current)
        current = current.prev
    path.reverse()
    for node in path:
        drawer.cute_draw(node, parents, False, onAPRays)
    drawer.save(store_path, duration)


def theta_ap_draw(grid_map, start_i, start_j, goal_i, goal_j, heuristic_func=None, search_tree=None,
                  store_path="theta.gif", duration=30, onAPRays=True):
    start_time = datetime.now()  # statistic

    stats = Stats()  # statistic

    grid_map.add_special_point((goal_i, goal_j))

    ast = search_tree()
    start = NodeAP(start_i, start_j, g=0, parent=None, prev=None)
    start.apply_heuristic(heuristic_func, goal_i, goal_j)
    ast.add_to_open(start)

    while not ast.open_is_empty():
        curr = ast.get_best_node_from_open()
        if curr is None:
            break

        ast.add_to_closed(curr)

        if (curr.i == goal_i) and (curr.j == goal_j):  # curr is goal
            stats.runtime = datetime.now() - start_time  # statistic
            stats.way_length = make_path(curr)[1]  # statistic
            draw_path(grid_map, start_i, start_j, goal_i, goal_j, curr, store_path, duration, onAPRays)
            return True, curr, stats, ast.OPEN, ast.CLOSED

        # expanding curr
        stats.expansions += 1  # statistic
        successors = getSuccessors(curr, grid_map, goal_i, goal_j, heuristic_func, start_i, start_j, ast)

        for node in successors:
            if not ast.was_expanded(node):
                ast.add_to_open(node)

        stats.max_tree_size = max(stats.max_tree_size, len(ast))  # statistic

    stats.runtime = datetime.now() - start_time  # statistic
    stats.way_length = 0  # statistic
    print("Path not found!")
    return False, None, stats, ast.OPEN, ast.CLOSED


# it draws gif and save it to 'store_path'
def draw_gif(grid_map, start=None, goal=None, store_path="theta.gif", duration=30, onAPRays=True):
    theta_ap_draw(grid_map, start[0], start[1], goal[0], goal[1], euclidian_distance, SearchTreePQS,
                  store_path, duration, onAPRays)


# it draws final path and shows it
def draw_png(grid_map, start=None, goal=None):
    _, _, stats, _, _ = theta_ap(grid_map, start[0], start[1], goal[0], goal[1], euclidian_distance, SearchTreePQS)
    draw_static(grid_map, start, goal, stats.path)
