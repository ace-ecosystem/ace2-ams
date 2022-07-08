
###############################################################
### Configure Backend Remote State and Providers
###############################################################

terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "FifthThird"
    workspaces {
      prefix = "idr-aws-ice2-module-filetype-dev"
    }
  }
}

provider "aws" {
  region = "us-east-2"
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

module "filetype-idr-analysis-module" {
  source  = "app.terraform.io/FifthThird/idr-analysis-module/aws"
  version = "1.0.9"
  #Vars
  environment              = var.environment
  analysis_module_name     = var.analysis_module_name
  analysis_ecr_image       = var.analysis_ecr_image
  analysis_lambda_env_vars = var.analysis_lambda_env_vars
}

resource "aws_cloudwatch_log_subscription_filter" "analysis_lambda_logfilter" {
  name            = "${var.analysis_module_name}_analysis_logfilter"
  role_arn        = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/CloudwatchToKinesisRole"
  log_group_name  = "/aws/lambda/${var.analysis_module_name}_analysis"
  filter_pattern  = ""
  destination_arn = "arn:aws:firehose:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:deliverystream/kinesis-firehose-to-splunk"
  distribution    = "Random"

  depends_on      = [ module.filetype-idr-analysis-module ]
}