##week08
  
Week 8 was all about serverless image processing. 
   
Guest -  
Kristi Perreault, an AWS serverless hero. Kristi is a Principal Software Engineer at Liberty Mutual Insurance, focusing on serverless enablement and development for the last several years. 
She said Liberty Mutual has gone all in on the AWS CDK space.
  
CDK, or Cloud Development Kit, is an IaaC tool. Where in CloudFormation you would define your infrastructure in .json or .yml, in CDK you could define your infrastructure in TypeScript, JavaScript, Python, Java, C#/. Net, or Go. 
There’s a couple different versions of CDK, we will be using version 2. If we’ve never used CDK before, that’s fine, you don’t need to know about version 1, there were import and packaging changes. Version 2 is easier to use.
  
[AWS CDK doc](https://docs.aws.amazon.com/cdk/api/v2/)
  
  
![Visual Representation](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/71173401-e998-4b05-b0e7-3233b37eec32)

  
We will be creating resources for an S3 bucket, a Lambda function that will process our image, interactions with an API, and a webhook.

In our workspace, we create a new directory named thumbing-serverless-cdk through the CLI. We then cd into the directory.

```
mkdir thumbing-serverless-cdk

cd thumbing-serverless-cdk
```
  
Installed aws-cdk in our directory.The -g means globally, which will allow CDK to be referenced wherever we are in our directories.

```
npm install aws-cdk -g
```
  
  
  
Running cdk init app --language typescript initializes a new AWS CDK (Cloud Development Kit) app project with TypeScript as the programming language.
This command sets up a basic structure for building infrastructure as code using the AWS CDK framework, allowing developers to define cloud resources using TypeScript code.
```
cdk init app --language typescript
```
 
![Installation of cdk and intialising app project](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/521f7d95-1809-4ec7-88af-f0acbdbe41d7)
  
The package.json and the package-lock.json file are what house our dependencies. 
Here, we look at our package.json file:

```
{
  "name": "thumbing-serverless-cdk",
  "version": "0.1.0",
  "bin": {
    "thumbing-serverless-cdk": "bin/thumbing-serverless-cdk.js"
  },
  "scripts": {
    "build": "tsc",
    "watch": "tsc -w",
    "test": "jest",
    "cdk": "cdk"
  },
  "devDependencies": {
    "@types/jest": "^29.4.0",
    "@types/node": "18.14.6",
    "aws-cdk": "2.73.0",
    "jest": "^29.5.0",
    "ts-jest": "^29.0.5",
    "ts-node": "^10.9.1",
    "typescript": "~4.9.5"
  },
  "dependencies": {
    "aws-cdk-lib": "2.73.0",
    "constructs": "^10.0.0",
    "dotenv": "^16.0.3",
    "sharp": "^0.32.0",
    "source-map-support": "^0.5.21"
  }
}
```


By default, we’re given the latest version of aws-cdk out of the box. 
These are updated relatively quickly and frequently.
In the lib directory we get thumbing-serverless-cdk-stack.ts file. 
This is where we define all of our infrastructure. CDK prefills the file with a sample resource so you as an engineer can see how it works.
  

We begin importing s3 for our S3 bucket we're going to need.
```
import * as s3 from 'aws-cdk-lib/aws-s3';
```

  
We need to define our bucket with a bucket name.

```
const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;
```
  
We create a new function named createBucket. When we create a bucket, we're taking in our bucketName as a string.
```
createBucket(bucketName: string){
  const bucket = new s3.Bucket(this, 'ThumbingBucket');
}
```
  
The id we're setting is __ThumbingBucket__ . We want to give the function a few more properties or props to make sure that it interacts with our other objects and has a name for us to identify it. 
We do this with {} brackets. One of the properties we add is a removalPolicy, which is an IAM policy.


In statically-typed languages, including Go, TypeScript, Java, C#, Swift, and others, you typically need to explicitly declare the return type of a function. 
This explicit declaration helps ensure type safety and allows the compiler to catch type-related errors during compilation.

In the context of the AWS CDK (Cloud Development Kit) for TypeScript, s3.IBucket is a type definition representing an interface or class that describes an S3 bucket. 
When you see s3.IBucket as a return definition in TypeScript, it means that the function returns an object that implements the IBucket interface, which represents an Amazon S3 bucket.

```
createBucket(bucketName: string): s3.IBucket {
  const bucket = new s3.Bucket(this, 'ThumbingBucket', {
    bucketName: bucketName,
    removalPolicy: cdk.RemovalPolicy.DESTROY
    });
    return bucket;
}
```
  
General overview of the typical properties and methods you might find in an s3.IBucket interface:

```
interface IBucket {
    /**
     * The ARN of the bucket.
     */
    readonly bucketArn: string;

    /**
     * The name of the bucket.
     */
    readonly bucketName: string;

    /**
     * The URL of the bucket.
     */
    readonly bucketUrl: string;

    /**
     * Adds a statement to the bucket's bucket policy.
     */
    addToResourcePolicy(statement: PolicyStatement): boolean;

    /**
     * Adds a statement to the bucket's lifecycle policy.
     */
    addLifecycleRule(rule: LifecycleRule): void;

    /**
     * Adds a statement to the bucket's notifications configuration.
     */
    addNotification(notification: BucketNotification): void;

    /**
     * Adds a metrics configuration for the bucket's logging configuration.
     */
    addMetric(metric: BucketMetrics): void;

    // Other properties and methods...
}

```



Back in our definition, we want to call this and make a bucket from our main class. We define another constant.
```
// Previously added
const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;

// New bucket we just added
const bucket = this.createBucket(bucketName);
```


  
The __cdk synth__ command generates a CloudFormation template from your CDK code, allowing you to see the complete AWS infrastructure that will be created or modified by your CDK app. This template can be used to inspect the resources, review the dependencies between resources, and even manually create or modify the stack outside of the CDK, if needed.
  
![s3 bucket cdk synth](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/7f71472c-2cf1-4f90-b2ac-4229503739c5)
  
![Screenshot 2024-02-11 125030](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/9ec7dc4c-504c-46ee-a628-5ab5ba69437c)
  
Although the template is output in our terminal as .yml, within our thumbing-serverless-cdk directory we created, there's a new folder named cdk.out. Within that folder, if we access the ThumbingServerlessCdkStack.template.json file, it displays our CloudFormation template in .json.

  

Bootstraping
[Bootstraping doc](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html)

>Preparation: Bootstrapping prepares your AWS environment for deploying AWS CDK applications. It creates the necessary infrastructure resources that AWS CDK relies on, such as an S3 bucket for storing assets and an IAM role for executing CloudFormation stacks.
>Dependency: AWS CDK requires certain resources to be available in your AWS account before you can deploy your application. For example, it needs an S3 bucket to store assets like Lambda code or Docker images and an IAM role with appropriate permissions to deploy CloudFormation stacks.
>Convenience: Bootstrapping before deployment streamlines the deployment process. Once the AWS environment is bootstrapped, you can deploy your AWS CDK applications without worrying about setting up infrastructure resources manually.
  
  
We only have to bootstrap once per AWS account, or per region, if you’re wanting multiple regions. Moving to our terminal, we perform a bootstrap.
  
  
```
cdk bootstrap "aws://<AWSACCOUNTNUMBER>/<AWSREGION>
```
![Screenshot 2024-02-11 130844](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/3cf8bb6d-0bbe-4f2e-be38-73cb312c65bb)
  
  
> Deployment involves synthesizing the infrastructure code into a CloudFormation template, while provisioning involves creating and configuring the actual AWS resources based on that template.
  
  
![cdkToolkit](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/8f098c96-c140-4a58-8433-252b600749e2)

```
cdk deploy
```

![cloudformation stack after deploy](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/60b23a39-f7f5-4e2b-93f4-a6d6a0f2b4a3)


