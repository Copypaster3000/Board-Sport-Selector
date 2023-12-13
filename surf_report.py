import requests
import json
import report_score
import condition

#This class gets surf data through api calls and returns surf conditions score for given time period

class surf_report():

    def __init__(self):
        #condition for each hour in current 24 hr period
        #weight, importance out of 100
        #boundaries, between [2] & [3] = perfect, between [1] & [4] = great, between [0] & [5] = good enough, outside [0] & [5] = terrible

        self.forecast_fetched = False #Initialize as forecast not yet gotten when class object is made

        self.temperature = condition.condition()
        self.temperature.weight = 20.0
        self.temperature.boundaries = [48.0, 55.0, 60.0, 107.0, 110.0, 118.0]
        self.cloud_cover =condition.condition()
        self.cloud_cover.weight = 15.0
        self.cloud_cover.boundaries = [25.0, 15.0, 0.0, 15.0, 25.0, 60.0]
        self.visibility = condition.condition()
        self.visibility.weight = 10.0
        self.visibility.boundaries = [5300.0, 20000.0, 50000.0, 200000.0, 50000.0, 20000.0]
        self.wind_speed = condition.condition()
        self.wind_speed.weight = 10.0
        self.wind_speed.boundaries = [10.0, 5.0, 0.0, 5.0, 10.0, 15.0]
        self.wind_direction = condition.condition()
        self.wind_direction.weight = 10.0
        self.wind_direction.boundaries = [0.0, 20.0, 30.0, 150.0, 160.0, 180.0]
        self.precipitation = condition.condition()
        self.precipitation.weight = 10.0
        self.precipitation.boundaries = [0.05, 0.0, 0.0, 0.0, 0.05, 0.1]
        self.wave_height = condition.condition()
        self.wave_height.weight = 20.0
        self.wave_height.boundaries = [1.0, 1.5, 2.0, 6.0, 6.7, 7.2]
        self.wave_period = condition.condition()
        self.wave_period.weight = 5.0
        self.wave_period.boundaries = [8.0, 12.0, 15.0, 100.0, 15.0, 12.0]

        #removed wave_direction, wind_wave_height, and wind_wave_direction

    

    #gets surfing conditions from api and stores data in class members
    def get_forecast(self):
        #current api calls contain more information than is utalized 
        cannon_beach_weather_api = 'https://api.open-meteo.com/v1/forecast?latitude=45.8918&longitude=-123.9615&hourly=temperature_2m,precipitation,cloudcover,visibility,windspeed_10m,winddirection_10m&daily=temperature_2m_max,temperature_2m_min,windspeed_10m_max,windgusts_10m_max&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FLos_Angeles&forecast_days=1'
        cannon_beach_waves_api = 'https://marine-api.open-meteo.com/v1/marine?latitude=45.8918&longitude=-123.9615&hourly=wave_height,wave_direction,wave_period,wind_wave_height,wind_wave_direction&length_unit=imperial&timezone=America%2FLos_Angeles&forecast_days=1'
        weather_response = requests.get(cannon_beach_weather_api) #makes the api call
        wave_response = requests.get(cannon_beach_waves_api)
        weather_json = weather_response.json() #puts data into json format
        wave_json = wave_response.json()

        self.temperature.weather = weather_json["hourly"]["temperature_2m"] #oragnizes data from api calls into class members
        self.cloud_cover.weather = weather_json["hourly"]["cloudcover"]
        self.visibility.weather = weather_json["hourly"]["visibility"]
        self.wind_speed.weather = weather_json["hourly"]["windspeed_10m"]
        self.wind_direction.weather = weather_json["hourly"]["winddirection_10m"]
        self.precipitation.weather = weather_json["hourly"]["precipitation"]
        self.wave_height.weather = wave_json["hourly"]["wave_height"]
        self.wave_period.weather = wave_json["hourly"]["wave_period"]

        self.forecast_fetched = True #Shows that forecast has been gotten and stored in class members
        
        
        #print(weather_json)
        #print(wave_json) 
        '''
        print("Hourly temperature: ", self.temperature.weather)
        print("Hourly cloud cover: ", self.cloud_cover.weather)
        print("Hourly visibility", self.visibility.weather)
        print("Hourly precipitation: ", self.precipitation.weather)
        print("Hourly wind speed: ", self.wind_speed.weather)
        print("Hourly wave height: ", self.wave_height.weather)
        print("Hourly wave period: ", self.wave_period.weather)
        print("Hourly wind direction: ", self.wind_direction.weather) 
        '''

    #Makes sure forecast has been fetched and stored in class member
    def ensure_forecast_fetched(self):
        if not self.forecast_fetched:
            self.get_forecast()


    def return_surf_score(self, time):
        self.ensure_forecast_fetched() #Makes sure forecast has been fetched and stored in class member

        score = 0

        score_object = report_score.report_score()

        score += score_object.get_score(self.temperature, time)
        score += score_object.get_score(self.cloud_cover, time)
        score += score_object.get_score(self.visibility, time) 
        score += score_object.get_score(self.wind_speed, time)
        score += score_object.get_score(self.wind_direction, time)
        score += score_object.get_score(self.precipitation, time)
        score += score_object.get_score(self.wave_height, time)
        score += score_object.get_score(self.wave_period, time)

        return score


        