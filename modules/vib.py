import RPi.GPIO as GPIO
import time

SW420_PIN = 17

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW420_PIN, GPIO.IN)

def loop():
    while True:
        if GPIO.input(SW420_PIN):
            print("Vibration detected!")
        time.sleep(0.1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
