#from aws_xray_sdk.core import xray_recorder
from lib.db import db

class UserActivities:
  def run(user_handle):
    try:
      model = {
        'errors': None,
        'data': None
      }
      
      if user_handle == None or len(user_handle) < 1:
        model['errors'] = ['blank_user_handle']
      else:
    # Create an SQL template for querying home activities
        sql = db.template('users', 'show')    
    # Query the database and retrieve results as an array of JSON
        results = db.query_array_object(sql)
        model['data'] = results

      #subsegment = xray_recorder.begin_subsegment('mock-data')
      ## xray ---
      #dict = {
      #  "now": now.isoformat(),
      #  "results-size": len(model['data'])
      #}
      #subsegment.put_metadata('key', dict, 'namespace')
      #xray_recorder.end_subsegment()
    finally:  
    ##  # Close the segment
    #  xray_recorder.end_subsegment()
      return model