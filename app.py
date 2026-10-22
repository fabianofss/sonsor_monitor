import streamlit as st


st.set_page_config(
    page_title="Projeto CIA@3039",
    page_icon="🛰️",
    layout="wide",
)

st.title("Projeto de IA com dados de sensores")
st.caption("Template inicial: complete as abas para desenvolver a atividade.")

aba_dados, aba_modelo, aba_simulacao, aba_etica = st.tabs([
    "Dados dos sensores",
    "Modelo de IA",
    "Simulação",
    "Ética e impactos",
])

with aba_dados:
    st.header("Dados dos sensores")
    st.write("**Sua tarefa:** carregar `data/sensores.csv`, mostrar os registros em uma tabela e criar pelo menos um gráfico.")
    st.info("Implemente esta aba aqui. Mostre também quantos registros indicam operação normal e quantos indicam falha.")

with aba_modelo:
    st.header("Modelo de IA")
    st.write("**Sua tarefa:** treinar um modelo para prever a coluna `falha` usando temperatura, umidade e vibração.")
    st.info("Implemente a separação entre treino e teste. Depois mostre pelo menos duas métricas e explique o que elas significam.")

with aba_simulacao:
    st.header("Simulação de uma nova leitura")
    st.write("**Sua tarefa:** criar campos para informar temperatura, umidade e vibração.")
    st.info("Use o modelo treinado para mostrar a previsão, o risco estimado e uma ação: Monitorar, Inspecionar ou Parar. Explique sua regra.")

with aba_etica:
    st.header("Ética e impactos")
    st.write("**Sua tarefa:** explicar pelo menos três riscos ou limitações do sistema em uma situação real.")
    st.info("Para cada risco, sugira uma forma de reduzir o problema. Escreva as respostas com base no cenário escolhido pelo grupo.")
