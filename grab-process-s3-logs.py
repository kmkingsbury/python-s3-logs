import boto3
import botocore
from pathlib import Path
from os import listdir
from os.path import isfile, join
import glob
import sys, os 
import datetime

prefix = "Log_Prefix"
bucket = "my-bucket"


# Create a client
client = boto3.client('s3', region_name='us-east-1')

s3 = boto3.resource('s3')

# Create a reusable Paginator
paginator = client.get_paginator('list_objects')

# Create a PageIterator from the Paginator
page_iterator = paginator.paginate(Bucket=bucket)

# Download all files to src, skip if have it already
for page in page_iterator:
    for file in page['Contents']:
        print("key: " + str(file['Key']))

        # test if exists:

        my_file = Path("src/" + file['Key'])
        if not my_file.is_file():
            try:
                s3.Bucket(bucket).download_file(file['Key'], "src/" + file['Key'])
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise

# Iterate and combine into a dated file.
# get list of files
# skip today
# skip already processed

now = datetime.datetime.now()
today =  "%04d-%02d-%02d" % (now.year, now.month, now.day)
print("Today:" + today)
#sys.exit()
completedlogs = glob.glob("src/*.log")
#print("CL:" + str(completedlogs))

onlyfiles = [f for f in listdir("src/") if isfile(join("src/", f))]
onlyfiles.sort()
for obj in onlyfiles:
    if not obj.endswith(".log"):
        # Log_File_2020-07-12-18-28-08-1F583BAA22302BFF
        strdate = obj.lstrip(prefix)
        #print("date:" + strdate)
        strdate = "-".join(strdate.split('-')[0:3])
        #print("filename:" + strdate)

        # Skip Today and If strdate.log exists in completed logs, then we already processed these files.
        if strdate != today and not "src/" + strdate + ".log" in completedlogs:
            os.system("cat src/"+obj + " >> src/" + strdate + ".log" )
            print("filename:" + strdate)
