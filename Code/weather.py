
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")

# Utility function to get the latitude and longitude of the city
def get_lat_lon(cityName):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={cityName}&limit=1&appid={api_key}"
    
    #To avoid any erros when internet is off
    try:
        geo_response = requests.get(geo_url)
        # Checking the response of the API
        if geo_response.status_code == 200:
            geo_data = geo_response.json()
            # Check if the response has any results
            if not geo_data:
                print("No data found for the given city.")
                return None, None
            
            # Extract latitude and longitude from the response
            lat = geo_data[0]['lat']
            lon = geo_data[0]['lon']
            return lat, lon
        else:
            print(f"Failed to fetch geocoding data. Status code: {geo_response.status_code}")
            return None, None
    except requests.RequestException:
        return None, None

#main function to get the data from the api.
def getData(cityName):
    lat, lon = get_lat_lon(cityName)
    
    #To avoid any erros when internet is off
    if lat is not None and lon is not None:
        #weather url using metric to get temperature in degrees
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        
        weather_response = requests.get(weather_url)
        
        #printing if response is 200
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
        
            temperature = f"{weather_data['main']['temp']}°C"
            humidity = f"{weather_data['main']['humidity']}%"
            weather_conditions = weather_data['weather'][0]['description']
            wind_speed = f"{weather_data['wind']['speed']} m/s"
            
            return temperature, humidity, weather_conditions, wind_speed
        else:
            print(f"Failed to fetch weather data. Status code: {weather_response.status_code}")
            return [None, None, None, None]
            
    else:
        print("Please check the Internet Connectivity or give correct spelling.")
        return [None, None, None, None]

# getData("Warangal")