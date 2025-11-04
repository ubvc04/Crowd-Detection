"""
Generate a simple alarm sound for testing
Run this script to create alarm.wav if you don't have an alarm file
"""

import math
import wave
import struct

def generate_alarm_sound(filename='static/sounds/alarm.wav', duration=2):
    """
    Generate a simple beep alarm sound
    """
    sample_rate = 44100  # samples per second
    frequency1 = 800  # Hz (high beep)
    frequency2 = 600  # Hz (low beep)
    
    # Calculate samples
    num_samples = int(sample_rate * duration)
    
    # Generate alternating beeps
    samples = []
    beep_duration = 0.5  # seconds per beep
    beep_samples = int(sample_rate * beep_duration)
    
    for i in range(num_samples):
        # Alternate between two frequencies every 0.5 seconds
        if (i // beep_samples) % 2 == 0:
            frequency = frequency1
        else:
            frequency = frequency2
        
        # Generate sine wave
        value = math.sin(2 * math.pi * frequency * i / sample_rate)
        
        # Convert to 16-bit integer
        samples.append(int(value * 32767))
    
    # Write to WAV file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters: 1 channel (mono), 2 bytes per sample, sample rate
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        # Write samples
        for sample in samples:
            wav_file.writeframes(struct.pack('h', sample))
    
    print(f"✅ Alarm sound generated: {filename}")
    print(f"   Duration: {duration} seconds")
    print(f"   Sample rate: {sample_rate} Hz")

if __name__ == '__main__':
    import os
    
    # Create sounds directory if it doesn't exist
    os.makedirs('static/sounds', exist_ok=True)
    
    # Generate alarm sound
    generate_alarm_sound()
    print("\n🔊 You can now use this alarm.wav file in your application!")
    print("   Or replace it with any alarm.mp3 or alarm.wav file you prefer.")
