import fastf1
import pandas as pd
import time
from datetime import date, datetime, timedelta

round_number = 1

sprint_weekends = [2, 4, 5, 9, 12, 16]

#quali_place = {}
def quali_position(round_number):
    """Gives the qualifying postion of the drivers"""
    quali_place = {}
    quali_session = fastf1.get_session(2026, round_number, "Q" )
    quali_session.load()
    #quali_results = quali_session.results.reset_index(drop = True, inplace = True) # this just changes the index to normal instead of the drivers numbers

    quali_results_df = quali_session.results[["Abbreviation", "TeamName","Position", "Q1"]]
    #quali_results_df.index = quali_results_df.index + 1

    for row in quali_results_df.itertuples():
        if not pd.isnull(row.Q1):
            quali_place[row.Abbreviation] = row.Position
        else:
            quali_place[row.Abbreviation] = "NC/DSQ"
    return quali_place


#fant_score_quali = {}
def quali_fantasy_score(dictionary, fant_score_quali = None):
    """Gives the fantasy score from the qualifying round"""
    if fant_score_quali is None:
        fant_score_quali = {}
    quali_scoring = {1: 10, 2: 9, 3: 8, 4:7, 5:6, 6:5, 7:4, 8:3, 9:2, 10:1}
    
    #return {k:quali_scoring.get(v,0) for k,v in dictionary.items() if v !="NC/DSQ"}
    for k,v in dictionary.items():
        fant_score_quali.setdefault(k,0)
        if v!= "NC/DSQ":
            fant_score_quali[k] += quali_scoring.get(v,0)
        else:
           fant_score_quali[k] = - 5 #?

    return fant_score_quali

    #return {k:quali_scoring.get(v,0) if v!= "NC/DSQ" else -5 for k,v in dictionary.items()}



def race_position(round_number):
    """Gives the race position of the drivers"""
    race_place = {}
    race_session = fastf1.get_session(2026, round_number, "R")
    race_session.load()

    #race_results = race_session.results.reset_index(drop = True, inplace = True) # this just changes the index to normal instead of the drivers numbers
    race_results_df = race_session.results[["Abbreviation", "TeamName","Position","Points", "Status"]]
    #race_results_df.index = race_results_df.index + 1
    
    for row in race_results_df.itertuples():
        if row.Status in ["Finished", "Lapped"]:
            race_place[row.Abbreviation] = row.Position
        else:
            race_place[row.Abbreviation] = "NC/DSQ"
    return race_place

# Perhaps come back and be more specific rather than nc or dsq do Retired or DNS or whatever
    





def race_fantasy_score(dictionary, fant_score_race = None):
    """Gives the fantasy score from the race"""
    if fant_score_race is None:
        fant_score_race = {}
    race_scoring = {1:25, 2:18, 3:15, 4:12, 5:10, 6:8, 7:6, 8:4, 9:2, 10:1}
    
    for k,v in dictionary.items():
        fant_score_race.setdefault(k,0)
        if v!= "NC/DSQ":
            fant_score_race[k] += race_scoring.get(v,0)
        else:
            fant_score_race[k] = -5

    return fant_score_race


# Ok now we have sprint weekends 



def sprint_race_position(round_number):
    """Gives the sprint race position of the drivers"""
    sprint_race_place = {}
    sprint_race_session = fastf1.get_session(2026, round_number, "S")
    sprint_race_session.load()

    #race_results = race_session.results.reset_index(drop = True, inplace = True) # this just changes the index to normal instead of the drivers numbers
    sprint_race_results_df = sprint_race_session.results[["Abbreviation", "TeamName","Position","Points", "Status"]]
    #race_results_df.index = race_results_df.index + 1
    
    for row in sprint_race_results_df.itertuples():
        if row.Status in ["Finished", "Lapped"]:
            sprint_race_place[row.Abbreviation] = row.Position
        else:
            sprint_race_place[row.Abbreviation] = "NC/DSQ"
    return sprint_race_place

def sprint_race_fantasy_score(dictionary, fant_score_sprint_race = None):
    """Gives the fantasy score for the sprint race"""
    if fant_score_sprint_race is None:
        fant_score_sprint_race = {}
    sprint_race_scoring = {1:8, 2:7, 3:6, 4:5, 5:4, 6:3, 7:2, 8:1}
    
    for k,v in dictionary.items():
        fant_score_sprint_race.setdefault(k,0)
        if v!= "NC/DSQ":
            fant_score_sprint_race[k] += sprint_race_scoring.get(v,0)
        else:
            fant_score_sprint_race[k] = -10

    return fant_score_sprint_race



def fantasy_score_quali_plus_race(quali_point_dict, race_point_dict):
    """Makes it easy to add two dictionaries together"""
    # I need to add the points from the quali and the race    
    total_fant_points_dict = {}
    for k,v in quali_point_dict.items():
        total_fant_points_dict[k] = v + race_point_dict[k] 
    return total_fant_points_dict


# def fantasy_score_normal_weekend(round_number):
#     """Gives the fantasy score for a normal weekend"""
#     # if round_number in sprint_weekends:
#     #     sprint_race_fantasy_score(sprint_race_position(round_number))
    
#     position = quali_position(round_number)
#     quali_points_dict = quali_fantasy_score(position)
#     position2 = race_position(round_number)
#     race_points_dict = race_fantasy_score(position2)
#     return fantasy_score_quali_plus_race(quali_points_dict, race_points_dict)


def fantasy_score_weekend(round_number):
    """Gives the fantasy score for a whole weekend"""
    if round_number in sprint_weekends: # scoring for a sprint weekend
        sprint_position = sprint_race_position(round_number)
        sprint_points = sprint_race_fantasy_score(sprint_position)
        position = quali_position(round_number)
        quali_points_dict = quali_fantasy_score(position)
        position2 = race_position(round_number)
        race_points_dict = race_fantasy_score(position2)
        quali_and_race_points = fantasy_score_quali_plus_race(quali_points_dict, race_points_dict)
        return fantasy_score_quali_plus_race(sprint_points, quali_and_race_points)
    else: #scoring for a normal weekend
        position = quali_position(round_number)
        quali_points_dict = quali_fantasy_score(position)
        position2 = race_position(round_number)
        race_points_dict = race_fantasy_score(position2)
        quali_and_race_points = fantasy_score_quali_plus_race(quali_points_dict, race_points_dict)
        return quali_and_race_points
    
# def clear_score():
#     fant_score_race = {}
#     race_fantasy_score(1)



