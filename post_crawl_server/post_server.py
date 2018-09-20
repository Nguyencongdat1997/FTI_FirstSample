from flask import Flask, g, jsonify
from redis import Redis
import sys
sys.path.insert(0, './utilities')
from facebookapi_connector import FacebookAPIConnector
from file_saver import PostSaver
import json
import datetime

app = Flask(__name__)

@app.route("/hello")
def home():
	return 'Welcome'

@app.route("/crawl/<uid>/<since>/<limit>")
def crawl(uid, since, limit):
	#sample request: http://localhost:5001/crawl/100001087643358/2000-01-01T00:00:00/30
	#facebookapi_connector.get_token()
	count = 0
	user_posts = facebookapi_connector.get_posts_of_one_user(uid = uid, since = since, limit = limit)
	for post_id in user_posts:
		post = user_posts[post_id]
		data_to_save = dict(
			post_id = post_id, 
			user_id = uid, 
			message = post[0], 
			creator_id= post[1], 
			like= post[2]['LIKE'], 
			love= post[2]['LOVE'],
			wow= post[2]['WOW'], 
			haha= post[2]['HAHA'], 
			sad= post[2]['SAD'], 
			angry= post[2]['ANGRY'], 
			thankful= post[2]['THANKFUL'], 
			time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')
		)		
		data_to_save = dict((k,str(v)) for k,v in data_to_save.items())
		print(data_to_save)
		post_saver.write_to_file(json.dumps(data_to_save, ensure_ascii = False).encode('utf-8'))
		count += 1
		print(str(count))
	return '200'

facebookapi_connector = FacebookAPIConnector()
#user_dao = UserDAO()
post_saver = PostSaver()
app.run(host="0.0.0.0",port="5001",debug=True)

#db.create_all()



