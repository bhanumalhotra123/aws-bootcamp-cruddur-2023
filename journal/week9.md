# CI/CD with CodePipeline, CodeBuild, and CodeDeploy.

This week we opened the livestream with Andrew introducing Du’An Lightfoot, a Senior Cloud Networking Dev Advocate of AWS. He’s going to assist us with implementing CI/CD.

We spin up a new workspace, then do a Docker compose up to start our environment. We run our various scripts to get data to our web app, then launch it.

If we make changes to our production web application code, if we want to roll out the changes we have to build the images manually, we have to push them to AWS ECR, and then we have to trigger a deploy. We are looking to automate this process. To do this, we will use AWS CodePipeline.

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/513c709f-3156-4572-ae70-cd5c75ddd322)

We create a new pipeline.

![Screenshot 2024-03-02 002107](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/f638b24e-d1ef-4a82-b7b7-bad30a20e16e)

We name the Pipeline cruddur-backend-fargate. We're going to create a new service role for this pipeline. We allow a default S3 bucket to be created for our Artifact Store, using a Default AWS Managed Key for Encryption.
![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/bf34d7f1-ab9e-48fb-b63b-a925a4bdb634)

We click Next and now we get to add a source stage. We select Github (Version 2). We create a new connection, named cruddur. Then we click Connect to GitHub. We select Install a new App, which we're then redirected to sign in through our GitHub account and install the AWS Connector for GitHub.

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/e20925db-3776-42f4-8265-a2c650ad28ce)

We’re then prompted to select which Repositories from GitHub we would like to allow access. We select our aws-bootcamp-cruddur-2023 repository. We hit Connect, and our GitHub connection is ready for use.

Next, we add our aws-bootcamp-cruddur-2023 repository that we gave access to in the previous step and take a pause here. Andrew directs us over to GitHub, as he wants us to create a new branch from our repository. We create a new branch named prod.

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/476b8fa7-334e-4192-b787-462584e83e29)

We can now move back over to CodePipeline and continue on. We select a branch name and make it the prod branch we just created. Then, under "Change detection options", we select "Start the pipeline on source code change". This will automatically start the pipeline when a change is detected in our repository. Then for our Output artifact format, we leave the CodePipeline default and click Next.


![Screenshot 2024-03-02 002707](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/2bf263fd-5ef3-4591-b632-f53d8b07c3c1)


On the next page, we skip the build stage, as we’re wanting to do this later. We’re immediately prompted that we cannot skip the deploy stage.

AWS notes “Pipelines must have at least two stages. Your second stage must be either a build or deployment stage. Choose a provider for either the build stage or deployment stage.” 

Choose a provider for either the build stage or deployment stage.” We chose a deploy provider of Amazon ECS. We select our region, then choose our existing cluster, cruddur. For service name, we use backend-flask service from ECS. We leave the Image definition file blank for now, and click Next.

![Screenshot 2024-03-02 004500](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/fe56e1f7-a141-41ac-8a67-c7e34b90958f)

We review our steps, then click Create Pipeline.

The pipeline is successfully created.

![Screenshot 2024-03-02 191217](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/f383c704-b35d-4343-abb6-03b96862c54f)

However, the Deploy fails, because we have not configured it yet.

![Screenshot 2024-03-02 193106](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/1a6b8639-29c4-4d59-82fb-801ca529d31d)

The Deploy is expecting a file named imagedefinitions.json. We will need to make sure it's placed in our pipeline's S3 artifact bucket. Andrew then says we will need to add a build step to build out our image. We select Edit, then Add stage between Source and Deploy. We name the stage, bake-image.

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/4ea61b7c-04c2-465f-8f76-1a70b0efd2f4)

We add an action group to bake-image. We name the Action build, the Action provider AWS CodeBuild. We select our region, then select SourceArtifact as our Input artifacts. In the next step, we need to provide a Project name, but we don't have a Build project created yet. 

Instead of select Create Project and using the tiny window AWS provides, we open a new AWS console tab, then go to CodeBuild.

From there, we create a Build Project. We name the project cruddur-backend-flask-bake-image and enable the build badge.
![Screenshot 2024-02-27 034626](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/2b4e016e-f4d4-4d7f-9b3d-a005818f6432)



We select our source provider as GitHub, then again walk through the steps to connect our repository from GitHub. After it’s connected, we select our aws-bootcamp-cruddur-2023 repository. 

Under Source version, we enter the name of the branch we want to use, prod. We leave the additional configuration alone, scrolling down to the Primary source webhook events. We check the box for "Rebuild every time a code change is pushed to this repository", using Single build as the Build Type.

Under Event type, we add PUSH and PULL_REQUEST_MERGED as our events to trigger a new build.
![Screenshot 2024-02-27 035206](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/bccdd501-793d-4787-a2c5-0a2e25a880b1)


Under Environment, we selected Managed Image, using Amazon Linux 2 as the operating system.

We select a Standard runtime, the latest image, Linux environment type.
![Screenshot 2024-02-27 035338](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/92c951a6-426e-4c96-b31c-cf11ffe4273f)



We check the box for Privileged because we want to build Docker images. We’re going to also create a new service role named codebuild-cruddur-service-role.

![Screenshot 2024-02-27 035447](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/78bec5ad-7373-4b51-a56d-257ff25050bc)

We adjust the timeout of the build to 20 minutes, as we don’t want to wait too long if the build fails. We don’t use a certificate, then we select our default VPC, subnets, and security group for now. Moving onto compute, we leave it on the default option of 3 GB memory, 2 vCPUs. 

Back in our workspace, we create a new file in the root of ./backend-flask named buildspec.yml.

