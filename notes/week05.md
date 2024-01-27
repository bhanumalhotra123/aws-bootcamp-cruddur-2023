This week in the AWS Cloud Project Bootcamp, 
The entire livestream was lecture material on data modelling and access patterns, introducing DynamoDB.
guest instructor this week, Mr. Kirk Kirkconnell( lead developer advocate for Momento Serverless Cache and a NoSQL Database specialist.)
  
DynamoDB is a fully managed, serverless, NoSQL database designed to run high performance applications at any scale. It’s hosted by Amazon Web Services. 
  
This following helped me understand more about dynamodb(things like LSI, GSI etc):  
https://aws.amazon.com/blogs/compute/creating-a-single-table-design-with-amazon-dynamodb/
  

- Added boto3 to requirements.txt
- Ran pip install -r requirements.txt
- Got the environment up and running by performing a docker-compose up.
- Created 2 new folders in backend-flask/bin: db and rds.
- Moved all the db- batch scripts to db folder then removed “db-” from name to tidy up.
- Moved rds-update-sg-rule to rds folder and removed “rds”.
- Created a new folder in backend-flask/bin named ddb for DynamoDB stuff.
- Created new files in ddb folder: drop, schema-load, seed.(Also made them executable using chmod)
- Copied create table code from AWS Boto3 documentation. It wasn’t perfect, so adjusted code for schema.  
    
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/create_table.html
      
- Added the configuration for dynamodb in docker-compose which was commented out earlier for saving on compute.
- Ran ./bin/ddb/schema-load from the backend-flask directory.  It created our local DynamoDB table.
    
![Schemaload-ddb](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/c9bdec40-9edc-44a5-8ade-9673e8b43ba5)

  
- Created  list-tables under ddb.
- Created drop in ddb folder.
- Created seed in ddb folder.(The script fetches user information from a PostgreSQL database, creates message groups in DynamoDB, and populates these groups with messages, demonstrating integration between the two databases for user messaging functionality.)
![Seeding](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/3f48da00-c3f7-41f5-a78a-5834b33d366a)
  
  
- Ran schema-load
- Created scan and set it for local DynamoDB only, as doing a scan in production can be expensive.
  
- Created new folder in ddb named patterns, then created 2 new files: get-conversation and list-conversations.
  
> These allow us to begin implementing our access patterns. We first complete get-conversation, make it executable, then run it. This is similar to a scan, but
>  we’re returning information that we queried and limiting the results. In list-conversations, we began another our of access patterns. Andrew goes through
>  explaining the information we’re querying here as well, then we test. While testing, we go back to db.py in backend-flask/lib and update all instances of
>  print_sql to pass the params we set while refining our queries for mock data.
  
Added the following snippet in gitpod.yml
```yml
  - name: flask
    command: |
      cd backend-flask
      pip install -r requirements.txt
```
  
  
Made the drop file of psql by adding IF EXISTS to the statement:
```
psql $NO_DB_CONNECTION_URL -c "DROP DATABASE IF EXISTS cruddur;"
```
    
- created ddb.py in backend-flask/lib, and began implementing code to it. 
> Understood the difference between the Postgres database in db.py and what we’re implementing in ddb.py. In the Postgres database, we are doing initialization,
> using a constructor to create an instance of the class, and in ddb.py it’s a stateless class. If you can do things without state, it’s much easier for testing,
> as you just test the inputs and outputs, using simple data structures.
  
![db.py vs ddb.py](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/13b31d0a-df83-4efe-9a63-446e4da2f215)
  
  
- Had hardcoded the values of user_handle in last week, created a new file named cognito/list-users under backend-flask/bin.
 https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_users.html
  
```
export AWS_COGNITO_USER_POOL_ID="us-east-1_xxxx"
gp env AWS_COGNITO_USER_POOL_ID="us-east-1_xxxx"
```
  
- Updated AWS_COGNITO_USER_POOL_ID in docker-compose.yml to use the variable that was saved. Ran the file for list-users.
  ![list-users](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/47f263e7-47f7-4e0a-bf00-09ce9ce9634b)
  
  
- Under bin/db created update_cognito_user_ids.
> The sql command is updating our public.users table setting the cognito user id based on the sub we passed in. We then run a query commit to execute it. Further 
> down in the code, we’re doing the same thing that we did in list-users, but instead of printing the data, we’re returning it. Before we can do that, we have to 
> seed our data. We add a path to our setup file for update_cognito_user_ids. We run ./bin/db/setup, but get an error on that path, so instead we run 
> update_cognito_user_ids after running db/setup. We’re not returning the information we wanted, so we access db.py and find our query_commit definition. We were 
> missing params from being passed, so we added it, then back in terminal ran the script again. This time, it returned the information we wanted.
  
