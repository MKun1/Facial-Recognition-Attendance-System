# Facial Recognition Attendance System

## Overview
The **Facial Recognition Attendance System** is a Python-based application that automates attendance management using facial recognition technology. This system eliminates the need for manual attendance tracking and provides a reliable, efficient, and secure solution for educational institutions, workplaces, or any environment where attendance tracking is essential.

## Features
- **Real-Time Facial Recognition**: Detect and recognize faces using a live webcam feed.
- **Attendance Logging**: Automatically logs attendance data with timestamps.
- **Database Integration**: Stores user data and attendance records in a structured database.
- **Admin Dashboard**: View and manage attendance records.
- **CSV Export**: Export attendance reports for further analysis.
- **User Registration**: Add new users with facial data.

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - OpenCV: For face detection and recognition.
  - dlib: For facial landmark detection.
  - NumPy: For numerical operations.
  - pandas: For data manipulation.
  - SQLite3: For database management.
- **Optional Hardware**: A standard webcam or an external camera.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/facial-recognition-attendance.git
   cd facial-recognition-attendance
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```


3. **Download Pre-trained Models**:
   - Download the facial landmark predictor (`shape_predictor_68_face_landmarks.dat`) and face recognition model (`dlib_face_recognition_resnet_model_v1.dat`) from the [dlib website](http://dlib.net/).
   - Place these files in the `models/` directory.

6. **Run the Script**:
   ```bash
   python main.py
   ```

## Usage
1. **Register Users**:
   - Place user's picture in ImagesAttendance folder to capture and store user facial data.
   - Each user will be associated with a unique ID.

2. **Start Attendance System**:
   - Launch the application and enable the live webcam feed.
   - The system will automatically recognize faces and log attendance.

3. **View Attendance Records**:
   - Access the admin dashboard to view and export attendance logs.


## Future Enhancements
- Add support for multi-camera setups.
- Implement cloud-based storage for attendance records.
- Integrate with existing Learning Management Systems (LMS).
- Enhance the UI/UX of the admin dashboard.

## Contributing
We welcome contributions from the community! To contribute:
1. Fork this repository.
2. Create a new branch for your feature/bugfix.
3. Submit a pull request with a detailed explanation of your changes.

## License
This project is licensed under the [MIT License](LICENSE).

## Acknowledgments
- The dlib library for its powerful facial recognition capabilities.
- OpenCV for image and video processing.
- The open-source community for their invaluable resources and contributions.

---
Feel free to raise issues or submit pull requests to improve this project!

