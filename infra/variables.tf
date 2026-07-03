variable "aws_region" {
  description = "AWS region for the inexpensive Laxora AI agent POC."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Short project name used in AWS resource names."
  type        = string
  default     = "laxora-agent"
}

variable "environment" {
  description = "Environment name."
  type        = string
  default     = "dev"
}

variable "lambda_runtime" {
  description = "Python runtime for the Lambda functions."
  type        = string
  default     = "python3.12"
}

variable "agent_lambda_timeout_seconds" {
  description = "Timeout for the main agent Lambda."
  type        = number
  default     = 30
}

variable "reactor_lambda_timeout_seconds" {
  description = "Timeout for the waitlist reactor Lambda."
  type        = number
  default     = 30
}

variable "lambda_memory_mb" {
  description = "Memory for both Lambda functions."
  type        = number
  default     = 512
}

variable "allowed_cors_origins" {
  description = "Origins allowed by the future API/frontend endpoint."
  type        = list(string)
  default     = ["http://localhost:3000", "http://localhost:5173"]
}

variable "ses_from_email" {
  description = "Verified SES sandbox sender email. Leave blank until email demo is needed."
  type        = string
  default     = ""
}

variable "bedrock_classifier_model_id" {
  description = "Bedrock model used for cheap routing/classification and short replies."
  type        = string
  default     = "us.anthropic.claude-haiku-4-5-20251001-v1:0"
}

variable "bedrock_embedding_model_id" {
  description = "Bedrock embedding model for document ingestion."
  type        = string
  default     = "amazon.titan-embed-text-v2:0"
}

variable "vector_dimension" {
  description = "Embedding dimension for the S3 Vectors index. Titan Text Embeddings v2 commonly uses 1024 by default."
  type        = number
  default     = 1024
}

variable "enable_bedrock_guardrails" {
  description = "Set true after creating/configuring a Bedrock Guardrail. Regex guardrails still work when false."
  type        = bool
  default     = false
}

variable "bedrock_guardrail_id" {
  description = "Optional Bedrock Guardrail ID."
  type        = string
  default     = ""
}

variable "bedrock_guardrail_version" {
  description = "Optional Bedrock Guardrail version."
  type        = string
  default     = "DRAFT"
}
