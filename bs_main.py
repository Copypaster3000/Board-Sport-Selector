
import front
import snow_report

front_object = front.front()

time = front_object.get_session()

surf_score = front_object.return_surf_score(time)
snow_score = front_object.return_snow_score(time)
kite_score = front_object.return_kite_score(time)
skate_score = front_object.return_skate_score(time)

#print("The snow score is: ", snow_score)    
#print("The surf score is: ", surf_score)
#print("The kite score is: ", kite_score)   
#print("The skate score is: ", skate_score)

print("The best sport today for the time period you entered is", front_object.highest_score(surf_score, snow_score, kite_score, skate_score))