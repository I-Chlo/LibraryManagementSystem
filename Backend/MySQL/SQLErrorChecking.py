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

def _verifyBookTITLE(title):
    if len(title) > 100:
        return Response("Book TITLE too long.", status=400)
    else:
        return True
def _verifyBookAUTHOR(author):
    if len(author) > 255:
        return Response("Book AUTHOR too long.", status=400)
    else:
        return True

def _verifyBookEDITION(edition):
    if len(edition) > 45:
        return Response("Book EDITION too long.", status=400)
    else:
        return True

def _verifyBookDATE(date):
    date = datetime.datetime.strptime("2023-06-25", "%Y-%m-%d")


def verifyBookPOSTData(data):
    if data.__len__() != 0:

        # We now need to check that the data at least contains an ISBN, that it converts into a valid number and is 13 characters long
        if data['ISBN']:
            try:
                int(data['ISBN'])
                if len(data['ISBN']) == 13:
                    # Check that the other member variables for the book attribute are present and correct

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
                    # The ISBN wasn't the correct length - therefore we tell the use
                    return Response("ISBN Wrong length. L", status=400)
            except Exception as e:
                # The ISBN cannot be converted into an int and is therefore not valid
                return Response("ISBN invalid <- Only integers allowed in ISBN.\nException: " + str(e), status=400)
        else:
            # ISBN doesn't exist <- we need to inform the user
            return Response("No ISBN = No Bueno", status=400)

    else:
        # Nothing was sent in the POST request, so we need to send an angry letter back to the user.
        return Response("You didn't submit any data to the server. L + Ratio + No Data + Teapot", status=418)


def handleSQLErrors(exp: Exception) -> Response:
    # Take in the exception -> decode it -> produce a response that can be returned to the user.
    if exp.errno == 1062:
        # Integrity constraight violation
        return Response("Integritiy Error: Duplicate entry detected \n" + exp.msg, status=400)

