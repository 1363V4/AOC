from utils import Clock, read_data
from pprint import pprint

clock = Clock()

clock.tic()

data = read_data()

data = "_".join(data)

data = data.split("__")

data = [datum.split("_") for datum in data]

calories = [sum(map(int, datum)) for datum in data]

calories = sorted(calories)

print(calories[-1])

print(calories[-1] + calories[-2] + calories[-3])

clock.toc()
