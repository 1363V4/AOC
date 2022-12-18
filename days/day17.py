from utils import Clock, read_data
from pprint import pprint
from itertools import cycle


clock = Clock()
clock.tic()

data = read_data()
jet_length = len(data[0])
print(jet_length)
jets = cycle([jet for jet in data[0]])
rocks = cycle(["hor", "cro", "ang", "ver", "sqr"])
x_start = 3

def solve(nb_rocks):
    cave = {x: [0] for x in range(9)}
    memory = []
    jet_counter = 0
    for _ in range(nb_rocks):
        if _ % 5000 < 1:
            print(f"{100 * _ / nb_rocks:.04}%")
        max_height = 0
        for values in cave.values():
            max_height = max(max_height, max(values))
        max_height += 4
        new_rock = next(rocks)
        match new_rock:
            case "hor":
                rock = [
                    (max_height, x_start),
                    (max_height, x_start + 1),
                    (max_height, x_start + 2),
                    (max_height, x_start + 3),
                    ]
            case "cro":
                rock = [
                    (max_height, x_start + 1),
                    (max_height + 1, x_start),
                    (max_height + 1, x_start + 1),
                    (max_height + 1, x_start + 2),
                    (max_height + 2, x_start + 1),
                ]
            case "ang":
                rock = [
                    (max_height, x_start),
                    (max_height, x_start + 1),
                    (max_height, x_start + 2),
                    (max_height + 1, x_start + 2),
                    (max_height + 2, x_start + 2),
                ]
            case "ver":
                rock = [
                    (max_height, x_start),
                    (max_height + 1, x_start)
                    ,
                    (max_height + 2, x_start),
                    (max_height + 3, x_start),
                ]
            case "sqr":
                rock = [
                    (max_height, x_start),
                    (max_height, x_start + 1),
                    (max_height + 1, x_start),
                    (max_height + 1, x_start + 1),
                ]
            case _:
                print("fuck")
        can_move = True
        first_check = True
        while can_move:
            new_jet = next(jets)
            jet_counter = (jet_counter + 1) % jet_length
            if first_check:
                if (jet_counter, new_rock) in memory:
                    #return _, cave, memory
                    pass
                memory += [(jet_counter, new_rock)]
                first_check = False
            can_jet = True
            match new_jet:
                case "<":
                    possible_pos = [(t[0], t[1] - 1) for t in rock]
                    for elem in possible_pos:
                        if elem[0] in cave[elem[1]]:
                            can_jet = False
                        if elem[1] < 1:
                            can_jet = False
                    if can_jet:
                        rock = possible_pos
                case ">":
                    possible_pos = [(t[0], t[1] + 1) for t in rock]
                    for elem in possible_pos:
                        if elem[0] in cave[elem[1]]:
                            can_jet = False
                        if elem[1] > 7:
                            can_jet = False
                    if can_jet:
                        rock = possible_pos
            possible_pos = [(t[0] - 1, t[1]) for t in rock]
            for elem in possible_pos:
                if elem[0] in cave[elem[1]]:
                    can_move = False
                if elem[0] == 0:
                    can_move = False
            if can_move:
                rock = possible_pos
        for elem in rock:
            cave[elem[1]] += [elem[0]]
    return cave

#silver = solve(2022)
#print(gold)
#gold = solve(jet_length * 5)
gold = solve(13345)
for k, v in gold.items():
    print(k, ".", max(v))
#clock.toc(f"Silver {silver}")
clock.tic()

# 1644633831302
# too high
# 1590305828044 ?
# too high
# 1581092062256
# nope... filtered

gold = 0
clock.toc(f"Gold {gold}")
