import os
import pytz
from sqlalchemy import create_engine
from datetime import datetime, timezone
from sqlalchemy_utils import database_exists, create_database
from flask import Flask, render_template, url_for, request, redirect

from models import db

from waitress import serve

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)
else:
    # Connect the database if exists.
    engine.connect()

from models import Message
with app.app_context():
	db.create_all()

@app.route('/')
def home():

	local_tz = pytz.timezone('Asia/Kuala_Lumpur')
	utc_tz = pytz.timezone('UTC')

	messages = Message.query.order_by(Message.created_at.desc()).all()

	for message in messages:
		date = message.created_at
		date = utc_tz.localize(date)
		date = local_tz.normalize(date.astimezone(local_tz))
		message.created_at = date		

	return render_template('home.html', messages = messages)

@app.route('/proc', methods = ['POST'])
def proc():

	message = request.form['message']
	if (message != None) and (message != ""):
		msg = Message(message = message)
		db.session.add(msg)
		db.session.commit()

	return redirect(url_for('home'))

if __name__=='__main__':

	serve(app, listen='*:8080')

	#Uncomment to run in debug mode. FOR DEVELOPMENT USE ONLY
	#app.run(debug = True)
