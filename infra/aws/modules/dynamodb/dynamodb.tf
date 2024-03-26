resource "aws_dynamodb_table" "dynamodb_table_histories" {
  name           = var.env["AWS_DYNAMODB_TABLE_NAME_HISTORIES"]
  billing_mode   = "PROVISIONED"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "partition_key"
  range_key      = "update_at"

  attribute {
    name = "partition_key"
    type = "S"
  }

  attribute {
    name = "update_at"
    type = "S"
  }
}
