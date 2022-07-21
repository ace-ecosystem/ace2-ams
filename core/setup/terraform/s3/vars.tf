###################################################
### KMS
###################################################

variable "identifier" {
  type = string
  default = "ice2-s3"
  description = "Identifier for KMS key to identify this key as being for ice2-s3 encryption"
}