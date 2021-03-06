#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 13:55:37 2019

@author: pat
"""
#import libraries
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import pymysql
import pymysql
from pandastable import Table, TableModel

#import other pages
import BackEnd
from config import LoginInfo, DBConnect
import os
import sys

def init_styleSheet():
    global styleDict 
    styleDict = {}
    styleDict["Title"] = "CMT - Bike"
    styleDict["windowSize"] = "1024x768"
    styleDict["windowWidth"] = 1024
    styleDict["windowHeight"] = 768
    styleDict["labelLen"] = 15
    styleDict["xPadding"] = 20
    styleDict["yPadding"] = 5
    styleDict["inlinePadding"] = 5
    styleDict["topPadding"] = 150
    styleDict["fontColor"] = "black"
    styleDict["fontType"] = "Arial"
    styleDict["fontSize"] = "18"
    styleDict["fontStyle"] = "bold"
    styleDict["buttonWidth"] = 10
    styleDict["TabHeaderFgColor"] = "white"
    styleDict["TabHeaderBgColor"] = "#4B96E9"
    return(styleDict)

def restart_program():
    print(LoginInfo.loginid[0] + 223)
    del LoginInfo.loginid[0]
    python = sys.executable
    os.execl(python, python, *sys.argv)

def popupMsg(msg):
        popup = tk.Tk()
        popup.title(styleDict["Title"])
        msg_label = tk.Label(popup, text = msg)
        msg_label.pack()
        done_button = tk.Button(popup, text="Done", command = popup.destroy)
        done_button.pack()
        popup.mainloop()
        
def chkNumber(character):
    if character.isdigit():
        return True
    else:
        return False
    
def connectDB():
    host = 'localhost'
    user = 'root'
    password = DBConnect.password
    db = DBConnect.db
    try:
        connection = pymysql.connect(host, user, password, db)
        #print("Connect to DB Success")
    except pymysql.InternalError as e:
        popupMsg(e)
        #print("Connection Error", e)
    return connection

def disconnectDB(connection):
    connection.close()
    

class LocationMngPage(tk.Frame):
    def __init__(self, master):
        
        #Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill = tk.BOTH, expand = True)
        
        #Initialize Style Dict
        styleDict = init_styleSheet()

        #Set Header Frame
        h_frame = tk.Frame(self, height = styleDict["topPadding"])
        h_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])      
        home_button = tk.Button(h_frame, text = "Home", width = styleDict["buttonWidth"], command = lambda: master.switch_frame(BackEnd.BackEndHomePage), bg = styleDict["TabHeaderBgColor"])
        home_button.pack(side = tk.LEFT)
        lobutton = tk.Button(h_frame, text="Log Out", width = styleDict["buttonWidth"], command=restart_program, bg = styleDict["TabHeaderBgColor"])
        lobutton.pack(side=tk.RIGHT)
        
        #Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])

        menu_label = tk.Label(menu_frame, text = "Location Management: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)

        #Set Action Button Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        edit_button = tk.Button(act_button_frame, text = "Edit", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(LocationEditPage))
        edit_button.pack(side = tk.RIGHT)
        add_button = tk.Button(act_button_frame, text = "Add", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(LocationAddPage))
        add_button.pack(side = tk.RIGHT, padx = styleDict["inlinePadding"])
        
        #Create Data Table Frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill = tk.BOTH, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        
        #Get All Locations
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT l.ID ID, l.Zone_Name `Location Name`, c.City_Name `City Name`, 
                                l.Slot, l.`Status`, l.Updated_At `Last Updated At`, o.Username `Last Updated By`
                                FROM location AS l
                                INNER JOIN city AS c ON l.City_ID = c.ID
                                INNER JOIN operator_manager AS o ON l.Last_Operator_ID = o.ID
                                ORDER BY l.Updated_At DESC;'''
        sql = pd.read_sql_query(query, connection, params = None)
        location_df = pd.DataFrame(sql, columns = ['ID','Location Name', 'City Name', 'Slot', 'Status', 'Last Updated At', 'Last Updated By'])
        disconnectDB(connection)
        
        #Set Data Table Frame (Display table only have a data)
        if not location_df.empty:
            location_table = Table(table_frame, dataframe = location_df, showstatusbar = True)
            location_table.show()
        
class LocationAddPage(tk.Frame):
    def __init__(self, master):
        
        #Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill = tk.BOTH, expand = True)
        
        #Initialize Style Dict
        styleDict = init_styleSheet()
        
        #Set Header Frame
        h_frame = tk.Frame(self, height = styleDict["topPadding"])
        h_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])      
        home_button = tk.Button(h_frame, text = "Home", width = styleDict["buttonWidth"], command = lambda: master.switch_frame(BackEnd.BackEndHomePage), bg = styleDict["TabHeaderBgColor"])
        home_button.pack(side = tk.LEFT)
        lobutton = tk.Button(h_frame, text="Log Out", width = styleDict["buttonWidth"], command=restart_program, bg = styleDict["TabHeaderBgColor"])
        lobutton.pack(side=tk.RIGHT)
        
        #Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])

        menu_label = tk.Label(menu_frame, text = "Add Location: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)
        
        #Set Location Name Frame
        location_name_frame = tk.Frame(self)
        location_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        location_name_label = tk.Label(location_name_frame, text = "Location Name: ", width = styleDict["labelLen"], anchor = tk.W)
        location_name_label.pack(side = tk.LEFT)
        self.var_location_name = StringVar()
        location_name_input = tk.Entry(location_name_frame, textvariable = self.var_location_name)
        location_name_input.pack(fill = tk.X)
        
        #Set City Name Frame
        city_name_frame = tk.Frame(self)
        city_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        city_name_label = tk.Label(city_name_frame, text = "City Name: ", width = styleDict["labelLen"], anchor = tk.W)
        city_name_label.pack(side = tk.LEFT)
        
        #Get City from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT City_Name `City Name` FROM city ORDER BY City_Name;'''
        cursor.execute(query)
        city_list = []
        for row in cursor.fetchall():
            city_list.append(row)
        disconnectDB(connection)
        
        self.var_city_name = StringVar()
        city_name_input = ttk.Combobox(city_name_frame, values = city_list, state='readonly', textvariable = self.var_city_name)
        city_name_input.set('Select City')
        city_name_input.pack(fill = tk.X)
        
        
        #Set Slot Frame
        slot_frame = tk.Frame(self)
        slot_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        slot_label = tk.Label(slot_frame, text = "Slot: ", width = styleDict["labelLen"], anchor = tk.W)
        slot_label.pack(side = tk.LEFT)
        self.var_slot = StringVar()
        slot_input = tk.Entry(slot_frame, textvariable = self.var_slot)
        slot_register = slot_frame.register(chkNumber)
        slot_input.config(validate = "key", validatecommand = (slot_register, "%P"))
        slot_input.pack(fill = tk.X)
        
        #Set Status Frame
        status_frame = tk.Frame(self)
        status_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        status_label = tk.Label(status_frame, text = "Status: ", width = styleDict["labelLen"], anchor = tk.W)
        status_label.pack(side = tk.LEFT)
        status_list = ["Active", "Inactive"]
        self.var_status = StringVar()
        status_input = ttk.Combobox(status_frame, values = status_list, state='readonly', textvariable = self.var_status)
        status_input.current(0)
        status_input.pack(fill = tk.X)
        
        #Set Action Buttion Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        back_button = tk.Button(act_button_frame, text = "Back", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(LocationMngPage))
        back_button.pack(side = tk.RIGHT)
        confirm_button = tk.Button(act_button_frame, text = "Confirm", width = styleDict["buttonWidth"], 
                                command = self.addLocation)
        confirm_button.pack(side = tk.RIGHT, fill = tk.X, padx = styleDict["inlinePadding"])
        
    def addLocation(self):
        #Get All Data From User Control
        tmp_location_name = self.var_location_name.get()
        tmp_city_name = self.var_city_name.get()
        tmp_slot_input = self.var_slot.get()
        tmp_status_input = self.var_status.get()
        tmp_operator_ID = LoginInfo.loginid[0]
        
        try:
            #Get More Data from DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''SELECT ID, City_Name FROM city WHERE `City_Name` = %s;'''
            cursor.execute(query, tmp_city_name)
            for row in cursor.fetchall():
                tmp_city_id = row[0]
            disconnectDB(connection)
        
            #Insert Data into DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''INSERT INTO location (Zone_Name, Slot, `Status`, Created_At, Updated_At, City_ID, Last_Operator_ID) VALUES(%s, %s, %s, NOW(), NOW(), %s, %s);'''
            query_param = (tmp_location_name, tmp_slot_input, tmp_status_input, tmp_city_id, tmp_operator_ID)
            cursor.execute(query, query_param)
            connection.commit()
            disconnectDB(connection)
            result = True
        except:
            result = False
        
        if result:
            msg = "Location is added successfully"
        else:
            msg = "Some thing went wrong. Sorry for an inconvenience"
        popupMsg(msg)
    

class LocationEditPage(tk.Frame):
    def __init__(self, master):
        
        #Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill = tk.BOTH, expand = True)
        
        #Initialize Style Dict
        styleDict = init_styleSheet()
        
        #Set Header Frame
        h_frame = tk.Frame(self, height = styleDict["topPadding"])
        h_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])      
        home_button = tk.Button(h_frame, text = "Home", width = styleDict["buttonWidth"], command = lambda: master.switch_frame(BackEnd.BackEndHomePage), bg = styleDict["TabHeaderBgColor"])
        home_button.pack(side = tk.LEFT)
        lobutton = tk.Button(h_frame, text="Log Out", width = styleDict["buttonWidth"], command=restart_program, bg = styleDict["TabHeaderBgColor"])
        lobutton.pack(side=tk.RIGHT)
        
        #Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])

        menu_label = tk.Label(menu_frame, text = "Edit Location: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)
        
        #Set Location Name Frame
        location_name_frame = tk.Frame(self)
        location_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        location_name_label = tk.Label(location_name_frame, text = "Location Name: ", width = styleDict["labelLen"], anchor = tk.W)
        location_name_label.pack(side = tk.LEFT)
        
        #Get Location from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT ID, Zone_Name `Location Name` FROM location ORDER BY Zone_Name;'''
        cursor.execute(query)
        location_list = []
        for row in cursor.fetchall():
            location_list.append(row[1])
        disconnectDB(connection)

        #Set Location Combobox
        self.var_location_name = StringVar()
        location_name_input = ttk.Combobox(location_name_frame, values = location_list, state='readonly', textvariable = self.var_location_name)
        location_name_input.set('Select Zone')
        # >> Bind onchange event to location combobox
        location_name_input.bind("<<ComboboxSelected>>", self.callback)
        location_name_input.pack(fill = tk.X)
        
        #Set City Name Frame
        city_name_frame = tk.Frame(self)
        city_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        city_name_label = tk.Label(city_name_frame, text = "City Name: ", width = styleDict["labelLen"], anchor = tk.W)
        city_name_label.pack(side = tk.LEFT)
        
        #Get City from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT City_Name `City Name` FROM city ORDER BY City_Name;'''
        cursor.execute(query)
        city_list = []
        for row in cursor.fetchall():
            city_list.append(row)
        disconnectDB(connection)

        #Set City Combobox
        self.var_city_name = StringVar()
        city_name_input = ttk.Combobox(city_name_frame, values = city_list, state='readonly', textvariable = self.var_city_name)
        city_name_input.set('Select City')
        city_name_input.pack(fill = tk.X)
        
        
        #Set Slot Frame
        slot_frame = tk.Frame(self)
        slot_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        self.var_slot = StringVar()
        slot_label = tk.Label(slot_frame, text = "Slot: ", width = styleDict["labelLen"], anchor = tk.W)
        slot_label.pack(side = tk.LEFT)
        slot_input = tk.Entry(slot_frame, textvariable = self.var_slot)
        slot_register = slot_frame.register(chkNumber)
        slot_input.config(validate = "key", validatecommand = (slot_register, "%P"))
        slot_input.pack(fill = tk.X)
        
        #Set Status Frame
        status_frame = tk.Frame(self)
        status_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        status_label = tk.Label(status_frame, text = "Status: ", width = styleDict["labelLen"], anchor = tk.W)
        status_label.pack(side = tk.LEFT)
        status_list = ["Active", "Inactive"]
        self.var_status = StringVar()
        status_input = ttk.Combobox(status_frame, values = status_list, state='readonly', textvariable = self.var_status)
        status_input.current(0)
        status_input.pack(fill = tk.X)
        
        #Set Action Buttion Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        back_button = tk.Button(act_button_frame, text = "Back", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(LocationMngPage))
        back_button.pack(side = tk.RIGHT)
        confirm_button = tk.Button(act_button_frame, text = "Confirm", width = styleDict["buttonWidth"], 
                                command = self.editLocation)
        confirm_button.pack(side = tk.RIGHT, fill = tk.X, padx = styleDict["inlinePadding"])

    def callback(self, event):
        self.setCurrentLocData()
        
    def setCurrentLocData(self):
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT l.Zone_Name `Location Name`, c.City_Name `City Name`, l.Slot, l.`Status`
                                FROM location AS l
                                INNER JOIN city AS c ON l.City_ID = c.ID
                                WHERE l.Zone_Name = %s;'''
        cursor.execute(query, self.var_location_name.get())
        for row in cursor.fetchall():
            self.var_city_name.set(row[1])
            self.var_slot.set(row[2])
            self.var_status.set(row[3])
    
    def editLocation(self):
        #Get All Data From User Control
        tmp_location_name = self.var_location_name.get()
        tmp_city_name = self.var_city_name.get()
        tmp_slot_input = int(self.var_slot.get())
        tmp_status_input = self.var_status.get()
        tmp_operator_ID = LoginInfo.loginid[0]
        
        try:
            #Get More Data from DB
            connection = connectDB()
            cursor = connection.cursor()
            # >> Get Location ID
            query = '''SELECT ID, Zone_Name FROM location WHERE `Zone_Name` = %s;'''
            cursor.execute(query, tmp_location_name)
            for row in cursor.fetchall():
                tmp_location_id = row[0]            
            # >> Get City ID
            query = '''SELECT ID, City_Name FROM city WHERE `City_Name` = %s;'''
            cursor.execute(query, tmp_city_name)
            for row in cursor.fetchall():
                tmp_city_id = row[0]
            disconnectDB(connection)
        
            #Update Data into DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''UPDATE location SET Slot = %s, `Status` = %s, Updated_At = NOW(), City_ID = %s, Last_Operator_ID = %s WHERE ID = %s;'''
            query_param = (tmp_slot_input, tmp_status_input, tmp_city_id, tmp_operator_ID, tmp_location_id)
            cursor.execute(query, query_param)
            connection.commit()
            disconnectDB(connection)
            result = True
        except:
            result = False
        
        if result:
            msg = "Location is updated successfully"
        else:
            msg = "Some thing went wrong. Sorry for an inconvenience"
        popupMsg(msg)

