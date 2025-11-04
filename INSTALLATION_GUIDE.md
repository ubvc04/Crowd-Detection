# 🚀 Complete Installation & Running Guide

## 📋 Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager)
- ✅ Working webcam
- ✅ Modern web browser (Chrome, Firefox, Edge)
- ✅ Internet connection (for initial package download)

---

## 🔧 Installation Steps

### Step 1: Navigate to Project Directory

Open PowerShell and navigate to the project folder:

```powershell
cd "c:\Users\baves\Downloads\CSP"
```

---

### Step 2: Install Required Packages

Install all dependencies from requirements.txt:

```powershell
pip install -r requirements.txt
```

**Expected Output:**
```
Collecting Flask==3.0.0
  Downloading Flask-3.0.0...
Collecting opencv-python==4.8.1.78
  Downloading opencv_python-4.8.1.78...
Collecting numpy==1.24.3
  Downloading numpy-1.24.3...
Successfully installed Flask-3.0.0 opencv-python-4.8.1.78 numpy-1.24.3 Werkzeug-3.0.1
```

**If you get errors:**
- Update pip: `python -m pip install --upgrade pip`
- Or install individually:
  ```powershell
  pip install Flask
  pip install opencv-python
  pip install numpy
  ```

---

### Step 3: Add Alarm Sound File (IMPORTANT!)

⚠️ **The app needs an alarm sound to work properly!**

**Option A: Download from Free Sources**
1. Visit: https://freesound.org/ or https://mixkit.co/free-sound-effects/alarm/
2. Download any alarm/siren sound
3. Rename it to `alarm.mp3`
4. Place in: `c:\Users\baves\Downloads\CSP\static\sounds\alarm.mp3`

**Option B: Use Windows Built-in Sound**
1. Go to: `C:\Windows\Media\`
2. Copy any `.wav` file (e.g., `Alarm01.wav`)
3. Convert to MP3 (or modify dashboard.html to use .wav)
4. Place in: `static\sounds\alarm.mp3`

**Option C: Skip for Testing**
- The app will run without sound
- You'll see visual alarm indicators only
- Audio won't play (but won't crash)

---

### Step 4: Verify File Structure

Ensure your project looks like this:

```
CSP/
├── app.py ✅
├── requirements.txt ✅
├── database/
│   ├── __init__.py ✅
│   └── db_utils.py ✅
├── templates/
│   ├── home.html ✅
│   ├── signup.html ✅
│   ├── login.html ✅
│   └── dashboard.html ✅
└── static/
    ├── css/style.css ✅
    ├── js/
    │   ├── dashboard.js ✅
    │   └── animations.js ✅
    └── sounds/
        └── alarm.mp3 ⚠️ (ADD THIS!)
```

---

## ▶️ Running the Application

### Start the Flask Server

In PowerShell, run:

```powershell
python app.py
```

**Expected Output:**
```
Database initialized successfully!
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in production.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.x.x:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

✅ **Success!** Your server is now running!

---

## 🌐 Accessing the Application

### Step 1: Open Your Browser

Open any modern browser and go to:
```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

---

### Step 2: Home Page

You should see:
- **Title**: "🎥 Real-Time Crowd Detection System"
- **Subtitle**: "AI-Powered People Counting with Smart Alarm"
- **Features**: Live Detection, Smart Alerts, Secure Access
- **Buttons**: "Login" and "Sign Up"
- **Animated background** with floating gradient circles

---

### Step 3: Create an Account

1. Click **"Sign Up"** button
2. Fill in the form:
   - **Username**: Choose any username (e.g., "admin")
   - **Password**: Enter password (min 6 characters)
   - **Confirm Password**: Re-enter same password
3. Click **"Sign Up"**

**Success Message:**
```
✅ Registration successful! Login now
```

---

### Step 4: Login

1. Click **"Login here"** link or go back to home and click "Login"
2. Enter your credentials:
   - **Username**: Your username
   - **Password**: Your password
3. Click **"Login"**

**You'll be redirected to the dashboard!**

---

## 📊 Using the Dashboard

### What You'll See:

#### Header (Top)
- **Left**: "🎥 Live Crowd Detection"
- **Right**: "Welcome, [your-username]" + "Logout" button

#### Main Area (Left Side)
- **Live Camera Feed**
  - Real-time video from your webcam
  - Green rectangles around detected faces
  - Text overlay showing count and alarm status

#### Statistics Panel (Right Side)

1. **People Detected Card**
   - Large number showing current count
   - Updates every second
   - Pulsing animation

2. **Alarm Status Card**
   - Shows "OFF" when count ≤ 10 (green)
   - Shows "ACTIVE!" when count > 10 (red, pulsing)
   - "Monitoring..." or "More than 10 people detected!"

3. **System Information Card**
   - Detection updates every second
   - Alarm triggers at 10+ people
   - Real-time count display
   - AI-powered face detection

4. **Threshold Settings Card**
   - Visual progress bar
   - Shows current percentage of threshold
   - Changes color when approaching limit

---

## 🧪 Testing the System

### Test 1: Solo Detection
1. Sit in front of camera alone
2. **Expected**: Count = 1, Alarm OFF, green status

### Test 2: Multiple People
1. Have friends join you OR
2. Show photos/screens with faces to camera
3. **Expected**: Count increases, alarm triggers at >10

### Test 3: Alarm Trigger
1. Get 11+ people/faces in view
2. **Expected**: 
   - Count shows 11+
   - Alarm status card turns red
   - "ACTIVE!" displayed
   - Alarm sound plays (if alarm.mp3 exists)
   - Pulsing animation on alarm card

### Test 4: Alarm Stop
1. Reduce people to 10 or less
2. **Expected**:
   - Count decreases
   - Alarm status turns green
   - Shows "OFF"
   - Alarm sound stops
   - Animation stops

---

## 🎯 How It Works (Behind the Scenes)

### Every Second:

1. **Camera Capture**: OpenCV grabs frame from webcam
2. **Face Detection**: Haar Cascade detects all faces
3. **Counting**: System counts number of faces
4. **Threshold Check**: Compares count to 10
5. **Alarm Decision**:
   - If count > 10: Set alarm = TRUE
   - If count ≤ 10: Set alarm = FALSE
6. **UI Update**: JavaScript fetches current status
7. **Audio Control**: Play/stop alarm based on status
8. **Visual Feedback**: Update all indicators

### Detection Process:
```
Frame → Grayscale → Haar Cascade → Face Locations → Count
→ Draw Rectangles → Check Threshold → Trigger Alarm → Stream to Browser
```

---

## 🛑 Stopping the Application

### Method 1: Using Terminal
Press **Ctrl + C** in PowerShell where app is running

**Expected Output:**
```
^C
 * Detected change in 'app.py', reloading
