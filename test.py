#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test file to test the functionality of operation.py
"""

from operation import Electrical_storage, Operator

storage = Electrical_storage('li_ion', storage_type='Li-Ion', p_nom=3.0, capacity=2.0)

op = Operator(name='operator', device=storage)
op.importcsv(filename='storage_test_profile.csv', profile_name='profile1')
# print(op.profile1)
# print(op.profile1.index)
op.simple_storage_operation(op.profile1)