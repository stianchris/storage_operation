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
from six import iteritems, itervalues, iterkeys
from six.moves import map

#from weakref import reffrom numpy import array       
import numpy as np
from array import *
import csv
from pandas import ExcelWriter


__author__ = "Christian Brosig (TH Köln), ... (TH Köln)"
__copyright__ = "Copyright 2018-2019 Christian Brosig (TH Köln), ... (TH Köln), GNU GPL 3"


class Electrical_storage():
    """
    This class provides the functionalities of an electrical storage.
    Parameters are inspired by PyPSA component storage_units.
    """


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
    def __init__(self, name, devices, **kwargs):
        """
        Initialization of the Operator class.
        :param string name: Name of the operator.
        :param object device: Reference to the storage device.
        +++
        TODO:
        +++
        """
        self.name = name
        self.devices = devices
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
        
    # %%

    def quarter_storage(self, residual_load):
        
        """
        This function defines an optimized use of self-made energy   
        The goal is to have a maximized self-sufficiency with maximized self usage
        
                +++
            TODO:
                csv daten einzeln einbringen und nicht als Matrix sondern mit for Schleife aber wie? 
                    Einlesen einer CSV mit mehreren Spalten birgt das Problem das eine Zeile als 1 Indize in der Liste genommen wird.
                Quartierspeicher am Sonntag wenn der an Leistungsgrenze kommt?
                Lade und Entladeleistung einbringen
                Verluste
                 - Parameter und Autor(en) in docstring beschreiben
                 - Parameter in input der Funktion
                 - Test hierzu schreiben
                 - Einlesen von csv-Dateien externalisieren
                 - Ergebnis als return einer Variablen ausgeben
                
                +++
        """
        """
        # create empty Dataframe with headers for storage parameters
        storages = pd.DataFrame({'capacity':[],                 
                                 'p_nom':[],
                                 'state_of_charge_initial':[]})
        # read parameter values from all devices and write in DataFrame
        for i in range(len(self.devices)):  
            storages = storages.append(pd.DataFrame({'capacity':[self.devices[i].capacity],
                                                     'p_nom':[self.devices[i].p_nom], 
                                                     'state_of_charge_initial':[self.devices[i].state_of_charge_initial]}),
                                       ignore_index=True)
        """
        # This is how "residual_load" then looks like (input)
    
#        residual_load = pd.DataFrame({'device1':[10.0],
#                                     'device2':[100.0],
#                                     'device3':[-50.0]})
        residual_list = np.array([8.0,8.0,10.0])
        storage_list = np.array([0.0,0.0,0.0])
        capacity_list = np.array([7.0,7.0,9.0])
        
        grid_charge = float(0)
        grid_discharge = float(0)
        efficiency_dispatch = 0.02
        efficiency_store = 0.02
    
        #einlesen der csv, dient hier als Ersatz für die Lastprofile
    
        #for row in residual_list:  
            #Die Schleife soll nun alle x Minuten den Stand berechnen
            #x ist abhängig von "row" also der Liste selber
    
        """
        f = open("sum.csv",'r')
        reader = csv.reader(f)
        CSVlist = []
        for row in reader:
            CSVlist.append(row)
        del CSVlist[0]
        CSVlist = np.asarray(CSVlist)
        #CSVlist = [float(l[0]) for l in CSVlist]
        print(CSVlist[0])
        residual = CSVlist[0]
        #Einlesen einer CSV mit mehreren Spalten birgt das Problem das eine Zeile als 1 Indize in der Liste genommen wird.
        """
