from enum import Enum


class Suit(Enum):
    CLUBS = 0
    DIAMONDS = 1

Rank = {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: "J", 10: "Q", 11: "K", 12: "A"}
    
class Card:
    def __init__(self, value) -> None:
        """
        Diamonds 6-11 	(i/6 == 1)
        Clubs 0-5 		(i/6 == 0) (Clubs 2 = 0, Clubs A = 12)
        """
        if value > 11:
            raise Exception("Value should be in the range of [0, 51]")
        self.value = value
        self.suit = int(value / 6)
        self.rank = value % 6

    def __str__(self) -> str:
        return f"{Rank[self.rank]} of {Suit(self.suit).name}"


