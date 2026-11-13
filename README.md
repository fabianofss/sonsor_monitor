# Monitor de sensores com IA

Aplicação em Python com Streamlit para analisar dados simulados de sensores e ajudar a identificar possíveis falhas.

## Como executar

```powershell
uv python install 3.12
uv sync
uv run streamlit run app.py
```

Sem uv: `pip install -r requirements.txt`
e depois `streamlit run app.py`.

## Abas

1. **Dados dos sensores**: tabela (com filtro), gráficos (série temporal, médias por situação, dispersão) e contagem de leituras normais (645) e com falha (155).
2. **Modelo de IA**: treino, métricas, matriz de confusão e influência de cada variável.
3. **Nova leitura**: entrada dos três sensores, previsão, risco (0–100%) e ação sugerida.
4. **Limitações e cuidados**: cinco riscos, cada um com forma de reduzi-lo.

## Modelo e métricas

Modelo: **Regressão Logística** (variáveis padronizadas, `class_weight="balanced"`). 
Divisão: 75% treino (600) e 25% teste (200), estratificada, `random_state=42`.

| Métrica (teste) | Valor |
| --- | ---: |
| Acurácia | 83,0% |
| Precisão | 54,9% |
| Revocação | 71,8% |
| F1 | 62,2% |
| AUC | 0,871 |

## Perguntas da atividade

**Qual modelo escolhemos e por quê?**
Regressão Logística.
Experiencia adquirida em atividades anteriores.
E em validação cruzada ela supera a Random Forest em revocação, além de ser simples e de entregar uma probabilidade, que serve como risco.

**Qual métrica foi mais útil?**
A revocação, porque só 19% das leituras são falhas e a acurácia sozinha engana podendo have um falso positivo.
A revocação mostra quantas falhas reais foram encontradas.

**O que pode acontecer se o modelo não detectar uma falha?**
O equipamento continua operando com defeito, o que pode causar dano, parada não planejada e risco de segurança.
No teste, cerca de 28% das falhas passam despercebidas.

**Por que esses limites de ação?**
Monitorar abaixo de 45%, Inspecionar de 45% a menos de 75%, Parar a partir de 75%.
Inspecionar é opção mais barata e gera menores impactos, então o limite é baixo para perder poucas falhas.
Parar tem custo alto, então só ocorre com risco muito elevado.
Os valores são propostos pelo grupo e não foram otimizados com custos reais.

## Limitações

1. **Dados simulados**: o modelo pode não funcionar ou gerar falso positivo em equipamento real. Reduzir: validar com dados reais e histórico de manutenção.
2. **Falhas não detectadas**: a revocação de 71,8% deixa falhas passarem. Reduzir: apesar da recomentação do monitor sugerimos manter inspeções periódicas e baixar o limite de alerta.
3. **Alarmes falsos**: a precisão de 54,9% gera inspeções desnecessárias. Reduzir: ajustar limites conforme custos e realidade e exigir confirmação humana antes de parar.
4. **Poucas variáveis e poucos dados**: só 3 sensores e 800 registros. Reduzir: incluir mais variáveis e histórico, comparar modelos.
5. **Entradas fora do padrão**: a aplicação avisa quando um valor sai da faixa do treino.

## Arquivos

- `app.py`: aplicação Streamlit.
- `data/sensores.csv`: base de dados simulada.
- `pyproject.toml` e `uv.lock`: ambiente com uv.
- `requirements.txt`: instalação alternativa com pip.
