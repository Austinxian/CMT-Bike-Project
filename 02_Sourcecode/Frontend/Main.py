#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 19:18:57 2019

@author: wang
"""
# import libraries
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import pymysql
import pymysql
from pandastable import Table, TableModel
import getpass

# import other pages
from select_qr import select_qr
from config import LoginInfo, DBConnect
from sign_up import signup


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
    done_button = tk.Button(popup, text="Continue", command=popup.destroy)
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


class FrontEndApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.geometry(styleDict["windowSize"])
        self.title(styleDict["Title"])

        # Create Login Form
        self.labelframe = tk.Frame(self, height=styleDict["topPadding"])
        self.labelframe.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])

        title = tk.Label(self.labelframe, text='CMT-Bike System', font=("Arial, 30"))
        title.pack(side=tk.TOP, padx=30, pady=70)

        self.userframe = tk.Frame(self, height=styleDict["topPadding"])
        self.userframe.pack(fill=tk.X, padx=styleDict["xPadding"], pady=50)

        username = tk.Label(self.userframe, text='Username:', font=("Arial, 22"))
        username.pack(side=tk.LEFT, padx=20)

        self.var1 = tk.StringVar()
        usr = tk.Entry(self.userframe, textvariable=self.var1, show=None, width=50)
        usr.pack()

        self.pwframe = tk.Frame(self, height=styleDict["topPadding"])
        self.pwframe.pack(fill=tk.X, padx=styleDict["xPadding"], pady=50)
        password = tk.Label(self.pwframe, text='Password:', font=("Arial, 22"))
        password.pack(side=tk.LEFT, padx=20)

        self.var2 = tk.StringVar()
        pw = tk.Entry(self.pwframe, textvariable=self.var2, show="*" , width=50)
        pw.pack()

        self.buttonframe = tk.Frame(self, height=styleDict["topPadding"])
        self.buttonframe.pack(fill=tk.X, padx=styleDict["xPadding"])

        login = tk.Button(self.buttonframe, text="log in", font=("Arial, 22"), width=25, height=3,
                          command=self.callback)
        login.pack(pady=20)

        self.textframe = tk.Frame(self, height=styleDict["topPadding"])
        self.textframe.pack(fill=tk.X, padx=styleDict["xPadding"], pady=20)
        text = tk.Label(self.textframe, text="Not yet a Member? ", font=("Arial", "15"))
        text.pack(pady=10)
        text1 = tk.Label(self.textframe, text="Register Here", font=("Arial", "15", "underline"))
        text1.pack(pady=10)
        text1.bind("<Button-1>", self.callAdapator(self.call))

    def callback(self):
        num,userid = self.validateUser()
        if num == 1:
            # Go to Frontend page
            self.switch_frame(select_qr.QRPage)
            self.labelframe.destroy()
            self.userframe.destroy()
            self.pwframe.destroy()
            self.buttonframe.destroy()
            self.textframe.destroy()
        else:
            popupMsg("Incorrect Username/password or Invalid Users.")

    def call(self,event):
        self.switch_frame(signup.signup)
        self.labelframe.destroy()
        self.userframe.destroy()
        self.pwframe.destroy()
        self.buttonframe.destroy()
        self.textframe.destroy()

    def callAdapator(self,fun, **kwds):
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    def validateUser(self):
        usrname = self.var1.get()
        psw = self.var2.get()
        connection = connectDB()
        cursor = connection.cursor()
        cursor.execute(("""select ID from customer where Username=%s and Password=%s """), (usrname, psw))
        num = 0
        for data in cursor.fetchall():
            num = num + 1
            userid = data[0]
            LoginInfo.init()
            LoginInfo.loginid.append(userid)

        # Set validate result into tuple -> row_number: userid: role
        if num == 0:
            result = (0, 0)
        else:
            result = (1, userid)
        return result

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


if __name__ == "__main__":
    styleDict = init_styleSheet()
    app = FrontEndApp()
    app.mainloop()
