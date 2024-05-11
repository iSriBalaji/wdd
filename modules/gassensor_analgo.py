import time
import smbus
import Adafruit_ADS1x15

# Create an ADS1115 ADC instance
adc = Adafruit_ADS1x15.ADS1115()

# ADC gain (1 for +/-4.096V)
GAIN = 1

# MQ sensor pin connected to ADC (A0, A1, A2, or A3)
MQ_PIN = 0

# Read interval in seconds
READ_INTERVAL = 1.0

def read_mq_sensor():
    # Read the ADC value from the MQ sensor
    value = adc.read_adc(MQ_PIN, gain=GAIN)
    return value

try:
    while True:
        # Read the MQ sensor value
        mq_value = read_mq_sensor()
        print(f"MQ sensor value: {mq_value}")
        time.sleep(READ_INTERVAL)
except KeyboardInterrupt:
    print("Exiting...")
