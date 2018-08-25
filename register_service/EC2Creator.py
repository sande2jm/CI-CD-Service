import boto3
from subprocess import call
import yaml

class EC2Creator():
	def __init__(self):
		self.config = {}
		self.serviceName = 'register_service'
		self.repository = 'https://sande2jm@github.com/sande2jm/workflow_configuration.git'
		self.cmdList = {'get repo': 'git submodule add --force https://sande2jm@github.com/sande2jm/workflow_configuration.git', 
						'pull repo': 'git submodule update --recursive --remote',
						'delete repo': 'git rm -rf workflow_configuration',
						'push to repo': ['git submodule foreach git add * ', 
										'git submodule foreach git commit -m test',
										'git submodule foreach git push origin master']}
		self.ec2_connection = boto3.resource('ec2', 'us-east-1')
		self.config_path = 'config/' + self.serviceName + '_cloud_config.yaml'

	def getCloudConfig(self):
		with open(self.config_path, 'r') as stream:
			self.config = yaml.load(stream)
		cmds = "".join(list(map(lambda x: str(x) + "\n", self.config['init'])))
		self.config['init'] = cmds


	def runCommand(self, cmd):
		cmd = cmd.split(' ')     
		call(cmd)

	def createInstance(self):
		response = self.ec2_connection.create_instances(
		    TagSpecifications = [{'ResourceType': 'instance','Tags': [{'Key': 'Name','Value': self.config['name']}]}],
		    Placement = {'AvailabilityZone': self.config['region']},
		    ImageId = self.config['ami'], 
		    InstanceType = self.config['type'],
		    MinCount = 1,
		    MaxCount = 1,
		    Monitoring = {'Enabled':False},
		    KeyName = self.config['key'],
		    SecurityGroupIds = self.config['securityId'],
		    UserData = self.config['init'],
		    IamInstanceProfile = {'Arn': self.config['role']},
		)
	def describe(self):
		print("Virtual Machine Created")
		print('name: ', self.config['name'])
		print('type: ', self.config['type'])
		print('role: ', self.config['role'])
		print()

if __name__ == '__main__':
	e = EC2Creator()
	e.getCloudConfig()
	e.createInstance()
	e.describe()
	print(e.config)

