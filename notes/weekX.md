# Week X
Need to get our application working!

What we achieved in last week?
- have setup cfn infra and made architecture change for frontend as we now will server it through cloudfront


created a static-build file under bin/frontend



#! /usr/bin/bash

ABS_PATH=$(readlink -f "$0")
FRONTEND_PATH=$(dirname $ABS_PATH)
BIN_PATH=$(dirname $FRONTEND_PATH)
PROJECT_PATH=$(dirname $BIN_PATH)
FRONTEND_REACT_JS_PATH="$PROJECT_PATH/frontend-react-js"

cd $FRONTEND_REACT_JS_PATH

npm run build
REACT_APP_BACKEND_URL="https://api.gooddesignsolutions.in" \
REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
REACT_APP_AWS_USER_POOLS_ID="us-east-1_fpy2gmV5r" \
REACT_APP_CLIENT_ID="6roer8tk701iejmp627t0upavl" \
npm run build


tried running this locally and solved some of the errors that we got.


pushed the script and changes

after that we zipped the build dir in frontend-react-js

$ zip -r build.zip build/

upload the zipped build dir contents in gooddesignsolutions.in bucket in s3 that was created from frontend cfn infra created in week 10-11

once uploaded you can test going to the domain so as to see what cloudfront is serving you

Now we will use aws_s3_website_sync

This is a tool to sync a folder from your local developer environment to your S3 Bucket and then invalidate the CloudFront cache

https://github.com/teacherseat/aws-s3-website-sync

This have the instructions

Created a new script file sync in bin/frontend


#!/usr/bin/env ruby

require 'aws_s3_website_sync'
require 'dotenv'

env_path = "/workspace/aws-bootcamp-cruddur-2023/sync.env"
Dotenv.load(env_path)

puts "== configuration"
puts "aws_default_region:   #{ENV["AWS_DEFAULT_REGION"]}"
puts "s3_bucket:            #{ENV["SYNC_S3_BUCKET"]}"
puts "distribution_id:      #{ENV["SYNC_CLOUDFRONT_DISTRUBTION_ID"]}"
puts "build_dir:            #{ENV["SYNC_BUILD_DIR"]}"

changeset_path = ENV["SYNC_OUTPUT_CHANGESET_PATH"]
changeset_path = changeset_path.sub(".json","-#{Time.now.to_i}.json")

puts "output_changset_path: #{changeset_path}"
puts "auto_approve:         #{ENV["SYNC_AUTO_APPROVE"]}"

puts "sync =="
AwsS3WebsiteSync::Runner.run(
  aws_access_key_id:     ENV["AWS_ACCESS_KEY_ID"],
  aws_secret_access_key: ENV["AWS_SECRET_ACCESS_KEY"],
  aws_default_region:    ENV["AWS_DEFAULT_REGION"],
  s3_bucket:             ENV["SYNC_S3_BUCKET"],
  distribution_id:       ENV["SYNC_CLOUDFRONT_DISTRUBTION_ID"],
  build_dir:             ENV["SYNC_BUILD_DIR"],
  output_changset_path:  changeset_path,
  auto_approve:          ENV["SYNC_AUTO_APPROVE"],
  silent: "ignore,no_change",
  ignore_files: [
    'stylesheets/index',
    'android-chrome-192x192.png',
    'android-chrome-256x256.png',
    'apple-touch-icon-precomposed.png',
    'apple-touch-icon.png',
    'site.webmanifest',
    'error.html',
    'favicon-16x16.png',
    'favicon-32x32.png',
    'favicon.ico',
    'robots.txt',
    'safari-pinned-tab.svg'
  ]
)




once done we do: gem install aws_s3_website_sync

https://rubygems.org/gems/dotenv

went to the home page of this

https://github.com/bkeepers/dotenv

created sync.env.erb in erb folder

SYNC_S3_BUCKET=gooddesignsolutions.in
SYNC_CLOUDFRONT_DISTRUBTION_ID= needs to be filled from console
SYNC_BUILD_DIR=<%= ENV['THEIA_WORKSPACE_ROOT'] %>/frontend-react-js/build
SYNC_OUTPUT_CHANGESET_PATH=<%=  ENV['THEIA_WORKSPACE_ROOT'] %>/tmp/changeset.json
SYNC_AUTO_APPROVE=false




made the changes to /bin/frontend/generate-env

#!/usr/bin/env ruby

require 'erb'

template = File.read 'erb/frontend-react-js.env.erb'
content = ERB.new(template).result(binding)
filename = "frontend-react-js.env"
File.write(filename, content)

template = File.read 'erb/sync.env.erb'
content = ERB.new(template).result(binding)
filename = "sync.env"
File.write(filename, content)





after this we run ./bin/frontend/sync

till now we hadn't change anything in frontend

Let's go and make change

Went to DesktopSidebar.js and make change by adding an exclamation mark About!


then we run ./bin/frontend/static-build

then we will run ./bin/frontend/sync tool
It will show up some changes 

It creates invalidation



changeset_path = changeset_path.sub(".json","-#{Time.now.to_i}.json")

The provided line of code is written in Ruby and appears to be modifying a file path by appending the current Unix timestamp to the filename before the file extension.


Go to cloudformation and go to invalidation

