This week in the AWS Cloud Project Bootcamp, 
The entire livestream was lecture material on data modelling and access patterns, introducing DynamoDB.
guest instructor this week, Mr. Kirk Kirkconnell( lead developer advocate for Momento Serverless Cache and a NoSQL Database specialist.)
  
DynamoDB is a fully managed, serverless, NoSQL database designed to run high performance applications at any scale. It’s hosted by Amazon Web Services. 



Data modelling - access patterns
We started with a very insightful 2-hour live stream about data modelling. The design that was chosen for our database is a simple table design. It is a popular choice these days and works well in this kind of scenario where all data is closely linked together. Based on its name it sounds simple but turns out to be quite complicated in terms of data modelling. To get everything working and to keep the cost down, it is crucial to have your data mapped with all different access patterns.

When designing a relational database you simply map the data in logical entities, see what data belongs together in each table and then figure out how to access the data from these tables by using joins. However, with DynamoDB you have to approach this from a completely different perspective. You have to think of your application and what data it is going to need and how. When you know your access patterns, you can start to think about how to organize your data. You can break the rules you would have with relational databases - data can even be duplicated if that works with your access patterns! Storage is cheap and you want your base table to support as many of your access patterns as possible so duplicating data could make sense depending on the situation. You could also choose to save some of the data as JSON instead of separate items if it's not going to be used in any of your queries.

There are so many options for designing the data model for your database. To get the best results from DynamoDB in terms of cost-effectiveness and performance, you really need to do these initial steps correctly.

Access patterns in our application
Our application is a messaging app where the user is able to see a list of their conversations (message groups) and then click an individual message group and see all messages that belong to that message group. Additionally, the user is obviously able to send messages - these could be either completely new messages that start new message groups or further messages to existing message groups. Based on this it was possible to list our initial access patterns:

- pattern A: showing a single conversation (message group).

- pattern B: a list of conversations (message groups).

- pattern C: create a new message

- pattern D: add a message to an existing message group

- pattern E: update a message group using DynamoDB streams

So the database is going to have one table, which is going to contain messages and message groups. Each item is going to have a unique uuid among other fields such as date, display name and message content. Each message group is also going to be listed twice as two individual items, from the perspective of the two users who are parts of the conversation. This is because a list of conversations cannot be displayed identically to both users, the person who is looking at their message groups wants to see the name of the other user listed as a topic of that message group.

Partition keys and sort keys
Then we come to the hardest part of data modelling, choosing the partition key. Partition key means an identifier for the item and it dictates under which partition DynamoDB puts the item under the hood. The partition key doesn't have to be unique and several items can have the same partition key. Sort key instead allows you to uniquely identify that item and allows it to be sorted. The primary key in DynamoDB can be either a simple primary key or a composite primary key (a combination of partition key and sort key). A partition key is always obligatory for any query and only an equality operator can be used. The sort key is not obligatory and not using it would simply return everything.

Our application has two access patterns that relate to messages and three that relate to message groups. For messages, we have to be able to write new messages and display the messages that belong to a certain message group. 

The best option is to use message_group_uuid as the partition key and created_at as the sort key for it. This is quite logical as we want to display a single conversation, so its identifier uuid is the easiest way to access it. Using created_at as a sort key will give us the option to display the messages within certain timeframes:


```
 def create_message(client,message_group_uuid, message, my_user_uuid,                  my_user_display_name, my_user_handle):
    now = datetime.now(timezone.utc).astimezone().isoformat()
    created_at = now
    message_uuid = str(uuid.uuid4())

    record = {
      'pk':   {'S': f"MSG#{message_group_uuid}"},
      'sk':   {'S': created_at },
      'message': {'S': message},
      'message_uuid': {'S': message_uuid},
      'user_uuid': {'S': my_user_uuid},
      'user_display_name': {'S': my_user_display_name},
      'user_handle': {'S': my_user_handle}
    }
```


For message groups, it gets a little bit more complicated. We have to be able to list message groups, add messages to message groups and update message group details. As each user naturally needs to see the message groups that belong exactly to them, the logical option is to use my_user_uuid as the partition key. This will work well as there are two message groups for each conversation, so each participant is going to have a version of the message group with their user uuid. As we want to be able to sort the message groups based on date, the sort key is going to be last_message_at:



 def create_message_group(client, message,my_user_uuid, my_user_display_name, my_user_handle, other_user_uuid, other_user_display_name, other_user_handle):
    table_name = 'cruddur-messages'
```
    message_group_uuid = str(uuid.uuid4())
    message_uuid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).astimezone().isoformat()
    last_message_at = now

    my_message_group = {
      'pk': {'S': f"GRP#{my_user_uuid}"},
      'sk': {'S': last_message_at},
      'message_group_uuid': {'S': message_group_uuid},
      'message': {'S': message},
      'user_uuid': {'S': other_user_uuid},
      'user_display_name': {'S': other_user_display_name},
      'user_handle':  {'S': other_user_handle}
    }
```
The catch is that the value of the sort key will of course have to be updated every time a new message is created and added to the message group so that it reflects the date of the actual latest message (access pattern E). This is where a global secondary index is needed.

Global secondary index
GSI is a concept that takes some time to get familiar with. It is basically an index with a partition key and a sort key that can be different from those in the base table. You can imagine creating a new index almost as creating a new table in SQL. It can contain the same items as the base table but in a different order. That means the data is the same, but we twist it and look at it differently. GSIs always add extra costs and you want to avoid them if you can - as already previously mentioned, your base table should support as many of your access patterns as possible.

For our final access pattern E, we want to update the sort key (last_message_at) to reflect the sort key of the latest message (created_at). This will be implemented by using a DynamoDB stream. Every time a new message is created and pushed to a message group, the DynamoDB stream catches the event and triggers a Lambda function. So, how do we get this Lambda function to update the sort key?

As previously mentioned, the message groups have user_uuid as the partition key. So for each update, we have two different message groups with two different user_uuids (as there are always two versions of each conversation, one from the perspective of each participant). Hence we won't be able to find the correct message groups that we need to update based on the partition key. We could of course do a scan with a filter, but that is not a cost-effective solution.

