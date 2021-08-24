# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:10:43 2021

@author: SESA553573
"""
import numpy as np
import random as random
from matplotlib import pyplot as plt

#Probobility of winning expressed in a ratio 0-1
prob_of_winning = np.linspace(.60,.60,1)
#bet size expressed in a ration of total capital
bet_size = np.linspace(0,1,101)
#Total capital in dollars
capital = 100
#How many times the bet is made
bets = 100
#How many time each bet is repeated to generate an average
num_bets_to_average = 100000

results = np.array(np.zeros((len(prob_of_winning), len(bet_size), bets)))
#results[:,:,0] = capital

for given_prob_of_winning in range(len(prob_of_winning)):
    for given_bet_size in range(len(bet_size)):
        bets_to_average = np.array(np.zeros((num_bets_to_average, bets)))
        bets_to_average[:,0] = capital
        for avg_bet in range(num_bets_to_average):
            for bet in range(1, bets): 
                
                if (bets_to_average[avg_bet, bet-1] > capital*1000000000
                or bets_to_average[avg_bet, bet-1] < capital/1000000000):
                    bets_to_average[avg_bet, bet] = bets_to_average[avg_bet, bet-1]
                else:
                    #Win the bet
                    if (random.random() < prob_of_winning[given_prob_of_winning]):
                        bets_to_average[avg_bet, bet] = bets_to_average[avg_bet, bet-1] * (1 + bet_size[given_bet_size])
                    #Lose the bet
                    else :
                        bets_to_average[avg_bet, bet] = bets_to_average[avg_bet, bet-1] * (1 - bet_size[given_bet_size])
        
        results[given_prob_of_winning, given_bet_size,:] = np.median(bets_to_average, axis=0)

    plt.title(str(prob_of_winning[given_prob_of_winning] * 100) + "% Data") 
    plt.xlabel("Bet #") 
    plt.ylabel("capital") 
    plt.plot(results[given_prob_of_winning,:,bets-1].T) 
    plt.show()
    
    plt.title(str(prob_of_winning[given_prob_of_winning] * 100) + "% Data") 
    plt.xlabel("% Bet size") 
    plt.ylabel("capital") 
    plt.plot(results[given_prob_of_winning,:,bets-1]) 
    plt.show()