#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:59:32 2019

@author: FlyingPIG
"""
#import libraries
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import pymysql
from pandastable import Table, TableModel

#import other pages
from config import LoginInfo, DBConnect
from trip import StartTrip
from select_qr import select_qr
import os
import sys
from account import Account
from transaction import CMTMyRentalHistory

def init_styleSheet():
    global styleDict 
    styleDict = {}
    styleDict["Title"] = "CMT - Bike"
    styleDict["windowSize"] = "1024x768"
    styleDict["windowWidth"] = 1024
    styleDict["windowHeight"] = 768
    styleDict["labelLen"] = 20
    styleDict["xPadding"] = 20
    styleDict["yPadding"] = 5
    styleDict["inlinePadding"] = 5
    styleDict["topPadding"] = 150
    styleDict["fontColor"] = "white"
    styleDict["fontType"] = "Arial"
    styleDict["fontSize"] = "18"
    styleDict["fontStyle"] = "bold"
    styleDict["buttonWidth"] = 10
    styleDict["TabHeaderFgColor"] = "white"
    styleDict["TabHeaderBgColor"] = "#4B96E9"
    return(styleDict)

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
    except pymysql.InternalError as e:
        popupMsg(e)
    return connection

def disconnectDB(connection):
    connection.close()

class ReturnBikePage(tk.Frame):
    def __init__(self, master):
        
        #Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill = tk.BOTH, expand = True)
        
        #Initialize Style Dict
        styleDict = init_styleSheet()
        
        #Set Header Frame
        h_frame = tk.Frame(self, width=204, height=58)
        h_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        home_button = tk.Button(h_frame, text="Home", width=15, command=lambda: master.switch_frame(select_qr.QRPage))
        home_button.pack(side=tk.LEFT)
        logout_button = tk.Button(h_frame, text="Log Out", width=15, command=self.restart_program)
        logout_button.pack(side=tk.RIGHT)
        myrental_button = tk.Button(h_frame, text="My Rental", width=15,
                                    command=lambda: master.switch_frame(CMTMyRentalHistory.MyRentalHistoryPage))
        myrental_button.pack(side=tk.RIGHT)
        myaccount_button = tk.Button(h_frame, text="My Account", width=15,
                                     command=lambda: master.switch_frame(Account.AccountMngPage))
        myaccount_button.pack(side=tk.RIGHT)
        
        #Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        menu_label = tk.Label(menu_frame, text = "Which location return to？", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack()
        
        # LOCATION
        #Set location Name Frame
        location_name_frame = tk.Frame(self)
        location_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        location_name_label = tk.Label(location_name_frame, text = "Location Name: ", width = styleDict["labelLen"], anchor = tk.W)
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
        location_name_input.bind("<<ComboboxSelected>>", self.callback)
        location_name_input.pack(fill = tk.X)
        
        # CITY
        #Set location Name Frame
        city_name_frame = tk.Frame(self)
        city_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        city_name_label = tk.Label(city_name_frame, text = "City Name: ", width = styleDict["labelLen"], anchor = tk.W)
        city_name_label.pack(side = tk.LEFT)
        
        self.var_city_name = StringVar()
        self.var_city_name.set("City")
        city_name_input = tk.Entry(city_name_frame, textvariable = self.var_city_name, state='readonly')
        city_name_input.pack(fill = tk.X)
        
        # BUTTON        
        #Set Action Buttion Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        self.back_button = tk.Button(act_button_frame, text = "Back", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(StartTrip.StartTripPage))
        self.back_button.pack(side = tk.RIGHT)
        self.confirm_button = tk.Button(act_button_frame, text = "Confirm", width = styleDict["buttonWidth"], 
                                command = self.endtrip)
        self.confirm_button.pack(side = tk.RIGHT, fill = tk.X, padx = styleDict["inlinePadding"])
        
    def callback(self, event):
        self.setCurrentCityData()
        
    def setCurrentCityData(self):
        test_string = self.var_location_name.get().split(sep=' - ') 
        self.var_city_name.set(test_string[0])
        
    def endtrip(self):

        tmp_string = self.var_location_name.get().split(sep=' - ')
        tmp_city_name = tmp_string[0]
        tmp_location_name = tmp_string[1]
        
        
        #Get tmp customer ID
        tmp_customer_id = LoginInfo.loginid[0]

        msg = ""

        try:
            #print("END TRIP")
            connection = connectDB()
            cursor = connection.cursor()
            # >> Get Destination Location ID
            query = '''SELECT l.ID, l.Zone_Name, l.City_ID, c.City_Name, l.Slot
                            FROM location AS l
                            INNER JOIN city AS c ON l.City_ID = c.ID
                            WHERE c.City_Name = %s AND l.Zone_Name = %s;'''
            query_params = (tmp_city_name, tmp_location_name)
            cursor.execute(query, query_params)
            for row in cursor.fetchall():
                tmp_location_id = row[0]  
                tmp_slot = row[4]
                
            #print("tmp_slot")
            #print(tmp_slot)
            
            query = '''SELECT TIMEDIFF(CURRENT_TIMESTAMP,Created_At) AS TM_DIFF, HOUR(TIMEDIFF(CURRENT_TIMESTAMP,Created_At))/24 AS DAY, `transaction`.Bike_ID
                    FROM `transaction` WHERE Customer_ID = %s AND `Status` = "In Progress";'''
            cursor.execute(query, tmp_customer_id)
            for row in cursor.fetchall():
                tmp_dttm = str(row[0])
                tmp_day = int(row[1])
                tmp_bike_id = row[2]
            
            # >> Get Paid Amount
            query = '''SELECT t.ID, t.Fixed_Price, t.Add_Price, t.Day_Price
                                FROM Type AS t
                                INNER JOIN bike AS b ON b.Type_ID = t.ID
                                WHERE b.ID = %s;'''
            cursor.execute(query, tmp_bike_id)
            for row in cursor.fetchall():
                tmp_fixed_price = row[1]
                tmp_add_price = row[2]
                tmp_day_price = row[3]
                

            
            disconnectDB(connection)
            
            #print("tmp_dttm")
            #print(tmp_dttm)
                        
            #Not overnight
            if tmp_dttm.find("day") == -1:
                print("not find")
                list_dttm = tmp_dttm.split(":")
                tmp_hour = int(list_dttm[0])
                tmp_min = int(list_dttm[1])
            #Overnight
            else:
                print("find")
                list_dttm = tmp_dttm.split(" ")
                str_tm = list_dttm[2]
                list_tm = str_tm.split(":")
                tmp_hour = int(list_tm[0])
                tmp_min = int(list_tm[1])
                
            #Calculate paid amount
            total_amt = 0
            #Free of charge
            if tmp_day == 0 and tmp_hour == 0 and tmp_min <= 15:
                total_amt = 0
            else:
                total_amt = total_amt + (tmp_day*tmp_day_price)
                if tmp_min >= 0:
                    tmp_hour += 1
                total_amt = total_amt + (2*tmp_fixed_price)
                if tmp_hour > 2:
                    total_amt = total_amt + ((tmp_hour-2)*tmp_add_price)

            #print("total_amt")
            #print(total_amt)

            #print("tmp_location_id")
            #print(tmp_location_id)

            #Get Number of current bike
            connection = connectDB()
            cursor = connection.cursor()
            query = '''SELECT COUNT(*) AS Number FROM bike WHERE Location_ID = %s;'''
            cursor.execute(query, tmp_location_id)
            for row in cursor.fetchall():
                tmp_cur_bike_num = row[0]
            disconnectDB(connection)
                
            #print("tmp_cur_bike_num")
            #print(tmp_cur_bike_num)
            
            #Have available slot
            if tmp_cur_bike_num < tmp_slot:    
                #Update Data into DB
                #print("Have Slot")
                connection = connectDB()
                cursor = connection.cursor()
                query = '''UPDATE transaction SET Status = "Paid", Paid_Amount = %s, Updated_At = NOW(), Destination_ID = %s WHERE Customer_ID = %s AND Status = "In Progress";'''
                query_param = (total_amt, tmp_location_id, tmp_customer_id)
                cursor.execute(query, query_param)
                connection.commit()
                disconnectDB(connection)
                result = True
            else:
                msg = "Sorry, this location is not available for return. Please select a new one."
                result = False
        except:
            result = False
        if result:
            msg = "THANK YOU for using CMT-Bike.We hope that you have wonderful experience with us."
            self.confirm_button['state'] = 'disabled'
            self.back_button['state'] = 'disabled'
        else:
            if msg == "":
                msg = "Some thing went wrong. Sorry for an inconvenience"
        popupMsg(msg)
        

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)


