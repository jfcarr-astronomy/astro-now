#!/usr/bin/python

import AstroNowLib

if __name__ == '__main__':
	# Dayton, Ohio
	testLatitude = '39.759'
	testLongitude = '-84.192'
	
	myAstro = AstroNowLib.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True)
	#myAstro = AstroLib.CAstro(lat=testLatitude, long=testLongitude, prettyprint=True, calcdate="2016/01/17 20:00:00")

	print myAstro.GetCurrentConditions()
	