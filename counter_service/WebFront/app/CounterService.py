import boto3
import requests
import json
class CounterService():
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
		counter_service_info = self.getServiceInfoByName('counter_service')
		counter = int(counter_service_info['counter'])
		if counter %25 == 0:			
			self.hitGenerateIdService(counter)
		return counter

	def setCounter(self,value):
		self.table.update_item(
		    Key={
		    'service_name': 'counter_service'
		    },
		    UpdateExpression='SET #y = :val2',
		    ExpressionAttributeNames={
		        '#y': 'counter'
		    },
		    ExpressionAttributeValues={
		        ':val2': str(value)
		    }
		)

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

	def hitGenerateIdService(self, num):
		generate_id_service_info = self.getServiceInfoByName('generate_id_service')
		payload = {'name': str(num)}
		r = requests.post(generate_id_service_info['public_dns_name'] + 'getId', params=payload)




		