import streamlit as st

from src.crud import list_categorias, list_locais, list_registros, list_solicitacoes, list_usuarios
from src.database import init_db
from src.ui import render_page_feature

st.set_page_config(page_title="EncontraIFC", page_icon="🔎", layout="wide")
init_db()

st.markdown(
    """
    <style>
    [data-testid="stHeader"] {
        background: transparent;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    [data-testid="stMetric"] {
        min-height: 126px;
        padding: 1rem 1.15rem;
        border: 1px solid #d5e5f3;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 5px 16px rgba(29, 78, 121, 0.06);
    }
    [data-testid="stMetricLabel"] {
        color: #496882;
    }
    [data-testid="stMetricValue"] {
        color: #155b91;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #d5e5f3;
        background: rgba(255, 255, 255, 0.8);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Painel de achados e perdidos")
st.caption("IFC Campus Blumenau")
render_page_feature(
    "image-1794396498156.png",
    "Tudo sobre achados e perdidos, em um só lugar",
    "Acompanhe objetos cadastrados, organize categorias e locais e consulte solicitações de recuperação.",
    "EncontraIFC · IFC Campus Blumenau",
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Categorias", len(list_categorias()))
col2.metric("Locais", len(list_locais()))
col3.metric("Usuários", len(list_usuarios()))
col4.metric("Solicitações", len(list_solicitacoes()))

st.subheader("Visão geral")
summary_cols = st.columns(4)
summary_items = [
    ("Categorias", "Organize itens por tipo, como material escolar e eletrônicos."),
    ("Locais", "Encontre objetos em salas, biblioteca, cantina e outros espaços."),
    ("Registros", "Consulte itens perdidos ou encontrados na instituição."),
    ("Solicitações", "Acompanhe pedidos de recuperação de objetos."),
]
for column, (title, description) in zip(summary_cols, summary_items):
    with column:
        st.markdown(f"**{title}**")
        st.caption(description)

st.info("Acesse as áreas de cadastro pelo menu lateral.", icon="ℹ️")

st.subheader("Últimos registros")
registros = list_registros()[:3]
if registros:
    for item in registros:
        with st.container(border=True):
            st.markdown(f"**{item.titulo}** · {item.tipo.capitalize()}")
            st.caption(f"{item.categoria.nome}  ·  {item.local.nome}")
else:
    st.write("Ainda não há registros cadastrados.")
