# Full Test of plotter function - Non-network

from gpiozero import DigitalOutputDevice, Button
from time import sleep
import math

# Graham the plotter.
# Printer class for providing printer output functions.
class Printer(object):
	# Initialise objects and variables.
    def __init__(self):
        # HARDWARE INITIALISATION.
        
        # LIMIT SWITCHES
        self.xLim = Button(15, pull_up=False)
        self.yLim = Button(14, pull_up=False)
        
        # SOLENOID
        self.sol = DigitalOutputDevice(20)
        
        # STATUS LED
        self.sLED = DigitalOutputDevice(21)

        # MOTOR DRIVERS
        self.pins = [[DigitalOutputDevice(8), DigitalOutputDevice(7), DigitalOutputDevice(12), DigitalOutputDevice(16)],
					[DigitalOutputDevice(18), DigitalOutputDevice(23), DigitalOutputDevice(24), DigitalOutputDevice(25)]]


        # SOFTWARE INITIALISATION
        
        self.VERSION = "1.0"
        self.ARCHITECTURE = "DOT-MATRIX"

        # MOTOR STEP SEQUENCE
        self.seq = [[1, 0, 1, 0],
					[0, 1, 1, 0],
					[0, 1, 0, 1],
					[1, 0, 0, 1]]
        
        # POSITION
        self.pos = [200, 200]

        # STEP INDEX IN SEQUENCE
        self.step = 0

        # MAXIMUM ALLOWED STEPS
        self.maxSteps = 200

	# Output current position to console.
    def printPos(self):
        print("Position: (%d, %d)" % (self.pos[0], self.pos[1]))

	# Step pin set by number of steps
    def doSteps(self, pins, sDir, steps):
		# Step the requested number of steps.
        for x in range(steps):
            for x in range(4):
                if (self.seq[self.step][x]):
                    pins[x].on()
                else:
                    pins[x].off()
            if sDir:
                self.step += 1
            else:
                self.step -= 1
            sleep(0.005) #GOOD SPEED 0.005
            if self.step >= 4:
                self.step = 0
            elif self.step < 0:
                self.step = 3

	# Step axis by number of steps
	# Direction 1 is towards limits.
	# Axis X is 0.
    def stepAxis(self, axis, sDir, steps):
		# Modifier for adjusting position.
        mod = -1 if sDir else 1
		# DEBUG
		#print("Stepping axis %d by %d steps in direction %d" % (axis, steps, dir))
		# Check if step is valid from position.
        if (self.pos[axis] + mod*steps >= self.maxSteps) or (self.pos[axis] + mod*steps < 0):
            print("Cannot perform command: \'Step %d steps from position (%d, %d)\'" % (steps, self.pos[0], self.pos[1]))
            print(self.pos[axis] + mod*steps)
            return 0
		# Perform Steps
        self.doSteps(self.pins[axis], sDir, steps)
        self.pos[axis] = self.pos[axis] + mod*steps

	# Step to position given.
    def stepToPos(self, pos):
		# Check bounds
        if (max(pos) > self.maxSteps) or (min(pos) < 0):
            print("Invalid Position (%d, %d)." % (pos[0], pos[1]))
            return 0

        # Calculate deltas in dimensions.
        dx = pos[0] - self.pos[0]
        dy = pos[1] - self.pos[1]

		# Step required amounts
        for axis, value in [[0, dx], [1, dy]]:
            sleep(0.1)
            sDir = 0 if (value >= 0) else 1
            self.stepAxis(axis, sDir, int(math.fabs(value)))

        return 1

    # Home Axes and reset position.
    def home(self):
        sleep(0.5)
        print("Homing Axes.")
        for axis, limit in ([[0, self.xLim], [1, self.yLim]]):
            while not(limit.is_pressed):
                self.stepAxis(axis, 1, 1)
                self.pos = [200, 200]
            print("Axis %d homed." % axis)
        self.pos = [0, 0]
        # Offset by 20 steps
        self.stepAxis(0, 0, 20)
        self.stepAxis(0, 0, 20)
        sleep(0.5)

	# Draw a pixel at current position.
    def drawPixel(self):
        self.sol.on()
        sleep(0.15)
        self.sol.off()

	# Print the matrix onto paper.
    def printMatrix(self, matrix):
        self.sol.off()
		# Home
        self.home()

		# Iterate over pixels.
        print("Printing...")
        for x in range(len(matrix)-1):
           for y in range(len(matrix[0])-1):
                # If pixel is active.
                if(matrix[x][y] == "1"):

					# Step to position.
                    #print("Moving to Position (%d, %d)" % (x, y))
                    r = self.stepToPos([x, y])
                    # Invalid position error. Something has broken.
                    if not(r):
                        print("Error Encountered. Cancelling print.")
                        self.sol.off()
                        self.home()
                        return
                    sleep(0.15)
                    self.drawPixel()
                    
        # Done.
        self.sol.off()
        print("Complete.")

		# Home.
        self.home()	
