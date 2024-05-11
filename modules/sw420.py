from gpiozero import DigitalInputDevice
import time

SW420_PIN = 17
vibration_count = 0

def on_vibration():
    global vibration_count
    vibration_count +=1
    print(f"Vibration {vibration_count} detected!")

def setup():
    global sensor
    sensor = DigitalInputDevice(SW420_PIN)
    sensor.when_activated = on_vibration

def loop():
    while True:
        time.sleep(0.1)

def destroy():
    sensor.close()

if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        destroy()
