import * as cdk from 'aws-cdk-lib';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as lambda from 'aws-cdk-lib/aws-lambda'
import { Construct } from 'constructs';
import { LambdaSubscription } from 'aws-cdk-lib/aws-sns-subscriptions';
import { LambdaFunction } from 'aws-cdk-lib/aws-events-targets';

//load env vars
const dotenv = require('dotenv')
dotenv.config();

export class ThumbingServerlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;
    const functioPath: string = process.env.THUMBING_FUNCTION_PATH as string;


    const bucket = this.createBucket(bucketName)
    const lambda = this.createLambda(functioPath)
     
   
  }

  createBucket (bucketName: string): s3.IBucket {
    const bucket = new s3.Bucket(this, 'ThumbingBucket',{
      bucketName: bucketName,
      removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    return bucket;
  }

  createLambda(functionPath: string): lambda.IFunction{
    const lambdaFunction = new lambda.Function(this, 'ThumbLambda', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(functionPath)

    });
    return lambdaFunction

  }
    
}
