
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
  version = "1.0.12"
  #Vars
  environment              = var.environment
  analysis_module_name     = var.analysis_module_name
  analysis_ecr_image       = var.analysis_ecr_image
  analysis_lambda_env_vars = var.analysis_lambda_env_vars
}