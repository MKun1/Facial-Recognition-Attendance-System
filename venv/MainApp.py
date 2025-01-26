import sys
import cv2
import csv
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from FacialRecUI import Ui_MainWindow  # Import the generated UI file
from AttendanceProject import findEncoding, markAttendance, process_frame  # Import functions from the logic file

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Load the UI setup

        # Webcam feed and attendance table setup
        self.timer = QtCore.QTimer(self)
        self.cap = None  # To hold the video capture instance

        # Load known face encodings
        self.images = []  # List to hold images loaded from the folder
        self.classNames = []  # List to hold names corresponding to each image
        self.path = '../ImagesAttendance'
        myList = os.listdir(self.path)  # Get a list of all files in the directory
        for cl in myList:
            curImg = cv2.imread(f'{self.path}/{cl}')
            self.images.append(curImg)  # Append the loaded image to the images list
            self.classNames.append(os.path.splitext(cl)[0])  # Add the name to the classNames list

        self.encodeListKnown = findEncoding(self.images)  # Generate face encodings for the known faces

        # Link buttons to their functionalities
        self.ui.openwebcambutton.clicked.connect(self.start_webcam)
        self.ui.closewebcambutton.clicked.connect(self.stop_webcam)
        self.ui.exitprogbtn.clicked.connect(self.exit_application)

        # Set up the attendance table
        self.setup_attendance_table()

        # Timer for updating attendance table
        self.table_timer = QtCore.QTimer(self)
        self.table_timer.timeout.connect(self.update_attendance_table)
        self.table_timer.start(5000)  # Refresh the table every 5 seconds

        # Link right-click to remove attendance record
        self.ui.AttendanceTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.AttendanceTable.customContextMenuRequested.connect(self.open_context_menu)

    def setup_attendance_table(self):
        # Configure attendance table headers
        self.ui.AttendanceTable.setColumnCount(2)
        self.ui.AttendanceTable.setHorizontalHeaderLabels(["Name", "Time"])
        self.ui.AttendanceTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.ui.AttendanceTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

    def update_attendance_table(self):
        # Populate the attendance table with the latest CSV data
        self.ui.AttendanceTable.setRowCount(0)  # Clear the table
        try:
            with open('../attendancelog.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    row_index = self.ui.AttendanceTable.rowCount()
                    self.ui.AttendanceTable.insertRow(row_index)
                    for column_index, data in enumerate(row):
                        self.ui.AttendanceTable.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(data))
        except FileNotFoundError:
            print("Attendance log file not found.")

    def start_webcam(self):
        # Start the webcam and display frames in the QLabel
        if not self.cap:
            self.cap = cv2.VideoCapture(0)  # Use default webcam
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return
        self.timer.timeout.connect(self.display_webcam_feed)
        self.timer.start(30)  # Set frame refresh rate (30ms for ~30 FPS)

    def stop_webcam(self):
        # Stop the webcam feed
        if self.cap:
            self.timer.stop()
            self.cap.release()
            self.cap = None
        self.ui.WebCamDisplay.clear()  # Clear the QLabel

    def display_webcam_feed(self):
        # Capture frame and process it for face recognition
        ret, frame = self.cap.read()
        if ret:
            frame = process_frame(frame)  # Process frame for face recognition and attendance marking

            # Convert processed frame to QPixmap and display it on the QLabel
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            q_image = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
            self.ui.WebCamDisplay.setPixmap(QtGui.QPixmap.fromImage(q_image))
        else:
            print("Error: Failed to capture frame.")

    def exit_application(self):
        # Close the application safely
        self.stop_webcam()
        QtWidgets.QApplication.quit()

    def closeEvent(self, event):
        # Ensure resources are released when the window is closed
        self.stop_webcam()
        super().closeEvent(event)

    def open_context_menu(self, pos):
        context_menu = QtWidgets.QMenu(self)

        # Add "Remove Record" action to the context menu
        remove_action = context_menu.addAction("Remove Record")
        action = context_menu.exec_(self.ui.AttendanceTable.mapToGlobal(pos))

        if action == remove_action:
            self.remove_selected_record()

    def remove_selected_record(self):
        # Get selected row
        selected_row = self.ui.AttendanceTable.currentRow()
        if selected_row != -1:
            name_to_remove = self.ui.AttendanceTable.item(selected_row, 0).text()  # Get name from the first column
            self.remove_from_csv(name_to_remove)  # Remove record from CSV
            self.update_attendance_table()  # Refresh table to reflect changes

    def remove_from_csv(self, name):
        # Remove the entry with the matching name from the attendance CSV
        try:
            with open('../attendancelog.csv', 'r+') as file:
                lines = file.readlines()
                file.seek(0)
                file.truncate()  # Clear the file
                # Write back all lines except the ones with the name to be removed
                for line in lines:
                    if not line.startswith(name):
                        file.write(line)
        except FileNotFoundError:
            print("Attendance log file not found.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec_())
