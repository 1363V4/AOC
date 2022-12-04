from utils import Clock, read_data
from pprint import pprint

clock = Clock()

clock.tic()

data = read_data()


def contains(a, b, m, n):
    a, b, m, n = map(int, [a, b, m, n])
    return (a-m)*(b-n) <= 0


silver = 0
for datum in data:
    up, down = datum.split(",")
    [a, b], [m, n] = up.split("-"), down.split("-")
    silver += contains(a, b, m, n)

clock.toc(f"Silver {silver}")
clock.tic()


def overlaps(a, b, m, n):
    a, b, m, n = map(int, [a, b, m, n])
    return not (b < m or a > n)


gold = 0
for datum in data:
    up, down = datum.split(",")
    [a, b], [m, n] = up.split("-"), down.split("-")
    gold += overlaps(a, b, m, n)

clock.toc(f"Gold: {gold}")
