############################################
# Key Pair (mantida) + Secrets Manager
############################################
resource "random_string" "random" {
  length  = 4
  special = false
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
}

resource "aws_key_pair" "key_pair" {
  key_name   = "${var.name}-${var.environments}-key"
  public_key = tls_private_key.private_key.public_key_openssh
  tags       = local.tags
}

resource "aws_secretsmanager_secret" "secret" {
  name                           = "${var.name}-${var.environments}-${random_string.random.result}-key-pair"
  recovery_window_in_days        = 0
  force_overwrite_replica_secret = true
}

resource "aws_secretsmanager_secret_version" "secret_version" {
  secret_id     = aws_secretsmanager_secret.secret.id
  secret_string = tls_private_key.private_key.private_key_pem
}

data "aws_secretsmanager_secret" "secret" {
  arn = aws_secretsmanager_secret.secret.arn
}

data "aws_secretsmanager_secret_version" "open_finance_private" {
  secret_id  = data.aws_secretsmanager_secret.secret.id
  depends_on = [aws_secretsmanager_secret.secret]
}

locals {
  open_finance_private = nonsensitive(data.aws_secretsmanager_secret_version.open_finance_private.secret_string)
}

output "open_finance_private" {
  description = "Chave privada recuperada do Secrets Manager"
  value       = local.open_finance_private
  sensitive   = true
}
