from flask import Flask, request, render_template
import numpy as np
import tabulate
import pandas as pd
from cryptography.fernet import Fernet
import psycopg2
import os
from datetime import datetime
import cv2
from PIL import Image
from io import BytesIO


app = Flask(__name__)

# Generate a key for encryption and decryption
key = b'_4F4Bp21s-oW6x8mcvENwkS1d2A_uS0W0z8fgvLlMBE='
cipher_suite = Fernet(key)

 # Connect to PostgreSQL database
conn = psycopg2.connect(
        host="localhost",
        database="employee_db",
        user="Admin",
        password="Admin@123"
)

@app.route('/')
def index():
    # Return the HTML form
    return open('/Users/avinash/Desktop/Capstone project/GetEmployeeData/validate_employee.html').read()

@app.route('/submit-valform', methods=['POST'])
def submit_form():

    # Get the ID from the form
    card_ID = request.form['employee_id'].encode('utf-8')

    # Query the database to check if the ID exists
    cur = conn.cursor()
    # cur.execute("SELECT ek.key, ep.fingerprint FROM emp_key ek inner join emp_fingerprint ep on ek.emp_id = ep.emp_id")

    cur.execute("SELECT ed.* FROM employee_data ed inner join emp_key ek  on ek.emp_id = ed.emp_id WHERE ek.key  = %s", [card_ID])
    result = cur.fetchone()
    cur.close()

    if not result:
        return "No employee data found."
# Generate the HTML table
    table_html = "<table><tr><th>First Name</th><th>Middle Name</th><th>Last Name</th><th>Gender</th><th>Department</th><th>Date of Joining</th><th>Date of Birth</th><th>Mobile Number</th><th>Email</th><th>SIN Number</th><th>Address</th><th>City</th><th>Province</th><th>Zip Code</th><th>Finger Print</th></tr>"

# Loop through the result and add rows to the HTML table
        # Decrypt the specified columns using Fernet key
    dob = cipher_suite.decrypt(bytes(result[7])).decode()
    mobile = cipher_suite.decrypt(bytes(result[8])).decode()
    email = cipher_suite.decrypt(bytes(result[9])).decode()
    sin = cipher_suite.decrypt(bytes(result[10])).decode()
    add = cipher_suite.decrypt(bytes(result[11])).decode()
    city = cipher_suite.decrypt(bytes(result[12])).decode()
    province = cipher_suite.decrypt(bytes(result[13])).decode()
    zip_code = cipher_suite.decrypt(bytes(result[14])).decode()
        # fingerprint = result[16]
    

    table = "<table style='border-collapse: collapse; width: 100%;'>"
    table += "<tr><th style='border: 1px solid black; width: 10%;'>First Name</th><th style='border: 1px solid black; width: 10%;'>Middle Name</th><th style='border: 1px solid black; width: 10%;'>Last Name</th><th style='border: 1px solid black; width: 5%;'>Gender</th><th style='border: 1px solid black; width: 10%;'>Department</th><th style='border: 1px solid black; width: 10%;'>Date of Joining</th><th style='border: 1px solid black; width: 10%;'>Date of Birth</th><th style='border: 1px solid black; width: 10%;'>Mobile Number</th><th style='border: 1px solid black; width: 10%;'>Email</th><th style='border: 1px solid black; width: 10%;'>SIN Number</th><th style='border: 1px solid black; width: 10%;'>Address</th><th style='border: 1px solid black; width: 10%;'>City</th><th style='border: 1px solid black; width: 10%;'>Province</th><th style='border: 1px solid black; width: 10%;'>Zip Code</th>"

    Employee_Data = [result[1][1:-1], result[2][1:-1], result[3][1:-1], result[4][1:-1], result[5][1:-1], result[6], dob[2:-2], mobile[2:-2], email[2:-2], sin[2:-2], add[2:-2],  city[2:-2], province[2:-2], zip_code[2:-2]]
    table += "<tr>"
    for data in Employee_Data:
        table += "<td style='border: 1px solid black;'>" + str(data) + "</td>"
    table += "</tr>"

    table += "</table>"

    return f'''
        <h1>Employee validated Successfully<h1> <br>
        <h2> Data of {result[1][1:-1]}:</h2>
        {table}
    '''           

if __name__ == '__main__':
    app.run(debug=True)