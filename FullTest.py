# Full Test of plotter function - Non-network

from gpiozero import DigitalOutputDevice, Button
from time import sleep
import math


# Graham the plotter.
class Plotter(object):
	# Initialise objects and variables.
    def __init__(self):
        self.xLim = Button(15, pull_up=False)
        self.yLim = Button(14, pull_up=False)
        self.sol = DigitalOutputDevice(20)
        self.sLED = DigitalOutputDevice(21)

        self.pos = [200, 200]

        self.pins = [[DigitalOutputDevice(8), DigitalOutputDevice(7), DigitalOutputDevice(12), DigitalOutputDevice(16)],
					[DigitalOutputDevice(18), DigitalOutputDevice(23), DigitalOutputDevice(24), DigitalOutputDevice(25)]]

        self.seq = [[1, 0, 1, 0],
					[0, 1, 1, 0],
					[0, 1, 0, 1],
					[1, 0, 0, 1]]

        self.step = 0

        self.maxSteps = 200

	# Output current position to console.
    def printPos(self):
        print("Position: (%d, %d)" % (self.pos[0], self.pos[1]))

	# Step pin set by number of steps
    def doSteps(self, pins, dir, steps):
		# Step the requested number of steps.
        for x in range(steps):
            for x in range(4):
                if (self.seq[self.step][x]):
                    pins[x].on()
                else:
                    pins[x].off()
            if dir:
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
    def stepAxis(self, axis, dir, steps):
		# Modifier for adjusting position.
        mod = -1 if dir else 1
		# DEBUG
		#print("Stepping axis %d by %d steps in direction %d" % (axis, steps, dir))
		# Check if step is valid from position.
        if (self.pos[axis] + mod*steps >= self.maxSteps) or (self.pos[axis] + mod*steps < 0):
            print("Cannot perform command: \'Step %d steps from position (%d, %d)\'" % (steps, self.pos[0], self.pos[1]))
            print(self.pos[axis] + mod*steps)
            return 0
		# Perform Steps
        self.doSteps(self.pins[axis], dir, steps)
        self.pos[axis] = self.pos[axis] + mod*steps

	# Step to position given.
    def stepToPos(self, pos):
		# Check bounds
        if (max(pos) > self.maxSteps) or (min(pos) < 0):
            print("Invalid Position (%d, %d)." % (pos[0], pos[1]))
            return

        # Calculate deltas in dimensions.
        dx = pos[0] - self.pos[0]
        dy = pos[1] - self.pos[1]

		# Step required amounts
        for axis, value in [[0, dx], [1, dy]]:
            sleep(0.1)
            dir = 0 if (value >= 0) else 1
            self.stepAxis(axis, dir, int(math.fabs(value)))

    # Home Axes and reset position.
    def home(self):
        sleep(0.5)
        print("Homing Axes.")
        for axis, limit in ([[0, self.xLim], [1, self.yLim]]):
            while not(limit.is_pressed):
                self.pos = [200, 200]
                self.stepAxis(axis, 1, 1)
            print("Axis %d homed." % axis)
            self.pos = [0, 0]
        self.printPos()
        sleep(0.5)

	# Draw a pixel at current position.
    def drawPixel(self):
        sleep(0.15)
        self.sol.on()
        sleep(0.15)
        self.sol.off()
        sleep(0.15)

	# Read a binary matrix from a text file.
    def readFromFile(self, filename):
        print("Reading \'%s\'." % filename)
        try:
			# Open file.
            with open(filename, 'r') as f:
				# Read lines
                matrix = []
                for line in f:
                    matrix.append([x for x in line])
			# Display
            print("Success.")
            pixels = sum(row.count("1") for row in matrix)
            print("Total Pixels: %d" % pixels)
            return matrix
		# Error Reading file
        except:
            print("Error reading \'%s\'." % filename)

	# Print the matrix onto paper.
    def printMatrix(self, matrix):
        self.sol.off()
		# Home
        self.home()

		# Iterate over pixels.
        for x in range(len(matrix)-1):
           for y in range(len(matrix[0])-1):
                # If pixel is active.
                if(matrix[x][y] == "1"):

					# Step to position.
                    print("Moving to Position (%d, %d)" % (x, y))
                    self.stepToPos([x, y])
                    self.drawPixel()

        # Done.
        self.sol.off()
        print("Complete.")

		# Home.
        self.home()

Graham = Plotter()
filename = raw_input("Enter image filename:\t>>")
matrix = Graham.readFromFile('./img/' + filename + '.txt')
Graham.printMatrix(matrix)
