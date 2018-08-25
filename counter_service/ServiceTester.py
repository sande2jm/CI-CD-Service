import requests
import json
class ServiceTester():
	def __init__(self):
		self.restApi = ['getCounter', 'increment']
		self.service_public_dns_filepath = 'config/counter_service_public_dns_name.txt'
		self.service_public_dns = None

	def getPublicDNS(self):
		if not self.service_public_dns:
			with open(self.service_public_dns_filepath, 'r+') as f:
				self.service_public_dns = 'http://' + f.readline().rstrip() + '/'
			print('Hitting AWS at ' +self.service_public_dns)

	def jsonPing(self, cmd):
		r = requests.get(self.service_public_dns + cmd)
		json_data = json.loads(r.text)
		print(r, json_data)
	def noJsonPing(self, cmd):
		r = requests.get(self.service_public_dns + cmd)
		print(r)
	def setCounter(self,value):
		payload = {'value': str(value)}
		r = requests.post(self.service_public_dns + 'setCounter', params=payload)

if __name__ == '__main__':
	s = ServiceTester()
	s.getPublicDNS()
	print("Creating User Acceptance Test ")
	s.setCounter(0)
	for i in range(100):
		s.noJsonPing('increment')
	for i in range(1):
		s.jsonPing('getCounter')