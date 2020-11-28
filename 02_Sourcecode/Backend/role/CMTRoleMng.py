#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:59:32 2019

@author: FlyingPIG
"""
# import libraries
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
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

def restart_program():
    print(LoginInfo.loginid[0] + 223)
    del LoginInfo.loginid[0]
    python = sys.executable
    os.execl(python, python, *sys.argv)

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


class RoleMngPage(tk.Frame):

    def __init__(self, master):
        # Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=True)

        # Initialize Style Dict
        styleDict = init_styleSheet()

        #Set Header Frame
        h_frame = tk.Frame(self, height = styleDict["topPadding"])
        h_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])      
        home_button = tk.Button(h_frame, text = "Home", width = styleDict["buttonWidth"], command = lambda: master.switch_frame(BackEnd.BackEndHomePage), bg = styleDict["TabHeaderBgColor"])
        home_button.pack(side = tk.LEFT)
        lobutton = tk.Button(h_frame, text="Log Out", width = styleDict["buttonWidth"], command=restart_program, bg = styleDict["TabHeaderBgColor"])
        lobutton.pack(side=tk.RIGHT)

        # Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])

        menu_label = tk.Label(menu_frame, text="Role Management: ", font=('Arial', 18), anchor=tk.W)
        menu_label.pack(side=tk.LEFT)
        
#BUTTON ADD & edit
        # Set Action Button Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        edit_button = tk.Button(act_button_frame, text="Edit", width=styleDict["buttonWidth"],
                                command=lambda: master.switch_frame(RoleEditPage))
        edit_button.pack(side=tk.RIGHT)
        add_button = tk.Button(act_button_frame, text="Add", width=styleDict["buttonWidth"],
                               command=lambda: master.switch_frame(RoleAddPage))
        add_button.pack(side=tk.RIGHT, padx=styleDict["inlinePadding"])
#TABLE
        # Create Data Table Frame
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, padx=styleDict["xPadding"], pady=styleDict["yPadding"])

        # Get All Locations
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT ID, Role, Full_Name, Username,Status FROM operator_manager;'''
        sql = pd.read_sql_query(query, connection, params=None)
        location_df = pd.DataFrame(sql, columns=['ID', 'Role', 'Full_Name', 'Username', 'Status'])
        disconnectDB(connection)

        # Set Data Table Frame (Display table only have a data)
        if not location_df.empty:
            location_table = Table(table_frame, dataframe=location_df, showstatusbar=True)
            location_table.show()


class RoleAddPage(tk.Frame):
    def __init__(self, master):

        # Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=True)

        # Initialize Style Dict
        styleDict = init_styleSheet()

        #Set Header Frame
        h_frame = tk.Frame(self, height = styleDict["topPadding"])
        h_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])      
        home_button = tk.Button(h_frame, text = "Home", width = styleDict["buttonWidth"], command = lambda: master.switch_frame(BackEnd.BackEndHomePage), bg = styleDict["TabHeaderBgColor"])
        home_button.pack(side = tk.LEFT)
        lobutton = tk.Button(h_frame, text="Log Out", width = styleDict["buttonWidth"], command=restart_program, bg = styleDict["TabHeaderBgColor"])
        lobutton.pack(side=tk.RIGHT)

        # Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        menu_label = tk.Label(menu_frame, text="Add Role: ", font=('Arial', 18), anchor=tk.W)
        menu_label.pack(side=tk.LEFT)
        
        # Ful_Name
        #Set FullName Frame
        full_name_frame = tk.Frame(self)
        full_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        full_name_label = tk.Label(full_name_frame, text = "Fullname: ", width = styleDict["labelLen"], anchor = tk.W)
        full_name_label.pack(side = tk.LEFT)
        self.var_full_name = StringVar()
        full_name_input = tk.Entry(full_name_frame, textvariable = self.var_full_name)
        full_name_input.pack(fill = tk.X)
        
        # Role
        # Set Role Name Frame
        role_frame = tk.Frame(self)
        role_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        role_label = tk.Label(role_frame, text="Role: ", width=styleDict["labelLen"], anchor=tk.W)
        role_label.pack(side=tk.LEFT)

        # Set Role Combobox
        self.var_role = StringVar()
        role_list = ["Operator","Manager"]
        role_input = ttk.Combobox(role_frame, values = role_list, state='readonly', textvariable=self.var_role)
        role_input.set('Select Type')
        role_input.current(0)
        role_input.pack(fill=tk.X)   
        
        # User_Name
        #Set UserName Frame
        user_name_frame = tk.Frame(self)
        user_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        user_name_label = tk.Label(user_name_frame, text = "Username: ", width = styleDict["labelLen"], anchor = tk.W)
        user_name_label.pack(side = tk.LEFT)
        self.var_user_name = StringVar()
        user_name_input = tk.Entry(user_name_frame, textvariable = self.var_user_name)
        user_name_input.pack(fill = tk.X)
        
        # BUTTON
        # Set Action Buttion Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        back_button = tk.Button(act_button_frame, text="Back", width=styleDict["buttonWidth"],
                                command=lambda: master.switch_frame(RoleMngPage))
        back_button.pack(side=tk.RIGHT)
        confirm_button = tk.Button(act_button_frame, text="Confirm", width=styleDict["buttonWidth"],
                                   command=self.addRole)
        confirm_button.pack(side=tk.RIGHT, fill=tk.X, padx=styleDict["inlinePadding"])

    def addRole(self):
        # Get All Data From User Control
        tmp_full_name = self.var_full_name.get()
        tmp_username = self.var_user_name.get()
        tmp_role = self.var_role.get()
#        tmp_string = self.var_location_name.get().split(sep=' ')
#        tmp_location_name = tmp_string[2]
        

        try:
            # Insert Data into DB
            connection = connectDB()
            cursor = connection.cursor()
            query = '''INSERT INTO operator_manager (Full_Name, Username, Password, Role, Status) 
                    VALUES(%s,%s,'q12345678',%s,'Active');'''
            query_param = (tmp_full_name, tmp_username,tmp_role)
            cursor.execute(query, query_param)
            connection.commit()
            disconnectDB(connection)
            result = True
        except:
            result = False

        if result:
            msg = "Operator is added successfully. Initial password as q12345678."
        else:
            msg = "Some thing went wrong. Sorry for an inconvenience."
        popupMsg(msg)


class RoleEditPage(tk.Frame):
    def __init__(self, master):

        # Initialize Frame
        tk.Frame.__init__(self, master)
        self.pack(fill=tk.BOTH, expand=True)

        # Initialize Style Dict
        styleDict = init_styleSheet()

        # Set Header Frame
        h_frame = tk.Frame(self, height = styleDict["topPadding"])
        h_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])      
        home_button = tk.Button(h_frame, text = "Home", width = styleDict["buttonWidth"], command = lambda: master.switch_frame(BackEnd.BackEndHomePage), bg = styleDict["TabHeaderBgColor"])
        home_button.pack(side = tk.LEFT)
        lobutton = tk.Button(h_frame, text="Log Out", width = styleDict["buttonWidth"], command=restart_program, bg = styleDict["TabHeaderBgColor"])
        lobutton.pack(side=tk.RIGHT)

        # Set Menu Frame
        menu_frame = tk.Frame(self)
        menu_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        menu_label = tk.Label(menu_frame, text="Edit Role: ", font=('Arial', 18), anchor=tk.W)
        menu_label.pack(side=tk.LEFT)

    # Operator_id
        # Set role Name Frame
        Operator_id_frame = tk.Frame(self)
        Operator_id_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        Operator_id_label = tk.Label(Operator_id_frame, text="Operator ID: ", width=styleDict["labelLen"], anchor=tk.W)
        Operator_id_label.pack(side=tk.LEFT)

        # Get all role from DB
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT ID FROM operator_manager;'''
        cursor.execute(query)
        Operator_id_list = []
        for row in cursor.fetchall():
            Operator_id_list.append(row)
        disconnectDB(connection)

        # Set role Combobox
        self.var_Operator_id = StringVar()
        Operator_id_input = ttk.Combobox(Operator_id_frame, values = Operator_id_list, state='readonly', textvariable = self.var_Operator_id)
        # >> Bind onchange event to role combobox
        Operator_id_input.bind("<<ComboboxSelected>>", self.callback)
        Operator_id_input.set('Select ID')
        Operator_id_input.pack(fill=tk.X)
        
        # Ful_Name
        #Set FullName Frame
        full_name_frame = tk.Frame(self)
        full_name_frame.pack(fill = tk.X, padx = styleDict["xPadding"], pady = styleDict["yPadding"])
        full_name_label = tk.Label(full_name_frame, text = "Fullname: ", width = styleDict["labelLen"], anchor = tk.W)
        full_name_label.pack(side = tk.LEFT)
        self.var_full_name = StringVar()
        full_name_input = tk.Entry(full_name_frame, textvariable = self.var_full_name)
        full_name_input.pack(fill = tk.X)

        # Role
        # Set Role Name Frame
        role_frame = tk.Frame(self)
        role_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        role_label = tk.Label(role_frame, text="Role: ", width=styleDict["labelLen"], anchor=tk.W)
        role_label.pack(side=tk.LEFT)

        # Set Role Combobox
        self.var_role = StringVar()
        role_list = ["Operator","Manager"]
        role_input = ttk.Combobox(role_frame, values = role_list, state='readonly', textvariable=self.var_role)
        role_input.set('Select Type')
        role_input.pack(fill=tk.X)  
        
        # Status
        # Set status Name Frame
        status_frame = tk.Frame(self)
        status_frame.pack(fill=tk.X, padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        status_label = tk.Label(status_frame, text="Status: ", width=styleDict["labelLen"], anchor=tk.W)
        status_label.pack(side=tk.LEFT)

        # Set status Combobox
        self.var_status = StringVar()
        status_list = ["Active","Inactive"]
        status_input = ttk.Combobox(status_frame, values = status_list, state='readonly', textvariable = self.var_status)
        status_input.set('Select Type')
        status_input.pack(fill=tk.X)  

        # BUTTON
        # Set Action Buttion Frame
        act_button_frame = tk.Frame(self)
        act_button_frame.pack(padx=styleDict["xPadding"], pady=styleDict["yPadding"])
        back_button = tk.Button(act_button_frame, text="Back", width=styleDict["buttonWidth"],
                                command=lambda: master.switch_frame(RoleMngPage))
        back_button.pack(side=tk.RIGHT)
        confirm_button = tk.Button(act_button_frame, text="Confirm", width=styleDict["buttonWidth"],
                                   command=self.editRole)
        confirm_button.pack(side=tk.RIGHT, fill=tk.X, padx=styleDict["inlinePadding"])

    def callback(self, event):
        self.setCurrentLocData()

    def setCurrentLocData(self):
        connection = connectDB()
        cursor = connection.cursor()
        query = '''SELECT Full_Name, Role, Status FROM operator_manager WHERE ID = %s;'''
        cursor.execute(query, self.var_Operator_id.get())
        for row in cursor.fetchall():
            self.var_full_name.set(row[0])
            self.var_role.set(row[1])
            self.var_status.set(row[2])
        
    def editRole(self):
        # Get All Data From User Control
        tmp_Operator_id = self.var_Operator_id.get()
        tmp_full_name = self.var_full_name.get()
        tmp_role = self.var_role.get()
        tmp_status = self.var_status.get()
        
        print(tmp_full_name)

        try:
            connection = connectDB()
            cursor = connection.cursor()
            
            query = '''SELECT Full_Name FROM operator_manager WHERE Full_Name = %s;'''
            cursor.execute(query, tmp_full_name)
            
            num=0
            for row in cursor.fetchall():
                num+=1
            if num==1:
                msg = "Duplicated Name, Please input the new name."
                disconnectDB(connection)
                result = False
            else:
                connection = connectDB()
                cursor = connection.cursor()           
                # Update Data into DB
                query = '''UPDATE operator_manager SET `Full_Name` = %s, `Role` = %s, Status = %s WHERE ID = %s;'''
                query_param = (tmp_full_name, tmp_role, tmp_status, tmp_Operator_id)
                cursor.execute(query, query_param)
                connection.commit()
                disconnectDB(connection)
                result = True
        except:
            result = False

        if result:
            msg = "Role is updated successfully"
        else:
            if msg == "":
                msg = "Some thing went wrong. Sorry for an inconvenience"
        popupMsg(msg)




