#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Christian Brosig (TH Köln), Sascha Birk (TH Köln), 
# Silvan Rummeny (TH Köln), Sven Meier (TH Köln)

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
This package is used to provide models for storages or other devices.
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

__author__ = "Christian Brosig (TH Köln), Sascha Birk (TH Köln), Silvan Rummeny (TH Köln), Sven Meier (TH Köln)"
__copyright__ = "Copyright 2018-2019 Christian Brosig (TH Köln), Sascha Birk (TH Köln), Silvan Rummeny (TH Köln), Sven Meier (TH Köln), GNU GPL 3"
__version__ = "0.0.1"
# 1.0.0 --> means no more API-changes - a stable release
# 0.1.0 --> first stable release
# 0.0.1 --> bug-fixes and minor changes

class Electrical_storage():
    """
    This class provides the functionalities of an electrical storage.
    Parameters are inspired by PyPSA component storage_units.
    """
    __version__ = "0.0.1"
    
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
