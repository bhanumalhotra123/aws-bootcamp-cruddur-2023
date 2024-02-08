# week02

This week, learned about Observability. 


Had a guest speaker this week, __Jessica Kerr__, Honeycomb.io Engineering to discuss Honeycomb, observability in general, and best practices when implementing.


Goals:

- implement our backend Flask application to use Open Telemetry (OTEL) with Honeycomb.io as the provider
- run queries to explore traces within Honeycomb
- instrument AWS X-Ray into the backend Flask application
- configure and provision X-Ray daemon within docker-compose.yml and send data back to X-Ray API
- observe X-Ray traces within the AWS console
- integrate Rollbar for error logging
- trigger an error and observe an error with Rollbar
- install Watchtower and write a custom logger to send application log data to AWS CloudWatch group




Honeycomb
Open Telemetry is like a toolbox designed to help developers peek into the inner workings of their cloud-native software. It's all about gathering what we call "telemetry data," which is basically information about how the software is running, what it's doing, and how it's performing.
Now, think of Honeycomb as a big warehouse where you can store and analyze all this telemetry data. It's like having a super-powered magnifying glass that lets you zoom in and examine every tiny detail of your software's behavior.
So, when we say Honeycomb supports Open Telemetry, we mean that it's like saying, "Hey, Honeycomb is ready to work with whatever data Open Telemetry gathers." And because we're setting up Open Telemetry within our system, we can directly send all that juicy telemetry data straight to Honeycomb's doorstep. 
It's like setting up a pipeline from our software's brain to Honeycomb's analytical engine, so we can gain insights and understand exactly what's going on under the hood.



![Honeycomb Charts](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/82c33b29-a159-4aaf-82ab-07d9fc93afc3)
![Honeycomb Queries](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/8c5910a6-49ad-41d0-a4fa-7175e24f5588)
We began by added installation instructions for Open Telemetry by adding the following files to our ‘requirements.txt’:
  
```
opentelemetry-api 
opentelemetry-sdk 
opentelemetry-exporter-otlp-proto-http 
opentelemetry-instrumentation-flask 
opentelemetry-instrumentation-requests
```

Jessica  guided us further through Honeycomb, including accessing our API key. We then ran the export and gp env commands for our HONEYCOMB_API_KEY and our HONEYCOMB_SERVICE_NAME to store the variables in our environment. 
We then installed the dependencies from the console:
```
pip install -r requirements.txt
```


Added the following to ‘backend-flask/app.py’ :

```
# HoneyComb ---------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# HoneyComb -----------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

```



>These lines initialize tracing for Flask and Requests, and set up an exporter to send data to Honeycomb using the OpenTelemetry Protocol (OTLP). The TracerProvider and BatchSpanProcessor manage the tracing process, while get_tracer retrieves the tracer instance. This setup enables capturing and exporting telemetry data to Honeycomb for analysis and monitoring.

```
# Initialize automatic instrumentation with Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```


>These lines initialize Flask's automatic instrumentation and instrumentation for Requests. The FlaskInstrumentor instruments the Flask application, while >RequestsInstrumentor instruments the Requests library for tracing. This setup enables automatic tracing of Flask endpoints and outgoing HTTP requests.


>FlaskInstrumentor primarily focuses on instrumenting Flask itself, capturing data related to incoming requests and outgoing responses within the Flask framework. However, while FlaskInstrumentor can capture some information about outgoing HTTP requests made by the Flask application, it may not provide as detailed or comprehensive telemetry data as RequestsInstrumentor.

>RequestsInstrumentor, on the other hand, is specifically designed to instrument the Requests library, which is commonly used within Flask applications to make outgoing HTTP requests to external services or APIs. RequestsInstrumentor ensures that detailed telemetry data about these outgoing requests, including timing information, headers, and other metadata, is captured accurately.




```
OTEL_SERVICE_NAME: 'bakend-flask'
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
```
  
> When OpenTelemetry initializes, it checks for specific environment variables that follow a naming convention to determine configuration parameters. For example, the OTEL_EXPORTER_OTLP_ENDPOINT environment variable is recognized as the endpoint configuration for the OTLP exporter.

  

```
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


# Show this in the logs within the backend-flask app (STDOUT)
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
```

>OpenTelemetry, a span represents a segment of code execution or a unit of work within an application. Breaking the flow of information into parts, each represented by a span, allows you to track the lifecycle of an operation as it traverses different components and services.
  
>For example, in a distributed system handling an HTTP request, you might have spans representing the processing of the request on the client side, the handling of the request on the server side, interactions with external services like a database, and the generation of the response back to the client. Each of these spans captures information about the corresponding segment of code execution, including timing, contextual details, and any related operations, enabling you to trace the flow of information across the system and understand its behavior and performance.
  
