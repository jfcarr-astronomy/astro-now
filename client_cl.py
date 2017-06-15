#!/usr/bin/python3

import argparse
import astro_now_lib as AL
import geocode as GC
import sys

def main(args):
	parser = argparse.ArgumentParser()

	try:

		parser.add_argument("-c", "--current", help="Info for all known objects.", action="store_true")
		parser.add_argument("-d", "--date", type=str, help="Date and time, in the form 'yyyy/mm/dd hh:mm:ss', e.g., '2017/06/11 22:15:00'.  If omitted, current date/time is used.")
		parser.add_argument("-l", "--location", type=str, help="Location, in the form 'City, State', e.g., 'Dayton, OH'")
		parser.add_argument("-m", "--moon", help="Moon info.", action="store_true")
		parser.add_argument("-o", "--object", type=str, help="Info for a custom object, in the form 'name','right ascension','declination','magnitude', e.g., 'KIC8462852,20:6:15,44:27:25,11'")
		parser.add_argument("-p", "--planet", type=str, help="Info for individual planet, or 'all'")
		parser.add_argument("-s", "--star", type=str, help="Info for individual star, or 'all' for 50 brightest stars.")
		parser.add_argument("-su", "--sun", help="Sun info.", action="store_true")
		parser.add_argument("-t", "--twilight", help="Twilight state.", action="store_true")
		args = parser.parse_args()
	except Exception as ex:
		print(ex)
		sys.exit(1)

	if args.location:
		myGeocoder = GC.CGeocode()
		myCoordinates = myGeocoder.GetCoordinatesForCity(args.location)
	else:
		print("Location is required.")
		sys.exit(-1)

	if args.date:
		myAstro = AL.CAstroNow(lat=str(myCoordinates['Latitude']), long=str(myCoordinates['Longitude']), prettyprint=True, calcdate=args.date)
	else:
		myAstro = AL.CAstroNow(lat=str(myCoordinates['Latitude']), long=str(myCoordinates['Longitude']), prettyprint=True)

	if args.current:
		print(myAstro.GetCurrentConditions())

	if args.planet:
		if args.planet.strip() == "all":
			print(myAstro.GetPlanetsInfo())
		else:
			print(myAstro.GetPlanetInfo(args.planet.strip()))

	if args.moon:
		print(myAstro.GetMoonInfo())

	if args.star:
		if args.star.strip() == "all":
			print(myAstro.GetStarsInfo())
		else:
			print(myAstro.GetStarInfo(args.star.strip()))

	if args.sun:
		print(myAstro.GetSunInfo())

	if args.twilight:
		print('Twilight state: ' + myAstro.GetTwilight())

	if args.object:
		object_args = args.object.split(',')
		print(myAstro.GetObjectInfo(object_args[0],object_args[1],object_args[2],object_args[3]))

	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
