import requests
import json
class ServiceTester():
	def __init__(self):
		self.serviceName = 'register_service'
		self.restApi = ['getCounter', 'increment']
		self.service_public_dns_filepath = 'config/' + self.serviceName + '_public_dns_name.txt'
		self.service_public_dns = None

	def getPublicDNS(self):
		with open(self.service_public_dns_filepath, 'r+') as f:
			self.service_public_dns = 'http://' + f.readline().rstrip() + '/'
	def test_registering_user(self):
		payload = {'uid': '234132451234', 'name': 'Jacob Sanders'}
		r = requests.post(self.service_public_dns + 'registerUser', params=payload)

if __name__ == '__main__':
	s = ServiceTester()
	s.getPublicDNS()
	s.test_registering_user()
	