import datetime
import ephem
import json
import xml.etree.ElementTree as ET

class CAstroNow(object):
	
		
	def __init__(self, lat='51.478', long='-0.001', prettyprint=False, calcdate=datetime.datetime.now(), timeoffset=-5):
		"""
		Arguments:
			lat = Observer's latitude.
			long = Observer's longitude.
			prettyprint = Create nicely formatted JSON (True) or a flat string (False).
			calcdate = Date and time of calculation.  Default to now.
			timeoffset = Offset of observer's time from universal time, e.g. -5 for Eastern Standard Time.
		"""
		
		bright_stars = ['Sirrah', 'Caph', 'Algenib', 'Schedar', 'Mirach', 'Achernar', 'Almach', 'Hamal', 'Polaris', 'Menkar', 'Algol', 'Electra', 'Taygeta', 'Maia', 'Merope', 'Alcyone', 'Atlas', 'Zaurak', 'Aldebaran', 'Rigel', 'Capella', 'Bellatrix', 'Elnath',	'Nihal', 'Mintaka', 'Arneb', 'Alnilam', 'Alnitak', 'Saiph', 'Betelgeuse', 'Menkalinan', 'Mirzam', 'Canopus',	'Alhena', 'Sirius', 'Adara', 'Wezen', 'Castor', 'Procyon', 'Pollux', 'Naos', 'Alphard', 'Regulus',	'Algieba', 'Merak', 'Dubhe', 'Denebola', 'Phecda', 'Minkar', 'Megrez', 'Gienah Corvi', 'Mimosa', 'Alioth',	'Vindemiatrix', 'Mizar', 'Spica', 'Alcor', 'Alcaid', 'Agena', 'Thuban', 'Arcturus', 'Izar', 'Kochab',	'Alphecca', 'Unukalhai', 'Antares', 'Rasalgethi', 'Shaula', 'Rasalhague', 'Cebalrai', 'Etamin',	'Kaus Australis', 'Vega', 'Sheliak', 'Nunki', 'Sulafat', 'Arkab Prior', 'Arkab Posterior',	'Rukbat', 'Albereo', 'Tarazed', 'Altair', 'Alshain', 'Sadr', 'Peacock', 'Deneb', 'Alderamin',	'Alfirk', 'Enif', 'Sadalmelik', 'Alnair', 'Fomalhaut', 'Scheat', 'Markab']
		
		self.latitude = lat
		self.longitude = long
		self.prettyprint = prettyprint
		self.timeoffset = timeoffset
		
		self.bright_stars = bright_stars
        
		self.myObserver = ephem.Observer()
		self.myObserver.lat = str(self.latitude)
		self.myObserver.lon = str(self.longitude)
		
		if self.timeoffset < 0:
			utDate = ephem.Date(calcdate) + (ephem.hour * abs(self.timeoffset))
		else:
			utDate = ephem.Date(calcdate) - (ephem.hour * abs(self.timeoffset))
		
		self.myObserver.date = utDate

	def GetCurrentConditions(self):
		"""
		Full set of current condition information:
			Moon phase
			Moon location
			Planet locations
			Planet info
			Bright star locations
			Bright star info
		"""
		
		sunLocationInfo = self.GetSunLocation()
		sunLocationInfo = "\"location\": " + sunLocationInfo
		
		sunAll = "\"sun\": {"
		sunAll += sunLocationInfo + "}"
		
		moonPhaseInfo = self.GetMoonPhase()
		moonPhaseInfo = "\"phases\": " + moonPhaseInfo
		
		moonLocationInfo = self.GetMoonLocation()
		moonLocationInfo = "\"location\": " + moonLocationInfo
		
		moonAll = "\"moon\": {"
		moonAll += moonPhaseInfo + "," + moonLocationInfo + "}"
		
		planetsLocationInfo = self.GetPlanetsLocation()
		planetsLocationInfo = "\"location\": " + planetsLocationInfo
		
		planetsInfo = self.GetPlanetsInfo()
		planetsInfo = "\"info\": " + planetsInfo
		
		planetsAll = "\"planets\": {"
		planetsAll += planetsInfo + "," + planetsLocationInfo + "}"
				
		starsLocationInfo = self.GetStarsLocation()
		starsLocationInfo = "\"location\": " + starsLocationInfo
		
		starsInfo = self.GetStarsInfo()
		starsInfo = "\"info\": " + starsInfo
		
		starsAll = "\"stars\": {"
		starsAll += starsInfo + "," + starsLocationInfo + "}"				
				
		allInfo = "{" + sunAll + "," + moonAll + "," + planetsAll + "," + starsAll + "}"
		
		obj = json.loads(str(allInfo))
		if self.prettyprint == True:
			json_string = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
		else:
			json_string = json.dumps(obj, sort_keys=True, separators=(',', ': '))
		
		return json_string

	def GetMoonLocation(self):
		try:
			moon = ephem.Moon()
			moon.compute(self.myObserver)
			
			moon_altitude = moon.alt
			moon_azimuth = moon.az
			moon_constellation = ephem.constellation(moon)[1]
	    
			if moon_altitude <= 0:
				moon_visible = False
			else:
				moon_visible = True
	    
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
			if rise_details <> "":
				next_rise_local += " (" + rise_details + ")"

			next_set_local = str(ephem.localtime(set_time_ut))
			if set_details <> "":
				next_set_local += " (" + set_details + ")"
			
			dictionaryData = {}
			dictionaryData['Altitude'] = str(moon_altitude)
			dictionaryData['IsVisible'] = moon_visible
			dictionaryData['Azimuth'] = str(moon_azimuth)
			dictionaryData['InConstellation'] = moon_constellation
			dictionaryData['NextRiseUT'] = str(rise_time_ut)
			dictionaryData['NextRiseLocal'] = str(rise_time_local)
			dictionaryData['NextRiseUntil'] = str(rise_details)
			dictionaryData['NextSetUT'] = str(set_time_ut)
			dictionaryData['NextSetLocal'] = str(set_time_local)
			dictionaryData['NextSetUntil'] = str(set_details)
			
			if self.prettyprint == True:
				json_string = json.dumps(dictionaryData, sort_keys=True, indent=4, separators=(',', ': '))
			else:
				json_string = json.dumps(dictionaryData, sort_keys=True, separators=(',', ': '))
			
			return json_string
			
		except Exception as ex:
			print str(ex)
			return ""

	def GetMoonPhase(self):
		try:
			now = datetime.datetime.now()

			moon = ephem.Moon()
			moon.compute(self.myObserver)

			dictionaryData = {}
			dictionaryData['Phase'] = str(moon.phase)
			dictionaryData['NextFirstQuarter'] = str(ephem.next_first_quarter_moon(now))
			dictionaryData['NextFull'] = str(ephem.next_full_moon(now))
			dictionaryData['NextLastQuarter'] = str(ephem.next_last_quarter_moon(now))
			dictionaryData['NextNew'] = str(ephem.next_new_moon(now))

			if self.prettyprint == True:
				json_string = json.dumps(dictionaryData, sort_keys=True, indent=4, separators=(',', ': '))
			else:
				json_string = json.dumps(dictionaryData, sort_keys=True, separators=(',', ': '))
				
			return json_string
				
		except Exception as ex:
			print str(ex)
			return ""			

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
			else:
				print planetName + " is not valid."

			dictionaryData = {}
			dictionaryData['RightAscension'] = str(planet_rightascension)
			dictionaryData['Declination'] = str(planet_declination)
			dictionaryData['Magnitude'] = str(planet_magnitude)
			dictionaryData['Elongation'] = str(planet_elongation)
			dictionaryData['Size'] = str(planet_size)
			dictionaryData['Circumpolar'] = planet_circumpolar
			dictionaryData['NeverUp'] = planet_neverup
			dictionaryData['SunDistance'] = str(planet_sundistance)
			dictionaryData['EarthDistance'] = str(planet_earthdistance)
			dictionaryData['Phase'] = str(planet_phase)
			
			if self.prettyprint == True:
				json_string = json.dumps(dictionaryData, sort_keys=True, indent=4, separators=(',', ': '))
			else:
				json_string = json.dumps(dictionaryData, sort_keys=True, separators=(',', ': '))
				
			json_string = "\"" + checkName + "\": " + json_string
			
			return json_string
		
		except Exception as ex:
			print str(ex)
			print ""		

	def GetPlanetLocation(self, planetName):
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
				
				planet_altitude = p.alt
				planet_azimuth = p.az
				planet_constellation = str(ephem.constellation(p)[1])
				planet_rise_ut = self.myObserver.next_rising(p)
				planet_set_ut = self.myObserver.next_setting(p)
				planet_rise_local = ephem.localtime(planet_rise_ut)
				planet_set_local = ephem.localtime(planet_set_ut)
				if planet_altitude > 0:
					planet_visible = True
				else:
					planet_visible = False
			else:
				print planetName + " is not valid."
                
			print ""
			
			dictionaryData = {}
			dictionaryData['Altitude'] = str(planet_altitude)
			dictionaryData['IsVisible'] = planet_visible
			dictionaryData['Azimuth'] = str(planet_azimuth)
			dictionaryData['InConstellation'] = str(planet_constellation)
			dictionaryData['NextRiseUT'] = str(planet_rise_ut)
			dictionaryData['NextRiseLocal'] = str(planet_rise_local)
			#dictionaryData['NextRiseUntil'] = str(rise_details)
			dictionaryData['NextSetUT'] = str(planet_set_ut)
			dictionaryData['NextSetLocal'] = str(planet_set_local)
			#dictionaryData['NextSetUntil'] = str(set_details)
			
			if self.prettyprint == True:
				json_string = json.dumps(dictionaryData, sort_keys=True, indent=4, separators=(',', ': '))
			else:
				json_string = json.dumps(dictionaryData, sort_keys=True, separators=(',', ': '))
				
			json_string = "\"" + checkName + "\": " + json_string
			
			return json_string
			
		except Exception as ex:
			print str(ex)
			print ""

	def GetPlanetsInfo(self):
		json_string = \
			"{" + \
			self.GetPlanetInfo("Mercury") + "," + \
			self.GetPlanetInfo("Venus") + "," + \
			self.GetPlanetInfo("Mars") + "," + \
			self.GetPlanetInfo("Jupiter") + "," + \
			self.GetPlanetInfo("Saturn") + "," + \
			self.GetPlanetInfo("Uranus") + "," + \
			self.GetPlanetInfo("Neptune") + "," + \
			self.GetPlanetInfo("Pluto") + \
			"}"
		
		obj = json.loads(str(json_string))
		if self.prettyprint == True:
			json_string = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
		else:
			json_string = json.dumps(obj, sort_keys=True, separators=(',', ': '))
		
		return json_string		

	def GetPlanetsLocation(self):
		json_string = \
			"{" + \
			self.GetPlanetLocation("Mercury") + "," + \
			self.GetPlanetLocation("Venus") + "," + \
			self.GetPlanetLocation("Mars") + "," + \
			self.GetPlanetLocation("Jupiter") + "," + \
			self.GetPlanetLocation("Saturn") + "," + \
			self.GetPlanetLocation("Uranus") + "," + \
			self.GetPlanetLocation("Neptune") + "," + \
			self.GetPlanetLocation("Pluto") + \
			"}"
		
		obj = json.loads(str(json_string))
		if self.prettyprint == True:
			json_string = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
		else:
			json_string = json.dumps(obj, sort_keys=True, separators=(',', ': '))
		
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
			
			dictionaryData = {}
			dictionaryData['RightAscension'] = str(star_rightascension)
			dictionaryData['Declination'] = str(star_declination)
			dictionaryData['Magnitude'] = str(star_magnitude)
			dictionaryData['Elongation'] = str(star_elongation)
			dictionaryData['Circumpolar'] = star_circumpolar
			dictionaryData['NeverUp'] = star_neverup

			if self.prettyprint == True:
				json_string = json.dumps(dictionaryData, sort_keys=True, indent=4, separators=(',', ': '))
			else:
				json_string = json.dumps(dictionaryData, sort_keys=True, separators=(',', ': '))
			
			json_string = "\"" + starName + "\": " + json_string
			
			return json_string

		except Exception as ex:
			print str(ex)
			return "{ }"

	def GetStarLocation(self, starName):
		try:
			s = ephem.star(starName)
			s.compute(self.myObserver)

			star_altitude = s.alt
			star_azimuth = s.az
			star_constellation = str(ephem.constellation(s)[1])
			if star_altitude > 0:
				star_visible = True
			else:
				star_visible = False
			
			dictionaryData = {}
			dictionaryData['Altitude'] = str(star_altitude)
			dictionaryData['Azimuth'] = str(star_azimuth)
			dictionaryData['IsVisible'] = star_visible

			if self.prettyprint == True:
				json_string = json.dumps(dictionaryData, sort_keys=True, indent=4, separators=(',', ': '))
			else:
				json_string = json.dumps(dictionaryData, sort_keys=True, separators=(',', ': '))
			
			json_string = "\"" + starName + "\": " + json_string
			
			return json_string

		except Exception as ex:
			print str(ex)
			return "{ }"		

	def GetStarsInfo(self):
		json_string = ""
		first_pass = True
		
		for starname in self.bright_stars:
			if first_pass == True:
				json_string = json_string + self.GetStarInfo(starname)
				first_pass = False
			else:
				json_string = json_string + "," + self.GetStarInfo(starname)

		json_string = "{" + json_string + "}"
			
		obj = json.loads(str(json_string))
		if self.prettyprint == True:
			json_string = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
		else:
			json_string = json.dumps(obj, sort_keys=True, separators=(',', ': '))
		
		return json_string		

	def GetStarsLocation(self):
		json_string = ""
		first_pass = True
		
		for starname in self.bright_stars:
			if first_pass == True:
				json_string = json_string + self.GetStarLocation(starname)
				first_pass = False
			else:
				json_string = json_string + "," + self.GetStarLocation(starname)

		json_string = "{" + json_string + "}"
			
		obj = json.loads(str(json_string))
		if self.prettyprint == True:
			json_string = json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
		else:
			json_string = json.dumps(obj, sort_keys=True, separators=(',', ': '))
		
		return json_string		
			
	def GetSunLocation(self):
		try:
			sun = ephem.Sun()
			sun.compute(self.myObserver)

			sun_altitude = sun.alt
			if sun_altitude > 0:
				sun_visible = True
			else:
				sun_visible = False
			sun_azimuth = sun.az
			sun_constellation = ephem.constellation(sun)[1]

	    		rise_time_ut = self.myObserver.next_rising(sun)
			rise_time_local = str(ephem.localtime(rise_time_ut))

			set_time_ut = self.myObserver.next_setting(sun)
			set_time_local = str(ephem.localtime(set_time_ut))

			dictionaryData = {}
			dictionaryData['Altitude'] = str(sun_altitude)
			dictionaryData['IsVisible'] = sun_visible
			dictionaryData['Azimuth'] = str(sun_azimuth)
			dictionaryData['InConstellation'] = str(sun_constellation)
			dictionaryData['NextRiseUT'] = str(rise_time_ut)
			dictionaryData['NextRiseLocal'] = str(rise_time_local)
			dictionaryData['NextSetUT'] = str(set_time_ut)
			dictionaryData['NextSetLocal'] = str(set_time_local)
		
			if self.prettyprint == True:
				json_string = json.dumps(dictionaryData, sort_keys=True, indent=4, separators=(',', ': '))
			else:
				json_string = json.dumps(dictionaryData, sort_keys=True, separators=(',', ': '))
			
			return json_string
						
		except Exception as ex:
			print str(ex)
			print ""

	def GetTwilight(self):
		"""
		Calculate twilight times.
		
		Currently NOT working!
		"""
		try:
			twilightObserver = ephem.Observer()
			twilightObserver.lat, twilightObserver.lon = str(self.latitude), str(self.longitude)
			twilightObserver.horizon = -6
			
			return twilightObserver.previous_rising(ephem.Sun(), use_center=True)
		
		except Exception as ex:
			print str(ex)
			return 0


	def ShowStarLocation(self, starName):
		"""
		Placeholder:  This will be converted to a "Get" method.
		"""
		try:
			s = ephem.star(starName)
			s.compute(self.myObserver)
			
			print "__" + starName + "__"
			print 'Altitude: ' + str(s.alt)
			print 'Azimuth:  ' + str(s.az)
			print ""
		except Exception as ex:
			print str(ex)
