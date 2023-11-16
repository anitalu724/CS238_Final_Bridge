from .card import Card
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
    
    def play_expert(self, deck_card):
        pass

    def play_policy(self, state_index, Q):
        policy = Q[state_index]
        max_q = -1
        card_to_play = None
        for possible_card in self.hand:
            if policy[possible_card.value] > max_q:
                card_to_play = possible_card
                max_q = policy[possible_card.value]
        
        self.remove_card(card_to_play)
        return card_to_play



            