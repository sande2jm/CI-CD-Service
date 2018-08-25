import boto3
import requests
from uuid import uuid4
class GenerateIdService():
	def __init__(self):
		self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		self.table = self.dynamodb.Table('Service_State_Variables')
		self.counter = 0
		
	def getServiceInfoByName(self,name):
		info = self.table.get_item(
			Key={
			'service_name': name
			})
		return info['Item']

	def getCounter(self):
		state = self.table.get_item(
			Key={
			'service_name': 'counter_service'
			})
		return int(state['Item']['counter'])
		

	def increment(self):
		self.table.update_item(
		    Key={
		    'service_name': 'counter_service'
		    },
		    UpdateExpression='SET #y = :val2',
		    ExpressionAttributeNames={
		        '#y': 'counter'
		    },
		    ExpressionAttributeValues={
		        ':val2': str(self.getCounter()+1)
		    }
		)

	def getUniqueId(self):
		return str(uuid4())

	def getId(self, name):
		uid = self.getUniqueId()
		register_service = self.getServiceInfoByName('register_service')
		payload = {'uid': uid, 'name': name}
		r = requests.post(register_service['public_dns_name'] + 'registerUser', params=payload)
		return 'Called GetID'
		

		

		