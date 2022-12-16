from utils import Clock, read_data
from pprint import pprint
import re
import heapq
from itertools import combinations, permutations
from collections import defaultdict


clock = Clock()
clock.tic()

data = read_data()


valves = {}
for line in data:
    big_v, name, *tunnels = re.findall(r"[A-Z]+", line)
    flow_rate = int(re.search(r"\d+", line).group())
    valves[name] = {'flow_rate': flow_rate, 'tunnels': tunnels}


good_ones = ["AA"]
for name, valve in valves.items():
    if valve['flow_rate'] != 0:
        good_ones += [name]


graph = {}
for name in valves:
    graph[name] = {tunnel: 1 for tunnel in valves[name]['tunnels']}


def dijkstra(start, end):
    q = [(0, start, [])]
    visited = set()
    known_paths = {start: 0}
    BIGNUM = 999999999
    while q:
        cost, node, path = heapq.heappop(q)
        if node not in visited:
            visited.add(node)
            path = [node] + path
            if node == end:
                return path
            for move, move_cost in graph[node].items():
                best_so_far = known_paths.get(move, BIGNUM)
                alt_cost = cost + move_cost
                if alt_cost < best_so_far:
                    known_paths[move] = alt_cost
                    to_check = (alt_cost, move, path)
                    heapq.heappush(q, to_check)


good_pairs = combinations(good_ones, 2)
good_graph = defaultdict(dict)
for pair in good_pairs:
    start, end = pair
    result = {
        end: {
            'cost': len(dijkstra(start, end)),
            'flow_rate': valves[end]['flow_rate']
            }
    }
    good_graph[start].update(result)


inverse_path = defaultdict(dict)
for name, moves in good_graph.items():
    for move_name, move_attrs in moves.items():
        result = {
            name: {
                'cost': move_attrs['cost'],
                'flow_rate': valves[name]['flow_rate']
                }
            }
        inverse_path[move_name].update(result)


for inverse_name, inverse_attrs in inverse_path.items():
    good_graph[inverse_name].update(inverse_attrs)


silver_path = {}
best_score = 0
SCOPE = 6
good_ones.remove("AA")
possible_paths = map(list, permutations(good_ones, SCOPE))
for path in possible_paths:
    start = "AA"
    time = 30
    score = 0
    path_memory = [start]
    while path:
        end = path.pop(0)
        path_memory += [end]
        time -= good_graph[start][end]['cost']
        if time < 0:
            break
        score += time * good_graph[start][end]['flow_rate']
        start = end
    if score > best_score:
        best_score = score
        silver_path = {score: path_memory}


print(f"Best path: {silver_path}")
silver = silver_path.popitem()[0]
clock.toc(f"Silver {silver}")
clock.tic()


gold_path = {}
SCOPE = 6
possible_paths = map(list, permutations(good_ones, SCOPE))
memories = []
for path in possible_paths:
    time = 26
    start = "AA"
    path_memory = {start: 0}
    while path:
        end = path.pop(0)
        time -= good_graph[start][end]['cost']
        if time < 0:
            break
        path_memory[end] = time * good_graph[start][end]['flow_rate']
        start = end
    memories += [path_memory]


memories = [(sum(memory.values()), memory) for memory in memories]
memories = sorted(memories, key=lambda x: x[0], reverse=True)[:5000]
memories = [memory[1] for memory in memories]


best_score = 0
for memory in combinations(memories, 2):
    human, elephant = memory
    seen = set()
    score = 0
    for step_human, step_elephant in zip(human, elephant):
        if step_human not in seen:
            score += human[step_human]
            seen.add(step_human)
        if step_elephant not in seen:
            score += elephant[step_elephant]
            seen.add(step_elephant)
    if score > best_score:
        best_score = score

print(f"Human goes {human},\nElephant goes {elephant}")
gold = best_score
clock.toc(f"Gold {gold}")
