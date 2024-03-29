# Import necessary modules for working with date and time, and the database
from datetime import datetime, timedelta, timezone
from lib.db import db

# Define a class named CreateActivity
class CreateActivity:
  # Define a method named run, which takes three parameters: message, user_handle, and ttl
  def run(message, cognito_user_id, ttl):
    # Initialize a dictionary to store the model's errors and data
    model = {
      'errors': None,
      'data': None
    }

    # Get the current date and time in UTC
    now = datetime.now(timezone.utc).astimezone()

    # Check the value of ttl and set the corresponding time offset
    if (ttl == '30-days'):
      ttl_offset = timedelta(days=30) 
    elif (ttl == '7-days'):
      ttl_offset = timedelta(days=7) 
    elif (ttl == '3-days'):
      ttl_offset = timedelta(days=3) 
    elif (ttl == '1-day'):
      ttl_offset = timedelta(days=1) 
    elif (ttl == '12-hours'):
      ttl_offset = timedelta(hours=12) 
    elif (ttl == '3-hours'):
      ttl_offset = timedelta(hours=3) 
    elif (ttl == '1-hour'):
      ttl_offset = timedelta(hours=1) 
    else:
      # If ttl is not one of the expected values, set an error in the model
      model['errors'] = ['ttl_blank']

    # Check if user_handle is None or has less than 1 character, set an error in the model
    if cognito_user_id == None or len(cognito_user_id) < 1:
      model['errors'] = ['cognito_user_id_blank']

    # Check if message is None or has less than 1 character, or exceeds the maximum allowed characters
    if message == None or len(message) < 1:
      model['errors'] = ['message_blank'] 
    elif len(message) > 280:
      model['errors'] = ['message_exceed_max_chars'] 

    # Check if there are any errors in the model
    if model['errors']:
      # If there are errors, populate the model's data with user_handle and message
      model['data'] = {
        'handle':  user_handle,
        'message': message
      }   
    else:
      # If no errors, calculate the expiration time, create an activity, and query the object
      expires_at = (now + ttl_offset)
      uuid = CreateActivity.create_activity(cognito_user_id, message, expires_at)
      object_json = CreateActivity.query_object_activity(uuid)
      model['data'] = object_json

    # Return the model
    return model

  # Define a method named create_activity, which takes handle, message, and expires_at as parameters
  def create_activity(cognito_user_id, message, expires_at):
    # Create an SQL template for creating an activity
    sql = db.template('activities', 'create')
    # Query the database and commit the changes, storing the UUID
    uuid = db.query_commit(sql, {
      'cognito_user_id': cognito_user_id,
      'message': message,
      'expires_at': expires_at
    })
    # Return the UUID
    return uuid

  # Define a method named query_object_activity, which takes uuid as a parameter
  def query_object_activity(uuid):
    # Create an SQL template for querying an activity
    sql = db.template('activities', 'object')
    # Query the database and return the result as JSON
    return db.query_object_json(sql, {
      'uuid': uuid
    })
