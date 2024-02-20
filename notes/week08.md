##week08
  
Week 8 was all about serverless image processing. 
   
Guest -  
Kristi Perreault, an AWS serverless hero. Kristi is a Principal Software Engineer at Liberty Mutual Insurance, focusing on serverless enablement and development for the last several years. 
  
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
  
- The id we're setting is __ThumbingBucket__ . We want to give the function a few more properties or props to make sure that it interacts with our other objects 
  and has a name for us to identify it. 
  We do this with {} brackets. One of the properties we add is a removalPolicy, which is an IAM policy.


- In statically-typed languages, including Go, TypeScript, Java, C#, Swift, and others, you typically need to explicitly declare the return type of a function. 
  This explicit declaration helps ensure type safety and allows the compiler to catch type-related errors during compilation.

- In the context of the AWS CDK (Cloud Development Kit) for TypeScript, s3.IBucket is a type definition representing an interface or class that describes an S3 
  bucket. 
- When you see s3.IBucket as a return definition in TypeScript, it means that the function returns an object that implements the IBucket interface, which 
  represents an Amazon S3 bucket.

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

> Preparation: Bootstrapping prepares your AWS environment for deploying AWS CDK applications. It creates the necessary infrastructure resources that AWS CDK relies on, such as an S3 bucket for storing assets and an IAM role for executing CloudFormation stacks.
> Dependency: AWS CDK requires certain resources to be available in your AWS account before you can deploy your application. For example, it needs an S3 bucket to store assets like Lambda code or Docker images and an IAM role with appropriate permissions to deploy CloudFormation stacks.
> Convenience: Bootstrapping before deployment streamlines the deployment process. Once the AWS environment is bootstrapped, you can deploy your AWS CDK applications without worrying about setting up infrastructure resources manually.
  
  
We only have to bootstrap once per AWS account, or per region, if you’re wanting multiple regions. Moving to our terminal, we perform a bootstrap.
    
  
```
cdk bootstrap "aws://<AWSACCOUNTNUMBER>/<AWSREGION>
```
  
![Bootstrap Output](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/3cf8bb6d-0bbe-4f2e-be38-73cb312c65bb)
  
    
> Deployment involves synthesizing the infrastructure code into a CloudFormation template, while provisioning involves creating and configuring the actual AWS resources based on that template.
    
  
![cdkToolkit](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/8f098c96-c140-4a58-8433-252b600749e2)
  
```
cdk deploy
```

CLI output of cdk deploy
![cloudformation stack after deploy](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/60b23a39-f7f5-4e2b-93f4-a6d6a0f2b4a3)

    
cdk deploy creates stack in cloudformation  
![cloudformation stack](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/e4f2794f-a8c5-4577-9563-c76d6607bf52)
  
S3 Bucket Formed
![s3 bucket](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/0deac8bb-e117-4223-a386-23087ea51d86)
  
    
We now move back over to our workspace and begin with our Lambda function. We first import lambda to our thumbing-serverless-cdk-stack.ts file.
  
```
import * as lambda from 'aws-cdk-lib/aws-lambda';
```
    
Then we create a Lambda function to return a Lambda function.
  
```
createLambda(): lambda.IFunction {
  const lambdaFunction = new lambda.Function(this, 'ThumbLambda', {
    runtime: lambda.Runtime.NODEJS_18_X,
    handler: 'index.handler',
    code: lambda.Code.fromAsset(functionPath)
  });
```

  
__this__ is the Construct object that the Lambda function will be a part of. ThumbLamdba is the name of the function in the CloudFormation stack. The runtime is the runtime of our environment. In this instance, we chose Node.js 18.x. The handler is the name of the handler function that will be invoked when the Lambda function is triggered. The code is the source code of our Lambda function. We haven't defined a variable for this yet, so we enter a placeholder of functionPath for the time being.
  
When the handler is set to "index.handler," it means that the Lambda function will look for a file named "index.js" (or whatever file extension is appropriate for the chosen runtime, like "index.ts" for TypeScript) and will execute the function named "handler" within that file when it's triggered. So, in this case, the Lambda function will trigger the code inside the "handler" function in the "index.js" file.  

  
We now define that __lambda__ function.
  
```
const functionPath: string = process.env.THUMBING_FUNCTION_PATH as string;
```
  
Now we have to pass this into our createLambda function, then return the lambdaFunction.

```  
createLambda(functionPath: string): lambda.IFunction {
  const lambdaFunction = new lambda.Function(this, 'ThumbLambda', {
    runtime: lambda.Runtime.NODEJS_18_X,
    handler: 'index.handler',
    code: lambda.Code.fromAsset(functionPath)
  });
  return lambdaFunction;
```
  
Our bucket is there, but not our lambda. We need to define the lambda.
  
```
const lambda = this.createLambda(functionPath);
```
  
![ERROR because environment variables not being set](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/bd72b047-5bbc-4eeb-aa31-b8cbd3387069)
  
We haven’t defined our environment variables yet where we’re using bucketName and functionPath as strings. To fix this, we create a new .env file in our thumbing-serverless-cdk directory. In the .env file, we begin defining our env vars.
  
```
THUMBING_BUCKET_NAME="assets.gooddesignsolutions.in"
THUMBING_FUNCTION_PATH="/workspaces/aws-bootcamp-cruddur-2023/aws/lambdas/process-images"
```
  
Later, we will put these variables elsewhere once the Lambda is created. We again try to cdk synth but this time we get a ERR_INVALID_ARG_TYPE error. We come to find out after trying to console.log(functionPath) that it came back undefined. We still need to load our environment variables from the .env file we created. In our code we do this:
  
// Load env variables
```
const dotenv = require('dotenv')
dotenv.config();

```
  
Again we cdk synth and again we get a new error:
We need to load the module into our environment for dotenv.
   
```
npm i dotenv
```
  
We alter how we’re loading our environmental variables by commenting out a line.
  
// Load env variables
//const dotenv = require('dotenv')
```
dotenv.config();
```
We again cdk synth. This time it completes successfully.  
  
![cdk synth lambda function](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/35df0918-eed2-4bc8-b1b9-133d431318f0)  


We continue on, now defining a few environment variables for our Lambda function.

```
createLambda(functionPath: string, bucketName: string, folderInput: string, folderOutput: string): lambda.IFunction {
  const lambdaFunction = new lambda.Function(this, 'ThumbLambda', {
    runtime: lambda.Runtime.NODEJS_18_X,
    handler: 'index.handler',
    code: lambda.Code.fromAsset(functionPath),
    environment: {
      DEST_BUCKET_NAME: bucketName,
      FOLDER_INPUT: folderInput,
      FOLDER_OUTPUT: folderOutput,
      PROCESS_WIDTH: '512',
      PROCESS_HEIGHT: '512'
    }
  });
  return lambdaFunction;
```
  
Next we must define the variables we passed, as we have not defined them yet.
   
 ```
const bucketName: string = process.env.THUMBING_BUCKET_NAME as string;
const functionPath: string = process.env.THUMBING_FUNCTION_PATH as string;
const folderInput: string = process.env.THUMBING_S3_FOLDER_INPUT as string;
const folderOutput: string = process.env.THUMBING_S3_FOLDER_OUTPUT as string;

const bucket = this.createdBucket(bucketName);
const lambda = this.createLambda(functionPath, bucketname, folderInput, folderOutput);
```


Then, we have to add the env vars to our .env file.

```
THUMBING_BUCKET_NAME="assets.gooddesignsolutions.in"
THUMBING_S3_FOLDER_INPUT="avatars/orignal"
THUMBING_S3_FOLDER_OUTPUT="avatars/processed"
THUMBING_WEBHOOK_URL="api.gooddesignsolutions.in/webhooks/avatars"
THUMBING_TOPIC_NAME="cruddur-assets"
THUMBING_FUNCTION_PATH="/workspaces/aws-bootcamp-cruddur-2023/aws/lambdas/process-images"
```


    
Add the install of CDK to our .gitpod.yml file. We navigate to our .gitpod.yml file and add the installation.
  
```
  - name: cdk
    before: |
      npm install aws-cdk -g
```
    

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/0401a281-8fb9-4e6d-a06c-c83097c4eb5b)




MISSING PARTS HERE ----------------------------


