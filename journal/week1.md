# week01


Created an openapi-3.0.yml file as a standard for defining APIs. 
The API is providing us with mock data
  
[openapi yml file](../backend-flask/openapi-3.0.yml)
  

Added the section for notifications in openapi-3.0.yml document

```yml
  /api/activities/notifications:
    get:
      description: 'Return a feed of activity for all of those that I follow'
      tags:
        - activities
      parameters: []
      responses:
        '200':
          description: Returns an array of activities
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Activity'
```

  
  

To create a Flask Backend Endpoint for Notifications, added the following in app.py:
  
```
from services.notifications_activities import *
```
> In Python, when you import a module using the asterisk * notation, it means that you are importing all the names (functions, classes, variables) defined in that module into the current namespace.

    
```py
@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities.run()
  return data, 200
```
>This Flask route handles GET requests to "/api/activities/notifications" by calling the run() method of the NotificationsActivities class and returning its result with a status code of 200.
  
  
```
from datetime import datetime, timedelta, timezone
class NotificationsActivities:
  def run():
    now = datetime.now(timezone.utc).astimezone()
    results = [{
      'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
      'handle':  'coco',
      'message': 'I am white unicorn',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'likes_count': 5,
      'replies_count': 1,
      'reposts_count': 0,
      'replies': [{
        'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
        'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Worf',
        'message': 'This post has no honor!',
        'likes_count': 0,
        'replies_count': 0,
        'reposts_count': 0,
        'created_at': (now - timedelta(days=2)).isoformat()
      }],
    },
    ]
    return results
```
   
>The run() method within the NotificationsActivities class generates dummy notification data, encapsulating each notification as a dictionary within a list, and returns this list.

  

  
For frontend, to implement the notifications accessed app.js and added the following:

  
```
import NotificationsFeedPage from './pages/NotificationsFeedPage';
```
> This line of code imports the NotificationsFeedPage component from the file located at './pages/NotificationsFeedPage' in the project directory.

  
  
```
  {
    path: "/notifications",
    element: <NotificationsFeedPage />
  },
```
> These lines define a route configuration object where the path "/notifications" is mapped to render the NotificationsFeedPage component when accessed.
    
    
Then under pages, we created the pages NotificationsFeedPage.js and NotificationsFeedPage.css.
  
[notificationfeedpage.js](../frontend-react-js/src/pages/NotificationsFeedPage.js)
[notificationfeedpage.css](../frontend-react-js/src/pages/NotificationsFeedPage.css)
  
Used the HomeFeedPage.js and  editing it to reflect the notification page:
  
> This React component represents a page for displaying notifications. It fetches notification data from a backend API upon rendering and checks user authentication using cookies. It renders a desktop navigation bar, content area containing forms for adding activities and replies, and an activity feed displaying notifications. The sidebar displays user information.

     
        
Added DynamoDB local and Postgres local configuration in Docker-compose.yml file:
  


# For Postgres

```
services:
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data
```
  
# For Dynamodb
  
```yml
services:
  dynamodb-local:
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
```
-  https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
-  We needed to add user:root to get this working.

  
  
Then at the bottom of the docker-compose.yml file, we added the rest of the Postgres code for the volumes:
```
volumes:
  db:
    driver: local
```
  
This wrapped up Week 1 of the bootcamp.
