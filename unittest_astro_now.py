#!/usr/bin/python3

import astro_now_lib as AL
import sys
import unittest

def CheckTwilightValue(inputString):
	isValid = True if inputString in ["Daylight", "Civil", "Nautical", "Astronomical", "Night"] else False
	
	return isValid

class AstroTest(unittest.TestCase):
	def setUp(self):
		# Dayton, Ohio
		testLatitude = '39.759'
		testLongitude = '-84.192'

		self.myAstro = AL.CAstroNow(lat=testLatitude, long=testLongitude, prettyprint=True)

	def test_Twilight(self):
		self.assertTrue(CheckTwilightValue(self.myAstro.GetTwilight()))

def main(args):
	unittest.main()

if __name__ == '__main__':
	sys.exit(main(sys.argv))
