#report_score.py
#This class returns the score given to the specific condition of a sport input into it

import condition

class report_score():

    #weight should represent how important it is out of 100 for all the conditions considered for the sport. The weight of all the conditions together should add up to %100
    #boundaries should include 6 numbers. The innermost contains ideal conditions, the second two contain good conditions, and outside of the third pair are conditions that are not useable
    #condition is the forecast data passed in as an array of data for each hour in the day
    #time is an array containing the start and end of the time period the user is interested in doing the sport for the day

    #given a condition object that holds the weight of importance of the condition, the condition data, and the boundaries for what is considered good conditions and the time the user wants to do the sport
    #today, it returns the score for the specific condition of the sport. Keep in mind it just returns the score for the weight of this condition, to get the total score all condition scores for the sport must be added together. 
    def get_score(self, condition, time):
        score = 0 #holds the score for this condition
        session_length = time[1] - time[0] #holds session length by subtracting start time from end time

        #for each element in the conditions array (the condition data per hour)
        #inside boundary [2] & [3] = perfect so 1, inside [1] & [4] = .75, inside [0] & [5] = .5, outside [0] & [5] = 0
        for item in condition.weather[time[0]:time[1]]:
            if (item >= condition.boundaries[2] and item <= condition.boundaries[3]): #if condition is inside perfect boundaries
                score += (1 / session_length) #plus full point to score divided by number of hours being considered
            elif (item >= condition.boundaries[1] and item <= condition.boundaries[4]):
                score += (.5 / session_length)
            elif (item >= condition.boundaries[0] and condition.boundaries[5]):
                score += (.3 / session_length)
            else:
                score -= .3

        #return the final weighted condition score
        return score * condition.weight


