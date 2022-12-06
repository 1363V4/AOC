from utils import Clock, read_data
from pprint import pprint

clock = Clock()

clock.tic()

data = read_data()[0]

silver = 0
window = data[silver:silver+4]
while len(set(window)) != 4:
    silver += 1
    window = data[silver:silver+4]

clock.toc(f"Silver {silver+4}")
clock.tic()

gold = 0
window = data[gold:gold+14]
while len(set(window)) != 14:
    gold += 1
    window = data[gold:gold+14]

clock.toc(f"Gold {gold+14}")
