#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Christian Brosig (TH Köln), ... (TH Köln)

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This package is used to calculate the operation of storages or other devices.
"""
from __future__ import division, absolute_import

import os
from typing import Any, Union

import pandas as pd
import pickle
# maybe not needed:
import six
from pandas import DataFrame
from pandas.io.parsers import TextFileReader
from six import iteritems, itervalues, iterkeys
from six.moves import map
from weakref import ref

__author__ = "Christian Brosig (TH Köln), ... (TH Köln)"
__copyright__ = "Copyright 2018-2019 Christian Brosig (TH Köln), ... (TH Köln), GNU GPL 3"


class Electrical_storage():
    """
    This class provides the functionalities of an electrical storage.
    Parameters are inspired by PyPSA component storage_units.
    """
    __version__ = 0.0.1
    # 1.0.0 --> means no more API-changes - a stable release
    # 0.1.0 --> first stable release
    # 0.0.1 --> bug-fixes and minor changes
    def __init__(self, name, **kwargs):
        """
        Electrical storage class.

        :param string name: Name of the storage.

        +++
        TODO: - write import and export functions and find a way to store these presets
              - decide how time is implemented!
              - write proper implementation of kwargs-method and the initialization of params!
        +++
        """
        self.name = name
        self.storage_type = 'lithium ion'
        self.efficiency_store = float()  # in per unit
        self.efficiency_dispatch = float()  # in per unit
        self.standing_loss = float()  # in per unit
        self.p_nom = float()  # in kW
        self.capacity = float()  # in kWh
        self.investment_costs = float()  # in €/kWh
        self.operational_costs = float()  # in €/kWh
        self.state_of_charge_initial = float()  # in kWh?
        self.state_of_charge_t = float()
        self.t0 = pd.datetime(year=2015,
                              month=1,
                              day=1,
                              hour=0,
                              minute=0)
        self.temperatur_coeff = float()  # placeholder for temperature-curve etc.
        self.cycles_init = float()
        self.cycles = float()

        for key, value in iteritems(kwargs):
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                message = str(self) + " has no attribute {}".format(key)
                raise AttributeError(message)


    def __repr__(self):
        return("Electrical storage {} of type {}".format(self.name,self.storage_type))

    def import_preset(self, name):
        pass

    def export_preset(self, name):
        pass


class Operator():
    """
    This class provides functions to operate storages and other devices.
    """

    # %%
    def __init__(self, name, device, **kwargs):
        """
        Initialization of the Operator class.

        :param string name: Name of the operator.
        :param object device: Reference to the storage device.

        +++
        TODO:

        +++
        """
        self.name = name
        self.device = device
        self.time_base = 15/60
        for key, value in iteritems(kwargs):
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                message = str(self) + " has no attribute {}".format(key)
                raise AttributeError(message)

    def __repr__(self):
        return ("Operator {}".format(self.name))

    def simple_storage_operation(self, residual_load):
        """
        A simple storage operation strategy that charges while residual_load is positive and state of charge less than 1
        and decharges while residual_load is negative and state_of_charge higher than 0.
        No efficiency! No test for the installed power!
        :param residual_load:
        :return:
        """
        self.operation_profile = pd.DataFrame()
        cap = self.device.capacity
        for load in residual_load.index:
            pass

#            if residual_load.loc[load] > 0:
#                print(residual_load.loc[load])
 
    def charge_storage(self, residual_load):
        """
        #TODO: Find better name for this function
        
        residual_load > 0 = Energy demand
        residual_load < 0 = Energy surplus
        
        needed from device:                 implemented:
            device.p_nom                        ()
            device.efficiency_store             ()
            device.efficiency_dispatch          ()
            device.capacity                     (x)
            device.state_of_charge_initial      (needed?)
            device.state_of_charge_t            (x)
            device.time_base                    (x)
        """
        if residual_load > 0:
            #Energy demand --> discharge storage if state_of_charge_t > 0
            
            if self.device.state_of_charge_t > 0:
                #storage is not empty

                self.device.state_of_charge_t -= residual_load * self.time_base
                
                #do not discharge below 0 kWh
                if self.device.state_of_charge_t < 0:
                    residual_load = self.device.state_of_charge_t / self.time_base * -1
                    self.device.state_of_charge_t = 0
                    
                else:
                    residual_load = 0
                    
            else:
                return self.device.state_of_charge_t, residual_load
                
        elif residual_load < 0:
            
            #Energy surplus --> charge storage if state_of_charge_t < capacity 
            
            if self.device.state_of_charge_t < self.device.capacity:
                #storage has not reached its max capacity
                
                self.device.state_of_charge_t += residual_load *self.time_base * -1
                
                #do not overcharge the storage
                if self.device.state_of_charge_t > self.device.capacity:
                    residual_load = (self.device.capacity - 
                                     self.device.state_of_charge_t) /self.time_base
                    self.device.state_of_charge_t = self.device.capacity
                    
                else:
                    residual_load = 0
                    
            else:
                #storage has reached its max capacity
                return self.device.state_of_charge_t, residual_load
        
        return self.device.state_of_charge_t, residual_load

    def importcsv(self,
                  filename: str,
                  profile_name):
        """
        Import a csv and store it in a standardized DataFrame.

        :param str filename: the filename of the csv to be imported.
        :param str profile_name: the name of the profile (e.g. residual_load_HH1)
        :return:
        +++
        TODO: - imply tests for the csv-import and format of the DataFrame.
              - check the Datetimeindex for summer/wintertime and change it!
        """

        profile = pd.read_csv(filename, sep=',',index_col='Time')
        profile.index= pd.DatetimeIndex(profile.index)
        assert isinstance(profile, pd.DataFrame)
        setattr(self, profile_name, profile)
