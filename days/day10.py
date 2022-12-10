from utils import Clock, read_data
from collections import defaultdict

clock = Clock()
clock.tic()

data = read_data()
data = [datum.split() for datum in data]

checks = [n * 40 + 20 for n in range(6)]
register = 1
cycles = 1
memory = {1: 1}
for ins in data:
    match ins:
        case ["noop"]:
            cycles += 1
            memory[cycles] = register
        case ["addx", n]:
            cycles += 1
            memory[cycles] = register
            cycles += 1
            register += int(n)
            memory[cycles] = register

silver = 0
for k, v in memory.items():
    if k in checks:
        silver += k*v

clock.toc(f"Silver {silver}")
clock.tic()

W, H = 40, 6
sprite = [0, 1, 2]
buffer = []
for n, (k, v) in enumerate(memory.items()):
    n = n % 40
    sprite = [v-1, v, v+1]
    buffer += [".", "#"][n in sprite]

screen = defaultdict(str)
for n, char in enumerate(buffer):
    line = n // W
    screen[line] += char

for line in range(H):
    print(screen[line])
