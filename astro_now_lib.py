import datetime
import ephem
import json
import astro_util as AU
import sys

class CAstroNow(object):

	def __init__(self, lat='51.478', long='-0.001', prettyprint=False, calcdate=datetime.datetime.now()):
		"""
		Arguments:
			lat = Observer's latitude.
			long = Observer's longitude.
			prettyprint = Create nicely formatted JSON (True) or a flat string (False).
			calcdate = Date and time of calculation.  Default to now.
			timeoffset = Offset of observer's time from universal time, e.g. -5 for Eastern Standard Time.
		"""
		
		bright_stars = ['Sirrah', 'Caph', 'Algenib', 'Schedar', 'Mirach', 'Achernar', 'Almach', 'Hamal', 'Polaris', 'Menkar', 'Algol', 'Electra', 'Taygeta', 'Maia', 'Merope', 'Alcyone', 'Atlas', 'Zaurak', 'Aldebaran', 'Rigel', 'Capella', 'Bellatrix', 'Elnath', 'Nihal', 'Mintaka', 'Arneb', 'Alnilam', 'Alnitak', 'Saiph', 'Betelgeuse', 'Menkalinan', 'Mirzam', 'Canopus', 'Alhena', 'Sirius', 'Adara', 'Wezen', 'Castor', 'Procyon', 'Pollux', 'Naos', 'Alphard', 'Regulus', 'Algieba', 'Merak', 'Dubhe', 'Denebola', 'Phecda', 'Minkar', 'Megrez', 'Gienah Corvi', 'Mimosa', 'Alioth', 'Vindemiatrix', 'Mizar', 'Spica', 'Alcor', 'Alcaid', 'Agena', 'Thuban', 'Arcturus', 'Izar', 'Kochab', 'Alphecca', 'Unukalhai', 'Antares', 'Rasalgethi', 'Shaula', 'Rasalhague', 'Cebalrai', 'Etamin', 'Kaus Australis', 'Vega', 'Sheliak', 'Nunki', 'Sulafat', 'Arkab Prior', 'Arkab Posterior', 'Rukbat', 'Albereo', 'Tarazed', 'Altair', 'Alshain', 'Sadr', 'Peacock', 'Deneb', 'Alderamin', 'Alfirk', 'Enif', 'Sadalmelik', 'Alnair', 'Fomalhaut', 'Scheat', 'Markab']
		
		self.latitude = lat
		self.longitude = long
		self.prettyprint = prettyprint
		
		self.bright_stars = bright_stars
		
		self.myObserver = ephem.Observer()
		self.myObserver.lat = str(self.latitude)
		self.myObserver.lon = str(self.longitude)

		# translate local date/time to universal date/time for the observer
		current_ut = self.myObserver.date
		current_local = ephem.localtime(current_ut)
		current_diff = current_ut - ephem.date(current_local)
		use_date = ephem.date(ephem.date(calcdate) + ephem.date(current_diff))
		
		self.LocalCalcDate = ephem.date(calcdate)
		self.myObserver.date = use_date

	def FormatNumber(self, inputNumber, places):
		return '{number:.{places}f}'.format(places=places, number=inputNumber)

	def DumpJSON(self, jsonObj):
		"""
		Given an object formatted as key-value pairs (e.g., Dictionary), format as JSON.
		"""
		if self.prettyprint == True:
			json_string = json.dumps(jsonObj, sort_keys=True, indent=4, separators=(',', ': '))
		else:
			json_string = json.dumps(jsonObj, sort_keys=True, separators=(',', ': '))
		
		return json_string

	def ErrorJSON(self, errorMessage):
		dictionaryData = {}
		dictionaryData['Message'] = str(errorMessage)

		json_string = "\"errors\": " + self.DumpJSON(dictionaryData)

		print(json_string)

		sys.exit(-1)

	def GetObserverInfo(self, embedded=False):
		"""
		Observer data: latitude, longitude, and observation date (local and UT).
		"""
		try:
			dictionaryData = {}
			dictionaryData['Latitude'] = str(self.myObserver.lat)
			dictionaryData['Longitude'] = str(self.myObserver.lon)
			dictionaryData['ObservationDateUT'] = str(self.myObserver.date)
			dictionaryData['ObservationDateLocal'] = str(self.LocalCalcDate)

			if self.prettyprint == True:
				json_string = json.dumps(dictionaryData, sort_keys=True, indent=4, separators=(',', ': '))
			else:
				json_string = json.dumps(dictionaryData, sort_keys=True, separators=(',', ': '))
			
			json_string = "\"observer\": " + json_string

			if embedded == False:
				json_string = "{" + json_string + "}"

				obj = json.loads(str(json_string))
				if self.prettyprint == True:
					json_string = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
				else:
					json_string = json.dumps(obj, sort_keys=True, separators=(',', ': '))

			return json_string

		except Exception as ex:
			self.ErrorJSON(str(ex))
			sys.exit(-1)

	def GetCurrentConditions(self):
		"""
		Full set of current condition information: sun info, moon info, planet info, and bright star info
		"""
		
		observerAll = self.GetObserverInfo(embedded=True)

		sunAll = self.GetSunInfo(embedded=True)
		
		moonAll = self.GetMoonInfo(embedded=True)
	
		planetsAll = self.GetPlanetsInfo(embedded=True)
		
		starsAll = self.GetStarsInfo(embedded=True)

		twilightAll = self.GetTwilight(embedded=True)
		
		allInfo = "{" + observerAll + "," + sunAll + "," + moonAll + "," + planetsAll + "," + starsAll + "," + twilightAll + "}"
		
		obj = json.loads(str(allInfo))
		if self.prettyprint == True:
			json_string = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
		else:
			json_string = json.dumps(obj, sort_keys=True, separators=(',', ': '))
		
		return json_string

	def GetMoonInfo(self, embedded=False):
		try:
			now = datetime.datetime.now()
			
			moon = ephem.Moon()
			moon.compute(self.myObserver)
			
			moon_altitude = moon.alt
			moon_azimuth = moon.az
			moon_compass = AU.AzimuthToCompassDirection(moon_azimuth)
			moon_constellation = ephem.constellation(moon)[1]

			moon_visible = True if moon_altitude > 0 else False

			rise_time_ut = self.myObserver.next_rising(moon)
			rise_time_local = str(ephem.localtime(rise_time_ut))
			
			set_time_ut = self.myObserver.next_setting(moon)
			set_time_local = str(ephem.localtime(set_time_ut))
	    
			altitude_string = str(moon_altitude)
			rise_details = ""
			set_details = ""
			if moon_altitude <= 0:
				altitude_string += " (Not visible)"

				time_until_rise = ephem.localtime(rise_time_ut) - datetime.datetime.now()
				hours_until_rise = time_until_rise.seconds / 60 / 60
				minutes_until_rise = time_until_rise.seconds / 60
				
				if hours_until_rise > 0:
					minutes_until_rise -= hours_until_rise * 60
					rise_details += str(hours_until_rise)
					if hours_until_rise > 1:
						rise_details += " hours"
					else:
						rise_details += " hour"
				rise_details += " " + str(minutes_until_rise) + " minutes from now"
			else:
				altitude_string = altitude_string + " (Visible)"				
			
			time_until_set = ephem.localtime(set_time_ut) - datetime.datetime.now()
			hours_until_set = time_until_set.seconds / 60 / 60
			minutes_until_set = time_until_set.seconds / 60
			if hours_until_set > 0:
				minutes_until_set -= hours_until_set * 60
				set_details += str(hours_until_set)
				if hours_until_set > 1:
					set_details += " hours"
				else:
					set_details += " hour"
			set_details += " " + str(minutes_until_set) + " minutes from now"
						
			next_rise_local = str(ephem.localtime(rise_time_ut))
			if rise_details != "":
				next_rise_local += " (" + rise_details + ")"

			next_set_local = str(ephem.localtime(set_time_ut))
			if set_details != "":
				next_set_local += " (" + set_details + ")"
			
			dictionaryData = {}
			dictionaryData['Name'] = "Moon"
			dictionaryData['Altitude'] = str(moon_altitude)
			dictionaryData['IsVisible'] = moon_visible
			dictionaryData['Azimuth'] = str(moon_azimuth)
			dictionaryData['Compass'] = str(moon_compass)
			dictionaryData['InConstellation'] = moon_constellation
			dictionaryData['NeverUp'] = str(moon.neverup)
			dictionaryData['NextRiseUT'] = str(rise_time_ut)
			dictionaryData['NextRiseLocal'] = str(rise_time_local)
			dictionaryData['NextRiseUntil'] = str(rise_details)
			dictionaryData['NextSetUT'] = str(set_time_ut)
			dictionaryData['NextSetLocal'] = str(set_time_local)
			dictionaryData['NextSetUntil'] = str(set_details)
			dictionaryData['Phase'] = str(self.FormatNumber(moon.phase,4))
			dictionaryData['Magnitude'] = str(moon.mag)
			dictionaryData['NextFirstQuarter'] = str(ephem.next_first_quarter_moon(now))
			dictionaryData['NextFull'] = str(ephem.next_full_moon(now))
			dictionaryData['NextLastQuarter'] = str(ephem.next_last_quarter_moon(now))
			dictionaryData['NextNew'] = str(ephem.next_new_moon(now))
		
			json_string = "\"moon\": " + self.DumpJSON(dictionaryData)

			if embedded == False:
				json_string = "{" + self.GetObserverInfo(embedded=True) + "," + json_string + "}"

				obj = json.loads(str(json_string))
				json_string = self.DumpJSON(obj)

			return json_string
			
		except Exception as ex:
			self.ErrorJSON(str(ex))
			sys.exit(-1)

	def GetObjectInfo(self, objectName, rightAscension, declination, magnitude=0, embedded=False):
		"""
		Calculate local info for custom objects, given Right Ascension and Declination info.
		
		XEphem format for fixed object:
		 "ObjectName,f,right_ascension,declination,magnitude"
		   Right Ascension is given as hours:minutes:seconds
		   Declination is given as degrees:minutes:seconds
		Example:
		 "KIC 8462852,f,20:6:15,44:27:25,11"
		"""
		
		ephemeris = objectName + "," + "f" + "," + rightAscension + "," + declination + "," + str(magnitude)
		
		customObject = ephem.readdb(ephemeris)
		customObject.compute(self.myObserver)
		
		object_altitude = customObject.alt
		object_azimuth = customObject.az
		object_compass = AU.AzimuthToCompassDirection(object_azimuth)
		object_constellation = ephem.constellation(customObject)[1]
		object_visible = True if object_altitude > 0 else False
		object_magnitude = customObject.mag

		dictionaryData = {}
		dictionaryData['Name'] = objectName
		dictionaryData['Altitude'] = str(object_altitude)
		dictionaryData['IsVisible'] = object_visible
		dictionaryData['Azimuth'] = str(object_azimuth)
		dictionaryData['Compass'] = str(object_compass)
		dictionaryData['InConstellation'] = object_constellation
		dictionaryData['Magnitude'] = object_magnitude

		json_string = "\"objects\": [" + self.DumpJSON(dictionaryData) + "]"

		if embedded == False:
			json_string = "{" + json_string + "}"

			obj = json.loads(str(json_string))
			json_string = self.DumpJSON(obj)

		return json_string

	def GetPlanetInfo(self, planetName):
		try:
			IsReady = False
            
			checkName = planetName.lower()
			
			if checkName == 'mercury':
				p = ephem.Mercury()
				IsReady = True
    
			if checkName == 'venus':
				p = ephem.Venus()
				IsReady = True
            
			if checkName == 'mars':
				p = ephem.Mars()
				IsReady = True
    
			if checkName == 'jupiter':
				p = ephem.Jupiter()
				IsReady = True
    
			if checkName == 'saturn':
				p = ephem.Saturn()
				IsReady = True
    
			if checkName == 'uranus':
				p = ephem.Uranus()
				IsReady = True
    
			if checkName == 'neptune':
				p = ephem.Neptune()
				IsReady = True
                
			if checkName == 'pluto':
				p = ephem.Pluto()
				IsReady = True
                
			if IsReady == True:
				p.compute(self.myObserver)
                
				planet_rightascension = p.ra
				planet_declination = p.dec
				planet_magnitude = p.mag
				planet_elongation = p.elong  # angle to sun
				planet_size = p.size  # arcseconds
				planet_circumpolar = p.circumpolar  # stays above horizon?				
				planet_neverup = p.neverup  # never rises?				
				planet_sundistance = p.sun_distance  # distance to sun
				planet_earthdistance = p.earth_distance  # distance to earth
				planet_phase = p.phase  # % illuminated

				planet_altitude = p.alt
				planet_azimuth = p.az
				planet_compass = AU.AzimuthToCompassDirection(planet_azimuth)
				planet_constellation = str(ephem.constellation(p)[1])
				planet_rise_ut = self.myObserver.next_rising(p)
				planet_set_ut = self.myObserver.next_setting(p)
				planet_rise_local = ephem.localtime(planet_rise_ut)
				planet_set_local = ephem.localtime(planet_set_ut)

				planet_visible = True if planet_altitude > 0 else False

			else:
				self.ErrorJSON("Planet '" + planetName + "' is not valid.")

			dictionaryData = {}
			dictionaryData['Name'] = str(planetName)
			dictionaryData['RightAscension'] = str(planet_rightascension)
			dictionaryData['Declination'] = str(planet_declination)
			dictionaryData['Magnitude'] = str(planet_magnitude)
			dictionaryData['Elongation'] = str(planet_elongation)
			dictionaryData['Size'] = str(planet_size)
			dictionaryData['Circumpolar'] = planet_circumpolar
			dictionaryData['NeverUp'] = planet_neverup
			dictionaryData['SunDistance'] = str(planet_sundistance)
			dictionaryData['EarthDistance'] = str(planet_earthdistance)
			dictionaryData['Phase'] = str(self.FormatNumber(planet_phase,4))
			dictionaryData['Altitude'] = str(planet_altitude)
			dictionaryData['IsVisible'] = planet_visible
			dictionaryData['Azimuth'] = str(planet_azimuth)
			dictionaryData['Compass'] = str(planet_compass)
			dictionaryData['InConstellation'] = str(planet_constellation)
			dictionaryData['NextRiseUT'] = str(planet_rise_ut)
			dictionaryData['NextRiseLocal'] = str(planet_rise_local)
			#dictionaryData['NextRiseUntil'] = str(rise_details)
			dictionaryData['NextSetUT'] = str(planet_set_ut)
			dictionaryData['NextSetLocal'] = str(planet_set_local)
			#dictionaryData['NextSetUntil'] = str(set_details)
			dictionaryData['CalcDateUT'] = str(self.myObserver.date)
			
			json_string = self.DumpJSON(dictionaryData)

			return json_string
		
		except Exception as ex:
			self.ErrorJSON(str(ex))
			sys.exit(-1)

	def GetPlanetsInfo(self, planetName="", embedded=False):
		if planetName == "":
			json_string = \
				"\"planets\": [" + \
				self.GetPlanetInfo("Mercury") + "," + \
				self.GetPlanetInfo("Venus") + "," + \
				self.GetPlanetInfo("Mars") + "," + \
				self.GetPlanetInfo("Jupiter") + "," + \
				self.GetPlanetInfo("Saturn") + "," + \
				self.GetPlanetInfo("Uranus") + "," + \
				self.GetPlanetInfo("Neptune") + "," + \
				self.GetPlanetInfo("Pluto") + \
				"]"
		else:
			json_string = \
				"\"planets\": [" + \
				self.GetPlanetInfo(planetName) + \
				"]"

		if embedded == False:
			json_string = "{" + self.GetObserverInfo(embedded=True) + "," + json_string + "}"
		
			obj = json.loads(str(json_string))
			json_string = self.DumpJSON(obj)
		
		return json_string		

	def GetStarInfo(self, starName):
		try:
			s = ephem.star(starName)
			s.compute(self.myObserver)

			star_rightascension = s._ra
			star_declination = s._dec
			star_magnitude = s.mag
			star_elongation = s.elong  # angle to sun
			star_circumpolar = s.circumpolar  # stays above horizon?				
			star_neverup = s.neverup  # never rises?				
			star_altitude = s.alt
			star_azimuth = s.az
			star_compass = AU.AzimuthToCompassDirection(star_azimuth)
			star_constellation = str(ephem.constellation(s)[1])
			star_visible = True if star_altitude > 0 else False

			dictionaryData = {}
			dictionaryData['Name'] = str(starName)
			dictionaryData['RightAscension'] = str(star_rightascension)
			dictionaryData['Declination'] = str(star_declination)
			dictionaryData['Magnitude'] = str(star_magnitude)
			dictionaryData['Elongation'] = str(star_elongation)
			dictionaryData['Circumpolar'] = star_circumpolar
			dictionaryData['NeverUp'] = star_neverup
			dictionaryData['Altitude'] = str(star_altitude)
			dictionaryData['Azimuth'] = str(star_azimuth)
			dictionaryData['Compass'] = str(star_compass)
			dictionaryData['IsVisible'] = star_visible

			return self.DumpJSON(dictionaryData)

		except Exception as ex:
			self.ErrorJSON(str(ex))
			sys.exit(-1)

	def GetStarsInfo(self, starName="", embedded=False):
		json_string = ""
		first_pass = True

		if starName == "":		
			for starname in self.bright_stars:
				if first_pass == True:
					json_string = json_string + self.GetStarInfo(starname)
					first_pass = False
				else:
					json_string = json_string + "," + self.GetStarInfo(starname)
		else:
			json_string = self.GetStarInfo(starName)

		json_string = "\"stars\": [" + json_string + "]"

		if embedded == False:
			json_string = "{" + self.GetObserverInfo(embedded=True) + "," + json_string + "}"
			
			obj = json.loads(str(json_string))
			json_string = self.DumpJSON(obj)
		
		return json_string

	def GetSunInfo(self, embedded=False):
		try:
			sun = ephem.Sun()
			sun.compute(self.myObserver)

			sun_altitude = sun.alt
			sun_visible = True if sun_altitude > 0 else False
			sun_azimuth = sun.az
			sun_compass = AU.AzimuthToCompassDirection(sun_azimuth)
			sun_constellation = ephem.constellation(sun)[1]

			rise_time_ut = self.myObserver.next_rising(sun)
			rise_time_local = str(ephem.localtime(rise_time_ut))

			set_time_ut = self.myObserver.next_setting(sun)
			set_time_local = str(ephem.localtime(set_time_ut))

			dictionaryData = {}
			dictionaryData['Name'] = "Sun"
			dictionaryData['Altitude'] = str(sun_altitude)
			dictionaryData['IsVisible'] = sun_visible
			dictionaryData['Azimuth'] = str(sun_azimuth)
			dictionaryData['Compass'] = str(sun_compass)
			dictionaryData['InConstellation'] = str(sun_constellation)
			dictionaryData['NextRiseUT'] = str(rise_time_ut)
			dictionaryData['NextRiseLocal'] = str(rise_time_local)
			dictionaryData['NextSetUT'] = str(set_time_ut)
			dictionaryData['NextSetLocal'] = str(set_time_local)

			json_string = "\"sun\": " + self.DumpJSON(dictionaryData)

			if embedded == False:
				json_string = "{" + self.GetObserverInfo(embedded=True) + "," + json_string + "}"

				obj = json.loads(str(json_string))
				json_string = self.DumpJSON(obj)

			return json_string

		except Exception as ex:
			self.ErrorJSON(str(ex))
			sys.exit(-1)

	def GetTwilight(self, embedded=False):
		try:
			sun = ephem.Sun()
			sun.compute(self.myObserver)
			
			twilight_description = "None"
			
			sun_altitude_degrees = AU.RadiansToDegrees(sun.alt)
			
			if sun_altitude_degrees > 0:
				twilight_description = "Daylight"
			
			if sun_altitude_degrees <= 0 and sun_altitude_degrees >= -6:
				twilight_description = "Civil"
			
			if sun_altitude_degrees < -6 and sun_altitude_degrees >= -12:
				twilight_description = "Nautical"

			if sun_altitude_degrees < -12 and sun_altitude_degrees >= -18:
				twilight_description = "Astronomical"
			
			if sun_altitude_degrees < -18:
				twilight_description = "Night"
			
			dictionaryData = {}
			dictionaryData['Description'] = twilight_description

			json_string = "\"twilight\": " + self.DumpJSON(dictionaryData)

			if embedded == False:
				json_string = "{" + self.GetObserverInfo(embedded=True) + "," + json_string + "}"

				obj = json.loads(str(json_string))
				json_string = self.DumpJSON(obj)

			return json_string

		except Exception as ex:
			self.ErrorJSON(str(ex))
			sys.exit(-1)
