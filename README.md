# python-s3-logs

Assumes AWS API Account setup in ~/.aws/credentials or Environment variables with access to read the S3 Bucket and files/objects.

Two dirs:  
* `src` is where the raw log files are downloaded to.  
* `processed` is where the combined log file is created and kept.  


The Log Prefix and Bucket name variables are stored as Environment variables. This way using something like a Jenkins Job I can use the same code to pull from multiple buckets/logs/accounts just by setting the environment vars.

    export LOG_PREFIX = "" #no prefix
    export LOG_PREFIX = "My_Log_Prefix_" 
    export MY_BUCKET = "my-bucket-name"
    export AWS_ACCESS_KEY_ID=Axxxx
    export AWS_SECRET_ACCESS_KEY=yyyy
    export AWS_DEFAULT_REGION=us-east-1
