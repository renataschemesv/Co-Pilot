import streamlit as st

from src.crud import create_usuario, delete_usuario, list_usuarios, update_usuario
from src.database import init_db

init_db()

st.title("CRUD - Usuários")

usuarios = list_usuarios()
if usuarios:
    st.dataframe(
        [{"ID": item.id, "Nome": item.nome, "Email": item.email, "Vínculo": item.vinculo, "Situação": item.situacao, "Responsável": item.perm_responsavel, "Admin": item.perm_admin} for item in usuarios],
        use_container_width=True,
    )
else:
    st.info("Nenhum usuário cadastrado.")

options = ["Novo usuário"] + [f"{item.id} - {item.nome}" for item in usuarios]
selection = st.selectbox("Selecionar registro", options)
selected_id = None
selected = None
if selection != "Novo usuário":
    selected_id = int(selection.split(" - ")[0])
    selected = next((item for item in usuarios if item.id == selected_id), None)

with st.form("form_usuario"):
    nome = st.text_input("Nome", value=selected.nome if selected else "")
    email = st.text_input("Email", value=selected.email if selected else "")
    senha = st.text_input("Senha", type="password", value="")
    vinculo = st.selectbox("Vínculo", ["aluno", "servidor"], index=["aluno", "servidor"].index(selected.vinculo) if selected else 0)
    email_verificado = st.checkbox("Email verificado", value=selected.email_verificado if selected else False)
    situacao = st.selectbox("Situação", ["pendente", "ativa", "inativa"], index=["pendente", "ativa", "inativa"].index(selected.situacao) if selected else 0)
    perm_responsavel = st.checkbox("Permissão de responsável", value=selected.perm_responsavel if selected else False)
    perm_admin = st.checkbox("Permissão administrativa", value=selected.perm_admin if selected else False)

    if selected_id is None:
        submitted = st.form_submit_button("Cadastrar usuário")
    else:
        submitted = st.form_submit_button("Atualizar usuário")

    if submitted:
        if selected_id is None:
            create_usuario(nome, email, senha, vinculo, email_verificado, situacao, perm_responsavel, perm_admin)
            st.success("Usuário cadastrado com sucesso!")
        else:
            update_usuario(selected_id, nome, email, senha or None, vinculo, email_verificado, situacao, perm_responsavel, perm_admin)
            st.success("Usuário atualizado com sucesso!")
        st.rerun()

if selected_id is not None:
    if st.button("Excluir usuário"):
        delete_usuario(selected_id)
        st.success("Usuário removido com sucesso!")
        st.rerun()
