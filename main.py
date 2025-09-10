# main.py
# ============================================================
# Chatbot Streamlit com Google Gemini
# - Suporte a múltiplas personas para DevOps e Cloud
# - Sugestões de prompts contextuais por persona
# ============================================================

# 1. Imports essenciais
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 2. Configuração da Página
st.set_page_config(
    page_title="DevOps Mentor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 3. Carregamento e Verificação da API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("🔑 API Key não encontrada. Verifique o arquivo .env.")
    st.stop()

# 4. Configuração da API do Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Função para inicializar o modelo Gemini com persona
def init_gemini(system_prompt: str):
    """Inicializa e retorna o modelo GenerativeModel do Gemini com persona."""
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        system_instruction=system_prompt
    )
    return model

# Função para gerar resposta com histórico completo
def generate_response(model, prompt_history):
    try:
        response = model.generate_content(
            [
                {"role": "user", "parts": [m["content"]]} 
                if m["role"] == "user" 
                else {"role": "model", "parts": [m["content"]]}
                for m in prompt_history
            ]
        )
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"


# ========================== UI ===============================

with st.sidebar:
    st.header("⚙️ Configurações")

    # Escolha da persona
    persona = st.radio(
        "Escolha a Persona:",
        [
            "DevOps Expert",
            "FinOps Advisor",
            "DevSecOps Specialist",
            "Cloud Architect Mentor",
            "Tech Writer",
            "Assistente Geral"
        ]
    )

    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("📊 Estatísticas")
    st.metric("Mensagens trocadas", len(st.session_state.get('messages', [])))


# Definir o prompt da persona
if persona == "DevOps Expert":
    system_prompt = """
Você é um especialista em DevOps, SRE e Cloud.
Seu papel é atuar como um **DevOps Expert**, ajudando engenheiros a:
- Criar e revisar IaC (Terraform, Terragrunt, CloudFormation → Terraform).
- Construir pipelines CI/CD (GitHub Actions, GitLab CI/CD, Jenkins).
- Explicar práticas de observabilidade, SLO/SLI/SLA e automação de incidentes.
- Sugerir otimizações de custos e segurança em AWS, Azure e GCP.
- Fornecer exemplos práticos em código, YAML e Bash sempre que possível.
- Responder sempre em português técnico, organizado em tópicos quando fizer sentido.
"""
    example_prompts = [
        "Crie um módulo Terraform para uma VPC com 2 subnets públicas e 2 privadas.",
        "Monte um pipeline GitHub Actions para deploy em EKS.",
        "Explique a diferença entre Transit Gateway e VPC Peering.",
    ]

elif persona == "FinOps Advisor":
    system_prompt = """
Você é um consultor **FinOps** especializado em AWS, Azure e GCP.
Seu papel é ajudar engenheiros e gestores a:
- Interpretar relatórios de custo (CUR, CUDOS, QuickSight, Cost Explorer).
- Sugerir estratégias de otimização (rightsizing, savings plans, spot instances).
- Explicar práticas de governança financeira em nuvem.
- Ajudar na criação de dashboards de custos e recomendações para stakeholders.
"""
    example_prompts = [
        "Explique como configurar e interpretar um CUR no AWS S3.",
        "Quais práticas FinOps posso aplicar para reduzir custo no EKS?",
        "Como apresentar savings plans para a diretoria?",
    ]

elif persona == "DevSecOps Specialist":
    system_prompt = """
Você é um especialista em **DevSecOps**.
Seu papel é ajudar engenheiros a:
- Implementar boas práticas de segurança em pipelines CI/CD.
- Usar ferramentas de análise de vulnerabilidade (Trivy, Grype, Dependabot).
- Configurar secrets management (Vault, SOPS, AWS KMS, Azure Key Vault).
- Criar policies de compliance (CIS, ISO, LGPD).
- Reforçar segurança em Kubernetes, Docker e ambientes cloud.
"""
    example_prompts = [
        "Monte um pipeline CI/CD com análise de vulnerabilidade usando Trivy.",
        "Explique como configurar o SOPS para encriptar secrets em GitOps.",
        "Quais boas práticas aplicar em imagens Docker para reduzir riscos?",
    ]

elif persona == "Cloud Architect Mentor":
    system_prompt = """
Você é um **Cloud Architect Mentor**.
Seu papel é ajudar engenheiros a:
- Projetar arquiteturas escaláveis e seguras em AWS, Azure e GCP.
- Explicar trade-offs entre serviços (EKS vs ECS, Transit Gateway vs Peering, etc.).
- Apoiar estudos para certificações de arquiteto de soluções.
- Revisar diagramas de arquitetura e propor melhorias.
"""
    example_prompts = [
        "Explique quando usar ECS Fargate em vez de EKS.",
        "Qual arquitetura é melhor para um sistema de pagamentos global?",
        "Monte um diagrama de arquitetura multi-conta AWS com Transit Gateway.",
    ]

elif persona == "Tech Writer":
    system_prompt = """
Você é um **Tech Writer** especializado em documentação técnica para DevOps e Cloud.
Seu papel é ajudar engenheiros a:
- Criar READMEs claros e completos para projetos.
- Produzir ADRs (Architecture Decision Records) e documentação C4.
- Escrever tutoriais e guias passo a passo.
- Traduzir documentação entre português e inglês mantendo o tom técnico.
"""
    example_prompts = [
        "Crie um README.md para um projeto Terraform que provisiona EKS.",
        "Escreva um ADR para justificar a adoção de GitHub Actions no lugar do Jenkins.",
        "Monte um guia de onboarding para novos DevOps no time.",
    ]

else:
    system_prompt = """
Você é um assistente geral que ajuda em diversos temas, 
desde dúvidas técnicas até explicações simples.
"""
    example_prompts = [
        "Explique a diferença entre Python e Java.",
        "Me ajude a criar um cronograma de estudos para certificação AWS.",
        "Escreva um e-mail formal para um cliente.",
    ]


# Inicializar o modelo na sessão
if 'model' not in st.session_state or st.session_state.persona != persona:
    with st.spinner("🔄 Inicializando modelo Gemini..."):
        st.session_state.model = init_gemini(system_prompt)
        st.session_state.persona = persona

# Inicializar histórico de mensagens
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Olá! Eu sou seu assistente virtual. Como posso ajudar você hoje?"
    })

# Entrada do usuário
if prompt := st.chat_input("💬 Digite sua mensagem aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("🤔 Pensando..."):
        response = generate_response(st.session_state.model, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

# Exibição do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Exibir exemplos de prompts
st.divider()
st.subheader("💡 Sugestões de Perguntas")
for ex in example_prompts:
    st.markdown(f"- {ex}")
