import csv
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt

from tqdm import trange
from pathlib import Path
from src.card import Card
from os.path import exists
from src.genIdx import gen_idx
from src.player import Player
from src.util import dealing, find_state_index, decide_winner

VERBOSITY = 1

if not exists("json/state1_index.json") or not exists("json/state2_index.json") or not exists("json/state3_index.json"):
    gen_idx()

state_idx_dict_list = []
for i in range(1, 4):
    with open("json/state"+str(i)+"_index.json", "r") as f:
        state_idx_dict_list.append(json.loads(f.read()))

def main():
    parser = argparse.ArgumentParser(description="Bridge Game")
    parser.add_argument("-v", "--verbose", action="store", type=int)
    parser.add_argument("-i", "--init", action="store_true")
    parser.add_argument("-d", "--dealing", action="store_true")
    parser.add_argument("-r", "--redealing", action="store_true")
    parser.add_argument("-n", "--num_trials", type=int, default=30000)
    parser.add_argument("-a", "--alpha", type=float, default=0.8)
    parser.add_argument("-g", "--gamma", type=float, default=0.95)
    parser.add_argument("-s", "--save_interval", type=int, default=1000)
    arg = parser.parse_args()

    if arg.verbose:
        VERBOSITY = arg.verbose

    if arg.init:
        players = [Player(i) for i in range(4)]
        print("Start a 4-player bridge game")

    # if arg.dealing:
    #     print("Start dealing...")

    #     if arg.redealing:
    #         allow = False
    #         while not allow:
    #             allow = dealing(players, VERBOSITY)
    #             if not allow:
    #                 print("\nRedealing...")
    #     else:
    #         dealing(players, VERBOSITY)

    #     print("Finish dealing.")
    
    trials = arg.num_trials
    # alpha = arg.alpha
    # gamma = arg.gamma
    # save = arg.save_interval
    # deck_card = []
    # prev_card = []
    # hand_card = []
    # enemy1_card = None
    # enemy2_card = None
    # teammate_card = None
    # win = 0
    # r = 0

    collect_data = []

    # Q = np.zeros((3472921, 12))
    Q = np.load("./Q_trained_noshaping.npy")

    num_win = 0
    result = []
    for trial in trange(trials):

        dealing(players, VERBOSITY)
        deck_card = []
        prev_card = []
        hand_card = []
        enemy1_card = None
        enemy2_card = None
        teammate_card = None
        win = 0
        r = 0

        for round in range(3):
            for i, player in enumerate(players):

                if i == 0:
                    card = player.play(None)
                    trump_suit = card.suit
                    deck_card.append(card.value)
                    enemy1_card = card.value
                    # print("Player 1 plays " + str(card))
                
                if i == 1:
                    card = player.play(trump_suit)
                    deck_card.append(card.value)
                    teammate_card = card.value
                    # print("Player 2 plays " + str(card))

                if i == 2:
                    card = player.play(trump_suit)
                    deck_card.append(card.value)
                    enemy2_card = card.value
                    # print("Player 3 plays " + str(card))
                
                if i == 3:
                    hand_card = [card.value for card in player.hand]
                    state_tuple = find_state_index(prev_card, enemy1_card, teammate_card, enemy2_card, hand_card, win)

                    if round == 0:
                        state_index = state_index_dict1[str(state_tuple)]
                    elif round == 1:
                        state_index = state_index_dict2[str(state_tuple)] + 110880
                    elif round == 2:
                        state_index = state_index_dict3[str(state_tuple)] + 110880 + 3326400

                    # card = player.play(None)
                    # card = player.play(trump_suit)
                    card = player.play_policy(state_index, Q, trump_suit)
                    # print("Player 4 plays " + str(card))
                    action_index = card.value
                    deck_card.append(card.value)

                    winner = decide_winner(deck_card)
                        
                    
                    if winner == 1 or winner == 3:
                        win += 1
                        
                    if round != 0:
                        state = last_state_index
                        action = last_action_index
                        next_state = state_index
                        # reward = last_r

                        # collect_data.append((state, action, reward, next_state))
                        # Q[state, action] += alpha * (reward + (gamma * np.max(Q[next_state])) - Q[state, action])

                        last_state_index = state_index
                        last_action_index = action_index
                        # last_r = r

                    prev_card += deck_card
                    deck_card = []
                    last_state_index = state_index
                    last_action_index = action_index
                    # last_r = r
        
        state = last_state_index
        action = last_action_index
        next_state = 3472920
        # reward = last_r

        # collect_data.append((state, action, reward, next_state))
        # Q[state, action] += alpha * (reward + (gamma * np.max(Q[next_state])) - Q[state, action])

        if win >= 2:
            num_win += 1

        # if trial % save == save - 1:
            # np.save('Q_' + str(trial+1) + '.npy', Q)
    print(f'win rate: ', (num_win / (trials)))
            # num_win = 0

    # print("s, a, r, sp: " + str(collect_data))
    # plt.plot(result)
    # plt.show()
            

if __name__ == "__main__":
    main()
    

    