WILL ADD LATER -------------------------------

MOST OF STUFF HAS BEEN UNDERSTOOD AND HAVE SCREENSHOTS-----------------

LETME GO AHEAD FOR NOW AND FOCUS ON IMPLEMTATION PART WHICH I AM FINDING DIFFICULT--------





- Now that we’ve worked out uploading to our S3 buckets and processing the image
- We must work on implementation.

   
Moving back to our workspace, we begin on this by making sure we’re logged into ECR first.
   
```
./bin/ecr/login
```

- Docker Compose Up.
- ./bin/db/setup
- ./bin/ddb/schema-load
- ./bin/ddb/seed
- We access our web app, then login and head over the the Profile page to gather an idea of what we're looking at.
- We want to return some user activity on the Profile page. Over in our workspace, we create a new query named backend-flask/db/sql/users/show.sql.


   
```sql
-- Selecting specific columns from the 'users' table
SELECT
  users.uuid, -- Selecting the unique identifier for each user
  users.handle, -- Selecting the handle (username) of each user
  users.display_name, -- Selecting the display name of each user

  -- Subquery to fetch recent activities of the user and formatting them as JSON array
  (
    -- Using a subquery to format activities as a JSON array
    SELECT COALESCE( -- COALESCE function returns the first non-null value in the list
      array_to_json( -- Converts an array to a JSON array
        array_agg( -- Aggregates multiple rows into an array
          row_to_json(array_row) -- Converts a row to a JSON object
        )
      ),'[]'::json) -- If the result of the array_to_json is NULL, it returns an empty JSON array
    FROM (
      -- Selecting specific columns from the 'activities' table
      SELECT
        activities.uuid, -- Selecting the unique identifier for each activity
        users.display_name, -- Selecting the display name of the user associated with the activity
        users.handle, -- Selecting the handle of the user associated with the activity
        activities.message, -- Selecting the message content of the activity
        activities.created_at, -- Selecting the timestamp when the activity was created
        activities.expires_at -- Selecting the timestamp when the activity expires

      -- Joining 'activities' table with 'users' table based on user_uuid
      FROM public.activities  

      -- Filtering activities for the current user based on their UUID
      WHERE 
        activities.user_uuid = users.uuid

      -- Ordering the activities by their creation timestamp in descending order
      ORDER BY activities.created_at DESC

      -- Limiting the number of activities returned to 40
      LIMIT 40    
    ) array_row
  ) as activities

-- From the 'users' table
FROM public.users

-- Filtering users based on their handle (username)
WHERE
  users.handle = %(handle)s 

```

Activities Subquery:
Retrieves the latest activities associated with a specific user.
Includes details such as activity UUID, user display name, user handle, message, creation timestamp, and expiration timestamp.
Limits the result to the 40 most recent activities.
Converts the result into a JSON array.
  



Example result of this query:

```
{
  "uuid": "1a2b3c4d-1234-5678-90ab-cdef12345678",
  "handle": "example_handle",
  "display_name": "Example User",
  "activities": [
    {
      "uuid": "123e4567-e89b-12d3-a456-426614174000",
      "display_name": "Example User",
      "handle": "example_handle",
      "message": "Posted a photo",
      "created_at": "2024-02-20 15:30:00",
      "expires_at": "2024-02-27 15:30:00"
    },
    {
      "uuid": "234e5678-e89b-12d3-a456-426614174001",
      "display_name": "Example User",
      "handle": "example_handle",
      "message": "Liked a post",
      "created_at": "2024-02-20 14:45:00",
      "expires_at": "2024-02-27 14:45:00"
    }
  ]
}

```

In this query, the subquery is used to select data from the 'activities' table based on the user UUID, which effectively joins the 'activities' table with the 'users' table. The join condition activities.user_uuid = users.uuid is specified in the WHERE clause of the subquery.

  
In app.py

```
@app.route("/api/activities/@<string:handle>", methods=['GET']) -------> this is where the frontend will send the request 
#@xray_recorder.capture('activities_users')
def data_handle(handle):
  model = UserActivities.run(handle)        ---------> Here it goes to the UserActivities which we will edit further so that it runs the sql query on the db.
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
```



We begin removing our mock data from our code. We start with ./backend-flask/services/user_activities.py.
```py
class UserActivities:  # Defines a new class called UserActivities.

  def run(user_handle):  # Defines a method called run within the class, taking a parameter user_handle.
  
    try:  # Starts a try block to handle potential exceptions.
    
      model = {  # Initializes a dictionary called model.
        'errors': None,  # Initializes a key 'errors' with a value of None in the model dictionary.
        'data': None  # Initializes a key 'data' with a value of None in the model dictionary.
      }

      if user_handle == None or len(user_handle) < 1:  # Checks if the user_handle is None or its length is less than 1.
        model['errors'] = ['blank_user_handle']  # Sets the 'errors' key in the model dictionary to a list containing the string 'blank_user_handle'.
      else:  # If the user_handle is not None and its length is at least 1, execute the following block of code.
        sql = db.template('users','show')  # Constructs an SQL query using a template method provided by the db object, presumably to retrieve user data.
        results = db.query_onject_json(sql)  # Executes the SQL query and stores the results in JSON format, in the results variable.
        model['data'] = results  # Sets the 'data' key in the model dictionary to the results obtained from the query.
    
    finally:  # This block of code will execute regardless of whether an exception occurred in the try block.
      return model  # Returns the model dictionary containing either data or errors.
```




Since nothing was passing along, we comment out our try, update our indentation, and add a couple of print's to see what is returning and where.
  
![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/05d60e44-3a13-48fa-ad2c-a708192972bd)
  
  
We refresh our web app and immediately get an error stating NameError: name 'db' is not defined. That's because we need to import it.
  
```
from lib.db import db
```


After a few more syntax cleanups, we are now returning data in our Profile page, but our frontend isn’t built to implement it just yet. We move over to our frontend-react-js/src/pages/UserFeedPage.js file. Andrew explains we're returning the data and we have to setActivities, but now it's being set differently. We update our loadData function.




Making changes to UserFeedPage.js
```
const loadData = async () => {
  try {
    // Construct the backend URL using an environment variable and the 'title' variable
    const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/${title}`;      
    
    // Send a GET request to the backend URL using the fetch API 
    const res = await fetch(backend_url, {                              -----> here it goes to backend url and fetches the db
      method: "GET"
    });
    
    // Parse the response body as JSON
    let resJson = await res.json();        ---> Once it is fetched we colled the response 
    
    // Check if the response status is 200 (OK)
    if (res.status === 200) {
      // Update the state variable 'activities' with the activities data from the backend
      setActivities(resJson.activities);
    } else {
      // Log the entire response object to the console for debugging if the response status is not 200
      console.log(res);
    }
  } catch (err) {
    // Log any errors that occur during the execution of the try block
    console.log(err);
  }
};

```




Now, 

```
const [profile, setProfile] = React.useState([]); 
```

- React.useState([]): This part is calling the useState hook provided by React. The useState hook is a function that returns an array with two elements:

  * The first element is the current state value (profile in this case).
  * The second element is a function that allows you to update the state (setProfile in this case).

- const [profile, setProfile] = ...: This line uses array destructuring syntax (Destructuring assignment is a feature in JavaScript that allows you to extract values from arrays or properties from objects and assign them to variables in a concise and convenient way.) in JavaScript.
-  It's essentially a shortcut for extracting values from an array and assigning them to variables. In this case, it's extracting the first and second elements from the array returned by useState and assigning them to profile and setProfile respectively.

Example:

```
const person = { firstName: 'John', lastName: 'Doe', age: 30 };

// Extracting properties from the object
const { firstName, lastName, age } = person;

console.log(firstName); // Output: John
console.log(lastName); // Output: Doe
console.log(age); // Output: 30

```


Now 
```
const [profile, setProfile] = React.useState([]);

