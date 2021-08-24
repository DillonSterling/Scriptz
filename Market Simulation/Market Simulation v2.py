# -*- coding: utf-8 -*-
"""
Created on Sun Jul 25 14:22:58 2021

@author: SESA553573
"""
import participant as participant
import order1 as order
import random
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

price = [55]
time_Stamp = [datetime.now()]
volume = []
vol = 10
num_Participants = 500
prob_of_new_Order = .1
participants = []
ema_List = []
d1_price = [0]
d2_price = [0]
looping = 1
ema20 = [price[0]]
ema_smoothing = .2

orders = []
buy_Orders = []
sell_Orders = []
closed_Buy_Orders = []
closed_Sell_Orders = []

bid_Que = []
ask_Que = []

max_Bid_Amount = 0
min_Ask_Amount = 0

def print_Order(order):
    print("Person # " + str(order.person_Number) + " , " + str(order.buy_Sell)\
          + " " + str(order.order_Type) + " Order , $" + str(round(order.amount,2))\
          + ": " + str(order.order_Status)) 
    #print(order.__dict__)
    
def ema(values, alpha, min_periods):
    df = pd.DataFrame({'Price': values})
    rolling_exp_avg = df.ewm(alpha=alpha, adjust=False, min_periods=min_periods).mean()['Price']
    df['Avg'] = rolling_exp_avg
    averages = df['Avg'].tolist()
    return averages[len(averages)-1]

def update_Order_Lists():
    global buy_Orders
    global sell_Orders
    global orders
    
    replacement_orders = []
    buy_Orders = []
    sell_Orders = []
    
    for ord in range(len(orders)):
        if orders[ord].buy_Sell == "buy":
            if orders[ord].order_Status == "open":
                buy_Orders.append(orders[ord])
                replacement_orders.append(orders[ord])
        if orders[ord].buy_Sell == "sell":
            if orders[ord].order_Status == "open":
                sell_Orders.append(orders[ord])
                replacement_orders.append(orders[ord])
    orders = replacement_orders
    
class moving_Average():
    def update(self, price):
        self.Ema_5 = ema(price[len(price)-5:len(price)], ema_smoothing, 5)
        self.Ema_10 = ema(price[len(price)-10:len(price)], ema_smoothing, 10)
        self.Ema_20 = ema(price[len(price)-20:len(price)], ema_smoothing, 20)
        self.Ema_50 = ema(price[len(price)-50:len(price)], ema_smoothing, 50)
        self.Ema_100 = ema(price[len(price)-100:len(price)], ema_smoothing, 100)
        self.Ema_200 = ema(price[len(price)-200:len(price)], ema_smoothing, 200)

def next_Tick():
    global price
    global d1_price
    global d2_price
    global ema_List
    global looping
    
    temp_d1_price = price[len(price)-1] - price[len(price)-2]
    d1_price.append(temp_d1_price)
    
    temp_d2_price = d1_price[len(d1_price)-1] - d1_price[len(d1_price)-2]
    d2_price.append(temp_d2_price)
    
    next_Average = moving_Average()
    next_Average.update(price)
    ema_List.append(next_Average)
    
    for person in range(len(participants)):
        participants[person].update(price, d1_price, d2_price, vol)
        for b_order in range(len(buy_Orders)):
            if buy_Orders[b_order].person_Number == participants[person].number:
                buy_Orders[b_order].update(participants[person], price[len(price)-1], vol)
        for s_order in range(len(sell_Orders)):
            if sell_Orders[s_order].person_Number == participants[person].number:
                sell_Orders[s_order].update(participants[person], price[len(price)-1], vol)
        if(random.random() < prob_of_new_Order):    
            trade = order.order()
            trade.start(participants[person], price[len(price) - 1], vol)
            orders.append(trade)

    update_Order_Lists()
    if d2_price[len(d2_price)-1] != 0:
        return
    else:
        looping = 0
        plot_Price(price, time_Stamp)
        return

    
