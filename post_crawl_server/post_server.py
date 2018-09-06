from flask import Flask, g, jsonify
import sys
sys.path.insert(0, './utilities')
from facebookapi_connector import FacebookAPIConnector
from mongodb_connector import UserDAO,PostDAO,CommentDAO
from file_saver import PostSaver
import json
import datetime

app = Flask(__name__)


@app.route("/crawl/<uid>/<limit>")
def crawl(uid, limit):
	#facebookapi_connector.get_token()
	count = 0
	user_posts = facebookapi_connector.get_posts_of_one_user(uid = uid, since = '2000-01-01T00:00:00', limit = limit)
	for post_id in user_posts:
		post = user_posts[post_id]
		data_to_save = dict(post_id = post_id, user_id = uid, message = post[0], creator_id= post[1], time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))		
		print data_to_save
		post_saver.write_to_file(json.dumps(data_to_save, ensure_ascii = True, encoding = 'utf-8'))
		count += 1
		print (str(count))
	return '200'

facebookapi_connector = FacebookAPIConnector()
user_dao = UserDAO()
post_saver = PostSaver()
app.run(port=5001)

#db.create_all()



