output "agent_lambda_name" {
  description = "Main agent Lambda function name."
  value       = aws_lambda_function.agent.function_name
}

output "waitlist_reactor_lambda_name" {
  description = "Waitlist reactor Lambda function name."
  value       = aws_lambda_function.waitlist_reactor.function_name
}

output "documents_bucket" {
  description = "S3 bucket for uploaded clinic policy/FAQ documents."
  value       = aws_s3_bucket.documents.bucket
}

output "vector_bucket_name" {
  description = "S3 Vectors vector bucket name."
  value       = aws_s3vectors_vector_bucket.rag.vector_bucket_name
}

output "vector_index_name" {
  description = "S3 Vectors index name for RAG chunks."
  value       = aws_s3vectors_index.rag.index_name
}

output "event_bus_name" {
  description = "EventBridge bus for cancellation and waitlist events."
  value       = aws_cloudwatch_event_bus.poc.name
}

output "dynamodb_tables" {
  description = "DynamoDB tables created for the POC."
  value       = { for role, table in aws_dynamodb_table.poc : role => table.name }
}
