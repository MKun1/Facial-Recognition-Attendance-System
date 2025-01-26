import cv2  # OpenCV library for image processing and video capture
import numpy as np  # NumPy library for numerical operations
import face_recognition  # Library for face detection and recognition
import sys
import os  # Library for interacting with the operating system
from datetime import datetime  # Library to handle date and time
from concurrent.futures import ThreadPoolExecutor  # For multithreading to speed up processing

# Path to the folder containing the images of known faces
path = '../ImagesAttendance'



images = []  # List to hold images loaded from the folder
classNames = []  # List to hold names corresponding to each image
myList = os.listdir(path)  # Get a list of all files in the directory specified by 'path'
print(myList)

# Loop through each image in the directory to load it and extract the name
for cl in myList:
    # Read each image using OpenCV
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)  # Append the loaded image to the images list
    # Extract the file name (without extension) and add to classNames list
    classNames.append(os.path.splitext(cl)[0])
print(classNames)  # Print all loaded names for verification


# Function to encode faces - takes a list of images and returns a list of encodings
def findEncoding(images):
    encodelist = []  # Initialize an empty list to store encodings
    for img in images:
        # Convert image color from BGR (OpenCV format) to RGB (face_recognition format)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Get the encoding for each face found in the image
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)  # Add encoding to list
    return encodelist  # Return the list of encodings


# Function to mark attendance by logging the recognized name and timestamp
def markAttendance(name):
    with open('../attendancelog.csv', 'r+') as f:
        myDatalist = f.readlines()  # Read all lines from the attendance log file
        namelist = [line.split(',')[0] for line in myDatalist]  # List of names already marked

        # If name is not already marked, append it to the attendance file
        if name not in namelist:
            now = datetime.now()  # Get current date and time
            datestring = now.strftime('%H:%M:%S')  # Format time as hours, minutes, seconds
            f.writelines(f'\n{name},{datestring}')  # Write new attendance record to file


# Generate encodings for all known faces loaded from the directory
encodeListKnown = findEncoding(images)
print("Encoding Complete:", len(encodeListKnown))  # Confirm the number of encodings


# # Initialize webcam feed (using device index 1 for external webcams or 0 for default webcam)
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS, 30)  # Set the webcam frame rate (if supported by the camera)
#
# # Check if the webcam opened successfully
# if not cap.isOpened():
#     print("Error: Could not open webcam.")
#     exit()
#

# Function to process each frame, detects and recognizes faces
def process_frame(img):
    # Resize the frame to 1/4 of original size to increase processing speed
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # Convert resized frame to RGB format for compatibility with face_recognition
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect face locations in the current frame
    faceCurFrame = face_recognition.face_locations(imgS)
    # Get the encoding for each face found in the current frame
    encodingCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Loop through each detected face and its corresponding encoding
    for encodeFace, faceLoc in zip(encodingCurFrame, faceCurFrame):
        # Check if the face encoding matches any known faces
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        # Calculate the distance to each known face
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchindex = np.argmin(faceDis)  # Find the closest match

        # If the closest match is below a certain threshold, mark attendance
        if faceDis[matchindex] < 0.50:
            name = classNames[matchindex].upper()  # Get the name of the matched face
            markAttendance(name)  # Mark the recognized person's attendance
        else:
            name = 'Unknown'  # Label as unknown if no match is found

        # Scale up the face location coordinates to match the original frame size
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        # Draw a rectangle around the detected face in the original frame
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Draw a filled rectangle for name label
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        # Write the name below the rectangle
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    return img  # Return the processed frame with drawn rectangles and labels


# # Initialize a thread pool to process frames in parallel
#
# with ThreadPoolExecutor() as executor:
#     while True:
#         # Capture a frame from the webcam
#         success, img = cap.read()
#         if not success:
#             print("Error: Could not read frame from webcam.")
#             break
#
#         # Submit the frame to the thread pool for processing
#         future = executor.submit(process_frame, img)
#         img = future.result()  # Get the processed frame from the thread
#
#         # Display the processed frame with face recognition annotations
#         cv2.imshow("Webcam", img)
#
#         # Exit the loop if 'q' key is pressed
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
# # Release the webcam and close display windows
# cap.release()
# cv2.destroyAllWindows()

