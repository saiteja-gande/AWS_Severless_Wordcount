# 📢 Creating SNS Topic for Email Notifications

This guide explains how to create and configure an **Amazon Simple Notification Service (SNS)** topic that sends email notifications containing word count summaries after each file is processed.

---

## 🧠 Overview

The **`WordCountProcessor` Lambda** (Lambda #1) sends an SNS message after processing each `.txt` file.  
SNS then emails the word count summary to the subscribed recipients.

---

## ⚙️ Step 1 — Create an SNS Topic

1. Open the **AWS Console → SNS → Topics → Create topic**
2. Choose:
   - **Type:** `Standard`
   - **Name:** `WordCountTopic`
3. Click **Create topic**

✅ You’ve now created a topic to handle notifications.

---

## ⚙️ Step 2 — Create an Email Subscription

1. Inside your new topic, go to **Subscriptions → Create subscription**
2. Configure:
   - **Protocol:** `Email`
   - **Endpoint:** your email address
3. Click **Create subscription**

Then check your email inbox for a message from AWS titled  
**“AWS Notification - Subscription Confirmation”**  
Click **Confirm subscription** in that email.  
Once confirmed, the subscription status will change to **Confirmed** in the console.

---

## ⚙️ Step 3 — Add Environment Variable in Lambda

Go to your **`WordCountProcessor`** Lambda function →  
**Configuration → Environment variables → Edit**, and add:

| Key | Value |
|-----|--------|
| `snsTopicArn` | `arn:aws:sns:YOUR_REGION:YOUR_ACCOUNT_ID:WordCountTopic` |

> Replace `YOUR_REGION` and `YOUR_ACCOUNT_ID` with your values.

This lets the Lambda know which SNS topic to publish to.

