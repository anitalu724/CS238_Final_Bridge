import random
from .card import Card


def checking(players) -> bool:
    for player in players:
        if player.point < 4:
            return False
    return True

def dealing(players, verbosity = 1) -> bool:
    deck = [i for i in range(52)]
    random.shuffle(deck)
    each_hand = [deck[i*13:(i+1)*13] for i in range(4)]
    
    for idx, player in enumerate(players):
        player.point = 0
        for card in each_hand[idx]:
            player.append_card(Card(card))
        if verbosity >= 3:
            print(player)

    return checking(players)
    
    

    
    