from .card import Card

class Player:
    def __init__(self, name: int) -> None:
        self.name = name
        self.hand = []
    def __str__(self) -> str:
        result = "Player " + str(self.name) + ": "
        spades = sum(1 for card in self.hand if card.suit == 3)
        hearts = sum(1 for card in self.hand if card.suit == 2)
        diamonds = sum(1 for card in self.hand if card.suit == 1)
        clubs = sum(1 for card in self.hand if card.suit == 0)
        result += ("Spades: " + str(spades) + ", ")
        result += ("Hearts: " + str(hearts) + ", ")
        result += ("Diamonds: " + str(diamonds)+ ", ")
        result += ("Clubs: " + str(clubs))
        return result

    def __rep__(self):
        print(f"{self.name}'s hands:\n")
        for hand in self.hand:
            print(hand)
    
    def append_card(self, card: Card):
        self.hand.append(card)
    
    def remove_card(self, card: Card):
        if card in self.hand:
            self.hand.remove(card)
        else:
            print(f"{self.name}'s hand does not contain {card}")

            