![update-users-in-db](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/d8f065be-459c-4e14-9960-b7cc95c2ce85)

  
  
We then edited our definition of data_message_groups in app.py by using some code from our /api/activities/home route. 
>This route (/api/message_groups) returns data about message groups. When accessed, it verifies the provided access token to confirm the user's identity. If >authenticated, it retrieves message group data associated with the user from the backend. If there are no errors, it returns the message group data; otherwise, it >returns an error status code.
   
After this, we next moved on to replace the mock data we had in message_groups.py and replaced it with a query to our Dynamo DB.
> When its run method is called with a cognito_user_id, it retrieves the user's UUID using a SQL query. Then, it uses a DynamoDB client to list message groups
> associated with that UUID. The retrieved data is stored in a model dictionary, which is then returned.
  
  
For this, we created a new folder inside backend-flask/db/sql named users, then a new SQL file named uuid_from_handle.sql.   
After this, we updated HomeFeedPage.js, MessageGroupsPage.js, MessageGroupPage.js, and MessageForm.js to include authorization headers we just created. 
  
Moving on we pulled CheckAuth and defined it in it’s own file, frontend-react-js/src/lib/CheckAuth.js.
- It asynchronously checks if a user is authenticated using AWS Cognito's Amplify library.
- Upon successful authentication, it retrieves the user's attributes, such as name and preferred username.
- It sets the user's attributes using a provided function to update the application's state.
- Inside the checkAuth function, if the user is successfully authenticated, it updates the user state using the setUser function. It sets the display_name and handle attributes based on the user's attributes retrieved from Cognito.
  
We updated our HomeFeedPage.js, MessageGroupsPage.js, MessageGroupPage.js, and MessageForm.js to use setUser, which we defined in CheckAuth.
  
>The setUser function is a state updater function provided by React's useState hook. In the context of the HomePage component, setUser is responsible for updating >the user state variable.
  
- Add our AWS_ENDPOINT_URL variable to our docker-compose.yml file.

![AWS_ENDPOINT_URL](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/f8bfb9ae-0eab-4003-a651-16dae393b9d9)

- Updated App.js for our path for the MessageGroupPage. Instead of going to a static @:handle, it’s now dependent upon the message_group_uuid.
  
![messagegrouppage](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/8df4378d-e622-434a-b772-fea69df113f6)
  
Updated this in our MessageGroupPage.js file.


>We next moved onto making our message group definition a little more strict. In ddb.py, we updated the KeyConditionExpression with what we listed in our 
>get-converstation.py file. We removed the hardcoded value of the year, and instead passed datetime.now()year as year. This failed, so we ended up having to put >the value into a string, like so: year = str(datetime.now().year). We moved onto updating the same value in list-conversations.py as well. After refreshing, the >data is again showing in the Messages section, but it’s listing the @handle as the page. We go into our MessageGroupItem.js file and pass out message_group_uuid >for /messages/. We also needed to update our const classes to pass the message_group_uuid as well. A quick refresh to our web app, and there’s no errors, but the >messages are not displaying. Andrew notes this is because it’s part of the query we need on the MessageGroupPage.js. We check our const loadMessageGroupData, and >it’s already passing the message_group_uuid. We need to start implementing this into our backend.
  
In app.py, we remove the hardcoding of user_sender_handle and update our def data_messages to pass message_group_uuid as well. (removedhardcodingWeek5) We then updated this again, this time checking for cognito_user_id and message_group_uuid. In messages.py, we updated the code to pass in the message_group_uuid called client, then it will list messages. In ddb.py, we add define a function for list_messages passing client and the message_group_uuid as well.
  
We previously added code to get the cognito_user_id in message_groups.py, so we add this code to messages.py as well. This is not being used now, but it’s for permissions checks we will implement later.
  
The mock messages however, are in the wrong order. To fix this, we had to reverse the items in our code. In ddb.py, we added items.reverse() to our code, then from did the same from our ddb/patterns/get-conversations file as well. For our conversations, we need to be able to differentiate between starting a new conversation and contiuing an existing one. To do this, we added a conditional if statement with an else passing along either the handle (new conversation) or message_group_uuid(existing conversation).






  



- Need to create a Dynamo DB Stream trigger so as to update the message groups.
- To start this, we ran ./bin/ddb/schema-load prod. We then logged into AWS and checked DynamoDB to see our new table.

  ![prod-ddb-table](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/f8fe974d-58ec-4daa-86ca-0ee7dda61699)



We next needed to turn on streaming through the console. To do this, we went to Tables > Exports and streams > Turn on. We finalized this by selecting New Image.

  ![Screenshot 2024-01-22 220506](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/44e5fc6b-ed98-434d-8a23-e9aed2a57b05)

  

-  Gateway endpoints, which are whats used for connecting to DynamoDB, do not incur additional charges. Created VPC endpoint in AWS named ddb-cruddur1 then connected it to DynamoDB as a service.
    
