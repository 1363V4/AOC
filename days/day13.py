from utils import Clock, read_data
from pprint import pprint
import builtins
from copy import deepcopy
from itertools import permutations
from collections import defaultdict


clock = Clock()
clock.tic()

data = read_data()
data = [[*map(eval, [data[i], data[i+1]])] for i in range(0, len(data)-1, 3)]
backup = deepcopy(data)
gold_data = []
for datum in backup:
    gold_data += [*datum]


def compare(left, right):
    if left == right:
        return None
    match left, right:
        case [], _:
            return True
        case _, []:
            return False
        case _:
            pass

    left_elem = left.pop(0)
    right_elem = right.pop(0)

    match type(left_elem), type(right_elem):
        case builtins.int, builtins.int:
            if left_elem > right_elem:
                return False
            if left_elem < right_elem:
                return True
            return compare(left, right)
        case builtins.int, builtins.list:
            left_elem = [left_elem]
        case builtins.list, builtins.int:
            right_elem = [right_elem]
        case _:
            pass

    about_the_lists = compare(left_elem, right_elem)
    if about_the_lists is None:
        return compare(left, right)
    elif about_the_lists is True:
        return True
    elif about_the_lists is False:
        return False


good_pairs = {}
for n, pair in enumerate(data):
    _pair = str(pair)
    left, right = pair
    if compare(left, right):
        good_pairs[n+1] = eval(_pair)

silver = sum(good_pairs)
clock.toc(f"Silver {silver}")
clock.tic()

gold_data += [[[2]]]
gold_data += [[[6]]]
matchups = permutations(gold_data, 2)
scores = defaultdict(int)
for one, two in matchups:
    one_copy = deepcopy(one)
    two_copy = deepcopy(two)
    if compare(one_copy, two_copy):
        scores[str(one)] += 1
    else:
        scores[str(two)] += 1

gold = 1
scores = {v: k for k, v in scores.items()}
for n, k in enumerate(reversed(sorted(scores))):
    if scores[k] == "[[2]]" or scores[k] == "[[6]]":
        gold *= (n+1)

clock.toc(f"Gold {gold}")