>ConsoleSpanExporter() creates an exporter that sends spans (tracing data) to the console, typically for debugging or development purposes. Spans exported to the console are typically displayed in the terminal or log output.
  
>SimpleSpanProcessor(ConsoleSpanExporter()) creates a simple span processor that forwards spans to the specified exporter (in this case, the console exporter). The simple span processor doesn't batch or buffer spans; it simply sends each span to the exporter immediately after it's finished.
  
>Finally, provider.add_span_processor(processor) adds the span processor to the tracer provider. This ensures that spans collected by the tracer are processed by the simple span processor and exported to the console.



We adjusted our ‘backend-flask/services/home_activities.py’ file to add spans and attributes:
   


```
from datetime import datetime, timedelta, timezone
from opentelemetry import trace

tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run():

    with tracer.start_as_current_span("home-activites-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()      
      span.set_attribute("app.now", now.isoformat())
      results = [{
        'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Andrew Brown',
        'message': 'Cloud is very fun!',
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
      {
        'uuid': '66e12864-8c26-4c3a-9658-95a10f8fea67',
        'handle':  'Worf',
        'message': 'I am out of prune juice',
        'created_at': (now - timedelta(days=7)).isoformat(),
        'expires_at': (now + timedelta(days=9)).isoformat(),
        'likes': 0,
        'replies': []
      },
      {
        'uuid': '248959df-3079-4947-b847-9e0892d1bab4',
        'handle':  'Garek',
        'message': 'My dear doctor, I am just simple tailor',
        'created_at': (now - timedelta(hours=1)).isoformat(),
        'expires_at': (now + timedelta(hours=12)).isoformat(),
        'likes': 0,
        'replies': []
      }
      ]
      span.set_attribute("app.result_length", len(results))   
      return results                ,
```





>The OpenTelemetry instrumentation in your HomeActivities service will capture each span representing the activities within the HomeActivities.run() method.
>These spans are then exported to your Flask application (app.py), which is configured to handle tracing data.
>Your Flask application, being instrumented with OpenTelemetry, will receive these spans and forward them to Honeycomb via the configured exporter (OTLPSpanExporter).
>Once the spans reach Honeycomb, they can be stored, analyzed, and visualized for monitoring and debugging purposes.


>In the code, it's like having a special tool called a "tracer" that helps you write down what happens when you play with your toys. It starts a new page in your notebook called "home-activities-mock-data" and writes down all the fun things you do while playing. It also writes down important details like when you started playing and how many toys you used. This helps you keep track of everything and understand what you did later on.


Configured the ports for the frontend and backend to remain open(public) by adding port information to our gitpod.yml file:

```
ports:
  - name: frontend
    port: 3000
    onOpen: open-browser
    visibility: public
  - name: backend
    port: 4567
    visibility: public
```

  

We added instruction to our ‘gitpod.yml’ file to automatically run npm install from our environment upon start up of the workspace:
  
```
  - name: react-js
    command: |
      cd frontend-react-js
      npm i-
```







