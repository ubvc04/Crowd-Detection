# 🎥 Real-Time Crowd Detection System with Alarm

A complete web-based AI-powered crowd detection system built with Flask, OpenCV, and SQLite. The system monitors live camera feeds, counts people in real-time, and triggers an alarm when more than 10 people are detected.

## ✨ Features

- 🔐 **User Authentication**: Secure login/signup system with password hashing
- 📹 **Live Camera Detection**: Real-time webcam feed processing
- 👥 **People Counting**: AI-powered face detection using OpenCV Haar Cascades
- 🔔 **Smart Alarm System**: Automatic alarm triggering when crowd exceeds threshold
- 📊 **Live Dashboard**: Beautiful, animated UI with real-time statistics
- ⚡ **Real-Time Updates**: Count and alarm status update every second
- 🎨 **Modern UI**: Gradient backgrounds, smooth animations, responsive design

## 📁 Project Structure

```
CSP/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── database/
│   ├── db_utils.py            # Database utilities and user management
│   └── users.db               # SQLite database (auto-generated)
├── templates/
│   ├── home.html              # Landing page
│   ├── signup.html            # User registration page
│   ├── login.html             # User login page
│   └── dashboard.html         # Live detection dashboard
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet with animations
│   ├── js/
│   │   ├── dashboard.js       # Dashboard real-time updates
│   │   └── animations.js      # General animations
│   └── sounds/
│       ├── alarm.mp3          # Alarm sound file (add your own)
│       └── README.md          # Instructions for alarm sound
└── README.md                  # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Webcam or external camera
- Windows/Linux/Mac OS

### Step 1: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- OpenCV (computer vision)
- NumPy (numerical computations)

### Step 2: Add Alarm Sound

1. Download an alarm sound file (MP3 format)
2. Rename it to `alarm.mp3`
3. Place it in `static/sounds/` folder

**Free alarm sounds**: [freesound.org](https://freesound.org/), [mixkit.co](https://mixkit.co/free-sound-effects/alarm/)

### Step 3: Run the Application

```powershell
python app.py
```

The application will start on `http://localhost:5000`

## 📖 Usage Guide

### First Time Setup

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Sign Up**: Click "Sign Up" and create a new account
3. **Login**: Use your credentials to log in
4. **Dashboard**: You'll be redirected to the live detection dashboard

### Using the Detection System

1. **Camera Permission**: Allow browser access to your webcam
2. **Live Feed**: The camera feed will display with detection rectangles
3. **People Count**: See real-time count of detected people
4. **Alarm Status**: Monitor alarm status (triggers at 10+ people)
5. **Threshold Bar**: Visual indicator of current count vs threshold

### Understanding the Dashboard

- **Live Camera Feed**: Shows real-time video with detection boxes
- **People Detected**: Current count updated every second
- **Alarm Status**: Shows if alarm is active or off
- **Threshold Indicator**: Progress bar showing proximity to alarm threshold
- **System Information**: Details about detection settings

## 🔧 How It Works

### Authentication System (`database/db_utils.py`)
- SQLite database stores user credentials
- Passwords are hashed using SHA-256 for security
- Session-based authentication with Flask sessions

### Video Detection (`app.py`)
```python
# Detection Process (every frame):
1. Capture frame from webcam
2. Convert to grayscale
3. Apply Haar Cascade face detection
4. Count detected faces
5. Draw rectangles around faces
6. Check if count > 10
7. Trigger alarm if threshold exceeded
8. Stream frame to web interface
```

### Real-Time Updates (`static/js/dashboard.js`)
- JavaScript polls `/get_count` endpoint every 1 second
- Updates people count display
- Controls alarm audio playback
- Updates visual indicators (threshold bar, alarm card)

### Alarm Logic
```javascript
if (people_count > 10) {
    alarm_triggered = True
    play_alarm_sound()
} else {
    alarm_triggered = False
    stop_alarm_sound()
}
```

## 🎨 UI Features

- **Animated Background**: Floating gradient circles
- **Smooth Transitions**: Fade-in animations for all elements
- **Responsive Design**: Works on desktop and mobile
- **Color-Coded Alerts**: Visual feedback for alarm status
- **Live Progress Bar**: Shows crowd density relative to threshold

## 🔒 Security Features

- ✅ Password hashing with SHA-256
- ✅ Session-based authentication
- ✅ Protected routes (login required for dashboard)
- ✅ SQL injection prevention with parameterized queries
- ✅ Secure session secret key (change in production!)

## ⚙️ Configuration

### Change Alarm Threshold
In `app.py`, modify line:
```python
if people_count > 10:  # Change 10 to your desired threshold
    alarm_triggered = True
```

### Change Detection Method
Replace face detection with full-body detection in `app.py`:
```python
# Use body cascade instead of face cascade
faces = body_cascade.detectMultiScale(...)
```

### Adjust Detection Sensitivity
Modify parameters in `app.py`:
```python
faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,      # Lower = more sensitive
    minNeighbors=5,       # Lower = more detections
    minSize=(30, 30)      # Minimum face size
)
```

## 🐛 Troubleshooting

### Camera not working
- Check if another application is using the webcam
- Try changing camera index in `app.py`: `cv2.VideoCapture(1)` or `(2)`
- Grant camera permissions in browser settings

### Alarm not playing
- Ensure `alarm.mp3` exists in `static/sounds/` folder
- Check browser audio permissions
- Try a different audio format (WAV instead of MP3)

### Low detection accuracy
- Ensure good lighting conditions
- Face camera directly
- Adjust `minNeighbors` and `scaleFactor` parameters
- Try different Haar Cascade models

### Database errors
- Delete `database/users.db` and restart app
- Check file permissions in `database/` folder

## 📝 Code Comments

All code files include detailed comments explaining:
- Function purposes and parameters
- Logic flow and algorithms
- Security considerations
- Configuration options

## 🔄 Update Frequency

The system updates detection every **1 second**:
- Video frames: Continuous (30 FPS)
- People count check: Every 1 second
- Dashboard updates: Every 1 second
- Alarm check: Every 1 second

## 🚀 Future Enhancements

Possible improvements:
- Add person tracking (unique ID for each person)
- Historical data logging and analytics
- Email/SMS notifications when alarm triggers
- Multiple camera support
- Custom threshold settings per user
- Export detection logs to CSV
- Integration with external alarm systems

## 📄 License

This project is created for educational purposes. Feel free to modify and use as needed.

## 👨‍💻 Author

Created by AI Assistant for crowd monitoring and safety applications.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review code comments in respective files
3. Ensure all dependencies are installed correctly
4. Verify camera and audio permissions

---

**Important**: Change the `app.secret_key` in `app.py` before deploying to production!

**Note**: The alarm sound file (`alarm.mp3`) must be added manually as it's not included in the repository.
