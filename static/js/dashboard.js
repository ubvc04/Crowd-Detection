/*
   Dashboard JavaScript
   Handles real-time people count updates and alarm control
*/

// Audio element for alarm
const alarmSound = document.getElementById('alarmSound');
let isAlarmPlaying = false;
let audioContext = null;
let oscillator = null;
let gainNode = null;

// Initialize Web Audio API for fallback beep sound
function initWebAudio() {
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    } catch (e) {
        console.error('Web Audio API not supported:', e);
    }
}

// Update count and alarm status every second
function updateDetectionStatus() {
    fetch('/get_count')
        .then(response => response.json())
        .then(data => {
            // Update people count display
            const countElement = document.getElementById('peopleCount');
            countElement.textContent = data.count;
            
            // Update alarm status
            const alarmCard = document.getElementById('alarmCard');
            const alarmStatus = document.getElementById('alarmStatus');
            const alarmText = document.getElementById('alarmText');
            
            if (data.alarm) {
                // Alarm should be triggered
                alarmStatus.textContent = 'ACTIVE!';
                alarmText.textContent = 'More than 5 people detected!';
                alarmCard.classList.add('alarm-active');
                
                // Play alarm sound if not already playing
                if (!isAlarmPlaying) {
                    playAlarm();
                }
            } else {
                // Alarm should be off
                alarmStatus.textContent = 'OFF';
                alarmText.textContent = 'Monitoring...';
                alarmCard.classList.remove('alarm-active');
                
                // Stop alarm sound if playing
                if (isAlarmPlaying) {
                    stopAlarm();
                }
            }
            
            // Update threshold bar
            updateThresholdBar(data.count);
        })
        .catch(error => {
            console.error('Error fetching detection status:', error);
        });
}

// Play alarm sound
function playAlarm() {
    // Try to play the alarm.mp3 file first
    if (alarmSound && alarmSound.src) {
        alarmSound.play()
            .then(() => {
                isAlarmPlaying = true;
                console.log('Alarm started (audio file)');
            })
            .catch(error => {
                console.warn('Audio file not available, using beep fallback:', error);
                // Fallback to beep sound
                playBeepAlarm();
            });
    } else {
        // No audio file, use beep fallback
        console.log('No alarm.mp3 found, using beep fallback');
        playBeepAlarm();
    }
}

// Fallback beep alarm using Web Audio API
function playBeepAlarm() {
    if (!audioContext) {
        initWebAudio();
    }
    
    if (audioContext && !oscillator) {
        try {
            // Create oscillator for beep sound
            oscillator = audioContext.createOscillator();
            gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // Set alarm sound properties (alternating beep)
            oscillator.type = 'sine';
            oscillator.frequency.value = 800; // 800 Hz beep
            gainNode.gain.value = 0.3; // 30% volume
            
            oscillator.start();
            isAlarmPlaying = true;
            
            // Modulate frequency for siren effect
            let isHigh = true;
            setInterval(() => {
                if (isAlarmPlaying && oscillator) {
                    oscillator.frequency.value = isHigh ? 800 : 600;
                    isHigh = !isHigh;
                }
            }, 500); // Alternate every 500ms
            
            console.log('Beep alarm started');
        } catch (error) {
            console.error('Error creating beep alarm:', error);
        }
    }
}

// Stop alarm sound
function stopAlarm() {
    // Stop audio file if playing
    if (alarmSound) {
        alarmSound.pause();
        alarmSound.currentTime = 0;
    }
    
    // Stop beep sound if playing
    if (oscillator) {
        try {
            oscillator.stop();
            oscillator.disconnect();
            oscillator = null;
            if (gainNode) {
                gainNode.disconnect();
                gainNode = null;
            }
        } catch (error) {
            console.error('Error stopping beep:', error);
        }
    }
    
    isAlarmPlaying = false;
    console.log('Alarm stopped');
}

// Update threshold bar visualization
function updateThresholdBar(count) {
    const thresholdFill = document.getElementById('thresholdFill');
    const thresholdText = document.getElementById('thresholdText');
    
    // Calculate percentage (threshold is 5)
    const percentage = Math.min((count / 5) * 100, 100);
    
    thresholdFill.style.width = percentage + '%';
    thresholdText.textContent = `Current: ${percentage.toFixed(0)}% of threshold`;
    
    // Change color when approaching threshold
    if (count > 3) {
        thresholdFill.classList.add('warning');
    } else {
        thresholdFill.classList.remove('warning');
    }
}

// Start updating every 1 second
setInterval(updateDetectionStatus, 1000);

// Initial update
updateDetectionStatus();

// Initialize Web Audio on page load
initWebAudio();

// Stop detection when leaving page
window.addEventListener('beforeunload', function() {
    stopAlarm(); // Ensure alarm is stopped
    fetch('/stop_detection')
        .catch(error => console.error('Error stopping detection:', error));
});
