# Laxora AI Agent POC

This repository starts with a cheap AWS proof of concept for the Laxora AI front-desk agent.

The goal is not production HIPAA architecture yet. The goal is to prove the live demo flow:

- one main agent Lambda
- one waitlist reactor Lambda
- DynamoDB for demo state
- S3 for source documents
- S3 Vectors for RAG embeddings
- EventBridge for cancellation → waitlist automation
- SES permissions for confirmation emails
- Bedrock permissions for Haiku, Titan embeddings, and optional Guardrails

## Structure

```text
infra/
  versions.tf
  variables.tf
  locals.tf
  dynamodb.tf
  s3.tf
  iam.tf
  lambda.tf
  eventbridge.tf
  outputs.tf
  terraform.tfvars.example

lambda_src/
  agent/handler.py
  waitlist_reactor/handler.py
```

## First deploy

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

## What gets created

- DynamoDB tables:
  - sessions
  - customers
  - appointments
  - slots
  - payments
  - waitlist
  - audit-events
- S3 document bucket
- S3 Vectors vector bucket and index
- Lambda IAM role and policy
- agent Lambda
- waitlist reactor Lambda
- EventBridge custom bus, rule, and target
- CloudWatch log groups

## Next build step

The Lambda handlers are intentionally small placeholders. Next, replace `lambda_src/agent/handler.py` with the real app adapter that calls your graph:

```text
POST message
→ load session from DynamoDB
→ input guardrails
→ pending-action check
→ router
→ identity gate
→ scheduling/billing/waitlist/smalltalk path
→ output guardrail
→ save session + audit event
→ return reply
```

## Notes

- The Terraform does not create a public endpoint yet. Add API Gateway or a carefully controlled Lambda Function URL once the agent handler is ready.
- Keep `enable_bedrock_guardrails = false` until a Bedrock Guardrail exists in the account.
- SES sandbox requires verified sender and recipient emails.
- S3 Vectors support requires a recent AWS provider version, so the provider is pinned to `>= 6.24.0`.
