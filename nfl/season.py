"""
season.py is a script thats meant to get all games for the season, 
"""

import requests
import pandas as pd
from datetime import datetime,date, timedelta
import pytz
from calendar import WEDNESDAY
import json

est = pytz.timezone('US/Eastern')
utc = pytz.utc
utc_now = pytz.utc.localize(datetime.utcnow())
fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    
# Returns all Wednesdays for provided date range, not from 2021 to 2023 9 AM UTC
def getDateRange(last_wednesday,next_wednesday):
    # utc_timestamp = datetime.utcfromtimestamp(ts)
    # utc_tz_ts = utc_timestamp.replace(tzinfo=pytz.utc)
    return pd.date_range(start=last_wednesday, 
                        end=next_wednesday, 
                        freq='W-WED',tz='UTC').tolist()   

def assign_fav_spread(row):
    if "-" in str(row.spread):
        return row.team2_name+" "+str(row.spread)
    elif row.spread =="NOT FOUND":
        return row.spread
    else:
        return row.team1_name+" -"+str(row.spread)
def assign_dog_spread(row):
    if "-" in str(row.spread):
        return (row.team1_name+" +"+str(row.spread)).replace("-","")
    elif row.spread =="NOT FOUND":
        return row.spread
    else:
        return row.team2_name+" +"+str(row.spread)

def nflmain():
    wed_list = [int(datetime(2021, 9, 7, hour=9, minute=0).timestamp()*1000),int(datetime(2022, 1, 12, hour=9, minute=0).timestamp()*1000)]
    print(wed_list)
    daterange_list=wed_list
    # for i in range(len(tues_list)-1):
    # daterange_list.append(int(tues_list[i].timestamp()*1000))
    # daterange_list.append(int(tues_list[i+1].timestamp()*1000))
    startdate = daterange_list[0]
    enddate = daterange_list[1]
    # Get all games for Week 16:
    games_url = f"https://areyouwatchingthis.com/api/games.json?sport=nfl&startDate={startdate}&endDate={enddate}"
    games = requests.get(games_url)
    games_json = games.json()
    # games_json.dumps('test.json')
    # with open('test.json', 'w') as f:
    #     json.dump(games_json, f)
    # print(games_json)
    game_ids,team1_ids,team1_names,team2_ids,team2_names,starttimes,gametime_left,spreads,over_unders = [],[],[],[],[],[],[],[],[]
    # df = pd.DataFrame(columns=['team1_id','team2_id','game_id','start'])
    for game in games_json["results"]:
        game_ids.append(game["gameID"])
        team1_ids.append(game["team1ID"])
        team1_names.append(game["team1Name"])
        team2_ids.append(game["team2ID"])
        team2_names.append(game["team2Name"])
        #team1Score for score
        starttimes.append(game["date"])
        # Add time left in game
        try:
            gametime_left.append(game["timeLeft"])
        except:
            gametime_left.append(game["date"])
    game_dict = {"game_id":game_ids,"team1_id":team1_ids,"team1_name":team1_names,"team2_id":team2_ids,"team2_name":team2_names,"start_time":starttimes,"time_left":gametime_left}
    df = pd.DataFrame(data=game_dict)
    return df
allgames = nflmain()[['team1_id','team1_name']].drop_duplicates().reset_index(drop=True)
# allgames.to_csv('teams.csv',index=False)
print(allgames)


#TODO:
# change to wednesday
# Separate script:
    # get whole season instead 
    # ^ break out by weeks
    # from whole season info, get all team IDs to create teams table