#!/usr/bin/python3

import astro_util as AU
import sys

def main(args):
	#print(AU.AzimuthToCompassDirection(AU.DegreesToRadians(270)))
	#print(AU.DegreesToRadians(1))
	#print(AU.RadiansToDegrees(.0174532925199))
	print(AU.RadiansToDegrees(1))
	print(AU.DegreesToRadians(57))

if __name__ == '__main__':
	sys.exit(main(sys.argv))
