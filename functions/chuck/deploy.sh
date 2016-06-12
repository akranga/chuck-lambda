#!/bin/bash -xe

name="serverless-chuck"
handler="Main::handleRequest"
role="arn:aws:iam::776022106184:role/apex_lambda_function"

./gradlew clean build

aws lambda create-function --function-name="$name" \
                           --runtime="java8" \
                           --handler="$handler" \
                           --role="$role" \
                           --zip-file="fileb://build/libs/apex.jar"