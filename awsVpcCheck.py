#v1.0
#10/27/2017
#parse out the VPC subnets that do not have VPC flow logging enabled
#requires the Scout2 config.js file. EG, after running scout2 on [client] it will generate a file: scout2-report\inc-awsconfig\aws_config-[client].js
#usage: python parse_vpcflowlogs.py aws_config-[client].js

import sys
import simplejson
import re

print "Parsing JSON file and saving output to 'outfile.csv'\n"

#open json file from scout-2
with open(sys.argv[1]) as data:
	contents = data.read()
	contents = contents.replace('\n','') #remove line breaks
	contents = contents.replace('aws_info =', '') #remove the text at the beginnging of the json file
json = simplejson.loads(contents)

#commented out code can be used for testing 
#for x,y in enumerate(json["services"]["vpc"]["regions"]["ap-northeast-2"]["vpcs"]["vpc-0735d36e"]["subnets"]):
#	print y
	
#create array of regions and populate
regions = []
for key,value in enumerate(json["services"]["vpc"]["regions"]):
	regions.append(value)
#print regions

#counter declarations
a = 0 #counter to enumerate through regions
b = 0 #counter to enumerate through vpcs 
c = 0 #counter to enumerate through subnets

#open output file
with open('outfile.csv', 'w+') as csv:
	
	#write file headers
	csv.write("Region,VPC ID,Subnet\n")
	
	while a < len(regions):
		
		b = 0 #reset vpc counter
		
		#create array of VPCs and populate
		vpcs = []
		for key,value in enumerate(json["services"]["vpc"]["regions"][regions[a]]["vpcs"]):
			vpcs.append(value)
		#print vpcs
		
		#loop through the vpcs
		while b < len(vpcs):
			c = 0 #reset subnet counter for each vpc
			
			#create array for security groups in vpc and populate
			subnets = []
			for k,v in enumerate(json["services"]["vpc"]["regions"][regions[a]]["vpcs"][vpcs[b]]["subnets"]):
				subnets.append(v)
			
			#for each vpc, loop through subnets
			while c < len(subnets):
				
				#if there are flow logs, do nothing. Otherwise, write subnet to output file
				if json["services"]["vpc"]["regions"][regions[a]]["vpcs"][vpcs[b]]["subnets"][subnets[c]]["flow_logs"]:
					c += 1
				
				else:
					write_string = str(regions[a] + "," + vpcs[b]) + "," + str(subnets[c] + "\n")
					csv.write(write_string)
					c +=1
			b += 1
		a += 1
#end
