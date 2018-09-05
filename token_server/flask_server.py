from flask import Flask, g, jsonify
from sqlite_models import db
from sqlite_models import Token
from sqlite_models import TokenDAO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///token.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

@app.route("/get")
def get_token():
	token = token_dao.get_one_validated()
	if token == None:
		return jsonify('Error: No token available')
	return jsonify(token), 200


@app.route("/insert/<value>")
def insert_token(value):
	token_dao.insert_one(value)
	return 'OK', 201


@app.route("/pause/<value>")
def pause_token(value):
	token_dao.pause_one(value)
	return 'OK', 200


@app.route("/block/<value>")
def block_token(value):
	token_dao.block_one(value)
	return 'OK', 200


@app.route("/cleardb")
def clear_database():
	meta = db.metadata
	for table in reversed(meta.sorted_tables):
		print 'Clear table %s' % table
		db.session.execute(table.delete())
	db.session.commit()
	return 'OK', 200


@app.route("/view")
def view_all_tokens():
	tokens = db.session.query(Token).all()
	result = ''
	for x in tokens:
	 result += x.token_value + ':' + x.valid_time + '\n'
	return result, 200


token_dao = TokenDAO()
app.run()

#db.create_all()



