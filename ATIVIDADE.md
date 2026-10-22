# Atividade: IA aplicada a dados de sensores

**Disciplina:** CIA@3039 — Tópicos Especiais em IA e Ciência de Dados  
**Formato:** dupla ou trio

## Desafio

Crie uma aplicação simples em **Python e Streamlit** que use dados de sensores e um modelo de Inteligência Artificial para ajudar alguém a tomar uma decisão.

O tema é amplo: o grupo pode imaginar sensores monitorando uma máquina, uma estufa, um depósito ou outro sistema. Para que todos trabalhem com a mesma base, use o arquivo `data/sensores.csv` fornecido pelo professor. Não é necessário ter sensores, robôs ou equipamentos físicos.

## O que a aplicação deve fazer

Crie uma página Streamlit com estas quatro abas:

### 1. Dados dos sensores

- Carregue `sensores.csv` e mostre os registros em uma tabela.
- Faça pelo menos um gráfico com as leituras.
- Mostre quantos registros indicam operação normal e quantos indicam falha.

### 2. Modelo de IA

- Treine um modelo que tente prever a coluna `falha` usando temperatura, umidade e vibração.
- Separe os dados em treino e teste antes de avaliar o modelo. Reserve aproximadamente 25% para o teste.
- Mostre pelo menos duas métricas, como acurácia, precisão ou revocação.
- Explique em poucas palavras o que os resultados dizem sobre o modelo.

### 3. Teste de uma nova leitura

- Permita que a pessoa informe temperatura, umidade e vibração.
- Use o modelo treinado para mostrar a previsão de falha e o risco estimado, entre 0 e 100%.
- Mostre uma ação simulada: **Monitorar**, **Inspecionar** ou **Parar**.
- Escreva a regra usada para escolher a ação. Como exemplo: risco abaixo de 45% = Monitorar; de 45% a menos de 75% = Inspecionar; 75% ou mais = Parar. O grupo pode propor outros limites, desde que explique a escolha.

### 4. Limites e impactos

- Apresente pelo menos três riscos ou limitações de usar esse modelo em uma situação real.
- Para cada item, sugira uma forma de reduzir o problema.

## Conheça a base de dados

O arquivo fornecido contém leituras **simuladas**. Ele tem estas colunas:

| Coluna | Significado |
| --- | --- |
| `timestamp` | Data e hora simuladas da leitura; pode ser usada no gráfico. |
| `temperatura` | Temperatura do equipamento, em °C. |
| `umidade` | Umidade do ambiente, em %. |
| `vibracao` | Vibração do equipamento, em mm/s. |
| `falha` | Resultado conhecido: `0` = normal; `1` = falha. |

Use temperatura, umidade e vibração como informações para o modelo. Use `falha` como resposta que o modelo deve aprender a prever. Não use a coluna `falha` como entrada do próprio modelo.

## O que entregar

Envie o link de um repositório GitHub do grupo. Ele deve conter:

1. `app.py` — a aplicação Streamlit.
2. `data/sensores.csv` — a base utilizada.
3. `pyproject.toml` e `uv.lock` — configuração do Python e dependências do projeto com uv.
4. `README.md` — instruções para abrir a aplicação, nome do modelo, métricas, regra das ações e limitações.

O template já fixa Python 3.12. Para preparar o ambiente e executar a aplicação, use:

```powershell
uv python install 3.12
uv sync
uv run streamlit run app.py
```

O arquivo `requirements.txt` também pode ser mantido para quem precisar instalar dependências sem uv.

O código pode ficar todo em `app.py` ou ser separado em outros arquivos. O importante é que outra pessoa consiga executar o projeto seguindo o README.

No README, respondam com frases curtas:

- Qual modelo vocês escolheram e por quê?
- Qual métrica foi mais útil para avaliar o resultado? Por quê?
- O que poderia acontecer se o modelo não detectasse uma falha?
- Por que escolheram os limites das ações Monitorar, Inspecionar e Parar?

Escrevam as respostas com base nos resultados que apareceram na aplicação. Ferramentas de IA podem ajudar a programar, mas o grupo deve entender e explicar as escolhas do projeto. Se usarem uma ferramenta de IA, indiquem qual e como ela ajudou.

## Como saber se terminou

- A aplicação abre com `uv run streamlit run app.py`.
- A página usa o CSV fornecido e mostra tabela, gráfico e contagem das classes.
- O modelo é treinado com os dados e avaliado em dados separados para teste.
- Ao alterar os valores dos sensores, a previsão e o risco vêm do modelo treinado.
- As ações e suas regras estão explicadas.
- O README responde às perguntas e apresenta três riscos com formas de reduzi-los.

Não é necessário publicar a aplicação na internet, construir um robô, contratar uma API ou criar um modelo complexo. A avaliação considera se o projeto funciona e se o grupo sabe explicar os resultados e as decisões.

## Avaliação · 100 pontos

| Critério | Pontos |
| --- | ---: |
| Aplicação abre e arquivos estão organizados | 15 |
| Uso do CSV, tabela, gráfico e análise dos dados | 15 |
| Modelo treinado, teste separado e métricas | 25 |
| Teste de novas leituras e ação simulada | 20 |
| Interface clara e fácil de usar | 10 |
| Riscos, limites e formas de reduzi-los | 10 |
| README e explicação das escolhas | 5 |
| **Total** | **100** |
