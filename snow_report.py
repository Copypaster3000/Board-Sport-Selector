#snow_report.py

import requests
import json
import report_score
import condition

class snow_report():

    def __init__(self):
        #condition for each hour in current 24 hr period
        #weight, importance out of 100
        #boundaries, between [2] & [3] = perfect, between [1] & [4] = great, between [0] & [5] = good enough, outside [0] & [5] = terrible

        self.forecast_fetched = False #Initalize as forecast not yet gotten when class object is made

        self.snow_depth = condition.condition()
        self.snow_depth.weight = 10
        self.snow_depth.boundaries = [30, 40, 60, 20000, 20000, 20000]
        self.temperature = condition.condition()
        self.temperature.weight = 15
        self.temperature.boundaries = [9, 12, 15, 31, 32, 40]
        self.cloud_cover = condition.condition()
        self.cloud_cover.weight = 10
        self.cloud_cover.boundaries = [25, 15, 0, 15, 25, 60]
        self.rain = condition.condition()
        self.rain.weight = 15
        self.rain.boundaries = [0, 0, 0, 0, 0, 0]
        self.snowfall = condition.condition()
        self.snowfall.weight = 15
        self.snowfall.boundaries = [3, 8, 10, 36, 40, 48]
        self.visibility = condition.condition()
        self.visibility.weight = 10
        self.visibility.boundaries = [5000, 15000, 20000, 200000, 20000, 15000]
        self.wind_speed = condition.condition()
        self.wind_speed.weight = 15


    def get_forecast(self, time):
        mount_hood_api = 'https://api.open-meteo.com/v1/forecast?latitude=45.5379&longitude=-121.5684&hourly=temperature_2m,rain,showers,snowfall,snow_depth,cloud_cover,visibility,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FLos_Angeles&forecast_days=1'

        snow_response = requests.get(mount_hood_api)
        snow_json = snow_response.json()

        self.snow_depth.weather = snow_json["hourly"]["snow_depth"]
        self.temperature.weather = snow_json["hourly"]["temperature_2m"]
        self.cloud_cover.weather = snow_json["hourly"]["cloud_cover"]
        self.rain.weather = snow_json["hourly"]["rain"]
        self.snowfall.weather = snow_json["hourly"]["snowfall"]
        self.visibility.weather = snow_json["hourly"]["visibility"]
        self.wind_speed.weather = snow_json["hourly"]["wind_speed_10m"]
        self.get_fresh_snow(self.snowfall, time)

        self.forecast_fetched = True #Shows that forecast has been gotten and stored in class members

        # print(snow_json)
 
        # print("Hourly snow depth: ", self.snow_depth.weather)
        # print("Hourly temperature: ", self.temperature.weather)
        # print("Hourly cloud cover: ", self.cloud_cover.weather)
        # print("Hourly rain: ", self.rain.weather)
        # print("Hourly snowfall: ", self.snowfall.weather)
        # print("Hourly wind speed", self.wind_speed.weather) 

    def ensure_forecast_fetched(self, time):
        if not self.forecast_fetched:
            self.get_forecast(time)

    #Sets each element in self.snowfall to the total snowfall in the 12 hours before the session starts
    def get_fresh_snow(self, snowfall, time):
        snowfall_api = 'https://api.open-meteo.com/v1/forecast?latitude=45.5379&longitude=-121.5684&hourly=snowfall&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FLos_Angeles&past_days=1&forecast_days=1'
        snowfall_response = requests.get(snowfall_api)
        snowfall_json = snowfall_response.json()
        fresh_snow_depth = 0

        #print(snow_fall_json)

        snowfall.weather = snowfall_json["hourly"]["snowfall"]

        #adds all the snow fall for each hour 12 hours before session starts to find fresh snow fall at start of session
        for hour in snowfall.weather[11+time[0]:23+time[0]]:
            fresh_snow_depth += hour
        
        #sets each elemnt in this condition to fresh snow depth at the start of the session to be rated properly by scoring function
        for hour in snowfall.weather[0:47]:
            hour = fresh_snow_depth
            

        #print("Hourly snow fall: ", snowfall.weather)

    def return_snow_score(self, time):
        self.ensure_forecast_fetched(time)

        score = 0

        score_object = report_score.report_score()

        score += score_object.get_score(self.snow_depth, time)
        score += score_object.get_score(self.temperature, time)
        score += score_object.get_score(self.cloud_cover, time)
        score += score_object.get_score(self.rain, time)
        score += score_object.get_score(self.snowfall, time)
        score += score_object.get_score(self.visibility, time)
        score += score_object.get_score(self.wind_speed, time)

        return score




        