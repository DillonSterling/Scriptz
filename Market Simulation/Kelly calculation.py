# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 17:10:43 2021

@author: SESA553573
"""
import numpy as np
import random as random
import pandas as pd
from matplotlib import pyplot as plt

#Probobility of winning expressed in a ratio 0-1
prob_of_winning = np.linspace(0,1,11)
#bet size expressed in a ration of total capital
bet_size = np.linspace(0,1,101)
#Total capital in dollars
capital = 1000000
#How many times the bet is made
loops = 100
results = []

for given_prob_of_winning in range(len(prob_of_winning)):
    given_prob_of_winning_results = []
    
    for given_bet_size in range(len(bet_size)):
        
        loop_count = 0
        given_bet_size_results = [capital]
        
        while (loop_count < loops):
            #Win the bet
            
            if (random.random() < prob_of_winning[given_prob_of_winning]):
                given_bet_size_results.append(given_bet_size_results[len(given_bet_size_results)-1] * (1 + bet_size[given_bet_size]))
                #Lose the bet
            else :
                given_bet_size_results.append(given_bet_size_results[len(given_bet_size_results)-1] * (1 - bet_size[given_bet_size]))
            loop_count = loop_count + 1
        given_prob_of_winning_results.append(given_bet_size_results)
    results.append(given_prob_of_winning_results)
    
for given_prob_of_winning in range(len(prob_of_winning)):
    plt.title(str(given_prob_of_winning * 10) + "% Data") 
    plt.xlabel("Bet Number") 
    plt.ylabel("capital") 
    plt.plot(results[given_prob_of_winning]) 
    plt.show()