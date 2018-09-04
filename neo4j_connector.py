from neo4jrestclient import client


class Neo4jConnector(object):	

	def __init__(self):
		self.neo4j_gdb = client.GraphDatabase('http://localhost:7474/db/data/', username='neo4j', password='123456')
	
	def create_node(self, label, mongo_id):		
		if not self.is_node(mongo_id):
			new_node = self.neo4j_gdb.nodes.create(mongo_id=mongo_id)
			new_node.labels.add(label)

	def create_relationship(self, node_mongod_id1, node_mongod_id2, relationship):
		node1 = self.neo4j_gdb.query('MATCH (x{mongo_id: "' + node_mongod_id1 + '"}) RETURN x', returns=(client.Node))
		node2 = self.neo4j_gdb.query('MATCH (x{mongo_id: "' + node_mongod_id2 + '"}) RETURN x', returns=(client.Node))
		
		if (
			  len(node1)==1 
			  and len(node2)==1 
			  and len(node1[0])==1 
			  and len(node2[0])==1 
		 	  and not self.is_related(node_mongod_id1, node_mongod_id2, relationship)
		 	  and not self.is_related(node_mongod_id2, node_mongod_id1, relationship)
			):
			rel = self.neo4j_gdb.relationships.create(node1[0][0], relationship, node2[0][0])

	def is_node(self, mongo_id):
		node = self.neo4j_gdb.query('MATCH (x{mongo_id: "' + mongo_id + '"}) RETURN x', returns=(client.Node))
		if len(node) != 0:
			return True
		return False

	def is_related(self, node_mongod_id1, node_mongod_id2, relationship):
		exist_rel = self.neo4j_gdb.query('MATCH '
										+ '(node1{mongo_id: "' + node_mongod_id1 + '"})'
									    + '-[r:' + relationship + ']->'
									    + '(node2{mongo_id: "' + node_mongod_id2 + '"})'
									    + ' RETURN r',
									    returns=(client.Relationship)
									    )
		if len(exist_rel) != 0:
			return True
		return False