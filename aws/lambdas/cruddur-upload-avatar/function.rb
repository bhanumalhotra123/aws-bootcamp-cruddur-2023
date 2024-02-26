# Import necessary libraries
require 'aws-sdk-s3'  # AWS SDK for Ruby - S3 library for interacting with Amazon S3
require 'json'        # Library for working with JSON data
require 'jwt'         # JSON Web Token library for Ruby

# Lambda function handler
def handler(event:, context:)
  # Log the incoming event data
  puts event m

  # Check if the request is a preflight CORS check
  if event['routeKey'] == "OPTIONS /{proxy+}"
    # Log preflight check
    puts({step: 'preflight', message: 'preflight CORS check'}.to_json)

    # Return CORS headers for preflight check
    {
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization",   # Allow any headers in the request
        "Access-Control-Allow-Origin": "https://3000-bhanumalhotra-awsbootcampcru-2n1d6e0bd1f.ws-us94.gitpod.io",  # Allow requests from specific origin
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"     # Allow specified HTTP methods
      },
      statusCode: 200  # HTTP status code indicating success
    }
  else
    # Extract token from authorization header
    token = event['headers']['authorization'].split(' ')[1]
    # Log token extraction
    puts({step: 'presignedurl', access_token: token}.to_json)

    # Parse request body to get file extension
    body_hash = JSON.parse(event["body"])
    extension = body_hash["extension"]

    # Decode JWT token to get user UUID
    decoded_token = JWT.decode token, nil, false
    cognito_user_uuid = decoded_token[0]['sub']

    # Create an AWS S3 client
    s3 = Aws::S3::Resource.new  # Initialize AWS S3 client
    bucket_name = ENV["UPLOADS_BUCKET_NAME"]  # Get bucket name from environment variable
    object_key = "#{cognito_user_uuid}.#{extension}"  # Construct object key for the file in S3

    # Generate presigned URL for uploading the file to S3
    obj = s3.bucket(bucket_name).object(object_key)  # Get reference to S3 object
    url = obj.presigned_url(:put, expires_in: 60 * 5)  # Generate presigned URL with expiration time of 5 minutes

    # Prepare response body with the presigned URL
    body = {url: url}.to_json

    # Return response with CORS headers and presigned URL
    {
      headers: {
        "Access-Control-Allow-Headers": "*, Authorization",   # Allow any headers in the request
        "Access-Control-Allow-Origin": "https://3000-bhanumalhotra-awsbootcampcru-2n1d6e0bd1f.ws-us94.gitpod.io",  # Allow requests from specific origin
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"     # Allow specified HTTP methods
      },
      statusCode: 200,  # HTTP status code indicating success
      body: body        # Response body containing presigned URL
    }
  end # if 
end # def handler
