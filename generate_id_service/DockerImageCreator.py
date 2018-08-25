from subprocess import call

class DockerImageCreator():
	def __init__(self):
		self.directory_path = "?"
		self.serviceName = 'generate_id_service'
		self.repository = 'https://sande2jm@github.com/sande2jm/workflow_configuration.git'
		self.cmdList = {'build image': None,
						'push image': None }

		self.version_filepath = 'config/generate_id_service_version.txt'
		self.version = None

	def getVersion(self):
		with open(self.version_filepath, 'r+') as f:
			self.version = f.readline().rstrip()
		self.cmdList['build image'] = ['docker build -t ' + self.serviceName + ' WebFront/.', 
										'docker tag ' + self.serviceName + ' sande2jm/' + self.serviceName + ':' + self.version]
		self.cmdList['push image'] = 'docker push sande2jm/' + self.serviceName + ':' + self.version								

	def updateVersion(self):		
		with open(self.version_filepath, 'w') as f:
			f.write(str(round(float(self.version)+ 0.1,1)))

	def runCommand(self, cmd):
		cmd = cmd.split(' ')     
		call(cmd)

	def createImage(self):
		for cmd in self.cmdList['build image']:
			self.runCommand(cmd)

	def pushToDockerHub(self):
		self.runCommand(self.cmdList['push image'])

if __name__ == '__main__':
	d = DockerImageCreator()
	d.getVersion()
	d.updateVersion()
	d.createImage()
	d.pushToDockerHub()
	print(d.version, d.serviceName)



