
import front
import snow_report

surf_score = []
snow_score = []
kite_score = []
skate_score = []

front_object = front.front()

time = front_object.get_session()

#surf_score = front_object.return_surf_score(time)

snow_score = front_object.return_snow_score(time)

print("The snow score is: ", snow_score)    

#print(surf_score)