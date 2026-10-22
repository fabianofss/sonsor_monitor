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

O template não contém o modelo treinado nem as visualizações prontas. O grupo deve implementar essas partes, testar a aplicação e explicar as decisões no README.
