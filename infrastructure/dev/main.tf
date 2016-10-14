provider "aws" {
    profile = "${var.aws_profile}"
    region  = "${var.aws_region}"
}

module "iam" {
  source = "../modules/iam"
  apex_environment = "${var.apex_environment}"
}

module "www" {
  source = "github.com/akranga/terraform-modules//s3_www"
  name   = "${var.apex_environment}.${var.route53_domain}"
}

module "r53_www" {
  source = "github.com/akranga/terraform-modules//r53_alias"
  name        = "${var.apex_environment}"
  r53_zone_id = "${var.route53_zone_id}"
  r53_domain  = "${var.route53_domain}"
  alias_zone_id = "${module.www.hosted_zone_id}" 
  alias_name  = "${module.www.website_domain}"
}

module "r53_api" {
  source = "github.com/akranga/terraform-modules//r53"
  name        = "api.${var.apex_environment}"
  r53_zone_id = "${var.route53_zone_id}"
  r53_domain  = "${var.route53_domain}"
  records     = ["${module.api_gateway.endpoint_host}"]
}

module "api_gateway" {
  source     = "github.com/akranga/terraform-modules//api_gateway"
  name       = "api.${var.apex_environment}.${var.route53_domain}"
  stage_name = "v1"
  aws_region = "${var.aws_region}"
}