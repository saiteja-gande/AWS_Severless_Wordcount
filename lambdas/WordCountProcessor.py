"""
Lambda #1 — Word Count Processor
--------------------------------
This Lambda function is invoked by the Step Function.
It:
  - Downloads the uploaded text file from S3
  - Counts total and top words
  - Sends an SNS email with the results
  - Returns data to the Step Function for the next step
"""

import boto3
import os
import json
import uuid
from datetime import datetime

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Retrieve event data from Step Function input
    bucket = event['bucket']
    key = event['key']

    download_path = f"/tmp/{os.path.basename(key)}"
    s3.download_file(bucket, key, download_path)

    # Read file and count words
    word_count = {}
    with open(download_path, 'r') as file:
        for line in file:
            words = line.split()
            for word in words:
                word = word.lower().strip('.,!?;:"\'')
                if word:
                    word_count[word] = word_count.get(word, 0) + 1

    total_words = sum(word_count.values())
    top_words = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10])

    # Create a numeric ID (you chose integer)
    record_id = int(datetime.utcnow().timestamp())  # e.g., 1730468350

    # Prepare message for SNS
    message = (
        f"File processed: {key}\n"
        f"Total word count: {total_words}\n\n"
        "Top 10 words:\n"
    )
    for w, c in top_words.items():
        message += f"  {w}: {c}\n"

    sns.publish(
        TopicArn=os.environ['snsTopicArn'],
        Subject=f"Word Count Report: {os.path.basename(key)}",
        Message=message
    )

    # Pass result to next Lambda via Step Function output
    return {
        'id': record_id,
        'file_name': key,
        'total_words': total_words,
        'top_words': top_words,
        'processed_at': datetime.utcnow().isoformat(),
        'processed_date': datetime.utcnow().date().isoformat()
    }
