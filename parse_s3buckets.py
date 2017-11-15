#v1.0
#10/27/2017
#parse out the S3 bucket names for buckets that do not have access logging enabled
#requires the Scout2 config.js file. EG, after running scout2 on [client] it will generate a file: scout2-report\inc-awsconfig\aws_config-[client].js
#usage: python parse_s3buckets.py aws_config-[client].js

import sys
import simplejson

print "Parsing JSON file and saving output to 'outfile.csv'\n"

#open json file from scout-2
with open(sys.argv[1]) as data:
	contents = data.read()
	contents = contents.replace('\n','') #remove line breaks
	contents = contents.replace('aws_info =', '') #remove the text at the beginnging of the json file
json = simplejson.loads(contents)

#create array of S3 buckets and populate
buckets = []
for key,value in enumerate(json["services"]["s3"]["buckets"]):
	buckets.append(value)
#print buckets

#counter declarations
a = 0 #counter to enumerate through buckets

#open output file
with open('outfile.csv', 'w+') as csv:

	#write file headers
	csv.write("Bucket Name\n")
	
	#loop through the buckets
	while a < len(buckets):
		
		#write name of the bucket to output file if logging is disabled
		if json["services"]["s3"]["buckets"][buckets[a]]["logging"] == "Disabled":
			write_string = str(json["services"]["s3"]["buckets"][buckets[a]]["name"]) + "\n"
			csv.write(write_string)
			a += 1
		
		else:
			a += 1
#end
