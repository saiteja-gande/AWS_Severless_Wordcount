# 🪣 Creating S3 Bucket and Setting Up Trigger for Lambda

This guide explains how to create an **Amazon S3 bucket** to store uploaded `.txt` files and configure it to automatically trigger the **Step Function workflow** through the `TriggerStepFunction` Lambda.

---

## 🧠 Overview

When a `.txt` file is uploaded to S3:
1. The S3 event triggers `TriggerStepFunction` Lambda.
2. The Lambda starts the Step Function (`WordCountStateMachine`).
3. The Step Function processes the file and stores results in DynamoDB.

---

## ⚙️ Step 1 — Create the S3 Bucket

1. Open the **AWS Management Console** → Navigate to **S3 → Create bucket**  
2. Enter a **unique bucket name** (e.g., `wordcount-project-bucket-yourname`)
3. Choose your region (same region as your Lambdas and Step Function)
4. Keep defaults:
   - Object Ownership: *ACLs disabled*
   - Block Public Access: *All checked*
   - Versioning: Optional
   - Encryption: *Enable (AES-256)*
5. Click **Create bucket**

✅ You now have an S3 bucket ready for uploads.

---

## ⚙️ Step 2 — Enable Event Notifications (Trigger Lambda)

1. Go to your **S3 bucket → Properties tab**
2. Scroll to **Event notifications → Create event notification**
3. Configure the event:

| Setting | Value |
|----------|--------|
| **Event name** | `TriggerStepFunctionEvent` |
| **Prefix (optional)** | `uploads/` (if you store files in a folder) |
| **Suffix** | `.txt` |
| **Event types** | `All object create events` |
| **Destination** | Lambda Function |
| **Lambda function** | Select `TriggerStepFunction` |

4. Click **Save changes**

---

S3 bucket is now set up to trigger the Step Function workflow when a `.txt` file is uploaded.