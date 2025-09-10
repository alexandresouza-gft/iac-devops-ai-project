# 🚀 Projeto DevOps + IA

Uma aplicação Streamlit containerizada com deploy automatizado na AWS usando Infraestrutura como Código.

## 📋 Sobre o Projeto

Este projeto demonstra uma implementação completa de DevOps para uma aplicação de IA, incluindo:

- **Aplicação**: Interface web desenvolvida em Streamlit (Python 3.12)
- **Containerização**: Docker e Docker Compose
- **Infraestrutura**: AWS (EC2, VPC, Security Groups, IAM, Secrets Manager)
- **IaC**: Terraform para provisionamento de recursos
- **CI/CD**: GitHub Actions para deploy automatizado
- **Segurança**: AWS SSM para execução remota sem SSH direto

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│ GitHub Actions   │───▶│   AWS Cloud     │
│                 │    │                  │    │                 │
│ • Código fonte  │    │ • Terraform      │    │ • EC2 Instance  │
│ • Dockerfile    │    │ • AWS CLI        │    │ • VPC + Subnets │
│ • Terraform     │    │ • Deploy via SSM │    │ • Security Group│
│ • GitHub Actions│    │                  │    │ • Secrets Mgr   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   Streamlit App │
                                               │   (Port 8501)   │
                                               │                 │
                                               │ • Docker        │
                                               │ • Python 3.12   │
                                               │ • Auto-restart  │
                                               └─────────────────┘
