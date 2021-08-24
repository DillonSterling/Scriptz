# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 16:46:16 2021

@author: SESA553573
"""
import random

class order():
    
    def start(self, person, price, vol): #determinies how each participant responds to market conditions
        self.person_Number = person.number
    
        if random.random() < 0.5:
            if random.random() < person.bullishness:
                if person.perceived_Value > price:
                    self.buy_Sell = "buy"
                    self.order_Type = "market"
                    self.amount = price
                    self.order_Status = "open"
                else:
                    self.buy_Sell = "buy"
                    self.order_Type = "limit"
                    self.amount = person.perceived_Value
                    self.order_Status = "open"
    
            else:
                if person.perceived_Value < price:
                    self.buy_Sell = "sell"
                    self.order_Type = "market"
                    self.amount = price
                    self.order_Status = "open"
                else:
                    self.buy_Sell = "sell"
                    self.order_Type = "limit"
                    self.amount = person.perceived_Value
                    self.order_Status = "open"
        else:
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
    
            else:
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
    def update(self, person, price, vol):
        if random.random() < 1:
            if random.random() < person.bullishness:
                    self.buy_Sell = "buy"
                    self.order_Type = "market"
                    self.amount = price
                    self.order_Status = "open"

            else:
                    self.buy_Sell = "sell"
                    self.order_Type = "market"
                    self.amount = price
                    self.order_Status = "open"
