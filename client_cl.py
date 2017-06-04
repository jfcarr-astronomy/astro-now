#!/usr/bin/python3

import astro_now_lib as AL
import geocode as GC
import sys

def main(args):
	myGeocoder = GC.CGeocode()
	myCoordinates = myGeocoder.GetCoordinatesForCity('Dayton, OH')
	
	myAstro = AL.CAstroNow(lat=str(myCoordinates['Latitude']), long=str(myCoordinates['Longitude']), prettyprint=True)
	#myAstro = AL.CAstroNow(lat=str(myCoordinates['Latitude']), long=str(myCoordinates['Longitude']), prettyprint=True, calcdate="2016/06/12 23:35:00")

	#print(myAstro.GetCurrentConditions())
	#print(myAstro.GetPlanetsInfo())
	#print(myAstro.GetPlanetInfo("Mars"))
	#print(myAstro.GetMoonInfo())
	#print(myAstro.GetStarInfo("Sirius"))
	#print(myAstro.GetStarsInfo())
	#print(myAstro.GetSunInfo())
	#print(myAstro.GetTwilight())
	print(myAstro.GetObjectInfo("KIC 8462852","20:6:15","44:27:25",11))

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
