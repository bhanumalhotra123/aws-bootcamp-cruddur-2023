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


