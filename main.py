import csv
import copy
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt

from tqdm import trange
from pathlib import Path
from src.card import Card
from numpy import genfromtxt
from src.player import Player
from numpy import linalg as la
from src.genIdx import check_json
from src.util import dealing, find_state_index, decide_winner

def main():
    parser = argparse.ArgumentParser(description="Bridge Game")
    parser.add_argument("-v", "--verbose", action="store", type=int)
    parser.add_argument("-d", "--dealing", action="store_true")
    parser.add_argument("-r", "--redealing", action="store_true")
    parser.add_argument("-n", "--num_trials", type=int, default=4000000)
    parser.add_argument("-a", "--alpha", type=float, default = 0.8)
    parser.add_argument("-g", "--gamma", type=float, default = 0.95)
    parser.add_argument("-s", "--save_interval", type=int, default=40000)
    parser.add_argument("-sim", "--simulation", action="store_true")
    parser.add_argument("-st", "--strategy", type=int)    ## 0: None, 1: trump_suit, 2: expert
    parser.add_argument("-sh", "--shaping", action="store_true")
    parser.add_argument("-play", "--play", type = int)    ## 0: shaping, 1: non-shaping
    parser.add_argument("-t", "--train", action="store_true")
    arg = parser.parse_args()

    if arg.verbose:
        VERBOSITY = arg.verbose
    else:
        VERBOSITY = 1

    ## Initial 4 players
    players = [Player(i) for i in range(4)]
    if VERBOSITY > 1: print("Start a 4-player bridge game")

    ## Check and generate json files
    check_json()
    state_idx_dict_list = []
    for i in range(1, 4):
        with open("json/state"+str(i)+"_index.json", "r") as f:
            state_idx_dict_list.append(json.loads(f.read()))

    ## Set parameters
    
    trials = arg.num_trials
    alpha = arg.alpha
    gamma = arg.gamma
    save = arg.save_interval
    
    if arg.simulation or arg.play:
        collect_data = []
        if arg.simulation:
            Q = np.zeros((3472921, 12))
        elif arg.play:
            if arg.play == 0:
                try:
                    Q = np.load("./Q_trained_nonshaping.npy")
                except ValueError:
                    raise("File \"Q_trained_nonshaping.npy\" is missing! Do training first!")
            elif arg.play == 1:
                try:
                    Q = np.load("./Q_trained_shaping.npy")
                except ValueError:
                    raise("File \"Q_trained_shaping.npy\" is missing! Do training first!")
            else:
                raise("Parameter missing")

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
                        if arg.strategy == 0:
                            card = player.play(None)
                        elif arg.strategy == 1 or arg.strategy == 2 or arg.play:
                            card = player.play(trump_suit)
                        else:
                            raise("arg.strategy has wrong parameter.")
                        deck_card.append(card.value)
                        teammate_card = card.value
                        # print("Player 2 plays " + str(card))

                    if i == 2:
                        if arg.strategy == 0:
                            card = player.play(None)
                        elif arg.strategy == 1 or arg.strategy == 2 or arg.play:
                            card = player.play(trump_suit)
                        else:
                            raise("arg.strategy has wrong parameter.")
                        deck_card.append(card.value)
                        enemy2_card = card.value
                        # print("Player 3 plays " + str(card))

                    if i == 3:
                        hand_card = [card.value for card in player.hand]
                        state_tuple = find_state_index(prev_card, enemy1_card, teammate_card, enemy2_card, hand_card, win)

                        if round == 0:
                            state_index = state_idx_dict_list[0][str(state_tuple)]
                        elif round == 1:
                            state_index = state_idx_dict_list[1][str(state_tuple)] + 110880
                        elif round == 2:
                            state_index = state_idx_dict_list[2][str(state_tuple)] + 110880 + 3326400
                        
                        if arg.play:
                            card = player.play_policy(state_index, Q, trump_suit)
                        elif arg.simulation:
                            if arg.strategy == 0:
                                card = player.play(None)
                            elif arg.strategy == 1:
                                card = player.play(trump_suit)
                            elif arg.strategy == 2:
                                card = player.play_expert(prev_card, deck_card)
                            else:
                                raise("arg.strategy has wrong parameter.")
                        
                        # print("Player 4 plays " + str(card))
                        action_index = card.value
                        deck_card.append(card.value)

                        winner = decide_winner(deck_card)
                        # print("Winner: Player" + str(winner+1))

                        ## Shaping or non-shaping
                        if arg.shaping and arg.simulation:
                            if round == 0:
                                if winner == 1 or winner == 3:
                                    r = 0.5
                                    win += 1
                                else:
                                    r = 0
                            elif round == 1:
                                if winner == 1 or winner == 3:
                                    r = 0.5 + 0.5 * win
                                    win += 1
                                else:
                                    r = 0 
                            # giving a reward even for winning three rounds
                            elif round == 2:
                                if (winner == 1 and win >= 1) or (winner == 3 and win >= 1):
                                    r = 1
                                    win += 1
                                else:
                                    r = 0
                        elif not arg.shaping and arg.simulation:
                            if winner == 1 or winner == 3:
                                win += 1
                            if win >= 2:
                                r = 1
                            else:
                                r = 0
                        elif arg.play:
                            if winner == 1 or winner == 3:
                                win += 1


                        if round != 0:
                            state = last_state_index
                            action = last_action_index
                            next_state = state_index
                            if arg.simulation: 
                                reward = last_r
                                collect_data.append((state, action, reward, next_state))
                                Q[state, action] += alpha * (reward + (gamma * np.max(Q[next_state])) - Q[state, action])
                                last_r = r
                            last_state_index = state_index
                            last_action_index = action_index
                            

                        prev_card += deck_card
                        deck_card = []
                        last_state_index = state_index
                        last_action_index = action_index
                        if arg.simulation: 
                            last_r = r

            state = last_state_index
            action = last_action_index
            next_state = 3472920
            if arg.simulation: 
                reward = last_r
                collect_data.append((state, action, reward, next_state))
                Q[state, action] += alpha * (reward + (gamma * np.max(Q[next_state])) - Q[state, action])

            if win >= 2:
                num_win += 1
            
            if arg.play:
                print("Winning rate: ", float(num_win / (trials)))
            if arg.simulation:
                if trial % save == save - 1:
                    # np.save('Q_' + str(trial+1) + '.npy', Q)
                    result.append(num_win / save)
                    num_win = 0
    
    if arg.simulation:
        # print("s, a, r, sp: " + str(collect_data))
        print("Winning rate: ", sum(result)/len(result))
        plt.plot(result)
        plt.ylim((0.25, 0.6))
        ## Plot (x: time, y: range(0.25-0.6)) save fig
        if arg.strategy == 0:
            file_name = "none.1" if arg.shaping else "none.0"
        elif arg.strategy == 1:
            file_name = "trump_suit.1" if arg.shaping else "trump_suit.0"
        elif arg.strategy == 2:
            file_name = "expert.1" if arg.shaping else "expert.0"

        with open("csv/data_only2win."+file_name+".csv", "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerows(collect_data)
        np.save('npy/Q_' + str(trials)  + "." + file_name + ".npy", Q)
        with open("json/"+file_name+".json", "w") as f:
            f.write(json.dumps(result, indent=4))
            plt.savefig("fig/"+file_name+".pdf")

        # if arg.strategy == 0:
        #     with open("csv/data_only2win.none.csv", "w", newline="") as file:
        #         writer = csv.writer(file)
        #         writer.writerows(collect_data)
        #     np.save('npy/Q_' + str(trials)  + '.none.npy', Q)
        # elif arg.strategy == 1:
        #     with open("csv/data_only2win.trump_suit.csv", "w", newline="") as file:
        #         writer = csv.writer(file)
        #         writer.writerows(collect_data)
        #     np.save('npy/Q_' + str(trials)  + '.trump_suit.npy', Q)
        # elif arg.strategy == 2:
        #     with open("csv/data_only2win.expert.csv", "w", newline="") as file:
        #         writer = csv.writer(file)
        #         writer.writerows(collect_data)
        #     np.save('npy/Q_' + str(trials)  + '.expert.npy', Q)


    
        
    
    ## Training
    if arg.train:
        epochs = 50
        Q = np.zeros((3472921, 12))
        # Q = np.load("./Q_trained.npy")
        csv_file = "./csv/data_only2win"
        csv_file += ".none" if arg.strategy == 0 else ".trump_suit" if arg.strategy == 1 else ".expert"
        # if arg.strategy == 0:
        #     csv_file += ".none"
        # elif arg.strategy == 1:
        #     csv_file += ".trump_suit"
        # elif arg.strategy == 2:
        #     csv_file += ".expert"
        csv_file += ".1.csv" if arg.shaping else ".0.csv"
        
        data = genfromtxt(csv_file, delimiter=',')
        
        state = data[:,0].astype(int)
        action = data[:,1].astype(int)
        reward = data[:,2]
        next_state = data[:,3].astype(int)

        for _ in trange(epochs):
            q = copy.copy(Q)
            for i in range(len(data)):
                s = state[i]
                a = action[i]
                r = reward[i]
                sp = next_state[i]
                Q[s, a] += alpha * (r + (gamma * np.max(Q[sp])) - Q[s, a])
            # if la.norm(Q-q) < 1e-5:
            #     break
        print(la.norm(Q-q))
        # print(np.array_equal(Q,q))
        npy_file = "npy/Q_trained_only2win"
        if arg.strategy == 0:
            npy_file += ".none.npy"
        elif arg.strategy == 1:
            npy_file += ".trump_suit.npy"
        elif arg.strategy == 2:
            npy_file += ".expert.npy"
        np.save(npy_file, Q)

if __name__ == "__main__":
    main()
    

    
