resource "aws_s3_bucket" "documents" {
  bucket = "${local.name_prefix}-docs-${local.name_suffix}"

  tags = merge(local.tags, {
    Component = "documents"
  })
}

resource "aws_s3_bucket_public_access_block" "documents" {
  bucket = aws_s3_bucket.documents.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "documents" {
  bucket = aws_s3_bucket.documents.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "documents" {
  bucket = aws_s3_bucket.documents.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3vectors_vector_bucket" "rag" {
  vector_bucket_name = "${local.name_prefix}-vectors-${local.name_suffix}"
}

resource "aws_s3vectors_index" "rag" {
  vector_bucket_name = aws_s3vectors_vector_bucket.rag.vector_bucket_name
  index_name         = "clinic-policy-index"
  data_type          = "float32"
  dimension          = var.vector_dimension
  distance_metric    = "cosine"
}
