import argparse
from pathlib import Path
from src.card import Card
from src.util import dealing
from src.player import Player

VERBOSITY = 1

def main():
    parser = argparse.ArgumentParser(description="Bridge Game")
    parser.add_argument("-v", "--verbose", action="store", type=int)
    parser.add_argument("-i", "--init", action="store_true")
    parser.add_argument("-d", "--dealing", action="store_true")
    parser.add_argument("-r", "--redealing", action="store_true")
    arg = parser.parse_args()

    if arg.verbose:
        VERBOSITY = arg.verbose
    if arg.init:
        players = [Player(i) for i in range(4)]
        print("Start a 4-player bridge game")
    if arg.dealing:
        print("Start dealing...")
        if arg.redealing:
            allow = False
            while not allow:
                allow = dealing(players, VERBOSITY)
                if not allow:
                    print("\nRedealing...")
        else:
            dealing(players, VERBOSITY)
        print("Finish dealing.")

    

if __name__ == "__main__":
    main()
    

    
