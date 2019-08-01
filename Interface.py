# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 22:18:39 2019

@author: Jacob
"""

from imageConverter import ImageConverter
from Print import Printer
import subprocess
import datetime
import os

# Provides the CLI for accessing the different functions of the plotter.
class Interface(object):
    # Init.
    def __init__(self):
        # Start Printer Service.
        print("Initialising hardware.")
        self.Printer = Printer()
        print("Initialised %s Printer. Version: %s" % (self.Printer.ARCHITECTURE, self.Printer.VERSION))
        print("Done.")
        
        # Start Image converter.
        print("Initialising converter.")
        self.converter = ImageConverter()
        print("Done.")
        
        # Configure CLI.
        self.baseDir = "/home/pi/"
        
        # Start CLI.
        self.startInterface()
    
    #------------------#
    #                  #
    #   Input/Output   #
    #                  #
    #------------------#
    
    # Text file is pre-converted.
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
            time = str(datetime.timedelta(seconds=int(pixels/1.58)))
            print("Estimated Time: %s" % time)
            return matrix
		# Error Reading file
        except:
            print("Error reading \'%s\'." % filename)
            return []
        
    # Run Generic Menu
    def runMenu(self, title, prompt, options, back=True):
        # Print Title
        print("\n -- %s --" % title)
        # print Prompt
        print(prompt)
        lower = 1
        if back:
            # Back Option.
            print("0: Back.")
            lower = 0
        # List Options.
        for i, option in enumerate(options):
            print("%d: %s" % (i+1, option['text']))
        # Get Input until valid.
        while 1:
            try:
                choice = int(raw_input(">> "))
            except:
                # Non Integer
                print("Invalid input - Non-Number.")
            if (choice < lower) or (choice > len(options)):
                # Out of range
                print("Invalid input - Out of range.")
            elif (choice == 0) and back:
                # Back
                return None
            else:
                # Run Valid Choice function.
                if options[choice-1]['args'] == None:
                    return options[choice-1]['func']()
                else:
                    return options[choice-1]['func'](options[choice-1]['args'])
                
    # Choose a file from a directory.
    def chooseFile(self, directory):
        # Print Title
        print("\n -- Choose File --")
        # print Prompt
        print("Choose a file from below:")
        # Back Option.
        print("0: Back.")
        lower = 0
        # List Options.
        options = os.listdir(self.baseDir + directory)
        for i, option in enumerate(options):
            print("%d: %s" % (i+1, option))
        # Get Input until valid.
        while 1:
            try:
                choice = int(raw_input(">> "))
            except:
                # Non Integer
                print("Invalid input - Non-Number.")
            if (choice < lower) or (choice > len(options)):
                # Out of range
                print("Invalid input - Out of range.")
            elif (choice == 0):
                # Back
                return None
            else:
                # Run Valid Choice.
                return directory + "/" + options[choice-1]
            
    
    def confirmChoice(self):
        print("Are you sure? (Y/n)")
        ret = raw_input(">> ")
        if ret != "Y":
            return False
        else:
            return True
    
    def previewMatrix(self, matrix):
        print("Preview")
        for i in range(0, len(matrix), 4):
            line = ""
            for j in range(0, len(matrix[0]), 4):
                line = line + matrix[i][j]
            line = line.replace("1", ".")
            print(line.strip())
                
    #--------------------#
    #                    #
    #   Base Interface   #
    #                    #
    #--------------------#
    
    # Main Menu on loop.
    def startInterface(self):
        # Loop Menu.
        while 1:
            options = [{'text': 'Print', 'func': self.printFromFile, 'args': None},
                       {'text': 'Convert', 'func': self.convertImage, 'args': None},
                       {'text': 'Configuration', 'func': self.configInterface, 'args': None}]
            self.runMenu("Main Menu", "Choose an option:", options, back=False)
            
            
    #---------------------#
    #                     #
    #   Print Interface   #
    #                     #
    #---------------------#
    
    # Print from pre converted file.
    def printFromFile(self, filename=None):
        # If no filename provided, choose file.
        if filename == None:
            filename = self.chooseFile('img')
        # Back if none.
        if filename == None:
            return
        matrix = self.readFromFile(filename)
        self.previewMatrix(matrix)
        if self.confirmChoice():
            self.Printer.printMatrix(matrix)
        
    #-----------------------#
    #                       #
    #   Convert Interface   #
    #                       #
    #-----------------------#
    
    def convertImage(self):
        filename = self.chooseFile('src')
        # Back if none.
        if filename == None:
            return
        # Preview Image
        print("Preview")
        preview = subprocess.check_output(["sudo", "jp2a", "--width=50", filename])
        print(preview)
        if self.confirmChoice():
            try:
                self.converter.convert(filename, self.baseDir + "img/")
            except:
                print("Error.")
                return
        print("Success.")
    
    #----------------------#
    #                      #
    #   Config Interface   #
    #                      #
    #----------------------#
    
    def configInterface(self):
        options = [{'text': 'System Info', 'func': self.systemInfo, 'args': None}]
        self.runMenu("System Configuration", "Choose an option:", options)
    
    def systemInfo(self):
        print("\n-- System Info --")
        # Printer Arch
        print("Printer Architecture:    %s" % self.Printer.ARCHITECTURE)
        # Printer Version
        print("Printer Version:         %s" % self.Printer.VERSION)
        # Base Dir
        print("Base Directory:          %s" % self.baseDir)
        # Pi Temperature
        temp = subprocess.check_output(['sudo', 'vcgencmd', 'measure_temp']).strip()
        print("Current Core Temp:       %s" % temp)
        # Internet Connection
        network = subprocess.check_output("iw dev wlan0 link | grep SSID | awk '{print $2}'", shell=True).strip()
        print("Current Network:         %s" % network)
        
            
interface = Interface()