if (res.status === 200) {
    setProfile(resJson.profile);
}
```



Here's how it works:

- When the backend code triggers the SQL query and returns the response to the frontend, the response should include both profile and activities data, based on  the structure of the SQL query.

- In your frontend code, you check if the HTTP response status is 200, indicating a successful response.

- If the response is successful, you extract the profile and activities data from the resJson object returned by the backend.

- You then update the profile state variable using setProfile with the profile data obtained from the backend.

- Similarly, you update the activities state variable using setActivities with the activities data obtained from the backend.

  
  
  
Our data structure doesn’t reflect this yet, so we must update our template in backend-flask/db/sql/users/show.sql.
  
  
```
SELECT
  (SELECT COALESCE(row_to_json(object_row),'{}'::json) FROM (
    SELECT
      users.uuid,
      users.cognito_user_id as cognito_user_uuid,
      users.handle,
      users.display_name,
  ) object_row) as profile,
```
  
  
Profile Subquery:
Retrieves profile information for a specific user.
Includes details such as UUID, cognito user ID, handle, display name, bio, and the count of activities associated with the user.
Converts the result into a JSON object.
  
  
We refresh our web app, and we’re now returning data. Andrew points out that we can now use this data returned below:
  

To populate our Profile page with information.

Continuing on with integration, we create a new component, ./frontend-react-js/src/components/EditProfileButton.js.















```
// Importing the CSS file that contains styles for the EditProfileButton component
import './EditProfileButton.css';

// Defining the EditProfileButton component and exporting it as the default export
export default function EditProfileButton(props) {
  // Declaring a function named pop_profile_form which will handle the click event
  const pop_profile_form = (event) => {
    // Preventing the default action associated with the event (e.g., form submission, link navigation)
    event.preventDefault();
    
    // Calling the setPopped function passed via props to update the state in the parent component
    props.setPopped(true);
    
    // Returning false to prevent any further propagation of the event
    return false;
  }

  // Returning JSX to render a button element with an onClick event handler
  return (
    <button onClick={pop_profile_form} className='profile-edit-button'>Edit Profile</button>
  );
}

```




We add the EditProfileButton.js to our UserFeedPage.js by importing it.
```
import EditProfileButton from '../components/EditProfileButton';
```
  
  
We refactor some code by removing it from ./frontend-react-js/src/components/ActivityFeed.js and placing it into UserFeedPage.js.
![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/cc027632-c167-45e0-b083-e07113f31491)


We then take this refactored code and place it in HomeFeedPage.js.
```
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm
          popped={popped}
          setPopped={setPopped} 
          setActivities={setActivities} 
        />
        <ReplyForm 
          activity={replyActivity} 
          popped={poppedReply} 
          setPopped={setPoppedReply} 
          setActivities={setActivities} 
          activities={activities} 
        />
        <div className='activity_feed'>
          <div className='activity_feed_heading'>
            <div className='title'>Home</div>
          </div>         
          <ActivityFeed 
            setReplyActivity={setReplyActivity} 
            setPopped={setPoppedReply} 
            activities={activities} 
          />
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
```
We also add this to our NotificationsFeedPage.js as well.

```
        <div className='activity_feed'>
          <div className='activity_feed_heading'>
            <div className='title'>{title}</div>
          </div>        
          <ActivityFeed activities={activities} />
        </div>
```
        
When we go back to our web app and refresh, it still works. We login, and navigate around various pages to make sure it works. We notice on the Profile page, it’s not showing that we’re logged in. Andrew explains not all of our conditionals are showing in the Profile page. Back in our workspace, we go to our HomeFeedPage.js and add an import for our checkAuth and getAccessToken functions.

```
import {checkAuth, getAccessToken} from '../lib/CheckAuth';
```
We add headers to bring in our access_token, call the getAccessToken function, and add a const defining our access_token.
```
  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/@${params.handle}`
      await getAccessToken()
      const access_token = localStorage.getItem("access_token")
      const res = await fetch(backend_url, {
        headers: {
          Authorization: `Bearer ${access_token}`
        },
        method: "GET"
      });
```
      
We then passed setUser as an argument for checkAuth.
```
  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth(setUser);
  }, [])
```

When we refresh the Profile page now, it’s showing that we’re logged in. We begin to talk about how we can implement different structure into the Profile page. We move back over to our UserFeedPage.js and make some additions.

```
    <article>
      <DesktopNavigation user={user} active={'profile'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm popped={popped} setActivities={setActivities} />
      
        <div className='activity_feed'>
          <div className='activity_feed_heading'>
            <div className='title'>{profile.display_name}</div>
            <div className='cruds_count'>{profile.cruds_count} Cruds</div>
          </div>
          <ActivityFeed activities={activities} />
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>

```

We must update our SQL template to return this new data field, cruds_count. Back over in ./backend-flask/db/sql/users/show.sql we update the query.
```


SELECT
  (SELECT COALESCE(row_to_json(object_row),'{}'::json) FROM (
    SELECT
      users.uuid,
      users.cognito_user_id as cognito_user_uuid,
      users.handle,
      users.display_name,
      users.bio,
      (
      SELECT 
       count(true)
      FROM public.activities
      WHERE
        activities.user_uuid = users.uuid
       ) as cruds_count
  ) object_row) as profile,

```
We refresh our web app, and now when we inspect the page, we are getting a ReferenceError: title is not defined error.


This is what it’s referencing:


This is correct, we removed this field previously. We move over to UserFeedPage.js and update backend_url.

      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/@${params.handle}`

      
We refresh our web app again, and our Profile page is not displaying a name or any data. We navigate back to our UserFeedPage.js and find that we called setActivities twice. Assuming the HTTP response status of the fetch request is equal to 200, the first call to setActivities with resJson.profile as an argument would set the activities state to the profile value instead of the intended activities data. The second call to setActivities with resJson.activities would set the activities state to the correct value. We update our code:

      if (res.status === 200) {
        setProfile(resJson.profile)
        setActivities(resJson.activities)
Now when we refresh the web app, we are seeing a name displayed on the Profile page. The Crud Count is there as well, its just not easliy visible right now, but we will fix this later.


Andrew decides now that we’re going to break this up into its own component. In ./frontend-react-js-src/components/ we create a new component named ProfileHeading.js.

```
import './ProfileHeading.css';
import EditProfileButton from '../components/EditProfileButton';

export default function ProfileHeading(props) {

  return (
  <div className='activity_feed_heading profile_heading'>
    <div className='title'>{props.profile.display_name}</div>
    <div className="cruds_count">{props.profile.cruds_count} Cruds</div>
    
    <div className="avatar">
      <img src="https://assets.thejoshdev.com/avatars/data.jpg"></img>
    </div>
      
    <div className="display_name">{props.display_name}</div>
    <div className="handle">{props.handle}</div>
      
    <EditProfileButton setPopped={props.setPopped} />
  </div> 
  );
}

```

In our UserFeedPage.js file, we add a const:
```
  const [poppedProfile, setPoppedProfile] = React.useState([]);
