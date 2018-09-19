import sys
sys.path.insert(0, './utilities')
from facebookapi_connector import FacebookAPIConnector
from mongodb_connector import UserDAO,PostDAO,CommentDAO
from file_saver import PostSaver
import json
import datetime

facebookapi_connector = FacebookAPIConnector()
#facebookapi_connector.get_token()
user_dao = UserDAO()
post_saver = PostSaver()

count = 0
user_ids = user_dao.find_all_ids()[:20]
for uid in user_ids:
	uid = uid['_id'].encode('utf-8')
	user_posts = facebookapi_connector.get_posts_of_one_user(uid,'2000-01-01T00:00:00',30)
	for post_id in user_posts:
		post = user_posts[post_id]
		data_to_save = dict(post_id = post_id, user_id = uid, message = post[0], creator_id= post[1], time_stamp = str(datetime.datetime.now()))		
		post_saver.write_to_file(json.dumps(data_to_save, ensure_ascii = False, encoding = 'utf-8'))
		count += 1
		print (str(count) + ':' + post_id)