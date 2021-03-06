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
from PIL import Image, ImageTk

#import other pages
from config import LoginInfo, DBConnect
from select_qr import select_qr
from transaction import CMTMyRentalHistory
from account import Account
from trip import StartTrip
import os
import sys

def init_styleSheet():
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
    styleDict = init_styleSheet()
    popup = tk.Tk()
    popup.title(styleDict["Title"])
    msg_label = tk.Label(popup, text = msg)
    msg_label.pack()
    done_button = tk.Button(popup, text="Done", command = popup.destroy)
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

class ReportProblemPage(tk.Frame):
    #Cannot cancel if (1) No "In Progress" Transaction (2) 15 Min Passed
    def canCancel(self):
        #Get Current Transaction ID
        connection = connectDB()
        cursor = connection.cursor()
        customer_id = LoginInfo.loginid[0]
        query = '''SELECT t.ID, t.`Status`, c.Username, t.Origin_ID, t.Created_At, DATEDIFF(NOW(),t.Created_At) AS DATE_DIFF, ((HOUR(TIMEDIFF(NOW(), t.Created_At))*60)+MINUTE(TIMEDIFF(NOW(), t.Created_At))) AS TIME_DIFF 
                FROM transaction t
                INNER JOIN customer c ON t.Customer_ID = c.ID
                WHERE t.Customer_ID = %s AND t.`Status` = "In Progress"
                HAVING DATE_DIFF = 0 AND TIME_DIFF <= 15 ;'''
        cursor.execute(query, customer_id)
        if cursor.rowcount == 0:
            return False
        else:
            return True
    
    def __init__(self, master):
        
        #Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill = tk.BOTH, expand = True)
        
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

        menu_label = tk.Label(menu_frame, text = "Report a Problem: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)
        
        #Check can cancel or not
        can_cancel = self.canCancel()
        
        #Cannot cancel
        if not can_cancel:
            #Set Menu Description Frame
            menu_description_frame = tk.Frame(self)
            menu_description_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
            menu_description_label = tk.Label(menu_description_frame, text = "Sorry, you don't have a valid transaction to cancel.", font = ('Arial', 14), anchor = tk.W)
            menu_description_label.pack(side = tk.LEFT)
            
            #Set Action Buttion Frame
            act_button_frame = tk.Frame(self)
            act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
            back_button = tk.Button(act_button_frame, text = "Back", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(select_qr.QRPage))
            back_button.pack(side = tk.RIGHT)
            
        #Can cancel
        else:
            #Set Menu Description Frame
            menu_description_frame = tk.Frame(self)
            menu_description_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
            menu_description_label = tk.Label(menu_description_frame, text = "Please select the broken part(s) of a bike. ", font = ('Arial', 14), anchor = tk.W)
            menu_description_label.pack(side = tk.LEFT)
            
            #Set Defective Parts Frame
            one_df_part_frame = tk.Frame(self)
            one_df_part_frame.pack(fill = tk.X, padx = styleDict["xPadding"]+200, pady = styleDict["yPadding"])
            self.var_seat = StringVar()
            self.var_seat.set(False)
            seat_chkbtn = tk.Checkbutton(one_df_part_frame, text = "Seat", variable = self.var_seat)
            seat_chkbtn.pack(side = tk.LEFT)
            self.var_lock = StringVar()
            self.var_lock.set(False)
            lock_chkbtn = tk.Checkbutton(one_df_part_frame, text = "Lock", variable = self.var_lock)
            lock_chkbtn.place(x = 300)
        
            two_df_part_frame = tk.Frame(self)
            two_df_part_frame.pack(fill = tk.X, padx = styleDict["xPadding"]+200, pady = styleDict["yPadding"])
            self.var_brake = StringVar()
            self.var_brake.set(False)
            brake_chkbtn = tk.Checkbutton(two_df_part_frame, text = "Brake", variable = self.var_brake)
            brake_chkbtn.pack(side = tk.LEFT)
            self.var_chain = StringVar()
            self.var_chain.set(False)
            chain_chkbtn = tk.Checkbutton(two_df_part_frame, text = "Chain", variable = self.var_chain)
            chain_chkbtn.place(x = 300)

            three_df_part_frame = tk.Frame(self)
            three_df_part_frame.pack(fill = tk.X, padx = styleDict["xPadding"]+200, pady = styleDict["yPadding"])
            self.var_pedal = StringVar()
            self.var_pedal.set(False)
            pedal_chkbtn = tk.Checkbutton(three_df_part_frame, text = "Pedal", variable = self.var_pedal)
            pedal_chkbtn.pack(side = tk.LEFT)
            self.var_tire = StringVar()
            self.var_tire.set(False)
            tire_chkbtn = tk.Checkbutton(three_df_part_frame, text = "Tire    ", variable = self.var_tire)
            tire_chkbtn.place(x = 300)
        
            four_df_part_frame = tk.Frame(self)
            four_df_part_frame.pack(fill = tk.X, padx = styleDict["xPadding"]+200, pady = styleDict["yPadding"])
            self.var_light = StringVar()
            self.var_light.set(False)
            light_chkbtn = tk.Checkbutton(four_df_part_frame, text = "Light", variable = self.var_light)
            light_chkbtn.pack(side = tk.LEFT)
            self.var_other = StringVar()
            self.var_other.set(False)
            other_chkbtn = tk.Checkbutton(four_df_part_frame, text = "Other:", variable = self.var_other)
            other_chkbtn.place(x = 300)
            self.var_other_desc = StringVar()
            other_desc_input = tk.Entry(four_df_part_frame, text = "", textvariable = self.var_other_desc)
            other_desc_input.place(x = 380)

            #Set Action Buttion Frame
            act_button_frame = tk.Frame(self)
            act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
            back_button = tk.Button(act_button_frame, text = "Back", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(StartTrip.StartTripPage))
            back_button.pack(side = tk.RIGHT)
            report_button = tk.Button(act_button_frame, text = "Report", width = styleDict["buttonWidth"], 
                                command = self.reportProblem)
            report_button.pack(side = tk.RIGHT, fill = tk.X, padx = styleDict["inlinePadding"])
        
    def reportProblem(self):
        
        #Get All Defective Part
        defective_part = "Defective Part: "
        if self.var_seat.get() == "1":
            defective_part = defective_part + "[Seat] "
        if self.var_lock.get() == "1":
            defective_part = defective_part + "[Lock] "
        if self.var_brake.get() == "1":
            defective_part = defective_part + "[Brake] "
        if self.var_chain.get() == "1":
            defective_part = defective_part + "[Chain] "
        if self.var_pedal.get() == "1":
            defective_part = defective_part + "[Pedal] "
        if self.var_tire.get() == "1":
            defective_part = defective_part + "[Tire] "
        if self.var_light.get() == "1":
            defective_part = defective_part + "[Light] "
        if self.var_other_desc.get() != "":
            defective_part = defective_part + "[Other-" + self.var_other_desc.get() + "]"
        try:
            #Get Current Transaction ID
            connection = connectDB()
            cursor = connection.cursor()
            # >> Need to update Customer ID from log-in
            query = '''SELECT t.ID, t.`Status`, c.Username, t.Origin_ID
                    FROM transaction t
                    INNER JOIN customer c ON t.Customer_ID = c.ID
                    WHERE t.Customer_ID = 1 AND t.`Status` = "In Progress";'''
            cursor.execute(query)
            for row in cursor.fetchall():
                current_trans_ID = row[0]
                tmp_origin_id = row[3]
            disconnectDB(connection)
        
            #Cancel Current Transaction and Log Defective Parts
            connection = connectDB()
            cursor = connection.cursor()
            query = '''UPDATE transaction SET `Status` = "Cancelled", Paid_Amount = 0, Updated_At = NOW(), Remarks = %s, Destination_ID = %s WHERE ID = %s;'''
            query_param = (defective_part, tmp_origin_id, current_trans_ID)
            cursor.execute(query, query_param)
            connection.commit()
            disconnectDB(connection)
            result = True
        except:
            result = False
        
        if result:
            self.master.switch_frame(CompletedReportProblemPage)
        else:
            popupMsg("Something went wrong, please contact the administrator.")

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
        
        
class CompletedReportProblemPage(tk.Frame):
    def __init__(self, master):
        
        #Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill = tk.BOTH, expand = True)
        
        styleDict = init_styleSheet()
        
        #Set Header Frame
        h_frame = tk.Frame(self, width=204, height=58)
        h_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        self.pilImage2 = Image.open('select_qr/frontend-3.png')
        self.tkImage2 = ImageTk.PhotoImage(self.pilImage2)
        home = tk.Label(h_frame, text="Home", image=self.tkImage2)
        home.pack(side=tk.LEFT)

        #Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])

        menu_label = tk.Label(menu_frame, text = "Report a Problem: ", font = ('Arial', 18), anchor = tk.W)
        menu_label.pack(side = tk.LEFT)
        
        #Set Body Description Frame
        body_description_frame = tk.Frame(self)
        body_description_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        body_description_label = tk.Label(body_description_frame, text = "Thank you for reporting the defect. \n We will look into your issue and contact you soon.", font = ('Arial', 14), anchor = tk.W)
        body_description_label.pack()
        
        #Set Action Buttion Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        home_button = tk.Button(act_button_frame, text = "Home", width = styleDict["buttonWidth"], 
                                command = lambda: master.switch_frame(select_qr.QRPage))
        home_button.pack()
