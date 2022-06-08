##############################################################
### Configure Backend Remote State and Providers
##############################################################

terraform {
  backend "remote" {
    hostname     = "app.terraform.io"
    organization = "FifthThird"
    workspaces {
      prefix = "idr-aws-ice2-s3-dev"
    }
  }
}

#Declare AWS provider
provider "aws" {
  region = "us-east-2"
}

#Get info about current session
data "aws_caller_identity" "current" {}