The best option in this situation is to use a GSI. This basically creates a clone of our primary table using the message_group_uuid as the partition key, but the two tables are kept in sync. This GSI allows for querying the table based on the message_group_uuid attribute, in addition to the primary key attributes 'pk' and 'sk':

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/2ce58ad2-d895-4b23-895d-1749cfc05d87)



The GSI was added to the schema:
```
GlobalSecondaryIndexes= [{
    'IndexName':'message-group-sk-index',
    'KeySchema':[{
      'AttributeName': 'message_group_uuid',
      'KeyType': 'HASH'
    },{
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    }],
    'Projection': {
      'ProjectionType': 'ALL'
    },
  }],
```
Now the creation of a new message will be captured by the DynamoDB stream, which triggers a Lambda function that will use the GSI to query all message groups where the message group uuid matches the partition key of the message. It will then replace the sort key (last_message_at) with the sort key value (created_at) of the message. The sort keys for the message and two message groups are now matching:

![image](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/02604eaf-723f-4de0-b892-2d8f8ba5835e)

  
This following helped me understand more about dynamodb:  
https://aws.amazon.com/blogs/compute/creating-a-single-table-design-with-amazon-dynamodb/
  

- Added boto3 to requirements.txt
- Ran pip install -r requirements.txt
- Got the environment up and running by performing a docker-compose up.
- Created 2 new folders in backend-flask/bin: db and rds.
- Moved all the db- batch scripts to db folder then removed “db-” from name to tidy up.
- Moved rds-update-sg-rule to rds folder and removed “rds”.
- Created a new folder in backend-flask/bin named ddb for DynamoDB stuff.
- Created new files in ddb folder: drop, schema-load, seed.(Also made them executable using chmod)


[Dynamodb create_table boto3 doc](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/create_table.html)
- Copied create table code from AWS Boto3 documentation. It wasn’t perfect, so adjusted code for schema.  
    

      
- Added the configuration for dynamodb in docker-compose which was commented out earlier for saving on compute.

```
  dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
```

- Ran ./bin/ddb/schema-load from the backend-flask directory.  It created our local DynamoDB table.

Now going forward we can use it for messages

```
#!/usr/bin/env python3

import boto3
import sys

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

ddb = boto3.client('dynamodb',**attrs)

table_name = 'cruddur-messages'


response = ddb.create_table(
  TableName=table_name,
  AttributeDefinitions=[
    {
      'AttributeName': 'message_group_uuid',
      'AttributeType': 'S'
    },
    {
      'AttributeName': 'pk',
      'AttributeType': 'S'
    },
    {
      'AttributeName': 'sk',
      'AttributeType': 'S'
    },
  ],
  KeySchema=[
    {
      'AttributeName': 'pk',
      'KeyType': 'HASH'
    },
    {
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    },
  ],
  GlobalSecondaryIndexes= [{
    'IndexName':'message-group-sk-index',
    'KeySchema':[{
      'AttributeName': 'message_group_uuid',
      'KeyType': 'HASH'
    },{
      'AttributeName': 'sk',
      'KeyType': 'RANGE'
    }],
    'Projection': {
      'ProjectionType': 'ALL'
    },
    'ProvisionedThroughput': {
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
    },
  }],
  BillingMode='PROVISIONED',
  ProvisionedThroughput={
      'ReadCapacityUnits': 5,
      'WriteCapacityUnits': 5
  }
)

print(response)
```
    
![Schemaload-ddb](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/c9bdec40-9edc-44a5-8ade-9673e8b43ba5)

  
- Created  list-tables under ddb.
- Created drop in ddb folder.
- Created seed in ddb folder.(The script fetches user information from a PostgreSQL database, creates message groups in DynamoDB, and populates these groups with messages, demonstrating integration between the two databases for user messaging functionality.)
  
  

Script for seeding
This script is a Python script that interacts with AWS DynamoDB to create message records for a messaging system. Here's a breakdown of what it does:

- Imports: The script imports necessary libraries including boto3 for AWS interaction, os, sys, datetime, timedelta, timezone, and uuid.
- Setting up paths: It sets up paths for importing custom libraries.
- Establishing DynamoDB Client: It creates a DynamoDB client using boto3.client.
- get_user_uuids Function: This function queries a database for user information based on their handles.
- create_message_group Function: This function creates a message group record in DynamoDB.
- create_message Function: This function creates individual message records in DynamoDB.
- Initial Data Setup: It sets up some initial data including a conversation and extracts users' messages and their corresponding user UUIDs.
- Loop for Creating Messages: It iterates through the conversation lines, determines which user the message belongs to (Person 1 or Person 2), assigns a timestamp to the message, and calls the create_message function to insert each message into DynamoDB.

