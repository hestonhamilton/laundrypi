#!/usr/bin/env python3
import os
import subprocess
import sounddevice as sd
import numpy as np

# Constants
SAMPLING_RATE = 44100  # Sample rate in Hertz
THRESHOLD_HIGH = 0.01  # High noise level threshold
THRESHOLD_LOW = 0.005  # Low noise level threshold
NOISE_TIME_REQUIRED = 2 * SAMPLING_RATE  # Num frames noise level must be above threshold
QUIET_TIME_REQUIRED = 2 * SAMPLING_RATE  # Num frames noise level must be below threshold

def calculate_rms(indata):
    """Calculate the RMS (volume level) of the current audio frame."""
    return np.sqrt(np.mean(indata**2))

def check_thresholds(rms_value):
    """Determine if current RMS value is above or below set thresholds."""
    return rms_value >= THRESHOLD_HIGH, rms_value <= THRESHOLD_LOW

def update_frame_counters(is_above_high, is_below_low, noise_frames, quiet_frames, frames):
    """Update frame counters based on threshold checks."""
    if is_above_high:
        # Noise detected, increment noise counter
        noise_frames += frames
    elif not is_above_high and noise_frames < NOISE_TIME_REQUIRED:
        # Quiet detected and noise duration is less than 2 seconds, reset noise counter
        noise_frames = 0

    if is_below_low:
        # Quiet detected, increment quiet counter
        quiet_frames += frames
    else:
        # Noise detected, reset quiet counter
        quiet_frames = 0

    return noise_frames, quiet_frames

def sound_event_detected(noise_duration_frames, quiet_duration_frames):
    """Triggers when the noise threshold is exceeded, then falls below another threshold."""
    cast_script_path = os.path.join(os.path.expanduser('~/laundrypi'), 'cast.py')
    # Execute cast.py
    try:
        print("Executing cast.py")
        subprocess.Popen(['python3', cast_script_path])
    except subprocess.CalledProcessError as e:
        print(f"Error executing script: {e}")

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
        noise_frames, quiet_frames = update_frame_counters(is_above_high, is_below_low, noise_frames, quiet_frames, frames)

        # Check for the first notification condition
        if is_above_high and noise_frames >= NOISE_TIME_REQUIRED:
            noise_detected = True

        # Notifications triggered here if both conditions are met
        if noise_detected and quiet_frames >= QUIET_TIME_REQUIRED:
            sound_event_detected(noise_frames, quiet_frames)
            noise_frames = 0
            quiet_frames = 0
            noise_detected = False

        if is_above_high:
            print("Noise duration (seconds):", noise_frames / SAMPLING_RATE)
        elif is_below_low and noise_detected:
            print("Quiet duration (seconds):", quiet_frames / SAMPLING_RATE)

    with sd.InputStream(callback=callback, samplerate=SAMPLING_RATE, channels=1):
        while True:
            sd.sleep(1000)

monitor_audio_thresholds()

