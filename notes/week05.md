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
- Copied create table code from AWS Boto3 documentation. It wasn’t perfect, so we adjusted code for schema.https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/create_table.html
- 
- Added the configuration for dynamodb in docker-compose which was commented out earlier for saving on compute.
- Ran ./bin/ddb/schema-load from the backend-flask directory.  It created our local DynamoDB table.
- 
![table-created](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/32056cdb-2bab-40d9-95c7-9ad7ae8a7d21)

