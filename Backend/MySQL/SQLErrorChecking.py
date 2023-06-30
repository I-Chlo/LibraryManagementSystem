#
# Author: Chloe Hazell
# Date: 26/06/2023
# FileName: SQLErrorChecking.py
# Description:
#

##IMPORTS
from flask import Response
import datetime
import string
import re

def _verifyBookTITLE(title: string) -> Response or bool :
    if len(title) > 100:
        return Response("Book TITLE too long.", status=400)
    else:
        return True
def _verifyBookAUTHOR(author: string) -> Response or bool:
    if len(author) > 255:
        return Response("Book AUTHOR too long.", status=400)
    else:
        return True
def _verifyBookEDITION(edition: string) -> Response or bool:
    if len(edition) > 45:
        return Response("Book EDITION too long.", status=400)
    else:
        return True
def _verifyBookDATE(date: string) -> Response or bool:
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except Exception as e:
        return Response("Book DATE is in the wrong format: ERR: " + e, status=400)
def _verifyBookISBN(isbn: string) -> Response or bool:
    try:
        int(isbn)
        if len(isbn) == 13:
            # Return if both criteria are satified
            return True
        else:
            # Return if the ISBN isn't exactly 13 character long
            return Response("ISBN Wrong length. L", status=400)
    except Exception as e:
        # Return if the ISBN is not an integer value
        return Response("ISBN invalid <- Only integers allowed in ISBN.\nException: " + str(e), status=400)
bookVerifySelector ={
    "TITLE": _verifyBookTITLE,
    "AUTHOR": _verifyBookAUTHOR,
    "DATE": _verifyBookDATE,
    "EDITION": _verifyBookEDITION
}
def verifyBookAddPOSTData(data: dict) -> Response or bool:
    if data.__len__() != 0:

        # We now need to check that the data at least contains an ISBN, that it converts into a valid number and is 13 characters long
        if not data['ISBN']:
            # ISBN doesn't exist <- we need to inform the user
            return Response("No ISBN = No Bueno", status=400)
        else:
                if isinstance(bookISBNVerifyReturn := _verifyBookISBN(data['ISBN']), Response):
                    # Return if the ISBN isn't valid
                    return bookISBNVerifyReturn

                else:
                    # The ISBN is valid so we can continue
                    # CHECK TITLE DATA
                    if not data['TITLE']:
                        # No TITLE has been found in the data
                        return Response("Book TITLE not found", status=400)
                    else:
                        if isinstance(bookTitleVerifyReturn := _verifyBookTITLE(data['TITLE']), Response):
                            # TITLE data is good so we can continue
                            return bookTitleVerifyReturn

                        # CHECK AUTHOR DATA
                    if not data['AUTHOR']:
                            # No AUTHOR has been found in the data
                            return Response("Book AUTHOR not found", status=400)
                    else:
                            if isinstance(bookAuthorVerifyReturn := _verifyBookAUTHOR(data['AUTHOR']), Response):
                                # AUTHOR data is good so we can continue
                                return bookAuthorVerifyReturn

                        # CHECK EDITION DATA
                    if not data['EDITION']:
                            # No EDITION has been found in the data
                            return Response("Book EDITION not found", status=400)
                    else:
                            if isinstance(bookEditionVerifyReturn := _verifyBookAUTHOR(data['EDITION']), Response):
                                # EDITION data is good so we can continue
                                return bookEditionVerifyReturn

                        # CHECK DATE DATA
                    if not data['DATE']:
                            # No DATE has been found in the data
                            return Response("Book DATE not found", status=400)
                    else:
                            if isinstance(bookDateVerifyReturn := _verifyBookDATE(data['DATE']), Response):
                                # DATA data is good so we can continue
                                return bookDateVerifyReturn

                        # If we have reached here that means that all elements in the POST request where valid and can be entered into the database.
                    return True


    else:
        # Nothing was sent in the POST request, so we need to send an angry letter back to the user.
        return Response("You didn't submit any data to the server. L + Ratio + No Data + Teapot", status=418)
def verifyBookDeletePOSTData(data: dict) -> Response or bool:
    # Check that data isn't empty
    if data.__len__() != 0:
        # Verify the ISBN
        if not data['ISBN']:
            # ISBN doesn't exist <- we need to inform the user
            return Response("No ISBN = No Bueno", status=400)
        else:
                # Run the ISBN checking method and if it returns a Response object then return it to the user else return True
                if isinstance(bookISBNVerifyReturn := _verifyBookISBN(data['ISBN']), Response):
                    # Return if the ISBN isn't valid
                    return bookISBNVerifyReturn

                else:
                    # The ISBN is valid
                    return True
    else:
        return Response('No Data submitted. Please try again.', status=400)
def verifyBookUpdatePOSTData(data: dict) -> Response or bool:
    # Check that data isn't empty
    if data.__len__() != 0:
        # Verify the ISBN
        if not data['ISBN']:
            # ISBN doesn't exist <- we need to inform the user
            return Response("No ISBN = No Bueno", status=400)
        else:
            # Run the ISBN checking method and if it returns a Response object then return it to the user else return True
            if isinstance(bookISBNVerifyReturn := _verifyBookISBN(data['ISBN']), Response):
                # Return if the ISBN isn't valid
                return bookISBNVerifyReturn

            else:
                # If the ISBN is valid then we need to verify that the data provided from the user is valid.
                # The correct artibute verifying function will be selected based on the attribute that is to be updated
                return bookVerifySelector[data["updatedField"]](data)
    else:
        return Response('No Data submitted. Please try again.', status=400)


# CUSTOMER VERIFICATION
def _verifyCustomerFullName(fname: string) -> Response or bool:
    # Customer full name <= 255
    if len(fname) >= 255:
        # it is invalid
        return Response("The Full Name Property is too long.", status=400)
    else:
        return True

def _vertifyCustomerGivenName(gname: string) -> Response or bool:
    # Customer given name <= 100
    if len(gname) >= 100:
        # it is invalid
        return Response("The Given Name Property is too long.", status=400)
    else:
        return True

def _verifyCustomerUsername(username: string) -> Response or bool:
    # Customer Username <= 50
    if len(username) <= 50:
        # it is invalid
        return Response("The Given Name Property is too long.", status=400)
    else:
        return True

def _verifyCustomerEmail(email: string) -> Response or bool:
    emailVerify = re.compile("/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/")
    if emailVerify.match(email):
        # The email is in a valid format
        if len(email) >= 255:
            # The email is too long
            return Response("The Email is too long.", status=400)
        else:
            # The email is valid
            return True
    else:
        # It is not a valid email
        return Response("The Email Format is not valid.", status=400)



def handleSQLErrors(exp: Exception) -> Response:
    # Take in the exception -> decode it -> produce a response that can be returned to the user.
    if exp.errno == 1062:
        # Integrity constraight violation
        return Response("Integritiy Error: Duplicate entry detected \n" + exp.msg, status=400)
    else:
        print("Unknown Error")
        print(exp)
        return Response("Unknown SQL Error: " + exp.msg, status=400)