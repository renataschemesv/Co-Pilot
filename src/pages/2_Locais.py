import streamlit as st

from src.crud import create_local, delete_local, list_locais, update_local
from src.database import init_db
from src.ui import render_page_feature

init_db()

st.title("CRUD - Locais")
render_page_feature(
    "image-1794396575907.png",
    "Cada lugar deixa uma pista",
    "Organize os espaços do campus para que os objetos encontrados possam ser localizados com mais facilidade.",
    "Gestão de locais",
)

locais = list_locais()
if locais:
    st.dataframe(
        [{"ID": item.id, "Nome": item.nome, "Setor": item.setor or "", "Descrição": item.descricao or "", "Ativo": item.ativo} for item in locais],
        use_container_width=True,
    )
else:
    st.info("Nenhum local cadastrado.")

options = ["Novo local"] + [f"{item.id} - {item.nome}" for item in locais]
selection = st.selectbox("Selecionar registro", options)
selected_id = None
selected = None
if selection != "Novo local":
    selected_id = int(selection.split(" - ")[0])
    selected = next((item for item in locais if item.id == selected_id), None)

with st.form("form_local"):
    nome = st.text_input("Nome", value=selected.nome if selected else "")
    setor = st.text_input("Bloco/Setor", value=selected.setor or "" if selected else "")
    descricao = st.text_area("Descrição", value=selected.descricao or "" if selected else "")
    ativo = st.checkbox("Local ativo", value=selected.ativo if selected else True)

    if selected_id is None:
        submitted = st.form_submit_button("Cadastrar local")
    else:
        submitted = st.form_submit_button("Atualizar local")

    if submitted:
        if selected_id is None:
            create_local(nome, descricao, setor, ativo)
            st.success("Local cadastrado com sucesso!")
        else:
            update_local(selected_id, nome, descricao, setor, ativo)
            st.success("Local atualizado com sucesso!")
        st.rerun()

if selected_id is not None:
    if st.button("Excluir local"):
        delete_local(selected_id)
        st.success("Local removido com sucesso!")
        st.rerun()
