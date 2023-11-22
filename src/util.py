import random
from .card import Card

def checking(players) -> bool:
    for player in players:
        if player.point < 4:
            return False
    return True

def dealing(players, verbosity = 1) -> bool:
    deck = [i for i in range(12)]
    random.shuffle(deck)
    each_hand = [deck[i * 3 : (i + 1) *3] for i in range(4)]
    
    for idx, player in enumerate(players):
        player.point = 0
        for card in each_hand[idx]:
            player.append_card(Card(card))
        # if verbosity >= 3:
        #     print(player)

    return checking(players)

def find_state_index(prev_card, enemy1_card, teammate_card, enemy2_card, hand_card, win):

    if not prev_card:
        return tuple(sorted(hand_card) + [enemy1_card, teammate_card, enemy2_card])
    else:
        return tuple(sorted(prev_card) + sorted(hand_card) + [enemy1_card, teammate_card, enemy2_card, win])


def decide_winner(deck):
    trump_suit = deck[0] // 6

    winner = 0
    biggest_rank = -1
    for i, card in enumerate(deck):
        if card // 6 == trump_suit and card % 6 > biggest_rank:
            biggest_rank = card % 6
            winner = i
    
    return winner
    
    

    
    