```

## ⚡ Recursos AWS Utilizados

- **EC2**: Instância t3.micro com Ubuntu 22.04
- **VPC**: Rede privada com subnets públicas em 2 AZs
- **Security Groups**: Firewall permitindo SSH (22) e Streamlit (8501)
- **Elastic IP**: IP público fixo
- **IAM**: Perfis e políticas para SSM
- **Secrets Manager**: Armazenamento seguro de chaves privadas
- **Systems Manager (SSM)**: Deploy remoto sem SSH

## 🛠️ Pré-requisitos

### AWS
- Conta AWS com permissões para EC2, VPC, IAM, SSM e Secrets Manager
- Bucket S3 para armazenar o estado do Terraform
- Região configurada (padrão: us-east-1)

### GitHub
Configurar os seguintes secrets no repositório:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `GMS_GITHUB_TOKEN_USER`
- `GMS_GITHUB_TOKEN`
- `GEMINI_TOKEN` (se aplicável)

### Local (opcional – desenvolvimento)
- Docker e Docker Compose
- Terraform >= 1.0
- AWS CLI
- Python 3.12+

## 🚀 Como Fazer o Deploy

### 1. Configurar Backend do Terraform

Edite o arquivo `terraform/backend.tf` com seu bucket S3:

```hcl
terraform {
  backend "s3" {
    bucket = "seu-bucket-terraform-state"
    key    = "envs/projeto/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações da aplicação
GEMINI_TOKEN=your_gemini_api_token
GMS_GITHUB_TOKEN=your_github_token
GMS_GITHUB_TOKEN_USER=your_github_username

# Outras variáveis específicas da aplicação
APP_DEBUG=false
APP_PORT=8501
```

### 3. Executar o Deploy

1. Acesse **Actions** no GitHub
2. Selecione **Deploy IaC - Deploy Docker With AWS SSM**
3. Clique em **Run workflow**
4. Escolha a branch (padrão: master)
5. Aguarde a conclusão do pipeline

### 4. Acompanhar o Progresso

O pipeline executa as seguintes etapas:

```mermaid
graph TD
    A[Checkout Code] --> B[Setup AWS CLI]
    B --> C[Setup Terraform]
    C --> D[Terraform Init]
    D --> E[Terraform Plan]
    E --> F[Terraform Apply]
    F --> G[Wait EC2 Ready]
    G --> H[Wait SSM Ready]
    H --> I[Deploy via SSM]
    I --> J[Publish Summary]
```

## 📱 Acessando a Aplicação

Após o deploy bem-sucedido:

1. Verifique o **Job Summary** no GitHub Actions
2. Localize o **IP Público** da EC2
3. Acesse no navegador: `http://SEU_IP_PUBLICO:8501`

## 🔧 Desenvolvimento Local

### Instalação

```bash
# Clonar repositório
git clone <seu-repositorio>
cd projeto-devops-ia

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### Executar Localmente

```bash
# Via Python
streamlit run main.py

# Via Docker
docker compose up --build
```

A aplicação estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
projeto-devops-ia/
├── .github/
│   └── workflows/
│       └── deploy.yml          # Pipeline CI/CD
├── terraform/
│   ├── main.tf                 # Recursos principais
│   ├── variables.tf            # Variáveis
│   ├── outputs.tf              # Outputs
│   └── backend.tf              # Configuração do backend
├── app/
│   ├── main.py                 # Aplicação Streamlit
│   └── requirements.txt        # Dependências Python
├── Dockerfile                  # Imagem Docker
├── docker-compose.yml          # Orquestração
├── .env.example                # Exemplo de variáveis
└── README.md                   # Este arquivo
```

## 🤖 Funcionalidades da Aplicação

O DevOps Mentor não é apenas um chatbot genérico. Ele foi configurado para atuar como um mentor especializado, oferecendo múltiplas personas técnicas com foco em DevOps, Cloud e SRE.

### 🎭 Personas Disponíveis

Na sidebar, o usuário pode escolher a persona desejada:

- **DevOps Expert** → IaC, CI/CD, observabilidade e práticas de cloud
- **FinOps Advisor** → Custos em nuvem (CUR, CUDOS, dashboards, otimização)
- **DevSecOps Specialist** → Segurança em pipelines, secrets management, compliance
- **Cloud Architect Mentor** → Arquitetura de soluções, trade-offs, multi-conta
- **Tech Writer** → Documentação técnica (READMEs, ADRs, diagramas C4)
- **Assistente Geral** → Respostas mais amplas e genéricas

### 💡 Sugestões de Prompts

A interface exibe exemplos prontos de perguntas úteis, variando conforme a persona.

**Exemplo – DevOps Expert:**
- Crie um módulo Terraform para uma VPC com 2 subnets públicas e 2 privadas
- Monte um pipeline GitHub Actions para deploy em EKS
- Explique a diferença entre Transit Gateway e VPC Peering

**Exemplo – FinOps Advisor:**
- Explique como configurar e interpretar um CUR no AWS S3
- Quais práticas FinOps posso aplicar para reduzir custo no EKS?
- Como apresentar savings plans para a diretoria?

### 🚀 Benefícios para Times DevOps

- 📌 **Centralização de conhecimento** → Um único ponto de consulta para DevOps, FinOps e SRE
- ⚡ **Agilidade** → Geração de código IaC, pipelines e documentação em segundos
- 🔒 **Segurança & Governança** → Personas focadas em DevSecOps e FinOps
- 🎯 **Onboarding acelerado** → Prompts prontos ajudam novos membros do time a aprender rapidamente

## 🔒 Segurança

- **Sem SSH direto**: Deploy via AWS SSM Run Command
- **Chaves privadas** armazenadas no AWS Secrets Manager
- **Secrets sensíveis** em GitHub Secrets
- **Firewall** via Security Groups restritivos
- **IAM** com princípio do menor privilégio

## 🐛 Troubleshooting

### Erro: "EC2 instance not ready"
- Aguarde alguns minutos para a instância inicializar
- Verifique se a instância está rodando no console AWS

### Erro: "SSM agent not registered"
- A instância pode levar até 5 minutos para se registrar no SSM
- Verifique o IAM Instance Profile

### Erro: "Application not accessible"
- Confirme se o Security Group permite tráfego na porta 8501
- Verifique se o container está rodando: `docker ps`

### Erro: "Terraform state lock"
Aguarde ou force unlock:
```bash
terraform force-unlock <LOCK_ID>
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 🎯 Roadmap

- [ ] Implementar monitoramento com CloudWatch
- [ ] Adicionar testes automatizados
- [ ] Configurar SSL/HTTPS
- [ ] Implementar backup automatizado
- [ ] Adicionar ambiente de staging
- [ ] Configurar alertas de saúde da aplicação
- [ ] Expandir catálogo de personas com mais especializações

## 📞 Suporte

- Verifique a documentação de deploy
- Consulte as issues existentes
- Abra uma nova issue se necessário

---

Desenvolvido com ❤️ para demonstrar as melhores práticas de DevOps e IA