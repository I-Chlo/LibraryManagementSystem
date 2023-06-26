##
## Date: 24-06-23
## Author: Chloe Hazell
## Description: Create the flask server and methods for controlling the Management system.
##

## IMPORTS -----
from flask import Flask, url_for, request, Response
from MySQL.sql_connector import createSQLConnection, db_AddBook, db_RemoveBook, db_UpdateTitle, db_UpdateEdition, \
    db_UpdateDate, db_UpdateAuthor

## NOTES / TO-DO
# Be able to add/delete/update book in system
# Check out books <- and register customers
# Query late returns <- find consistently late returners (i.e. find dickheads)
# register users - authentication <- only authorised users can access specific things
# compare input data against an ISBN database to check for irregularities
# export statistics <- most taken books / other fun stats
# have react ui using flask <- will be the last thing as it will probably take the longest as im not very cool at react


# DEV LOG 25-06-2023
# -> Created SQL connection
# -> Created SQL Create, Delete, Update statements for books
# -> Create POST receive method for Adding Books and error checking for the ISBN
# TO DO:
#   -> Add error checking for other parts of the adding books section
#   -> Create routes for other SQL methods with error checking for each
#   -> Create error checking functions to remove repeated code


# Create flask server
app = Flask(__name__)
# Create connection to MySQL server <- may switch to NoSQL in the future but not sure as of now
# E.g. MongoDB
conn = createSQLConnection()

print(conn)


@app.route('/api/Book/add', methods=['POST', 'GET'])
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
        if data.__len__() != 0:
            # We now need to check that the data at least contains an ISBN, that it converts into a valid number and is 13 characters long
            if data["ISBN"]:
                try:
                    int(data["ISBN"])
                    if len(data["ISBN"]) == 13:
                        db_AddBook(conn, data['ISBN'], data['TITLE'], data['AUTHOR'], data['DATE'], data['EDITION'])
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

    return '<h1>Hello, World!</h1>'


if __name__ == "__main__":
    app.run(debug=True)
