# 1. Imports essenciais
import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 2. Configuração da Página (Aba do Navegador)
# Deve ser o primeiro comando Streamlit do seu script!
st.set_page_config(
    page_title="Chatbot com Google Gemini",  # Título que aparece na aba do navegador
    page_icon="🤖",                          # Ícone da aba do navegador
    layout="wide",                           # Layout amplo ou centralizado
    initial_sidebar_state="expanded"         # Sidebar expandida ou colapsada
)

# 3. Carregamento e Verificação da API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Verificar se a API Key está presente
if not GEMINI_API_KEY:
    st.error("🔑 API Key não encontrada. Verifique o arquivo .env.")
    st.stop()

# 4. Configuração da API do Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Função para INICIALIZAR o modelo com configurações específicas
def init_gemini():
    """Inicializa e retorna o modelo GenerativeModel do Gemini."""
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config
    )
    return model

# Função para gerar resposta do chatbot
def generate_response(model, prompt_history):
    """
    Gera uma resposta do modelo Gemini, com tratamento de erros.
    Usa o histórico para dar mais contexto ao modelo.
    
    Args:
        model: O modelo Gemini inicializado.
        prompt_history: O histórico da conversa.
    
    Returns:
        str: A resposta gerada pelo modelo ou uma mensagem de erro.
    """
    try:
        # Nota: A API do Gemini pode se beneficiar do histórico completo.
        # Por simplicidade aqui, usamos apenas o último prompt, mas o ideal
        # seria enviar o histórico formatado.
        latest_prompt = prompt_history[-1]['content']
        response = model.generate_content(latest_prompt)
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

# --- Interface Gráfica (UI) ---

# Configuração da sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    if st.button("🗑️ Limpar Conversa"):
        # Limpa o estado da sessão
        st.session_state.messages = []
        # Força a re-execução do script para atualizar a UI
        st.rerun()
    
    st.divider()
    st.subheader("📊 Estatísticas")
    # Usa 'st.session_state.get' para evitar erros se a chave não existir
    st.metric("Mensagens trocadas", len(st.session_state.get('messages', [])))


# Inicializar o modelo na sessão se ainda não existir
if 'model' not in st.session_state:
    with st.spinner("🔄 Inicializando modelo Gemini..."):
        st.session_state.model = init_gemini()

# Título e descrição principal
st.title("🤖 Chatbot com Google Gemini")
st.write("Bem-vindo ao seu assistente virtual inteligente!")

# Personalização com CSS (opcional)
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# =================== LÓGICA DE CHAT CORRIGIDA ===================================
# ==============================================================================

# 1. Inicializa o histórico de mensagens na sessão se for a primeira execução
if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Adiciona uma mensagem de boas-vindas inicial do assistente
    st.session_state.messages.append({
        "role": "assistant",
        "content": """👋 Olá! Eu sou seu assistente virtual powered by Google Gemini. 

Posso ajudar você com:
- ❓ Responder perguntas gerais
- 💻 Explicar conceitos de programação
- 📝 Criar e revisar textos
- 🧮 Resolver problemas matemáticos
- 🎨 Ideias criativas

Como posso ajudar você hoje?"""
    })

# 2. LÓGICA DE PROCESSAMENTO (SEMPRE ANTES DA EXIBIÇÃO)
# Captura a entrada do usuário a partir da caixa de texto
if prompt := st.chat_input("💬 Digite sua mensagem aqui..."):
    # Adiciona a mensagem do usuário ao histórico de estado
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Gera a resposta do assistente
    with st.spinner("🤔 Pensando..."):
        # Passa o histórico para a função de geração para dar contexto
        response = generate_response(st.session_state.model, st.session_state.messages)
        # Adiciona a resposta do assistente ao histórico de estado
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Força um rerun para exibir a nova mensagem imediatamente
        st.rerun()


# 3. LÓGICA DE EXIBIÇÃO (SEMPRE POR ÚLTIMO)
# Exibe cada mensagem guardada no histórico de estado
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])