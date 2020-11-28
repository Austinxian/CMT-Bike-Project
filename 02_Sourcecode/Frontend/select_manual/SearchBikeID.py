"""
Created on Sun Nov  3 22:34:25 2019

@author: wang
"""
#import libraries
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import pymysql
import tkinter.font as tkFont

#import other pages
from config import LoginInfo, DBConnect
from transaction import CMTMyRentalHistory
from select_manual import SearchBikeID
from account import Account
from select_qr import select_qr
from trip import StartTrip
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

def popupMsg(msg):
        popup = tk.Tk()
        popup.title(styleDict["Title"])
        msg_label = tk.Label(popup, text=msg)
        msg_label.pack()
        done_button = tk.Button(popup, text="continue", command=popup.destroy)
        done_button.pack()
        popup.mainloop()

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


class SearchBikeID(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        styleDict = init_styleSheet()
        self.pack(fill=tk.BOTH, expand=True)

        h_frame = tk.Frame(self, width = 204, height = 58)
        h_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        home_button = tk.Button(h_frame, text="Home", width=15, command=lambda: master.switch_frame(select_qr.QRPage))
        home_button.pack(side=tk.LEFT)
        logout_button = tk.Button(h_frame, text="Log Out", width=15, command=self.restart_program)
        logout_button.pack(side=tk.RIGHT)
        myrental_button = tk.Button(h_frame, text="My Rental", width=15, command=lambda: master.switch_frame(CMTMyRentalHistory.MyRentalHistoryPage))
        myrental_button.pack(side=tk.RIGHT)
        myaccount_button = tk.Button(h_frame, text="My Account", width=15, command=lambda: master.switch_frame(Account.AccountMngPage))
        myaccount_button.pack(side=tk.RIGHT)

#Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])

        menu_label = tk.Label(menu_frame, text = "Reserve a Bike: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)


        self.citytext = tk.Frame(self)
        self.citytext.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        city = tk.Label(self.citytext, text = 'City:', font = ("Arial, 15"))
        city.pack(side = tk.LEFT, pady=10)

        self.city_list = []
        self.loc_list = []
        self.bike_list = []
        

        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT `City_Name` FROM city WHERE Status = "Active" ORDER BY City_Name;'''
        cursor.execute(query)
        for row in cursor.fetchall():
            self.city_list.append(row[0])
        disconnectDB(connection)

        self.citybox = tk.Frame(self)
        self.citybox.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        self.citycombo = ttk.Combobox(self.citybox, width=50)
        # >> Bind onchange event to city combobox
        self.citycombo.bind("<<ComboboxSelected>>", self.callback_loc)
        self.citycombo.pack(fill = tk.X)
        self.citycombo['values'] = self.city_list
        self.citycombo.set('Select City')
        self.citycombo.pack(side=tk.TOP)
        

        self.zonetext = tk.Frame(self)
        self.zonetext.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        self.zone = tk.Label(self.zonetext, text = 'Location:', font = ("Arial, 15"))
        self.zone.pack(side = tk.LEFT, pady=10)

        self.zonebox = tk.Frame(self)
        self.zonebox.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        self.zonecombo = ttk.Combobox(self.zonebox, width=50)
        # >> Bind onchange event to location combobox
        self.zonecombo.bind("<<ComboboxSelected>>", self.callback_bike)
        self.zonecombo.pack(fill = tk.X)
        self.zonecombo['values'] = self.loc_list
        #self.zonecombo.set('Select Location')
        self.zonecombo.pack(side=tk.TOP)

        

        self.bikeIDtext = tk.Frame(self)
        self.bikeIDtext.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        self.BikeID = tk.Label(self.bikeIDtext, text = 'Bike ID:', font = ("Arial, 15"))
        self.BikeID.pack(side = tk.LEFT, pady=10)

        self.bikeidbox = tk.Frame(self)
        self.bikeidbox.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        self.BikeIDcombo = ttk.Combobox(self.bikeidbox, width=50)
        self.BikeIDcombo['values'] = self.bike_list
        # >> Bind onchange event to location combobox
        self.BikeIDcombo.bind("<<ComboboxSelected>>", self.callback_reserve)
        #self.BikeIDcombo.set('Select Bike')
        self.BikeIDcombo.pack(fill = tk.X)
        self.BikeIDcombo.pack(side=tk.TOP)

        self.confirmframe = tk.Frame(self)
        self.confirmframe.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        confirm = tk.Button(self.confirmframe, text = 'Reserved',font = ("Arial, 28"), width=10, height=2, command=lambda: master.switch_frame(StartTrip.StartTripPage))
        self.confirmframe.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        confirm.pack(side=tk.TOP, pady=30)
        self.textframe = tk.Frame(self, height=styleDict["topPadding"])
        self.textframe.pack(fill=tk.X, padx=styleDict["xPadding"], pady=20)
        text = tk.Label(self.textframe, text="Return to the previous page ", font=("Arial", "15", "underline"), fg="blue")
        text.pack(pady=10)
        text.bind("<Button-1>", lambda event: master.switch_frame(select_qr.QRPage))

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
    
    def callback_loc(self, event):
        connection = connectDB()
        cursor = connection.cursor()
        
        tmp_customer_id = LoginInfo.loginid[0]
        
        #Check Are there any In Progress transaction
        num = 0
        query = '''SELECT ID FROM transaction where Status = "In Progress" AND Customer_ID = %s;'''
        cursor.execute(query, tmp_customer_id)
        for row in cursor.fetchall():
            num += 1
            
        #Create New Transaction
        if num == 0:
            query = '''SELECT l.Zone_Name FROM location l
                    INNER JOIN city c ON l.City_ID = c.ID
                    WHERE l.`Status` = "Active" AND c.`Status` = "Active" AND c.City_Name = %s
                    ORDER BY l.Zone_Name;'''
            query_param = (self.citycombo.get())
            cursor.execute(query, query_param)
            self.loc_list = []
            for row in cursor.fetchall():
                self.loc_list.append(row[0])
            self.zonecombo['values'] = self.loc_list
            self.zonecombo.set('Select Location')
        else:
            msg = "Please return the previous bike before renting a new one."
            popupMsg(msg)
        disconnectDB(connection)
        
        
    def callback_bike(self, event):
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT b.ID FROM location l
                INNER JOIN city c ON l.City_ID = c.ID
                INNER JOIN bike b ON b.Location_ID = l.ID
                WHERE b.`Condition` = "Available" AND c.City_Name = %s AND l.Zone_Name = %s
                ORDER BY b.ID;'''
        query_param = (self.citycombo.get(), self.zonecombo.get())
        cursor.execute(query, query_param)
        self.bike_list = []
        for row in cursor.fetchall():
            self.bike_list.append(row[0])
        disconnectDB(connection)
        self.BikeIDcombo['values'] = self.bike_list
        self.BikeIDcombo.set('Select Bike')
        
    def callback_reserve(self, event):
        LoginInfo.bikeid.clear()
        LoginInfo.bikeid.append(self.BikeIDcombo.get())
