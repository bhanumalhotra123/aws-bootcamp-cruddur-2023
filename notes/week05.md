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
  
![table-created](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/32056cdb-2bab-40d9-95c7-9ad7ae8a7d21)

- Created  list-tables under ddb.
- Created drop in ddb folder.
- Created seed in ddb folder.
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

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/13b31d0a-df83-4efe-9a63-446e4da2f215)

