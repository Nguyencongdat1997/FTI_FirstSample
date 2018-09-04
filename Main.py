from mongodb_connector import UserDAO,PostDAO,CommentDAO
from neo4j_connector import Neo4jConnector
from facebookapi_connector import FacebookAPIConnector

import Queue

#consts:
UNKNOWN_USER_ID = '00000000000'


def crawl_users():
	remain_queue = Queue.Queue()
	num_of_users = 0

	remain_queue.put('100001087643358')
	while num_of_users < 10:
		new_user_id = remain_queue.get()
		if new_user_id == None:
			break

		new_user_name, new_user_friend_ids= facebookapi_connector.get_one_user_data(new_user_id)
		print(new_user_id + ' : ' + new_user_name)

		user_dao.insert_one(new_user_id, new_user_name)		
		neo4j_connector.create_node('User', new_user_id)

		for x in new_user_friend_ids:
			if user_dao.find_one(x):
				continue
			remain_queue.put(x)
		num_of_users += 1


def crawl_friendships():
	user_ids = user_dao.find_all_ids()
	for uid in user_ids:
		uid = uid['_id'].encode('utf-8')
		user_friend_ids = facebookapi_connector.get_one_user_friends(uid)
		for x in user_friend_ids:
			if user_dao.find_one(x):
				print(uid + ' -Friend_of-> ' + x)
				neo4j_connector.create_relationship(uid, x, 'Friend_of')			


def crawl_posts():
	user_ids = user_dao.find_all_ids()
	for uid in user_ids:
		uid = uid['_id'].encode('utf-8')
		user_posts = facebookapi_connector.get_posts_of_one_user(uid)
		for post_id in user_posts:
			post = user_posts[post_id]
			if user_dao.find_one(post[1]):
				print('Post: ' + post[1] + '-Create->' + post_id)
				post_dao.insert_one(post_id, post[0])
				neo4j_connector.create_node('Post', post_id)
				neo4j_connector.create_relationship(post[1], post_id, 'Create')

				comments = post[2]
				for comment_id in comments:
					comment = comments[comment_id]
					if user_dao.find_one(comment[1]):
						print('Comment: '+ comment[1] + '-Create->' + comment_id)
						comment_dao.insert_one(comment_id, comment[0])
						neo4j_connector.create_node('Comment', comment_id)
						neo4j_connector.create_relationship(comment[1], comment_id, 'Create')
						neo4j_connector.create_relationship(post_id, comment_id, 'Contain')


user_dao = UserDAO()
post_dao = PostDAO()
comment_dao = CommentDAO()
neo4j_connector = Neo4jConnector()
facebookapi_connector = FacebookAPIConnector()
crawl_users()
crawl_friendships()
crawl_posts()
