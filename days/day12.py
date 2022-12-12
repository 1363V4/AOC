from utils import Clock, read_data
from pprint import pprint
import string
import heapq
from functools import cache

clock = Clock()
clock.tic()

data = read_data()
W, H = len(data[0]), len(data)

grid = {
    (i, j): char
    for i, datum in enumerate(data)
    for j, char in enumerate(datum)
    }

for coord, char in grid.items():
    if char == "S":
        S = coord
    if char == "E":
        E = coord

string_value = {char: n for n, char in enumerate(string.ascii_lowercase)}
string_value.update({'S': 0, 'E': 25})


@cache
def get_neighbours(node):
    i, j = node
    neighbours = []
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        if grid.get((i+di, j+dj), False):
            neighbours += [((i+di, j+dj))]
    return neighbours


graph = {}
for node in grid:
    d = {}
    for neighbour in get_neighbours(node):
        if string_value[grid[neighbour]] < string_value[grid[node]] + 2:
            d.update({neighbour: 1})
    graph[node] = d


def dijkstra(start=S):
    q = [(0, start, [])]
    visited = set()
    known_paths = {start: 0}
    BIGNUM = 9999999
    while q:
        cost, node, path = heapq.heappop(q)
        if node not in visited:
            visited.add(node)
            path = [node] + path
            if node == E:
                return path
            for move, move_cost in graph[node].items():
                if move in visited:
                    continue
                best_so_far = known_paths.get(move, BIGNUM)
                alt_cost = cost + move_cost
                if alt_cost < best_so_far:
                    known_paths[move] = alt_cost
                    to_check = (alt_cost, move, path)
                    heapq.heappush(q, to_check)


def path_check(path):
    for i in range(H):
        for j in range(W):
            print([".", grid[(i, j)]][(i, j) in path], end="")
        print("")


silver_path = dijkstra()
path_check(silver_path)

silver = len(silver_path) - 1
clock.toc(f"Silver {silver}")
clock.tic()

why_not_bruteforce = [coord for coord, char in grid.items() if char == 'a']
paths = {}
while why_not_bruteforce:
    a = why_not_bruteforce.pop(0)
    a_path = dijkstra(start=a)
    if a_path:
        paths[len(a_path)] = a_path

path_check(paths[min(paths)])

gold = min(paths) - 1
clock.toc(f"Gold {gold}")
