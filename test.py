#!/usr/bin/python

import AstroNowLib

if __name__ == '__main__':
	# Dayton, Ohio
	testLatitude = '39.759'
	testLongitude = '-84.192'
	
	myAstro = AstroNowLib.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True)
	#myAstro = AstroNowLib.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True, calcdate="2016/01/17 20:00:00")

	print myAstro.GetCurrentConditions()
	#print myAstro.GetPlanetsInfo()
	#print myAstro.GetPlanetInfo("Mars")
	#print myAstro.GetMoonInfo()	
	#print myAstro.GetStarInfo("Sirius")
	#print myAstro.GetStarsInfo()
	#print myAstro.GetSunInfo()
