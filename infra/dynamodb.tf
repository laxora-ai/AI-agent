resource "aws_dynamodb_table" "poc" {
  for_each = local.dynamodb_tables

  name         = "${local.name_prefix}-${each.key}-${local.name_suffix}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "pk"

  attribute {
    name = "pk"
    type = "S"
  }

  point_in_time_recovery {
    enabled = false
  }

  tags = merge(local.tags, {
    Component = "state"
    TableRole = each.key
  })
}
