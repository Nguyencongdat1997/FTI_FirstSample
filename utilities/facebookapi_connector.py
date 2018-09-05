import requests


class FacebookAPIConnector(object):	

	def __init__(self):
		self.url = 'https://graph.facebook.com/'
		self.access_token = 'EAAAAAYsX7TsBACYOsVKFOLtRB2WOG0Fp53IU07ffjZCZB4LQRlNsQxS3wZC0YhxNcE00FjKPxNiO6xSi129cgovRbh2AoNDoNoT6TJQNAAKeZCupKMfrp9Su8DbROVHnTGJEK6ecBs1Qi7zcZCFPaadKZAtZCUwJ3tB9FOGmJfyFtLJ1GteYIwD'

	def get_token(self):
		response = requests.get(url='http://localhost:5000/get')		
		if response.json() != 'Error: No token available':
			self.access_token = response.json()
			print('Update new token: ' + self.access_token)
		else:
			print(response.json())
		return None

	def get_json_attribute(self, data, attribute, default_value):
		return data.get(attribute) or default_value

	def get_one_user_data(self, uid):		
		params = dict(
			id = uid,
			fields = 'id,name,friends',
			access_token = self.access_token
		)
		response = requests.get(url=self.url, params=params)

		name = response.json()['name'].encode('utf-8')
		friend_ids = [x['id'].encode('utf-8') for x in self.get_json_attribute(response.json(), 'friends', {'data':[]})['data']]
		return name, friend_ids


	def get_one_user_friends(self, uid):
		params = dict(
			id = uid,
			fields = 'id,friends',
			access_token = self.access_token
		)
		response = requests.get(url=self.url, params=params)

		friend_ids = [x['id'].encode('utf-8') for x in self.get_json_attribute(response.json(), 'friends', {'data':[]})['data']]
		return friend_ids


	def get_posts_of_one_user(self, uid):
		url = self.url + uid + '/feed/'
		params = dict(
			fields = 'id,from,message,comments',
			access_token = self.access_token
		)
		response = requests.get(url=url, params=params)

		list_posts = {}
		list_posts_raw = self.get_json_attribute(response.json(), 'data', [])
		for post_raw in list_posts_raw:
			post_id = post_raw['id'].encode('utf-8')
			post_message = self.get_json_attribute(post_raw, 'message', '').encode('utf-8')
			post_creator_id = post_raw['from']['id'].encode('utf-8')

			list_comments = {}
			list_comments_raw = self.get_json_attribute(post_raw['comments'], 'data', [])
			for comment_raw in list_comments_raw:
				comment_id =  comment_raw['id'].encode('utf-8')
				comment_message = comment_raw['message'].encode('utf-8')
				comment_creator_id = comment_raw['from']['id'].encode('utf-8')
				list_comments[comment_id] = [comment_message, comment_creator_id]

			list_posts[post_id] = [post_message, post_creator_id, list_comments]

		return list_posts