In summary, the script creates:
```
#!/usr/bin/env python3

import boto3
import os
import sys
from datetime import datetime, timedelta, timezone
import uuid

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..'))
sys.path.append(parent_path)
from lib.db import db

attrs = {
  'endpoint_url': 'http://localhost:8000'
}
# unset endpoint url for use with production database
if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}
ddb = boto3.client('dynamodb',**attrs)


def get_user_uuids():
  sql = """
    SELECT 
      users.uuid,
      users.display_name,
      users.handle
    FROM users
    WHERE
      users.handle IN(
        %(my_handle)s,
        %(other_handle)s
        )
  """


#This part defines an SQL query that selects uuid, display_name, and handle from the users table where the handle matches either %(my_handle)s or %(other_handle)s.

  users = db.query_array_json(sql,{
    'my_handle':  'andrewbrown',
    'other_handle': 'bayko'
  })

                                                                                          now here we are calling query_array_json, the code for the query_array_json is following this isn't part of this script:
                                                                                          
                                                                                            def query_array_json(self,sql,params={}):
                                                                                              self.print_sql('array',sql,params)
                                                                                          
                                                                                              wrapped_sql = self.query_wrap_array(sql)
                                                                                              with self.pool.connection() as conn:
                                                                                                with conn.cursor() as cur:
                                                                                                  cur.execute(wrapped_sql,params)
                                                                                                  json = cur.fetchone()
                                                                                                  return json[0]



                                                                                          now this is further calling query_wrap_array from the class we created initially
                                                                                          
                                                                                          def query_wrap_array(self,template):
                                                                                              sql = f"""
                                                                                              (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
                                                                                              {template}
                                                                                              ) array_row);
                                                                                              """
                                                                                              return sql



                                                                                              In the context of this code snippet, the conversion to a JSON array is likely done to make the result set of the SQL query more compatible with modern web applications or other systems that consume JSON data.
                                                                                              
                                                                                              Here's a breakdown of the terms involved:
                                                                                              
                                                                                              JSON (JavaScript Object Notation): JSON is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate. It is based on key-value pairs and supports various data types, including objects (key-value pairs), arrays (ordered lists of values), strings, numbers, booleans, and null.
                                                                                              
                                                                                              Array: An array is a data structure that stores a collection of elements, typically of the same type, in a contiguous block of memory. In programming, arrays are commonly used to store lists of items that can be accessed by index.
                                                                                              
                                                                                              Here's what's happening:
                                                                                              
                                                                                              row_to_json(array_row): This function converts each row of the result set (array_row) into a JSON object.
                                                                                              array_agg(): This function aggregates the JSON objects generated by row_to_json() into an array.
                                                                                              array_to_json(): This function converts the aggregated array into a JSON array.
                                                                                              COALESCE(): This function returns the first non-null value among its arguments. If the result of array_to_json(array_agg()) is null (i.e., the result set is empty), it returns an empty JSON array [].
                                                                                              So, the entire subquery converts the result set of the provided SQL template into a JSON array, where each row of the result set is represented as a JSON object within the array. This can be useful for applications that expect data in JSON format or for easier data manipulation and transmission in modern web development contexts.


                                                                                              this is further calling calling template
                                                                                              
                                                                                                def template(self,*args):
                                                                                                  pathing = list((app.root_path,'db','sql',) + args)
                                                                                                  pathing[-1] = pathing[-1] + ".sql"
                                                                                              
                                                                                                  template_path = os.path.join(*pathing)
                                                                                              
                                                                                                  green = '\033[92m'
                                                                                                  no_color = '\033[0m'
                                                                                                  print("\n")
                                                                                                  print(f'{green} Load SQL Template: {template_path} {no_color}')
                                                                                              
                                                                                                  with open(template_path, 'r') as f:
                                                                                                    template_content = f.read()
                                                                                                  return template_content
                                                                                              
                                                                                              Now what this template do when called?
                                                                                              
                                                                                              It constructs a file path by concatenating app.root_path, 'db', 'sql', and the arguments provided (args). These are converted to a list and then combined.
                                                                                              It appends the file extension .sql to the last element of the pathing list.
                                                                                              It joins the elements of the pathing list to form the complete file path using os.path.join().
                                                                                              It prints a message indicating the SQL template file being loaded.
                                                                                              It opens the file specified by template_path in read mode and reads its contents into the template_content variable.
                                                                                              Finally, it returns the content of the SQL template file.



  my_user    = next((item for item in users if item["handle"] == 'andrewbrown'), None)
  other_user = next((item for item in users if item["handle"] == 'bayko'), None)
  results = {
    'my_user': my_user,
    'other_user': other_user
  }
  print('get_user_uuids')
  print(results)
  return results

#This code searches for users with handles 'andrewbrown' and 'bayko' in the list users, creates a dictionary named results with the found user information, prints the dictionary, and finally returns it.





def create_message_group(client,message_group_uuid, my_user_uuid, last_message_at=None, message=None, other_user_uuid=None, other_user_display_name=None, other_user_handle=None):
  table_name = 'cruddur-messages'
  record = {
    'pk':   {'S': f"GRP#{my_user_uuid}"},
    'sk':   {'S': last_message_at},
    'message_group_uuid': {'S': message_group_uuid},
    'message':  {'S': message},
    'user_uuid': {'S': other_user_uuid},
    'user_display_name': {'S': other_user_display_name},
    'user_handle': {'S': other_user_handle}
  }

  response = client.put_item(
    TableName=table_name,
    Item=record
  )
  print(response)

#Put Item Operation: The client.put_item() method is used to insert the record into the DynamoDB table specified by table_name. It takes the table name and the record dictionary as parameters.



def create_message(client,message_group_uuid, created_at, message, my_user_uuid, my_user_display_name, my_user_handle):
  table_name = 'cruddur-messages'
  record = {
    'pk':   {'S': f"MSG#{message_group_uuid}"},
    'sk':   {'S': created_at },
    'message_uuid': { 'S': str(uuid.uuid4()) },
    'message': {'S': message},
    'user_uuid': {'S': my_user_uuid},
    'user_display_name': {'S': my_user_display_name},
    'user_handle': {'S': my_user_handle}
  }
  # insert the record into the table
  response = client.put_item(
    TableName=table_name,
    Item=record
  )
  # print the response
  print(response)

message_group_uuid = "5ae290ed-55d1-47a0-bc6d-fe2bc2700399" 
now = datetime.now(timezone.utc).astimezone()
users = get_user_uuids()


create_message_group(
  client=ddb,
  message_group_uuid=message_group_uuid,
  my_user_uuid=users['my_user']['uuid'],
  other_user_uuid=users['other_user']['uuid'],
  other_user_handle=users['other_user']['handle'],
  other_user_display_name=users['other_user']['display_name'],
  last_message_at=now.isoformat(),
  message="this is a filler message"
)

create_message_group(
  client=ddb,
  message_group_uuid=message_group_uuid,
  my_user_uuid=users['other_user']['uuid'],
  other_user_uuid=users['my_user']['uuid'],
  other_user_handle=users['my_user']['handle'],
  other_user_display_name=users['my_user']['display_name'],
  last_message_at=now.isoformat(),
  message="this is a filler message"
)

conversation = """
Person 1: Have you ever watched Babylon 5? It's one of my favorite TV shows!
Person 2: Yes, I have! I love it too. What's your favorite season?
Person 1: I think my favorite season has to be season 3. So many great episodes, like "Severed Dreams" and "War Without End."
Person 2: Yeah, season 3 was amazing! I also loved season 4, especially with the Shadow War heating up and the introduction of the White Star.
Person 1: Agreed, season 4 was really great as well. I was so glad they got to wrap up the storylines with the Shadows and the Vorlons in that season.
Person 2: Definitely. What about your favorite character? Mine is probably Londo Mollari.

"""


lines = conversation.lstrip('\n').rstrip('\n').split('\n')
for i in range(len(lines)):
  if lines[i].startswith('Person 1: '):
    key = 'my_user'
    message = lines[i].replace('Person 1: ', '')
  elif lines[i].startswith('Person 2: '):
    key = 'other_user'
    message = lines[i].replace('Person 2: ', '')
  else:
    print(lines[i])
    raise 'invalid line'

  created_at = (now + timedelta(minutes=i)).isoformat()
  create_message(
    client=ddb,
    message_group_uuid=message_group_uuid,
    created_at=created_at,
    message=message,
    my_user_uuid=users[key]['uuid'],
    my_user_display_name=users[key]['display_name'],
    my_user_handle=users[key]['handle']
  )
```


  

