#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test file to test the functionality of operation.py
"""

from operation import Electrical_storage, Operator
import numpy as np

residual_list = np.array([6.0,6.0,12.0,9.0])


# battery parameters
p_nom_list = np.array([4.0,2.0,5.0,3.0])
capacity_list = np.array([7.0,7.0,9.0,9.0])
SOC_list = np.array([0.0,0.0,0.0,0.0])

devices = []
for i in range(len(residual_list)): 
    devices.append(Electrical_storage('li_ion', storage_type='Li-Ion', 
                              p_nom=p_nom_list[i], 
                              capacity=capacity_list[i], 
                              state_of_charge_initial = SOC_list[i]))      

op = Operator(name='operator', device=devices)
# op.importcsv(filename='storage_test_profile.csv', profile_name='profile1')
# print(op.profile1)
# print(op.profile1.index)
#grid_discharge, grid_charge, storage_list, capacity_list2 = op.quarter_storage(op.profile1)

grid_discharge, grid_charge, SOC, C_comparision = op.quarter_storage(residual_list)
