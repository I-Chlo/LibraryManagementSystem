#
# Author: Chloe Hazell
# Date: 29/06/2023
# FileName: book_control_api.py
# Description: Moved the book api methods into a seperate file to clean up the app.py file.
#

# IMPORTS
from flask import Blueprint, request, Response

from Backend.MySQL.SQLErrorChecking import verifyBookUpdatePOSTData, verifyBookAddPOSTData, verifyBookDeletePOSTData
from Backend.MySQL.sql_connector import sqlBookFunctionSelect, createSQLConnection, db_AddBook, db_DeleteBook

book_control_api = Blueprint('book_control_api', __name__)

conn = createSQLConnection()
@book_control_api.route('/api/Book/update', methods=['POST','GET'])
def updateBook():
    if request.method == "POST":
        data = request.form
        # The user will submit the field that they want to update along with the data that they want inserted into that field
        if isinstance(verifyBookUpdatePOSTDataReturn := verifyBookUpdatePOSTData(data), Response):
            return verifyBookUpdatePOSTDataReturn
        else:
            # The request has been verified so we can commit the change to the database.
            if isinstance(db_UpdateBookResponse := sqlBookFunctionSelect[data['updatedField']](conn, data['ISBN'], data[data['updatedField']]), Response):
                # Return the error to the user
                return db_UpdateBookResponse
            else:
                # The Book has been successfully deleted
                return Response("'" + data['ISBN'] + "' successfully updated " + data['updatedField'])

@book_control_api.route('/api/Book/add', methods=['POST', 'GET'])
def addBook():
    # This methods despiratly needs error checking
    # I.E - some genius might decide to try and just send q request to the server without actually checking the data they are sending
    # Check if data actually exists
    # Check that all expected fields are present <- if ISBN doesn't exist send error back to user

    if request.method == "POST":
        # The user has sent us a book that they wish to store in the library system
        # The data is sent in form-data format and this appears to python as a dictionary of key value pairs
        # e.g. data["ISBN"] = x
        data = request.form
        if isinstance(verifyBookAddPOSTDataReturn := verifyBookAddPOSTData(data), Response):
            return verifyBookAddPOSTDataReturn
        else:
            if isinstance(db_AddBookResponse := db_AddBook(conn, data['ISBN'], data['TITLE'], data['AUTHOR'], data['DATE'], data['EDITION']), Response):
                # DATA data is good so we can continue
                return db_AddBookResponse
            else:
                # The data was addedd successfully to the server - This is seperate incase I want to chain an event to this process.
                return Response("'" + data['TITLE'] + " by " + data['AUTHOR'] + "' successfully added to collection")

    return Response(status=418)

@book_control_api.route('/api/Book/delete', methods=['POST','GET'])
def deleteBook():
    # This methods deletes books from the MySQL databse
    # The user will provide a ISBN number and this will be used as the index for the book in the database
    if request.method == "POST":

        data = request.form
        if isinstance(verifyBookDeletePOSTDataReturn := verifyBookDeletePOSTData(data), Response):
            return verifyBookDeletePOSTDataReturn
        else:
            # The request is valid so we now need to delete the book from the database
            if isinstance(db_DeleteBookResponse := db_DeleteBook(conn, data['ISBN']), Response):
                # Return the error to the user
                return db_DeleteBookResponse
            else:
                # The Book has been successfully deleted
                return Response("'" + data['ISBN'] + "' successfully deleted from collection")