import requests
import json
import boto3
class ServiceTester():
	def __init__(self):
		self.serviceName = 'generate_id_service'
		self.restApi = ['getCounter', 'increment']
		self.service_public_dns_filepath = 'config/' + self.serviceName + '_public_dns_name.txt'
		self.service_public_dns = None
		self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		self.table = self.dynamodb.Table('Service_State_Variables')

	def getServiceInfoByName(self,name):
		info = self.table.get_item(
			Key={
			'service_name': name
			})
		return info['Item']

	def getPublicDNS(self):
		with open(self.service_public_dns_filepath, 'r+') as f:
			self.service_public_dns = 'http://' + f.readline().rstrip() + '/'

	def test_get_id_method(self):
		generate_id_service_info = self.getServiceInfoByName('generate_id_service')
		payload = {'name': 'Jacob Sanders'}
		print(generate_id_service_info['public_dns_name'])
		r = requests.post(generate_id_service_info['public_dns_name'] + 'getId', params=payload)
		print(r.text)

	# def test_register_user_method(self):
	# 	register_service = self.getServiceInfoByName('register_service')
	# 	payload = {'uid': '555555555', 'name': 'Jessica'}
	# 	r = requests.post(register_service['public_dns_name'] + 'registerUser', params=payload)
	# 	print(r)


if __name__ == '__main__':
	s = ServiceTester()
	s.getPublicDNS()
	s.test_get_id_method()
	