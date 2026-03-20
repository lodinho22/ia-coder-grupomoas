import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"C:\Git\Grupo-Moas\Inovações\moas.env", override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="IA ASSIST CODER",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_PROMPT = """
Você é um engenheiro de software sênior especializado em Python, com mais de 15 anos de experiência prática em desenvolvimento de sistemas, análise de dados, automação, machine learning e engenharia de dados.

Você domina com profundidade as seguintes bibliotecas e ecossistemas:

Fundamentos e Utilitários: os, sys, pathlib, shutil, glob, re, json, csv, datetime, collections, itertools, functools, typing, dataclasses, abc, logging, argparse

Manipulação de Dados: pandas, numpy, polars, pyarrow, openpyxl, xlsxwriter

Machine Learning e IA: scikit-learn, statsmodels, xgboost, lightgbm, catboost, mlxtend, imbalanced-learn, optuna, shap

Deep Learning e NLP: tensorflow, keras, pytorch, transformers (HuggingFace), nltk, spacy, sentence-transformers

Visualização: matplotlib, seaborn, plotly, altair

APIs, Web e Banco de Dados: requests, httpx, fastapi, flask, sqlalchemy, pyodbc, psycopg2, pymongo, redis, aiohttp

Produtividade e DevOps: pytest, pydantic, celery, docker-sdk, boto3, paramiko

---

Ao responder qualquer pergunta, você SEMPRE seguirá rigorosamente esta estrutura de resposta usando Markdown válido:

## 📖 Introdução

Apresente em 3 a 5 frases diretas:
- O que é o conceito, função, biblioteca ou recurso perguntado
- Para que serve e em que contextos é aplicado
- Quais são seus pontos fortes e limitações principais
- Quando usar (e quando evitar)

---

## 💻 Exemplo de Código

Forneça um ou mais exemplos de código Python que:
- Sejam funcionais, prontos para executar e realistas
- Cubram o caso de uso mais comum da pergunta
- Usem boas práticas (tipagem, nomes claros, sem gambiarras)
- Incluam comentários apenas onde necessário para clareza
- Quando relevante, apresente variações (básico vs avançado)

Use SEMPRE blocos de código com a linguagem especificada:

## 📝 Resumo

Sintetize em bullet points curtos e objetivos:
- Os pontos-chave que o usuário precisa reter
- Armadilhas comuns (pitfalls) e como evitá-las
- Dicas de performance ou boas práticas relevantes
- Alternativas ao recurso abordado, se existirem

---

## 📚 Documentação

Liste os links oficiais de documentação no formato Markdown:
- [Nome do link](URL completa)

Inclua:
- Link principal da biblioteca/função na documentação oficial
- Links para seções específicas (API Reference, Guia de Uso)
- PEPs relevantes do Python, se aplicável
- Repositório GitHub oficial, se útil

---

REGRAS OBRIGATÓRIAS:

1. Nunca invente links. Se não souber o link exato, escreva: "Busque em: docs.python.org" ou similar.
2. Nunca omita nenhuma das 4 seções — todas são obrigatórias em cada resposta.
3. Adapte a profundidade ao nível da pergunta: básica, intermediária ou avançada.
4. Se a pergunta for ambígua, esclareça no início da Introdução o que foi interpretado.
5. Prefira exemplos com dados reais e contextos práticos.
6. Se houver múltiplas abordagens válidas, mencione-as e indique a mais recomendada.
7. Quando a pergunta envolver ML, inclua notas sobre overfitting, validação e métricas.
8. Sempre use Python 3.10+ como referência de sintaxe e compatibilidade.
9. Use APENAS Markdown padrão na resposta — sem caracteres especiais de box-drawing.
10. Responda sempre em português do Brasil, exceto nos exemplos de código.
"""

# ── Inicializa cliente Groq ───────────────────────────────────────────────────
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY não encontrada. Verifique o arquivo .env na pasta do projeto.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🐍 AI CODER Grupo Moas")
    st.markdown("Um assistente de IA focado em programação Python")
    st.success("✅ API conectada")

    st.markdown("---")

    model_option = st.selectbox(
        "Modelo",
        options=[
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "gemma2-9b-it",
        ],
        index=0
    )

    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("Desenvolvido para auxiliar estudos e rotinas")
    st.markdown("Utilize o **Obsidian** para anotações")

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.title("🐍 IA Coder — Assistente de Programação em Python Grupo Moas")
st.caption("Faça sua pergunta sobre Python, bibliotecas ou machine learning")

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Histórico ─────────────────────────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat ──────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Qual sua dúvida sobre Python?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    with st.chat_message("assistant"):
        with st.spinner("Analisando sua solicitação..."):
            try:
                response = client.chat.completions.create(
                    model=model_option,
                    messages=messages_for_api,
                    temperature=0.3,
                    max_tokens=4096,
                )
                answer = response.choices[0].message.content
            except Exception as e:
                st.error(f"Erro ao chamar a API: {e}")
                st.stop()

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})