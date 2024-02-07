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




   
