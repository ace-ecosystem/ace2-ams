##############################################################
### Configure Backend Remote State
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

#Get info about current session
data "aws_caller_identity" "current" {}
