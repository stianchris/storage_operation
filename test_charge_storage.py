#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test file to test the functionality of operation.py
"""

from devices import Electrical_storage
from operation import Operator
import pandas as pd
import matplotlib.pyplot as plt

storage = Electrical_storage('li_ion', storage_type='Li-Ion', p_nom=3.0, capacity=3.0)

op = Operator(name='operator', device=storage)
op.importcsv(filename='grid_loadshapes.csv', profile_name='profile1')

#%%
#TODO: Include df in Electrical_storage class
df = pd.DataFrame({'Time': op.profile1.index , 'soc': None, 'res_load': None})
df.set_index('Time', inplace = True)
print(df.head())

for index, load in op.profile1.iterrows():
    
    df.soc.loc[index], df.res_load.loc[index] = op.charge_storage(load.item())
    
#%%
print(df.head())
df.plot(figsize = (9,5))
plt.show()