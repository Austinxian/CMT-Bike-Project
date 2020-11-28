#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:59:32 2019

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
    styleDict["labelLen"] = 6
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
    

class BikeMngPage(tk.Frame):
    
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

        menu_label = tk.Label(menu_frame, text = "Bike Management: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)

        #Set Action Button Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        edit_button = tk.Button(act_button_frame, text = "Edit", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(BikeEditPage))
        edit_button.pack(side = tk.RIGHT)
        add_button = tk.Button(act_button_frame, text = "Add", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(BikeAddPage))
        add_button.pack(side = tk.RIGHT, padx = styleDict["inlinePadding"])
        
        #Set Input Filter Frame
        input_filter_frame = tk.Frame(self)
        input_filter_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        
        #Filter by Bike ID
        bike_label = tk.Label(input_filter_frame, text = "Bike ID: ", width = styleDict["labelLen"], anchor = tk.W)
        bike_label.pack(side = tk.LEFT)
        
        #Get Bike ID from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT ID `Bike ID` FROM bike ORDER BY ID;'''
        cursor.execute(query)
        bike_list = []
        for row in cursor.fetchall():
            bike_list.append(row)
        disconnectDB(connection)
        
        self.var_bike_id = StringVar()
        bike_id_input = ttk.Combobox(input_filter_frame, values = bike_list, state='readonly', textvariable = self.var_bike_id)
        bike_id_input.set('Select Bike')
        bike_id_input.pack(side = tk.LEFT, padx = styleDict["inlinePadding"])
        
        
        #Filter by Location
        location_label = tk.Label(input_filter_frame, text = "Location: ", width = styleDict["labelLen"], anchor = tk.W)
        location_label.pack(side = tk.LEFT)
        
        #Get Location from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT Zone_Name FROM location ORDER BY Zone_Name;'''
        cursor.execute(query)
        location_list = []
        for row in cursor.fetchall():
            location_list.append(row[0])
        disconnectDB(connection)
        
        self.var_location_name = StringVar()
        location_input = ttk.Combobox(input_filter_frame, values = location_list, state='readonly', textvariable = self.var_location_name)
        location_input.set('Select Location')
        location_input.pack(side = tk.LEFT, padx = styleDict["inlinePadding"])
        
        #Filter by City
        city_label = tk.Label(input_filter_frame, text = "City: ", width = styleDict["labelLen"], anchor = tk.W)
        city_label.pack(side = tk.LEFT)
        
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
        city_input = ttk.Combobox(input_filter_frame, values = city_list, state='readonly', textvariable = self.var_city_name)
        city_input.set('Select City')
        city_input.pack(side = tk.LEFT, padx = styleDict["inlinePadding"])
        
        
        #Add Clear & Search Button
        clear_button = tk.Button(input_filter_frame, text = "Clear", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(BikeMngPage))
        clear_button.pack(side = tk.RIGHT)
        
        search_button = tk.Button(input_filter_frame, text = "Search", width = styleDict["buttonWidth"], 
                                command = self.FilterResult)
        search_button.pack(side = tk.RIGHT, padx = styleDict["inlinePadding"])
        
        
    def FilterResult(self):
        #Create Data Table Frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill = tk.BOTH, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT b.ID `Bike ID`, t.Type_Name `Type Name`, b.`Condition` `Status`, b.Updated_At `Last Updated At`, l.Zone_Name `Location`, c.City_Name `City`
                    FROM bike b
                    INNER JOIN type t ON b.Type_ID = t.ID
                    INNER JOIN location l ON l.ID = b.Location_ID
                    INNER JOIN city c ON c.ID = b.City_ID
                    ORDER BY b.ID;'''
        sql = pd.read_sql_query(query, connection, params = None)

        bike_df = pd.DataFrame(sql, columns = ['Bike ID','Type Name', 'Status', 'Last Updated At', 'Location', 'City'])
        disconnectDB(connection)
        if len(self.var_bike_id.get()) != 0:
            bike_id = int(self.var_bike_id.get())
            bike_df = bike_df.loc[bike_df['Bike ID'] == bike_id]
        if len(self.var_location_name.get()) != 0:
            bike_df = bike_df.loc[bike_df['Location'] == self.var_location_name.get()]
        if len(self.var_city_name.get()) != 0:
            bike_df = bike_df.loc[bike_df['City'] == self.var_city_name.get()]  
       
        #Set Data Table Frame (Display table only have a data)
        if not bike_df.empty:
            bike_table = Table(table_frame, dataframe = bike_df, showstatusbar = True)
            bike_table.show()
        else:
            popupMsg("No data found.")
        
class BikeAddPage(tk.Frame):
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
        menu_label = tk.Label(menu_frame, text = "Add Bike: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)
        
        # TYPE       
        #Set Type Name Frame
        type_name_frame = tk.Frame(self)
        type_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        type_name_label = tk.Label(type_name_frame, text = "Type: ", width = 15, anchor = tk.W)
        type_name_label.pack(side = tk.LEFT)
        
        #Get Type from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT ID, Type_Name `Type Name` FROM type ORDER BY Type_Name;'''
        cursor.execute(query)
        type_list = []
        for row in cursor.fetchall():
            type_list.append(row[1])
        disconnectDB(connection)
        
        #Set Type Combobox
        self.var_type_name = StringVar()
        type_name_input = ttk.Combobox(type_name_frame, values = type_list, state='readonly', textvariable = self.var_type_name)
        type_name_input.set('Select Type')
        #city_name_input.current(0)
        type_name_input.pack(fill = tk.X)
  
        # LOCATION      
        #Set Location Name Frame
        location_name_frame = tk.Frame(self)
        location_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        location_name_label = tk.Label(location_name_frame, text = "Location Name: ", width = 15, anchor = tk.W)
        location_name_label.pack(side = tk.LEFT)
        
        #Get Location from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT l.ID, l.Zone_Name, c.City_Name
                        FROM location AS l
                        INNER JOIN city AS c ON l.City_ID = c.ID;'''
        cursor.execute(query)
        location_list = []
        for row in cursor.fetchall():
            location_list.append(row[2].upper()+' - '+row[1])
        disconnectDB(connection)
        
        #Set Location Combobox
        self.var_location_name = StringVar()
        location_name_input = ttk.Combobox(location_name_frame, values = location_list, state='readonly', textvariable = self.var_location_name)
        location_name_input.set('Select Location')
        location_name_input.pack(fill = tk.X)

        #Set Action Buttion Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        back_button = tk.Button(act_button_frame, text = "Back", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(BikeMngPage))
        back_button.pack(side = tk.RIGHT)
        confirm_button = tk.Button(act_button_frame, text = "Confirm", width = styleDict["buttonWidth"], 
                                command = self.addBike)
        confirm_button.pack(side = tk.RIGHT, fill = tk.X, padx = styleDict["inlinePadding"])
        
    def addBike(self):
        #Get All Data From User Control
        tmp_type_name = self.var_type_name.get()
        tmp_string = self.var_location_name.get().split(sep=' - ')
        tmp_location_name = tmp_string[1]
        tmp_operator_ID = LoginInfo.loginid[0]
        
        msg = ""

        try:
            
            #Get More Data from DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''SELECT ID, Zone_Name, City_ID, Slot FROM location WHERE Zone_Name = %s;'''
            cursor.execute(query, tmp_location_name)
            for row in cursor.fetchall():
                tmp_location_id = row[0]
                tmp_city_id = row[2]
                tmp_slot = row[3]
            disconnectDB(connection)
            
            #Get More Data from DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''SELECT COUNT(*) AS Number FROM bike WHERE Location_ID = %s;'''
            cursor.execute(query, tmp_location_id)
            for row in cursor.fetchall():
                tmp_cur_bike_num = row[0]
            disconnectDB(connection)
            
            #Have available slot
            if tmp_cur_bike_num < tmp_slot:

                #Get More Data from DB
                connection = connectDB()
                cursor = connection.cursor()
                query = '''SELECT ID, Type_Name `Type Name` FROM type WHERE Type_Name = %s;'''
                cursor.execute(query, tmp_type_name)
                for row in cursor.fetchall():
                    tmp_type_id = row[0]
                    disconnectDB(connection)
        
                #Insert Data into DB
                connection = connectDB()
                cursor = connection.cursor()
                query = '''INSERT INTO bike (`Condition`, Location_ID, City_ID, Created_At, Updated_At, Type_ID, Last_Operator_ID) VALUES('Available', %s, %s, NOW(), NOW(), %s, %s);'''
                query_param = (tmp_location_id, tmp_city_id, tmp_type_id, tmp_operator_ID)
                cursor.execute(query, query_param)
                connection.commit()
                disconnectDB(connection)
                result = True
                
            #Not Have available slot
            else:
                msg = "Sorry, no available slot in your selected location."
                result = False
                
        except:
            result = False
        
        if result:
            msg = "Bike is added successfully"
        else:
            if msg == "":
                msg = "Some thing went wrong. Sorry for an inconvenience."
        popupMsg(msg)


class BikeEditPage(tk.Frame):
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
        menu_label = tk.Label(menu_frame, text = "Edit Bike: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)
        
        # BIKE
        #Set bike Name Frame
        bike_name_frame = tk.Frame(self)
        bike_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        bike_name_label = tk.Label(bike_name_frame, text = "Bike Name: ", width = 15, anchor = tk.W)
        bike_name_label.pack(side = tk.LEFT)  
        
        #Get all bike from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT ID FROM bike;'''
        cursor.execute(query)
        bike_list = []
        for row in cursor.fetchall():
            bike_list.append(row)
        disconnectDB(connection)
        
        #Set bike Combobox
        self.var_bike_id = StringVar()
        bike_id_input = ttk.Combobox(bike_name_frame, values = bike_list, state='readonly', textvariable = self.var_bike_id)
        bike_id_input.set('Select Bike')
        # >> Bind onchange event to bike combobox
        bike_id_input.bind("<<ComboboxSelected>>", self.callback)
        bike_id_input.pack(fill = tk.X)
        
        # CONDITION
        #Set Condition Name Frame
        condition_frame = tk.Frame(self)
        condition_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        condition_label = tk.Label(condition_frame, text = "Condition: ", width = 15, anchor = tk.W)
        condition_label.pack(side = tk.LEFT)
        
        condition_list= ["Available", "Broken", "Void"]
        #Set Condition Combobox
        self.var_condition = StringVar()
        condition_input = ttk.Combobox(condition_frame, values = condition_list, state='readonly', textvariable = self.var_condition)
        condition_input.set('Select Condition')
        condition_input.pack(fill = tk.X)
        
        # LOCATION
        #Set location Name Frame
        location_name_frame = tk.Frame(self)
        location_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        location_name_label = tk.Label(location_name_frame, text = "Location Name: ", width = 15, anchor = tk.W)
        location_name_label.pack(side = tk.LEFT)
        
        #Get Location from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT l.ID, l.Zone_Name, c.City_Name
                        FROM location AS l
                        INNER JOIN city AS c ON l.City_ID = c.ID;'''
        cursor.execute(query)
        location_list = []
        for row in cursor.fetchall():
            location_list.append(row[2].upper()+' - '+row[1])
        disconnectDB(connection)
        
        #Set Location Combobox
        self.var_location_name = StringVar()
        location_name_input = ttk.Combobox(location_name_frame, values = location_list, state='readonly', textvariable = self.var_location_name)
        location_name_input.set('Select Location')
        location_name_input.pack(fill = tk.X)
        
        # TYPE
        #Set Type Name Frame
        type_name_frame = tk.Frame(self)
        type_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        type_name_label = tk.Label(type_name_frame, text = "Type Name: ", width = 15, anchor = tk.W)
        type_name_label.pack(side = tk.LEFT)
        
        #Get all Location from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT ID, Type_Name FROM type;'''
        cursor.execute(query)
        type_list = []
        for row in cursor.fetchall():
            type_list.append(row[1])
        disconnectDB(connection)
        
        #Set type Combobox
        self.var_type_name = StringVar()
        type_name_input = ttk.Combobox(type_name_frame, values = type_list, state='readonly', textvariable = self.var_type_name)
        type_name_input.set('Select Type')
        type_name_input.pack(fill = tk.X)
        
        # BUTTON        
        #Set Action Buttion Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        back_button = tk.Button(act_button_frame, text = "Back", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(BikeMngPage))
        back_button.pack(side = tk.RIGHT)
        confirm_button = tk.Button(act_button_frame, text = "Confirm", width = styleDict["buttonWidth"], 
                                command = self.editBike)
        confirm_button.pack(side = tk.RIGHT, fill = tk.X, padx = styleDict["inlinePadding"])
        

    def callback(self, event):
        self.setCurrentLocData()
        
    def setCurrentLocData(self):
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT b.Condition `Condition`, l.Zone_Name `Location Name`, c.City_Name `City Name`, t.Type_Name `Type Name`
                        FROM bike AS b
                        INNER JOIN location AS l ON b.Location_ID = l.ID
                        INNER JOIN city AS c ON b.City_ID = c.ID
                        INNER JOIN type AS t ON b.Type_ID = t.ID
                        WHERE b.ID = %s;'''
        cursor.execute(query, self.var_bike_id.get())
        for row in cursor.fetchall():
            self.var_condition.set(row[0])
            self.var_location_name.set(row[2].upper()+' - '+row[1])
            self.var_type_name.set(row[3])
    
    def editBike(self):
        #Get All Data From User Control
        tmp_bike_id = self.var_bike_id.get()
        
        tmp_condition = self.var_condition.get()
        
        tmp_string = self.var_location_name.get().split(sep=' - ')
        tmp_location_name = tmp_string[1]
        
        tmp_type_name = self.var_type_name.get()
        
        tmp_city_name = tmp_string[0].lower()
        tmp_operator_ID = LoginInfo.loginid[0]
        
        msg = ""

        try:
            #Get More Data from DB
            connection = connectDB()
            cursor = connection.cursor()
            # >> Get Location ID
            query = '''SELECT l.ID, l.Zone_Name, l.City_ID, c.City_Name, l.Slot
                            FROM location AS l
                            INNER JOIN city AS c ON l.City_ID = c.ID
                            WHERE c.City_Name = %s AND l.Zone_Name = %s;'''
            query_params = (tmp_city_name, tmp_location_name)
            cursor.execute(query, query_params)
            for row in cursor.fetchall():
                tmp_location_id = row[0]  
                tmp_city_id = row[2]
                tmp_slot = row[4]
            disconnectDB(connection)

            #Get More Data from DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''SELECT COUNT(*) AS Number FROM bike WHERE Location_ID = %s;'''
            cursor.execute(query, tmp_location_id)
            for row in cursor.fetchall():
                tmp_cur_bike_num = row[0]
            disconnectDB(connection)
            
            #Get More Data from DB
            connection = connectDB()
            cursor = connection.cursor()
            # >> Get Location ID
            query = '''SELECT ID FROM type WHERE `Type_Name` = %s;'''
            cursor.execute(query, tmp_type_name)
            for row in cursor.fetchall():
                tmp_type_id = row[0]  
            disconnectDB(connection)
        
            #Have available slot
            if tmp_cur_bike_num < tmp_slot:   
            
                #Update Data into DB
                connection = connectDB()
                cursor = connection.cursor()
                query = '''UPDATE bike SET `Condition` = %s, `Location_ID` = %s, City_ID = %s, Updated_At = NOW(), Type_ID = %s, Last_Operator_ID = %s WHERE ID = %s;'''
                query_param = (tmp_condition, tmp_location_id, tmp_city_id, tmp_type_id, tmp_operator_ID, tmp_bike_id)
                cursor.execute(query, query_param)
                connection.commit()
                disconnectDB(connection)
                result = True
            #Not Have available slot
            else:
                msg = "Sorry, no available slot in your selected location."
                result = False
                
        except:
            result = False
        
        if result:
            msg = "Bike is updated successfully"
        else:
            if msg == "":
                msg = "Some thing went wrong. Sorry for an inconvenience."
        popupMsg(msg)
        






