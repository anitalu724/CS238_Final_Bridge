import random
from .card import Card

def dealing(players):
    deck = [i for i in range(52)]
    random.shuffle(deck)
    each_hand = [deck[i*13:(i+1)*13] for i in range(4)]
    
    for idx, player in enumerate(players):
        for card in each_hand[idx]:
            player.append_card(Card(card))
        print(player)
    

    
    