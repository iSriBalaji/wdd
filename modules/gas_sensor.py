from gpiozero import DigitalInputDevice
import time

# GPIO pin for the sensor
SENSOR_PIN = 17
i = 0 

# Create a DigitalInputDevice instance
sensor = DigitalInputDevice(SENSOR_PIN)

try:
    while True:
        # Read the digital signal from the sensor
        print(sensor)
        sensor_value = sensor.value
        print(f"Sensor value-{i}: {sensor_value}")
        time.sleep(1)
        i+=1
except KeyboardInterrupt:
    print("Exiting...")
