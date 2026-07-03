data "archive_file" "agent" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda_src/agent"
  output_path = "${path.module}/agent.zip"
}

data "archive_file" "waitlist_reactor" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda_src/waitlist_reactor"
  output_path = "${path.module}/waitlist_reactor.zip"
}

resource "aws_cloudwatch_log_group" "agent" {
  name              = "/aws/lambda/${local.name_prefix}-agent-${local.name_suffix}"
  retention_in_days = 14
  tags              = local.tags
}

resource "aws_cloudwatch_log_group" "waitlist_reactor" {
  name              = "/aws/lambda/${local.name_prefix}-waitlist-reactor-${local.name_suffix}"
  retention_in_days = 14
  tags              = local.tags
}

resource "aws_lambda_function" "agent" {
  function_name    = "${local.name_prefix}-agent-${local.name_suffix}"
  role             = aws_iam_role.lambda.arn
  runtime          = var.lambda_runtime
  handler          = "handler.lambda_handler"
  filename         = data.archive_file.agent.output_path
  source_code_hash = data.archive_file.agent.output_base64sha256
  timeout          = var.agent_lambda_timeout_seconds
  memory_size      = var.lambda_memory_mb

  environment {
    variables = {
      ENVIRONMENT                 = var.environment
      PROJECT_NAME                = var.project_name
      SESSIONS_TABLE              = aws_dynamodb_table.poc["sessions"].name
      CUSTOMERS_TABLE             = aws_dynamodb_table.poc["customers"].name
      APPOINTMENTS_TABLE          = aws_dynamodb_table.poc["appointments"].name
      SLOTS_TABLE                 = aws_dynamodb_table.poc["slots"].name
      PAYMENTS_TABLE              = aws_dynamodb_table.poc["payments"].name
      WAITLIST_TABLE              = aws_dynamodb_table.poc["waitlist"].name
      AUDIT_EVENTS_TABLE          = aws_dynamodb_table.poc["audit-events"].name
      DOCUMENTS_BUCKET            = aws_s3_bucket.documents.bucket
      VECTOR_BUCKET_NAME          = aws_s3vectors_vector_bucket.rag.vector_bucket_name
      VECTOR_INDEX_NAME           = aws_s3vectors_index.rag.index_name
      EVENT_BUS_NAME              = aws_cloudwatch_event_bus.poc.name
      SES_FROM_EMAIL              = var.ses_from_email
      BEDROCK_CLASSIFIER_MODEL_ID = var.bedrock_classifier_model_id
      BEDROCK_EMBEDDING_MODEL_ID  = var.bedrock_embedding_model_id
      ENABLE_BEDROCK_GUARDRAILS  = tostring(var.enable_bedrock_guardrails)
      BEDROCK_GUARDRAIL_ID        = var.bedrock_guardrail_id
      BEDROCK_GUARDRAIL_VERSION   = var.bedrock_guardrail_version
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.agent,
    aws_iam_role_policy_attachment.basic_lambda,
    aws_iam_role_policy_attachment.poc_app
  ]

  tags = merge(local.tags, {
    Component = "agent"
  })
}

resource "aws_lambda_function" "waitlist_reactor" {
  function_name    = "${local.name_prefix}-waitlist-reactor-${local.name_suffix}"
  role             = aws_iam_role.lambda.arn
  runtime          = var.lambda_runtime
  handler          = "handler.lambda_handler"
  filename         = data.archive_file.waitlist_reactor.output_path
  source_code_hash = data.archive_file.waitlist_reactor.output_base64sha256
  timeout          = var.reactor_lambda_timeout_seconds
  memory_size      = var.lambda_memory_mb

  environment {
    variables = {
      ENVIRONMENT        = var.environment
      WAITLIST_TABLE     = aws_dynamodb_table.poc["waitlist"].name
      SLOTS_TABLE        = aws_dynamodb_table.poc["slots"].name
      APPOINTMENTS_TABLE = aws_dynamodb_table.poc["appointments"].name
      AUDIT_EVENTS_TABLE = aws_dynamodb_table.poc["audit-events"].name
      SES_FROM_EMAIL     = var.ses_from_email
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.waitlist_reactor,
    aws_iam_role_policy_attachment.basic_lambda,
    aws_iam_role_policy_attachment.poc_app
  ]

  tags = merge(local.tags, {
    Component = "waitlist-reactor"
  })
}
