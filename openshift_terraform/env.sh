#!/usr/bin/env bash

# USAGE: source env.sh

echo "Updating repo to use versioned githooks"
git config core.hookspath githooks

# If AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are NOT set, use the default creds from ~/.aws/credentials
if [ -z "${AWS_ACCESS_KEY_ID}" ] && [ -z "${AWS_SECRET_ACCESS_KEY}" ]; then
  export AWS_ACCESS_KEY_ID="$(aws configure get default.aws_access_key_id)"
  export AWS_SECRET_ACCESS_KEY="$(aws configure get default.aws_secret_access_key)"
fi

if [ -z "${AWS_ACCESS_KEY_ID}" ] && [ -z "${AWS_SECRET_ACCESS_KEY}" ]; then
  echo "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are not set"
  echo "Tried to obtain them from ~/.aws/credentials but failed"
  echo "Ensure that you have the above ENV variables set or a ~/.aws/credentials file"

else
  echo "AWS Keys exported successfully"
  env | grep AWS
fi
