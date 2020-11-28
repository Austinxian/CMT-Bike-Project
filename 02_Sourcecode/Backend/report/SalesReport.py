#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 11:08:40 2019
@author: Melissa
"""
#import libraries
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import pymysql
# Provides classic Python interface
from matplotlib import pyplot as plt
# Handle Dates
import matplotlib.dates as mdates  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import array

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
    styleDict["TabHeaderFgColor"] = "#FFFFFF"
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
    
class ReportMngPage(tk.Frame):
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
        
        # Select City Name Frame
        city_name_frame = tk.Frame(self)
        city_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        city_name_label = tk.Label(city_name_frame, text = "Sales Report by City: ", width = 25, anchor = tk.W)
        city_name_label.pack(side = tk.LEFT)
        
        #Get City Name from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT City_Name `City Name` FROM city ORDER BY City_Name;'''
        cursor.execute(query)
        city_list = []
        for row in cursor.fetchall():
            city_list.append(row)
        disconnectDB(connection)
        
        self.var_status = tk.StringVar()
        self.var_status.set("Paid")

        self.var_city_name = tk.StringVar()
        city_name_input = ttk.Combobox(city_name_frame, values = city_list, state='readonly', textvariable = self.var_city_name)
        city_name_input.bind("<<ComboboxSelected>>", self.callback)
        #city_name_input.insert(0, 'Select City')
        city_name_input.pack(fill = tk.X)
        
    def callback(self, event):
        connection = connectDB()
        print("Database")
        cursor = connection.cursor()
        print("Cursor")
        query = '''SELECT CAST(SUM(trans.`Paid_Amount`) AS CHAR) AS Amount,  
						CONCAT(YEAR(trans.Updated_At), "-", MONTH(trans.Updated_At)) AS YR_MN, trans.Origin_ID, l.City_ID
                        FROM transaction AS trans
    				INNER JOIN location AS l ON trans.Origin_ID=l.ID
    				INNER JOIN city AS c ON l.City_ID=c.ID
    				WHERE c.City_Name=%s AND trans.Status=%s
                    GROUP BY trans.Origin_ID, l.City_ID, YR_MN
    				ORDER BY YR_MN;'''
        query_params = (self.var_city_name.get(), self.var_status.get())
        cursor.execute(query, query_params)
        
        # Initialise 2 arrays
        self.arr_x = []
        self.arr_y = []
        
        # Store Data
        for row in cursor.fetchall():
            self.arr_x.append(row[1])
            self.arr_y.append(row[0])
        disconnectDB(connection)
        
        print(self.arr_x)
        print(self.arr_y)
        # Changing List into NumPy Array
        x = np.array(self.arr_x)
        y = np.array(self.arr_y)
        
        # Plot
        plt.plot(x, y)
        plt.xlabel("Time")
        plt.ylabel("Sales")
        plt.show()
        
