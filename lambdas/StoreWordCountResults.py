"""
Lambda #2 — Store Word Count Results
------------------------------------
This Lambda function is invoked by the Step Function after
the word count process completes.

It stores results (filename, total words, top words, timestamp)
in a DynamoDB table named 'WordCountResults'.
"""

import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table_name = os.environ['dynamoTableName']
    table = dynamodb.Table(table_name)

    # The Step Function passes this payload from Lambda #1
    record_id = event['id']
    file_name = event['file_name']
    total_words = event['total_words']
    top_words = event['top_words']
    processed_at = event['processed_at']
    processed_date = event['processed_date']

    # Insert into DynamoDB
    table.put_item(
        Item={
            'id': record_id,
            'file_name': file_name,
            'total_words': total_words,
            'top_words': top_words,
            'processed_at': processed_at,
            'processed_date': processed_date
        }
    )

    print(f"Successfully stored record for {file_name} (ID: {record_id})")

    return {
        'status': 'success',
        'message': f"Stored results for {file_name}",
        'id': record_id
    }
