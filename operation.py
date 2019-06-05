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
        print(residual_load)
        
        residual_list = np.array([6.0,6.0,10.0])
#        df = pd.read_csv('test.csv')
#        print(df)
        #The incoming List in which load and production are already added together (- equals still load left; + means prdouction surplus)
        
        SOC_list = np.array([0.0,0.0,0.0])

        grid_charge = float(0)                      #The energy that is needed from the grid
        grid_discharge = float(0)                   #The energy that is put into the grid
        efficiency = 0.98                  #efficency for li ion batteries


    
        #for row in residual_list:  
            #Die Schleife soll nun alle x Minuten den Stand berechnen
            #x ist abhängig von "row" also der Liste selber

            
        SOC = []                # State of Charge
        C_n = []                # nominal Capacity of the storages
        C_t = []                # capacity of the storages at the time t
        p_nom = []              # maximum power list
        capacity_list = []      #The absolut capacity

        
        
        for i in range(len(self.device)):
            
            
            capacity_list.append(self.device[i].capacity)
#           print('capacity_list', capacity_list)
            
            p_nom.append(self.device[i].p_nom) 
#           print('p_nom', p_nom)
            
            C_n.append(self.device[i].capacity) 
#           print(C_n)
            
            SOC.append(self.device[i].state_of_charge_t)
#           print(SOC)
            
            self.device[i].state_of_charge_t = self.device[i].state_of_charge_initial  # set initial SOC as SOC_t 
#           charge or discharge batteries by residual_loads, betrachtet die Einspeicherverluste beim Einspeichern der PV Leistung in die Speicher
            
            SOC[i] += residual_load[i]/C_n[i] * efficiency   
            C_t.append(SOC[i] * C_n[i])
#           print(C_t)


        print("Beginning SOC:", SOC)
                
        C_t = np.asarray(C_t)
        capacity_list = np.asarray(capacity_list)
        C_comparision = capacity_list - C_t
        print("C_t", C_t)
        print("C_comparision", C_comparision)
        print("capacity", capacity_list)
        #überprüft ob ein Speicher in der Liste seine Kapazität überschreitet
        #negative Werte Bedeuten das dieser Speicher mit dem Betragswert überfüllt ist
        #C_comparision ist der Test ob die speicher voll sind oder nict
        #capacity_list ist die feststehende Kapazität die sich für einen Speicher nicht ändert
    
        while min(C_t) < 0 or min(C_comparision) < 0:
            #This loop looks into the stroages and checks if they can exchange energy to cover the need or if grid involvement is needed

#            print("min(C_t)", min(C_t))
#            print("max(C_t)", max(C_t))
#            print("max(C_comparision)", max(C_comparision))            
#            print("min(C_comparision)", min(C_comparision))
            
            maximum_list = C_t[np.where(C_t==C_t.max())]
            minimum_list = C_t[np.where(C_t==C_t.min())]
            
            #finds all maxima and minima in the comparisions list and makes a list out of it. Makes it possible to deal with many different storages with different power
   
            if min(C_t) < 0 and max(C_t) > 0:
                
                #this statement checks if on storage is empty and if it can be covered with energy from another one without the grid
                
        
                C_t = C_t.tolist()
                y = C_t.index(min(C_t))
                z = C_t.index(max(C_t)) 
                C_t = np.asarray(C_t)
                
                #gives the index number of the max and min storage
                
                b = float(minimum_list[0] + (maximum_list[0] - maximum_list[0] * efficiency))
                
                if p_nom[z] >= b*4 and p_nom[y] >= b*4:
                    
                    #checks if the storages are able to handle the incoming power
                    
                    C_t[y] = b
                    C_t[z] = float(0)
                
                else:
                    
                    #if the possible storage power is too small it still gives the maximum power but can't fill it in this step
                    
                    C_t[y] = float(minimum_list[0] + p_nom[z]/4)
                    C_t[z] = float(maximum_list[0] - p_nom[z]/4)
                
                
                C_comparision = capacity_list - C_t 
                C_comparision = np.asarray(C_comparision)
                
                
            elif min(C_t) < 0 and max(C_t) == 0:
                
                #this statement invovles grid energy to charge storages if all other storages are also empty or have demand
                

                grid_charge = float(grid_charge + (min(C_t)*-1))     
                C_t[np.where(C_t==C_t.min())] = 0
                print("necessary grid_charge =", grid_charge)
                #print(C_t)
                C_comparision = capacity_list - C_t
                C_comparision = np.asarray(C_comparision)

                
            
            elif max(C_comparision) > 0:
                
                #this statement checks if storages are at their full usable capacity and gives all the remaining energy to 
                #other storages if they still have free capacity
                
                
                full_list = C_comparision[np.where(C_comparision==C_comparision.min())] 
                
                         
                C_t = C_t.tolist()
                C_comparision = C_comparision.tolist()
                
                
                z = C_comparision.index(max(C_comparision)) 
                y = C_comparision.index(min(C_comparision))
                
                
                C_comparision = np.asarray(C_comparision)
                C_t = np.asarray(C_t)
                
                """
                Fehler im else
                """                
                
                
                b = full_list[0] * -1

                if p_nom[z] >= full_list[0] * -4 and p_nom[y] >= full_list[0] *-4:
                
                    C_t[z] = float(C_t[z] + full_list[0] * -1) 
                    C_t[y] = capacity_list[y]
                
                else:
                    print("else")
                    C_t[z] = float(C_t[z] + full_list[0] * -1) 
                    C_t[y] = capacity_list[y]
                    
                    
                """
                Fehler im else
                """

                C_comparision = capacity_list - C_t 
                C_comparision = np.asarray(C_comparision)
                
                
            elif min(C_comparision) < 0 or max(C_comparision) < 0:  
                
                #this statement is used when all the storages are at their full capacity and puts the remaining energy into the grid
                
                grid_discharge = sum(C_comparision)*-1
                C_t = capacity_list
                
                
                C_comparision = capacity_list - C_t 
                C_comparision = np.asarray(C_comparision)
                
                
                print("necessary grid_discharge =", grid_discharge)
              
                                
            else:
                break
        print ("Result of the storages :", C_t)
        print ("Result of the C_comparision :", C_comparision)
        return grid_discharge, grid_charge, C_t, C_comparision
        """
        Diese Operation ist in der Lage Ergebnisse in eine Excel-Datei zu packen
            df = pd.DataFrame({'storage list':storage_list})
            writer = ExcelWriter('Ergebnisse.xlsx')
            df.to_excel(writer,'Sheet1',index=False)
            writer.save()
        """