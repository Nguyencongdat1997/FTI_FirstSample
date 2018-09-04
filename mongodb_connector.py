import pymongo


class MongoDAOBase(object):	

	def __init__(self):
		self.mongo_client = pymongo.MongoClient('mongodb://localhost:27017/')
		self.mongo_database = self.mongo_client['FirstSample']


class UserDAO(MongoDAOBase):	

	def __init__(self):
		super(UserDAO,self).__init__()   
		self.collection = self.mongo_database['User']

	def insert_one(self, uid, name):
		if self.find_one(uid) != None:
			print('User ' + uid + ' has already been in list.')
			return None
		mydict = {'_id': uid, 'name': name}
		x = self.collection.insert_one(mydict)

	def find_one(self, uid):
		for x in self.collection.find({'_id': uid}):
  			return x
  		return None

	def find_all(self):
		return self.collection.find()

	def find_all_ids(self):
		return self.collection.find({},{"name": 0})

	def print_all(self):
		for x in self.collection.find():
			print(x)
			

class PostDAO(MongoDAOBase):	

	def __init__(self):
		super(PostDAO,self).__init__()   
		self.collection = self.mongo_database['Post']

	def insert_one(self, pid, message):
		if self.find_one(pid) != None:
			print('Post ' + pid + ' has already been in list.')
			return None
		mydict = {'_id': pid, 'message': message}
		x = self.collection.insert_one(mydict)

	def find_one(self, pid):
		for x in self.collection.find({'_id': pid}):
  			return x
  		return None

	def find_all(self):
		return self.collection.find()

	def find_all_ids(self):
		return self.collection.find({},{"message": 0})

	def print_all(self):
		for x in self.collection.find():
			print(x)
			

class CommentDAO(MongoDAOBase):	

	def __init__(self):
		super(CommentDAO, self).__init__()   
		self.collection = self.mongo_database['Comment']

	def insert_one(self, cid, message):
		if self.find_one(cid) != None:
			print('Comment ' + cid + ' has already been in list.')
			return None
		mydict = {'_id': cid, 'message': message}
		x = self.collection.insert_one(mydict)

	def find_one(self, cid):
		for x in self.collection.find({'_id': cid}):
  			return x
  		return None

	def find_all(self):
		return self.collection.find()

	def find_all_ids(self):
		return self.collection.find({}, {"message": 0})

	def print_all(self):
		for x in self.collection.find():
			print(x)


