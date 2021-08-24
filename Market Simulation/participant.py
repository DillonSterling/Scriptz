# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 17:41:05 2021

@author: SESA553573
"""
import random

class participant(): #defines the properties of the market participants
    def __init__(self, number, vol):
        self.bullishness = random.random()
        self.perceived_Value = random.gauss(50, vol)
        self.number = number
        
    def update(self, price, d1_price, d2_price, vol):
        #self.bullishness = min(max(self.bullishness + (random.random()-0.5)/10,0),1)
        dpdt = price[len(d1_price)-1]/price[len(d1_price)-2]-1
        dpdv = price[len(price)-1]/self.perceived_Value - 1
        if random.random() < 1:
            self.bullishness = min(max(self.bullishness + .001 * (dpdt - .01*dpdv**3)/vol,0),1)
        else:
            self.bullishness = self.bullishness
        self.perceived_Value = self.perceived_Value