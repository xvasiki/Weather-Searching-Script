#Weather Data Program

#Objective: Displays temperature, humdity, etc. for given location. User inserts location name or zipcode

import requests
import pprint
import json
#for timestamp conversion into time format
from datetime import datetime
#for local timezone
from timezonefinder import TimezoneFinder
import pytz

#API_Key
api_key = "INSERT_OPENWEATHER_API_KEY"
tz = TimezoneFinder()

#User gives location
def loc_input():
	location_input=input("Specify city name or zipcode to get the weather information!")

	#Checks if input empty
	if not location_input:
		raise ValueError("No location given...")
	#Checks if input is zipcode
	if location_input.isnumeric() and len(location_input)==5:
		return location_input
	#Defaults to location	
	else:
		return location_input

#Calling function for input and error handling
try:
	location = loc_input()
	#Choosing API to request based on input
	if location.isnumeric() and len(location)==5:
		api_call = f"http://api.openweathermap.org/geo/1.0/zip?zip={location}&appid={api_key}"
		#Requesting GeocodeAPI output for lon & lat
		json_str=requests.get(api_call).text
		lat = json.loads(json_str)["lat"]
		lon = json.loads(json_str)["lon"]
	
	else:
		api_call = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&appid={api_key}"
		#Requesting GeocodeAPI output for lon & lat
		json_str=requests.get(api_call).text
		lat = json.loads(json_str)[0]["lat"]
		lon = json.loads(json_str)[0]["lon"]
		print(f"{lat}, {lon}")
	
	#requesting API for weather
	weather_call = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"

	#assigning request to var
	response = requests.get(weather_call)
	
	#checking if successful request to run code
	if response.status_code == 200:
		#formatting json for easy retrieval of content
		data = json.loads(response.text)

		#finding timezone for lon/lat
		t_z = pytz.timezone(tz.timezone_at(lng=lon, lat=lat))
		# print(t_z)

		#defining vars
		location = data["name"]
		temp = data["main"]["temp"]
		low = data["main"]["temp_min"]
		high = data["main"]["temp_max"]
		feels_like = data["main"]["feels_like"]
		humidity = data["main"]["humidity"]

		#converting timestamp into UTC and then into local timezone of coordinates to provide sunset time
		sunset = datetime.utcfromtimestamp(data["sys"]["sunset"]).astimezone(tz=t_z).strftime("%-I:%M %p")

		#final output
		output = f"Location: {location}\nCurrent Temp: {temp}°F\nLow: {low}°F\nHigh: {high}°F\nFeels like: {feels_like}°F\nHumidity: {humidity}%\nSunset: {sunset}"
		print(output)
	
	else:
		print(f"Error:{respnse.status_code}")

#if no location inputted by user
except ValueError as e:
	print("No location given!")

