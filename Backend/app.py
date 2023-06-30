##
## Date: 24-06-23
## Author: Chloe Hazell
## Description: Create the flask server and methods for controlling the Management system.
##

## IMPORTS -----
from flask import Flask, url_for, request, Response
from MySQL.sql_connector import createSQLConnection, db_AddBook, db_DeleteBook, db_UpdateTitle, db_UpdateEdition,\
    db_UpdateDate, db_UpdateAuthor, sqlBookFunctionSelect
from MySQL.SQLErrorChecking import verifyBookAddPOSTData, verifyBookDeletePOSTData, verifyBookUpdatePOSTData
from book_control_api import book_control_api
## NOTES / TO-DO
# Be able to add/delete/update book in system <- done
# Check out books <- and register customers
# Query late returns <- find consistently late returners (i.e. find dickheads)
# register users - authentication <- only authorised users can access specific things
# compare input data against an ISBN database to check for irregularities
# export statistics <- most taken books / other fun stats
# have react ui using flask <- will be the last thing as it will probably take the longest as im not very cool at react

# TO-DO 2
# Add Books <- Done
# Delete Books <- Done
# Update Books <- Done
# Register Customers <- In Progress
# Register Staff
# Check out books


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
# This needs some kind of error checking method as if the SQL server cannot be found the program aborts - not very cool ngl



app.register_blueprint(book_control_api)




# This is only here so that i don't have to run the script from the terminal
# and so i can use the pycharm debugger
# pycharm > VSCode don't @ me.
if __name__ == "__main__":
    app.run(debug=True)
