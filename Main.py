from MongoDBConnector import UserDAO
import requests
import Queue

def getJsonAttribute(data, attribute, default_value):
    return data.get(attribute) or default_value

def getOneUserData(uid):
	url = 'https://graph.facebook.com/'
	params = dict(
		id=uid,
		fields='id,name,friends',
		access_token='EAAAAAYsX7TsBACYOsVKFOLtRB2WOG0Fp53IU07ffjZCZB4LQRlNsQxS3wZC0YhxNcE00FjKPxNiO6xSi129cgovRbh2AoNDoNoT6TJQNAAKeZCupKMfrp9Su8DbROVHnTGJEK6ecBs1Qi7zcZCFPaadKZAtZCUwJ3tB9FOGmJfyFtLJ1GteYIwD'
	)
	response = requests.get(url=url, params=params)

	name = response.json()["name"].encode("utf-8")
	friend_ids = [x["id"].encode("utf-8") for x in getJsonAttribute(response.json(),"friends",{"data":[]})["data"]]
	return name,friend_ids

if __name__ == "__main__":
	remain_queue = Queue.Queue()
	user_set = {}	

	remain_queue.put("100001087643358")
	while len(user_set)<1000:
		new_user_id = remain_queue.get()
		if new_user_id == None:
			break

		new_user_name,new_user_friend_ids = getOneUserData(new_user_id)
		user_set[new_user_id] = [new_user_name,new_user_friend_ids]
		print(new_user_id +" : "+ user_set[new_user_id][0])
		for x in new_user_friend_ids:
			if x in user_set:
				continue
			remain_queue.put(x)

	user_dao = UserDAO()
	for x in user_set:
		user_dao.insertOne(x,user_set[x][0],user_set[x][1][:20])
	user_dao.printAll()