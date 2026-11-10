# EncontraIFC

Este projeto é uma aplicação web em Streamlit para o gerenciamento de objetos perdidos e encontrados no IFC Campus Blumenau.

## Objetivo

O sistema permite:

- cadastrar categorias de objetos;
- registrar locais da instituição;
- manter usuários com vínculo institucional;
- cadastrar registros de objetos perdidos e encontrados;
- acompanhar solicitações de recuperação;
- usar SQLite em ambiente local e MySQL em produção.

## Tecnologias

- Streamlit
- SQLAlchemy
- SQLite
- MySQL + PyMySQL
- uv
- variáveis de ambiente

## Estrutura do projeto

```text
.
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── src/
    ├── app.py
    ├── config.py
    ├── crud.py
    ├── database.py
    ├── models.py
    ├── __init__.py
    └── pages/
        ├── 1_Categorias.py
        ├── 2_Locais.py
        ├── 3_Usuarios.py
        ├── 4_Registros.py
        └── 5_Solicitacoes.py
```

## Requisitos

- Python 3.11+
- uv

## Configuração inicial

1. Instale as dependências:

```bash
uv sync
```

2. Crie o arquivo de ambiente:

```bash
cp .env.example .env
```

3. Ajuste as configurações para produção, caso necessário:

```env
APP_ENV=production
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
MYSQL_DB=ifc_achados_perdidos
```

Se `APP_ENV` estiver como `development`, o sistema usa SQLite local (`ifc_achados_perdidos.db`).

## Execução

```bash
uv run streamlit run src/app.py
```

Acesse: http://localhost:8501

## Observações

- SQLite é usado para testes locais.
- MySQL é usado em ambiente de produção.
- As credenciais do banco ficam em variáveis de ambiente.
- O sistema foi construído conforme o contexto de achados e perdidos do IFC.
