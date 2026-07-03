resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  name_suffix = random_id.suffix.hex

  tags = {
    ManagedBy = "terraform"
    Project   = var.project_name
    Env       = var.environment
  }

  dynamodb_tables = toset([
    "sessions",
    "customers",
    "appointments",
    "slots",
    "payments",
    "waitlist",
    "audit-events"
  ])
}
