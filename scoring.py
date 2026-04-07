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
    quali_results = quali_session.results.reset_index(drop = True, inplace = True) # this just changes the index to normal instead of the drivers numbers

    quali_results_df = quali_session.results[["Abbreviation", "TeamName", "Q1"]]
    quali_results_df.index = quali_results_df.index + 1

    for row in quali_results_df.itertuples():
        if not pd.isnull(row.Q1):
            quali_place[row.Abbreviation] = row.Index
        else:
            quali_place[row.Abbreviation] = "NC/DSQ"
    return quali_place


#fant_score_quali = {}
def quali_fantasy_score(dictionary, fant_score_quali = {}):
    """Gives the fantasy score from the qualifying round"""
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

    race_results = race_session.results.reset_index(drop = True, inplace = True) # this just changes the index to normal instead of the drivers numbers
    race_results_df = race_session.results[["Abbreviation", "TeamName","Points", "Status"]]
    race_results_df.index = race_results_df.index + 1
    return race_results_df





def race_fantasy_score(dictionary, fant_score_race = {}):
    race_scoring = {1:25, 2:18, 3:15, 4:12, 5:10, 6:8, 7:6, 8:4, 9:2, 10:1}
    






