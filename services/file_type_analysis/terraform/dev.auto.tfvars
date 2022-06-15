environment          = "dev"
analysis_module_name = "FileType"
analysis_ecr_image   = "728226656595.dkr.ecr.us-east-2.amazonaws.com/file_type:latest"
analysis_lambda_env_vars = {
  "FILE_STORAGE_BUCKET" = "ice2-file-storage"
  "QUEUE_BASE_URL"      = "https://sqs.us-east-2.amazonaws.com/728226656595"
}