def fill_Orders():
    global bid_Que
    global ask_Que
    global max_Bid_Amount 
    global min_Ask_Amount
    global buy_Orders
    global sell_Orders
    global price
    global time_Stamp
    global closed_Buy_Orders
    global closed_Sell_Orders
    global volume
    
    tick_Volume = 0
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
        
    if ask_Que != []:
        min_Ask_Amount = min(ask_Que)

    #print("Number of bids: " + str(len(bid_Que)))
    #print("Number of asks: " + str(len(ask_Que)))
    
    while((bid_Que != []) & (ask_Que != []) & (max_Bid_Amount >= min_Ask_Amount)):
       
        tick_Volume += 1
        for ii in range(len(buy_Orders)):
            if buy_Orders[ii].amount == max_Bid_Amount:
                if buy_Orders[ii].order_Status == "open":
                    buy_Orders[ii].order_Status = "closed"
                    #print_Order(buy_Orders[ii])
                    #closed_Buy_Orders.append(buy_Orders[ii])
                    buy_Orders.pop(ii)
                    bid_Que.pop(bid_Que.index(max_Bid_Amount))
                    if bid_Que == []:
                        #max_Bid_Amount = min(ask_Que)
                        break
                    max_Bid_Amount = max(bid_Que)
                    break
    
        for jj in range(len(sell_Orders)):
            if sell_Orders[jj].amount == min_Ask_Amount:
                if sell_Orders[jj].order_Status == "open":
                    sell_Orders[jj].order_Status = "closed"
                    #print_Order(sell_Orders[jj])
                    #closed_Sell_Orders.append(sell_Orders[jj])
                    sell_Orders.pop(jj)
                    ask_Que.pop(ask_Que.index(min_Ask_Amount))
                    if ask_Que == []:
                        #min_Ask_Amount = max(bid_Que)
                        break
                    min_Ask_Amount = min(ask_Que)
                    break   
    if bid_Que == []:
        max_Bid_Amount = min(ask_Que)  
    if ask_Que == []:
        min_Ask_Amount = max(bid_Que)     
        
    temp_Price = (max_Bid_Amount + min_Ask_Amount)/2
    price.append(temp_Price)
    now = datetime.now()
    time_Stamp.append(now)
    volume.append(tick_Volume)
    print("Max bid: " + str(max_Bid_Amount))
    print("Min Ask: " + str(min_Ask_Amount))
    print("Price: " + str(temp_Price))
    print("Volume: " + str(tick_Volume))
    next_Tick()
    
def plot_Price(price, time_Stamp):
    global volume
    global ema_List
    ema5 = [price[0]]
    ema10 = [price[0]]
    global ema20
    ema50 = [price[0]]
    ema100 = [price[0]]
    ema200  = [price[0]]
    for ema in range(len(ema_List)):
        ema5.append(ema_List[ema].Ema_5)
        ema10.append(ema_List[ema].Ema_10)
        ema20.append(ema_List[ema].Ema_20)
        ema50.append(ema_List[ema].Ema_50)
        ema100.append(ema_List[ema].Ema_100)
        ema200.append(ema_List[ema].Ema_200)
        
    if(len(ema5)>len(volume)):
        ema5.pop(0)
        ema10.pop(0)
        ema20.pop(0)
        ema50.pop(0)
        ema100.pop(0)
        ema200.pop(0) 
        
    price.pop(0)
    time_Stamp.pop(0)
    df = pd.DataFrame({'Price':price, 'Timestamp':time_Stamp, 'ema200':ema200})
    #df = pd.DataFrame({'Price':price, 'Timestamp':time_Stamp, 'ema5':ema5, 'ema20':ema20, 'ema50':ema50, 'ema200':ema200})
    df2 = pd.DataFrame({'Timestamp': time_Stamp, 'Volume': volume})
    
    #chart_list = {'Price','ema5','ema20','ema50','ema200'}
    chart_list = {'Price','ema200'}
    
    ax1 = df.plot(kind='line',x='Timestamp', y=chart_list, style='r-')
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df2.plot(kind='line',x='Timestamp', y='Volume', style='b-', ax=ax2)
    plt.show()
    
def create_Participants(num_Participants):     
    current_Num_Participants = len(participants)
    for person in range(num_Participants): #establishes a list of market participants
        trader = participant.participant(current_Num_Participants + person, vol)
        participants.append(trader)
        trade = order.order()
        trade.start(participants[person], price[len(price) - 1], vol)
        orders.append(trade)

    update_Order_Lists()
    while(looping):
        fill_Orders()
    
    
try:
    create_Participants(num_Participants)
except:
    plot_Price(price, time_Stamp)

