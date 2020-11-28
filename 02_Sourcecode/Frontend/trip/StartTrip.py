# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 16:12:58 2019

@author: FlyingPIG
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:59:32 2019

@author: FlyingPIG
"""
# import libraries
import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import pymysql
from pandastable import Table, TableModel
import time
import sys
import time, datetime;

#import other pages
from config import LoginInfo, DBConnect
from report_bike import CMTReportProblem
from trip import EndTrip
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
    return (styleDict)


def popupMsg(msg):
    popup = tk.Tk()
    popup.title(styleDict["Title"])
    msg_label = tk.Label(popup, text=msg)
    msg_label.pack()
    done_button = tk.Button(popup, text="Done", command=popup.destroy)
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

class StartTripPage(tk.Frame,threading.Thread):

    def __init__(self, master):
        # Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=True)
        
        # Initialize Thread
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

        # Initialize Time
        self.starttime = time.time() 
        self.endtime = time.time()

        # Initialize Style Dict
        styleDict = init_styleSheet()
           
        # Set Header Frame
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
        # Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])

        menu_label = tk.Label(menu_frame, text="My Current Bike:", font=('Arial', 18), anchor=tk.W)
        menu_label.pack(side=tk.LEFT)
        
        #Create New transation
        self.start_transaction()
        
        #Need to read data from global variable
        tmp_customer_id = LoginInfo.loginid[0]
        
        #Select Current Transaction Value
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT t.Bike_ID, tp.Fixed_Price, tp.Add_Price, tp.Day_Price, t.Created_At, l.Zone_Name, TIMEDIFF(CURRENT_TIMESTAMP,t.Created_At) AS Time_Duration
                    FROM `transaction` t
                    INNER JOIN location l ON t.Origin_ID = l.ID
                    INNER JOIN bike b ON b.ID = t.Bike_ID
                    INNER JOIN type tp ON tp.ID = b.Type_ID
                    	WHERE t.`Status` = "In Progress" AND t.Customer_ID = %s;'''
        
        cursor.execute(query, tmp_customer_id)
        
        
        for row in cursor.fetchall():
            tmp_bike_id = row[0]
            tmp_fixed_price = row[1]
            tmp_add_price = row[2]
            tmp_day_price = row[3]
            tmp_start_time = str(row[4])
            tmp_location_name = row[5]
            self.tmp_time_duration = str(row[6])
        disconnectDB(connection)
        
        #print("tmp_start_time: " + tmp_start_time)
        #print("self.tmp_time_duration: " + self.tmp_time_duration)
        
        # BIKE ID
        #Set BIKE ID Frame
        bike_id_frame = tk.Frame(self)
        bike_id_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        bike_id_label = tk.Label(bike_id_frame, text = "BIKE ID:", width = styleDict["labelLen"], anchor = tk.W) 
        bike_id_label.pack(side = tk.LEFT)
        
        self.var_bike_id_get = StringVar()
        self.var_bike_id_get.set(tmp_bike_id)
        bike_id_get_frame = tk.Frame(self)
        bike_id_get_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        bike_id_get_label = tk.Label(bike_id_frame, text = self.var_bike_id_get.get(), width = styleDict["labelLen"], anchor = tk.W) 
        bike_id_get_label.pack(side = tk.LEFT)

        # Price Rate
        #Set FullName Frame
        price_rate_frame = tk.Frame(self)
        price_rate_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        price_rate_label = tk.Label(price_rate_frame, text = "Price Rate:", width = styleDict["labelLen"], anchor = tk.W) 
        price_rate_label.pack(side = tk.LEFT)
        
        
        tmp_price = "First 15 min: Free   /   Fist 2 Hours: " + str(tmp_fixed_price) + "  £/hr.   /   Next Hours: " + str(tmp_add_price) + "  £/hr.   /   Day Rate: " +  str(tmp_day_price) + "  £/hr."
        self.var_price_rate_get = StringVar()
        self.var_price_rate_get.set(tmp_price)
        price_rate_get_frame = tk.Frame(self)
        price_rate_get_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        price_rate_get_label = tk.Label(price_rate_frame, text = self.var_price_rate_get.get(), anchor = tk.W) 
        price_rate_get_label.pack(side = tk.LEFT)
        
        # Starting Time
        #Set FullName Frame
        starting_time_frame = tk.Frame(self)
        starting_time_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        starting_time_label = tk.Label(starting_time_frame, text = "Starting Time:", width = styleDict["labelLen"], anchor = tk.W) 
        starting_time_label.pack(side = tk.LEFT)
        
        self.var_starting_time_get = StringVar()
        self.var_starting_time_get.set(tmp_start_time)
        starting_time_get_frame = tk.Frame(self)
        starting_time_get_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        starting_time_get_label = tk.Label(starting_time_frame, text = self.var_starting_time_get.get(), anchor = tk.W) 
        starting_time_get_label.pack(side = tk.LEFT)
        
        # Starting Station
        #Set FullName Frame
        starting_station_frame = tk.Frame(self)
        starting_station_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        starting_station_label = tk.Label(starting_station_frame, text = "Starting Station:", width = styleDict["labelLen"], anchor = tk.W) 
        starting_station_label.pack(side = tk.LEFT)
        
        self.var_starting_station_get = StringVar()
        self.var_starting_station_get.set(tmp_location_name)
        starting_station_get_frame = tk.Frame(self)
        starting_station_get_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        starting_station_get_label = tk.Label(starting_station_frame, text = self.var_starting_station_get.get(), width = styleDict["labelLen"], anchor = tk.W) 
        starting_station_get_label.pack(side = tk.LEFT)

        # Time Duration
        #Set FullName Frame
        time_duration_frame = tk.Frame(self)
        time_duration_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        time_duration_label = tk.Label(time_duration_frame, text = "Time Duration:", width = styleDict["labelLen"], anchor = tk.W) 
        time_duration_label.pack(side = tk.LEFT)

        var_time_duration_label = tk.Label(time_duration_frame, text = self.tmp_time_duration, width = styleDict["labelLen"], anchor = tk.W) 
        var_time_duration_label.pack(side = tk.LEFT)
        
        # BUTTON
        # Set End Trip Buttion Frame
        action_button_frame = tk.Frame(self)
        action_button_frame.pack(padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        end_trip_button = tk.Button(action_button_frame, text="End the trip", width=20,command = lambda: master.switch_frame(EndTrip.ReturnBikePage))
        end_trip_button.pack()

        # Set Report Buttion Frame            
        report_a_problem_button = tk.Button(action_button_frame, text="Report a Problem", width=20,command = lambda: master.switch_frame(CMTReportProblem.ReportProblemPage))
        report_a_problem_button.pack(padx=styleDict["inlinePadding"])
        

    def start_transaction(self):
        connection = connectDB()
        cursor = connection.cursor()
        
        #Need to read data from global variable
        tmp_customer_id = LoginInfo.loginid[0]
        
        
        
        #Check Are there any In Progress transaction
        num = 0
        query = '''SELECT ID FROM transaction where Status = "In Progress" AND Customer_ID = %s;'''
        cursor.execute(query, tmp_customer_id)
        for row in cursor.fetchall():
            num += 1
        
        #Create New Transaction
        if num == 0:
            #Query Bike Origin ID
            tmp_bike_id = LoginInfo.bikeid[0]
            query = '''SELECT Location_ID FROM bike where id = %s;'''
            cursor.execute(query, tmp_bike_id)
            for row in cursor.fetchall():
                tmp_location_id = row[0]
            
            #Insert new transaction
            query = '''INSERT INTO transaction (Status, Created_At, Updated_At, Customer_ID, Bike_ID, Origin_ID)
                        VALUES("In Progress", NOW(), NOW(), %s, %s, %s);'''
            query_param = (tmp_customer_id, tmp_bike_id, tmp_location_id)
            cursor.execute(query, query_param)
            connection.commit()
            disconnectDB(connection)

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
