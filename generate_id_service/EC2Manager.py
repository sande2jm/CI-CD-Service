import boto3
import time
import paramiko
from subprocess import call


class EC2Manager():
	def __init__(self):
		self.instances = []
		self.serviceName = 'generate_id_service'
		self.cmdList = {'get repo': 'git submodule add --force https://sande2jm@github.com/sande2jm/workflow_configuration.git', 
						'pull repo': 'git submodule update --recursive --remote',
						'delete repo': 'git rm -rf workflow_configuration',
						'push to repo': ['git submodule foreach git add * ', 
										'git submodule foreach git commit -m test',
										'git submodule foreach git push origin master'],
						'check docker': 'sudo docker --version',
						'docker login': 'sudo docker login --username=sande2jm --email=sande2jm@gmail.com',
						'run image': None,
						'pull image': None,
						'stop container': None}
		self.ec2_connection = boto3.resource('ec2', 'us-east-1')
		self.version_filepath = 'config/generate_id_service_version.txt'
		self.public_dns_filepath = 'config/generate_id_service_public_dns_name.txt'
		self.version = None
		self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		self.table = self.dynamodb.Table('Service_State_Variables')

	def updatePublicDNS(self):
		instance = self.instances[0]
		with open(self.public_dns_filepath, 'w') as f:
			f.write(instance.public_dns_name)
		self.table.update_item(
		    Key={
		    'service_name': 'generate_id_service'
		    },
		    UpdateExpression='SET #y = :val2',
		    ExpressionAttributeNames={
		        '#y': 'public_dns_name'
		    },
		    ExpressionAttributeValues={
		        ':val2': str('http://' + instance.public_dns_name + '/')
		    }
		)

	def gatherInstances(self):
		filters = [{'Name': 'tag:Name', 'Values': [self.serviceName]}, 
					{'Name': 'instance-state-name', 'Values': ['running']}]
		while len(self.instances) < 1:
			self.instances = [x for x in self.ec2_connection.instances.filter(Filters=filters)]
			time.sleep(1)

	def getVersion(self):
		with open(self.version_filepath, 'r+') as f:
			self.version = f.readline().rstrip()
		self.version = str(round(float(self.version) - 0.1, 1))
		
		self.cmdList['run image'] = 'sudo docker run -d -p 80:80 sande2jm/' + self.serviceName + ':' + self.version
		self.cmdList['pull image'] = 'sudo docker pull sande2jm/' + self.serviceName + ':' + self.version
		self.cmdList['stop container'] = 'sudo docker rm -f $(sudo docker ps -a -q)'								

	def runCommand(self, cmd):
		cmd = cmd.split(' ')     
		call(cmd)

	def connectToInstances(self):
		for x in self.instances:
			while not self.connect_ssh(x, self.cmdList['check docker']):
				time.sleep(.3)

	def runDockerImage(self):
		for x in self.instances:
			self.connect_ssh(x, self.cmdList['pull image'])
			self.connect_ssh(x, self.cmdList['run image'])
			
	def stopDockerImage(self):
		for x in self.instances:
			self.connect_ssh(x, self.cmdList['stop container'])			
			

	def connect_ssh(self,instance, cmd):
		try:
			key = paramiko.RSAKey.from_private_key_file("../DLNAkey.pem")
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(hostname=instance.public_dns_name, username="ubuntu", pkey=key)
			stdin, stdout, stderr = client.exec_command(cmd)
			line = stderr.readline()
			while line:
				print(line)
				line = stderr.readline()
			print("Available ")
			ret = True
		except Exception as e:
			print('Unavailable, ', e)
			ret = False
		return ret

if __name__ == '__main__':
	e = EC2Manager()
	e.gatherInstances()
	e.connectToInstances()
	e.updatePublicDNS()
	e.getVersion()
	e.stopDockerImage()
	e.runDockerImage()
	print(e.version)