```
Then we add it in our 'activity_feed'.

        <div className='activity_feed'>
          <ProfileHeading setPopped={setPoppedProfile} profile={profile} />
We again refresh our web app.


ProfileHeading is not defined. We need to import it.

In UserFeedPage.js.
```
import ProfileHeading from '../components/ProfileHeading';
```

We again refresh our web app. The screenshot below is from Andrew’s Profile page.


We need to do some styling on this page now. In our ./frontend-react-js/src/components/ProfileHeading.css file, we begin creating some styling.

.profile_heading .avatar img {
    width: 140px;
    height: 140px;
    border-radius: 999px;
}
We again refresh our web app.


We need to add a banner image as well. We search for and find an image online for a banner. We need a way to upload this image as our banner, so we head over to S3 in the AWS console. Then we create a new folder in our assets bucket named banners and upload our banner.jpg.

In ProfileHeading.js, we make several changes.

export default function ProfileHeading(props) {
  const backgroundImage = 'url("https://assets.thejoshdev.com/banners/banner.jpg")';
  const styles = {
    backgroundImage: backgroundImage,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };
  return (
    <div className='activity_feed_heading profile_heading'>
    <div className='title'>{props.profile.display_name}</div>
    <div className="cruds_count">{props.profile.cruds_count} Cruds</div>
    <div className="banner" style={styles} >
When we refresh our web app now, we have a banner!


We make several changes to the ProfileHeading.css file.

.profile_heading .avatar {
    position: absolute;
    bottom: -74px;
    left: 16px;  
}
.profile_heading .avatar img {
    width: 148px;
    height: 148px;
    border-radius: 999px;
    border: solid 8px var(--fg);
}

.profile_heading .banner {
    position: relative;
    height: 200px;
}
Then, we made made changes to the styling of the EditProfileButton.css.

.profile-edit-button {
    border: solid 1px rgba(255,255,255,0.5);
    padding: 12px 20px;
    font-size: 18px;
    background: none;
    border-radius: 999px;
    color: rgba(255,255,255,0.8);
    cursor: pointer;
}

.profile-edit-button:hover {
    background: rgba(255,255,255,0.3);
}
We refresh our app and draw our attention to the double entries of the username and the extra line as well. Andrew spots the issue in our UserFeedPage.js file and removes the duplicate code, since it now has its own component. Speaking of that component, in ProfileHeading.js we begin wrapping our div's.

    <div className="info">
      <div className='id'>
        <div className="display_name">{props.display_name}</div>
        <div className="handle">@{props.handle}</div>
      </div>
We update the styling in ProfileHeading.css to reflect the changes.

.profile_heading .banner {
    position: relative;
    height: 200px;
}

.profile_heading .info {
    display: flex;
    flex-direction: row;
    align-items: start;
    padding: 16px;
}

.profile_heading .info .id {
    padding-top: 86px;
    flex-grow: 1;
    color: rgb(255,255,255);
}
We refresh our web app again. We find that our username isn’t displaying correctly now.


The div's we wrapped earlier aren't being called correctly. We fix this in the code:

From this:


To this:


    <div className="info">
      <div className='id'>
        <div className="display_name">{props.profile.display_name}</div>
        <div className="handle">@{props.profile.handle}</div>
      </div>
This fixes the issue:


We continue editing the styling in ProfileHeading.css.

.profile_heading {
    padding-bottom: 0px;
}

.profile_heading .profile-avatar {
    position: absolute;
    bottom: -74px;
    left: 16px;
    width: 148px;
    height: 148px;
    border-radius: 999px;
    border: solid 8px var(--fg);  
}

.profile_heading .banner {
    position: relative;
    height: 200px;
}

.profile_heading .info {
    display: flex;
    flex-direction: row;
    align-items: start;
    padding: 16px;
}

.profile_heading .info .id {
    padding-top: 70px;
    flex-grow: 1;
}

.profile_heading .info .id .display_name {
    font-size: 24px;
    font-weight: bold;
    color: rgb(255,255,255);    
}

.profile_heading .info .id .handle {
    font-size: 16px;
    color: rgba(255,255,255,0.7);
}
Then we give the Edit Profile button a hover. We edit our EditProfileButton.css file.

.profile-edit-button {
    border: solid 1px rgba(255,255,255,0.5);
    padding: 12px 20px;
    font-size: 18px;
    background: none;
    border-radius: 999px;
    color: rgba(255,255,255,0.8);
    cursor: pointer;
}

.profile-edit-button:hover {
    background: rgba(255,255,255,0.3);
}
When we refresh our web app this time, our Edit Profile button is visible, readable, and has a hover action.


We add more styling to ProfileHeading.css to make our Crud Count visible.

.profile_heading .cruds_count {
    color: rgba(255,255,255,0.7);
}

At the start of the next instructional video, Andrew explains that he’s found a solution to a constant problem we’ve had since the beginning of bootcamp. Consistantly when we update code and refresh our web app, additional spaces need to be entered for the new code to be pushed to the logs. We go to our ./backend-flask/Dockerfile and add the following:

ENV PYTHONUNBUFFERED=1
A little extra insight via ChatGPT:

“The ENV PYTHONUNBUFFERED=1 statement is used in a Dockerfile to set an environment variable. Specifically, it sets the PYTHONUNBUFFERED variable to the value of 1.

In Python, when the standard output (stdout) or standard error (stderr) streams are used, the output may be buffered, meaning that the output is held in a buffer before being written to the console. This can lead to unexpected behavior when running Python scripts in a containerized environment, where logs and output may not appear immediately.

Setting PYTHONUNBUFFERED to 1 disables output buffering for Python, which ensures that output is immediately written to the console. This can be useful for logging and debugging purposes."

We make sure we’re signed into ECR, then we attempt a Docker compose up.


This is happening because the script generate-env is not running correctly for our backend from our .gitpod.yml file. We view the file. While viewing, we add a new section for Docker, so we can be logged into ECR automatically when launching our workspace.


We also remove the source from the path to run the generate-env script.

  - name: flask 
    command: |
      "$THEIA_WORKSPACE_ROOT/bin/backend/generate-env"
To test this, we commit our changes, then quit and relaunch our workspace. The change failed.


For the sake of moving onward, for now, we remove the scripts from our .gitpod.yml file. We also remove the section for Docker we added above. Instead, we go back to our /bin/bootstrap file. Maybe we can get this working correctly for logging into ECR.

#! /usr/bin/bash
set -e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="bootstrap"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

ABS_PATH=$(readlink -f "$0")
BIN_DIR=$(dirname $ABS_PATH)

source "$BIN_DIR/ecr/login"
source "$BIN_DIR/backend/generate-env"
source "$BIN_DIR/frontend/generate-env"
When we run the script, it logs us into ECR and generates a backend-flask.env and a frontend-react-js.env file. We then decide to try and get a script running to do what we originally set out ./bin/bootstrap to do. We create ./bin/prepare.

#! /usr/bin/bash
set -e # stop if it fails at any point

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="prepare"
printf "${CYAN}====== ${LABEL}${NO_COLOR}\n"

ABS_PATH=$(readlink -f "$0")
BIN_PATH=$(dirname $ABS_PATH)
DB_PATH="$BIN_PATH/db"
DDB_PATH="$BIN_PATH/ddb"

source "$DB_PATH/create"
source "$DB_PATH/schema-load"
source "$DB_PATH/seed"
python "$DB_PATH/update_cognito_user_ids"
python "$DDB_PATH/schema-load"
python "$DDB_PATH/seed"
We make the file executable, then do a Docker compose up. With our environment running, we check the ports and see the backend is not running. We view the logs of the backend.


When we added ENV PYTHONUNBUFFERED=1 to our Dockerfile earlier, we forgot to remove the -u from our Docker CMD. We do so now.

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567", "--debug"]
We compose down our environment, then compose up again. We check the ports again and everything is now running. We then run our new script ./bin/prepare. This script does not work, so we manually run the scripts to setup our tables and seed data to our web app locally. With our app now getting data, we login. We navigate over to our Profile page.


When we click the Edit Profile button, nothing happens right now. We begin implenting some new code. We create a new file named ./frontend-react-js/jsconfig.json.

{
    "compilerOptions": {
      "baseUrl": "src"
    },
    "include": ["src"]
  }
The compilerOptions object contains options that affect how code is compiled into JavaScript. In this case, the option specified is baseUrl, which sets the base directory for resolving non-relative module names. Specifically, it sets the base URL for resolving module specifiers in import statements to the src directory.

For example, in our HomeFeedPage.js file, we can now alter our import statements from this:


To this:

import DesktopNavigation  from 'components/DesktopNavigation';
import DesktopSidebar     from 'components/DesktopSidebar';
import ActivityFeed from 'components/ActivityFeed';
import ActivityForm from 'components/ActivityForm';
import ReplyForm from 'components/ReplyForm';
import {checkAuth, getAccessToken} from 'lib/CheckAuth';
Andrew further explains its powerful due to this fact how we can move our files around anywhere in our directories as the pathing is absolute to the import.

Moving onward, we create another new component, ./frontend-react-js/src/components/ProfileForm.js

import './ProfileForm.css';
import React from "react";
import process from 'process';
import {getAccessToken} from 'lib/CheckAuth';

export default function ProfileForm(props) {
  const [bio, setBio] = React.useState(0);
  const [displayName, setDisplayName] = React.useState(0);

  React.useEffect(()=>{
    console.log('useEffects',props)
    setBio(props.profile.bio);
    setDisplayName(props.profile.display_name);
  }, [props.profile])

  const onsubmit = async (event) => {
    event.preventDefault();
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/profile/update`
      await getAccessToken()
      const access_token = localStorage.getItem("access_token")
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bio: bio,
          display_name: displayName
        }),
      });
      let data = await res.json();
      if (res.status === 200) {
        setBio(null)
        setDisplayName(null)
        props.setPopped(false)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }

  const bio_onchange = (event) => {
    setBio(event.target.value);
  }

  const display_name_onchange = (event) => {
    setDisplayName(event.target.value);
  }

  const close = (event)=> {
    console.log('close',event.target)
    if (event.target.classList.contains("profile_popup")) {
      props.setPopped(false)
    }
  }

  if (props.popped === true) {
    return (
      <div className="popup_form_wrap profile_popup" onClick={close}>
        <form 
          className='profile_form popup_form'
          onSubmit={onsubmit}
        >
          <div class="popup_heading">
            <div class="popup_title">Edit Profile</div>
            <div className='submit'>
              <button type='submit'>Save</button>
            </div>
          </div>
          <div className="popup_content">
            <div className="field display_name">
              <label>Display Name</label>
              <input
                type="text"
                placeholder="Display Name"
                value={displayName}
                onChange={display_name_onchange} 
              />
            </div>
            <div className="field bio">
              <label>Bio</label>
              <textarea
                placeholder="Bio"
                value={bio}
                onChange={bio_onchange} 
              />
            </div>
          </div>
        </form>
      </div>
    );
  }
}
“The component takes in props as a parameter, which includes props.popped, a boolean indicating whether the popup is currently shown or not, and props.profile, an object containing the current user profile information. We're using React hooks such as useState and useEffect to manage state and perform side effects. useState is used to manage the state of bio and displayName, which hold the user's bio and display name respectively. useEffect is used to update the bio and displayName states whenever the props.profile object changes. The component also defines several functions that handle events such as form submission and input change. When the form is submitted, it sends a POST request to the backend API to update the user's profile information. When the input fields are changed, it updates the corresponding states. Finally, the component returns the popup form if props.popped is true, and null otherwise." - thank you ChatGPT.

