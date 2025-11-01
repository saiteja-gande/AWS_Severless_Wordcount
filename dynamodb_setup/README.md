
---

## 📘 `dynamodb_setup/README.md`


# 🗃️ Creating DynamoDB Table for Word Count Results

This guide explains how to create and configure the **DynamoDB table** that stores word count results from your AWS Lambda workflow.

---

## 🧠 Overview

The `StoreWordCountResults` Lambda (Lambda #2) writes processed results from each file upload into this DynamoDB table.

Each record includes:
- Unique ID (integer timestamp)
- File name
- Total word count
- Top 10 frequent words
- Processed date and timestamp

---

## ⚙️ Step 1 — Create DynamoDB Table

1. Open **AWS Console → DynamoDB → Tables → Create table**
2. Enter Table name: `WordCountResults` and Partition key: `id` (Number)
3. Use the default settings for the rest:
   - No sort key
   - Default settings for capacity mode, encryption, etc.
4. Click **Create table**

✅ You now have a DynamoDB table to store results.

---

## ⚙️ Step 2 — (Optional) Add Additional Attributes

You don’t need to pre-define extra attributes, but your Lambda will store the following fields automatically:

| Attribute | Type | Description |
|------------|------|-------------|
| `id` | Number | Unique identifier (timestamp) |
| `file_name` | String | Name/key of the uploaded file |
| `total_words` | Number | Total number of words |
| `top_words` | Map | Dictionary of top 10 frequent words |
| `processed_at` | String | ISO UTC timestamp |
| `processed_date` | String | Date for querying |

Example record:

```json
{
  "id": 1730468350,
  "file_name": "uploads/story.txt",
  "total_words": 4823,
  "top_words": { "the": 312, "and": 243, "to": 195 },
  "processed_at": "2025-11-01T12:34:56Z",
  "processed_date": "2025-11-01"
}
