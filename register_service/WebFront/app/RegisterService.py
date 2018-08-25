import boto3
class RegisterService():
	def __init__(self):
		self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		self.table = self.dynamodb.Table('CI-CD-Users')
		
		
	def registerUser(self, uid, name):
		self.table.put_item(
		    Item={
		    'id': uid,
		    'name': name
		    }
		)


		

		

		