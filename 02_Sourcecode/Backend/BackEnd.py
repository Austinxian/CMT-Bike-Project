#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 19:21:48 2019

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
from bike import CMTBikeMng
from location import CMTLocationMng
from biketypes import CMTTypeMng
from city import CMT_CITY
from config import LoginInfo
from report import SalesReport
from role import CMTRoleMng
import os
import sys
from config import LoginInfo, DBConnect

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

class BackEndHomePage(tk.Frame):
    def __init__(self, master):
                
        #Initialize Frame
        tk.Frame.__init__(self, master)

        #Initialize Style Dict
        styleDict = init_styleSheet()
        
        #Display Back End Home Page
        self.logout = tk.Frame(self)
        self.logout.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        lobutton = tk.Button(self.logout, text="Log Out", font=("Arial, 12"), width=8, height=2,
                             command=restart_program)
        lobutton.pack(side=tk.RIGHT)

        h_frame = tk.Frame(self, height = styleDict["topPadding"])
        h_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        title = tk.Label(h_frame, text='CMT-Bike (Staff ONLY)', font=("Arial, 30"))
        title.pack(side=tk.LEFT, padx=30, pady=70)

        menu_frame_1 = tk.Frame(self)
        menu_frame_1.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        a = tk.Button(menu_frame_1, text='City\nManagement', font=("Arial, 25"), width=15, height=4,
                      command=lambda: master.switch_frame(CMT_CITY.CityMngPage))

        a.pack(side=tk.LEFT, padx=30, pady=30)

        b = tk.Button(menu_frame_1, text='Location\nManagement', font=("Arial, 25"), width=15, height=4,
                      command=lambda: master.switch_frame(CMTLocationMng.LocationMngPage))

        b.pack(side=tk.LEFT, padx=30, pady=30)

        c = tk.Button(menu_frame_1, text='Bike\nManagement', font=("Arial, 25"), width=15, height=4,
                      command=lambda: master.switch_frame(CMTBikeMng.BikeMngPage))

        c.pack(side=tk.LEFT, padx=30, pady=30)
        menu_frame_2 = tk.Frame(self)
        menu_frame_2.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])

        d = tk.Button(menu_frame_2, text='Type\nManagement', font=("Arial, 25"), width=15, height=4,
                      command=lambda: master.switch_frame(CMTTypeMng.TypeMngPage))

        d.pack(side=tk.LEFT, padx=30, pady=50)

        IDnum = LoginInfo.loginid[0]
        connection = connectDB()
        cursor = connection.cursor()
        sql = "select Role from operator_manager where id=%s"
        cursor.execute(sql, IDnum)
        s = cursor.fetchone()[0]

        if (s == "Manager"):
            e = tk.Button(menu_frame_2, text='Role\nManagement', font=("Arial, 25"), width=15, height=4,
                          command=lambda: master.switch_frame(CMTRoleMng.RoleMngPage))

            e.pack(side=tk.LEFT, padx=30, pady=50)

            f = tk.Button(menu_frame_2, text='Sales\nReport', font=("Arial, 25"), width=15, height=4,
                          command=lambda: master.switch_frame(SalesReport.ReportMngPage))

            f.pack(side=tk.LEFT, padx=30, pady=50)

def restart_program():
    print(LoginInfo.loginid[0] + 223)
    del LoginInfo.loginid[0]
    python = sys.executable
    os.execl(python, python, *sys.argv)

def connectDB():
    host = 'localhost'
    user = 'root'
    password = DBConnect.password
    db = DBConnect.db
    try:
        connection = pymysql.connect(host, user, password, db)
    # print("Connect to DB Success")
    except pymysql.InternalError as e:
        popupMsg(e)
    # print("Connection Error", e)
    return connection

def popupMsg(msg):
        popup = tk.Tk()
        popup.title(styleDict["Title"])
        msg_label = tk.Label(popup, text=msg)
        msg_label.pack()
        done_button = tk.Button(popup, text="Done", command=popup.destroy)
        done_button.pack()
        popup.mainloop()