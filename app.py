from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

CSV = Path(__file__).parent / "data" / "sensores.csv"
FEATURES = ["temperatura", "umidade", "vibracao"]
ROTULOS = {
    "temperatura": "Temperatura (°C)",
    "umidade": "Umidade (%)",
    "vibracao": "Vibração (mm/s)",
}
LIMITE_INSPECIONAR = 45  # risco (%) a partir do qual se inspeciona
LIMITE_PARAR = 75  # risco (%) a partir do qual se para o equipamento

st.set_page_config(page_title="Monitor de sensores", page_icon="🛰️", layout="wide")


@st.cache_data
def carregar_dados() -> pd.DataFrame:
    return pd.read_csv(CSV, parse_dates=["timestamp"])


@st.cache_resource
def treinar(df: pd.DataFrame):
    X_treino, X_teste, y_treino, y_teste = train_test_split(
        df[FEATURES], df["falha"], test_size=0.25, random_state=42, stratify=df["falha"]
    )
    modelo = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", random_state=42),
    )
    modelo.fit(X_treino, y_treino)
    previsao = modelo.predict(X_teste)
    proba = modelo.predict_proba(X_teste)[:, 1]
    metricas = {
        "Acurácia": accuracy_score(y_teste, previsao),
        "Precisão": precision_score(y_teste, previsao),
        "Revocação": recall_score(y_teste, previsao),
        "F1": f1_score(y_teste, previsao),
        "AUC": roc_auc_score(y_teste, proba),
    }
    return modelo, metricas, confusion_matrix(y_teste, previsao), len(X_treino), len(X_teste)


def acao_para_risco(risco: float) -> tuple[str, str]:
    if risco >= LIMITE_PARAR:
        return "Parar", "error"
    if risco >= LIMITE_INSPECIONAR:
        return "Inspecionar", "warning"
    return "Monitorar", "success"


df = carregar_dados()
modelo, metricas, matriz, n_treino, n_teste = treinar(df)

st.title("🛰️ Análise de sensores com IA")
st.caption("Dados simulados de um equipamento: temperatura, umidade e vibração.")

aba_dados, aba_modelo, aba_leitura, aba_limites = st.tabs(
    ["Dados dos sensores", "Modelo de IA", "Nova leitura", "Limitações e cuidados"]
)

# ---------------------------------------------------------------- Aba 1
with aba_dados:
    st.header("Dados dos sensores")
    total = len(df)
    falhas = int(df["falha"].sum())
    c1, c2, c3 = st.columns(3)
    c1.metric("Leituras no total", total)
    c2.metric("Operação normal", total - falhas, f"{(total - falhas) / total:.1%}", delta_color="off")
    c3.metric("Falhas", falhas, f"{falhas / total:.1%}", delta_color="off")

    st.subheader("Leituras ao longo do tempo")
    variavel = st.selectbox("Variável", FEATURES, format_func=ROTULOS.get)
    serie = df.set_index("timestamp")[[variavel]].rename(columns={variavel: ROTULOS[variavel]})
    st.line_chart(serie)
    st.caption(f"Primeira leitura: {df['timestamp'].min():%d/%m/%Y %H:%M} · última: {df['timestamp'].max():%d/%m/%Y %H:%M}")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Média por situação")
        medias = df.assign(situação=df["falha"].map({0: "Normal", 1: "Falha"})).groupby("situação")[FEATURES].mean()
        st.bar_chart(medias.rename(columns=ROTULOS).T)
        st.caption("Leituras com falha tendem a ter temperatura e vibração mais altas.")
    with col_b:
        st.subheader("Temperatura × vibração")
        dispersao = df.assign(situação=df["falha"].map({0: "Normal", 1: "Falha"}))
        st.scatter_chart(dispersao, x="vibracao", y="temperatura", color="situação")

    st.subheader("Tabela de registros")
    filtro = st.radio("Mostrar", ["Todos", "Normais", "Falhas"], horizontal=True)
    visivel = df if filtro == "Todos" else df[df["falha"] == (filtro == "Falhas")]
    st.dataframe(visivel, width="stretch", hide_index=True)

# ---------------------------------------------------------------- Aba 2
with aba_modelo:
    st.header("Modelo de IA")
    st.write(
        f"**Modelo:** Regressão Logística (com padronização das variáveis e `class_weight='balanced'`). "
        f"Os dados foram divididos em **{n_treino} leituras de treino (75%)** e **{n_teste} de teste (25%)**, "
        "mantendo a proporção de falhas nos dois grupos. As métricas abaixo vêm só do conjunto de teste."
    )
    cols = st.columns(len(metricas))
    for col, (nome, valor) in zip(cols, metricas.items()):
        col.metric(nome, f"{valor:.1%}" if nome != "AUC" else f"{valor:.3f}")

    col_m, col_t = st.columns([1, 1.4])
    with col_m:
        st.subheader("Matriz de confusão")
        tabela = pd.DataFrame(
            matriz,
            index=["Real: normal", "Real: falha"],
            columns=["Previsto: normal", "Previsto: falha"],
        )
        st.dataframe(tabela)
        vn, fp, fn, vp = matriz.ravel()
        st.caption(f"{vp} falhas detectadas, {fn} falhas perdidas, {fp} alarmes falsos.")
    with col_t:
        st.subheader("O que os resultados dizem")
        st.markdown(
            f"""
- **Acurácia ({metricas['Acurácia']:.1%})**: proporção de previsões corretas. Sozinha engana, pois só
  {falhas / total:.0%} dos registros são falhas: um modelo que sempre dissesse "normal" já acertaria ~{1 - falhas / total:.0%}.
- **Revocação ({metricas['Revocação']:.1%})**: das falhas reais, quantas o modelo encontrou. É a métrica mais importante aqui,
  porque uma falha não detectada pode danificar o equipamento.
- **Precisão ({metricas['Precisão']:.1%})**: dos alertas de falha, quantos eram falhas de verdade. Valor baixo significa
  muitos alarmes falsos (inspeções desnecessárias) — o preço de priorizar a revocação.
- **AUC ({metricas['AUC']:.3f})**: capacidade de separar falhas de leituras normais em qualquer limite de risco.
"""
        )

    coef = pd.Series(modelo[-1].coef_[0], index=[ROTULOS[f] for f in FEATURES]).sort_values()
    st.subheader("Influência de cada variável")
    st.bar_chart(coef)
    st.caption("Coeficientes da regressão (variáveis padronizadas): valores positivos aumentam o risco de falha.")

