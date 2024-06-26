#Import Time and Board features to get the ADS1115 working
import time
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance. Note you can change the I2C address from its default (0x48) and/or bus number
#adc = Adafruit_ADS1x15.ADS1115()
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 2

for i in range(27):
	print(i)
	value = adc.read_adc_difference(0, gain=GAIN)
	print("VALUE", value)
