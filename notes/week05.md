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




