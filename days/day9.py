from utils import Clock, read_data
from pprint import pprint

clock = Clock()

clock.tic()

data = read_data()
data = [datum.split() for datum in data]

head = {'x': 0, 'y': 0}
tail = {'x': 0, 'y': 0}


def move(direction, knot):
    match direction:
        case "L":
            knot['x'] -= 1
        case "R":
            knot['x'] += 1
        case "U":
            knot['y'] += 1
        case "D":
            knot['y'] -= 1


def get_delta(head, tail):
    return {'dx': head['x'] - tail['x'], 'dy': head['y'] - tail['y']}


def adjust_delta(delta):
    for k, v in delta.items():
        if v in [-2, 2]:
            delta[k] = v / 2


def too_far(delta):
    return not (abs(delta['dx']) <= 1 and abs(delta['dy']) <= 1)


visited = set()
for direction, times in data:
    times = int(times)
    for _ in range(times):
        move(direction, head)
        delta = get_delta(head, tail)
        if too_far(delta):
            adjust_delta(delta)
            tail['x'] += delta['dx']
            tail['y'] += delta['dy']
        visited.add((tail['x'], tail['y']))

silver = len(visited)

clock.toc(f"Silver {silver}")
clock.tic()

rope = {n: {'x': 0, 'y': 0} for n in range(10)}
head = rope[0]
visited = set()
for direction, times in data:
    times = int(times)
    for _ in range(times):
        move(direction, head)
        for n in range(0, 9):
            current, follow = rope[n], rope[n+1]
            delta = get_delta(current, follow)
            if too_far(delta):
                adjust_delta(delta)
                follow['x'] += delta['dx']
                follow['y'] += delta['dy']
        visited.add((follow['x'], follow['y']))

gold = len(visited)
clock.toc(f"Gold {gold}")
