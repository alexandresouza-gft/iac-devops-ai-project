############################################
# Security Group (SSH + Porta 8501)
############################################
module "security_group_ec2" {
  source = "terraform-aws-modules/security-group/aws"

  name        = "${local.name}-ec2"
  description = "Security group for single EC2"
  vpc_id      = module.vpc.vpc_id

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["ssh-tcp"]

  ingress_with_cidr_blocks = [
    {
      from_port   = 8501
      to_port     = 8501
      protocol    = "tcp"
      cidr_blocks = "0.0.0.0/0"
    }
  ]

  egress_rules = ["all-all"]

  tags = merge(local.tags, { Name = "${local.name}-sg-ec2" })
}