![Seeding](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/3f48da00-c3f7-41f5-a78a-5834b33d366a)
  
  
- Ran schema-load
- Created scan and set it for local DynamoDB only, as doing a scan in production can be expensive.
  
- Created new folder in ddb named patterns, then created 2 new files: get-conversation and list-conversations.

> These allow us to begin implementing our access patterns. We first complete get-conversation, make it executable, then run it. This is similar to a scan, but
>  we’re returning information that we queried and limiting the results. In list-conversations, we began another our of access patterns. Andrew goes through
>  explaining the information we’re querying here as well, then we test. While testing, we go back to db.py in backend-flask/lib and update all instances of
>  print_sql to pass the params we set while refining our queries for mock data.


Get converstaion:
```
#!/usr/bin/env python3

import boto3
import sys
import json
import os

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..', '..'))
sys.path.append(parent_path)
from lib.db import db

attrs = {
  'endpoint_url': 'http://localhost:8000'
}

if len(sys.argv) == 2:
  if "prod" in sys.argv[1]:
    attrs = {}

dynamodb = boto3.client('dynamodb',**attrs)
table_name = 'cruddur-messages'

def get_my_user_uuid():
  sql = """
    SELECT 
      users.uuid
    FROM users
    WHERE
      users.handle =%(handle)s
  """
  uuid = db.query_value(sql,{
    'handle':  'andrewbrown'
  })
  return uuid

my_user_uuid = get_my_user_uuid()
print(f"my-uuid: {my_user_uuid}")
year = str(datetime.now().year)
# define the query parameters
query_params = {
  'TableName': table_name,
  'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',
  'ScanIndexForward': False,
  'ExpressionAttributeValues': {
    ':year': {'S': year },
    ':pk': {'S': f"GRP#{my_user_uuid}"}
  },
  'ReturnConsumedCapacity': 'TOTAL'
}

# query the table
response = dynamodb.query(**query_params)

# print the items returned by the query
print(json.dumps(response, sort_keys=True, indent=2))
```


The function that is used in the above get-converstations script to fetch the user.uuid:
```
def query_value(self, sql, params={}):
    self.print_sql('value', sql, params)
    with self.pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            result = cur.fetchone()
            return result[0]

```



List-tables script:
The code is similar to get-converstaions so just writing the query

```
query_params = {
  'TableName': table_name,
  'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',
  'ScanIndexForward': False,
  'ExpressionAttributeValues': {
    ':year': {'S': year },
    ':pk': {'S': f"GRP#{my_user_uuid}"}
  },
  'ReturnConsumedCapacity': 'TOTAL'
}

# query the table 
response = dynamodb.query(**query_params)

# print the items returned by the query
print(json.dumps(response, sort_keys=True, indent=2))
```



In DynamoDB, each item's partition key (pk) must be unique within the table. Unlike the sort key (sk), which can have duplicate values within a partition key, the partition key itself must be unique across all items in the table.  


  
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


