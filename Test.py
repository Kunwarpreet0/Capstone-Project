import cv2

# Load the saved image and the resized original image
saved_img = cv2.imread("'/Users/avinash/Desktop/Capstone project/GetEmployeeData/Original_image.jpeg'")
resize_original_img = cv2.imread("'/Users/avinash/Desktop/Capstone project/GetEmployeeData/Original_image.jpeg'")

# Compare the two images pixel-by-pixel
match_result = cv2.compare(saved_img, resize_original_img, cv2.CMP_EQ)

# Check if the images match or not
if cv2.countNonZero(match_result) == 0:
    print("Images match!")
else:
    print("Images do not match.")
