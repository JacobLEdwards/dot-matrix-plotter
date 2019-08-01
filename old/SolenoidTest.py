from gpiozero import DigitalOutputDevice
from time import sleep

sol = DigitalOutputDevice(20)
sLED = DigitalOutputDevice(21)

for i in range(10):
	sol.on()
	sLED.on()
	sleep(0.5)
	sol.off()
	sLED.off()
	sleep(0.5)

sol.close()
