import streamlit as st

from src.crud import create_categoria, delete_categoria, list_categorias, update_categoria
from src.database import init_db

init_db()

st.title("CRUD - Categorias")

categorias = list_categorias()
if categorias:
    st.dataframe(
        [{"ID": item.id, "Nome": item.nome, "Descrição": item.descricao or "", "Ativa": item.ativa} for item in categorias],
        use_container_width=True,
    )
else:
    st.info("Nenhuma categoria cadastrada.")

options = ["Nova categoria"] + [f"{item.id} - {item.nome}" for item in categorias]
selection = st.selectbox("Selecionar registro", options)
selected_id = None
selected = None
if selection != "Nova categoria":
    selected_id = int(selection.split(" - ")[0])
    selected = next((item for item in categorias if item.id == selected_id), None)

with st.form("form_categoria"):
    nome = st.text_input("Nome", value=selected.nome if selected else "")
    descricao = st.text_area("Descrição", value=selected.descricao or "" if selected else "")
    ativa = st.checkbox("Categoria ativa", value=selected.ativa if selected else True)

    if selected_id is None:
        submitted = st.form_submit_button("Cadastrar categoria")
    else:
        submitted = st.form_submit_button("Atualizar categoria")

    if submitted:
        if selected_id is None:
            create_categoria(nome, descricao, ativa)
            st.success("Categoria cadastrada com sucesso!")
        else:
            update_categoria(selected_id, nome, descricao, ativa)
            st.success("Categoria atualizada com sucesso!")
        st.rerun()

if selected_id is not None:
    if st.button("Excluir categoria"):
        delete_categoria(selected_id)
        st.success("Categoria removida com sucesso!")
        st.rerun()
