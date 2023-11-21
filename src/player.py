from .card import Card
from .util import decide_winner
import random

class Player:
    def __init__(self, name: int) -> None:
        self.name = name
        self.hand = []
        self.point = 0

    # def __str__(self) -> str:
    #     result = "Player " + str(self.name) + ": "
    #     diamonds = sum(1 for card in self.hand if card.suit == 1)
    #     clubs = sum(1 for card in self.hand if card.suit == 0)
    #     result += ("Diamonds: " + str(diamonds)+ ", ")
    #     result += ("Clubs: " + str(clubs))
    #     result += (" -> Points: " + str(self.point))
    #     return result
    
    def __str__(self) -> str:
        result = "Player " + str(self.name) + ": "
        for card in self.hand:
            space = 3
            if card.suit == 0:
                space += 3

            result += str(card) + " " * space
        return result

    def __rep__(self):
        print(f"{self.name}'s hands:\n")
        for hand in self.hand:
            print(hand)
    
    def append_card(self, card: Card):
        self.hand.append(card)
        if card.rank >= 9:
            self.point += (card.rank - 8)
    
    def remove_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
        else:
            print(f"{self.name}'s hand does not contain {card}")
    
    def play(self, trump_suit: int):

        if trump_suit is None:
            card = random.choice(self.hand)
            self.remove_card(card)
            return card

        else:
            trump_suit_card = [card for card in self.hand if card.suit == trump_suit]

            if len(trump_suit_card) != 0:
                card = random.choice(trump_suit_card)
                self.remove_card(card)
                return card

            else:
                card = random.choice(self.hand)
                self.remove_card(card)
                return card
    
    def play_expert(self, prev_card, deck_card):
        if len(self.hand) == 1:
            card = self.hand[0]
            self.remove_card(card)
            return card
        
        all_card = prev_card + deck_card + [card.value for card in self.hand]
        suit_0 = len([i for i in all_card if i // 6 == 0])
        suit_1 = len(all_card) - suit_0
        possible_suit = 0
        if suit_0 > suit_1:
            possible_suit = 1

        possible_suit_card = [card for card in self.hand if card.suit == possible_suit]
        not_possible_suit_card = [card for card in self.hand if card.suit != possible_suit]

        cur_win = decide_winner(deck_card)
        consider_card = None
        if cur_win == 1:
            if len(not_possible_suit_card) != 0:
                consider_card = not_possible_suit_card
            
            else:
                consider_card = possible_suit_card

        else:
            win_card = []
            lose_card = []
            for card in self.hand:
                deck_card.append(card.value)
                winner = decide_winner(deck_card)
                deck_card.pop()
                if winner == 3:
                    win_card.append(card)
                else:
                    lose_card.append(card)

            if len(win_card) != 0:
                consider_card = win_card
            
            else:
                consider_card = lose_card
            
        min_value = 100
        for card in consider_card:
            if card.value < min_value:
                min_value = card.value
                card_to_play = card

        self.remove_card(card_to_play)
        return card_to_play

    def play_policy(self, state_index, Q, trump_suit: int):
        policy = Q[state_index]
        max_q = -1
        card_to_play = None
        for possible_card in self.hand:

            if possible_card.suit == trump_suit:
                same_suit = 1
            else:
                same_suit = 0

            if policy[possible_card.value] + same_suit * 10000000000 > max_q:
                card_to_play = possible_card
                max_q = policy[possible_card.value] + same_suit * 10000000000
        
        self.remove_card(card_to_play)
        return card_to_play



            