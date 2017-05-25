#!/usr/bin/python3

import astro_now_lib as AL

if __name__ == '__main__':
	# Dayton, Ohio
	testLatitude = '39.759'
	testLongitude = '-84.192'
	
	myAstro = AL.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True)
	#myAstro = AL.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True, calcdate="2016/06/12 23:35:00")

	#print(myAstro.GetCurrentConditions())
	#print(myAstro.GetPlanetsInfo())
	#print(myAstro.GetPlanetInfo("Mars"))
	#print(myAstro.GetMoonInfo())
	#print(myAstro.GetStarInfo("Sirius"))
	#print(myAstro.GetStarsInfo())
	#print(myAstro.GetSunInfo())
	#print(myAstro.GetTwilight())
	print(myAstro.GetObjectInfo("KIC 8462852","20:6:15","44:27:25",11))
