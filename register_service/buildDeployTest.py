from DockerImageCreator import DockerImageCreator
from EC2Creator import EC2Creator
from EC2Manager import EC2Manager
from ServiceTester import ServiceTester

counter_service_image = DockerImageCreator()
counter_service_image.getVersion()
counter_service_image.updateVersion()
counter_service_image.createImage()
counter_service_image.pushToDockerHub()
print()
print('Docker Image Created Version:', counter_service_image.version)

counter_service_ec2_creator = EC2Creator()
counter_service_ec2_creator.getCloudConfig()
counter_service_ec2_creator.createInstance()
counter_service_ec2_creator.describe()

print()
print('AWS Virtual Image Created')

counter_service_ec2_manager = EC2Manager()
counter_service_ec2_manager.gatherInstances()
counter_service_ec2_manager.connectToInstances()
counter_service_ec2_manager.updatePublicDNS()
counter_service_ec2_manager.getVersion()
counter_service_ec2_manager.runDockerImage()
#print(counter_service_ec2_manager.version)

print()
print('Manager connection attempt completed')

service_tester = ServiceTester()
service_tester.getPublicDNS()
service_tester.noJsonPing('increment')
service_tester.jsonPing('getCounter')

print('Service Test Complete')



