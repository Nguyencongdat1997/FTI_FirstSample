from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

#const
INVALID_TIMESTAMP = 'INVALID'

db = SQLAlchemy()
#engine = create_engine('postgresql://python:python@127.0.0.1/production') # connection properties stored

def compare_timestamps(timestamp1, timestamp2):
	time1 = datetime.datetime.strptime(timestamp1, "%Y-%m-%d %H:%M:%S")
	time2 = datetime.datetime.strptime(timestamp2, "%Y-%m-%d %H:%M:%S")
	return time1 > time2


class Token(db.Model):
	id = db.Column('id', db.Integer, primary_key = True)
	token_value = db.Column(db.String(100))
	valid_time = db.Column(db.String(50))
	
	def __init__(self, token_value, valid_time):
		self.token_value = token_value
		self.valid_time = valid_time
	
	
class TokenDAO(object):
	def insert_one(self, new_token_value):
		db.session.add(Token(token_value = new_token_value, valid_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
		db.session.commit()
	
	def get_one_validated(self):
		now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		for token in Token.query.all():
			if (token.valid_time != INVALID_TIMESTAMP) and (compare_timestamps(now, token.valid_time) > 0):
				return token.token_value
		return None

	def revalidate_one(self, token_value):
		db.session.query(Token).filter(Token.token_value == token_value).update({Token.valid_time: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
		db.session.commit()

	def block_one(self, token_value):
		db.session.query(Token).filter(Token.token_value == token_value).update({Token.valid_time: INVALID_TIMESTAMP})
		db.session.commit()

	def pause_one(self, token_value):
		new_time = datetime.datetime.now() + datetime.timedelta(seconds=100)
		db.session.query(Token).filter(Token.token_value == token_value).update({Token.valid_time: new_time.strftime("%Y-%m-%d %H:%M:%S")})				
		db.session.commit()

