from enum import Enum


class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

Rank = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: "J", 10: "Q", 11: "K", 12: "A"}
    
class Card:
    def __init__(self, value) -> None:
        """
        Spades 39-51   	(i/13 == 3) (Spades 2 = 39, Spades A = 51)
        Hearts 26- 38 	(i/13 == 2)
        Diamonds 13-25 	(i/13 == 1)
        Clubs 0-12 		(i/13 == 0)
        """
        if value > 51:
            raise Exception("Value should be in the range of [0, 51]")
        self.value = value
        self.suit = int(value/13)
        self.rank = value%13
    def __str__(self) -> str:
        return f"{Rank[self.rank]} of {Suit(self.suit).name}"


