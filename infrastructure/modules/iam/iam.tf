
resource "aws_iam_role" "lambda_function" {
  name = "${var.apex_environment}-lambda-execution"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "cloudwatchlogs_full_access" {
  name = "${var.apex_environment}-cloudwatch-full"
  role = "${aws_iam_role.lambda_function.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "dynamodb_full_access" {
  name = "${var.apex_environment}-dynamo-full"
  role = "${aws_iam_role.lambda_function.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "dynamodb:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}


resource "aws_iam_role_policy" "s3_full_access" {
  name = "${var.apex_environment}-s3-full"
  role = "${aws_iam_role.lambda_function.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "invoke_lambda" {
  name = "${var.apex_environment}-invoke-lambda"
  role = "${aws_iam_role.lambda_function.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "*"
      ],
      "Action": [
        "lambda:InvokeFunction"           
      ]       
    }    
  ]
}
EOF
}