##
## Date: 25-06-23
## Author: Chloe Hazell
## Description: Creates the SQL connection and defines methods for interacting with the server
##

## METHOD LIST

#   createSQLConnection -> create the connection with the SQL server and return the connection object
#   db_AddBook -> Add a book to the Books table
#       -> Expects (connection, ISBN, TITLE, AUTHOR, DATE, EDITION)
#   db_RemoveBook -> Removes a book from the Books table
#       -> Expects (connection, ISBN)
#   db_UpdateTitle <- Updates the Title of a book given an ISBN
#       -> Expects (connection, ISBN, TITLE)
#   db_UpdateAuthor <- Updates the Author of a book given an ISBN
#       -> Expects (connection, ISBN, AUTHOR)
#   db_UpdateTitle <- Updates the Date of a book given an ISBN
#       -> Expects (connection, ISBN, DATE)
#   db_UpdateEdition <- Updates the Edition of a book given an ISBN
#       -> Expects (connection, ISBN, EDITION)

## IMPORTS
import os
import mysql.connector
from dotenv import load_dotenv

## LOAD .ENV FILE ##
load_dotenv()

## METHODS ##
def createSQLConnection():
    conn = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        passwd=os.getenv("PASSWORD"),
        db=os.getenv("DATABASE"))

    #db_AddBook(conn, "1234567890002","Chloe", "How to be Trans", "2023-06-25", "1")
    db_UpdateTitle(conn, "1234567890002", "How to be Trans")
    #db_RemoveBook(conn, "1234567890001")
    return conn


def db_AddBook(conn, ISBN,TITLE,AUTHOR,DATE,EDITION):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (ISBN,TITLE,AUTHOR,DATE_PUB,EDITION) VALUES (%s,%s,%s,%s,%s)", (ISBN,TITLE,AUTHOR,DATE,EDITION))
    conn.commit()

def db_RemoveBook(conn, ISBN):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Books WHERE ISBN = %s", (ISBN,))
    conn.commit()

def db_UpdateTitle(conn, ISBN, TITLE):
    cursor = conn.cursor()
    cursor.execute("UPDATE Books SET TITLE = %s WHERE ISBN = %s", (TITLE, ISBN))
    conn.commit()

def db_UpdateAuthor(conn, ISBN, AUTHOR):
    cursor = conn.cursor()
    cursor.execute("UPDATE Books SET AUTHOR = %s WHERE ISBN = %s", (AUTHOR, ISBN))
    conn.commit()

def db_UpdateDate(conn, ISBN, DATE):
    cursor = conn.cursor()
    cursor.execute("UPDATE Books SET DATE = %s WHERE ISBN = %s", (DATE, ISBN))
    conn.commit()

def db_UpdateEdition(conn, ISBN, EDITION):
    cursor = conn.cursor()
    cursor.execute("UPDATE Books SET DATE = %s WHERE ISBN = %s", (EDITION, ISBN))
    conn.commit()