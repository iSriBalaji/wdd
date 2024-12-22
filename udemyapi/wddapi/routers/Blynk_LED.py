import gpiod
import time
import requests

LED_PIN = 17  # GPIO pin number where the LED is connected
BLYNK_URL = "https://ny3.blynk.cloud/external/api/get?token=aLSTxiPxgQc0zBc4IeBIkiC4EL5oL0XW&v0"

# Open GPIO chip
chip = gpiod.Chip('gpiochip4')

# Get the GPIO line for the LED
led_line = chip.get_line(LED_PIN)

# Request exclusive access to the line and configure it as an output
led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

def get_led_status():
    try:
        response = requests.get(BLYNK_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        status = response.text.strip()  # Get the status from the response
        return int(status)  # Convert status to an integer (0 or 1)
    except requests.RequestException as e:
        print(f"Error fetching status from Blynk server: {e}")
        return 0  # Default to 0 in case of error////

def control_led(status):
    if status == 1:
        led_line.set_value(1)  # Turn on the LED
    else:
        led_line.set_value(0)  # Turn off the LED

while True:
    status = get_led_status()  # Get the LED status from the Blynk server
    control_led(status)  # Control the LED based on the status
    time.sleep(1)  # Wait for 1 second before checking again