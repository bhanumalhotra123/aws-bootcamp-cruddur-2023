# Import the ConnectionPool class from the psycopg_pool module
from psycopg_pool import ConnectionPool
# Import necessary modules for handling file paths, regular expressions, and Flask's current_app
import os
import re
import sys
from flask import current_app as app

# Define a class named Db
class Db:
  # Constructor method to initialize the connection pool
  def __init__(self):
    self.init_pool()

  # Method to generate a SQL template path and load its content
  def template(self, *args):
    # Create a list containing the root path, 'db', 'sql', and provided arguments
    pathing = list((app.root_path, 'db', 'sql',) + args)
    # Append ".sql" to the last element of the list
    pathing[-1] = pathing[-1] + ".sql"
    # Join the elements of the list to form the file path
    template_path = os.path.join(*pathing)

    # Set color codes for terminal output
    green = '\033[92m'
    no_color = '\033[0m'
    # Print a message indicating the loaded SQL template
    print("\n")
    print(f'{green} Load SQL Template: {template_path} {no_color}')

    # Open the SQL template file and read its content
    with open(template_path, 'r') as f:
      template_content = f.read()
    # Return the content of the SQL template
    return template_content

  # Method to initialize the connection pool
  def init_pool(self):
    # Retrieve the PostgreSQL connection URL from the environment variable
    connection_url = os.getenv("CONNECTION_URL")
    # Create a ConnectionPool instance using the retrieved connection URL
    self.pool = ConnectionPool(connection_url)

  # Method to print SQL parameters
  def print_params(self, params):
    # Set color codes for terminal output
    blue = '\033[94m'
    no_color = '\033[0m'
    # Print a header indicating SQL parameters
    print(f'{blue} SQL Params:{no_color}')
    # Iterate through key-value pairs in the params dictionary and print them
    for key, value in params.items():
      print(key, ":", value)

  # Method to print SQL statements
  def print_sql(self, title, sql, params={}):
    # Set color codes for terminal output
    cyan = '\033[96m'
    no_color = '\033[0m'
    # Print a header indicating the type of SQL statement
    print(f'{cyan} SQL STATEMENT-[{title}]------{no_color}')
    # Print the SQL statement
    print(sql, params)

  # Method to execute a SQL statement with commit and returning functionality
  def query_commit(self, sql, params={}, verbose=True):
    if verbose:
    # Print the SQL statement with a header indicating the type
      self.print_sql('commit with returning', sql, params)

    # Check if the SQL statement contains the keyword RETURNING
    pattern = r"\bRETURNING\b"
    is_returning_id = re.search(pattern, sql)

    try:
      # Execute the SQL statement within a connection
      with self.pool.connection() as conn:
        # Create a cursor for executing SQL commands
        cur = conn.cursor()
        # Execute the SQL statement with the provided parameters
        cur.execute(sql, params)
        # If RETURNING is present, fetch the returned ID
        if is_returning_id:
          returning_id = cur.fetchone()[0]
        # Commit the changes to the database
        conn.commit()
        # If RETURNING is present, return the fetched ID
        if is_returning_id:
          return returning_id
    except Exception as err:
      # Handle exceptions related to psycopg errors and print details
      self.print_sql_err(err)


  def query_array_json(self, sql, params={}, verbose=True):
    # Print the SQL statement with a header indicating the type
    if verbose:
      self.print_sql('array', sql, params)

    # Wrap the SQL statement to return an array of JSON objects
    wrapped_sql = self.query_wrap_array(sql)
    # Execute the wrapped SQL statement within a connection
    with self.pool.connection() as conn:
      # Create a cursor for executing SQL commands
      with conn.cursor() as cur:
        # Execute the wrapped SQL statement with the provided parameters
        cur.execute(wrapped_sql, params)
        # Fetch the first row of the result (single JSON object)
        json = cur.fetchone()
        # Return the fetched JSON object
        return json[0]

  # Method to execute a SQL statement and return a single JSON object
  def query_object_json(self, sql, params={}, verbose=True):
    if verbose:
    # Print the SQL statement with a header indicating the type
      self.print_sql('json', sql, params)
    # Print the SQL parameters
      self.print_params(params)

    # Wrap the SQL statement to return a single JSON object
    wrapped_sql = self.query_wrap_object(sql)

    # Execute the wrapped SQL statement within a connection
    with self.pool.connection() as conn:
      # Create a cursor for executing SQL commands
      with conn.cursor() as cur:
        # Execute the wrapped SQL statement with the provided parameters
        cur.execute(wrapped_sql, params)
        # Fetch the first row of the result (single JSON object)
        json = cur.fetchone()
        # If the fetched JSON object is None, return an empty JSON object
        if json is None:
          return "{}"
        else:
          # Return the fetched JSON object
          return json[0]

  def query_value(self,sql,params={}, verbose=True):
    if verbose:
      self.print_sql('value',sql,params)
    with self.pool.connection() as conn:
      with conn.cursor() as cur:
        cur.execute(sql,params)
        json = cur.fetchone()
        return json[0]

  # Method to wrap a SQL statement for returning a single JSON object
  def query_wrap_object(self, template):
    # Construct a SQL statement that wraps the provided template for a single JSON object
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    # Return the wrapped SQL statement
    return sql

  # Method to wrap a SQL statement for returning an array of JSON objects
  def query_wrap_array(self, template):
    # Construct a SQL statement that wraps the provided template for an array of JSON objects
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    # Return the wrapped SQL statement
    return sql

  # Method to print errors related to psycopg
  def print_sql_err(self, err):
    # Get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # Get the line number when the exception occurred
    line_num = traceback.tb_lineno

    # Print the psycopg ERROR, traceback, exception type, pgerror, and pgcode
    print ("\npsycopg ERROR:", err, "on line number:", line_num)
    print ("psycopg traceback:", traceback, "-- type:", err_type)
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")

# Create an instance of the Db class
db = Db()
