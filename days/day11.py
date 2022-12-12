from utils import Clock, read_data
from pprint import pprint
from math import floor
import re

clock = Clock()
clock.tic()

data = read_data()


class Monkey:
    def __init__(self, attrs) -> None:
        pattern = re.compile(r"\d+")
        self._no = int(pattern.search(attrs[0])[0])
        self.items = [int(item) for item in pattern.findall(attrs[1])]
        self.op = re.search(r"Operation: (.+)", attrs[2]).groups()[0]
        self.test = int(pattern.search(attrs[3])[0])
        self.true = int(pattern.search(attrs[4])[0])
        self.false = int(pattern.search(attrs[5])[0])
        self.counter = 0


monkeys = [data[i:i+7] for i in range(0, len(data), 7)]
monkeys = [Monkey(monkey) for monkey in monkeys]
monkeys = {monkey._no: monkey for monkey in monkeys}

rounds = 20
for _ in range(rounds):
    for monkey in monkeys.values():
        monkey.counter += len(monkey.items)
        for item in monkey.items:
            old = item
            exec(monkey.op)
            new = floor(new / 3)
            if new % monkey.test:
                monkeys[monkey.false].items += [new]
            else:
                monkeys[monkey.true].items += [new]
        monkey.items = []


monkey_business = sorted([monkey.counter for monkey in monkeys.values()])
silver = monkey_business[-1] * monkey_business[-2]
clock.toc(f"Silver {silver}")
clock.tic()

monkeys = [data[i:i+7] for i in range(0, len(data), 7)]
monkeys = [Monkey(monkey) for monkey in monkeys]
monkeys = {monkey._no: monkey for monkey in monkeys}

modulos = [monkey.test for monkey in monkeys.values()]
modulo = 1
for m in modulos:
    modulo *= m

rounds = 10000
for _ in range(rounds):
    for monkey in monkeys.values():
        monkey.counter += len(monkey.items)
        for item in monkey.items:
            old = item
            exec(monkey.op)
            new %= modulo
            if new % monkey.test:
                monkeys[monkey.false].items += [new]
            else:
                monkeys[monkey.true].items += [new]
        monkey.items = []

monkey_business = sorted([monkey.counter for monkey in monkeys.values()])
gold = monkey_business[-1] * monkey_business[-2]
clock.toc(f"Gold {gold}")
