# astro-now README

astro-now is a Python library that exports astronomical viewing info in json format, either for the current date and time (default), or a specific date and time that you request.

astro-now depends on the pyephem library, so you'll need to install it first:  <https://github.com/brandon-rhodes/pyephem>

The CAstroNow class, in astro_now_lib.py, is instanciated with position, date/time, and other optional info.  Then, you call the method on the object to get the information you want.

For example, to get moon info for the current date and time for Dayton, Ohio, with nicely formatted json, you would do this:

	import astro_now_lib
	testLatitude = '39.759'
	testLongitude = '-84.192'
	myAstro = astro_now_lib.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True)
	print myAstro.GetMoonInfo()

...which will produce output similar to the following:

	{
		"Altitude": "25:51:45.1",
		"Azimuth": "272:26:17.5",
		"InConstellation": "Taurus",
		"IsVisible": true,
		"Name": "Moon",
		"NextFirstQuarter": "2016/6/12 08:09:48",
		"NextFull": "2016/6/20 11:02:18",
		"NextLastQuarter": "2016/6/27 18:18:39",
		"NextNew": "2016/7/4 11:00:59",
		"NextRiseLocal": "2016-06-06 07:51:50",
		"NextRiseUT": "2016/6/6 11:51:50",
		"NextRiseUntil": "",
		"NextSetLocal": "2016-06-05 21:35:58.000006",
		"NextSetUT": "2016/6/6 01:35:58",
		"NextSetUntil": "2 hours 29 minutes from now",
		"Phase": "1.45557224751"
	}

There are several methods for specific fragments of info, e.g., GetMoonInfo(), GetPlanetInfo(planetName), GetTwilight(), etc.  If you want to get ALL of the information in one call, you can use GetCurrentConditions().
