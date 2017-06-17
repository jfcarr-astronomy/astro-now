# astro-now README

## Summary

astro-now is a Python 3 library that exports astronomical viewing info in json format, either for the current date and time (default), or a specific date and time that you request.

## Dependencies

astro-now depends on the following libraries, so install them first:

Library Name | Installation Command
------------ | --------------------
pyephem | ``pip3 install pyephem``
geocoder | ``pip3 install geocoder``

## Usage - Library

The CAstroNow class, in astro_now_lib.py, is instanciated with position, date/time, and other optional info.  Then, you call the method on the object to get the information you want.

For example, to get moon info for the current date and time for Dayton, Ohio, with nicely formatted json, you would do this:

	import astro_now_lib
	import geocode
	myGeocoder = geocode.CGeocode()
	myCoordinates = myGeocoder.GetCoordinatesForCity('Dayton, OH')

	myAstro = astro_now_lib.CAstroNow(lat=str(myCoordinates['Latitude']), long=str(myCoordinates['Longitude']), prettyprint=True)
	print(myAstro.GetMoonInfo())

...which will produce output similar to the following:

	{
		"moon": {
			"Altitude": "-50:02:30.1",
			"Azimuth": "39:12:15.7",
			"Compass": "NorthEast",
			"InConstellation": "Aquarius",
			"IsVisible": false,
			"Name": "Moon",
			"NextFirstQuarter": "2017/7/1 00:51:06",
			"NextFull": "2017/7/9 04:06:33",
			"NextLastQuarter": "2017/6/17 11:32:43",
			"NextNew": "2017/6/24 02:30:42",
			"NextRiseLocal": "2017-06-17 01:49:39.000005",
			"NextRiseUT": "2017/6/17 05:49:39",
			"NextRiseUntil": "4.801111111111111 hours 0.0 minutes from now",
			"NextSetLocal": "2017-06-17 13:47:09.000005",
			"NextSetUT": "2017/6/17 17:47:09",
			"NextSetUntil": "16.759444444444444 hours 1.1368683772161603e-13 minutes from now",
			"Phase": "47.338165283203125"
		},
		"observer": {
			"Latitude": "39:45:32.2",
			"Longitude": "-84:11:29.8",
			"ObservationDateLocal": "2017/6/16 21:01:34",
			"ObservationDateUT": "2017/6/17 01:01:35"
		}
	}

There are several methods for specific fragments of info, e.g., GetMoonInfo(), GetPlanetInfo(planetName), GetTwilight(), etc.  If you want to get ALL of the information in one call, you can use GetCurrentConditions().

## Usage - Command Line

A command line tool, **client_cl.py**, is included that simplifies retrieving various types of information.  Issue the command **client_cl.py --help** to see all of the options available:

	usage: client_cl.py [-h] [-complete] [-coordinates COORDINATES] [-date DATE]
						[-location LOCATION] [-moon] [-object OBJECT] [-observer]
						[-planet PLANET] [-planets] [-star STAR] [-stars] [-sun]
						[-twilight]

	optional arguments:
	-h, --help            show this help message and exit
	-complete             Info for all known objects.
	-coordinates COORDINATES
							Location, in the form 'Latitude,Longitude', e.g.,
							'39.764200,-84.188201'
	-date DATE            Date and time, in the form 'yyyy/mm/dd hh:mm:ss',
							e.g., '2017/06/11 22:15:00'. If omitted, current
							date/time is used.
	-location LOCATION    Location, in the form 'City, State', e.g., 'Dayton,
							OH'
	-moon                 Moon info.
	-object OBJECT        Info for a custom object, in the form 'name','right
							ascension','declination','magnitude', e.g.,
							'KIC8462852,20:6:15,44:27:25,11'
	-observer             Observer info.
	-planet PLANET        Info for individual planet.
	-planets              Info for all planets.
	-star STAR            Info for individual star.
	-stars                Info for 50 brightest stars.
	-sun                  Sun info.
	-twilight             Twilight state.

Here's an example of using the command line tool to get moon info:

	./client_cl.py -location "Dayton, OH" -moon

Results:

	{
		"moon": {
			"Altitude": "-46:09:12.4",
			"Azimuth": "48:11:29.0",
			"Compass": "NorthEast",
			"InConstellation": "Aquarius",
			"IsVisible": false,
			"Name": "Moon",
			"NextFirstQuarter": "2017/7/1 00:51:06",
			"NextFull": "2017/7/9 04:06:33",
			"NextLastQuarter": "2017/6/17 11:32:43",
			"NextNew": "2017/6/24 02:30:42",
			"NextRiseLocal": "2017-06-17 01:49:39.000005",
			"NextRiseUT": "2017/6/17 05:49:39",
			"NextRiseUntil": "4.300555555555556 hours 0.0 minutes from now",
			"NextSetLocal": "2017-06-17 13:47:09.000005",
			"NextSetUT": "2017/6/17 17:47:09",
			"NextSetUntil": "16.258888888888887 hours 1.1368683772161603e-13 minutes from now",
			"Phase": "47.338165283203125"
		},
		"observer": {
			"Latitude": "39:45:32.2",
			"Longitude": "-84:11:29.8",
			"ObservationDateLocal": "2017/6/16 21:31:36",
			"ObservationDateUT": "2017/6/17 01:31:37"
		}
	}
