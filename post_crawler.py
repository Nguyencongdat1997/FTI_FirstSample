from facebookapi_connector import FacebookAPIConnector
from mongodb_connector import UserDAO,PostDAO,CommentDAO
from file_saver import PostSaver

facebookapi_connector = FacebookAPIConnector()
user_dao = UserDAO()
post_saver = PostSaver()

count = 0
user_ids = user_dao.find_all_ids()[:20]
for uid in user_ids:
	uid = uid['_id'].encode('utf-8')
	user_posts = facebookapi_connector.get_posts_of_one_user(uid)
	for post_id in user_posts:
		post = user_posts[post_id]
		post_saver.write_to_file(post_id + '|' + post[0].replace('\n',' ') + '|' + post[1])
		count += 1
		print (str(count) + ':' + post_id)