# DynamoDBで使用するテーブルを作成する

resource "aws_dynamodb_table" "dynamodb_table_histories" {
  name         = var.setting.table_name_histories
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "partition_key"
  range_key    = "update_at"

  attribute {
    name = "partition_key"
    type = "S"
  }

  attribute {
    name = "update_at"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
