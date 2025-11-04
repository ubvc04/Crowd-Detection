# 🚀 Quick Start Guide

## Installation (3 Simple Steps)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Add Alarm Sound (IMPORTANT!)
1. Download any alarm MP3 file
2. Rename it to `alarm.mp3`
3. Put it in: `static/sounds/alarm.mp3`

**Skip this if testing without sound**

### Step 3: Run the App
```powershell
python app.py
```

## First Use

1. Open browser: `http://localhost:5000`
2. Click **"Sign Up"** and create account
3. **Login** with your credentials
4. Allow camera access when prompted
5. Watch the live detection dashboard!

## How Detection Works

- System counts people every second
- **10 or less people** → Alarm OFF ✅
- **More than 10 people** → Alarm ON 🔔

## Test It!

Try these scenarios:
- Sit alone: Count = 1, Alarm OFF
- Show photos/screens with multiple faces: Count increases
- Invite friends in front of camera: Test threshold

## Need Help?

- **Camera not working?** Try changing `cv2.VideoCapture(0)` to `(1)` in app.py
- **No sound?** Check if `alarm.mp3` exists in `static/sounds/`
- **Login issues?** Delete `database/users.db` and restart

## Key Files to Know

- `app.py` - Main application (change threshold here)
- `database/db_utils.py` - User authentication
- `templates/dashboard.html` - Main dashboard
- `static/js/dashboard.js` - Real-time updates

---

**That's it! You're ready to go! 🎉**
