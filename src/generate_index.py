import itertools
import json

possible = [i for i in range(12)]
state1 = []
for hand in itertools.combinations(possible, 3):
    hand = list(hand)
    unused = [i for i in range(12) if i not in hand]

    for deck in itertools.permutations(unused, 3):
        total = hand + list(deck)
        state1.append(tuple(total))

possible = [i for i in range(12)]
state2 = []
for prev in itertools.combinations(possible, 4):
    prev = list(prev)
    unused = [i for i in range(12) if i not in prev]

    for hand in itertools.combinations(unused, 2):
        prev_and_hand = prev + list(hand)
        unused = [i for i in range(12) if i not in prev_and_hand]
    
        for deck in itertools.permutations(unused, 3):
            prev_and_hand_and_deck = prev_and_hand + list(deck)

            for win in range(2):
                total = prev_and_hand_and_deck + [win]
                state2.append(tuple(total))

possible = [i for i in range(12)]
state3 = []
for prev in itertools.combinations(possible, 8):
    prev = list(prev)
    unused = [i for i in range(12) if i not in prev]

    for hand in itertools.combinations(unused, 1):
        prev_and_hand = prev + list(hand)
        unused = [i for i in range(12) if i not in prev_and_hand]
    
        for deck in itertools.permutations(unused, 3):
            prev_and_hand_and_deck = prev_and_hand + list(deck)

            for win in range(3):
                total = prev_and_hand_and_deck + [win]
                state3.append(tuple(total))
        
print(len(state1))
print(len(state2))
print(len(state3))

dct = {}
for i, state in enumerate(state1):
    dct[str(state)] = i

with open("state1_index.json", "w") as f:
    f.write(json.dumps(dct, indent=4))

dct = {}
for i, state in enumerate(state2):
    dct[str(state)] = i

with open("state2_index.json", "w") as f:
    f.write(json.dumps(dct, indent=4))

dct = {}
for i, state in enumerate(state3):
    dct[str(state)] = i

with open("state3_index.json", "w") as f:
    f.write(json.dumps(dct, indent=4))
