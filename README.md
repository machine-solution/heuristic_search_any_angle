# Для аналитики

Давайте примем несколько соглашений о сигнатуре функций поиска.  
1. Функция поиска  ```search_function``` должна принимать на вход следующие параметры:
```
def search_function(grid_map, start_i, start_j, goal_i, goal_j, heuristic_func = None, search_tree = None, w = 1, *args, **kwargs);
```
w - число, на которое умножается эвристика. С большой вероятностью мы хотим подвигать его в алгоритмах и посмотреть что получится.  
Важно, что если у вас есть дополнительные аргументы, например k в алгоритме 2^k A*, напишите в комментарии что это за аргументы, чтобы было ясно что туда передавать и как это тестить.  

2. Возвращать функция должна тройку: 
```
(path_found, last_node, stats)
```
Где stats имеет тип Stats, определённый ниже. Помеченные поля алгоритм должен заполнить соответствующей статистикой.  
Для своих целей после трёх перечисленных значений можно возвращать всё, что угодно. Например, для отрисовки возвращать список раскрытых вершин.  

```
# using for counting statistics and returning it as one variable
class Stats:
    def __init__(self):
        self.difficulty = 0
        self.expansions = 0 # algorithm must set this value
        self.runtime = 0 # algorithm must set this value
        self.way_length = 0 # algorithm must set this value
        self.suboptimal = 0
        self.max_tree_size = 0 # algorithm must set this value

```

3. Про карты в movingai:  
В картах, с которыми имел дело лично я, препятствия обозначаются '@' и 'T', а свободные клетки '.'

# В целом идеи по проекту

Пишите сюда что-нибудь прикольное, чтобы не забыть. Например:  
- При обилии времени можно нарисовать свои running examples для алгоритмов.
