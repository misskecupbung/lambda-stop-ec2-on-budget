
# lambda-stop-ec2-on-budget

Small AWS Lambda project that stops EC2 instances when an AWS Budget alarm (via SNS) notifies the function.

What this repo contains

- `lambda-stop-ec2-on-budget/scripts/stop_ec2_on_budget.py` — Lambda handler and helpers.
- `lambda-stop-ec2-on-budget/policy/stopec2instance.json` — IAM policy for the Lambda execution role.
- `lambda-stop-ec2-on-budget/policy/awsbudgetsns.json` — SNS topic policy template (update placeholders).

Quick overview (deploy)

1. Create an IAM role for the Lambda with the policy in `lambda-stop-ec2-on-budget/policy/stopec2instance.json` plus `AWSLambdaBasicExecutionRole` (for CloudWatch Logs).
2. Deploy the function using the handler `stop_ec2_on_budget.lambda_handler` and the role above. The function uses the `boto3` available in the AWS Lambda runtime.
3. Create an SNS topic for AWS Budgets and update `lambda-stop-ec2-on-budget/policy/awsbudgetsns.json` with your region, account id and topic name; attach the policy to the topic so Budgets can publish.
4. Subscribe the Lambda to the SNS topic (add the SNS trigger to the Lambda). Configure an AWS Budget to send notifications to that SNS topic.

Local testing

- Ensure `boto3` is installed and you have valid AWS credentials configured (e.g., via `~/.aws/credentials` or environment variables).
- Run a safe dry-run locally:

```bash
python lambda-stop-ec2-on-budget/scripts/stop_ec2_on_budget.py
```

The script prints discovered running instances and runs in dry-run mode when executed directly so you won't accidentally stop instances during local testing.

Security and safety notes

- The Lambda needs only the permissions in `policy/stopec2instance.json` — described/stop privileges limited to EC2. Minimize other permissions.
- Verify the SNS topic policy placeholders in `awsbudgetsns.json` to ensure only AWS Budgets (and your account) can publish to the topic.
- Test with a small, non-production account or with instance tags/filters to avoid stopping critical instances.

Commands

- Syntax check the Python file:

```bash
python3 -m py_compile lambda-stop-ec2-on-budget/scripts/stop_ec2_on_budget.py
```

- Run the script locally (dry run):

```bash
python lambda-stop-ec2-on-budget/scripts/stop_ec2_on_budget.py
```

If you'd like, I can:
- Commit these README changes and clean up empty folders.
- Add environment-variable support for `DRY_RUN` or instance tag filtering.