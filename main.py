from flask import (Flask, abort, flash, jsonify, make_response, redirect, render_template, request, session, url_for, Markup,session)

# from flask.ext.session import Session

from flask_sqlalchemy import SQLAlchemy
import pandas as pd
# from send_mail import send_mail
from nfl.week import nflmain
import datetime
import pytz
from app import app

# app = Flask(__name__)
est = pytz.timezone('US/Eastern')

#TODO: leadpipes layout, drag and drop to right for fav, dog, etc.
#TODO: or instead of drag drop, place labels on picks with fav, dog, etc?
# or drag drop for computer, select for mobile?
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

# Date conversion functions
def UnixToTimeEST(row):
    return datetime.datetime.utcfromtimestamp(int(row.start_time)/1000).replace(tzinfo=pytz.utc).astimezone(est).strftime("%-I:%M %p ET")
def UnixToDateEST(row):
    return datetime.datetime.utcfromtimestamp(int(row.start_time)/1000).replace(tzinfo=pytz.utc).astimezone(est).strftime("%Y-%m-%d")

# Value lookup functions
def renderPick(row,lookupdf,type_of_pick):
    gameid_pipe_value = row[f'input-{type_of_pick}']
    game_id = gameid_pipe_value.split("|")[0]
    value = gameid_pipe_value.split("|")[1]
    matchup = lookupdf.loc[lookupdf['game_id']==int(game_id), 'matchup'].iloc[0]
    favorite = lookupdf.loc[lookupdf['game_id']==int(game_id), 'fav_spread'].iloc[0]
    underdog = lookupdf.loc[lookupdf['game_id']==int(game_id), 'dog_spread'].iloc[0]

    if type_of_pick == 'over' or type_of_pick == 'under':
        return matchup + f" {type_of_pick[0]}" + value
    elif type_of_pick == 'favorite':
        return favorite
    elif type_of_pick == 'underdog':
        return underdog
    # else:
    #     return 'test'
        
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)


# class Feedback(db.Model):
#     __tablename__ = 'feedback'
#     id = db.Column(db.Integer, primary_key=True)
#     customer = db.Column(db.String(200), unique=True)
#     dealer = db.Column(db.String(200))
#     rating = db.Column(db.Integer)
#     comments = db.Column(db.Text())

#     def __init__(self, customer, dealer, rating, comments):
#         self.customer = customer
#         self.dealer = dealer
#         self.rating = rating
#         self.comments = comments

# sort df by time and team1 name
# df = nflmain()
# df.to_csv('sampledf.csv',index=False)
# df_picks = df[['start_time','fav_spread','dog_spread','O/U']]
df = pd.read_csv('sampledf.csv')
df['date'] = df.apply(lambda row: UnixToDateEST(row),axis=1)
df['time'] = df.apply(lambda row: UnixToTimeEST(row),axis=1)
df['matchup'] = df['team1_name']+' @ '+df['team2_name']
# df['date'] = df.utc_date.dt.tz_localize('UTC').tz_convert('US/Eastern').strftime("%H:%M:%S")
# utc_timestamp = datetime.utcfromtimestamp(ts)
#             utc_tz_ts = utc_timestamp.replace(tzinfo=pytz.utc)
#             time = utc_tz_ts.astimezone(est)
# df_picks=df[['date','time','matchup','fav_spread','dog_spread','O/U']]
df_picks = df
days = df_picks['date'].unique()
times = df_picks['time'].unique()

#TODO: get unique days, then loop through by those days. Plant the day, then get everything underneath it, loop.
# @app.route('/')
# def index():
#     return render_template('index.html',
#                             unique_days = days, 
#                             unique_times = times,
#                             records=df_picks,#.to_dict(orient='records'),
#                             columns=df_picks.columns)
@app.route('/',methods = ['GET', 'POST'])
def index():
    return render_template('index.html',
                            unique_days = days, 
                            unique_times = times,
                            records=df_picks,#.to_dict(orient='records'),
                            columns=df_picks.columns)

@app.route('/select',methods = ['POST'])
def select():
    global df_picks
    type_of_picks_list = ['input-over','input-under','input-favorite','input-underdog']
    #TODO: Check for validity of selections (missing a type, )
    if request.method == 'POST':
        # flash(request.form)
        # print(request.form)
        gameids_and_picks = request.form.to_dict(flat=False)
        # df_selectedpicks = pd.DataFrame(gameids_and_picks)
        # for key,value in gameids_and_picks.items():
        #     flash(key)
        #     flash(value)

        # return render_template('index.html',
        #                     unique_days = days, 
        #                     unique_times = times,
        #                     records=df_picks,#.to_dict(orient='records'),
        #                     columns=df_picks.columns)
        # # df_selectedpicks['render-over'] = df_selectedpicks.apply(lambda row: df_picks.loc[df_picks['game_id']==df_selectedpicks['input-over'].split("|")[0], 'matchup'] + " " + df_selectedpicks['input-over'].split("|")[1]
        # for type_of_pick in type_of_picks_list:
        #     try:
        #         df_selectedpicks[f'render-{type_of_pick}'] = df_selectedpicks.apply(lambda row: renderPick(row,df_picks,type_of_pick),axis=1)
        #     except Exception as e:
        #         flash("You're missing ")

        # # in format of [{}]
        # df_selectedpicks_dict = df_selectedpicks.to_dict(orient='records')
        flash(gameids_and_picks)
        return render_template('select.html', records = gameids_and_picks, df = gameids_and_picks, type_of_picks_list=type_of_picks_list)

@app.route('/success',methods = ['POST'])
def success():
    if request.method == 'POST':
        flash(request.form)
        print(request.form)
        return render_template('success.html')

# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         customer = request.form['customer']
#         dealer = request.form['dealer']
#         rating = request.form['rating']
#         comments = request.form['comments']
#         # print(customer, dealer, rating, comments)
#         if customer == '' or dealer == '':
#             return render_template('index.html', message='Please enter required fields')
#         if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
#             data = Feedback(customer, dealer, rating, comments)
#             db.session.add(data)
#             db.session.commit()
#             send_mail(customer, dealer, rating, comments)
#             return render_template('success.html')
#         return render_template('index.html', message='You have already submitted feedback')

if __name__ == '__main__':
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)

    # app.debug = True
    
    app.run()