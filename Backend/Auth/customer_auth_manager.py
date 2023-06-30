#
# Author: Chloe Hazell
# Date: 29/06/2023
# FileName: customer_auth_manager.py
# Description:
#



# IMPORT
from flask import Blueprint, request, Response
import bcrypt

customer_auth_manager = Blueprint('customer_auth_manager', __name__)

# TO DO
# Allow for customers to be resgistered <- In Progress
# Allow for customer details to be managed

@customer_auth_manager.route('/api/Auth/customer/regsiter', methods=['POST', 'GET'])
def register_customer():
    # We need to get the customers data and then send the data to the db.
    # The password will be transmitted to the server and then bcrypt will be used to be hash the password
    # This password is what will be stored in the db

    if request.method == "POST":
        data = request.form
        # DATA
        #   "full_name" <- Required - e.g. Chloe Hazell
        #   "chosen_name" <- Required e.g. Chloe
        #   "user_name" <- Required e.g. I-Chlo
        #   "email_address" <- Required e.g. xxx@gmail.com
        #   "password" <- Required e.g. 1234password5678
        #   "address_line_1" <- Required <- 308 Belmost Avenue, Ontario, California
        #   "address_line_2" <- Optional
        #   "post_code" <- Required <- 91764
        # We will use client side validation to make sure that the client's data is in the corrct format,
        # then use server side validation to make sure that the data that is going to be stored is actually ok to be stored

