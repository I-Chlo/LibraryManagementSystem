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
import string
from flask import Response

import mysql.connector
from dotenv import load_dotenv
from .SQLErrorChecking import handleSQLErrors

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


def db_AddBook(conn, ISBN: string,TITLE: string,AUTHOR: string,DATE: string,EDITION: string) -> Response or bool:
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Books (ISBN,TITLE,AUTHOR,DATE_PUB,EDITION) VALUES (%s,%s,%s,%s,%s)",
                       (ISBN, TITLE, AUTHOR, DATE, EDITION))
        conn.commit()
    except mysql.connector.Error as e:
        return handleSQLErrors(e)
    return True

def db_DeleteBook(conn, ISBN) -> Response or bool:
    cursor = conn.cursor(buffered=True)
    try:
        # Attempt to delete the given ISBN from the database
        cursor.execute("DELETE FROM Books WHERE ISBN = %s ", (ISBN,))
    except mysql.connector.Error as e:
        # If there is some kind of error then handle it
        return handleSQLErrors(e)
    # Check the amount of rows affected by the DELETE command. If none where affected then there was nothing to remove.
    # In that case return an error to the user.
    if cursor.rowcount != 1:
        # The method didn't delete anything so we need to return an error to the user
        return Response("SQL Delete Error: This ISBN doesn't exist!", status=400)
    else:
        # If there was a book to delete then commit the change to the database and return true
        conn.commit()
        return True


def db_UpdateTitle(conn, ISBN, TITLE) -> None:
    cursor = conn.cursor()
    cursor.execute("UPDATE Books SET TITLE = %s WHERE ISBN = %s", (TITLE, ISBN))
    conn.commit()

def db_UpdateAuthor(conn, ISBN, AUTHOR) -> None:
    cursor = conn.cursor()
    cursor.execute("UPDATE Books SET AUTHOR = %s WHERE ISBN = %s", (AUTHOR, ISBN))
    conn.commit()

def db_UpdateDate(conn, ISBN, DATE) -> None:
    cursor = conn.cursor()
    cursor.execute("UPDATE Books SET DATE_PUB = %s WHERE ISBN = %s", (DATE, ISBN))
    conn.commit()

def db_UpdateEdition(conn, ISBN: string, EDITION) -> None:
    cursor = conn.cursor()
    cursor.execute("UPDATE Books SET EDITION = %s WHERE ISBN = %s", (EDITION, ISBN))
    conn.commit()

sqlBookFunctionSelect = {
    "TITLE": db_UpdateTitle,
    "AUTHOR": db_UpdateAuthor,
    "DATE": db_UpdateDate,
    "EDITION": db_UpdateEdition
}




# CUSTOMER SQL FUNCTIONS