```

### Method 2: Close Terminal
Simply close the PowerShell window

### Method 3: From Browser
Click **"Logout"** button (recommended to clean up session)

---

## ⚠️ Troubleshooting

### Problem: Camera not working

**Error**: Black screen or "No camera" message

**Solutions**:
1. Check if another app is using camera (Zoom, Teams, etc.)
2. Close those apps and refresh browser
3. Try different camera index in `app.py`:
   ```python
   camera = cv2.VideoCapture(1)  # or 2, 3, etc.
   ```
4. Grant camera permission in browser settings

---

### Problem: Alarm not playing

**Error**: Alarm triggers visually but no sound

**Solutions**:
1. Verify `alarm.mp3` exists in `static/sounds/`
2. Check browser audio permissions
3. Unmute your system volume
4. Try different audio format (WAV instead of MP3)
5. Check browser console (F12) for audio errors

---

### Problem: Login not working

**Error**: "Invalid username or password"

**Solutions**:
1. Ensure you created account first (Sign Up)
2. Check username spelling (case-sensitive)
3. Re-register if needed
4. Delete `database/users.db` and restart app (fresh database)

---

### Problem: Low detection accuracy

**Error**: Not detecting all faces or too many false positives

**Solutions**:
1. Improve lighting (face camera toward light)
2. Ensure face is fully visible (no obstructions)
3. Adjust detection parameters in `app.py`:
   ```python
   faces = face_cascade.detectMultiScale(
       gray,
       scaleFactor=1.05,  # Try: 1.05, 1.1, 1.2
       minNeighbors=3,    # Try: 3, 4, 5, 6
       minSize=(20, 20)   # Try: (20,20), (30,30), (40,40)
   )
   ```

---

### Problem: App crashes on start

**Error**: Import errors or module not found

**Solutions**:
1. Reinstall dependencies:
   ```powershell
   pip uninstall Flask opencv-python numpy
   pip install -r requirements.txt
   ```
2. Check Python version: `python --version` (need 3.8+)
3. Try: `python -m pip install --upgrade pip`

---

### Problem: Port already in use

**Error**: "Address already in use"

**Solutions**:
1. Stop other Flask apps running on port 5000
2. Change port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```
3. Kill process using port 5000:
   ```powershell
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

---

## 📱 Browser Compatibility

| Browser | Status | Notes |
|---------|--------|-------|
| Chrome | ✅ Fully Supported | Best performance |
| Edge | ✅ Fully Supported | Recommended |
| Firefox | ✅ Fully Supported | Good performance |
| Safari | ⚠️ Partial | Audio might need user interaction |
| Opera | ✅ Supported | Works well |

---

## 💡 Tips for Best Results

1. **Lighting**: Ensure good, even lighting on faces
2. **Camera Position**: Place camera at eye level
3. **Background**: Plain background works best
4. **Distance**: Stay 2-6 feet from camera
5. **Audio**: Use headphones for alarm testing
6. **Browser**: Use Chrome or Edge for best compatibility
7. **Refresh**: If issues occur, refresh browser page

---

## 🎓 Understanding the Code

### Want to modify the threshold?

**File**: `app.py`, Line ~61
```python
if people_count > 10:  # CHANGE THIS NUMBER
    alarm_triggered = True
```

Example: Change to 5 for smaller crowds:
```python
if people_count > 5:
    alarm_triggered = True
```

---

### Want faster updates?

**File**: `static/js/dashboard.js`, Line ~87
```javascript
setInterval(updateDetectionStatus, 1000);  // CHANGE 1000 (1 second)
```

Example: Update every 500ms:
```javascript
setInterval(updateDetectionStatus, 500);
```

---

### Want different detection?

**File**: `app.py`, Line ~24
```python
# Change from face to full body:
cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.xml'
```

---

## 🎉 Success Checklist

- [ ] Dependencies installed without errors
- [ ] alarm.mp3 file added to sounds folder
- [ ] App starts successfully
- [ ] Browser loads home page
- [ ] Can create new account
- [ ] Can log in successfully
- [ ] Camera feed displays on dashboard
- [ ] Can see face detection rectangles
- [ ] People count updates in real-time
- [ ] Alarm status changes at threshold
- [ ] Audio plays when triggered (if sound file added)
- [ ] Threshold bar updates correctly
- [ ] Can log out successfully

---

## 📞 Need More Help?

1. **Check README.md** - Full documentation
2. **Check PROJECT_SUMMARY.md** - Feature overview
3. **Check code comments** - Every file is documented
4. **Browser Console** - F12 for error messages
5. **Terminal Output** - Check for Flask errors

---

**Your Real-Time Crowd Detection System is ready! 🚀**

**Enjoy monitoring crowds with AI! 🎉**
