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

