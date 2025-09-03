variable "name" {
  description = "Nome base do projeto/stack"
  type        = string
  default = "projet-devops-ia"
}

variable "environments" {
  description = "Ambiente (ex: dev, hml, prd)"
  type        = string
  default = "sandbox"
}

variable "region" {
  description = "Região AWS onde os recursos serão criados"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr_block" {
  description = "CIDR para a VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "default_tags" {
  description = "Tags padrão aplicadas a todos os recursos"
  type        = map(string)
  default = {
    Project     = "projet-devops-ia"
    Environment = "sandbox"
    ManagedBy   = "Terraform"
  }
}