```
import boto3
import sys
from datetime import datetime, timedelta, timezone
import uuid
import os
import botocore.exceptions

class Ddb:                                            
  def client():
    endpoint_url = os.getenv("AWS_ENDPOINT_URL")
    if endpoint_url:
      attrs = { 'endpoint_url': endpoint_url }
    else:
      attrs = {}
    dynamodb = boto3.client('dynamodb',**attrs)
    return dynamodb

  def list_message_groups(client,my_user_uuid):
    year = str(datetime.now().year)
    table_name = 'cruddur-messages'
    query_params = {
      'TableName': table_name,
      'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',
      'ScanIndexForward': False,
      'Limit': 20,
      'ExpressionAttributeValues': {
        ':year': {'S': year },
        ':pk': {'S': f"GRP#{my_user_uuid}"}
      }
    }
    print('query-params:',query_params)
    print(query_params)
    # query the table
    response = client.query(**query_params)
    items = response['Items']
    

    results = []
    for item in items:
      last_sent_at = item['sk']['S']
      results.append({
        'uuid': item['message_group_uuid']['S'],
        'display_name': item['user_display_name']['S'],
        'handle': item['user_handle']['S'],
        'message': item['message']['S'],
        'created_at': last_sent_at
      })
    return results
  def list_messages(client,message_group_uuid):
    year = str(datetime.now().year)
    table_name = 'cruddur-messages'
    query_params = {
      'TableName': table_name,
      'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',
      'ScanIndexForward': False,
      'Limit': 20,
      'ExpressionAttributeValues': {
        ':year': {'S': year },
        ':pk': {'S': f"MSG#{message_group_uuid}"}
      }
    }

    response = client.query(**query_params)
    items = response['Items']
    items.reverse()
    results = []
    for item in items:
      created_at = item['sk']['S']
      results.append({
        'uuid': item['message_uuid']['S'],
        'display_name': item['user_display_name']['S'],
        'handle': item['user_handle']['S'],
        'message': item['message']['S'],
        'created_at': created_at
      })
    return results
  def create_message(client,message_group_uuid, message, my_user_uuid, my_user_display_name, my_user_handle):
    now = datetime.now(timezone.utc).astimezone().isoformat()
    created_at = now
    message_uuid = str(uuid.uuid4())

    record = {
      'pk':   {'S': f"MSG#{message_group_uuid}"},
      'sk':   {'S': created_at },
      'message': {'S': message},
      'message_uuid': {'S': message_uuid},
      'user_uuid': {'S': my_user_uuid},
      'user_display_name': {'S': my_user_display_name},
      'user_handle': {'S': my_user_handle}
    }
    # insert the record into the table
    table_name = 'cruddur-messages'
    response = client.put_item(
      TableName=table_name,
      Item=record
    )
    # print the response
    print(response)
    return {
      'message_group_uuid': message_group_uuid,
      'uuid': my_user_uuid,
      'display_name': my_user_display_name,
      'handle':  my_user_handle,
      'message': message,
      'created_at': created_at
    }
  def create_message_group(client, message,my_user_uuid, my_user_display_name, my_user_handle, other_user_uuid, other_user_display_name, other_user_handle):
    print('== create_message_group.1')
    table_name = 'cruddur-messages'

    message_group_uuid = str(uuid.uuid4())
    message_uuid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).astimezone().isoformat()
    last_message_at = now
    created_at = now
    print('== create_message_group.2')

    my_message_group = {
      'pk': {'S': f"GRP#{my_user_uuid}"},
      'sk': {'S': last_message_at},
      'message_group_uuid': {'S': message_group_uuid},
      'message': {'S': message},
      'user_uuid': {'S': other_user_uuid},
      'user_display_name': {'S': other_user_display_name},
      'user_handle':  {'S': other_user_handle}
    }

    print('== create_message_group.3')
    other_message_group = {
      'pk': {'S': f"GRP#{other_user_uuid}"},
      'sk': {'S': last_message_at},
      'message_group_uuid': {'S': message_group_uuid},
      'message': {'S': message},
      'user_uuid': {'S': my_user_uuid},
      'user_display_name': {'S': my_user_display_name},
      'user_handle':  {'S': my_user_handle}
    }

    print('== create_message_group.4')
    message = {
      'pk':   {'S': f"MSG#{message_group_uuid}"},
      'sk':   {'S': created_at },
      'message': {'S': message},
      'message_uuid': {'S': message_uuid},
      'user_uuid': {'S': my_user_uuid},
      'user_display_name': {'S': my_user_display_name},
      'user_handle': {'S': my_user_handle}
    }

    items = {
      table_name: [
        {'PutRequest': {'Item': my_message_group}},
        {'PutRequest': {'Item': other_message_group}},
        {'PutRequest': {'Item': message}}
      ]
    }

    try:
      print('== create_message_group.try')
      # Begin the transaction
      response = client.batch_write_item(RequestItems=items)
      return {
        'message_group_uuid': message_group_uuid
      }
    except botocore.exceptions.ClientError as e:
      print('== create_message_group.error')
      print(e)
```


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

```
#!/usr/bin/env python3

import boto3
import os
import json

userpool_id = os.getenv("AWS_COGNITO_USER_POOL_ID")
client = boto3.client('cognito-idp')
params = {
  'UserPoolId': userpool_id,
  'AttributesToGet': [
      'preferred_username',
      'sub'
  ]
}
response = client.list_users(**params)
users = response['Users']

print(json.dumps(users, sort_keys=True, indent=2, default=str))

dict_users = {}
for user in users:
  attrs = user['Attributes']
  sub    = next((a for a in attrs if a["Name"] == 'sub'), None)
  handle = next((a for a in attrs if a["Name"] == 'preferred_username'), None)
  dict_users[handle['Value']] = sub['Value']

print(json.dumps(dict_users, sort_keys=True, indent=2, default=str))
```

  
- Updated AWS_COGNITO_USER_POOL_ID in docker-compose.yml to use the variable that was saved. Ran the file for list-users.
  ![list-users](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/47f263e7-47f7-4e0a-bf00-09ce9ce9634b)
  
  
- Under bin/db created update_cognito_user_ids.

```



#!/usr/bin/env python3

import boto3
import os
import sys

print("== db-update-cognito-user-ids")

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..'))
sys.path.append(parent_path)
from lib.db import db

def update_users_with_cognito_user_id(handle,sub):
  sql = """
    UPDATE public.users
    SET cognito_user_id = %(sub)s
    WHERE
      users.handle = %(handle)s;
  """

  db.query_commit(sql,{          -------> this function is taking the above sql which updates the cognito_user_id in users table
    'handle' : handle,
    'sub' : sub
  })
                                                                                                                                      def query_commit(self,sql,params={}):
                                                                                                                                        self.print_sql('commit with returning',sql,params)
                                                                                                                                      
                                                                                                                                        pattern = r"\bRETURNING\b"
                                                                                                                                        is_returning_id = re.search(pattern, sql)
                                                                                                                                      
                                                                                                                                        try:
                                                                                                                                          with self.pool.connection() as conn:
                                                                                                                                            cur =  conn.cursor()
                                                                                                                                            cur.execute(sql,params)
                                                                                                                                            if is_returning_id:
                                                                                                                                              returning_id = cur.fetchone()[0]
                                                                                                                                            conn.commit() 
                                                                                                                                            if is_returning_id:
                                                                                                                                              return returning_id
                                                                                                                                        except Exception as err:
                                                                                                                                          self.print_sql_err(err)
The query in this case doesn't contain a RETURNING clause, so the is_returning_id variable will be None, and the code won't fetch any ID after executing this query. It simply updates records in the public.users table based on the provided parameters (sub and handle).


                                                                                              
def get_cognito_user_ids():
  userpool_id = os.getenv("AWS_COGNITO_USER_POOL_ID")

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cognito-idp/client/list_users.html

  client = boto3.client('cognito-idp')
  params = {
    'UserPoolId': userpool_id,
    'AttributesToGet': [
        'preferred_username',
        'sub'
    ]
  }
  response = client.list_users(**params)              ** is used when passing number of arguments

  users = response['Users']
  dict_users = {}
  for user in users:
    attrs = user['Attributes']
    sub    = next((a for a in attrs if a["Name"] == 'sub'), None)
    handle = next((a for a in attrs if a["Name"] == 'preferred_username'), None)
    dict_users[handle['Value']] = sub['Value']
  return dict_users


users = get_cognito_user_ids()

for handle, sub in users.items():
  print('----',handle,sub)
  update_users_with_cognito_user_id(
    handle=handle,
    sub=sub
  )



```
> The sql command is updating our public.users table setting the cognito user id based on the sub we passed in. We then run a query commit to execute it. Further 
> down in the code, we’re doing the same thing that we did in list-users, but instead of printing the data, we’re returning it. Before we can do that, we have to 
> seed our data. We add a path to our setup file for update_cognito_user_ids. We run ./bin/db/setup, but get an error on that path, so instead we run 
> update_cognito_user_ids after running db/setup. We’re not returning the information we wanted, so we access db.py and find our query_commit definition. We were 
> missing params from being passed, so we added it, then back in terminal ran the script again. This time, it returned the information we wanted.
  
