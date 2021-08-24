# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 14:22:58 2021

@author: SESA553573
"""
import random
import pandas as pd
#import numpy as np

vol = 5
num_Participants = 2000
participants = []
price = [50]
ema_List = []
d1_price = [0]
d2_price = [0]

buy_Orders = []
sell_Orders = []
closed_Buy_Orders = []
closed_Sell_Orders = []

bid_Que = []
ask_Que = []

max_Bid_Amount = 0
max_Bid = 0
min_Ask_Amount = 0
min_Ask = 0

def print_Order(order):
    print("Person # " + str(order.person_Number) + " , " + str(order.buy_Sell)\
          + " " + str(order.order_Type) + " Order , $" + str(round(order.amount,2))\
          + ": " + str(order.order_Status)) 
    #print(order.__dict__)
    
def ema(values, alpha):
    df = pd.DataFrame({'Price': values})
    rolling_exp_avg = df.ewm(alpha=alpha).mean()['Price']
    df['Avg'] = rolling_exp_avg
    averages = df['Avg'].tolist()
    return averages[len(averages)-1]


class moving_Average():
    def update(self, price):
        self.Ema_5 = ema(price[len(price)-5:len(price)], 0.5)
        self.Ema_10 = ema(price[len(price)-10:len(price)], 0.5)
        self.Ema_20 = ema(price[len(price)-20:len(price)], 0.5)
        self.Ema_50 = ema(price[len(price)-50:len(price)], 0.5)
        self.Ema_100 = ema(price[len(price)-100:len(price)], 0.5)
        self.Ema_200 = ema(price[len(price)-200:len(price)], 0.5)


    
class Participant(): #defines the properties of the market participants
    def __init__(self, number):
        self.bullishness = random.random()
        self.perceived_Value = random.gauss(50, vol)
        self.number = number
        
    def update(self, price, d1_price, d2_price):
        self.bullishness = min(max(self.bullishness + d1_price[len(d1_price)-1] + (self.perceived_Value - price[len(price)-1])/vol,0),1)
        self.perceived_Value =  self.perceived_Value + 0 * d1_price[len(d1_price)-1] + 0 * d2_price[len(d2_price)-1] + .2 * (d1_price[len(d1_price)-1] * d2_price[len(d2_price)-1])

        
class order():

    def start(self, person, price): #determinies how each participant responds to market conditions
        self.person_Number = person.number
        
        if person.perceived_Value > price:
            if random.random() < person.bullishness:
                self.buy_Sell = "buy"
                self.order_Type = "market"
                self.amount = price
                self.order_Status = "open"
            else:
                self.buy_Sell = "buy"
                self.order_Type = "limit"
                self.amount = price - (1 - person.bullishness) * vol
                self.order_Status = "open"
        elif person.perceived_Value <= price:
            if random.random() > person.bullishness:
                self.buy_Sell = "sell"
                self.order_Type = "market"
                self.amount = price
                self.order_Status = "open"
            else:
                self.buy_Sell = "sell"
                self.order_Type = "limit"
                self.amount = price + (1 - person.bullishness) * vol
                self.order_Status = "open"
                
    def update(self, person, price):
        if person.perceived_Value > price:
            if random.random() < person.bullishness:
                self.buy_Sell = "buy"
                self.order_Type = "market"
                self.amount = price
                self.order_Status = "open"
            else:
                pass
                # self.buy_Sell = "buy"
                # self.order_Type = "limit"
                # self.amount = price - (1 - person.bullishness) * vol
                # self.order_Status = "open"
        elif person.perceived_Value <= price:
            if random.random() > person.bullishness:
                self.buy_Sell = "sell"
                self.order_Type = "market"
                self.amount = price
                self.order_Status = "open"
            else:
                pass
                # self.buy_Sell = "sell"
                # self.order_Type = "limit"
                # self.amount = price + (1 - person.bullishness) * vol
                # self.order_Status = "open"

def close_Orders():
    global max_Bid
    global max_Bid_Amount
    global min_Ask
    global min_Ask_Amount
    global buy_Orders
    global sell_Orders
    
    for ii in range(len(buy_Orders)):
        if buy_Orders[ii].amount == max_Bid_Amount:
            if buy_Orders[ii].order_Status == "open":
                buy_Orders[ii].order_Status = "closed"
                print_Order(buy_Orders[ii])
                closed_Buy_Orders.append(buy_Orders[ii])
                buy_Orders.pop(ii)
                break

    for jj in range(len(sell_Orders)):
        if sell_Orders[jj].amount == min_Ask_Amount:
            if sell_Orders[jj].order_Status == "open":
                sell_Orders[jj].order_Status = "closed"
                print_Order(sell_Orders[jj])
                closed_Sell_Orders.append(sell_Orders[jj])
                sell_Orders.pop(jj)
                break

    fill_Orders()

def next_Tick():
    global price
    global d1_price
    global d2_price
    global ema_List
    
    temp_d1_price = price[len(price)-1] - price[len(price)-2]
    d1_price.append(temp_d1_price)
    
    temp_d2_price = d1_price[len(price)-1] - d1_price[len(price)-2]
    d2_price.append(temp_d2_price)
    
    next_Average = moving_Average()
    next_Average.update(price)
    ema_List.append(next_Average)
    
    for person in range(len(participants)):
        participants[person].update(price, d1_price, d2_price)
        for b_order in range(len(buy_Orders)):
            if buy_Orders[b_order].person_Number == participants[person].number:
                buy_Orders[b_order].update(participants[person], price[len(price)-1])
        for s_order in range(len(sell_Orders)):
            if sell_Orders[s_order].person_Number == participants[person].number:
                sell_Orders[s_order].update(participants[person], price[len(price)-1])       
    fill_Orders()
    
def fill_Orders():
    global bid_Que
    global ask_Que
    global max_Bid_Amount 
    global max_Bid
    global min_Ask_Amount
    global min_Ask
    global buy_Orders
    global sell_Orders
    global price
    
    bid_Que = []
    ask_Que = []
    
    for bids in range(len(buy_Orders)):
        if(buy_Orders[bids].order_Status == "open"):
            bid_Que.append(buy_Orders[bids].amount)
    for asks in range(len(sell_Orders)):
        if(sell_Orders[asks].order_Status == "open"):
            ask_Que.append(sell_Orders[asks].amount)
            
    if bid_Que != []:
        max_Bid_Amount = max(bid_Que)
        max_Bid = bid_Que.index(max_Bid_Amount)
    else:
        max_Bid_Amount = None
        max_Bid = None
        
    if ask_Que != []:
        min_Ask_Amount = min(ask_Que)
        min_Ask = ask_Que.index(min_Ask_Amount)
    else:
        min_Ask_Amount = None
        min_Ask = None  
        
    if (max_Bid_Amount == None):
        if (min_Ask_Amount == None):
            price.append(min_Ask_Amount)
            return
    elif (min_Ask_Amount == None):
        price.append(max_Bid_Amount)     
        return
    elif ((bid_Que != []) & (ask_Que != []) & (max_Bid_Amount >= min_Ask_Amount)):
        close_Orders()
    else:
        temp_Price = (max_Bid_Amount + min_Ask_Amount)/2
        price.append(temp_Price)     
        next_Tick()

        
for person in range(num_Participants): #establishes a list of market participants
    trader = Participant(person)
    participants.append(trader)
    trade = order()
    trade.start(participants[person], price[0])
    # print(person, trade.buy_Sell, trade.order_Type, trade.amount)
    if trade.buy_Sell == "buy":
        buy_Orders.append(trade)
    if trade.buy_Sell == "sell":
        sell_Orders.append(trade)

fill_Orders()






