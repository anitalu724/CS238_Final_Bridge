from src.card import Card
from src.util import dealing
from src.player import Player

players = [Player(i) for i in range(4)]

dealing(players)