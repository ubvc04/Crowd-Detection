"""
Real-Time Crowd Detection Flask Application
Author: AI Assistant
Description: Web-based crowd detection system with user authentication
"""

from flask import Flask, render_template, Response, request, redirect, url_for, session, jsonify
import cv2
import os
from database.db_utils import register_user, verify_user
import threading

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production!

# Global variables for detection
camera = None
detection_active = False
people_count = 0
alarm_triggered = False

# Haar Cascade for people detection (upper body detection)
# We'll use full body detection for better accuracy
cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'
body_cascade = cv2.CascadeClassifier(cascade_path)

# Alternative: Face detection (more reliable for counting people)
face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(face_cascade_path)


def generate_frames():
    """
    Generate video frames with people detection
    This function runs continuously and yields frames for video streaming
    """
    global camera, people_count, alarm_triggered
    
    # Initialize camera
    camera = cv2.VideoCapture(0)  # 0 for default webcam
    
    while detection_active:
        success, frame = camera.read()
        
        if not success:
            break
        
        # Convert frame to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect people/faces in the frame
        # Using face detection as it's more reliable than full body
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Update people count
        people_count = len(faces)
        
        # Check if alarm should be triggered (more than 2 people)
        if people_count > 2:
            alarm_triggered = True
        else:
            alarm_triggered = False
        
        # Draw rectangles around detected faces/people
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Add text overlay with count and status
        count_text = f'People Count: {people_count}'
        status_text = f'Alarm: {"TRIGGERED!" if alarm_triggered else "OFF"}'
        
        cv2.putText(frame, count_text, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(frame, status_text, (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 
                    (0, 0, 255) if alarm_triggered else (0, 255, 0), 2)
        
        # Encode frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        # Yield frame in byte format for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    # Release camera when done
    if camera:
        camera.release()


@app.route('/')
def home():
    """Home page route"""
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign-up page route - handles user registration"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate input
        if not username or not password:
            return render_template('signup.html', error="All fields are required!")
        
        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match!")
        
        if len(password) < 6:
            return render_template('signup.html', error="Password must be at least 6 characters!")
        
        # Register user
        success, message = register_user(username, password)
        
        if success:
            return render_template('signup.html', success=message)
        else:
            return render_template('signup.html', error=message)
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page route - handles user authentication"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate credentials
        if verify_user(username, password):
            session['user'] = username  # Store username in session
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password!")
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page - only accessible after login"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['user'])


@app.route('/video_feed')
def video_feed():
    """Video streaming route - returns video frames"""
    global detection_active
    
    if 'user' not in session:
        return "Unauthorized", 401
    
    detection_active = True
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_count')
def get_count():
    """API endpoint to get current people count and alarm status"""
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'count': people_count,
        'alarm': alarm_triggered
    })


@app.route('/stop_detection')
def stop_detection():
    """Stop the detection and release camera"""
    global detection_active, camera
    
    detection_active = False
    
    if camera:
        camera.release()
    
    return jsonify({'status': 'stopped'})


@app.route('/logout')
def logout():
    """Logout route - clears session"""
    global detection_active, camera
    
    # Stop detection and release camera
    detection_active = False
    if camera:
        camera.release()
    
    session.pop('user', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    # Run Flask app in debug mode
    app.run(debug=True, host='0.0.0.0', port=5000)