![Screenshot 2024-01-22 223230](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/62a67f7d-7734-4801-b04f-db8b39f0a443)

  
From here, we needed to create a Lambda function to run for every time we create a message in Cruddur (our web app). While reviewing the Lambda code to create the trigger, Andrew made note that it’s recreating the message group rows with the new sort key value from DynamoDB. This is because in DynamoDB, we cannot update these values. They must be removed and recreated.

```
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource(
 'dynamodb',
 region_name='us-east-1',
 endpoint_url="http://dynamodb.us-east-1.amazonaws.com"
)

def lambda_handler(event, context):
  print('event-data',event)

  eventName = event['Records'][0]['eventName']
  if (eventName == 'REMOVE'):
    print("skip REMOVE event")
    return
  pk = event['Records'][0]['dynamodb']['Keys']['pk']['S']
  sk = event['Records'][0]['dynamodb']['Keys']['sk']['S']
  if pk.startswith('MSG#'):
    group_uuid = pk.replace("MSG#","")
    message = event['Records'][0]['dynamodb']['NewImage']['message']['S']
    print("GRUP ===>",group_uuid,message)
    
    table_name = 'cruddur-messages'
    index_name = 'message-group-sk-index'
    table = dynamodb.Table(table_name)
    data = table.query(
      IndexName=index_name,
      KeyConditionExpression=Key('message_group_uuid').eq(group_uuid)
    )
    print("RESP ===>",data['Items'])
    
    # recreate the message group rows with new SK value
    for i in data['Items']:
      delete_item = table.delete_item(Key={'pk': i['pk'], 'sk': i['sk']})
      print("DELETE ===>",delete_item)
      
      response = table.put_item(
        Item={
          'pk': i['pk'],
          'sk': sk,
          'message_group_uuid':i['message_group_uuid'],
          'message':message,
          'user_display_name': i['user_display_name'],
          'user_handle': i['user_handle'],
          'user_uuid': i['user_uuid']
        }
      )
      print("CREATE ===>",response)
```
  

## Overview

The Lambda function is designed to update the position of a message within a message group that already exists in the DynamoDB table.

## Existing Message Group

The DynamoDB table contains multiple message groups, each identified by a unique partition key (pk). Within each message group, there are multiple messages stored with different sort key values (sk), representing their order within the group.

## Event Trigger

When an event occurs, such as a user reordering a message within a group, DynamoDB streams capture this event and trigger the Lambda function.

## Processing by Lambda Function

The Lambda function processes the event and extracts relevant information, such as the message group's unique identifier (group_uuid) and the updated sort key value (sk) of the message.

## Querying Existing Messages

The function queries the DynamoDB table using an index to retrieve all messages within the message group.

## Updating Sort Key

For each message retrieved from the query, the function updates its sort key value to reflect the new position or order within the group.

## Result

After the function completes execution, the messages within the group are repositioned according to the updated sort key values, ensuring that they are correctly ordered based on the new order specified by the event.

 When you update the sort key without deleting and recreating items, the sort key is changed, but the relative order of items within the table remains the same. However, if you delete and recreate items with updated sort keys, not only are the sort keys changed, but the items are also repositioned correctly according to the new sort order, ensuring that the table maintains the correct chronological order.

So, deleting and recreating items is crucial when you need to update the sort keys and maintain the sorted order within the table. This ensures consistency and accuracy in the representation of data.



# Conversation Update Example

Consider a scenario where we have a DynamoDB table storing messages exchanged between two people in a conversation.

## Original Table

| pk                | sk                      | message        |
|-------------------|-------------------------|----------------|
| MSG#Alice#Bob   | 2024-01-30T12:00:00Z   | "Hi Bob!"      |
| MSG#Alice#Bob   | 2024-01-30T12:05:00Z   | "How are you?" |
| MSG#Alice#Bob   | 2024-01-30T12:10:00Z   | "I'm good, thanks!" |
| MSG#Alice#Bob   | 2024-01-30T12:15:00Z   | "Want to grab lunch?" |

## Update Message

Let's say Alice wants to update her message "How are you?" to "How are you doing?" and also update the timestamp of the message.

### Without Deleting and Recreating Items

| pk                | sk                      | message                |
|-------------------|-------------------------|------------------------|
| MSG#Alice#Bob   | 2024-01-30T12:00:00Z   | "Hi Bob!"              |
| MSG#Alice#Bob   | 2024-01-30T12:05:00Z   | "How are you doing?"   | <- Updated Message
| MSG#Alice#Bob   | 2024-01-30T12:10:00Z   | "I'm good, thanks!"    |
| MSG#Alice#Bob   | 2024-01-30T12:15:00Z   | "Want to grab lunch?"  |

