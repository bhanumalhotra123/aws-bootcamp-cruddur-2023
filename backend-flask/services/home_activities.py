# Import necessary modules for working with date and time, distributed tracing, and the database
from datetime import datetime, timedelta, timezone
from opentelemetry import trace
from lib.db import db

# Uncomment the following line if the tracer is intended to be used
#tracer = trace.get_tracer("home.activities")

# Define a class named HomeActivities
class HomeActivities:
  # Define a method named run, which takes cognito_user_id as an optional parameter
  def run(cognito_user_id=None):
    # Uncomment the following lines if logging and distributed tracing are intended to be used
    #logger.info("HomeActivities")
    #with tracer.start_as_current_span("home-activites-mock-data"):
    #  span = trace.get_current_span()
    #  now = datetime.now(timezone.utc).astimezone()
    #  span.set_attribute("app.now", now.isoformat())
    
    # Create an SQL template for querying home activities
    sql = db.template('activities', 'home')
    
    # Query the database and retrieve results as an array of JSON
    results = db.query_array_json(sql)
    
    # Return the results
    return results
