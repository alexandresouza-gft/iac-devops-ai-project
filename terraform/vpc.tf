############################################
# VPC (apenas públicos; simples e direto)
############################################
data "aws_availability_zones" "available" {}

locals {
  region   = var.region
  vpc_cidr = var.vpc_cidr_block
  # 2 AZs públicas (poderia ser 1, mas manter 2 é prática antiga comum)
  azs  = slice(data.aws_availability_zones.available.names, 0, 2)
  tags = var.default_tags
  name = "${var.name}-${var.environments}"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = local.name
  cidr = local.vpc_cidr

  azs            = local.azs
  public_subnets = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 4)]

  # Apenas internet pública; sem NAT, sem VPN
  enable_nat_gateway = false
  enable_vpn_gateway = false

  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = local.tags
}