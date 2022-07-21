###########################
### Configuration vars
###########################

variable "region" {
  type = string
  description = "AWS Region infrastructure will be deployed to"
  default = "us-east-2"
  validation {
    condition     = contains(["us-east-1", "us-east-2"], var.region)
    error_message = "Must be in us-east-*."
  } 
}

variable "environment" {
  type = string
  description = "dev or prod"
  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Valid values for environment are : dev or prod."
  } 
}

###########################
### Analysis module vars
###########################

variable "analysis_module_name" {
  type = string
  description = "Name of the analysis module the infrastructure is for"
}

variable "analysis_ecr_image" {
    type = string
    description = "ECR image URI containing the analysis function's deployment package"
}
 
variable "analysis_lambda_env_vars" {
  type = map(any)
  description = "Add map of env vars to be added to the analysis module lambda function runtime"
}