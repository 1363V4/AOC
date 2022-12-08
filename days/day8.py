from utils import Clock, read_data
from pprint import pprint

clock = Clock()

clock.tic()

data = read_data()
data = [[int(char) for char in datum] for datum in data]
data = {
    (l, c): {"size": tree, "visible": False, "scenic": 1}
    for l, row in enumerate(data)
    for c, tree in enumerate(row)
}

directions = {
    "left": lambda t: (t[0], t[1]-1),
    "up": lambda t: (t[0]-1, t[1]),
    "right": lambda t: (t[0], t[1]+1),
    "down": lambda t: (t[0]+1, t[1]),
}


def is_visible(coords, tree, direction):
    if tree["visible"]:
        return
    while True:
        coords = directions[direction](coords)
        if data.get(coords, False):
            if data[coords]["size"] >= tree["size"]:
                return
        else:
            break
    tree["visible"] = True


for coords, tree in data.items():
    for direction in directions:
        is_visible(coords, tree, direction)

d_visible = [v for v in data.values() if v["visible"]]
silver = len(d_visible)

clock.toc(f"Silver {silver}")
clock.tic()


def scenic_score(coords, tree, direction):
    seen = 0
    while True:
        coords = directions[direction]((coords))
        if data.get((coords), False):
            seen += 1
            size = data[(coords)]["size"]
            if size >= tree["size"]:
                break
        else:
            break
    return seen


for coords, tree in data.items():
    for direction in directions:
        tree["scenic"] *= scenic_score(coords, tree, direction)

gold = max([tree["scenic"] for tree in data.values()])
clock.toc(f"Gold {gold}")
