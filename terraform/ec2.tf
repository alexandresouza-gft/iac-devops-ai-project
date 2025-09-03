############################################
# User data (opcional – mantenho como estava)
############################################
data "template_file" "user_data" {
  template = file("${path.module}/cloud-init/ec2-multiple.yaml")
}

############################################
# AMI Ubuntu 22.04 (x86_64)
############################################
data "aws_ami" "latest_ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-*-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

############################################
# EC2 única
############################################
resource "aws_instance" "main" {
  ami                         = data.aws_ami.latest_ubuntu.id
  instance_type               = "t3.micro"
  subnet_id                   = module.vpc.public_subnets[0]
  vpc_security_group_ids      = [module.security_group_ec2.security_group_id]
  key_name                    = aws_key_pair.key_pair.key_name
  monitoring                  = true
  associate_public_ip_address = true

  # mantém seu cloud-init externo
  user_data = data.template_file.user_data.rendered

  # >>> ESSENCIAL para SSM:
  iam_instance_profile = aws_iam_instance_profile.ssm_profile.name

  root_block_device {
    encrypted             = true
    delete_on_termination = true
    volume_type           = "gp3"
    volume_size           = 16
    throughput            = 200
  }

  tags = merge(local.tags, { Name = "${local.name}-ec2" })

  depends_on = [
    module.vpc,
    aws_key_pair.key_pair,
    aws_secretsmanager_secret.secret,
    aws_secretsmanager_secret_version.secret_version,
    aws_iam_instance_profile.ssm_profile, # garante criação antes
  ]
}

############################################
# Elastic IP + Associação
############################################
resource "aws_eip" "main" {
  # Em contas modernas, VPC é o padrão; manter explícito:
  domain = "vpc"
  tags   = merge(local.tags, { Name = "${local.name}-eip" })
}

resource "aws_eip_association" "main" {
  instance_id   = aws_instance.main.id
  allocation_id = aws_eip.main.id
}

############################################
# IAM para SSM (role + instance profile)
############################################
resource "aws_iam_role" "ssm_role" {
  name = "${local.name}-ec2-ssm-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "ec2.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ssm_profile" {
  name = "${local.name}-ec2-ssm-profile"
  role = aws_iam_role.ssm_role.name
}

output "ec2_public_ip" {
  description = "IP público (EIP) da instância"
  value       = try(aws_eip.main.public_ip, aws_instance.main.public_ip)
}

output "instance_id" {
  description = "ID da instância EC2 para SSM"
  value       = aws_instance.main.id
}
