# astro-now README

astro-now is a Python library that exports astronomical viewing info in json format, either for the current date and time (default), or a specific date and time that you request.

astro-now depends on the pyephem library, so you'll need to install it first:  <http://rhodesmill.org/pyephem/>

The CAstroNow class, in AstroNowLib.py, is instanciated with position, date/time, and other optional info.  Then, you call the method on the object to get the information you want.

For example, to get moon location info for the current date and time for Dayton, Ohio, with nicely formatted json, you would do this:

	import AstroNowLib
	testLatitude = '39.759'
	testLongitude = '-84.192'
	myAstro = AstroNowLib.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True)
	print myAstro.GetMoonLocation()

...which will produce output similar to the following:

	{
		"Altitude": "10:30:14.6",
		"Azimuth": "257:04:29.4",
		"InConstellation": "Pisces",
		"IsVisible": true,
		"NextRiseLocal": "2016-02-11 09:23:53.000003",
		"NextRiseUT": "2016/2/11 14:23:53",
		"NextRiseUntil": "",
		"NextSetLocal": "2016-02-10 20:48:53.000002",
		"NextSetUT": "2016/2/11 01:48:54",
		"NextSetUntil": "1 hour 2 minutes from now"
	}

There are several methods for specific fragments of info, e.g., GetMoonLocation(), GetPlanetInfo(planetName), GetSunLocation(), etc.  If you want to get ALL of the information in one call, you can use GetCurrentConditions().

To Do
-----

* Observation info for brightest stars.
* Astronomical twilight calculation
