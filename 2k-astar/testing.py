from numpy.random import randint
from grid import Node
from visualisation import draw
from utils import make_path


def simple_test(unfilled_grid_map, search_func, task, *args, **kwargs):
    '''
    simple_test runs search_func on one task (use a number from 0 to 25 to choose a certain debug task on simple map or
    None to choose a random task from this pool) with *args as optional arguments and displays:
     - 'Path found!' and some statistics -- path was found
     - 'Path not found!' -- path was not found
     - 'Execution error' -- an error occurred while executing the SearchFunction In first two cases function also draws
     visualisation of the task
    '''
    height = 15
    width = 30
    map_str = '''
. . . . . . . . . . . . . . . . . . . . . @ @ . . . . . . .  
. . . . . . . . . . . . . . . . . . . . . @ @ . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . @ @ . . . . . . . 
. . . @ @ . . . . . . . . . . . . . . . . @ @ . . . . . . . 
. . . @ @ . . . . . . . . @ @ . . . . . . @ @ . . . . . . . 
. . . @ @ . . . . . . . . @ @ . . . . . . @ @ @ @ @ . . . . 
. . . @ @ . . . . . . . . @ @ . . . . . . @ @ @ @ @ . . . . 
. . . @ @ . . . . . . . . @ @ . . . . . . . . . . . . . . . 
. . . @ @ . . . . . . . . @ @ . . . . . . . . . . . . . . . 
. . . @ @ . . . . . . . . @ @ . . . . . . . . . . . . . . . 
. . . @ @ . . . . . . . . @ @ . . . . . . . . . . . . . . . 
. . . @ @ . . . . . . . . @ @ . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . @ @ . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . @ @ . . . . . . . . . . . . . . .
. . . . . . . . . . . . . @ @ . . . . . . . . . . . . . . .
'''

    task_map = unfilled_grid_map
    task_map.read_from_string(map_str, width, height)
    starts = [(9, 0), (13, 0), (7, 28), (14, 29), (4, 1), (0, 17), (5, 6), (5, 20), (12, 2), (7, 28), (11, 9), (3, 2),
              (3, 17), (13, 20), (1, 1), (9, 10), (14, 6), (2, 0), (9, 28), (8, 6), (11, 6), (3, 0), (8, 9), (14, 7),
              (12, 4)]
    goals = [(11, 20), (2, 19), (6, 5), (4, 18), (9, 20), (7, 0), (2, 25), (12, 4), (3, 25), (0, 12), (4, 23), (2, 24),
             (9, 2), (1, 6), (13, 29), (14, 29), (2, 28), (14, 16), (13, 0), (1, 27), (14, 25), (10, 20), (12, 28),
             (2, 29), (1, 29)]
    lengths = [36, 30, 30, 21, 28, 24, 32, 27, 42, 23, 35, 37, 23, 26, 40, 36, 42, 28, 44, 36, 38, 29, 33, 42, 44]

    if (task is None) or not (0 <= task < 25):
        task = randint(0, 24)

    start = Node(*starts[task])
    goal = Node(*goals[task])
    length = lengths[task]
    try:
        result = search_func(task_map, start.i, start.j, goal.i, goal.j, *args, **kwargs)
        number_of_expansions = result[2].expansions
        nodes_created = result[2].max_tree_size
        nodes_opened = result[3]
        nodes_expanded = result[4]
        if result[0]:
            path = make_path(result[1])
            correct = int(path[1]) == int(length)
            print("Path found! Length: " + str(path[1]) +
                  ". Nodes created: " + str(nodes_created) +
                  ". Number of steps: " + str(number_of_expansions) + ". Correct: " + str(correct) +
                  ". Runtime: " + str(result[2].runtime) + "ms.")
            draw(task_map, start, goal, path[0], nodes_opened, nodes_expanded)
        else:
            print("Path not found!")
        return result

    except Exception as e:
        print("Execution error")
        print(e)
