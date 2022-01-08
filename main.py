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

def UnixToTimeEST(row):
    return datetime.datetime.utcfromtimestamp(int(row.start_time)/1000).replace(tzinfo=pytz.utc).astimezone(est).strftime("%-I:%M %p ET")
def UnixToDateEST(row):
    return datetime.datetime.utcfromtimestamp(int(row.start_time)/1000).replace(tzinfo=pytz.utc).astimezone(est).strftime("%Y-%m-%d")
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
@app.route('/success',methods = ['POST'])
def success():
    if request.method == 'POST':
        flash(request.form)
        print(request.form)
        return render_template('success.html')
        # return redirect(url_for('success'))
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