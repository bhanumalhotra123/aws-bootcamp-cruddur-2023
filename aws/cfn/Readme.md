## Architecture Guide

Before you run any templates, be sure to create an S3 bucket to contain all of our artiacts for CloudFormation.

```
aws mk s3://cfn-artifacts
export CFN_BUCKET="cfn-artifacts-1"
gp env CFN_BUCKET="cfn-artifacts-1"


> Remember bucket names are unique. So you may need to adjust the provided code example