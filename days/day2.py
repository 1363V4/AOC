from utils import Clock, read_data
from pprint import pprint

clock = Clock()

clock.tic()

data = read_data()

game = {
    "Rock": {
        "Rock": "Draw",
        "Paper": "Loss",
        "Scissors": "Win",
    },
    "Paper": {
        "Rock": "Win",
        "Paper": "Draw",
        "Scissors": "Loss",
    },
    "Scissors": {
        "Rock": "Loss",
        "Paper": "Win",
        "Scissors": "Draw",
    },
}

# other version with R,P,S = 0,1,2 and [D,L,W][(P1+P2)%3]

elves = {
    "A": "Rock",
    "B": "Paper",
    "C": "Scissors",
}

shape_score = {
    "Rock": 1,
    "Paper": 2,
    "Scissors": 3,
}

round_score = {
    "Loss": 0,
    "Draw": 3,
    "Win": 6,
}

silver = {
    "X": "Rock",
    "Y": "Paper",
    "Z": "Scissors",
}
score = 0
for hand in data:
    p1, p2 = hand.split()
    p1 = elves[p1]
    p2 = silver[p2]
    score += shape_score[p2]
    outcome = game[p2][p1]
    score += round_score[outcome]
    
print("Silver", score)

clock.toc("Silver")
clock.tic()

gold = {
    "X": "Loss",
    "Y": "Draw",
    "Z": "Win",
}

score = 0
for hand in data:
    p1, p2 = hand.split()
    p1 = elves[p1]
    outcome = gold[p2]
    score += round_score[outcome]
    p2 = [move for move in game if game[move][p1] == outcome][0]
    score += shape_score[p2]
    
print("Gold", score)

clock.toc("Gold")

# could be faster with a new game dict