```
# Buildspec runs in the build stage of your pipeline.
version: 0.2
phases:
  install:
    runtime-versions:
      docker: 20
    commands:
      - echo "cd into $CODEBUILD_SRC_DIR/backend"
      - cd $CODEBUILD_SRC_DIR/backend-flask
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $IMAGE_URL
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...          
      - docker build -t backend-flask .
      - "docker tag $REPO_NAME $IMAGE_URL/$REPO_NAME"
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image..
      - docker push $IMAGE_URL/$REPO_NAME
      - echo "imagedefinitions.json > [{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json
      - printf "[{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json

env:
  variables:
    AWS_ACCOUNT_ID: 999999999999
    CONTAINER_NAME: backend-flask
    IMAGE_URL: 9999999999.dkr.ecr.us-east-1.amazonaws.com
    REPO_NAME: backend-flask:latest
artifacts:
  files:
    - imagedefinitions.json
```

We move back over to CodeBuild in AWS. We know we’re needing to pass environment variables, so we open a new tab and go to ECS to view our backend-flask service and see what env vars are being passed there. We pass these variables in our buildspec.yml file initially.

Moving on with CodeBuild, we can specify our Buildspec file. We select to use a buildspec file, then give the path to the file, which is backend-flask/buildspec.yml.

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/5c8b0922-7938-4d95-9aba-652e3126da22)


Scrolling further down, we enable logs from CloudWatch, then give a Group name and stream name.

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/e1546d07-9341-49d1-b384-f85afbf48d89)

Then we create the build project. The project is now created.

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/79a7b4c5-79f9-42d3-86a9-048697c624ea)

Our project doesn’t build automatically. Instead, we go back over to GitHub and initiate a Pull request. We merge our main branch into prod. We create the Pull request, then merge the Pull request. Back over in CodeBuild, our build has triggered multiple times now, not just from the Pull request.


![Screenshot 2024-03-02 225741](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/6d523247-1177-4b47-b382-cc0ecaa7acf8)


We stop all the builds in CodeBuild, then start a new one. The build never completes. We stop the build. We edit the environment of the build, removing the VPC option, subnet option, and security group option we set previously. We also realize that we aren’t passing anything to our ./bin/backend/build script when building the backend, so we will not need to pass our env vars to our buildspec.yml file either. We remove these.

I again reattempt the build. When I view the logs, I’m getting an AccessDeniedException error.

I’m able to resolve this by creating an inline policy in IAM for the codebuild-cruddur-service-role created earlier.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ssm:GetParameters",
            "Resource": [
                "arn:aws:ssm:us-east-1:999999999999:parameter/backend-flask/*",
                "arn:aws:ssm:us-east-1:999999999999:parameter/cruddur/backend-flask/*",
                "arn:aws:ssm:us-east-1:999999999999:parameter/*"
            ]
        }
    ]
}
```


With that, I attempt the build again, this time triggered by another pull request. The build succeeds.

![Screenshot 2024-03-03 024517](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/e6993ffb-c0ef-4daf-bf3e-9fb2c0e078c5)


We move back over to CodePipeline and edit the pipeline. We add an additional stage between the Source and the Deploy named build.


![Screenshot 2024-03-03 024851](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/520e675f-0ae9-4cb8-89d9-9d24b8be5c47)

We save the changes to our pipeline, then release the changes. Our build fails on the Deploy.

We edit the build stage of the pipeline, adding an Output artifact name of ImageDefinition.

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/ab89397c-007d-4f9c-86b5-b6fd04439ef0)

Then, we edit the Deploy action, changing the Input Artifacts to the ImageDefinition artifact outputted in the previous stage.


We save the pipeline, then release the changes. Our pipeline is now failing at the build stage.

There’s a CLIENT_ERROR message in the logs stating there's no matching artifact paths. With this, Andrew knows what's wrong and guides us back to our workspace. In our buildspec.yml file, we cd to our base path in the post_build.

```
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image..
      - docker push $IMAGE_URL/$REPO_NAME
      - cd $CODEBUILD_SRC_DIR
      - echo "imagedefinitions.json > [{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json
      - printf "[{\"name\":\"$CONTAINER_NAME\",\"imageUri\":\"$IMAGE_URL/$REPO_NAME\"}]" > imagedefinitions.json

 ```

 We commit this change to our code, then submit another pull request. We’re merging main into prod. Then we merge the request. The Deploy succeeds this time.



![Screenshot 2024-03-03 035033](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/e2aecbb8-8f4b-48c0-977f-1fb738b00d9c)




![Screenshot 2024-03-03 035620](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/4ca62ce2-1cbe-4ac0-af38-fefdc7fbefc3)
![Screenshot 2024-03-03 035637](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/38bb6ca4-84af-42fa-b62c-6e4723de4287)

We want to make sure this is working so we need to submit a change to our code. We open ./backend-flask/app.py and add a change to our health check returned data.

```
@app.route('/api/health-check')
def health_check():
  return {'success': True, 'ver': 1}, 200
  
```

We commit the change, then create another pull request. We head back over to CodePipeline. Once our pipeline passes the build stage, we open EC2 > Load Balancing > Target Groups and update the target groups for our backend-flask. One target must completely drain before the new target is active, the service is running, and the deploy stage completes.
![Screenshot 2024-03-03 035912](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/7b332ea2-a7b9-481b-92c3-3ef1ad0cf081)

We test our API health check to see if we’re up to date. We are. The health check is displaying our updated code.


![Screenshot 2024-03-03 040626](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/a5855c07-09e3-456d-8b37-d0cf075620e1)