In this case, only the message content is updated, but the relative order of messages remains the same.

### Deleting and Recreating Items

After deletion and recreation:

| pk                | sk                      | message                |
|-------------------|-------------------------|------------------------|
| MSG#Alice#Bob   | 2024-01-30T12:00:00Z   | "Hi Bob!"              |
| MSG#Alice#Bob   | 2024-01-30T12:05:00Z   | "How are you doing?"   | <- Updated Message
| MSG#Alice#Bob   | 2024-01-30T12:10:00Z   | "I'm good, thanks!"    |
| MSG#Alice#Bob   | 2024-01-30T12:15:00Z   | "Want to grab lunch?"  |

In this case, "How are you doing?" is re-inserted into the table with the same timestamp. However, since the sort key is updated, the message is correctly positioned within the conversation chronologically according to its new content and timestamp.

This illustrates how deleting and recreating items within a conversation ensures not only the update of message content but also the maintenance of the correct chronological order of messages.


From the AWS console, we navigate to Lambda, then create a new trigger named cruddur-messageing-stream, using Python 3.9 runtime, and x86_64 architecture. For the execution role, we granted it a new role with Lambda permissions. We then enabled the VPC and selected our pre-existing one we configured last week, then selected “Create”



From here we went to Configuration > Permissions to set IAM role permissions for the function. We ran into a few snags during this process, as the pre-existing policies in AWS did not give us the role permissions we needed for our function to operate correctly. We found that we had not yet added our GSI (Global Secondary Indexes) to our db yet, so we deleted the DynamoDB table we created moments ago in AWS, then edited our ddb/schema-load file to include the GSI.

![gsi](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/8fb679a2-0c12-4aac-929a-245770092fa7)


Once the code was added to our ddb/schema-load file, we again ran ./bin/ddb/schema-load prod from terminal to recreate our table inside AWS DynamoDB. Next, we went back through and again turned on stremaing, setting stream details to New image. 
- Now we assign the trigger we created earlier to our table.


  ![add trigger](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/463ce0d8-007c-4ddf-a7d8-0b4de00dd234)


Now all we need to do is make our web app use production data. We went back over to docker-compose.yml and commented out the AWS_ENDPOINT_URL variable we had set previously.

After that, we then composed up our environment, and began testing the function.

Added IAM policy to lambda:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:Query"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-east-1:xxxx:table/cruddur-messages",
                "arn:aws:dynamodb:us-east-1:xxxx:table/cruddur-messages/index/message-group-sk-index"
            ]
        }
    ]
  }
```

With the new policy enabled, we tested again, then went back to the Cloudwatch logs.
Turned out, we were returning a record of events removed. We edited the Lambda again, this time adding a conditional that if the event is a remove event, we will return early.


![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/a1db4cf1-dd1f-4d74-9d2f-a9ba8ebad679)

  

```
Week 5 Notes Security Considerations – 

Amazon DynamDB – What is it and how does it work? 
DynamoDB use cases by industry: Customers rely on DynamoDB to support their mission-critical workloads
- Banking and finance
o Fraud detection
o User transactions
o Mainframe offloading
- Gaming
o Game states
o Leaderboards
o Player data stores
- Software and Internet
o Metadata caches
o Ride-tracking data stores
o Relationship graph data stores
- Ad tech
o User profile stores
o Metadata stores for assets
o Popular-item cache
- Retail
o Shopping carts
o Workflow engines
o Customer profiles
- Media and Entertainment
o User data stores
o Media metadata stores
o Digital rights management stores
Security Best Practices – AWS side
- Use VPC Endpoints: Use Amazon Virtual Private Cloud (VPC) to create a private network from your application or Lambda to a DynamoDB. This helps prevent unauthorized access to your instance from the public internet
- Compliance standard is what your business requires
- Amazon DynamoDB should only be in the AWS region that you are legally allowed to be holding user data in
- Amazon Organizations SCP – to manage DynamoDB table deletion, DynamoDB creation, region lock, etc
- AWS CloudTrail is enabled and monitored to trigger alerts on malicious DynamoDB behavior by an identity in AWS
- AWS Config Rules (as no GuardDuty even in March 2023) is enabled in the account and region of DynamoDB

Security Best Practices – application side
- DynamoDB to use appropriate Authentication – use IAM roles/AWS Cognito Identity Pool – avoid IAM users/groups
- DynamoDB User Lifecycle Management – create, modify, delete users
- AWS IAM roles instead of individual users to access and manage DynamoDB
- DAX Service (IAM) Role to have Read Only Access to DynamoDB (if possible)
- Not have DynamoDB be accessed from the internet (use VPC endpoints)
- Site to site VPN or Direct Connect for Onprem and DynamoDB Access
- Client side encryption is recommended by Amazon for DyanmoDB
```


