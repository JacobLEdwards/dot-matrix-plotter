from gpiozero import Button
from time import sleep

btn = Button(15, pull_up=False)

btn.wait_for_press()
print "BTN"

btn.close()
