#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test file to test the functionality of operation.py
"""

from operation import Electrical_storage, Operator

storage1 = Electrical_storage('li_ion', storage_type='Li-Ion', 
                              p_nom=3.0, 
                              capacity=2.0, 
                              state_of_charge_initial = 0.0)
storage2 = Electrical_storage('li_ion', storage_type='Li-Ion', 
                              p_nom=5.0, 
                              capacity=4.0, 
                              state_of_charge_initial = 0.0)

op = Operator(name='operator', devices=[storage1, storage2])
op.importcsv(filename='storage_test_profile.csv', profile_name='profile1')
# print(op.profile1)
# print(op.profile1.index)
grid_discharge, grid_charge, storage_list = op.quarter_storage(op.profile1)