# ---------------------------------------------------------------- Aba 3
with aba_leitura:
    st.header("Teste de uma nova leitura")
    medias_gerais = df[FEATURES].mean()
    c1, c2, c3 = st.columns(3)
    temperatura = c1.number_input(
        ROTULOS["temperatura"], 0.0, 150.0, round(float(medias_gerais["temperatura"]), 1), 0.5
    )
    umidade = c2.number_input(
        ROTULOS["umidade"], 0.0, 100.0, round(float(medias_gerais["umidade"]), 1), 0.5
    )
    vibracao = c3.number_input(
        ROTULOS["vibracao"], 0.0, 30.0, round(float(medias_gerais["vibracao"]), 1), 0.1
    )

    leitura = pd.DataFrame([[temperatura, umidade, vibracao]], columns=FEATURES)
    risco = float(modelo.predict_proba(leitura)[0, 1]) * 100
    acao, nivel = acao_para_risco(risco)

    fora = [
        ROTULOS[f]
        for f in FEATURES
        if not df[f].min() <= leitura[f].iloc[0] <= df[f].max()
    ]
    if fora:
        st.warning(
            "Valor fora da faixa vista no treino (" + ", ".join(fora) + "). "
            "A previsão pode não ser confiável."
        )

    r1, r2 = st.columns(2)
    r1.metric("Previsão", "Falha" if risco >= 50 else "Normal")
    r2.metric("Risco estimado de falha", f"{risco:.1f}%")
    st.progress(min(int(round(risco)), 100))
    getattr(st, nivel)(f"Ação sugerida: **{acao}**")

    st.markdown(
        f"""
**Regra usada para a ação**

| Risco estimado | Ação |
| --- | --- |
| abaixo de {LIMITE_INSPECIONAR}% | Monitorar |
| de {LIMITE_INSPECIONAR}% a menos de {LIMITE_PARAR}% | Inspecionar |
| {LIMITE_PARAR}% ou mais | Parar |

A previsão é "Falha" quando o risco chega a 50%. O modelo foi treinado com pesos balanceados,
então o risco tende a ser alto em leituras limítrofes; por isso 45% já pede inspeção
(prioriza não perder falhas) e só se para o equipamento com 75% ou mais, pois parar tem custo alto.
"""
    )

# ---------------------------------------------------------------- Aba 4
with aba_limites:
    st.header("Limitações e cuidados")
    st.write("Antes de tomar qualquer decisão com este modelo, considere:")
    riscos = [
        (
            "Dados simulados",
            "O modelo aprendeu com leituras artificiais, não de um equipamento real. Em campo, ruído, "
            "desgaste e sensores descalibrados mudam o comportamento.",
            "Retreinar e validar com dados reais do equipamento antes de usar; comparar previsões com "
            "o histórico de manutenção.",
        ),
        (
            "Falhas não detectadas (falsos negativos)",
            f"A revocação no teste é {metricas['Revocação']:.1%}: parte das falhas passa despercebida, "
            "e uma falha ignorada pode causar parada não planejada ou dano.",
            "Não depender só do modelo: manter inspeções periódicas e alarmes físicos; "
            "baixar o limite de alerta se o custo de perder uma falha for alto.",
        ),
        (
            "Alarmes falsos (baixa precisão)",
            f"Com precisão de {metricas['Precisão']:.1%}, muitos alertas não são falhas reais, "
            "gerando inspeções desnecessárias e perda de confiança na ferramenta.",
            "Ajustar os limites de ação conforme o custo de inspecionar versus parar; "
            "exigir confirmação humana antes de parar o equipamento.",
        ),
        (
            "Poucas variáveis e dados limitados",
            f"Só 3 sensores e {total} registros, com {falhas} falhas. Causas fora desses sensores "
            "(energia, lubrificação, idade da peça) não são vistas, e o modelo linear é simples.",
            "Incluir mais variáveis e mais histórico; comparar com outros modelos; "
            "monitorar a qualidade das previsões ao longo do tempo.",
        ),
        (
            "Valores fora do padrão de treino",
            "Leituras muito diferentes das vistas no treino geram previsões sem garantia.",
            "Avisar quando a entrada sair da faixa conhecida (a aba Nova leitura faz isso) "
            "e tratar esses casos manualmente.",
        ),
    ]
    for titulo, problema, mitigacao in riscos:
        with st.container(border=True):
            st.subheader(titulo)
            st.markdown(f"**Risco:** {problema}")
            st.markdown(f"**Como reduzir:** {mitigacao}")
    st.info("O modelo é um apoio à decisão: a decisão final de parar um equipamento deve ser de uma pessoa responsável.")
