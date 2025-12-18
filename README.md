# aws-lambda-function

Project: Lambda to stop EC2 instances when an AWS Budget alarm triggers.

Directory layout:

- lambda-stop-ec2-on-budget/
	- scripts/stop_ec2_on_budget.py  # main Lambda handler and helpers
	- policy/awsbudgetsns.json       # SNS topic policy (replace placeholders)
	- policy/stopec2instance.json    # IAM policy for the Lambda role

Usage

- Deploy `stop_ec2_on_budget.lambda_handler` as a Lambda function.
- Give the function an execution role with the policy in `policy/stopec2instance.json`.
- Create an SNS topic for AWS Budgets, update `policy/awsbudgetsns.json` with your account/region/topic, and attach it to the topic.
- Subscribe the Lambda to the SNS topic (Lambda trigger) so budget notifications invoke it.

Testing locally

Install boto3 and configure AWS credentials, then run:

```bash
python lambda-stop-ec2-on-budget/scripts/stop_ec2_on_budget.py
```

This runs a dry run by default when invoked locally.

Notes

- The script now enumerates regions and avoids making AWS calls at import time.
- Keep `DryRun=True` locally to avoid accidental stops; remove for real runs in Lambda.
# aws-lambda-function