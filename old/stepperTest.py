from gpiozero import DigitalOutputDevice, Button
from time import sleep

xLim = Button(15, pull_up=False)
yLim = Button(14, pull_up=False)
sol = DigitalOutputDevice(20)
sLED = DigitalOutputDevice(21)

yPins = [DigitalOutputDevice(18), DigitalOutputDevice(23), DigitalOutputDevice(24), DigitalOutputDevice(25)]
xPins = [DigitalOutputDevice(8), DigitalOutputDevice(7), DigitalOutputDevice(12), DigitalOutputDevice(16)]

seq = [
	[1, 0, 1, 0],
	[0, 1, 1, 0],
	[0, 1, 0, 1],
	[1, 0, 0, 1]
]
step = 0

def stepAxis(axis, dir, steps):
	global step
	if (axis == "X"):
		pins = xPins
	else:
		pins = yPins

	for x in range(steps):
		for x in range(4):
			if (seq[step][x]):
				pins[x].on()
			else:
				pins[x].off()
		sleep(0.005) #GOOD SPEED 0.005
		if dir:
			step += 1
		else:
			step -= 1
		if step >= 4:
			step = 0
		elif step < 0:
			step = 3
sol.on()
for i in range(3):
	steps = 0
	if (i % 2 == 0):
		axis = "X"
		lim = xLim
	else:
		axis = "Y"
		lim = yLim
	if (i > 2):
		dir = False
	else:
		dir = True

	while not(lim.is_pressed):
		stepAxis(axis, dir, 1)
		steps += 1
		sleep(0.005)

		if (steps % 10 == 0):
			sol.off()
			sleep(0.25)
			sol.on()
			sleep(0.25)

	print steps
