# xp-suspense-with-aws-dynamo

A proof of concept trial with DynamoDB and AWS Lambda

## Running

These functions are designed to run with the excellent Python [pipenv](https://pipenv.readthedocs.io/en/latest/) management tool. See their documentation to install and setup pre-requisites.

Dependencies are defined in the [Pipfile](./Pipfile) and deterministic builds are setup by the [Pipfile.lock](./Pipfile.lock).

To setup your environment execute `pipenv sync --dev` and recieve the deterministic build.

## Provisioning

### DynamoDB Table

Use the CFT

Run `aws cloudformation create-stack --stack-name DemoDynamoTable --template-body=file:///Users/[userName]/Development/xps/Dynamo/dynamo.yml --region us-east-1`

This creates the dynamo table and provisions low write and read for proof of concept work

### IAM

The Lambda function will need an IAM role. I've included an [example policy](./dynamo-role.json) for the role that restricts it to the table created and provides telemetry permissions.

### Lambda

To compile the lambda package, run [`./build.sh`](./build.sh). This will use the pipenv and package all of the dependencies for AWS Lambda.

After packaging, the file will need to be uploaded to Lambda via the console or S3.

The lambda needs to be configured with the IAM role established with the policy and X-Ray.

## Live Testing

1. Run `pipenv shell` to access your python virtual environment
1. Run `python dynamo_controller.py` to set the value in the DynamoDB table
1. Log into the AWS console
1. Navigate to Lambda
1. Navigate to your function
1. Click the test button and accept the default test event

Now you can review your results within CloudWatch and X-Ray.

### Findings

By increasing the Lambda memory allocation to 640MB I found that I was able to drop the cold start time from 200ms to 100ms. Further memory increases yield no discernable benefit.

The function routinely executes in less than 100ms with an average closer to 50ms and fastest times running in single digit milliseconds.

When paired with database connections, a VPC layer, proxies or processing other than the AWS API Gateway response methods, there will be changes, but this seems to be a sound solution to sharing elements between functions.

## Release Notes

- 1.0.0
  - Build Script
  - Lambda Role Policy
  - Lambda Function implementing DynamoDB checks
  - DynamoDB CloudFormation Template to Provision Table
  - Pipenv setup
