from utils import Clock, read_data
from pprint import pprint


clock = Clock()
clock.tic()

data = read_data()

cave = {}
j = complex(0, 1)


def add_line(start, end):
    if start.real == end.real:
        delta = int(end.imag - start.imag)
        direction = (delta // abs(delta)) * j
    else:
        delta = int(end.real - start.real)
        direction = delta // abs(delta)
    cave[start] = "#"
    for y in range(abs(delta)):
        start += direction
        cave[start] = "#"


for lines in data:
    points = lines.split(" -> ")
    while points:
        start = [*map(int, points.pop(0).split(","))]
        start = start[0] + start[1] * j
        if points:
            end = [*map(int, points[0].split(","))]
            end = end[0] + end[1] * j
            add_line(start, end)


xs = [int(x.real) for x in cave]
ys = [int(y.imag) for y in cave]
left, right = min(xs), max(xs)+1
up, down = 0, max(ys)


def see_cave(cave_to_see):
    for y in range(up, down+2):
        for x in range(left, right):
            char = cave_to_see.get((x+y*j), ".")
            print(char, end="")
        print()


SAND_START = 500 + 0*j
cave[SAND_START] = "+"
gold_cave = {k: v for k, v in cave.items()}

flowing_into_the_eternal_abyss = False
possible_moves = [1*j, -1+1*j, 1+1*j]
sand_pos = SAND_START
sand_count = 0
while not flowing_into_the_eternal_abyss:
    for move in possible_moves:
        if cave.get(sand_pos + move, ".") == ".":
            sand_pos += move
            break
    else:
        cave[sand_pos] = "o"
        sand_count += 1
        sand_pos = SAND_START
    if sand_pos.imag > down:
        flowing_into_the_eternal_abyss = True


#see_cave(cave)
silver = sand_count
clock.toc(f"Silver {silver}")
clock.tic()

infinity = 168
down += 2
for x in range(left - infinity, right + infinity):
    gold_cave[x + down*j] = "#"

sand_pos = SAND_START
sand_count = 0
source = False
while not source:
    for move in possible_moves:
        if gold_cave.get(sand_pos + move, ".") == ".":
            sand_pos += move
            break
    else:
        if sand_pos == SAND_START:
            source = True
        gold_cave[sand_pos] = "o"
        sand_count += 1
        sand_pos = SAND_START

#see_cave(gold_cave)

gold = sand_count
clock.toc(f"Gold {gold}")
