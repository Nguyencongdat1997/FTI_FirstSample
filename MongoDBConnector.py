import pymongo

class MongoDAOBase(object):	
	def __init__(self):
		self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
		self.mongo_database = self.mongo_client["FirstSample"]

class UserDAO(MongoDAOBase):	
	def __init__(self):
		super(UserDAO,self).__init__()
		self.collection = self.mongo_database["User"]
	def insertOne(self,uid,name,friend_ids):
		if self.findOne(uid) != None:
			print("User "+uid+" has already been in list.")
			return 
		mydict = { "_id" : uid, "name": name, "friendIds" :friend_ids }
		x = self.collection.insert_one(mydict)
		print(x.inserted_id)
	def findOne(self,uid):
		for x in self.collection.find({ "_id": uid }):
  			return x
  		return None
	def findAll(self):
		return self.collection.find()
	def printAll(self):
		for x in self.collection.find():
			print(x)
			
			


