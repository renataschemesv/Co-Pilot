import streamlit as st

from src.crud import list_categorias, list_locais, list_registros, list_solicitacoes, list_usuarios
from src.database import init_db

st.set_page_config(page_title="EncontraIFC", page_icon="🔎", layout="wide")
init_db()

st.title("EncontraIFC - Sistema de Achados e Perdidos")
st.caption("Gerenciamento de objetos perdidos e encontrados no IFC Campus Blumenau.")

st.markdown(
    """
    O sistema permite registrar objetos perdidos e encontrados, associar categorias e locais, acompanhar solicitações de recuperação e manter o histórico de devolução.
    """
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Categorias", len(list_categorias()))
col2.metric("Locais", len(list_locais()))
col3.metric("Usuários", len(list_usuarios()))
col4.metric("Solicitações", len(list_solicitacoes()))

st.subheader("Resumo geral")
st.markdown("- Categorias: agrupam objetos por tipo, como material escolar e eletrônicos.")
st.markdown("- Locais: representam bibliotecas, salas, cantina, pátio e outros pontos da instituição.")
st.markdown("- Registros: itens perdidos ou encontrados cadastrados no sistema.")
st.markdown("- Solicitações: pedidos de recuperação realizados por usuários autenticados.")

st.info("Use o menu lateral para acessar as páginas de CRUD de cada entidade.")

st.markdown("### Últimos registros")
registros = list_registros()[:3]
if registros:
    for item in registros:
        st.write(f"- {item.tipo}: {item.titulo} | Categoria: {item.categoria.nome} | Local: {item.local.nome}")
else:
    st.write("Ainda não há registros cadastrados.")
