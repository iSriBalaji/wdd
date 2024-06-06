import pyaudio
import wave
import time
import math  # Import for RMS calculation

# Define recording parameters
CHUNK = 1024  # Samples to read from microphone at a time
FORMAT = pyaudio.paInt16  # Audio format (16-bit signed integer)
CHANNELS = 1  # Mono recording
RATE = 96000  # Sampling rate (Hz)
RECORD_SECONDS = 5  # Recording duration (2 minutes)

# Initialize PyAudio object
p = pyaudio.PyAudio()

# Open audio stream for recording
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* Recording started for 2 minutes...")

# Function to calculate Root Mean Square (RMS) of a byte array
def calculate_rms(data):
    rms = 0
    count = len(data)
    for x in data:
        rms += (x * x)
    rms = math.sqrt(rms / float(count))
    return rms

audio_data = []  # List to store audio frames
start_time = time.time()  # Record start time

# Continuously record for 2 minutes
while time.time() - start_time < RECORD_SECONDS:
    data = stream.read(CHUNK)
    audio_data.append(data)

print("* Recording finished...")

# Stop stream and close PyAudio
stream.stop_stream()
stream.close()
p.terminate()

# Define noise detection threshold (adjust based on your environment)
threshold = 150  # Adjust this based on your noise level (higher for quieter environments)

# Check for noise exceeding the threshold
noise_detected = False
for frame in audio_data:
    rms = calculate_rms(frame)  # Function call after definition
    print("RMS", rms)
    if rms > threshold:
        noise_detected = True
        break  # Exit loop on first noise detection (optional)

# Display result
if noise_detected:
    print("Noise detected!")
else:
    print("No significant noise detected within the recording.")

# (Optional) Save recording to WAV file (uncomment if needed)
# (Optional) Save recording to WAV file (uncomment if needed)
with wave.open("recording.wav", 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_data))

# JACK message handling (optional)
# If you're using JACK and encounter the "JackShmReadWritePtr" message:
#  - If not using JACK, ignore the message.
#  - If using JACK, check the JACK
