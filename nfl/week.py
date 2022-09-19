# import southpaw
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

# token = 'NzczMjgzODBmNzVmMWE5ZjUyMzQxZjZjNDRjNmZiYTY6'
# basic_auth_token = f'Basic {token}'
# fanduel_email = 'abbatemich1@gmail.com'
# fanduel_password = ''

# fd = southpaw.Fanduel(fanduel_email, fanduel_password, basic_auth_token)
# print(fd.get_upcoming())



def getLastWednesday():
    offset = (utc_now.weekday() - WEDNESDAY) % 7
    last_wednesday = utc_now - timedelta(days=offset)
    # last_tuesday_millis = int(last_tuesday.timestamp()*1000)
    return last_wednesday.replace(hour=9,minute=0)

def getNextWednesday():
    offset = (WEDNESDAY - utc_now.weekday()) % 7
    next_wednesday = utc_now + timedelta(days=(offset))
    return next_wednesday.replace(hour=9,minute=0)
    
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
    wed_list = [int(getLastWednesday().timestamp()*1000),int(getNextWednesday().timestamp()*1000)]
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
    game_dict = {"game_id":game_ids,"team1_name":team1_names,"team2_name":team2_names,"start_time":starttimes,"time_left":gametime_left}
    df = pd.DataFrame(data=game_dict)

    # Get info for each game
    for gameID in df['game_id']:
        r = requests.get(f"https://areyouwatchingthis.com/api/odds.json?gameID={gameID}")
        odds_json = r.json()
        # print("GAME ID:", gameID, odds_json["results"][0]["team1Name"], "vs.", odds_json["results"][0]["team2Name"])

        # Get odds data from each provider
        for line in odds_json["results"][0]["odds"]:
            # print(line)
            provider = line["provider"]
            ts = line["date"]/1000
            utc_timestamp = datetime.utcfromtimestamp(ts)
            utc_tz_ts = utc_timestamp.replace(tzinfo=pytz.utc)
            time = utc_tz_ts.astimezone(est)
            try:
                spread = line["spread"]
                o_u = line["overUnder"]
            except:
                spread = "NOT FOUND"
                o_u = "NOT FOUND"

            # Get FANDUEL lines (TODO: add check for line to be before the game start time)
            # if ((line["date"] < df.loc[df['game_id']==gameID,'start_time'].iloc[0]) & (provider=="FANDUEL")):
            if provider=="FANDUEL":
                spreads.append(spread)
                over_unders.append(o_u)
                # print("Provider:",provider, "Time:",time, " Spread:",spread," O/U:",o_u)
            #TODO: else need to make sure we get something to render!

            # if line["date"] < df.loc[df['game_id']==gameID,'start_time'].iloc[0]:
            #     print("Provider:",provider, "Time:",time, " Spread:",spread," O/U:",o_u)
        # print("******")
    print()
    # df["spread"]=df["team2_name"]+" "+spreads
    df["spread"]=spreads
    # df["spread"] = ["NOT FOUND" if "NOT FOUND" in value else value for value in df['spread']]
    # df["spread"] = [df['team1_name']+" -"+str(value) if "-" not in str(value) else df['team2_name']+" "+str(value) for value in df['spread']]
    df["fav_spread"]=df.apply(lambda row: assign_fav_spread(row), axis=1)
    df["dog_spread"]=df.apply(lambda row: assign_dog_spread(row), axis=1)
    df["O/U"]=over_unders
    return df
#TODO: 
# change to wednesday
# Separate script:
    # get whole season instead 
    # ^ break out by weeks
    # from whole season info, get all team IDs to create teams table