#        df = pd.read_csv('test.csv')
#        print(df)
    
        storage_list = storage_list + residual_list
        for i in range(len(storage_list)):
            # if storages['capacity'][i] > 0.0: 
            if storage_list[i] > 0.0 :
                storage_list[i] = storage_list[i] - storage_list[i] * efficiency_store 
                #Betrachtet die Einspeicherverluste beim Einspeichern der PV Leistung in die Speicher
        print("Beginning:", storage_list)
        a = storage_list
        
        capacity_list2 = [x1 - x2 for (x1, x2) in zip(capacity_list, storage_list)] 
        capacity_list2 = np.asarray(capacity_list2)
        print("capacity_list2", capacity_list2)
        #überprüft ob ein Speicher in der Liste seine Kapazität überschreitet
        #negative Werte Bedeuten das dieser Speicher mit dem Betragswert überfüllt ist
        #capacity_list2 ist der Test ob die speicher voll sind oder nict
        #Capacity_list ist die feststehende Kapazität die sich nicht ändert
    
        while min(storage_list) < 0:
            """
            die while Schleife soll schauen das alle Stromspeicher erst geleert werden bevor Netzbezug in betracht gezogen wird.
            Diese Betrachtung würde für eine reele maximale Eigennutzung des Stromes sorgen
            Überlegung ob billanziell kann später in einer abänderung passieren
            """
    
            if min(storage_list) < 0 and max(storage_list) > 0: #and len(storage_list[np.where(a==a.max())]) > 1:
                
                
                maximum_list = storage_list[np.where(a==a.max())]
                minimum_list = storage_list[np.where(a==a.min())]
                
                
                b = float(minimum_list[0] + (maximum_list[0] - maximum_list[0] * efficiency_dispatch))
                c = float(0)
                
                
                storage_list = storage_list.tolist()
                z = storage_list.index(max(storage_list)) 
                y = storage_list.index(min(storage_list))
                storage_list = np.asarray(storage_list)
                
                
                storage_list[y] = b
                storage_list[z] = c
                
                
                capacity_list2 = [x1 - x2 for (x1, x2) in zip(capacity_list, storage_list)] 
                capacity_list2 = np.asarray(capacity_list2)
                
                
            elif min(storage_list) < 0 and max(storage_list) == 0:
                grid_charge = float(grid_charge + (min(storage_list)*-1))     
                storage_list[np.where(a==a.min())] = 0
                print("necessary grid_charge =", grid_charge)
                #print(storage_list)
                capacity_list2 = [x1 - x2 for (x1, x2) in zip(capacity_list, storage_list)] 
                capacity_list2 = np.asarray(capacity_list2)
                
            else: 
                print("wut")
                break
    
        while min(capacity_list2) < 0:
            """
            die 2te while Schleife betrachtet den Fall das bei dem Zwischenstand die maximale Speicherkapazität überschritten wird.
            Hier wird dann die überflüßige Energie and die nicht vollen Speicher weitergegeben und 
            bei vollem Stand ins Netz gespeist
            """
            
            if max(capacity_list2) > 0:
                
                
                fempty_list = capacity_list2[np.where(capacity_list2==capacity_list2.max())]
                full_list = capacity_list2[np.where(capacity_list2==capacity_list2.min())] 
                
                         
                storage_list = storage_list.tolist()
                capacity_list2 = capacity_list2.tolist()
                
                
                z = capacity_list2.index(max(capacity_list2)) 
                y = capacity_list2.index(min(capacity_list2))
                
                
                capacity_list2 = np.asarray(capacity_list2)
                storage_list = np.asarray(storage_list)
                
                
                storage_list[z] = float(storage_list[z] + full_list[0] * -1) 
                storage_list[y] = capacity_list[y]
                
                
                capacity_list2 = [x1 - x2 for (x1, x2) in zip(capacity_list, storage_list)] 
                capacity_list2 = np.asarray(capacity_list2)
                    
                
            elif min(capacity_list2) < 0 and max(capacity_list2) < 0:   
                
                
                grid_discharge = sum(capacity_list2)*-1
                storage_list = capacity_list
                
                
                capacity_list2 = [x1 - x2 for (x1, x2) in zip(capacity_list, storage_list)] 
                capacity_list2 = np.asarray(capacity_list2)
                
                
                print("necessary grid_discharge =", grid_discharge)
              
                                
            else:
                print("wut 2")
                break
        print ("Result of the storages :", storage_list)
        print ("Result of the capacity_list2 :", capacity_list2)
        return grid_discharge, grid_charge, storage_list, capacity_list2
        """
        Diese Operation ist in der Lage Ergebnisse in eine Excel-Datei zu packen
            df = pd.DataFrame({'storage list':storage_list})
            writer = ExcelWriter('Ergebnisse.xlsx')
            df.to_excel(writer,'Sheet1',index=False)
            writer.save()
        """