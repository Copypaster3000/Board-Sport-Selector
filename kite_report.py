import requests
import json
import report_score
import condition

#This class gets kite data from api calls and returns kite score for given time period

class kite_report():

    def __init__(self):
        #condition for each hour in current 24 hr period
        #weight, importance out of 100
        #boundaries, between [2] & [3] = perfect, between [1] & [4] = great, between [0] & [5] = good enough, outside [0] & [5] = terrible

        self.forecast_fetched = False #Initialize as forecast not yet gotten when class object is made

        self.temperature = condition.condition()
        self.temperature.weight = 20.0
        self.temperature.boundaries = [48.0, 60.0, 75.0, 107.0, 110.0, 118.0]
        self.precipitation = condition.condition()
        self.precipitation.weight = 20.0
        self.precipitation.boundaries = [0.05, 0.0, 0.0, 0.0, 0.05, 0.1]
        self.cloud_cover = condition.condition()    
        self.cloud_cover.weight = 20.0
        self.cloud_cover.boundaries = [25.0, 15.0, 0.0, 15.0, 25.0, 60.0]
        self.wind_speed = condition.condition() 
        self.wind_speed.weight = 20.0
        self.wind_speed.boundaries = [12.0, 15.0, 20, 40.0, 45.0, 46.0]
        self.wind_direction = condition.condition()
        self.wind_direction.weight = 20.0
        self.wind_direction.boundaries = [315.0, 45.0, 45.0, 225.0, 225.0, 45.0]
        
    #gets kite conditions from api and stores data in class members
    def get_forecast(self):   
        
        hood_river_kite_api = 'https://api.open-meteo.com/v1/forecast?latitude=45.7054&longitude=-121.5215&hourly=temperature_2m,precipitation,cloud_cover,wind_speed_10m,wind_direction_10m&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FLos_Angeles&past_days=1&forecast_days=1'
        weather_response = requests.get(hood_river_kite_api) #makes the api call
        weather_json = weather_response.json() #puts data into json format

        self.temperature.weather = weather_json["hourly"]["temperature_2m"] #organizes data from api calls into class members
        self.precipitation.weather = weather_json["hourly"]["precipitation"]
        self.cloud_cover.weather = weather_json["hourly"]["cloud_cover"]
        self.wind_speed.weather = weather_json["hourly"]["wind_speed_10m"]
        self.wind_direction.weather = weather_json["hourly"]["wind_direction_10m"]

        self.forecast_fetched = True #Shows that forecast has been gotten and stored in class members

        #print(weather_json)
        '''
        print("Hourly temperature: ", self.temperature.weather)
        print("Hourly precipitation: ", self.precipitation.weather)
        print("Hourly cloud cover: ", self.cloud_cover.weather)
        print("Hourly wind speed: ", self.wind_speed.weather)   
        print("Hourly wind direction: ", self.wind_direction.weather)
            '''

    #Makes sure forecast has been fetched and stored in class members
    def ensure_forecast_fetched(self):
        if not self.forecast_fetched:
            self.get_forecast()


    def return_kite_score(self, time):
        self.ensure_forecast_fetched()

        score = 0

        score_object = report_score.report_score()

        score += score_object.get_score(self.temperature, time)
        score += score_object.get_score(self.precipitation, time)
        score += score_object.get_score(self.cloud_cover, time)
        score += score_object.get_score(self.wind_speed, time)
        score += score_object.get_score(self.wind_direction, time)

        return score
