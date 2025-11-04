/*
   Dashboard JavaScript
   Handles real-time people count updates and alarm control
*/

// Audio element for alarm
const alarmSound = document.getElementById('alarmSound');
let isAlarmPlaying = false;

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
                alarmText.textContent = 'More than 2 people detected!';
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
    if (alarmSound) {
        alarmSound.play()
            .then(() => {
                isAlarmPlaying = true;
                console.log('Alarm started');
            })
            .catch(error => {
                console.error('Error playing alarm:', error);
            });
    }
}

// Stop alarm sound
function stopAlarm() {
    if (alarmSound) {
        alarmSound.pause();
        alarmSound.currentTime = 0;
        isAlarmPlaying = false;
        console.log('Alarm stopped');
    }
}

// Update threshold bar visualization
function updateThresholdBar(count) {
    const thresholdFill = document.getElementById('thresholdFill');
    const thresholdText = document.getElementById('thresholdText');
    
    // Calculate percentage (threshold is 2)
    const percentage = Math.min((count / 2) * 100, 100);
    
    thresholdFill.style.width = percentage + '%';
    thresholdText.textContent = `Current: ${percentage.toFixed(0)}% of threshold`;
    
    // Change color when approaching threshold
    if (count > 1) {
        thresholdFill.classList.add('warning');
    } else {
        thresholdFill.classList.remove('warning');
    }
}

// Start updating every 1 second
setInterval(updateDetectionStatus, 1000);

// Initial update
updateDetectionStatus();

// Stop detection when leaving page
window.addEventListener('beforeunload', function() {
    fetch('/stop_detection')
        .catch(error => console.error('Error stopping detection:', error));
});
