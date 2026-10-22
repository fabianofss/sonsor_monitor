# Template inicial — Projeto CIA@3039

Este repositório é o ponto de partida da atividade. O `app.py` já cria as quatro abas do Streamlit, mas deixa as análises para o grupo implementar.

Leia primeiro o [enunciado da atividade](ATIVIDADE.md). Use `data/sensores.csv` e complete as tarefas indicadas em cada aba.

## Ambiente Python com uv

O projeto fixa Python 3.12 em `.python-version` e declara as dependências em `pyproject.toml`. Com o [uv instalado](https://docs.astral.sh/uv/getting-started/installation/), execute na pasta do repositório:

```powershell
uv python install 3.12
uv sync
uv run streamlit run app.py
```

`uv sync` cria o ambiente `.venv` do projeto e instala as versões registradas em `uv.lock`. O `requirements.txt` fica disponível para ambientes que não usam uv.

## Arquivos

- `app.py`: página inicial com as quatro abas e orientações sobre o que implementar.
- `ATIVIDADE.md`: enunciado, entregáveis e critérios de avaliação.
- `data/sensores.csv`: leituras simuladas para usar no projeto.
- `pyproject.toml` e `uv.lock`: versão do Python e dependências do ambiente uv.
- `requirements.txt`: dependências para instalação alternativa com pip.

## Modelo, métricas e decisões

- **Modelo:** Random Forest (`scikit-learn`, 200 árvores, `class_weight="balanced"`). Funciona bem com poucas variáveis, não exige normalização e estima probabilidades usadas como risco.
- **Divisão:** 75% treino / 25% teste (estratificada, `random_state=42`).
- **Métricas no teste:** acurácia ≈ 84,5%, precisão ≈ 59,1%, revocação ≈ 66,7%.
- **Métrica mais útil:** a revocação, pois as falhas são minoria (~19%) e a acurácia sozinha esconde falhas não detectadas.
- **Se uma falha não for detectada:** o equipamento continua operando e pode sofrer danos, paradas não planejadas ou riscos de segurança.
- **Regra das ações (risco estimado):** abaixo de 45% = Monitorar; de 45% a menos de 75% = Inspecionar; 75% ou mais = Parar. Os limites são um meio-termo entre o custo de parar sem necessidade e o de ignorar uma falha.

## Limitações e como reduzi-las

1. **Dados simulados:** podem não refletir a realidade → validar e retreinar com dados reais.
2. **Falhas não detectadas / alarmes falsos:** a revocação é de ~67% → ajustar limites conforme o custo dos erros e manter revisão humana.
3. **Mudança nos dados (drift) e poucas variáveis:** o desempenho pode cair com o tempo → monitorar e retreinar periodicamente, coletar mais sensores.