We then get to work on the frontend-react-js/src/components/ProfileForm.css file.

form.profile_form input[type='text'],
form.profile_form textarea {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  outline: none;
  display: block;
  outline: none;
  resize: none;
  width: 100%;
  padding: 16px;
  border: solid 1px var(--field-border);
  background: var(--field-bg);
  color: #fff;
}

.profile_popup .popup_content {
  padding: 16px;
}

form.profile_form .field.display_name {
  margin-bottom: 24px;
}

form.profile_form label {
  color: rgba(255,255,255,0.8);
  padding-bottom: 4px;
  display: block;
}

form.profile_form textarea {
  height: 140px;
}

form.profile_form input[type='text']:hover,
form.profile_form textarea:focus {
  border: solid 1px var(--field-border-focus)
}

.profile_popup button[type='submit'] {
  font-weight: 800;
  outline: none;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 16px;
  background: rgba(149,0,255,1);
  color: #fff;
}
With the styling completed, we now move over to our UserFeedPage.js file and import the ProfileForm then return it.

import ProfileForm from 'components/ProfileForm'; 

  return (
    <article>
      <DesktopNavigation user={user} active={'profile'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm popped={popped} setActivities={setActivities} />
        <ProfileForm 
          profile={profile}
          popped={poppedProfile} 
          setPopped={setPoppedProfile} 
        />

        <div className='activity_feed'>
          <ProfileHeading setPopped={setPoppedProfile} profile={profile} />
          <ActivityFeed activities={activities} />
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
When we refresh our web app and click Edit Profile it's getting a bit better.


We refactor some code from ./frontend-react-js/src/components/ReplyForm.css by removing a portion, then refactoring it into a new component called Popup.css.

.popup_form_wrap {
  z-index: 100;
  position: fixed;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding-top: 48px;
  background: rgba(255,255,255,0.1)
}

.popup_form {
  background: #000;
  box-shadow: 0px 0px 6px rgba(190, 9, 190, 0.6);
  border-radius: 16px;
  width: 600px;
}

.popup_form .popup_heading {
  display: flex;
  flex-direction: row;
  border-bottom: solid 1px rgba(255,255,255,0.4);
  padding: 16px;
}

.popup_form .popup_heading .popup_title{
  flex-grow: 1;
  color: rgb(255,255,255);
  font-size: 18px;

}
We need to import this. Andrew says since this is a global component, we will import it into frontend-react-js/src/app.js.

import './components/Popup.css';
We refresh our web app and take a look.


Andrew notes that if we click outside of the Profile form, the form goes away. This is by design. Andrew shows us frontend-react-js/src/components/ProfileForm.js.


The close function in the code is an event listener function that is called when the user clicks on the div element with className of popup_form_wrap profile_popup. The function checks if the clicked element has a classList that contains profile_popup and, if so, it calls props.setPopped(false) to update the popped state to false and close the popup.

We now must add an endpoint for the Profile so it will save. We navigate over to our ./backend-flask/app.py file and implement it.

@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()
def data_update_profile():
  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verify(access_token)
    cognito_user_id = claims['sub']
    model = UpdateProfile.run(
      cognito_user_id=cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    return {}, 401
More ChatGPT insight: “The function first retrieves the bio and display_name parameters from the JSON data in the request body, and extracts the access_token from the request headers using the extract_access_token function. The try block attempts to verify the access token using the cognito_jwt_token.verify function, which returns a dictionary containing the token's claims if successful. The cognito_user_id is extracted from the claims using the sub key.

The UpdateProfile.run method is then called with the cognito_user_id, bio, and display_name parameters to update the user's profile data. The model variable contains the result of the UpdateProfile.run method call.

If model['errors'] is not None, indicating that there were errors during the update operation, the function returns the errors and a status code of 422. Otherwise, the function returns the data and a status code of 200 (OK).

If the access token cannot be verified due to a TokenVerifyError, the function returns an empty dictionary and a status code of 401 (Unauthorized)."

We also add an import statement for the service.

from services.update_profile import *
Then, we create a new service for this in ./backend-flask/services named update_profile.py.

from lib.db import db

class UpdateProfile:
  def run(cognito_user_id,bio,display_name):
    model = {
      'errors': None,
      'data': None
    }

    if display_name == None or len(display_name) < 1:
      model['errors'] = ['display_name_blank']

    if model['errors']:
      model['data'] = {
        'bio': bio,
        'display_name': display_name
      }
    else:
      handle = UpdateProfile.update_profile(bio,display_name,cognito_user_id)
      data = UpdateProfile.query_users_short(handle)
      model['data'] = data
    return model

  def update_profile(bio,display_name,cognito_user_id):
    if bio == None:    
      bio = ''

    sql = db.template('users','update')
    handle = db.query_commit(sql,{
      'cognito_user_id': cognito_user_id,
      'bio': bio,
      'display_name': display_name
    })
  def query_users_short(handle):
    sql = db.template('users','short')
    data = db.query_select_object(sql,{
      'handle': handle
    })
    return data
The run method takes cognito_user_id, bio, and display_name parameters, and returns a dictionary containing errors and data keys. The method first sets the errors and data values to None.

If display_name is None or has a length less than 1, the errors list is set to ['display_name_blank']. Andrew said we will handle errors near the end of the bootcamp. Otherwise, the update_profile method is called with the bio, display_name, and cognito_user_id parameters, and the query_users_short method is called with the handle value returned from the update_profile method to retrieve the updated user data.

If there are no errors, the data value is set to the updated user data. The model dictionary is then returned with the errors and data keys.

The update_profile method takes bio, display_name, and cognito_user_id parameters and updates the user data in the database with the specified values. The method first sets the bio value to an empty string if it is None, and then executes a query to update the user data in the database.

The query_users_short method takes a handle parameter and executes an SQL query to retrieve the user data associated with the specified handle. The method then returns the user data as a dictionary.

Now we must add the query that’s going to update the user’s profile. We make a new file in ./backend-flask/db/users named update.sql.

UPDATE public.users 
SET 
  bio = %(bio)s,
  display_name= %(display_name)s
WHERE 
  users.cognito_user_id = %(cognito_user_id)s
RETURNING handle;
We’re returning the handle after updating the bio and display_name fields in the public.users table for the user with a cognito_user_id that matches the value provided by the %(cognito_user_id)s parameter. The values provided by the %(bio)s and %(display_name)s parameters sets the bio and display_name fields respectively.

Andrew explained that in our update_profile.py file, we are using ./backend-flask/db/users/short.sql which takes a handle, which is why we're returning handle in ./backend-flask/db/users/update.sql.


Currently, there’s no bio field added to our database. This code will fail if ran. We need to add it to our database. Andrew said we could've just added a query to insert it, but at some point we were needing migrations functionality added, so we begin discussing SQL migrations.

What are SQL migrations? Let’s let ChatGPT explain: “SQL migrations are a way of managing changes to the database schema over time, typically as part of a software development process. A migration is a script that describes a change to the database schema, such as adding or modifying a table, column, or index. The migration script is executed by a tool or framework that manages the database schema, which applies the changes to the database.

SQL migrations allow developers to evolve the database schema over time in a controlled and repeatable manner. They also help to manage the complexity of database changes by providing a history of changes that can be reviewed, rolled back, or applied incrementally. In addition, migrations enable collaboration between developers working on the same project by providing a standardized way of managing database changes.”

Andrew shows us an example of a SQL migration library built on SQLAlchemy, but said that for the purposes of our learning, we’re going to setup one of our own. We create a new folder in our ./bin/ directory named generate, then inside the new folder, a new Python script named migration.

#!/usr/bin/env python3
import time
import os
import sys

if len(sys.argv) == 2:
  name = sys.argv[1]
else:
  print("pass a filename: eg. ./bin/generate/migration add_bio_column")
  exit(0)

timestamp = str(time.time()).replace(".","")

filename = f"{timestamp}_{name}.py"

# convert undername name to title case e.g. add_bio_column -> AddBioColumn
klass = name.replace('_', ' ').title().replace(' ','')

file_content = f"""
from lib.db import db
class {klass}Migration:
  def migrate_sql():
    data = \"\"\"
    \"\"\"
    return data
  def rollback_sql():
    data = \"\"\"
    \"\"\"
    return data
  def migrate():
    db.query_commit({klass}Migration.migrate_sql(),{{
    }})
  def rollback():
    db.query_commit({klass}Migration.rollback_sql(),{{
    }})
migration = AddBioColumnMigration
"""
# remove leading and trailing new lines
file_content = file_content.lstrip('\n').rstrip('\n')

current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations',filename))
print(file_path)

with open(file_path, 'w') as f:
  f.write(file_content)
Andrew breaks this down. First we have a name:

if len(sys.argv) == 2:
  name = sys.argv[1]
else:
  print("pass a filename: eg. ./bin/generate/migration hello")
  exit(0)
We generate a unique timestamp based on the current time in seconds, to create a unique filename for the migration file:

timestamp = str(time.time()).replace(".","")
The script then constructs the filename by concatenating the timestamp and the desired migration name:

filename = f"{timestamp}_{name}.py"
Then we generate out a Python Migration file.

file_content = f"""
from lib.db import db
class {klass}Migration:
  def migrate_sql():
    data = \"\"\"
    \"\"\"
    return data
  def rollback_sql():
    data = \"\"\"
    \"\"\"
    return data
  def migrate():
    db.query_commit({klass}Migration.migrate_sql(),{{
    }})
  def rollback():
    db.query_commit({klass}Migration.rollback_sql(),{{
    }})
migration = AddBioColumnMigration
"""
We then write the contents of the migration file by getting the current directory of the script, contructing a path to the migrations directory, which we haven't created yet.

current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations',filename))
Next, it then opens a file object at this path and writes the contents of the file_content variable to it.

with open(file_path, 'w') as f:
  f.write(file_content)
We now have to create the directory our script is writing to. We navigate over to backend-flask/db/ and create a new folder named migrations. Within the directory, we create a .keep file, since the directory is currently empty, but we want to KEEP the directory around regardless. Then, we make our new script executable. After this, we test the script.

./bin/generate/migration add_bio_column

You can see we now generated the Python file below:


We view the generated migration file:


Andrew explains the idea is we can generate the file, then we populate it.

from lib.db import db

class AddBioColumnMigration:
  def migrate_sql():
    data = """
    ALTER TABLE public.users ADD COLUMN bio text;
    """
    return data
  def rollback_sql():
    data = """
    ALTER TABLE public.users DROP COLUMN;
    """
    return data
    
  def migrate():
    this.query_commit(AddBioColumnMigration.migrate_sql(),{
    })
    
  def rollback():
    this.query_commit(AddBioColumnMigration.rollback_sql(),{
    })
    
migration = AddBioColumnMigration
With what we’ve populated in the migration file, the function migrate_sql will return a string that performs the SQL query to add the new column bio to our database. rollback_sql function will return a string that performs a SQL query to drop the bio column instead, hence "rollback". Andrew explains in Ruby and other languages, these functions are called an "up" and a "down" instead of "migrate" and "rollback" respectively. We're naming them as they are because you "migrate forward" to add the column and "rollback" to revert the changes and drop the column.

We need a way to trigger these migration files. For this, we will create a couple of new scripts. We head to our ./bin/db directory and create two new scripts within this folder: migrate and rollback. Before even implementing code to these scripts, we make them executable so we don't forget. Then, we implement ./bin/db/migrate.

#!/usr/bin/env python3

import os
import sys
import glob
import re
import time
import importlib

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask'))
sys.path.append(parent_path)
from lib.db import db

def get_last_successful_run():
  sql = """
  SELECT
      coalesce(
      (SELECT last_successful_run
      FROM public.schema_information
      LIMIT 1),
      '0') as last_succesful_run
  """
  return int(db.query_value(sql,{},verbose=False))

def set_last_successful_run(value):
  sql = """
  UPDATE schema_information
  SET last_successful_run = %(last_successful_run)s
  """
  db.query_commit(sql,{'last_successful_run': value})
  return value

last_successful_run = get_last_successful_run()

migrations_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations'))
sys.path.append(migrations_path)
migration_files = glob.glob(f"{migrations_path}/*")


for migration_file in migration_files:
  filename = os.path.basename(migration_file)
  module_name = os.path.splitext(filename)[0]
  match = re.match(r'^\d+', filename)
  if match:
    file_time = int(match.group())
    if last_successful_run <= file_time:
      mod = importlib.import_module(module_name)
      mod.migration.migrate()
      print('running migration: ',module_name)
      timestamp = str(time.time()).replace(".","")
      last_successful_run = set_last_successful_run(timestamp)
In this script, we are importing the necessary modules, including the db module from our backend lib. Then, we're setting the current_path and parent_path env vars based on the location of the script and our backend directory.

import os
import sys
import glob
import re
import time
import importlib

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask'))
sys.path.append(parent_path)
from lib.db import db
Our get_last_successful_run function is querying the schema_information table to get the timestamp of the last successful migration. If there's been no successful migration recorded, it's returning a value of 0.

def get_last_successful_run():
  sql = """
  SELECT
      coalesce(
      (SELECT last_successful_run
      FROM public.schema_information
      LIMIT 1),
      '0') as last_succesful_run
  """
  return int(db.query_value(sql,{},verbose=False))
The set_last_successful_run function updates the schema_information table with the provided timestamp and returns the same value.

The script then retrieves the last successful migration timestamp using get_last_successful_run, and sets the migrations_path env var to the migrations directory in the backend's db directory. It uses glob to retrieve a list of all migration files in the directory, and iterates over them in order of filename as a list or array.

def set_last_successful_run(value):
  sql = """
  UPDATE schema_information
  SET last_successful_run = %(last_successful_run)s
  """
  db.query_commit(sql,{'last_successful_run': value})
  return value

last_successful_run = get_last_successful_run()

migrations_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations'))
sys.path.append(migrations_path)
migration_files = glob.glob(f"{migrations_path}/*")
For each migration file, the script extracts the filename and module name, and extracts the timestamp from the filename using a regular expression. If the timestamp is greater than or equal to the last successful migration timestamp, the script imports the module and calls its migrate method to perform the migration. It then updates the schema_information table with the current timestamp using set_last_successful_run.

for migration_file in migration_files:
  filename = os.path.basename(migration_file)
  module_name = os.path.splitext(filename)[0]
  match = re.match(r'^\d+', filename)
  if match:
    file_time = int(match.group())
    if last_successful_run <= file_time:
      mod = importlib.import_module(module_name)
      mod.migration.migrate()
      print('running migration: ',module_name)
      timestamp = str(time.time()).replace(".","")
      last_successful_run = set_last_successful_run(timestamp)
For this to run correctly, we must implement the schema_information table into our ./backend-flask/db/schema.sql file. We add a query to create the table.

CREATE TABLE IF NOT EXISTS public.schema_information (
  last_successful_run text
);
Andrew explains this query is different than others because we’re not dropping this table if it exists, we’re creating the table if it doesn’t exist since it’s storing useful information for migrations. Since our code is already expecting the table to be created, from our terminal we will manually add it. But first, we must connect to our database, so we’ll use our connect script to do so.

./bin/db/connect
Now that we’re connected to our database, we create the table.


We next run the query for our get_last_successful_run function manually, just so we can see what the value is returned.


Since we have not run the migration yet, the value is 0. Andrew explains the way coalesce works within our function.


Since we always want to return a default value, and there’s current no value since we’ve never ran a migration, we want to return back a number, or empty value. In the snippet above, if there is no record, coalesce returns back a NULL value. Since we can't return a number, we're returning a string value of 0 instead. If this does not make sense, just remember: the query retrieves the value of the last_successful_run column from the schema_information table, or the string '0' if the column does not exist or is NULL.

We now move onto the other script we were working on, ./bin/db/rollback.

#!/usr/bin/env python3

import os
import sys
import glob
import re
import time
import importlib

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask'))
sys.path.append(parent_path)
from lib.db import db

def get_last_successful_run():
  sql = """
  SELECT
      coalesce(
      (SELECT last_successful_run
      FROM public.schema_information
      LIMIT 1),
      '0') as last_succesful_run
  """
  return int(db.query_value(sql,{},verbose=False))

def set_last_successful_run(value):
  sql = """
  UPDATE schema_information
  SET last_successful_run = %(last_succesful_run)s
  """
  db.query_commit(sql,{'last_successful_run': value})
  return value

last_successful_run = get_last_successful_run()

migrations_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations'))
sys.path.append(migrations_path)
migration_files = glob.glob(f"{migrations_path}/*")


last_migration_file = None
for migration_file in migration_files:
  if last_migration_file == None:
    filename = os.path.basename(migration_file)
    module_name = os.path.splitext(filename)[0]
    match = re.match(r'^\d+', filename)
    if match:
      file_time = int(match.group())
      if last_successful_run > file_time:
        last_migration_file = module_name
print(last_migration_file)
This script is similar to migrate as we're using get_last_successful_run and set_last_successful_run, adding the migration file path and iterating through it, but the key difference is, we're just checking for the last migration.

last_migration_file = None
for migration_file in migration_files:
  if last_migration_file == None:
    filename = os.path.basename(migration_file)
    module_name = os.path.splitext(filename)[0]
    match = re.match(r'^\d+', filename)
    if match:
      file_time = int(match.group())
      if last_successful_run > file_time:
        last_migration_file = module_name
print(last_migration_file)
last_migration_file is initially set to None. On each migration file, if last_migration_file is still None, the filename and module name is extracted, then it's checked to see if the timestamp is smaller than the last successful migration file's timestamp. If this condition is true, the module_name is assigned to last_migration_file. The loop will stop after the first migration file that is older than the last successful run is found, and last_migration_file will contain the name of the last migration that was run successfully. Then we print out the value of the last_migration_file.

We attempt to run the migrate script.

./bin/db/migrate

Andrew explains we’re receiving this error because he didn’t want our queries to print out on our return statement return int(db.query_value(sql,{},verbose=False)). To fix this, we must update ./backend-flask/lib/db.py.

  def query_commit(self,sql,params={},verbose=True):
    if verbose:
      self.print_sql('commit with returning',sql,params)
  def query_array_json(self,sql,params={},verbose=True):
    if verbose: 
      self.print_sql('array',sql,params)
  def query_object_json(self,sql,params={},verbose=True):
    if verbose: 
      self.print_sql('json',sql,params)
      self.print_params(params)
  def query_value(self,sql,params={},verbose=True):
    if verbose: 
      self.print_sql('value',sql,params)
We again attempt to run our script. This time, we receive a different error from the terminal:


We must navigate back over to our migration.py file to fix. We update the file from this:


To this:


Then we make the same changes to the queries in our migration file in the ./backend-flask/db/migrations directory itself.


We again run our script: ./bin/db/migrate.


You can see from the image above that we’re setting the last_successful_run. Since we know that's working, we add the additional flag we added above to our migrate script to remove the query from printing out.

db.query_commit(sql,{'last_successful_run': value},verbose=False)
Since migrate is now working, we need to see of rollback will. We run our script: ./bin/db/rollback. It returns None, but it should be returning the value of last_migration_file, which we know ran successfully with migrate. We add a few print lines to our code in rollback to see what's being returned, then run the script again.



We can see that last_successful_run is returning None. We return to the terminal where we're connected to our database and repeat our query for get_last_successful_run:


We try to manually set last_successful_run in the schema_information table by running our query manually for set_last_successful_run:

UPDATE schema_information SET last_successful_run ="1";
Then we again repeat the get_last_successful_run query to see what's returned:


Andrew said this is because we’re trying to update the table instead of inserting into it. Since last_successful_run should never be None or NULL value, we have to update our queries. In migrate, we update the query for get_last_successful_run.

def get_last_successful_run():
  sql = """
    SELECT last_successful_run
    FROM public.schema_information
    LIMIT 1
  """
  return int(db.query_value(sql,{},verbose=False))
We update rollback with the updated query as well. Then, we move over to ./backend-flask/db/schema.sqlas we must insert into the schema_information table.

INSERT INTO public.schema_information (last_successful_run) 
VALUES ("0")
Andrew further explains that we only want to do this once. So there must be a condition where the record is only created if the record doesn’t exist. We add this:

INSERT INTO public.schema_information (last_successful_run) 
VALUES ("0")
WHERE (SELECT count(true) FROM public.schema_information) = 0
We attempt to manually insert into our database from terminal where we’re connected, but it doesn’t work. Our WHERE clause is invalid. We modify the query:

INSERT INTO public.schema_information (last_successful_run) 
SELECT "0"
WHERE (SELECT count(true) FROM public.schema_information) = 0

After some review, Andrew provides a solution. We will add another field to our schema_information table. This will allow us to insert into the database but it will be dependent upon the value of id. We also add the UNIQUE constraint to the id field to ensure that nothing else can appear with the same value.

CREATE TABLE IF NOT EXISTS public.schema_information (
  id integer UNIQUE,
  last_successful_run text
);
INSERT INTO public.schema_information (id,last_successful_run) 
VALUES (1,'0')
ON CONFLICT (id) DO NOTHING;
The query now inserts a single row with id set to 1 and last_successful_run set to '0'. The ON CONFLICT clause specifies that if a row with id of 1 already exists, then the insert should do nothing.

We manually drop our table schema_information. Then we manually run our first query above:

CREATE TABLE IF NOT EXISTS public.schema_information (
  id integer UNIQUE,
  last_successful_run text
);
Then our second:


It completed successfully. We check to be sure.

SELECT * FROM schema_information;

Then to test our ON CONFLICT clause by running the query again to make sure it won't insert.


Before we can test our rollback script again, we must manually run the query from our generated migration file, since it didn't run correctly the first time.


ALTER TABLE public.users DROP COLUMN bio;
The query completes successfully. Now, we can attempt our migration again.

./bin/db/migrate

We again query our database to make sure the migrate script worked correctly.


We again test rollback.

./bin/db/rollback
This time it completes successfully.


We now must alter our rollback script as we only want it to run once. For this, we grab code from our migrate script and refactor it into our rollback script.

last_migration_file = None
for migration_file in migration_files:
  if last_migration_file == None:
    filename = os.path.basename(migration_file)
    module_name = os.path.splitext(filename)[0]
    match = re.match(r'^\d+', filename)
    if match:
      file_time = int(match.group())
      if last_successful_run > file_time:
        last_migration_file = module_name
        mod = importlib.import_module(module_name)
        print('=== rolling back: ',module_name)      
        mod.migration.rollback()
        set_last_successful_run(file_time)
We also update our query for set_last_successful_run in rollback and migrate to be more explicit by adding a WHERE clause.

def set_last_successful_run(value):
  sql = """
  UPDATE schema_information
  SET last_successful_run = %(last_successful_run)s
  WHERE id = 1
  """
  db.query_commit(sql,{'last_successful_run': value})
  return value
We want to test this, so we again run our migrate script.

./bin/db/migrate
We refresh our web app, then navigate to the Profile page and click Edit Profile. When we attempt to update the Bio field then save, nothing happens. We access the backend logs to see if we're getting any errors, which it turns out, we are:


Andrew has a good idea what the problem is. We move over to our backend-flask/services/update_profile.py file and take a look at the query_users_short function.


It’s no longer query_select_object just query_object. We update the code:


We refresh the web app, then view our backend logs again:


We navigate to ./backend-flask/lib/db.py to check the function there and make sure we're naming it correctly here.


Since we’re wanting to return JSON here, we need to update update_profile.py to use query_object_json instead.


Another app refresh, and another error is returned from the backend logs.


We navigate to our ./backend-flask/app.py file and review. It's a problem with our try. We're not assigning model :

@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()
def data_update_profile():
  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verify(access_token)
    cognito_user_id = claims['sub']
    UpdateProfile.run(
      cognito_user_id=cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    return {}, 401
We make the change to assign it:

  try:
    claims = cognito_jwt_token.verify(access_token)
    cognito_user_id = claims['sub']
    model = UpdateProfile.run(
      cognito_user_id=cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    if model['errors'] is not None:
      return model['errors'], 422
Now when we make a change to our Profile from the web app and click Save, our edit menu goes away. The change isn’t propagated right away, but requires a refresh of the page, then the changes are reflected in the Profile. Now that this is working, we need to render out our Bio that we added to the Profile. We head over to ./frontend-react-js/src/components/ProfileHeading.js. We want to add this as a separate div beneath our Edit Profile button.

  return (
    <div className='activity_feed_heading profile_heading'>
    <div className='title'>{props.profile.display_name}</div>
    <div className="cruds_count">{props.profile.cruds_count} Cruds</div>
    <div className="banner" style={styles} >
      <ProfileAvatar id={props.profile.cognito_user_uuid} />
    </div>
    <div className="info">
      <div className='id'>
        <div className="display_name">{props.profile.display_name}</div>
        <div className="handle">@{props.profile.handle}</div>
      </div>
      <EditProfileButton setPopped={props.setPopped} />
    </div>
    <div className="bio">{props.profile.bio}</div>

  </div> 
  );
}
Next we move over to the ProfileHeading.css file to work on the styling for the Bio section:

.profile_heading .bio {
    padding: 16px;
    color: rgba(255,255,255,0.7);
}
Then, we have to make sure bio is included in data returned, so we navigate to our template query in ./backend-flask/db/sql/users/show.sql and add it.

SELECT
  (SELECT COALESCE(row_to_json(object_row),'{}'::json) FROM (
    SELECT
      users.uuid,
      users.cognito_user_id as cognito_user_uuid,
      users.handle,
      users.display_name,
      users.bio,
      (
Now when we refresh our web app, we have a bio field added to the Profile page!


Moving on, we need to implement the uploading of our avatars to our web app. To get started on this, we need to install the AWS SDK for S3. From the terminal, we install it.

npm i @aws-sdk/client-s3 --save
Next, we start a new function to ProfileForm.js.

const s3upload = async (event)=> {

}
Then, we have to add an onClick event for this function.

<div className="upload" onClick={s3upload}>
  Upload Avatar
</div>
We’re going to upload to our bucket through use of an API endpoint that will trigger a Lambda, so now we move over to the AWS Console and launch API Gateway. From here, we are prompted as to what type of API we would like to build.


We select HTTP API, then we’re prompted to configure our integrations. We choose a Lambda integration, but we do not have our Lambda function created yet. So we open an additional tab, and navigate to Lambda through the AWS console. Andrew mentions we can make this function in any language we want. Andrew’s affinity for Ruby shines through, and we select Ruby as the Runtime for our newly named function, CruddurAvatarUpload.


On permissions, we leave it with the option “Create a new role with basic Lambda permissions”, as we’ll create our own role. We leave all Advanced Settings unchecked.


Then, we create our function. We want to generate out a presigned URL. The reason for this is a client will make a request to the API Gateway we’re setting up. It requests a presigned URL for uploading an object, in our case, an image to S3. API Gateway will invoke the Lambda function, generating the presigned URL using the AWS SDK. Our Lambda function will return the presigned URL to the API, in turn returning it to the client as well. The client then uses the presigned URL to upload the image to our S3 bucket.

To have a place to work on our function, we create a new folder in our ./aws/lambdas directory named cruddur-upload-avatar, then a new file within named function.rb. We first add code to initialize the client.

require 'aws-sdk-s3'

client = Aws::S3::Client.new()
Andrew explains we will next generate out a Gem file. A Gem file, or Gemfile, is a configuration file used in Ruby to specify the required Ruby gems (or libraries) for a Ruby project.

Further clarification per Google: “When you start a new Ruby project or work on an existing one, you may need to use external libraries or frameworks to add extra functionality to your project. RubyGems is a package manager that allows you to easily install and manage these libraries. A Gemfile is a text file that lists the required gems for a Ruby project, and specifies their version requirements.”

To generate out the Gemfile, we cd over to the correct directory in our terminal. /workspace/aws-bootcamp-cruddur-2023/aws/lambdas/cruddur-upload-avatar/. Next, we run a command to generate the Gemfile.

bundle init

The Gemfile is generated.


We access the Gemfile created. Then, we add a library for “aws-sdk-s3”.

# frozen_string_literal: true

source "https://rubygems.org"

# gem "rails"
gem "aws-sdk-s3"
Next, we install the library from terminal.

bundle install
This installs from terminal.


We can also see there’s now a Gemfile.lock file in our directory. This file lists all of the versions of all the gems (or libraries) that are installed in the Ruby project (directory), along with their dependencies.


Next we must add code to return a presigned URL for upload to our function. While researching this, we find that we don’t actually need to initialize the client.

require 'aws-sdk-s3'

s3 = Aws::S3::Resource.new
bucket_name = ENV["UPLOADS_BUCKET_NAME"]
object_key = "mock.jpg"

obj = s3.bucket(bucket_name).object(object_key)
url = obj.presigned_url(:put, expires_in: 3600)
puts url
We’re going to be passing some env vars to our function that need to be stored in our workspace. We’re generating some of the env vars in our .env.example file from our ./thumbing-serverless-cdk directory, particularly UPLOADS_BUCKET_NAME, but they need to be accessible from the entire workspace, so we pass the env vars through our terminal in our workspace.

export  UPLOADS_BUCKET_NAME="thejoshdev-uploaded-avatars"
gp env UPLOADS_BUCKET_NAME="thejoshdev-uploaded-avatars"
We run our function from the terminal to see what is returning for url.

bundle exec ruby function.rb
We receive a runtime error. We’re missing an XML pareser:


We go back to our Gemfile and edit the libraries to include Ox, which is an XML parser.

# frozen_string_literal: true

source "https://rubygems.org"

# gem "rails"
gem "aws-sdk-s3"
gem "ox"
We install the new library from our Gemfile.

bundle install
The new library is installing.


We again try running our function.rb file.

bundle exec ruby function.rb
This time it runs and returns a presigned URL via the terminal.


Andrew then shows us how to use an API client through our workspace in GitPod. We install a new client from the UI called Thunder Client.


If we use the presigned URL that was generated and insert it into Thunder Client, it prepopulates our Query Parameters.


We need to see if we can upload to our S3 bucket using the API. We upload an image downloaded from the internet to our workspace in our ./aws/lambdas/cruddur-upload-avatar directory.


Back in Thunder Client, we go to Body > Binary > Choose File > then select our lore.jpg file. We click Send, and receive a 403 Forbidden error.


With the error provided, it gives some insight: “Check your key and signing method.” We go back to our function.rb file and view the expires_in parameter of our presigned url.


It’s currently set to 3600 seconds or 1 hour. This should be sufficient time for the lore.jpg file to upload to our S3 bucket. We change the method of the request from Thunder Client to a PUT. Then, we try to Send again.