![update-users-in-db](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/d8f065be-459c-4e14-9960-b7cc95c2ce85)

  
  
We then edited our definition of data_message_groups in app.py by using some code from our /api/activities/home route. 

```
@app.route("/api/message_groups", methods=['GET'])   #This line of code decorates the data_message_groups function with a Flask route. It specifies that the function should be called when a GET request is made to the "/api/message_groups" URL.
def data_message_groups():
  access_token = extract_access_token(request.headers)        #Here, the code calls a function extract_access_token() to retrieve the access token from the headers of the incoming request.


                                                                                       def extract_access_token(request_headers):
                                                                                          access_token = None    #This line initializes the variable access_token to None. This variable will be used to store the access token extracted from the Authorization header.
                                                                                          auth_header = request_headers.get("Authorization")  #This line retrieves the value of the "Authorization" header from the request_headers dictionary using the get() method. If the "Authorization" header is not present in request_headers, auth_header will be None.
                                                                                          if auth_header and " " in auth_header:
                                                                                              _, access_token = auth_header.split()
                                                                                          return access_token






  try:
    claims = cognito_jwt_token.verify(access_token)    #This part attempts to verify the extracted access token using a method verify() provided by cognito_jwt_token

                                                                                                                def verify(self, token, current_time=None):
                                                                                                                    """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
                                                                                                                    if not token:
                                                                                                                        raise TokenVerifyError("No token provided")
                                                                                                            
                                                                                                                    headers = self._extract_headers(token)
                                                                                                                    pkey_data = self._find_pkey(headers)
                                                                                                                    self._verify_signature(token, pkey_data)
                                                                                                            
                                                                                                                    claims = self._extract_claims(token)
                                                                                                                    self._check_expiration(claims, current_time)
                                                                                                                    self._check_audience(claims)
                                                                                                            
                                                                                                                    self.claims = claims 
                                                                                                                    return claims

    # authenicatied request
    app.logger.debug("authenicated")
    app.logger.debug(claims)
    cognito_user_id = claims['sub']    #If the request is authenticated, the user's cognito user ID is extracted from the claims.
    model = MessageGroups.run(cognito_user_id=cognito_user_id)



                                                                                          from datetime import datetime, timedelta, timezone
                                                                                          
                                                                                          from lib.ddb import Ddb
                                                                                          from lib.db import db
                                                                                          
                                                                                          class MessageGroups:
                                                                                            def run(cognito_user_id):
                                                                                              model = {
                                                                                                'errors': None,
                                                                                                'data': None
                                                                                              }
                                                                                          
                                                                                              sql = db.template('users','uuid_from_cognito_user_id')
                                                                                                                                                                SELECT
                                                                                                                                                                  users.uuid
                                                                                                                                                                FROM public.users
                                                                                                                                                                WHERE 
                                                                                                                                                                  users.cognito_user_id = %(cognito_user_id)s
                                                                                                                                                                LIMIT 1



                                                                                              my_user_uuid = db.query_value(sql,{
                                                                                                'cognito_user_id': cognito_user_id
                                                                                              })


                                                                                                                                    
                                                                                          
                                                                                              print(f"UUID: {my_user_uuid}")
                                                                                          
                                                                                              ddb = Ddb.client()
                                                                                              data = Ddb.list_message_groups(ddb, my_user_uuid)  #It calls the list_message_groups method of the Ddb class instance to retrieve the message groups associated with the user's UUID from DynamoDB.
                                                                                              print("list_message_groups:",data)
                                                                                          
                                                                                              model['data'] = data
                                                                                              return model






    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    return {}, 401
```


>This route (/api/message_groups) returns data about message groups. When accessed, it verifies the provided access token to confirm the user's identity. If >authenticated, it retrieves message group data associated with the user from the backend. If there are no errors, it returns the message group data; otherwise, it
>returns an error status code.
   
After this, we next moved on to replace the mock data we had in message_groups.py and replaced it with a query to our Dynamo DB.

```
from datetime import datetime, timedelta, timezone
from lib.ddb import Ddb
from lib.db import db

class Messages:
  def run(message_group_uuid,cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }

    sql = db.template('users','uuid_from_cognito_user_id')
    my_user_uuid = db.query_value(sql,{
      'cognito_user_id': cognito_user_id
    })

    print(f"UUID: {my_user_uuid}")

    ddb = Ddb.client()
    data = Ddb.list_messages(ddb, message_group_uuid)
    print("list_messages")
    print(data)

    model['data'] = data
```

> When its run method is called with a cognito_user_id, it retrieves the user's UUID using a SQL query. Then, it uses a DynamoDB client to list message groups
> associated with that UUID. The retrieved data is stored in a model dictionary, which is then returned.
  
For this, we created a new folder inside backend-flask/db/sql named users, then a new SQL file named uuid_from_handle.sql.   




After this, we updated HomeFeedPage.js, MessageGroupsPage.js, MessageGroupPage.js, and MessageForm.js to include authorization headers we just created. 

