# Any-Angle Pathfinding algorithms (2^k A*, Theta, Anya)

## Description

A project at St Petersburg University.

We implemented and compared these Any-Angle Pathfinding algorithms:
- 2^k A\*
    - regular 2^k A\* with euclidian and $h_{2^k}$ heuristics;
    - canonical 2^k A\* with euclidian and $h_{2^k}$ heuristics;
- Theta
    - Basic Theta
    - Lazy Theta
    - Theta Angle Propagation
- Anya

## Demo

- [Visualization of paths found by different algorithms](demo/main_demo.ipynb)
- [Animation of running Theta](demo/animation_for_theta.ipynb)
- [Visualization of 2^k A* with expanded nodes](demo/extra_plots_for_2k_astar.ipynb)

## Algorithm comparison

We run algorithms on maps ... (links, names)

All data is stored in folder [analysis](analysis).

[Notebook with analytics](https://github.com/machine-solution/heuristic_search_any_angle/blob/restructure/graphics.ipynb)

## Installation

Clone repository:
```
git clone https://github.com/machine-solution/heuristic_search_any_angle
cd heuristic_search_any_angle
```

Install requirements:
```
python -m pip install -r requirements.txt
```

Please make sure you have Jupyter Notebook installed (or something else to open .ipynb files).

You can do it with pip:
```
python -m pip install notebook
```

And then you can start it like that:
```
python -m notebook
```

## Getting started

The main entrance point is IPython notebook `demo/main_demo.ipynb`.

There you can try different maps and get visualization of paths that were found by different algorithms.

API of the algorithms can be found in files `any_angle/[algorithm]/api.py`, where `algorithm` can be `_2k_astar`, `theta`, `anya` or `full_graph` (the last is a brute-force algorithm used for testing).

Abstract API is described in `any_angle/common/api.py`.

## References

[1] Rivera, N., Hernández, C., Hormazábal, N. and Baier, J.A., 2020. [The 2^ k Neighborhoods for Grid Path Planning. Journal of Artificial Intelligence Research, 67, pp.81-113.](https://www.jair.org/index.php/jair/article/view/11383)

[2] Daniel, K., Nash, A., Koenig, S. and Felner, A., 2010. [Theta*: Any-angle path planning on grids. Journal of Artificial Intelligence Research, 39, pp.533-579.](https://www.jair.org/index.php/jair/article/view/10676)

[3] Harabor, D.D., Grastien, A., Öz, D. and Aksakalli, V., 2016. [Optimal any-angle pathfinding in practice. Journal of Artificial Intelligence Research, 56, pp.89-118.](https://www.jair.org/index.php/jair/article/view/11383)

## Mentor

Yakovlev Konstantin Sergeevich

## Us

- Andrey Zaytsev
- Maria Radionova
- Ekaterina Tochilina
