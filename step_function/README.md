# ⚙️ AWS Step Functions — Word Count Pipeline

This folder contains the **Step Function definition** and documentation for the
**AWS Serverless Word Count Project**.

The Step Function coordinates two Lambda functions:
1. `WordCountProcessor` — Reads file, counts words, sends SNS notification  
2. `StoreWordCountResults` — Saves results in DynamoDB

---

## 🧠 Creating the Step Function in AWS Console

1. AWS Console → Step Functions → Create state machine
2. Choose create from blank, enter state machine name: `WordCountStateMachine` and choose standard type as state machine type.
3. In code, paste the content of `step_function/word_count_state_machine.json` file.
4. In config, in execution role, choose "Create new role with basic Step Functions permissions". or If you already created this manually, select your existing role instead.
5. Create state machine.

---

## 🧪 Testing the Step Function

1. Click Start execution
2. Use this sample JSON as input:
```json
{
  "bucket": "your-s3-bucket-name",
  "key": "path/to/your/textfile.txt"
}
```
3. Click Start execution and ensure the execution completes successfully.

