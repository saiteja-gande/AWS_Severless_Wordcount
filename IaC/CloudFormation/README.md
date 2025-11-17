# CloudFormation Deployment Guide

This folder contains the CloudFormation template used to deploy the fully automated, event‑driven Word Count Pipeline on AWS.

## 📌 About This CloudFormation Version

Most details about the project architecture, pipeline behavior, and service flow are already explained in the main folder **README.md**.  
This CloudFormation-specific README focuses only on:

- The **additional Lambda function** required to configure S3 bucket notifications  
- How to **deploy and use** this CloudFormation stack  

---

## 🆕 Additional Lambda Function: S3 Notification Configurator

In this CloudFormation template, an extra Lambda function named:

### **`S3NotificationConfigurator`**

is included to automatically attach S3 → Lambda event notifications.

### Why is this needed?

CloudFormation is encountering **circular dependency errors** when  **attaching S3 event notifications to a Lambda function in the same stack**.

To solve this, CloudFormation uses:

1. A helper Lambda (`S3NotificationConfigurator`)
2. A custom resource (`Custom::S3Notification`)

This helper Lambda is invoked automatically during stack creation and configures the S3 notification rule:

```
When a file is uploaded → TriggerStepFunction Lambda is invoked
```

This ensures:

- Full automation  
- No manual setup in the S3 console  
- No circular dependency issues  
- Clean removal on stack deletion  

Note: This Lambda has **no relation** to the main pipeline logic. It only runs once during stack creation.
---

## 🚀 How to Deploy This Stack

### 1️⃣ Upload the CloudFormation Template

In AWS Console:

1. Go to **CloudFormation**
2. Click **Create stack → With new resources (standard)**
3. Choose **Choose an existing template** and **upload a template file**
4. Edit(replace email address in line 29) and Upload the file:  
   `serverless-wordcount.yaml`
5. Click **Next**

---

### 2️⃣ Provide Stack Name

Example:

```
WordCountPipelineStack
```

No parameters are required.

---

### 3️⃣ Deploy the Stack

Click **Next → Next → Create stack**

CloudFormation will:

- Create S3 bucket  
- Create SNS topic  
- Create DynamoDB table  
- Create IAM roles  
- Deploy all Lambdas  
- Deploy Step Functions workflow  
- Run the custom notification Lambda  
- Configure S3 → Lambda triggering  

---

## 🔍 Confirming Deployment

After stack creation:

### ✓ Check S3 Notification
Go to:

**S3 →  Bucket → Properties → Event notifications**

You should see:

```
Event: s3:ObjectCreated:*
Destination: TriggerStepFunction Lambda
```

### ✓ Check Step Function
Go to:

**Step Functions → State Machines → WordCountStateMachine**

You should see two steps:

1. ProcessFile  
2. StoreResults  

---

## 📂 How to Use the Pipeline

After deployment, upload any `.txt` file to the S3 bucket:

```
aws s3 cp myfile.txt s3://wordcount-bucket-<account-id>/
```

The pipeline will:

1. Trigger the Step Function  
2. Count all words using Lambda  
3. Email top words through SNS  
4. Store results in DynamoDB  

Everything runs automatically.

---

## 🧼 Clean Up

To delete all resources:

Go to **CloudFormation → Stacks → Delete**

The custom resource will:

- Remove S3 notifications  
- Clean up additional settings  

Then CloudFormation will delete:

- Lambdas  
- IAM roles  
- SNS  
- DynamoDB  
- Step Function  
- S3 bucket (if empty)

---

## ✅ Summary

This CloudFormation folder includes everything needed to deploy the word count pipeline automatically.  
The only major difference from the general project is:

> **This version includes a special Lambda function to configure S3 notifications and avoid circular dependencies.**

Once deployed, pipeline becomes fully automated and production-ready.
