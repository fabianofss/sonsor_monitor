from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split

CAMINHO_DADOS = Path(__file__).parent / "data" / "sensores.csv"
FEATURES = ["temperatura", "umidade", "vibracao"]
LIMITE_INSPECIONAR = 45
LIMITE_PARAR = 75


st.set_page_config(
    page_title="Projeto CIA@3039",
    page_icon="🛰️",
    layout="wide",
)


@st.cache_data
def carregar_dados():
    return pd.read_csv(CAMINHO_DADOS, parse_dates=["timestamp"])


@st.cache_resource
def treinar_modelo(df):
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        df[FEATURES], df["falha"], test_size=0.25, random_state=42, stratify=df["falha"]
    )
    modelo = RandomForestClassifier(
        n_estimators=200, class_weight="balanced", random_state=42
    )
    modelo.fit(X_treino, y_treino)
    previsoes = modelo.predict(X_teste)
    metricas = {
        "Acurácia": accuracy_score(y_teste, previsoes),
        "Precisão": precision_score(y_teste, previsoes, zero_division=0),
        "Revocação": recall_score(y_teste, previsoes, zero_division=0),
    }
    matriz = confusion_matrix(y_teste, previsoes, labels=[0, 1])
    return modelo, metricas, matriz, len(X_treino), len(X_teste)


def escolher_acao(risco):
    if risco < LIMITE_INSPECIONAR:
        return "Monitorar"
    if risco < LIMITE_PARAR:
        return "Inspecionar"
    return "Parar"


df = carregar_dados()
modelo, metricas, matriz, n_treino, n_teste = treinar_modelo(df)

st.title("Projeto de IA com dados de sensores")
st.caption("Análise de dados simulados de sensores para identificar possíveis falhas.")

aba_dados, aba_modelo, aba_simulacao, aba_etica = st.tabs([
    "Dados dos sensores",
    "Modelo de IA",
    "Simulação",
    "Ética e impactos",
])

with aba_dados:
    st.header("Dados dos sensores")
    normais = int((df["falha"] == 0).sum())
    falhas = int((df["falha"] == 1).sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de registros", len(df))
    c2.metric("Operação normal", normais)
    c3.metric("Falhas", falhas)

    st.subheader("Leituras ao longo do tempo")
    selecionados = st.multiselect("Sensores no gráfico", FEATURES, default=FEATURES)
    if selecionados:
        st.line_chart(df.set_index("timestamp")[selecionados])

    st.subheader("Registros")
    st.dataframe(df, width="stretch")

with aba_modelo:
    st.header("Modelo de IA")
    st.write(
        "Modelo: **Random Forest** (200 árvores, classes balanceadas). Ele prevê `falha` "
        "a partir de temperatura, umidade e vibração. "
        f"Os dados foram divididos em {n_treino} registros de treino (75%) e "
        f"{n_teste} de teste (25%)."
    )
    colunas = st.columns(len(metricas))
    for coluna, (nome, valor) in zip(colunas, metricas.items()):
        coluna.metric(nome, f"{valor:.1%}")

    st.subheader("Matriz de confusão (dados de teste)")
    st.dataframe(
        pd.DataFrame(
            matriz,
            index=["Real: normal", "Real: falha"],
            columns=["Previsto: normal", "Previsto: falha"],
        )
    )
    st.markdown(
        "**Interpretação:** a acurácia mostra o total de acertos, mas as falhas são a "
        "minoria dos registros. Por isso, a **revocação** (quantas falhas reais foram "
        "detectadas) e a **precisão** (quantos alertas eram falhas de verdade) são mais "
        "informativas. Falhas não detectadas aparecem em *Real: falha / Previsto: normal*."
    )

with aba_simulacao:
    st.header("Simulação de uma nova leitura")
    c1, c2, c3 = st.columns(3)
    temperatura = c1.number_input(
        "Temperatura (°C)", value=float(round(df["temperatura"].median(), 1)), step=0.5
    )
    umidade = c2.number_input(
        "Umidade (%)", value=float(round(df["umidade"].median(), 1)), step=0.5
    )
    vibracao = c3.number_input(
        "Vibração (mm/s)", value=float(round(df["vibracao"].median(), 2)), step=0.1
    )

    leitura = pd.DataFrame([[temperatura, umidade, vibracao]], columns=FEATURES)
    previsao = int(modelo.predict(leitura)[0])
    risco = float(modelo.predict_proba(leitura)[0][1]) * 100
    acao = escolher_acao(risco)

    r1, r2, r3 = st.columns(3)
    r1.metric("Previsão", "Falha" if previsao == 1 else "Normal")
    r2.metric("Risco estimado", f"{risco:.0f}%")
    r3.metric("Ação simulada", acao)
    if acao == "Parar":
        st.error("Ação recomendada: Parar o equipamento.")
    elif acao == "Inspecionar":
        st.warning("Ação recomendada: Inspecionar o equipamento.")
    else:
        st.success("Ação recomendada: Monitorar.")

    st.markdown(
        f"""
**Regra da ação** (baseada no risco estimado pelo modelo):

- risco abaixo de {LIMITE_INSPECIONAR}% → **Monitorar**
- de {LIMITE_INSPECIONAR}% a menos de {LIMITE_PARAR}% → **Inspecionar**
- {LIMITE_PARAR}% ou mais → **Parar**

Os limites são intermediários: parar uma máquina tem custo, mas ignorar uma falha
também; a faixa de inspeção cobre os casos duvidosos.
"""
    )

with aba_etica:
    st.header("Ética e impactos")
    riscos = [
        (
            "Dados simulados",
            "O modelo aprendeu com dados fictícios e pode não refletir um equipamento real.",
            "Retreinar e validar com leituras reais antes de qualquer uso operacional.",
        ),
        (
            "Falhas não detectadas",
            "Uma falha real classificada como normal pode causar danos, paradas ou acidentes.",
            "Priorizar a revocação, reduzir o limite de inspeção e manter inspeções periódicas.",
        ),
        (
            "Alarmes falsos",
            "Paradas desnecessárias geram custo e levam a equipe a desconfiar do sistema.",
            "Ajustar os limites com base no custo de cada erro e exigir confirmação humana.",
        ),
        (
            "Mudança nos dados (drift)",
            "Desgaste, clima ou troca de sensores alteram as leituras e degradam o modelo.",
            "Monitorar o desempenho continuamente e retreinar periodicamente.",
        ),
        (
            "Poucos sensores e dados desbalanceados",
            "Só três variáveis e poucas falhas limitam o que o modelo consegue aprender.",
            "Coletar mais variáveis e mais exemplos de falha.",
        ),
    ]
    for titulo, risco_texto, mitigacao in riscos:
        st.subheader(titulo)
        st.write(f"**Risco:** {risco_texto}")
        st.write(f"**Como reduzir:** {mitigacao}")
