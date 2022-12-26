# Полученные результаты по итогам экспериментов

## 2^k A*

* Канонический 2^k A* значительно быстрее классической версии

![Normed runtime](analysis/graphics/canonical_vs_basic_normed_runtime.png)
![Runtime](analysis/graphics/canonical_vs_basic_runtime.png)

* С увеличением k существенно уменьшается длина пути и немного увеличивается время работы. 

* На практике почти для любых карт эвристика h_2k хуже, чем расстояние евклида.

*Карта из игры Startcraft, на 3 других результаты аналогичные*
![Starcraft runtime](analysis/graphics/k-dynamic_runtime_sc.png)
![Starcraft suboptimality](analysis/graphics/k-dynamic_suboptimal_sc.png)

*Карта Random*
![Random runtime](analysis/graphics/k-dynamic_runtime_random.png)
![Random suboptimality](analysis/graphics/k-dynamic_suboptimal_random.png)

## Theta

* Lazy Theta значительно быстрее Basic Theta

![Lazy vs Basic normed runtime](analysis/graphics/lazy_vs_basic_normed_runtime.png)
![Lazy vs Basic runtime](analysis/graphics/lazy_vs_basic_runtime.png)

* Theta Angle Propagation на сложных для алгоритма (но не на всех) картах даёт существенный выигрыш в скорости взамен на длину пути

![Lazy vs Basic normed runtime](analysis/graphics/ap_vs_lazy_normed_runtime.png)
![Lazy vs Basic runtime](analysis/graphics/ap_vs_lazy_runtime.png)
![Lazy vs Basic suboptimality](analysis/graphics/ap_vs_lazy_suboptimal.png)

* Новая взвешенная эвристика позволяет находить более короткие пути, но увеличивает время работы

*Карта City*
![Weighted heuristic city runtime](analysis/graphics/theta_heuristic_runtime_city.png)
![Weighted heuristic city suboptimal](analysis/graphics/theta_heuristic_suboptimal_city.png)

*Карта Random*
![Weighted heuristic random runtime](analysis/graphics/theta_heuristic_runtime_random.png)
![Weighted heuristic random suboptimal](analysis/graphics/theta_heuristic_suboptimal_random.png)

## Сравнение разных алгоритмов

* Чаще самый быстрый алгоритм -- 2^k A* за счёт быстрого раскрытия вершин. Алгоритм Anya имеет более сложную логику раскрытия и требует больше времени, зато общее число раскрытий значительно меньше. Theta делает примерно столько же раскрытий, сколько и 2^k A*, а сложность логики и необходимое время немногим меньше, чем у Anya, поэтому этот алгоритм значительно долше других

*Карта Starcraft*
![Starcraft runtime](analysis/graphics/runtime_sc.png)
![Starcraft expansions](analysis/graphics/expansions_sc.png)

*Карта City*
![City runtime](analysis/graphics/runtime_city.png)
![City expansions](analysis/graphics/expansions_city.png)

*Карта Maze*
![Maze runtime](analysis/graphics/runtime_maze.png)
![Maze expansions](analysis/graphics/expansions_maze.png)

*Карта Random*
![Random runtime](analysis/graphics/runtime_random.png)
![Random expansions](analysis/graphics/expansions_random.png)

*Карта Room*
![Room runtime](analysis/graphics/runtime_room.png)
![Room expansions](analysis/graphics/expansions_room.png)

* Все алгоритмы находят очень близкие к оптимальным пути

*На всех картах результаты практически одинаковые*
![General suboptimality](analysis/graphics/extra_suboptimal_general.png)

