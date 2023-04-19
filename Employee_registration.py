from flask import Flask, request
import numpy as np
import tabulate
import pandas as pd
from cryptography.fernet import Fernet
import psycopg2
import os
from datetime import datetime
import cv2


app = Flask(__name__)

# Generate a key for encryption and decryption
key = b'_4F4Bp21s-oW6x8mcvENwkS1d2A_uS0W0z8fgvLlMBE='
# key = Fernet.generate_key()
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
    return open('/Users/avinash/Desktop/Capstone project/Employee-Registration/templates/Employee_registration.html').read()

@app.route('/submit-form', methods=['POST'])
def submit_form():
    # Get the form data

    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    last_name = request.form['last_name']
    
    gender = request.form['gender']
    department = request.form['department']
    doj = request.form['date_of_joining']
    
    dob = request.form['date_of_birth']
    mobile = request.form['mobile_number']
    email = request.form['email']
    
    sin = request.form['sin_number']
    add= request.form['address']
    
    city = request.form['city']
    province = request.form['province']
    zip_code = request.form['zip_code']
    fingerprint_img = request.files['fingerprint_image']
   

 # Read the image file using OpenCV
    img_bytes = fingerprint_img.read()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    # Resize the image to a fixed size (e.g. 100x100)
    fingerprint = cv2.resize(img, (100, 100))

     # Create a DataFrame with the form data
    emp_data = {'First Name': [first_name],
            'Middle Name': [middle_name],
            'Last Name': [last_name],
            'Gender': [gender],
            'Department': [department],
            'Date of Joining': [doj],
            'Date of Birth': [dob],
            'Mobile Number': [mobile],
            'Email': [email],
            'SIN Number': [sin],
            'Address': [add],
            'City': [city],
            'Province': [province],
            'Zip Code': [zip_code],
            'Finger Print': [fingerprint]
            }
    
    df = pd.DataFrame(emp_data)

    # Create a DataFrame with the form data
    df = pd.DataFrame([emp_data])

    # Encrypt the sensitive fields
    encrypted_data = emp_data.copy()
    for field in ['Date of Birth', 'Mobile Number', 'Email', 'SIN Number', 'Address', 'City', 'Province', 'Zip Code', 'Finger Print']:
        if field in encrypted_data:
            if field == 'Finger Print':
                # Convert the fingerprint image to bytes
                fingerprint_bytes = cv2.imencode('.jpeg', fingerprint)[1].tobytes()
                # Encrypt the fingerprint image bytes
                encrypted_data[field] = cipher_suite.encrypt(fingerprint_bytes)
                # encrypted_data[field] = cipher_suite.encrypt(encrypted_data[field].tobytes())
            else:
                encrypted_data[field] = cipher_suite.encrypt(str(encrypted_data[field]).encode()).decode()

    # Create a DataFrame with the encrypted data
    encrypted_df = pd.DataFrame([encrypted_data])

    # Display the DataFrames in a tabular format
    emp_table = tabulate.tabulate(df, headers='keys', tablefmt='html', disable_numparse=True)
    emp_table = '<table border="1">\n' + emp_table.split('\n', 1)[1]  # Add border attribute

    encrypted_table = tabulate.tabulate(encrypted_df, headers='keys', tablefmt='html', disable_numparse=True)
    encrypted_table = '<table border="1">\n' + encrypted_table.split('\n', 1)[1]  # Add border attribute

    encp_fingerprint = encrypted_data['Finger Print']

    try: 
# Insert the encrypted data into the database
        cur = conn.cursor()

        # define the insert statement and values
        insert_emp = """INSERT INTO employee_data 
        (first_name, middle_name, last_name, gender, department, doj, dob, mobile, email, sin, address, city, province, zip_code) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = [(df['First Name'][0], df['Middle Name'][0], df['Last Name'][0], df['Gender'][0], df['Department'][0], datetime.strptime(df['Date of Joining'][0][0], '%Y-%m-%d').date(), encrypted_data['Date of Birth'], encrypted_data['Mobile Number'], encrypted_data['Email'], encrypted_data['SIN Number'], encrypted_data['Address'], encrypted_data['City'], encrypted_data['Province'], encrypted_data['Zip Code'])]

    # execute the insert statement with multiple rows
        cur.executemany(insert_emp, values)
        cur.executemany("INSERT INTO emp_key (key) VALUES (%s)", [(key,)])
        cur.executemany("INSERT INTO emp_fingerprint (fingerprint) VALUES (%s)", [(encp_fingerprint,)])
        conn.commit()

    except Exception as e:
        print("Error occurred:", e)
        conn.rollback()   

    finally:
    # Close the database connection
# Close the database connection
        cur.close()
        conn.close()

    # Return the HTML template with the tables
    return f'''
        <h1>Employee Data Saved Successfully:</h1>
        <h1>Original Data:</h1>
        {emp_table}

        # <h1>Encrypted Data:</h1>
        # {encrypted_table}
    '''





















       # Encrypt the employee data using Fernet
    # key = Fernet.generate_key()
    # cipher = Fernet(key)
    # encrypted_emp_data = cipher.encrypt(df.to_csv().encode())

    # # Display the encrypted employee data in a web page
    # encrypted_emp_table = '<table border="1">\n'
    # encrypted_emp_table += '<tr><th>Encrypted Employee Data</th></tr>\n'
    # encrypted_emp_table += f'<tr><td>{encrypted_emp_data.decode()}</td></tr>\n'
    # encrypted_emp_table += '</table>\n'

    # return encrypted_emp_table

    # # Display the DataFrame in a tabular format
    # emp_table = tabulate.tabulate(df, headers='keys', tablefmt='html', disable_numparse=True)
    # emp_table = '<table border="1">\n' + emp_table.split('\n', 1)[1]  # Add border attribute

    # print ('Employee data')

    # return emp_table


if __name__ == '__main__':
    app.run(debug=True)


#     # Define the Fernet key for encryption and decryption
#     key = Fernet.generate_key()
#     fernet = Fernet(key)

#  # Encrypt the DataFrame using Fernet encryption
#     emp_table_bytes = emp_table.encode()
#     encrypted_data = fernet.encrypt(emp_table_bytes)

# import base64
# import csv
# from cryptography.fernet import Fernet
# from hashlib import sha256

# # Define a function to generate a Fernet key from a password
# def generate_key(password):
#     salt = b'salt_' # add a salt value for added security
#     kdf = sha256()
#     kdf.update(password.encode())
#     key = kdf.digest()
#     return Fernet(base64.urlsafe_b64encode(key + salt))

# # Generate a Fernet key from a password
# password = "my_password"
# key = generate_key(password)


# # Encrypt the data using the Fernet key
# with open('https://github.com/abhishah1608/DataSetRepository/blob/Algorithm/details_emp.csv', 'r') as infile:
#     reader = csv.reader(infile)
#     with open('encrypted_details_emp.csv', 'w', newline='') as outfile:
#         writer = csv.writer(outfile)
#         for row in reader:
#             # Encrypt each value in the row
#             encrypted_row = []
#             for value in row:
#                 encrypted_value = key.encrypt(value.encode())
#                 encrypted_row.append(encrypted_value.decode())
#             writer.writerow(encrypted_row)