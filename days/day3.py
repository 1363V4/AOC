from utils import Clock, read_data
from pprint import pprint
import string

clock = Clock()

clock.tic()

data = read_data()

letters = {letter: ord(letter)-96 for letter in string.ascii_lowercase}
letters.update({letter: ord(letter)-38 for letter in string.ascii_uppercase})

silver = 0
for datum in data:
    midsize = int(len(datum)/2)
    left, right = datum[:midsize], datum[midsize:]
    left, right = map(set, [left, right])
    common_letter = left.intersection(right).pop()
    silver += letters[common_letter]

clock.toc(f"Silver {silver}")
clock.tic()

groups = [data[i:i+3] for i in range(0, len(data), 3)]

gold = 0
for group in groups:
    common_letter = set(letters.keys())
    for bag in group:
        common_letter = common_letter.intersection(set(bag))
    common_letter = common_letter.pop()
    gold += letters[common_letter]

clock.toc(f"Gold: {gold}")
