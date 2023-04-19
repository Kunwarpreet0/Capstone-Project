import cv2
import psycopg2
from io import BytesIO
import numpy as np
from cryptography.fernet import Fernet
from sklearn.decomposition import PCA

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
# Query the database to check if the ID exists
cur = conn.cursor()
    # cur.execute("SELECT ek.key, ep.fingerprint FROM emp_key ek inner join emp_fingerprint ep on ek.emp_id = ep.emp_id")

cur.execute("SELECT ek.key, ep.fingerprint FROM emp_key ek inner join emp_fingerprint ep on ek.emp_id = ep.emp_id WHERE key = %s", [key])
result = cur.fetchone()
    # # Read the result values
    # out_fingerprint = result[0]
    # out_key = result[1]


# Read the result values
encrypted_image = result[1].tobytes()
key = result[0]
decrypted_image = cipher_suite.decrypt(encrypted_image)
saved_img = cv2.imdecode(np.frombuffer(decrypted_image, np.uint8), cv2.IMREAD_GRAYSCALE)

# Load an image from a file
original_img = cv2.imread('/Users/avinash/Desktop/Capstone project/GetEmployeeData/Original_image.jpeg')
resize_original_img = cv2.resize(original_img, (saved_img.shape[1], saved_img.shape[0]), interpolation=cv2.INTER_AREA)
resize_original_img = cv2.cvtColor(resize_original_img, cv2.COLOR_BGR2GRAY)

# Resize the image to (100, 100)
# resize_original_img = cv2.resize(img, (100, 100))

# # Decrypt the image using Fernet and OpenCV
# decrypted_image = cipher_suite.decrypt(encrypted_image)
# # Convert the byte string back to an image array
# saved_img = cv2.imdecode(np.frombuffer(decrypted_image, np.uint8), cv2.IMREAD_GRAYSCALE)
# resized_img = cv2.resize(decrypted_image, ((100, 100)))

print('Original image shape:', resize_original_img.shape)
print('Resized image shape:', saved_img.shape)


# print(result[0])
# print(result[1].shape)

# # decrypted_image = decrypted_image.reshape(img.shape)

# print(result[0])
# print(result[1].tobytes())


# Close the cursor
cur.close()

match_result = cv2.compare(saved_img, resize_original_img, cv2.CMP_EQ)

    # Return the result of the image comparison
# Return the result of the image comparison
if np.all(match_result == 255):
    print("Matched")
else:
    print("Not matched")

cv2.imshow('Saved Image', saved_img)
cv2.imshow('Original Image', resize_original_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# decrypted_image = decrypted_image.reshape(img.shape)


# # Check if the image was loaded successfully
# if decrypted_image is not None:
#     # Display the image
#     cv2.imshow('Image', decrypted_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# else:
#     print('Failed to load image')