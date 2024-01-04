#!/usr/bin/env python3
import os
import subprocess
import sounddevice as sd
import numpy as np

# Constants
SAMPLING_RATE = 44100  # Sample rate in Hertz
THRESHOLD_HIGH = 0.05  # Arbitrary high noise level threshold
THRESHOLD_LOW = 0.02  # Arbitrary low noise level threshold
NOISE_TIME_REQUIRED = 2 * SAMPLING_RATE  # Frames noise level must be exceeded
QUIET_TIME_REQUIRED = 2 * SAMPLING_RATE  # Frames noise level must be below threshold

def calculate_rms(indata):
    """Calculate the RMS (volume level) of the current audio frame."""
    return np.sqrt(np.mean(indata**2))

def check_thresholds(rms_value):
    """Determine if current RMS value is above or below set thresholds."""
    return rms_value >= THRESHOLD_HIGH, rms_value <= THRESHOLD_LOW

def update_frame_counters(is_above_high, is_below_low, noise_frames, quiet_frames, SAMPLING_RATE):
    """Update frame counters based on threshold checks."""
    if is_above_high:
        return noise_frames + SAMPLING_RATE, 0  # Reset quiet counter
    if is_below_low:
        return noise_frames, quiet_frames + SAMPLING_RATE
    return noise_frames, quiet_frames

def sound_event_detected(noise_duration_frames, quiet_duration_frames):
    """Triggers when the noise threshold is exceeded, then falls below another threshold."""
    # Implement notification logic here?
    wav_file_path = os.path.join(os.path.expanduser('~'), 'success.wav')
    # Play the .wav file
    try:
        subprocess.run(['aplay', wav_file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error playing sound: {e}")

def monitor_audio_thresholds():
    noise_frames = 0
    quiet_frames = 0
    noise_detected = False

    def callback(indata, frames, time, status):
        nonlocal noise_frames, quiet_frames, noise_detected
        
        # Check for errors
        if status:
            print(status)

        # Record volume level and check against thresholds
        rms_value = calculate_rms(indata)
        is_above_high, is_below_low = check_thresholds(rms_value)
        # Record frame counts for both thresholds
        noise_frames, quiet_frames = update_frame_counters(is_above_high, is_below_low, noise_frames, quiet_frames, SAMPLING_RATE)

        # Check for the first notification condition
        if is_above_high and noise_frames >= NOISE_TIME_REQUIRED:
            noise_detected = True

        # Notifications triggered here if both conditions are met
        if noise_detected and quiet_frames >= QUIET_TIME_REQUIRED:
            sound_event_detected(noise_frames, quiet_frames)
            noise_frames = 0
            quiet_frames = 0
            noise_detected = False

    with sd.InputStream(callback=callback, samplerate=SAMPLING_RATE, channels=1):
        while True:
            sd.sleep(1000)

monitor_audio_thresholds()

