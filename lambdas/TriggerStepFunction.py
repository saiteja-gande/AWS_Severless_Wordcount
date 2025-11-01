"""
Lambda Trigger — S3 → Step Function Starter
-------------------------------------------
This Lambda is triggered by an S3 event notification whenever
a new file (e.g., .txt) is uploaded to the bucket.

It starts the Step Function execution automatically.
"""

import boto3
import json
import os

sf = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print(json.dumps(event))  # log the S3 event for debugging
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Start the Step Function execution
        response = sf.start_execution(
            stateMachineArn=os.environ['stateMachineArn'],
            input=json.dumps({'bucket': bucket, 'key': key})
        )
        print(f"Started Step Function: {response['executionArn']}")
    
    return {"status": "started"}
