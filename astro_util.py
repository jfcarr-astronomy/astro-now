import math

OneDegreeInRadians = math.pi / 180

def AzimuthToCompassDirection(azimuth):
	"""
	Compass is divided into 16 segments, mapped to
	 N, NNE, NE, NEE, E, SEE, SE, SSE, S, SSW, SW, SWW, W, NWW, NW, and NNW.
	 
	IMPORTANT:  input azimuth must be in radians, NOT degrees.
	"""
	compassDirection = ""

	if azimuth >= 0 and azimuth <= 0.1963350785:
		compassDirection = "North"
	if azimuth > 0.1963350785 and azimuth <= 0.5890052356:
		compassDirection = "North-NorthEast"
	if azimuth > 0.5890052356 and azimuth <= 0.9816753927:
		compassDirection = "NorthEast"
	if azimuth > 0.9816753927 and azimuth <= 1.37434555:
		compassDirection = "NorthEast-East"
	if azimuth > 1.37434555 and azimuth <= 1.767015707:
		compassDirection = "East"
	if azimuth > 1.767015707 and azimuth <= 2.159685864:
		compassDirection = "SouthEast-East"
	if azimuth > 2.159685864 and azimuth <= 2.552356021:
		compassDirection = "SouthEast"
	if azimuth > 2.552356021 and azimuth <= 2.945026178:
		compassDirection = "South-SouthEast"
	if azimuth > 2.945026178 and azimuth <= 3.337696335:
		compassDirection = "South"
	if azimuth > 3.337696335 and azimuth <= 3.730366492:
		compassDirection = "South-SouthWest"
	if azimuth > 3.730366492 and azimuth <= 4.123036649:
		compassDirection = "SouthWest"
	if azimuth > 4.123036649 and azimuth <= 4.515706806:
		compassDirection = "SouthWest-West"
	if azimuth > 4.515706806 and azimuth <= 4.908376963:
		compassDirection = "West"
	if azimuth > 4.908376963 and azimuth <= 5.30104712:
		compassDirection = "NorthWest-West"
	if azimuth > 5.30104712 and azimuth <= 5.693717277:
		compassDirection = "NorthWest"
	if azimuth > 5.693717277 and azimuth <= 6.086387435:
		compassDirection = "North-NorthWest"
	if azimuth >= 6.086387435:
		compassDirection = "North"

	return compassDirection

def DegreesToRadians(degrees):
	global OneDegreeInRadians
	
	return degrees * OneDegreeInRadians
	
def RadiansToDegrees(radians):
	global OneDegreeInRadians

	return radians / OneDegreeInRadians
