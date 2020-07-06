# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 11:59:35 2020

@author: Design
"""
from sys import exit
import mysql.connector
from mysql.connector import errorcode


def create_connection(host_name='localhost', user_name='root', user_password='Password'):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(f"The error '{err}' occurred")
        exit(1)

    return connection

def create_database(cursor, db_name):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        print("Database created successfully")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            cStr = input("Database {} already exists.  Would you like to overwrite it? (y/n)\n".format(db_name))
            if cStr.lower() == 'y':
                try:
                    cursor.execute("DROP DATABASE {}".format(db_name))
                    cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
                    print("Database re-created successfully")
                except mysql.connector.Error as err:
                    print(f"The error '{err}' occurred")
                    exit(1)
            else:
                print(f"The error '{err}' occurred")

        else:
            print(f"The error '{err}' occurred")
            exit(1)
