import grovepi
import time

# Connect the Piezo vibration sensor to a specific analog port (adjust as needed)
piezo_pin = 4  # Analog port A0

# Set up the GrovePi library (if using)
grovepi.set_mode("BCM")  # Use BCM pin numbering (recommended)
grovepi.setup(piezo_pin, "INPUT")

# Function to detect and handle vibrations
def detect_vibration():
    vibration_detected = grovepi.analogRead(piezo_pin)  # Read analog value
    threshold = 500  # Adjust threshold based on sensor sensitivity and noise level

    if vibration_detected > threshold:
        print("Vibration detected!")
        # Add your custom actions here (e.g., trigger an LED, send a notification)
        # ...

# Main loop for continuous vibration detection
while True:
    try:
        detect_vibration()
        time.sleep(0.1)  # Adjust sleep time for desired polling frequency
    except IOError:
        print("Error reading sensor. Retrying...")
        time.sleep(1)  # Wait in case of temporary errors
