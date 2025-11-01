# 🧠 AWS Lambda Functions — Word Count Project

This folder contains all three Lambda functions used in the **AWS Serverless Word Count Pipeline**.

---

## 📂 Functions Overview

| File | Function | Purpose |
|------|-----------|----------|
| `wordcount_processor.py` | Lambda #1 | Reads file from S3, counts words, sends SNS report |
| `store_results_dynamodb.py` | Lambda #2 | Stores the results in DynamoDB |
| `trigger_stepfunction.py` | Trigger Lambda | Starts the Step Function when a new file is uploaded to S3 |

---

## ⚙️ Environment Variables

Each Lambda requires certain environment variables to function correctly.

### 🔹 For `WordCountProcessor.py`
| Variable | Example | Description |
|-----------|----------|-------------|
| `snsTopicArn` | `arn:aws:sns:us-east-1:123456789012:WordCountTopic` | SNS topic to send email notifications |
| `s3Bucket` | `WordCountBucker` | S3 Bucket Name where .txt files are uploaded |

---

### 🔹 For `StoreWordCountResults.py`
| Variable | Example | Description |
|-----------|----------|-------------|
| `dynamoTableName` | `WordCountResults` | DynamoDB table name to store results |

---

### 🔹 For `TriggerStepFunction.py`
| Variable | Example | Description |
|-----------|----------|-------------|
| `stateMachineArn` | `arn:aws:states:us-east-1:123456789012:stateMachine:WordCountStateMachine` | Step Function ARN to trigger |

---

## 🧰 Permissions (IAM Role)

All Lambdas use the same **execution role** (`LambdaExecutionRole-WordCount`), which has:

- `AmazonS3FullAccess`
- `AmazonSNSFullAccess`
- `AWSLambdaBasicExecutionRole`
- `CloudWatchFullAccess`
- Inline policy for DynamoDB + Step Function access
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "DynamoDBAccess",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:UpdateItem",
                "dynamodb:GetItem",
                "dynamodb:DescribeTable"
            ],
            "Resource": "*"
        },
        {
            "Sid": "StepFunctionStartExecution",
            "Effect": "Allow",
            "Action": "states:StartExecution",
            "Resource": "*"
        }
    ]
}

```


To follow the **Principle of Least Privilege**, use this **minimal inline policy** instead of multiple full-access managed policies.
### 🔹 Inline Policy (Recommended)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificS3",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::YOUR_BUCKET_NAME",
        "arn:aws:s3:::YOUR_BUCKET_NAME/*"
      ]
    },
    {
      "Sid": "AllowSNSPublish",
      "Effect": "Allow",
      "Action": ["sns:Publish"],
      "Resource": "arn:aws:sns:YOUR_REGION:YOUR_ACCOUNT_ID:WordCountTopic"
    },
    {
      "Sid": "AllowDynamoDBPut",
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:DescribeTable"
      ],
      "Resource": "arn:aws:dynamodb:YOUR_REGION:YOUR_ACCOUNT_ID:table/WordCountResults"
    },
    {
      "Sid": "AllowStepFunctionStart",
      "Effect": "Allow",
      "Action": ["states:StartExecution"],
      "Resource": "arn:aws:states:YOUR_REGION:YOUR_ACCOUNT_ID:stateMachine:WordCountStateMachine"
    },
    {
      "Sid": "AllowCloudWatchLogs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```
---

## 🚀 How to Deploy

### AWS Console (manual)
1. Go to **AWS Lambda → Create function**
2. Choose “Author from scratch”
3. Enter function name (e.g., `WordCountProcessor`) and select Python 3.12 runtime
4. Choose or create the existing role `LambdaExecutionRole-WordCount`
5. create the function
6. In the function code section: paste the code from the relevant file
7. Add environment variables (listed above)
8. Save
9. Repeat for other Lambda functions