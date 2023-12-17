import requests
import json
import report_score
import condition

#This class gets weather conditions related to skating and returns a score based on those conditions
class skate_report():

    def __init__(self):
        #condition for each hour in current 24 hr period
        #weight, importance out of 100
        #boundaries, between [2] & [3] = perfect, between [1] & [4] = great, between [0] & [5] = good enough, outside [0] & [5] = terrible

        self.forecast_fetched = False #Initialize as forecast not yet gotten when class object is made

        self.temperature = condition.condition()
        self.temperature.weight = 25.0
        self.temperature.boundaries = [40.0, 45.0, 50.0, 89.0, 105.0, 108.0]
        self.precipitation = condition.condition()
        self.precipitation.weight = 25.0
        self.precipitation.boundaries = [0.05, 0.0, 0.0, 0.0, 0.05, 0.1]
        self.wind_speed = condition.condition()
        self.wind_speed.weight = 25.0
        self.wind_speed.boundaries = [15.0, 10.0, 0.0, 10.0, 15.0, 17.5]
        self.snow_depth = condition.condition()
        self.snow_depth.weight = 25.0
        self.snow_depth.boundaries = [0, 0, 0, 0, 0, 0]

    #gets skate conditions from api and stores data in class members
    def get_forecast(self):
        portland_weather_api = 'https://api.open-meteo.com/v1/forecast?latitude=45.5234&longitude=-122.6762&hourly=temperature_2m,precipitation,snow_depth,cloud_cover,wind_speed_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FLos_Angeles&past_days=1&forecast_days=1'

        weather_response = requests.get(portland_weather_api) #makes the api call
        weather_json = weather_response.json() #puts data into json format

        self.temperature.weather = weather_json["hourly"]["temperature_2m"] #organizes data from api calls into class members
        self.precipitation.weather = weather_json["hourly"]["precipitation"]
        self.wind_speed.weather = weather_json["hourly"]["wind_speed_10m"]
        self.snow_depth.weather = weather_json["hourly"]["snow_depth"]


    def ensure_forecast_fetched(self):
        if not self.forecast_fetched:
            self.get_forecast()


    def return_skate_score(self, time):
        self.ensure_forecast_fetched()

        score = 0

        skate_score = report_score.report_score()

        score += skate_score.get_score(self.temperature, time)
        score += skate_score.get_score(self.precipitation, time)
        score += skate_score.get_score(self.wind_speed, time)
        score += skate_score.get_score(self.snow_depth, time)

        return score
        