from utils import Clock, read_data
from pprint import pprint
from collections import deque
from copy import deepcopy

clock = Clock()

clock.tic()

with open("input.txt") as f:
    data = [datum[:-1] for datum in f.readlines()]

# parsing

stacks, instructions = data[:data.index("")], data[data.index("")+1:]
stacks, stacks_nos = stacks[:-1], stacks[-1]
stacks = [stack.replace("    ", " _ ").strip() for stack in stacks]
stacks = [stack.replace("  ", " ").strip() for stack in stacks]
stacks = [stack.split(" ") for stack in stacks]
stacks_nos = map(int, stacks_nos.split())
instructions = [ins.split() for ins in instructions]
instructions = [[ins[1], ins[3], ins[5]] for ins in instructions]
instructions = [[*map(int, ins)] for ins in instructions]

# building stacks

d_stacks = {no: deque() for no in stacks_nos}
for stack in stacks:
    for n, col in enumerate(stack):
        if col != "_":
            d_stacks[n+1].append(col[1])

# move 9000
        
silver = deepcopy(d_stacks)
for ins in instructions:
    _move, _from, _to = ins
    buffer = []
    for _ in range(_move):
        buffer += silver[_from].popleft()
    for b in buffer:
        silver[_to].appendleft(b)

silver = [stack.popleft() for stack in silver.values()]
silver = "".join(silver)

clock.toc(f"Silver {silver}")
clock.tic()

# move 9001

gold = deepcopy(d_stacks)
for ins in instructions:
    _move, _from, _to = ins
    buffer = []
    for _ in range(_move):
        buffer += gold[_from].popleft()
    for b in buffer[::-1]:
        gold[_to].appendleft(b)

gold = [stack.popleft() for stack in gold.values()]
gold = "".join(gold)

clock.toc(f"Gold {gold}")
