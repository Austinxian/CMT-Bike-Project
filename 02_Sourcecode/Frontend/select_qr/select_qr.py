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
import os
import sys
from trip import StartTrip

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


class QRPage(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            styleDict = init_styleSheet()
            self.pack(fill=tk.BOTH, expand=True)

            h_frame = tk.Frame(self, width = 204, height = 58)
            h_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
            self.pilImage2 = Image.open('select_qr/frontend-3.png')
            self.tkImage2 = ImageTk.PhotoImage(self.pilImage2)
            home = tk.Label(h_frame, text="Home", image = self.tkImage2)
            home.pack(side = tk.LEFT)
            logout_button = tk.Button(h_frame, text="Log Out", width=15, command=self.restart_program)
            logout_button.pack(side=tk.RIGHT)
            myrental_button = tk.Button(h_frame, text="My Rental", width=15, command=lambda: master.switch_frame(CMTMyRentalHistory.MyRentalHistoryPage))
            myrental_button.pack(side=tk.RIGHT)
            myaccount_button = tk.Button(h_frame, text="My Account", width=15, command=lambda: master.switch_frame(Account.AccountMngPage))
            myaccount_button.pack(side=tk.RIGHT)



            #Set Bike ID Lable
            l1_frame = tk.Frame(self)
            l1_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
            l1_label = tk.Label(l1_frame, text="Bike ID", font=('Arial', 40, tkFont.BOLD))
            l1_label.pack(side = tk.LEFT, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
            self.var_bike_ID = StringVar()
            l1_text = tk.Entry(l1_frame,width = 30, textvariable = self.var_bike_ID)
            l1_text.pack(fill = tk.X ,padx = styleDict["xPadding"], pady = 60)


            l2_frame = tk.Frame(self)
            l2_frame.pack(fill=tk.Y, padx=styleDict["xPadding"], pady=5)
            l2_label = tk.Label(l2_frame, text="or", font=('Arial', 18))
            l2_label.pack(fill = tk.Y ,padx = styleDict["xPadding"], pady = styleDict["yPadding"])

            b1_frame = tk.Frame(self)
            b1_frame.pack(fill=tk.Y, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
            self.pilImage = Image.open('select_qr/fronted-1.png')
            self.tkImage = ImageTk.PhotoImage(self.pilImage)
            b1_button = tk.Button(self, text = "Scan QR Code", font=('Arial', 28),compound = 'bottom', image = self.tkImage )
            b1_button.pack(padx = styleDict["xPadding"], pady = 40)

            b2_frame = tk.Frame(self)
            b2_frame.pack(fill=tk.Y, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
            chk_button = tk.Button(b2_frame, text="Check Availabilty",width=50, height=3,  command =self.searchID)
            chk_button.pack()
            self.pilImage1 = Image.open('select_qr/frontend-2.png')
            self.tkImage1 = ImageTk.PhotoImage(self.pilImage1)
            self.b3_frame = tk.Frame(self)
            self.b3_frame.pack(fill=tk.Y, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
            self.b2_button = tk.Button(self.b3_frame, text="Confirm", width=50, height=3,  state=DISABLED, command=lambda: master.switch_frame(StartTrip.StartTripPage))
            self.b2_button.pack()
            b4_frame = tk.Frame(self)
            b4_frame.pack(fill=tk.Y, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
            l3_label = tk.Label(b4_frame, image=self.tkImage1)
            l3_label.pack(fill=tk.Y, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
            self.textframe = tk.Frame(self, height=styleDict["topPadding"])
            self.textframe.pack(fill=tk.X, padx=styleDict["xPadding"], pady=20)
            text = tk.Label(self.textframe, text="Find Bike Manually ", font=("Arial", "15", "underline"), fg = "blue")
            text.pack(pady=10)
            text.bind("<Button-1>", lambda event :master.switch_frame(SearchBikeID.SearchBikeID))


        def searchID(self):
            
            tmp_customer_id = LoginInfo.loginid[0]
            connection = connectDB()
            cursor = connection.cursor()
            
            #Check Are there any In Progress transaction
            num = 0
            query = '''SELECT ID FROM transaction where Status = "In Progress" AND Customer_ID = %s;'''
            cursor.execute(query, tmp_customer_id)
            for row in cursor.fetchall():
                num += 1
                
            #Check Availability
            if num == 0:
                tmp_bike_ID = self.var_bike_ID.get()
            
                cursor.execute('''SELECT `Condition` from bike WHERE bike.ID = %s;''', tmp_bike_ID)
                for x in cursor.fetchall():
                    if x[0].lower() == "available":
                        self.b2_button['state'] = 'normal'
                        LoginInfo.bikeid.append(tmp_bike_ID)
                        popupMsg("This bike is available.")
                    else:
                        popupMsg("This bike is unavailable.Please try another bike ID")
            else:
                msg = "Please return the previous bike before renting a new one."
                popupMsg(msg)
            disconnectDB(connection)
            

        def restart_program(self):
            python = sys.executable
            os.execl(python, python, *sys.argv)