```
import { Auth } from 'aws-amplify'; #The Auth object provides methods for authentication and user management in AWS Amplify applications.

const checkAuth = async (setUser) => {          #This code defines an asynchronous function named checkAuth. It takes one parameter, setUser, which appears to be a function used to set user data

  Auth.currentAuthenticatedUser({               #This code calls the currentAuthenticatedUser method of the Auth object with an optional parameter bypassCache set to false. This parameter specifies whether to bypass the local cache and fetch the latest user data from Cognito.

    // Optional, By default is false. 
    // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {                            #This code handles the promise returned by currentAuthenticatedUser method. If the promise is resolved successfully, it logs the user object to the console and then calls currentAuthenticatedUser again without any parameters.
    console.log('user',user);

    return Auth.currentAuthenticatedUser()   #This code handles the promise returned by the second call to currentAuthenticatedUser. If successful, it sets the user data by calling the setUser function with an object containing display_name and handle properties extracted from the cognito_user object.

  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));          #This code handles any errors that occur during the promise chain and logs them to the console.
};

export default checkAuth;
```



 In summary, this code defines a function checkAuth that checks if a user is authenticated using AWS Cognito. If the user is authenticated, it retrieves user data and sets it using the provided setUser function. Any errors encountered during this process are logged to the console.

  
Moving on we pulled CheckAuth and defined it in it’s own file, frontend-react-js/src/lib/CheckAuth.js.
- It asynchronously checks if a user is authenticated using AWS Cognito's Amplify library.
- Upon successful authentication, it retrieves the user's attributes, such as name and preferred username.
- It sets the user's attributes using a provided function to update the application's state.
- Inside the checkAuth function, if the user is successfully authenticated, it updates the user state using the setUser function. It sets the display_name and handle attributes based on the user's attributes retrieved from Cognito.


  
We updated our HomeFeedPage.js, MessageGroupsPage.js, MessageGroupPage.js, and MessageForm.js to use setUser, which we defined in CheckAuth.

  
>The setUser function is a state updater function provided by React's useState hook. In the context of the HomePage component, setUser is responsible for updating the user state variable.
  
- Add our AWS_ENDPOINT_URL variable to our docker-compose.yml file.


![AWS_ENDPOINT_URL](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/f8bfb9ae-0eab-4003-a651-16dae393b9d9)

- Updated App.js for our path for the MessageGroupPage. Instead of going to a static @:handle, it’s now dependent upon the message_group_uuid.
  
![messagegrouppage](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/8df4378d-e622-434a-b772-fea69df113f6)
  
Updated this in our MessageGroupPage.js file.




>We next moved onto making our message group definition a little more strict. In ddb.py, we updated the KeyConditionExpression with what we listed in our 
>get-converstation.py file. We removed the hardcoded value of the year, and instead passed datetime.now()year as year. This failed, so we ended up having to put >the value into a string, like so: year = str(datetime.now().year). We moved onto updating the same value in list-conversations.py as well.

```
my_user_uuid = get_my_user_uuid()
print(f"my-uuid: {my_user_uuid}")
year = str(datetime.now().year)      ----------> earlier this was fixed value
# define the query parameters
query_params = {
  'TableName': table_name,
  'KeyConditionExpression': 'pk = :pk AND begins_with(sk,:year)',
  'ScanIndexForward': False,
  'ExpressionAttributeValues': {
    ':year': {'S': year },
    ':pk': {'S': f"GRP#{my_user_uuid}"}
  },
  'ReturnConsumedCapacity': 'TOTAL'
```


> After refreshing, the data is again showing in the Messages section, but it’s listing the @handle as the page. We go into our MessageGroupItem.js file and pass out message_group_uuix> for /messages/. We also needed to update our const classes to pass the message_group_uuid as well. A quick refresh to our web app, and there’s no errors, but the >messages are not displaying. Andrew notes this is because it’s part of the query we need on the MessageGroupPage.js. We check our const loadMessageGroupData, and >it’s already passing the message_group_uuid. We need to start implementing this into our backend.

```

  const classes = () => {
    let classes = ["message_group_item"];
    if (params.message_group_uuid == props.message_group.uuid){        ------> Earlier it was handle here
      classes.push('active')
    }
    return classes.join(' ');
  }

  return (
    <Link className={classes()} to={`/messages/`+props.message_group.uuid}>
      <div className='message_group_avatar'></div>
      <div className='message_content'>
        <div classsName='message_group_meta'>
```


  
In app.py, we remove the hardcoding of user_sender_handle and update our def data_messages to pass message_group_uuid as well. 

We then updated this again, this time checking for cognito_user_id and message_group_uuid. In messages.py, we updated the code to pass in the message_group_uuid called client, then it will list messages. In ddb.py, we add define a function for list_messages passing client and the message_group_uuid as well.
  
We previously added code to get the cognito_user_id in message_groups.py, so we add this code to messages.py as well. This is not being used now, but it’s for permissions checks we will implement later.
    
The mock messages however, are in the wrong order. To fix this, we had to reverse the items in our code. In ddb.py, we added items.reverse() to our code, then from did the same from our ddb/patterns/get-conversations file as well. For our conversations, we need to be able to differentiate between starting a new conversation and contiuing an existing one. To do this, we added a conditional if statement with an else passing along either the handle (new conversation) or message_group_uuid(existing conversation).
  
  
In app.py, we need to adjust what we have for a create function. Under the definition for data_create_message, we again remove the hardcoding for the user_handle, then pass the same code we previously passed, this time passing the message, message_group_uuid, cognito_user_id, and the user_receiver_handle.
  
  
We also needed to update our variables for message_group_uuid and user_receiver_handle to request.json and get the message_group_uuid and handle. 
  
Additionally we added an if else statement indicating if the message_group_uuid is None, we’re creating a new message. If it is not, we’re doing an update. Essentially similar to what we did earlier in ddb.py. Since we’re still working on existing messages, we comment out the create elif statement for now.
  
Back in ddb.py, we update our code to define our create_message function here as well. It will generate the uuid for us, since DynamoDB cannot by itself, it will create a record with message_group_uuid, message, message_uuid, amongst more information.


When we refresh our web app again, we’re not getting errors from the backend logs, but upon using Inspect from our browser, it’s giving TypeError: Cannot set property json of Object which has only a getter.


We jump back over create_message.py and find we have a template added that we need to create.

We go into backend-flask/db/sql/users directory and create create_message_users.sql.

