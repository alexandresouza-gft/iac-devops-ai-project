terraform {
  required_version = ">= 1.5.0"
  backend "s3" {
    bucket         = "iac-tfstate-us-east-1-alexandresouza-gft" # troque
    key            = "envs/puc-minas/terraform.tfstate"         # caminho do state no bucket
    region         = "us-east-1"
    encrypt        = true
  }
}
