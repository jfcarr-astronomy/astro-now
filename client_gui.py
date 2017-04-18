#!/usr/bin/python3

import astro_now_lib as AL
from tkinter import *

# Dayton, Ohio
testLatitude = '39.759'
testLongitude = '-84.192'

myAstro = AL.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True)
#myAstro = AL.CAstro(lat=testLatitude, long=testLongitude, prettyprint=True, calcdate="2016/01/17 20:00:00")

def DisplayCurrentConditions():
	textOutput.delete(1.0, END)
	textOutput.insert(END, myAstro.GetCurrentConditions())

def DisplaySun():
	textOutput.delete(1.0, END)
	textOutput.insert(END, "Sun")
	textOutput.insert(END, "\n")
	textOutput.insert(END, myAstro.GetSunInfo())

def DisplayMoon():
	textOutput.delete(1.0, END)
	textOutput.insert(END, "Moon")
	textOutput.insert(END, "\n")
	textOutput.insert(END, myAstro.GetMoonInfo())

def DisplayPlanet(planetName):
	textOutput.delete(1.0, END)
	textOutput.insert(END, myAstro.GetPlanetInfo(planetName))

def DisplayTwilight():
	textOutput.delete(1.0, END)
	textOutput.insert(END, myAstro.GetTwilight())

def DisplayKIC():
	textOutput.delete(1.0, END)
	textOutput.insert(END, myAstro.GetObjectInfo("KIC 8462852","20:6:15","44:27:25",11))


if __name__ == '__main__':
	root = Tk()
	menubar = Menu(root)
	textOutput = Text(root)
	
	menubar.add_command(label="Current Conditions", command=DisplayCurrentConditions)
	menubar.add_command(label="Sun", command=DisplaySun)
	menubar.add_command(label="Moon", command=DisplayMoon)
	menubar.add_command(label="Venus", command= lambda: DisplayPlanet("Venus"))
	menubar.add_command(label="Mars", command= lambda: DisplayPlanet("Mars"))
	menubar.add_command(label="Jupiter", command= lambda: DisplayPlanet("Jupiter"))
	menubar.add_command(label="Saturn", command= lambda: DisplayPlanet("Saturn"))
	menubar.add_command(label="Twilight", command=DisplayTwilight)
	menubar.add_command(label="KIC", command=DisplayKIC)
	menubar.add_command(label="Exit", command=root.quit)
	
	root.config(menu=menubar)

	textOutput.insert(INSERT, "Ready...")
	textOutput.pack()

	root.mainloop()
