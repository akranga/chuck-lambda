output "lambda_function_role_id" {
  value = "${module.iam.lambda_function_role_id}"
}

output "domain_name_www" {
  value = "${module.r53_www.fqdn}"
}

output "api_gateway_id" {
  value = "${module.api_gateway.api_id}"
}

output "api_gateway_stage" {
  value = "${module.api_gateway.stage_name}"
}

output "api_gateway_domain" {
  value = "${module.api_gateway.endpoint_url}"
}

output "api_gateway_name" {
  value = "${module.api_gateway.name}"
}

output "api_gateway_host" {
  value = "${module.api_gateway.endpoint_host}"
}

output "aws_region" {
  value = "${var.aws_region}"
}

# output "api_gateway_domain2" {
#   value = "https://${module.r53_api.fqdn}/${module.api_gateway.stage_name}"
# }

output "dynamodb" {
  value = "${aws_dynamodb_table.chuck.arn}"
}

output "apex_function_role" {
  value = "${module.iam.lambda_function_role_id}"
}