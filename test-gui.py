#!/usr/bin/python

import AstroNowLib
from Tkinter import *

# Dayton, Ohio
testLatitude = '39.759'
testLongitude = '-84.192'

myAstro = AstroNowLib.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True)
#myAstro = AstroLib.CAstro(lat=testLatitude, long=testLongitude, prettyprint=True, calcdate="2016/01/17 20:00:00")

def DisplayCurrentConditions():
	textOutput.delete(1.0, END)
	textOutput.insert(END, myAstro.GetCurrentConditions())

def DisplayMars():
	textOutput.delete(1.0, END)
	textOutput.insert(END, myAstro.GetPlanetInfo('Mars'))
	textOutput.insert(END, "\n")
	textOutput.insert(END, myAstro.GetPlanetLocation('Mars'))


if __name__ == '__main__':
	root = Tk()
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Current Conditions", command=DisplayCurrentConditions)
	filemenu.add_command(label="Mars", command=DisplayMars)

	filemenu.add_separator()

	filemenu.add_command(label="Exit", command=root.quit)
	menubar.add_cascade(label="Info", menu=filemenu)

	root.config(menu=menubar)

	textOutput = Text(root)
	textOutput.insert(INSERT, "Ready...")
	textOutput.pack()

	root.mainloop()
