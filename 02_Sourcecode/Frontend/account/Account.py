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
from config import LoginInfo, DBConnect
from select_qr import select_qr
from transaction import CMTMyRentalHistory
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
    
class AccountMngPage(tk.Frame):
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
                                     command=lambda: master.switch_frame(AccountMngPage))
        myaccount_button.pack(side=tk.RIGHT)

        # --------------------------------------------------------------------------------------------
        # Section 1: User Profile Details
        # --------------------------------------------------------------------------------------------
        self.var_username = StringVar()
        self.var_name = StringVar()
        self.var_phone = StringVar()
        self.var_email = StringVar()
        self.var_card_no = StringVar()
        self.var_date = StringVar()
        self.var_cvv = StringVar()

        connection = connectDB()
        cursor = connection.cursor()
        customer_ID = LoginInfo.loginid[0]
        print(customer_ID)
        query = '''SELECT Username, Phone_Number, Full_Name, Email, Card_No, Expired_Date, CVV
                    FROM customer WHERE ID=%s;'''
        cursor.execute(query, customer_ID)

        for row in cursor.fetchall():
            self.var_username.set(row[0])
            self.var_phone.set(row[1])
            self.var_name.set(row[2])
            self.var_email.set(row[3])
            self.var_card_no.set(row[4])
            self.var_date.set(row[5])
            self.var_cvv.set(row[6])

        # Profile Picture [Fixed] + Username
        username_frame = tk.Frame(self)
        username_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])

        username_label = tk.Label(username_frame, text = "Username: ", width = styleDict["labelLen"], anchor = tk.W)
        username_label.pack(side = tk.LEFT)
        username_input = tk.Label(username_frame, textvariable = self.var_username)
        username_input.pack(side = tk.LEFT)


        # Full Name
        name_frame = tk.Frame(self)
        name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        name_label = tk.Label(name_frame, text = "Full Name: ", width = styleDict["labelLen"], anchor = tk.W)
        name_label.pack(side = tk.LEFT)
        name_input = tk.Label(name_frame, textvariable=self.var_name)
        name_input.pack(side=tk.LEFT)
        
        # Phone Number
        phone_frame = tk.Frame(self)
        phone_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        #self.var_phone = StringVar()
        phone_label = tk.Label(phone_frame, text = "Phone No.: ", width = styleDict["labelLen"], anchor = tk.W)
        phone_label.pack(side = tk.LEFT)
        phone_input = tk.Entry(phone_frame, textvariable = self.var_phone)
        phone_input.pack(fill = tk.X)
        
        # Email
        email_frame = tk.Frame(self)
        email_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        #self.var_email = StringVar()
        email_label = tk.Label(email_frame, text = "Email: ", width = styleDict["labelLen"], anchor = tk.W)
        email_label.pack(side = tk.LEFT)
        email_input = tk.Entry(email_frame, textvariable = self.var_email)
        email_input.pack(fill = tk.X)
        
        # --------------------------------------------------------------------------------------------
        # Section 2: Card Details
        # --------------------------------------------------------------------------------------------        
        
        # Card No.
        card_no_frame = tk.Frame(self)
        card_no_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        #self.var_card_no = StringVar()
        card_no_label = tk.Label(card_no_frame, text = "Card No.: ", width = styleDict["labelLen"], anchor = tk.W)
        card_no_label.pack(side = tk.LEFT)
        card_no_input = tk.Entry(card_no_frame, textvariable = self.var_card_no)
        card_no_input.pack(fill = tk.X)
        
        # Expiry Date
        #self.var_date = StringVar()

        self.exdatetext = tk.Frame(self)
        self.exdatetext.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        cardnostr = tk.Label(self.exdatetext, text='Expired Date:')
        cardnostr.pack(side=tk.LEFT)

        self.exdate1 = tk.StringVar()
        exdate1entry1 = tk.Entry(self.exdatetext, textvariable=self.exdate1, show=None, width=10)
        exdate1entry1.insert(0, 'MM')
        exdate1entry1.pack(side=tk.LEFT,padx=45)

        text4 = tk.Label(self.exdatetext, text='/', font=("Arial, 15"))
        text4.pack(side=tk.LEFT)

        self.exdate2 = tk.StringVar()
        exdate1entry2 = tk.Entry(self.exdatetext, textvariable=self.exdate2, show=None, width=10)
        exdate1entry2.insert(0, 'YYYY')
        exdate1entry2.pack(side=tk.LEFT)
        
        # CVV
        cvv_frame = tk.Frame(self)
        cvv_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        #self.var_cvv = StringVar()
        cvv_label = tk.Label(cvv_frame, text = "CVV: ", width = styleDict["labelLen"], anchor = tk.W)
        cvv_label.pack(side = tk.LEFT)
        cvv_input = tk.Entry(cvv_frame, textvariable = self.var_cvv)
        cvv_input.pack(side = tk.LEFT, fill = tk.X)
        
        # --------------------------------------------------------------------------------------------
        # Section 3: Buttons
        # -------------------------------------------------------------------------------------------- 
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        
        # Save Button
        save_button = tk.Button(act_button_frame, text = "Save", width = styleDict["buttonWidth"],
                                command = self.editAccount)
        save_button.pack(side = tk.LEFT, fill = tk.X, padx = styleDict["inlinePadding"])
        
        # Cancel Button
        cancel_button = tk.Button(act_button_frame, text = "Cancel", width = styleDict["buttonWidth"],
                                command = lambda: master.switch_frame(AccountMngPage))
        cancel_button.pack(side = tk.RIGHT)


    def editAccount(self):
        #Get All Data From User Control
        tmp_username = self.var_username.get()
        #tmp_full_name = self.var_name.get()
        tmp_phone = int(self.var_phone.get())
        tmp_email = self.var_email.get()
        tmp_card_no = int(self.var_card_no.get())
        tmp_exdate = self.exdate1.get() + self.exdate2.get()
        tmp_cvv = int(self.var_cvv.get())
        
        try:
            #Get More Data from DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''SELECT ID, Username FROM customer WHERE `Username` = %s;'''
            cursor.execute(query, tmp_username)
            for row in cursor.fetchall():
                tmp_user_id = row[0]
            disconnectDB(connection)

            #Update Data into DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''UPDATE customer SET Phone_Number = %s, Email = %s, Card_No = %s, Expired_Date = %s, CVV = %s 
            WHERE ID = %s;'''
            query_param = (tmp_phone, tmp_email, tmp_card_no, tmp_exdate, tmp_cvv, tmp_user_id)
            cursor.execute(query, query_param)
            connection.commit()
            disconnectDB(connection)
            result = True

        except:
            result = False

        if result:
            msg = "Account is updated successfully"
        else:
            msg = "Something went wrong. Sorry for an inconvenience"
        popupMsg(msg)

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)