# AWS X-RAY
[X-Ray](https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html)
[Docker compose example of X-Ray](https://github.com/marjamis/xray/blob/master/docker-compose.yml)
  
AWS X-Ray is a distributed tracing service that helps developers analyze and debug applications in a distributed environment. It allows you to trace requests made to your application as they travel through various AWS resources and services, helping you identify the root cause of issues and bottlenecks.
  
With X-Ray, you can gain insights into how your application is performing and how it interacts with other AWS resources and services, such as EC2 instances, Lambda functions, API Gateway, and more. X-Ray generates a map of your application’s architecture, showing how different services are connected, and providing real-time visibility into the performance and behavior of your application.
  
X-Ray provides several features to help developers, including:
  
Trace Analysis: X-Ray collects trace data and generates a visual representation of the requests and how they interact with each other. Developers can use this data to identify the cause of issues and optimize the performance of their applications.
  
Service Maps: X-Ray creates a service map that shows how different services in your application are connected and how they interact with each other. This helps you understand the dependencies between different services and optimize their performance.
  
Trace Search: X-Ray allows you to search for traces based on specific criteria, such as service names, request IDs, and annotations. This makes it easy to find traces and troubleshoot issues quickly.
  
Overall, AWS X-Ray is a powerful tool that helps developers gain insights into the behavior and performance of their applications in a distributed environment, allowing them to optimize their application’s performance and quickly resolve any issues that arise.


Added the X-Ray Daemon in compose file:

```
version: "3.8"
services:
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "${AWS_REGION}"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000
```

Environment variables for X-Ray in our ‘docker-compose.yml’ file under backend so that it can communicate to x-ray:
```
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
      AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
```




Setup X-Ray resources. From our ‘aws’ folder, we created a ‘json’ folder, then an ‘xray.json’ file within. We then setup our resources in the file:

```
{
  "SamplingRule": {
      "RuleName": "Cruddur",
      "ResourceARN": "*",
      "Priority": 9000,
      "FixedRate": 0.1,
      "ReservoirSize": 5,
      "ServiceName": "backend-flask",
      "ServiceType": "*",
      "Host": "*",
      "HTTPMethod": "*",
      "URLPath": "*",
      "Version": 1
  }
}


```
>The x-ray.json file contains a sampling rule configuration for AWS X-Ray. Sampling rules define which requests and segments are recorded and sent to X-Ray for analysis.
```
FLASK_ADDRESS="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"$FLASK_ADDRESS\")"
```
>The code sets the Flask address dynamically using environment variables. Then, it creates an AWS X-Ray group named "Cruddur" filtering services based on the Flask address. This allows monitoring and tracing of requests within the Flask application deployed on Gitpod.
  

```
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```
  
We call X-Ray in our ‘backend-flask/app.py’ file:
```
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
```
> The code snippet imports AWS X-Ray SDK for Python, used for distributed tracing in AWS applications. It then integrates X-Ray middleware into a Flask application to automatically trace incoming requests.


  
We must also add instruction for it in ‘requirements.txt’ :
```  
aws-xray-sdk
```
   
We ran ‘pip install -r requirements.txt’ to reinstall Python dependencies, and found again we needed to adjust ‘backend-flask.py’ :
```
  
xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
  
app = Flask(__name__)
  
XRayMiddleware(app, xray_recorder) 
```

>  Dynamically configures the AWS X-Ray recorder for Flask, initializes the Flask app, and then manually adds the X-Ray middleware to enable distributed tracing within the application.


![x-ray-1](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/063c0327-f80d-4e8e-bb82-a8a538efa964)
![x-ray-2](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/4b956eb1-0926-4c4e-86a5-757dc4f83b29)
![x-ray-3](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/7ced7363-5bc5-48c0-9696-62b1e0290ffe)
![x-ray-4](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/521e3eb8-14aa-4d02-862c-dfde8ccb0f2c)


This got X-Ray semi-working. We added segments and subsegments to our [user_activities.py](../backend-flask/services/user_activities.py) file:
```
from aws_xray_sdk.core import xray_recorder

    segment = xray_recorder.begin_segment('user_activities')

    subsegment = xray_recorder.begin_subsegment('mock-data')
    # xray -------
    dict = {
      "now": now.isoformat(),
      "results-size": len(model['data'])   
    }    
    subsegment.put_metadata('key', dict, 'namespace')
```

> A segment named 'user_activities' is initiated for tracing user activities. Within this segment, a subsegment labeled 'mock-data' is started to encapsulate specific operations. Metadata related to the current timestamp and the size of a data model is added to the subsegment for contextual information during distributed tracing.

![x-ray-user-activities](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/8cc108bc-fb2e-482c-abad-6e01c37c06f2)



## Cloudwatch
'
CloudWatch is a monitoring and observability service provided by AWS that enables you to monitor and collect metrics, logs, and events from various resources and services in the AWS cloud environment. It allows you to gain insights into the performance, utilization, and health of your AWS resources and services, and take action to keep them running smoothly.


Added instructions to [requirements.txt](../backend-flask/requirements.txt) :

```
watchtower
```

In  [app.py](../backend-flask/app.py):


```
# Cloudwatch logs ----
import watchtower
import logging
from time import strftime

# Configuring Logger to Use CloudWatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("test log")
```
>The code sets up a logger in Python, configured to log messages to both the console and AWS CloudWatch Logs. It uses the Watchtower library to integrate CloudWatch logging. Finally, it logs a test message using the configured logger, which will be visible in both the console and CloudWatch Logs under the specified log group "cruddur".

```
@app.after_request
def after_request(response):
    timestamp = strftime('[%Y-%b-%d %H:%M]')
    LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    return response
```

>This Flask code snippet defines a function to execute after each request. It logs request details, including timestamp, client IP, HTTP method, scheme, and path, along with the response status, using the previously configured logger. It connects to the previous code by extending the logging setup to include request-response logging to AWS CloudWatch Logs.


  ![CloudWatch](https://github.com/bhanumalhotra123/aws-bootcamp-cruddur-2023/assets/144083659/33f93b5d-757e-4063-9a2f-937c495c116b)

```
class HomeActivities:
  def run():

   logger.info("HomeActivities")
    with tracer.start_as_current_span("home-activites-mock-data"):
      span = trace.get_current_span()
      now = datetime.now(timezone.utc).astimezone()  
```

>This Python class HomeActivities defines a method run() to execute certain actions. Inside run(), it logs a message using a logger named logger, then creates a new span with the name "home-activites-mock-data" using a tracer. It also retrieves the current span and obtains the current datetime in the UTC timezone.

