from utils import Clock, read_data
from pprint import pprint
from collections import namedtuple
import re


clock = Clock()
clock.tic()

data = read_data()

cave = {}

Sensor = namedtuple("Sensor", ["x", "y", "beacon"])
Beacon = namedtuple("Beacon", ["x", "y"])
pattern = re.compile(r"x=(.+), y=(.+)")
up, down, left, right = 0, 0, 0, 0
for line in data:
    sensor, beacon = line.split(":")
    beacon = [*map(int, pattern.search(beacon).groups())]
    beacon = Beacon(beacon[0], beacon[1])
    sensor = [*map(int, pattern.search(sensor).groups())]
    sensor = Sensor(sensor[0], sensor[1], beacon)
    cave[(sensor.x, sensor.y)] = sensor
    cave[(beacon.x, beacon.y)] = beacon
    up = min(up, sensor.y, beacon.y)
    down = max(down, sensor.y, beacon.y)
    left = min(left, sensor.x, beacon.x)
    right = max(right, sensor.x, beacon.x)


sensors = [spot for spot in cave.values() if isinstance(spot, Sensor)]
sensors_radius = {sensor: abs(sensor.x - sensor.beacon.x) + abs(sensor.y - sensor.beacon.y) for sensor in sensors}


def see_cave(cave_to_see):
    print()
    for y in range(up - 6, down + 6):
        print(f"{y:>2}|| ", end="")
        for x in range(left - 6, right + 6):
            char = "."
            if thing := cave_to_see.get((x, y)):
                char = ["B", "S"][isinstance(thing, Sensor)]
                if thing == "#":
                    char = "#"
            print(char, end="")
        print()
    print()


def beep(sensor, good_line):
    vertical = abs(sensor.y - good_line)
    radius = sensors_radius[sensor]
    radius = radius - vertical
    return (sensor.x - radius, sensor.x + radius) if radius >= 0 else None


def get_hits(good_line):
    hits = []
    for sensor in sensors:
        if beep_result := beep(sensor, good_line):
            hits += [beep_result]
    return hits


def line_score(good_line):
    hits = get_hits(good_line)
    score = set()
    for hit in hits:
        forbidden_pos = set([*range(hit[0], hit[1]+1)])
        score.update(forbidden_pos)
    other_stuff = len([stuff for stuff in cave.values() if stuff.y == good_line])
    return len(score) - other_stuff


silver = line_score(2000000)
clock.toc(f"Silver {silver}")
clock.tic()


lookup = [0, 4000000]


def line_score_gold(good_line):
    hits = get_hits(good_line)
    forbidden_pos = []
    for hit in hits:
        forbidden_pos += [[max(lookup[0], hit[0]), min(hit[1]+1, lookup[1])]]
    starts = sorted([pos[0] for pos in forbidden_pos])
    ends = sorted([pos[1] for pos in forbidden_pos])
    for n, start in enumerate(starts):
        if ends[n] == lookup[1]:
            break
        if starts[n+1] > ends[n]:
            return ends[n]
    return 0


gold = 0
for y in range(4000000):
    if score := line_score_gold(y):
        gold = score * 4000000 + y
        break

clock.toc(f"Gold {gold}")
