#!/usr/bin/python3

import argparse
import astro_now_lib as AL
import astro_util as AU
import geocode as GC
import sys

def main(args):
	parser = argparse.ArgumentParser()

	try:
		parser.add_argument("-complete", help="Info for all known objects.", action="store_true")
		parser.add_argument("-coordinates", type=str, help="Location, in the form 'Latitude,Longitude', e.g., '39.764200,-84.188201'")
		parser.add_argument("-date", type=str, help="Date and time, in the form 'yyyy/mm/dd hh:mm:ss', e.g., '2017/06/11 22:15:00'.  If omitted, current date/time is used.")
		parser.add_argument("-location", type=str, help="Location, in the form 'City, State', e.g., 'Dayton, OH'")
		parser.add_argument("-moon", help="Moon info.", action="store_true")
		parser.add_argument("-object", type=str, help="Info for a custom object, in the form 'name','right ascension','declination','magnitude', e.g., 'KIC8462852,20:6:15,44:27:25,11'")
		parser.add_argument("-observer", help="Observer info.", action="store_true")
		parser.add_argument("-planet", type=str, help="Info for individual planet.")
		parser.add_argument("-planets", help="Info for all planets.", action="store_true")
		parser.add_argument("-prettyprint", help="Display nicely formatted JSON.", action="store_true")
		parser.add_argument("-star", type=str, help="Info for individual star.")
		parser.add_argument("-stars", help="Info for 50 brightest stars.", action="store_true")
		parser.add_argument("-sun", help="Sun info.", action="store_true")
		parser.add_argument("-twilight", help="Twilight state.", action="store_true")
		args = parser.parse_args()
	except Exception as ex:
		AU.ErrorJSON(str(ex))
		sys.exit(1)

	if args.location:
		myGeocoder = GC.CGeocode()
		myCoordinates = myGeocoder.GetCoordinatesForCity(args.location)
		if myCoordinates['Latitude'] == None:
			AU.ErrorJSON("Geocoder is unavailable.", prettyprint=args.prettyprint)
			sys.exit(-1)
	else:
		if args.coordinates:
			coordinate_args = args.coordinates.split(',')
			myCoordinates = {'Latitude': coordinate_args[0], 'Longitude': coordinate_args[1]}
		else:
			AU.ErrorJSON("Location or Coordinates are required.", prettyprint=args.prettyprint)
			sys.exit(-1)

	if args.date:
		myAstro = AL.CAstroNow(lat=str(myCoordinates['Latitude']), long=str(myCoordinates['Longitude']), prettyprint=args.prettyprint, calcdate=args.date)
	else:
		myAstro = AL.CAstroNow(lat=str(myCoordinates['Latitude']), long=str(myCoordinates['Longitude']), prettyprint=args.prettyprint)

	if args.complete:
		print(myAstro.GetCurrentConditions())

	if args.planet:
		print(myAstro.GetPlanetsInfo(args.planet.strip()))

	if args.planets:
		print(myAstro.GetPlanetsInfo())

	if args.moon:
		print(myAstro.GetMoonInfo())

	if args.observer:
		print(myAstro.GetObserverInfo())

	if args.star:
		print(myAstro.GetStarsInfo(args.star.strip()))

	if args.stars:
		print(myAstro.GetStarsInfo())

	if args.sun:
		print(myAstro.GetSunInfo())

	if args.twilight:
		print(myAstro.GetTwilight())

	if args.object:
		object_args = args.object.split(',')
		print(myAstro.GetObjectInfo(object_args[0],object_args[1],object_args[2],object_args[3]))

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