```
SELECT -- Select statement to retrieve data
  users.uuid, -- Selecting the UUID column from the users table
  users.display_name, -- Selecting the display_name column from the users table
  users.handle, -- Selecting the handle column from the users table
  CASE users.cognito_user_id = %(cognito_user_id)s -- Conditional check on cognito_user_id
  WHEN TRUE THEN -- If the condition is true, set the result as 'sender'
    'sender'
  WHEN FALSE THEN -- If the condition is false, set the result as 'recv'
    'recv'
  ELSE -- If neither of the above conditions are met, set the result as 'other'
    'other'
  END as kind -- Assigning the result of the CASE statement to a column named 'kind'
FROM public.users -- Selecting data from the public schema's users table
WHERE
  users.cognito_user_id = %(cognito_user_id)s -- Filtering rows where cognito_user_id matches the provided parameter
  OR 
  users.handle = %(user_receiver_handle)s -- Or filtering rows where handle matches the provided parameter

```

When we refresh our web app this time, it will now post messages(data) correctly.


Now that that is working as intended, we now go back and focus on creating a new conversation.

  
In frontend-react, we navigate to src/App.js and add a new path for a new page, MessageGroupNewPage.
We then add the import to the top of the page as well. 

We then move over to src/pages and create the new page, MessageGroupNewPage.js. In this page, we import {CheckAuth}, then remove the function and pass our setUser. 

We then create a 3rd mock user for our database to our seed.sql file in backend-flask/db. So we don’t have to compose down our environment and then compose it back up, instead we pass the SQL query locally through the terminal after connecting to our Postgres db using ./bin/db/connect, then running our query of manually.


In app.py we define a new function data_users_short passing in the handle. We need to create a new service for this. In backend-flask/services we create a new one, users_short.py.

```
from lib.db import db

class UsersShort:
  def run(handle):
    sql = db.template('users','short')
    results = db.query_object_json(sql,{
      'handle': handle
    })
    return results
```

We then go into our sql/users and create a new file called short.sql.

```
SELECT
  users.uuid,
  users.handle,
  users.display_name
FROM public.users
WHERE 
  users.handle = %(handle)s
```



MessageGroupItem.js - This component is meant to render a single message group item with its details and provide a link to navigate to the message group's detailed view. Additionally, it formats the time of creation in a human-readable format.

Also in frontend-react/components we create MessageGroupNewItem.js. 

MessageGroupNewItem.js. -  this component serves as a UI element for creating a new message group, providing a link to navigate to a new message creation page with the user's handle included in the URL.




We also have to go back and update MessageGroupFeed.js. - MessageGroupFeed component is responsible for rendering a feed of message groups. It displays a heading, possibly for a messaging section, and then renders a list of existing message groups using MessageGroupItem components. Additionally, if provided with props.otherUser, it renders a special MessageGroupNewItem component, presumably for creating a new message group.


A refresh of our web app, and we have another conversation. 

In MessageForm.js, we add a conditional to create messages and then we uncomment the lines of code we previously commented out in create_message.py to imlement it. 

MessageForm.js encapsulates the logic for sending messages within the application, handling user input, form submission, and interaction with the backend API, while also providing basic error handling and styling.

In ddb.py, we then define the create_message_group function utilizing batch write and import botocore.exceptions as well.


  ![prod-ddb-table](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/f8fe974d-58ec-4daa-86ca-0ee7dda61699)



- Need to create a Dynamo DB Stream trigger so as to update the message groups.
- To start this, we ran ./bin/ddb/schema-load prod. We then logged into AWS and checked DynamoDB to see our new table.



We next needed to turn on streaming through the console. To do this, we went to Tables > Exports and streams > Turn on. We finalized this by selecting New Image.

  ![Screenshot 2024-01-22 220506](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/44e5fc6b-ed98-434d-8a23-e9aed2a57b05)



When your Lambda function is running within a VPC and needs to access DynamoDB, you still require a VPC endpoint called "DynamoDB VPC Endpoint" or "Gateway Endpoint" to enable communication between the Lambda function and DynamoDB. This is because the Lambda function within the VPC is isolated from the public internet, and the VPC endpoint provides a secure and direct connection to DynamoDB without needing to route traffic through the internet gateway.

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

This Lambda function is triggered whenever a new message is sent or updated in the DynamoDB table cruddur-messages. Let's break down how this function works and how it interacts with the table based on the provided schema:

Event Data Extraction:

The Lambda function receives an event containing information about the change that triggered it.
It extracts relevant data such as the event name (eventName), partition key (pk), sort key (sk), and message content (message) from the event.
Event Name Validation:

The function checks if the event name is 'REMOVE'. If it is, it skips processing because it indicates that a message is being deleted.
Message Group Identification:

If the event corresponds to a message (pk starts with 'MSG#'), the function identifies the message group UUID (group_uuid) by extracting it from the partition key (pk).
It retrieves the message content (message) from the event.
Querying Message Group Rows:

The function queries the DynamoDB table (cruddur-messages) using the message group UUID (group_uuid) to retrieve all rows associated with the message group.
It queries the table using the global secondary index (message-group-sk-index), which is indexed by message_group_uuid.
Updating Message Group Rows:

For each row retrieved, the function deletes the existing row and recreates it with the updated sort key (sk) value.
The updated row contains the same partition key (pk) and message group UUID (message_group_uuid) but with the new sort key (sk) and updated message content (message).
Logging and Error Handling:

The function logs the details of the operation performed (deletion and creation of rows) for debugging purposes.
Any errors encountered during the process are logged for troubleshooting.
Interaction with the Table:

When a new message is sent or updated, the Lambda function ensures that all rows associated with the message group are updated with the latest message content and sorted according to the new timestamp (sk).
It achieves this by querying the table using the message group UUID, deleting existing rows, and recreating them with the updated information.
This process ensures that the table remains consistent and up-to-date with the latest messages for each conversation.
In the context of the previously drawn table schema, this Lambda function effectively manages the update of messages within a conversation, ensuring that the table reflects the latest message content and maintains the correct chronological order of messages.





DynamoDB does not allow you to directly update the sort key of an existing item. Therefore, if you want to change the sort key of a message within a message group (for example, to reflect a new timestamp), you must delete the existing item and insert a new one with the updated sort key. This is likely why the code deletes and re-adds messages within the group.  

Overview

The Lambda function is designed to update the position of a message within a message group that already exists in the DynamoDB table.

 Existing Message Group

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

![Screenshot 2024-01-28 042331](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/04e8a92b-bdd6-4879-a685-54fefaf3a762)



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






